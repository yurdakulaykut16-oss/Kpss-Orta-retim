"""Sunucuda atomik, profil bazında tekrar engeli ve havuz ayrımı."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import app as server
from kpss_kapsam import question_key


class SoruAyirmaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cache=server.her_seyi_yukle()
        cls.index={sid:s for rows in cls.cache['soru_index'].values() for sid,s in rows.items()}
        cls.exams=cls.cache['denemeler']['denemeler']
        reserved={sid for d in cls.exams for sid in d['sorular']}
        roots={question_key(cls.index[i]) for i in reserved}
        cls.fresh=[sid for sid,s in cls.index.items() if sid not in reserved and question_key(s) not in roots]

    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        patcher=patch.object(server,'ILERLEME',Path(tmp.name));patcher.start();self.addCleanup(patcher.stop)
        self.client=server.app.test_client()
        # Başka testin zorunlu cache yenilemesi bu atomik işlem testini etkilemez.
        cachepatch=patch.object(server,'her_seyi_yukle',return_value=self.cache)
        cachepatch.start();self.addCleanup(cachepatch.stop)

    def claim(self, ids, **kwargs):
        return self.client.post('/api/soru-ayir/test',json=dict(tur='test',oturum='test-oturum',ids=ids,**kwargs))

    def test_ayni_soru_ikinci_oturuma_verilemez(self):
        self.assertEqual(self.claim(self.fresh[:2]).status_code,200)
        self.assertEqual(self.claim(self.fresh[:2]).status_code,409)
        self.assertEqual(len(server.ilerleme_oku('test')['ayrilan_sorular']),2)

    def test_kayit_cevap_verilmeden_olusur(self):
        self.claim(self.fresh[:1])
        data=server.ilerleme_oku('test')
        self.assertIn(self.fresh[0],data['ayrilan_sorular'])
        self.assertFalse(data.get('soru_kayit'))

    def test_bir_cakisma_butun_ayirmayi_reddeder(self):
        a,b=self.fresh[:2];self.claim([a])
        self.assertEqual(self.claim([a,b]).status_code,409)
        self.assertNotIn(b,server.ilerleme_oku('test')['ayrilan_sorular'])

    def test_gun_degisse_de_kullanim_kalir(self):
        self.claim(self.fresh[:1])
        self.client.post('/api/ilerleme/test',json={'gunluk':{'tarih':'2099-01-01','ids':{}},'ayrilan_sorular':{}})
        self.assertEqual(self.claim(self.fresh[:1]).status_code,409)

    def test_eski_cozum_kaydi_da_engeller(self):
        sid=self.fresh[0]
        server.ilerleme_yaz('test',{'soru_kayit':{sid:{'d':0,'y':0,'son':123}}})
        self.assertEqual(self.claim([sid]).status_code,409)

    def test_eski_yedek_legacy_cozum_gecmisini_silemez(self):
        sid=self.fresh[0]
        server.ilerleme_yaz('test',{'soru_kayit':{sid:{'d':1,'y':0,'son':123}}})
        server.ilerleme_yaz('test',{})
        self.assertEqual(self.claim([sid]).status_code,409)

    def test_denemeye_ayrilan_testte_verilemez(self):
        self.assertEqual(self.claim(self.exams[0]['sorular'][:1]).status_code,409)

    def test_tum_denemeler_ayri_ve_dagilim_korunur(self):
        all_ids=[]
        for d in self.exams:
            r=self.client.post('/api/soru-ayir/test',json={'tur':'deneme','oturum':d['id'],'deneme_id':d['id'],'ids':d['sorular']})
            self.assertEqual(r.status_code,200,r.get_json())
            all_ids.extend(d['sorular'])
        self.assertEqual(len(all_ids),220)
        self.assertEqual(len(set(all_ids)),220)
        self.assertEqual(len(server.ilerleme_oku('test')['ayrilan_sorular']),220)

    def test_denemeye_baska_dersle_doldurma_yok(self):
        d=self.exams[0]
        self.assertEqual(self.client.post('/api/soru-ayir/test',json={'tur':'deneme','oturum':'deneme','deneme_id':d['id'],'ids':self.fresh[:d['soru_sayisi']]}).status_code,400)

    def test_baska_denemeye_ayrilan_soru_alinamaz(self):
        d,e=self.exams[:2];ids=list(d['sorular'])
        pair=next((i,sid) for i,a in enumerate(ids) for sid in e['sorular'] if self.index[a]['ders']==self.index[sid]['ders'])
        ids[pair[0]]=pair[1]
        r=self.client.post('/api/soru-ayir/test',json={'tur':'deneme','oturum':'deneme','deneme_id':d['id'],'ids':ids})
        self.assertEqual(r.status_code,409)

    def test_kapsam_disi_ve_gecersiz_istek_reddedilir(self):
        for ids in (['GUN-0002'],['YOK'],[],[self.fresh[0],self.fresh[0]]):
            self.assertEqual(self.claim(ids).status_code,400)
        self.assertEqual(self.client.post('/api/soru-ayir/test',json=[]).status_code,400)

    def test_iki_eszamanli_istekten_yalniz_biri_ayirabilir(self):
        def request(_):
            with server.app.test_client() as c:
                return c.post('/api/soru-ayir/test',json={'tur':'test','oturum':'paralel','ids':self.fresh[:1]}).status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sorted(pool.map(request,range(2))),[200,409])

    def test_farkli_numara_ve_sik_sirasi_ayni_koku_yeni_yapmaz(self):
        a=dict(id='A',ders='guncel',kok='  İki,  kurum! ',siklar=['a','b','c','d','e'])
        b=dict(a,id='B',kok='iki kurum',siklar=list(reversed(a['siklar'])))
        fake=dict(soru_index={'guncel':{'A':a,'B':b}},denemeler={'denemeler':[]})
        with patch.object(server,'her_seyi_yukle',return_value=fake):
            self.assertEqual(self.claim(['A']).status_code,200)
            self.assertEqual(self.claim(['B']).status_code,409)

    def test_profillerin_kullanim_kaydi_ayri(self):
        self.claim(self.fresh[:1])
        r=self.client.post('/api/soru-ayir/baska',json={'tur':'test','oturum':'baska','ids':self.fresh[:1]})
        self.assertEqual(r.status_code,200)
