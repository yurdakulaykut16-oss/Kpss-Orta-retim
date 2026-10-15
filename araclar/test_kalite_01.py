"""Editoryal revizyonun sınırları; teknik testler güçlük kalibrasyonu değildir."""
import collections
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import app as server
from kpss_kapsam import record_hash, read_policy, filter_bank, project_exams, SUBJECTS

ROOT = Path(__file__).resolve().parent.parent


class KaliteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review=json.loads((ROOT/'data/kaynaklar/kalite_01_inceleme.json').read_text())['questions']
        cls.bank={d:list(map(json.loads,(ROOT/f'data/sorular/{d}.jsonl').read_text().splitlines())) for d in SUBJECTS}
        cls.index={s['id']:s for rows in cls.bank.values() for s in rows}
        cls.policy=read_policy(ROOT)
        cls.editor={l.split('|')[0]:l.split('|') for l in (ROOT/'data/kaynaklar/kalite_01.tsv').read_text().splitlines() if l and not l.startswith('#')}

    def test_50_mevcut_ozgun_10ar(self):
        self.assertEqual(len(self.review),50)
        self.assertEqual(self.review.keys(),self.editor.keys())
        self.assertEqual(collections.Counter(self.index[sid]['ders'] for sid in self.review),dict.fromkeys(SUBJECTS,10))
        for sid,r in self.review.items():
            self.assertEqual(record_hash(r['before']),r['before_sha256'])
            self.assertEqual(record_hash(self.index[sid]),r['after_sha256'])
            self.assertNotEqual(r['before_sha256'],r['after_sha256'])
            self.assertEqual(r['before']['kaynak'],'KPSS formatında')
            for k in ('id','ders','gun','konu','kaynak'):
                self.assertEqual(r['before'][k],self.index[sid][k])

    def test_editor_ve_banka_tam_eslesir(self):
        for sid,p in self.editor.items():
            s=self.index[sid]
            self.assertEqual(s['kok'],p[2].replace(r'\n','\n'))
            self.assertEqual(s['siklar'][s['dogru']],p[3])
            self.assertEqual(set(s['siklar']),set(p[3:8]))
            self.assertEqual(s['cozumler'][0]['metin'],p[8])
            self.assertNotIn('cikmis',s['etiketler'])

    def test_kapsam_konu_degisimi_yok_yeni_hash_ayri_onayli(self):
        active,report=filter_bank(self.bank,self.policy)
        ids={s['id'] for rows in active.values() for s in rows}
        self.assertEqual(report['aktif'],2869)
        self.assertTrue(self.review.keys()<=ids)
        for sid,r in self.review.items():
            self.assertEqual(self.policy['questions'][sid]['topics'],r['topics'])
            self.assertEqual(self.policy['questions'][sid]['sha256'],r['after_sha256'])

    def test_denemeler_birbirinden_de_ayri(self):
        active,_=filter_bank(self.bank,self.policy)
        exams=project_exams(json.loads((ROOT/'data/denemeler.json').read_text()),self.bank,active)['denemeler']
        ids=[sid for d in exams for sid in d['sorular']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),220)

    def test_geciken_ilerleme_kullanim_kaydini_silemez(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(server,'ILERLEME',Path(tmp)):
            server.ilerleme_yaz('test',{'ayrilan_sorular':{'TAR-0002':{'tur':'test'}},'ayrilan_kokler':{'örnek':True}})
            server.ilerleme_yaz('test',{'ayrilan_sorular':{},'ayrilan_kokler':{}})
            data=server.ilerleme_oku('test')
            self.assertIn('TAR-0002',data['ayrilan_sorular'])
            self.assertIn('örnek',data['ayrilan_kokler'])

    def test_kullanim_kaydi_yanlis_tip_ile_silinemez(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(server,'ILERLEME',Path(tmp)):
            server.ilerleme_yaz('test',{'ayrilan_sorular':{'GUN-0068':True}})
            server.ilerleme_yaz('test',{'ayrilan_sorular':[],'ayrilan_kokler':None})
            self.assertEqual(server.ilerleme_oku('test')['ayrilan_sorular'],{'GUN-0068':True})

    def test_hedef_3000_aktif_sayi_degil(self):
        meta=server.app.test_client().get('/api/meta').get_json()
        self.assertEqual(meta['havuz_hedefleri']['guncel'],3000)
        self.assertEqual(meta['soru_sayilari']['guncel'],526)
