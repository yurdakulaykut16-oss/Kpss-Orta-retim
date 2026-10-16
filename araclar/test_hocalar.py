"""Üç hocadan konu anlatımı: kapsam, yapı ve konu_yeniden.json ile tutarlılık testleri."""
import importlib
import json
import re
import sys
import unittest
from pathlib import Path

ARACLAR = Path(__file__).resolve().parent
sys.path.insert(0, str(ARACLAR))

from konu_anlatim_veri.hocalar import HOCALAR, MIN_BASLIK, MIN_UZUNLUK  # noqa: E402
import konu_anlatim_ekle  # noqa: E402

DERSLER = ['tarih', 'cografya', 'vatandaslik', 'turkce', 'guncel']
KART = ARACLAR.parent / 'data' / 'konu_yeniden.json'

# Her hocanın kendine özgü bölüm başlıkları (farklı kuram → farklı yapı).
IMZA = {
    'kemal': ['§ Büyük resim', '§ Hikâye', '§ Tek cümlede'],
    'ayse': ['§ Kavram haritası', '§ Adım adım'],
    'murat': ['§ Soru kalıpları', '§ Tuzaklar', '§ Hafıza kodu', '§ Mini test'],
}


def hoca_modulleri():
    for d in DERSLER:
        yield (d, importlib.import_module(f'konu_anlatim_veri.{d}'),
               importlib.import_module(f'konu_anlatim_veri.hoca_{d}'))


class HocaKapsamTest(unittest.TestCase):
    def test_uc_farkli_hoca(self):
        self.assertEqual([h['id'] for h in HOCALAR], ['kemal', 'ayse', 'murat'])
        self.assertEqual(len({h['yontem'] for h in HOCALAR}), 3)

    def test_her_ana_konu_uc_hocadan(self):
        toplam = 0
        for d, ders, hoca in hoca_modulleri():
            analar = {a for liste in ders.ESLEME.values() for a in liste}
            self.assertEqual(analar, set(hoca.HOCA), d)
            for ana, metinler in hoca.HOCA.items():
                self.assertEqual(len(metinler), 3, (d, ana))
                toplam += 1
        self.assertEqual(toplam, 50)

    def test_yapi_ve_uzunluk(self):
        for d, _, hoca in hoca_modulleri():
            for ana, metinler in hoca.HOCA.items():
                for h, metin in zip(HOCALAR, metinler):
                    with self.subTest(ders=d, ana=ana, hoca=h['id']):
                        self.assertGreaterEqual(len(metin), MIN_UZUNLUK)
                        basliklar = [s for s in metin.split('\n') if s.startswith('§ ')]
                        self.assertGreaterEqual(len(basliklar), MIN_BASLIK)
                        for imza in IMZA[h['id']]:
                            self.assertTrue(any(b.startswith(imza) for b in basliklar), imza)

    def test_murat_mini_test_uc_soru(self):
        for d, _, hoca in hoca_modulleri():
            for ana, (_, _, murat) in hoca.HOCA.items():
                mini = murat.split('§ Mini test', 1)[1]
                self.assertEqual(len(re.findall(r'— Cevap:', mini)), 3, (d, ana))

    def test_metinler_birbirinden_farkli(self):
        for d, _, hoca in hoca_modulleri():
            for ana, metinler in hoca.HOCA.items():
                satirlar = [set(s for s in m.split('\n') if len(s) > 40) for m in metinler]
                for i in range(3):
                    for j in range(i + 1, 3):
                        ortak = satirlar[i] & satirlar[j]
                        self.assertLessEqual(len(ortak), 1, (d, ana, i, j, list(ortak)[:2]))

    def test_taslak_kalintisi_yok(self):
        for d, _, hoca in hoca_modulleri():
            for ana, metinler in hoca.HOCA.items():
                for m in metinler:
                    self.assertNotRegex(m, r'TODO|XXX|\?\?|değil\?', (d, ana))


class KonuYenidenKartTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kartlar = json.loads(KART.read_text(encoding='utf-8'))

    def test_her_kartta_hocalar(self):
        for key, kart in self.kartlar.items():
            with self.subTest(key=key):
                self.assertTrue(kart.get('hocalar'))
                for g in kart['hocalar']:
                    self.assertEqual([a['hoca'] for a in g['anlatimlar']], ['kemal', 'ayse', 'murat'])
                    for a in g['anlatimlar']:
                        self.assertTrue(a['metin'] and a['ad'] and a['ikon'] and a['yontem'])

    def test_json_kaynakla_guncel(self):
        beklenen = konu_anlatim_ekle.hoca_gruplari()
        for key, kart in self.kartlar.items():
            self.assertEqual(kart['hocalar'], beklenen[key], key)

    def test_kalite_kontrolu_temiz(self):
        sorun, ana = konu_anlatim_ekle.kalite_sorunlari(konu_anlatim_ekle.hoca_gruplari())
        self.assertEqual(sorun, [])
        self.assertEqual(ana, 50)


if __name__ == '__main__':
    unittest.main()
