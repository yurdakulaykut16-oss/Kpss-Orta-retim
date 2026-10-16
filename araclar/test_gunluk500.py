"""Deneme hariç 5×400 (günlük üst sınır) test hedefi, gerçek kapasite ve editoryal ek aktarımı."""
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
        self.assertEqual(len({question_key(s) for s in self.index.values()}),14220)
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

    def test_her_derste_denemeler_haric_2800(self):
        t=self.cache['calisma_hedefi']
        self.assertEqual({d:s['baslangic_test_kapasitesi'] for d,s in t['dersler'].items()},
                         dict(tarih=2800,cografya=2800,vatandaslik=2800,turkce=2800,guncel=2800))
        self.assertTrue(all(s['ilk_gun_eksik']==0 for s in t['dersler'].values()))
        self.assertEqual(sum(s['denemeye_ayrilan'] for s in t['dersler'].values()),220)

    def test_50_set_her_ders_250_set_toplam_ve_denemeler_haric(self):
        t=self.cache['calisma_hedefi']
        self.assertEqual(t['ders_basina_gunluk_test'],400)
        self.assertIs(t['gunluk_ust_sinir'],True)
        self.assertEqual(t['ders_basina_test_seti'],40)
        self.assertEqual(t['set_boyutu'],10)
        self.assertEqual(t['gunluk_toplam_test'],2000)
        self.assertEqual(t['gunluk_toplam_set'],200)
        self.assertIs(t['denemeler_hedefe_dahil'],False)

    def test_yedi_test_gunu_her_ders_400(self):
        t=self.cache['calisma_hedefi']
        # 17-23 Ekim: 7 test günü (24 Ekim yalnızca deneme/tekrar), her gün her dersten 400.
        self.assertEqual(t['kamp_gun_sayisi'],7)
        self.assertTrue(all(s['kamp_test_ihtiyaci']==2800 for s in t['dersler'].values()))
        self.assertEqual(sum(s['kamp_asgari_havuz'] for s in t['dersler'].values()),14220)
        self.assertEqual(sum(s['kamp_test_eksigi'] for s in t['dersler'].values()),0)
        for s in t['dersler'].values():
            self.assertEqual(s['gun_dagilimi'],[400]*7)
            self.assertEqual(s['tam_gun'],7)
        self.assertIn('tamamlandı anlamına gelmez',t['notu'])

    def test_hedef_azaltilamaz_ve_deneme_karistirilamaz(self):
        target=load_target(ROOT)
        for change in ({'ders_basina_gunluk_test':399},{'gunluk_ust_sinir':False},{'set_boyutu':20},{'denemeler_hedefe_dahil':True}):
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);(root/'data').mkdir()
                (root/'data/calisma_hedefleri.json').write_text(json.dumps({**target,**change}))
                with self.assertRaises(ValueError):load_target(root)

    def test_api_ayni_hedef_ve_gercek_sayilari_verir(self):
        meta=server.app.test_client().get('/api/meta').get_json()
        self.assertEqual(meta['calisma_hedefi'],self.cache['calisma_hedefi'])
        self.assertEqual(meta['soru_sayilari']['guncel'],2826)
        self.assertEqual(meta['soru_sayilari']['vatandaslik'],2842)

    def test_2000_test_ve_220_deneme_sunucuda_cakismadan_ayrilabilir(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(server,'ILERLEME',Path(tmp)), patch.object(server,'her_seyi_yukle',return_value=self.cache):
            client=server.app.test_client()
            all_ids=[]
            for ders,rows in self.cache['sorular'].items():
                ids=[s['id'] for s in rows if s['id'] not in self.reserved and question_key(s) not in self.reserved_roots][:401]
                self.assertEqual(len(ids),401)
                all_ids.extend(ids)
                for start in range(0,400,50):
                    result=client.post('/api/soru-ayir/hedef-test',json={'tur':'test','oturum':f'{ders}-{start}','ids':ids[start:start+50]})
                    self.assertEqual(result.status_code,200,result.get_json())
                # Günlük üst sınır: 401. yeni soru bugün verilmez, sonraki güne kalır.
                result=client.post('/api/soru-ayir/hedef-test',json={'tur':'test','oturum':f'{ders}-fazla','ids':ids[400:]})
                self.assertEqual(result.status_code,429,result.get_json())
                self.assertIn('sonraki günlere',result.get_json()['hata'])
                all_ids.pop()
                # İstemcinin eski kaydı sunucunun gün/ders sayacını silemez.
                server.ilerleme_yaz('hedef-test',{'ayrilan_sorular':{ids[0]:{'tur':'test'}}})
                self.assertEqual(server.ilerleme_oku('hedef-test')['ayrilan_sorular'][ids[0]]['ders'],ders)
            for e in self.exams:
                result=client.post('/api/soru-ayir/hedef-test',json={'tur':'deneme','deneme_id':e['id'],'oturum':e['id'],'ids':e['sorular']})
                self.assertEqual(result.status_code,200,result.get_json())
                all_ids.extend(e['sorular'])
            self.assertEqual(len(set(all_ids)),2220)
            progress=server.ilerleme_oku('hedef-test')
            self.assertEqual(len(progress['ayrilan_sorular']),2220)
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
