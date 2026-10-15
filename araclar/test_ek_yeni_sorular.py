"""Elle yazılmış yeni soru partileri: 5 ders × 50, tekrarsız kök, onaylı ve aktif."""
import collections
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'araclar'))
import app as server  # noqa: E402
from kpss_kapsam import question_key, record_hash  # noqa: E402
from ek_yeni_sorular import build, add_to_bank  # noqa: E402


class YeniPartiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records, cls.topics = build(ROOT)
        cls.cache = server.her_seyi_yukle()
        cls.index = {s['id']: s for rows in cls.cache['sorular'].values() for s in rows}

    def test_her_derste_50_yeni_soru(self):
        self.assertEqual(len(self.records), 250)
        self.assertEqual(collections.Counter(s['ders'] for s in self.records),
                         dict(tarih=50, cografya=50, vatandaslik=50, turkce=50, guncel=50))

    def test_kokler_birbirinden_ve_bankadan_farkli(self):
        roots = [question_key(s) for s in self.records]
        self.assertEqual(len(set(roots)), 250)
        others = {question_key(s) for sid, s in self.index.items() if '-YS-' not in sid}
        self.assertFalse(set(roots) & others)

    def test_bankada_aktif_ve_kapsam_ozeti_eslesir(self):
        policy = json.loads((ROOT / 'data/kpss_kapsam.json').read_text(encoding='utf-8'))
        for s in self.records:
            self.assertIn(s['id'], self.index, s['id'])
            raw = {k: v for k, v in self.index[s['id']].items() if k != 'kpss_kapsam'}
            self.assertEqual(raw, s)
            self.assertEqual(policy['questions'][s['id']]['sha256'], record_hash(s))
            self.assertEqual(policy['questions'][s['id']]['topics'], [self.topics[s['id']]])
            self.assertNotIn('cikmis', s['etiketler'])

    def test_sik_cevap_cozum_ve_tekrar_uretim(self):
        self.assertEqual(build(ROOT), (self.records, self.topics))
        for s in self.records:
            self.assertEqual(len(set(s['siklar'])), 5)
            self.assertTrue(0 <= s['dogru'] < 5)
            self.assertTrue(s['cozumler'][0]['metin'])
            self.assertIn(s['gun'], range(1, 11))
        # Doğru şık her zaman ilk sırada kalmasın (karıştırma çalışıyor).
        self.assertGreater(len({s['dogru'] for s in self.records}), 3)

    def test_kok_cakismasi_ve_icerik_degisimi_reddedilir(self):
        s = dict(self.records[0])
        bank = {d: (None, []) for d in self.cache['sorular']}
        with self.assertRaises(ValueError):
            add_to_bank(ROOT, bank, {s['id']: {**s, 'kaynak': '2024-KPSS'}})
        clash = {**s, 'id': 'TAR-9998'}
        with self.assertRaises(ValueError):
            add_to_bank(ROOT, bank, {'TAR-9998': clash})

    def test_gecersiz_konu_reddedilir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data/kaynaklar').mkdir(parents=True)
            (root / 'data/kpss_kapsam.json').write_text((ROOT / 'data/kpss_kapsam.json').read_text(encoding='utf-8'), encoding='utf-8')
            (root / 'data/kaynaklar/yeni_parti_99.tsv').write_text(
                'TAR-YS-0001|Uydurma Konu|2|Kök?|A|B|C|D|E|Gerekçe\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                build(root)

    def test_parti_yoksa_bos_doner(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(build(Path(tmp)), ([], {}))


if __name__ == '__main__':
    unittest.main()
