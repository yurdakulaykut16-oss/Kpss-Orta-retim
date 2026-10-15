#!/usr/bin/env python3
"""Yeniden yazım TSV'leri ile uygulamanın gerçek bankasının tutarlılık testleri.

Bunlar veri/aktarımı test eder; soruların içerik doğruluğunun veya ölçme
zorluğunun istatistiksel kalibrasyonu değildir. Testler diske yazmaz.
"""
import json
import unittest
from pathlib import Path

from soru_yukselt import DERSLER, OZGUN_KAYNAK, yukseltilen_banka

ROOT = Path(__file__).resolve().parent.parent


class BankaTutarlilikTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.satirlar = []
        for dosya in sorted((ROOT / 'data/kaynaklar').glob('yukselt_*.tsv')):
            for line in dosya.read_text(encoding='utf-8').splitlines():
                if not line.strip() or line.lstrip().startswith('#'):
                    continue
                cls.satirlar.append([x.strip() for x in line.split('\t' if '\t' in line else '|')])
        cls.rows = {}
        cls.by_ders = {}
        for ders in DERSLER:
            yol = ROOT / f'data/sorular/{ders}.jsonl'
            rows = [json.loads(line) for line in yol.read_text(encoding='utf-8').splitlines() if line.strip()]
            cls.by_ders[ders] = rows
            cls.rows.update({s['id']: s for s in rows})

    def test_tekil_ve_mevcut_idler(self):
        ids = [p[0] for p in self.satirlar]
        self.assertGreaterEqual(len(ids), 2300)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(ids) <= self.rows.keys())

    def test_siklar_cevaplar_ve_cozumler_aktarilmis(self):
        for p in self.satirlar:
            with self.subTest(id=p[0]):
                s = self.rows[p[0]]
                self.assertEqual(s['kok'], p[2].replace(r'\n', '\n'))
                self.assertEqual(s['zorluk'], int(p[1]))
                self.assertEqual(set(s['siklar']), set(p[3:8]))
                self.assertEqual(len(set(s['siklar'])), 5)
                self.assertEqual(s['siklar'][s['dogru']], p[3])
                self.assertEqual(s['cozumler'][0]['metin'], p[8])

    def test_ozgun_etiketleri(self):
        for p in self.satirlar:
            with self.subTest(id=p[0]):
                s = self.rows[p[0]]
                self.assertEqual(s['kaynak'], OZGUN_KAYNAK)
                self.assertNotIn('cikmis', s['etiketler'])
                self.assertEqual(s['cozumler'][0]['yontem'], 'KPSS mantığı ile çözüm')

    def test_yuzluk_partide_her_dersten_yirmi_soru(self):
        sayilar = dict.fromkeys(DERSLER, 0)
        for dosya in (ROOT / 'data/kaynaklar').glob('yukselt_1[0-4]_*.tsv'):
            for line in dosya.read_text(encoding='utf-8').splitlines():
                if not line.strip() or line.lstrip().startswith('#'):
                    continue
                sid = line.split('|')[0]
                sayilar[self.rows[sid]['ders']] += 1
        self.assertEqual(sayilar, dict.fromkeys(DERSLER, 20))

    def test_tekrar_uygulama_bankayi_degistirmez(self):
        banka, sayilar = yukseltilen_banka(ROOT)
        self.assertEqual(sum(sayilar.values()), len(self.satirlar))
        for ders in DERSLER:
            self.assertEqual(banka[ders][1], self.by_ders[ders])


if __name__ == '__main__':
    unittest.main()
