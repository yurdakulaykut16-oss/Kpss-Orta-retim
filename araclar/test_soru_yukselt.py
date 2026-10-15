#!/usr/bin/env python3
"""python3 -m unittest discover -s araclar -p 'test_soru_yukselt.py' -v"""
import json
import tempfile
import unittest
from pathlib import Path

from soru_yukselt import DERSLER, OZGUN_KAYNAK, yukseltilen_banka, main


class SoruYukseltTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'data/sorular').mkdir(parents=True)
        (self.root / 'data/kaynaklar').mkdir()
        self.soru = dict(
            id='TAR-0001', ders='tarih', gun=1, konu='İlk Türk Devletleri',
            zorluk=1, kaynak=OZGUN_KAYNAK, kok='Eski soru',
            siklar=['a', 'b', 'c', 'd', 'e'], dogru=0, cozumler=[],
            etiketler=['konu', 'cikmis'],
        )
        for ders in DERSLER:
            self.bank_yaz(ders, [self.soru] if ders == 'tarih' else [])
        self.tsv = self.root / 'data/kaynaklar/yukselt_test.tsv'
        self.satir = 'TAR-0001|3|Yeni soru?|Doğru|Yanlış1|Yanlış2|Yanlış3|Yanlış4|Gerekçeli çözüm'
        self.tsv.write_text(self.satir + '\n', encoding='utf-8')

    def bank_yaz(self, ders, sorular):
        p = self.root / f'data/sorular/{ders}.jsonl'
        p.write_text(''.join(json.dumps(s, ensure_ascii=False) + '\n' for s in sorular), encoding='utf-8')

    def snapshot(self):
        return {p.name: p.read_bytes() for p in (self.root / 'data/sorular').glob('*.jsonl')}

    def test_dogru_sik_kimlik_ve_plan(self):
        before = self.snapshot()
        banka, adet = yukseltilen_banka(self.root)
        s = banka['tarih'][1][0]
        self.assertEqual(s['siklar'][s['dogru']], 'Doğru')
        for alan in ('id', 'ders', 'gun', 'konu'):
            self.assertEqual(s[alan], self.soru[alan])
        self.assertNotIn('cikmis', s['etiketler'])
        self.assertEqual(sum(adet.values()), 1)
        self.assertEqual(before, self.snapshot())  # saf doğrulama diske yazmaz

    def test_kitap_ve_cikmis_korunur(self):
        for kaynak in ('2024-KPSS', '2014-KPSS Lisans', '2024 Öğreti Akademi Efsane Tarih Soru Bankası'):
            with self.subTest(kaynak=kaynak):
                self.bank_yaz('tarih', [{**self.soru, 'kaynak': kaynak}])
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, 'değiştirilemez'):
                    main(self.root)
                self.assertEqual(before, self.snapshot())

    def test_eski_yaniltici_etiket_duzeltilir(self):
        self.bank_yaz('tarih', [{**self.soru, 'kaynak': 'Çıkmış KPSS sorusudur (yeniden düzenlendi)'}])
        banka, _ = yukseltilen_banka(self.root)
        self.assertEqual(banka['tarih'][1][0]['kaynak'], OZGUN_KAYNAK)

    def test_tekrar_calisma_ayni_sonuc(self):
        main(self.root)
        before = self.snapshot()
        main(self.root)
        self.assertEqual(before, self.snapshot())

    def test_gecersiz_satirlar_yazma_yapmaz(self):
        for line in (
            self.satir.replace('TAR-0001', 'TAR-9999'),
            self.satir + '\n' + self.satir,
            self.satir.replace('|3|', '|1|'),
            self.satir.replace('|Yanlış2|', '|Yanlış1|'),
            self.satir.replace('|Gerekçeli çözüm', '|'),
            self.satir + '|2024 Pegem Soru Bankası',
        ):
            with self.subTest(line=line):
                self.tsv.write_text(line + '\n', encoding='utf-8')
                before = self.snapshot()
                with self.assertRaises(ValueError):
                    main(self.root)
                self.assertEqual(before, self.snapshot())

    def test_sonraki_hatali_satirda_kismi_yazma_yok(self):
        self.tsv.write_text(self.satir + '\n' + self.satir.replace('TAR-0001', 'TAR-9999'), encoding='utf-8')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            main(self.root)
        self.assertEqual(before, self.snapshot())

    def test_kok_cakismasi_reddedilir(self):
        self.bank_yaz('tarih', [self.soru, {**self.soru, 'id': 'TAR-0002', 'kok': 'Yeni soru?'}])
        with self.assertRaisesRegex(ValueError, 'Yinelenen soru kökü'):
            yukseltilen_banka(self.root)


if __name__ == '__main__':
    unittest.main()
