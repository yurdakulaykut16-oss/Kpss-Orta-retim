#!/usr/bin/env python3
"""Konu kapsamının API/deneme yoluyla aşılamaması ve arşiv korunması.

Bunlar konu eşleştirmesini ve izolasyonu denetler; harici ÖSYM kitapçığı
veya pedagojik güçlük doğrulaması değildir.
"""
import collections
import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kpss_kapsam import SUBJECTS, read_policy, filter_bank, project_exams, record_hash
from kapsam_taslagi import draft
import app as server


class KpssKapsamTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = {d: list(map(json.loads, (ROOT/f'data/sorular/{d}.jsonl').read_text().splitlines()))
                    for d in SUBJECTS}
        cls.index = {s['id']:s for rows in cls.bank.values() for s in rows}
        cls.policy = read_policy(ROOT)
        cls.active, cls.report = filter_bank(cls.bank, cls.policy)
        cls.active_ids = {s['id'] for rows in cls.active.values() for s in rows}
        cls.exams = json.loads((ROOT/'data/denemeler.json').read_text())
        cls.client = server.app.test_client()
        server.her_seyi_yukle(zorla=True)

    def tearDown(self):
        # Hata enjekte edilen testlerin cache durumu başka teste sızmasın.
        server._cache.clear()

    def test_tam_envanter_aktif_ve_bekleyen_ayri(self):
        self.assertEqual(set(self.index), set(self.policy['questions']))
        self.assertEqual(len(self.index),14404)
        self.assertEqual(len(self.active_ids),14220)
        self.assertEqual(len(self.report['bekleyen_kayitlar']),184)
        self.assertEqual(self.active_ids | self.report['bekleyen_kayitlar'].keys(), self.index.keys())
        self.assertFalse(self.active_ids & self.report['bekleyen_kayitlar'].keys())
        for sid,s in self.index.items():
            self.assertEqual(record_hash(s),self.policy['questions'][sid]['sha256'])

    def test_her_aktif_konu_ayni_dersten_kaynak_ornegine_bagli(self):
        for ders, rows in self.active.items():
            for s in rows:
                self.assertTrue(s['kpss_kapsam']['konular'])
                for topic in s['kpss_kapsam']['konular']:
                    t=self.policy['topics'][topic['id']]
                    self.assertEqual(t['ders'],ders)
                    self.assertTrue(t['references'])
                    for ref in t['references']:
                        source=self.index[ref['id']]
                        self.assertEqual(source['ders'],ders)
                        self.assertRegex(source['kaynak'],r'^\d{4}-KPSS')
                        self.assertEqual(source['kaynak'],ref['kaynak'])
                        self.assertEqual(record_hash(source),ref['sha256'])

    def test_arsiv_ve_kaynakli_metinler_degismez(self):
        before=copy.deepcopy(self.bank)
        active,_=filter_bank(self.bank,self.policy)
        self.assertEqual(before,self.bank)
        source_rows=[s for s in self.index.values() if re.match(r'^\d{4}-KPSS',s['kaynak'])
                     or 'Soru Bankası' in s['kaynak']]
        self.assertEqual(len(source_rows),492)
        self.assertTrue(all(s['id'] in self.active_ids for s in source_rows))
        for rows in active.values():
            for s in rows:
                self.assertEqual({k:v for k,v in s.items() if k!='kpss_kapsam'},self.index[s['id']])

    def test_guncel_tarih_etiketi_otomatik_dogrulama_degil(self):
        unverified=[s['id'] for s in self.index.values() if s['kaynak'].startswith('Güncel olay')]
        self.assertEqual(len(unverified),63)
        self.assertTrue(all(sid not in self.active_ids for sid in unverified))
        self.assertTrue(all(s['konu'] not in ('Bilim','bilim_teknoloji','Ekonomi','Uzay')
                            for s in self.active['guncel']))

    def test_etiketi_uygun_yeni_kayit_onaysiz_gecemez(self):
        bank=copy.deepcopy(self.bank)
        s=copy.deepcopy(bank['tarih'][0]);s['id']='TAR-ONAYSIZ';s['kok']='Kapsam dışı yeni bilgi'
        bank['tarih'].append(s)
        active,report=filter_bank(bank,self.policy)
        self.assertNotIn(s['id'],{r['id'] for rows in active.values() for r in rows})
        self.assertIn(s['id'],report['bekleyen_kayitlar'])

    def test_aktif_sorunun_koku_degistirilince_izin_duser(self):
        bank=copy.deepcopy(self.bank)
        s=bank['tarih'][0];s['kok']+=' Yeni bir biyoloji sorusu.'
        active,report=filter_bank(bank,self.policy)
        self.assertNotIn(s['id'],{r['id'] for rows in active.values() for r in rows})
        self.assertIn('İçerik değişti',report['bekleyen_kayitlar'][s['id']]['gerekce'])

    def test_konu_ornegi_degistirilirse_konu_onayi_duser(self):
        bank=copy.deepcopy(self.bank)
        key='c-ticaret'
        ref=self.policy['topics'][key]['references'][0]['id']
        next(s for s in bank['cografya'] if s['id']==ref)['kok']+=' Değişiklik.'
        active,_=filter_bank(bank,self.policy)
        ids={s['id'] for rows in active.values() for s in rows}
        affected={sid for sid,r in self.policy['questions'].items() if key in r['topics']}
        self.assertTrue(affected)
        self.assertFalse(ids & affected)

    def test_baska_ders_veya_bos_dayanak_gecersiz(self):
        sid=self.bank['tarih'][0]['id']
        policy=copy.deepcopy(self.policy)
        policy['questions'][sid]['topics']=['u-paragraf']
        active,_=filter_bank(self.bank,policy)
        self.assertNotIn(sid,{s['id'] for rows in active.values() for s in rows})
        policy=copy.deepcopy(self.policy)
        key=policy['questions'][sid]['topics'][0]
        policy['topics'][key]['references']=[]
        active,_=filter_bank(self.bank,policy)
        self.assertNotIn(sid,{s['id'] for rows in active.values() for s in rows})

    def test_taslak_etiketten_aktif_izin_uretmez(self):
        bank=copy.deepcopy(self.bank)
        changed=bank['tarih'][0];changed['kok']+=' Değişti.'
        new=copy.deepcopy(changed);new['id']='TAR-YENI-ONAYSIZ';bank['tarih'].append(new)
        before=copy.deepcopy(self.policy)
        result=draft(bank,self.policy)
        self.assertEqual(before,self.policy)
        for sid in (changed['id'],new['id']):
            self.assertEqual(result['questions'][sid]['status'],'beklemede')
            self.assertEqual(result['questions'][sid]['topics'],[])
            self.assertTrue(result['questions'][sid]['aday_konular'])

    def test_taslak_araci_politika_ve_bankayi_ezemez(self):
        for path in (ROOT/'data/kpss_kapsam.json', ROOT/'data/sorular/tarih.jsonl'):
            before=path.read_bytes()
            result=subprocess.run([sys.executable,str(ROOT/'araclar/kapsam_taslagi.py'),
                                   '--output',str(path)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(before,path.read_bytes())

    def test_tum_soru_api_yollari_ayni_kapsamda(self):
        ids=set();cikmis=0
        for d in SUBJECTS:
            response=self.client.get('/api/sorular/'+d)
            self.assertEqual(response.status_code,200)
            rows=response.get_json();ids.update(s['id'] for s in rows)
            self.assertTrue(all(s.get('kpss_kapsam') for s in rows))
            official=self.client.get('/api/sorular/'+d+'?cikmis=1').get_json()
            cikmis+=len(official)
            self.assertTrue(all(re.match(r'^\d{4}-KPSS',s['kaynak']) for s in official))
        self.assertEqual(ids,self.active_ids)
        self.assertEqual(cikmis,404)
        for sid in ('GUN-0002','GUN-0060'):
            for query in ('','?arsiv=1','?kapsam=hepsi'):
                self.assertEqual(self.client.get('/api/soru/'+sid+query).status_code,404)
        active_id=next(iter(ids))
        self.assertEqual(self.client.get('/api/soru/'+active_id).get_json()['id'],active_id)

    def test_denemeler_sayi_ders_dagilimi_ve_tekilligi_korur(self):
        before=copy.deepcopy(self.exams)
        projected=project_exams(self.exams,self.bank,self.active)
        self.assertEqual(self.exams,before)
        self.assertEqual(projected,project_exams(self.exams,self.bank,self.active))
        api=self.client.get('/api/denemeler').get_json()
        self.assertEqual(api,projected)
        for old,new in zip(self.exams['denemeler'],projected['denemeler']):
            with self.subTest(deneme=old['id']):
                self.assertEqual(len(old['sorular']),len(new['sorular']))
                self.assertEqual(len(new['sorular']),len(set(new['sorular'])))
                self.assertEqual(collections.Counter(self.index[sid]['ders'] for sid in old['sorular']),
                                 collections.Counter(self.index[sid]['ders'] for sid in new['sorular']))
                self.assertTrue(set(new['sorular']) <= self.active_ids)
                response=self.client.get('/api/deneme/'+old['id']).get_json()
                self.assertEqual([s['id'] for s in response['soru_nesneleri']],new['sorular'])
                self.assertTrue(all(s.get('kpss_kapsam') for s in response['soru_nesneleri']))

    def test_yetersiz_onayli_denemede_kapsam_disi_yedek_yok(self):
        empty={d:[] for d in SUBJECTS}
        with self.assertRaisesRegex(ValueError,'yetersiz'):
            project_exams(self.exams,self.bank,empty)

    def test_gelecek_yil_kaydi_konu_dayanagi_olamaz(self):
        bank=copy.deepcopy(self.bank)
        policy=copy.deepcopy(self.policy)
        key='c-ticaret';ref=policy['topics'][key]['references'][0]
        s=next(s for s in bank['cografya'] if s['id']==ref['id'])
        s['kaynak']='2099-KPSS'
        ref.update(kaynak=s['kaynak'],sha256=record_hash(s))
        policy['questions'][s['id']]['sha256']=record_hash(s)
        active,_=filter_bank(bank,policy)
        affected={sid for sid,r in policy['questions'].items() if key in r['topics']}
        self.assertFalse(affected & {s['id'] for rows in active.values() for s in rows})

    def test_deneme_uretim_araci_da_kapsamdan_cikmaz(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'araclar').mkdir()
            shutil.copytree(ROOT/'data/sorular',root/'data/sorular')
            shutil.copy(ROOT/'data/kpss_kapsam.json',root/'data/kpss_kapsam.json')
            shutil.copy(ROOT/'kpss_kapsam.py',root/'kpss_kapsam.py')
            script=root/'araclar/deneme_uret.py'
            shutil.copy(ROOT/'araclar/deneme_uret.py',script)
            subprocess.run([sys.executable,str(script)],check=True,capture_output=True)
            first=(root/'data/denemeler.json').read_bytes()
            subprocess.run([sys.executable,str(script)],check=True,capture_output=True)
            self.assertEqual(first,(root/'data/denemeler.json').read_bytes())
            for exam in json.loads(first)['denemeler']:
                self.assertEqual(len(exam['sorular']),50 if exam['tur']=='buyuk' else 15)
                self.assertIn(exam['gun'],range(1,9))
                self.assertEqual(len(exam['sorular']),len(set(exam['sorular'])))
                self.assertTrue(set(exam['sorular']) <= self.active_ids)

    def test_eksik_politikada_ham_cache_kalmaz(self):
        server.her_seyi_yukle(zorla=True)
        with patch.object(server,'read_policy',side_effect=FileNotFoundError('Kapsam yok')):
            with self.assertRaises(FileNotFoundError):
                server.her_seyi_yukle(zorla=True)
            self.assertEqual(server._cache,{})

    def test_meta_ve_rapor_aktif_sayiyi_gosterir(self):
        meta=self.client.get('/api/meta').get_json()
        self.assertEqual(meta['soru_sayilari'],{d:len(self.active[d]) for d in SUBJECTS})
        self.assertEqual(meta['kapsam']['aktif'],14220)
        self.assertEqual(meta['kapsam']['bekleyen'],184)
        report=self.client.get('/api/kapsam').get_json()
        self.assertEqual(report,self.report)
        self.assertTrue(all(set(v)=={'ders','gerekce'} for v in report['bekleyen_kayitlar'].values()))


if __name__=='__main__':
    unittest.main()
