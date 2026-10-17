"""Soru kalitesi (2): yakın çeldirici, cevabı ele veren kök ve kolay soru kalıpları."""
import json
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from bilgi_veri import cografya, guncel, tarih  # noqa: E402
from bilgi_veri.ortak import farkli, yakin_sec  # noqa: E402

DERSLER = ['tarih', 'cografya', 'vatandaslik', 'guncel', 'turkce']


def banka(d):
    for line in (ROOT / f'data/sorular/{d}.jsonl').read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.startswith('#'):
            yield json.loads(line)


class KaliteTest(unittest.TestCase):
    def test_uretilen_sorularda_cevap_kokte_gecmez(self):
        for d in DERSLER:
            for r in banka(d):
                if 'bilgi-tablosu' not in (r.get('etiketler') or []):
                    continue
                kok = r['kok'].casefold()
                ic = [len(s) >= 4 and s.casefold() in kok for s in r['siklar']]
                self.assertFalse(ic[r['dogru']] and sum(ic) == 1, r['id'])

    def test_yakin_sec_en_yakinlardan_secer(self):
        rng = random.Random(1)
        for _ in range(50):
            yan = yakin_sec(50, list(range(100)), lambda v: abs(v - 50), rng, havuz=6)
            self.assertTrue(all(abs(v - 50) <= 3 for v in yan), yan)
        self.assertIsNone(yakin_sec('a', ['a', 'b'], lambda v: 0, rng))

    def test_farkli_kalibi_tek_dis_secenek(self):
        q = farkli(random.Random(2), 't', 'k', 'kök?', [(str(i), '') for i in range(6)], [('x', 'açıklama')],
                   lambda m, a, ic: a)
        self.assertEqual(q['dogru'], 'x')
        self.assertEqual(len(set(q['yanlis'])), 4)
        self.assertNotIn('x', q['yanlis'])

    def test_padisah_celdiricileri_yakin_donemden(self):
        qs = [x for x in tarih.uret(random.Random(3)) if x and x['tur'] == 'kisi']
        self.assertGreater(len(qs), 100)
        # Fatih dönemi olayında III. Selim / Abdülaziz gibi uzak padişahlar çeldirici olamaz
        for x in qs:
            if x['dogru'] == 'Fatih Sultan Mehmet':
                self.assertFalse({'III. Selim', 'Abdülaziz', 'II. Abdülhamit'} & set(x['yanlis']), x)

    def test_kolay_cografya_kaliplari_yok(self):
        qs = [x for x in cografya.uret(random.Random(4)) if x]
        turler = {x['tur'] for x in qs}
        self.assertFalse({'iklim', 'bitki', 'urun'} & turler)
        self.assertFalse(any('Anıtkabir' in x['kok'] for x in qs))
        ilk = {x[0]: x for x in cografya.iller()}
        for x in qs:
            if x['tur'].startswith('yer_il_'):
                d = ilk[x['dogru']]
                for y in x['yanlis']:
                    uz = ((ilk[y][2] - d[2]) ** 2 + (ilk[y][3] - d[3]) ** 2) ** 0.5
                    self.assertLess(uz, 3.0, (x['kok'], y))

    def test_ulke_celdiricileri_ayni_bolgeden(self):
        qs = [x for x in guncel.uret(random.Random(5)) if x and x['tur'] == 'baskent_geri']
        ayni = 0
        for x in qs:
            b = guncel.ULKE_BOLGE.get(x['dogru'])
            ayni += sum(guncel.ULKE_BOLGE.get(y) == b for y in x['yanlis'])
        self.assertGreater(ayni / (4 * len(qs)), 0.8)


if __name__ == '__main__':
    unittest.main()
