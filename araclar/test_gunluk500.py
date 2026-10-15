"""Deneme hariç 5×500 test hedefi, gerçek kapasite ve editoryal ek aktarımı."""
import collections
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import app as server
from calisma_hedefi import load_target, summarize
from ek_gunluk500 import build, add_to_bank
from kpss_kapsam import record_hash, question_key

ROOT=Path(__file__).resolve().parent.parent


class Gunluk500Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records,cls.topics=build(ROOT)
        cls.cache=server.her_seyi_yukle()
        cls.index={s['id']:s for rows in cls.cache['sorular'].values() for s in rows}
        cls.exams=cls.cache['denemeler']['denemeler']
        cls.reserved={sid for e in cls.exams for sid in e['sorular']}
        cls.reserved_roots={question_key(cls.index[sid]) for sid in cls.reserved}

    def test_188_ayri_editoryal_kayit_26_162(self):
        self.assertEqual(len(self.records),188)
        self.assertEqual(collections.Counter(s['ders'] for s in self.records),{'vatandaslik':26,'guncel':162})
        self.assertEqual(len({question_key(s) for s in self.index.values()}),4119)
        self.assertEqual(len({question_key(s) for s in self.records}),188)

    def test_ek_icerik_banka_kapsam_ve_inceleme_ozetleri_eslesir(self):
        policy=json.loads((ROOT/'data/kpss_kapsam.json').read_text())
        review=json.loads((ROOT/'data/kaynaklar/ek_188_inceleme.json').read_text())['questions']
        self.assertEqual(set(review),set(self.topics))
        for s in self.records:
            self.assertEqual(self.index[s['id']]['kok'],s['kok'])
            raw={k:v for k,v in self.index[s['id']].items() if k!='kpss_kapsam'}
            self.assertEqual(raw,s)
            self.assertEqual(review[s['id']]['sha256'],record_hash(s))
            self.assertEqual(policy['questions'][s['id']]['sha256'],record_hash(s))
            self.assertEqual(policy['questions'][s['id']]['topics'],[self.topics[s['id']]])
            self.assertEqual(s['kaynak'],'KPSS formatında')
            self.assertNotIn('cikmis',s['etiketler'])

    def test_sik_cevap_cozum_ve_tekrar_uretim(self):
        self.assertEqual(build(ROOT),(self.records,self.topics))
        for s in self.records:
            self.assertEqual(len(set(s['siklar'])),5)
            self.assertTrue(0<=s['dogru']<5)
            self.assertTrue(s['cozumler'][0]['metin'])

    def test_ek_kayit_ustune_farkli_icerik_yazilamaz(self):
        s=copy.deepcopy(self.records[0]);s['kaynak']='2024-KPSS'
        bank={d:(None,[]) for d in self.cache['sorular']}
        with self.assertRaises(ValueError):add_to_bank(ROOT,bank,{s['id']:s})

    def test_her_derste_denemeler_haric_en_az_500(self):
        t=self.cache['calisma_hedefi']
        self.assertEqual({d:s['baslangic_test_kapasitesi'] for d,s in t['dersler'].items()},
                         dict(tarih=800,cografya=761,vatandaslik=750,turkce=838,guncel=750))
        self.assertTrue(all(s['ilk_gun_eksik']==0 for s in t['dersler'].values()))
        self.assertEqual(sum(s['denemeye_ayrilan'] for s in t['dersler'].values()),220)

    def test_50_set_her_ders_250_set_toplam_ve_denemeler_haric(self):
        t=self.cache['calisma_hedefi']
        self.assertEqual(t['ders_basina_gunluk_test'],500)
        self.assertEqual(t['ders_basina_test_seti'],50)
        self.assertEqual(t['set_boyutu'],10)
        self.assertEqual(t['gunluk_toplam_test'],2500)
        self.assertEqual(t['gunluk_toplam_set'],250)
        self.assertIs(t['denemeler_hedefe_dahil'],False)

    def test_on_gun_henuz_tamamlandi_denmez(self):
        t=self.cache['calisma_hedefi']
        self.assertEqual(t['kamp_gun_sayisi'],10)
        self.assertTrue(all(s['kamp_test_ihtiyaci']==5000 for s in t['dersler'].values()))
        self.assertEqual(sum(s['kamp_asgari_havuz'] for s in t['dersler'].values()),25220)
        self.assertEqual(sum(s['kamp_test_eksigi'] for s in t['dersler'].values()),21101)

    def test_hedef_azaltilamaz_ve_deneme_karistirilamaz(self):
        target=load_target(ROOT)
        for change in ({'ders_basina_gunluk_test':499},{'set_boyutu':20},{'denemeler_hedefe_dahil':True}):
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);(root/'data').mkdir()
                (root/'data/calisma_hedefleri.json').write_text(json.dumps({**target,**change}))
                with self.assertRaises(ValueError):load_target(root)

    def test_api_ayni_hedef_ve_gercek_sayilari_verir(self):
        meta=server.app.test_client().get('/api/meta').get_json()
        self.assertEqual(meta['calisma_hedefi'],self.cache['calisma_hedefi'])
        self.assertEqual(meta['soru_sayilari']['guncel'],776)
        self.assertEqual(meta['soru_sayilari']['vatandaslik'],792)

    def test_2500_test_ve_220_deneme_sunucuda_cakismadan_ayrilabilir(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(server,'ILERLEME',Path(tmp)), patch.object(server,'her_seyi_yukle',return_value=self.cache):
            client=server.app.test_client()
            all_ids=[]
            for ders,rows in self.cache['sorular'].items():
                ids=[s['id'] for s in rows if s['id'] not in self.reserved and question_key(s) not in self.reserved_roots][:500]
                self.assertEqual(len(ids),500)
                all_ids.extend(ids)
                for start in range(0,500,50):
                    result=client.post('/api/soru-ayir/hedef-test',json={'tur':'test','oturum':f'{ders}-{start}','ids':ids[start:start+50]})
                    self.assertEqual(result.status_code,200,result.get_json())
            for e in self.exams:
                result=client.post('/api/soru-ayir/hedef-test',json={'tur':'deneme','deneme_id':e['id'],'oturum':e['id'],'ids':e['sorular']})
                self.assertEqual(result.status_code,200,result.get_json())
                all_ids.extend(e['sorular'])
            self.assertEqual(len(set(all_ids)),2720)
            progress=server.ilerleme_oku('hedef-test')
            self.assertEqual(len(progress['ayrilan_sorular']),2720)
            self.assertFalse(progress.get('gunluk',{}).get('sayi'))  # Ayırma, çözülmüş soru sayılmaz.

    def test_geciken_ilerleme_yeni_devam_kaydini_geri_alamaz(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(server,'ILERLEME',Path(tmp)):
            server.ilerleme_yaz('devam',{'devam_testleri':{'x':{'guncelleme':20,'bitti':True}}})
            server.ilerleme_yaz('devam',{'devam_testleri':{'x':{'guncelleme':10,'bitti':False}}})
            self.assertTrue(server.ilerleme_oku('devam')['devam_testleri']['x']['bitti'])

    def test_gecersiz_devam_alani_onceki_kaydi_silemez(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(server,'ILERLEME',Path(tmp)):
            server.ilerleme_yaz('devam',{'devam_testleri':{'x':{'guncelleme':20,'bitti':False}}})
            server.ilerleme_yaz('devam',{'devam_testleri':None})
            self.assertIn('x',server.ilerleme_oku('devam')['devam_testleri'])
