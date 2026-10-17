"""Türkçe dil bilgisi soru üreticisinin tek doğru cevap garantisini sınar."""
import random
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bilgi_veri import turkce, dilbilgisi_veri1 as V1, dilbilgisi_veri2 as V2, dilbilgisi_veri3 as V3  # noqa: E402

ROMA = ['I', 'II', 'III', 'IV', 'V']


def satirlar(kok):
    out = {}
    for line in kok.split('\\n'):
        m = re.match(r'^(I|II|III|IV|V)\. (.*)$', line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def tablo(blok, n):
    return [[x.strip() for x in l.split('|')] for l in blok.strip().splitlines() if l.strip() and len(l.split('|')) == n]


class DilBilgisiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sorular = [q for q in turkce.uret(random.Random(7)) if q]
        cls.ab_bozuk = {p[2]: p[3] for p in tablo(V1.AB, 5) if p[0] == 'B'}
        cls.ab_dogru = {p[1] for p in tablo(V1.AB, 2) if p[0] == 'D'} | set(cls.ab_bozuk.values())
        cls.yz_yanlis = {p[1]: p[2] for p in tablo(V2.YAZIM, 4) if p[0] == 'W'}
        cls.yz_dogru = {p[1] for p in tablo(V2.YAZIM, 2) if p[0] == 'C'} | set(cls.yz_yanlis.values())
        cls.iliski = {c: t for t, c in tablo(V1.ILISKI, 2)}
        cls.oznel = {c: t for t, c in tablo(V1.OZNEL, 2)}
        cls.mecaz = {c.replace('[', '“').replace(']', '”'): t for t, w, c in tablo(V3.MECAZ, 3)}

    def tur(self, t):
        qs = [q for q in self.sorular if q['tur'] == t]
        self.assertTrue(qs, t)
        return qs

    def tek_dogru(self, t, ozellik):
        for q in self.tur(t):
            s = satirlar(q['kok'])
            self.assertEqual(len(s), 5, q['kok'])
            uyan = [r for r, m in s.items() if ozellik(q, m)]
            self.assertEqual(uyan, [q['dogru']], q['kok'])

    def test_bes_farkli_sik(self):
        for q in self.sorular:
            opts = [q['dogru'], *q['yanlis']]
            self.assertEqual(len({o.casefold() for o in opts}), 5, q['kok'])

    def test_anlatim_bozuklugu(self):
        for t, bozuk_mu in (('ab_var', True), ('ab_yok', False)):
            for q in self.tur(t):
                s = satirlar(q['kok'])
                for m in s.values():
                    self.assertTrue(m in self.ab_bozuk or m in self.ab_dogru, m)
                uyan = [r for r, m in s.items() if (m in self.ab_bozuk) == bozuk_mu]
                self.assertEqual(uyan, [q['dogru']], q['kok'])
                # bozuk cümle ile kendi düzeltilmiş hâli aynı soruda bulunmaz
                for m in s.values():
                    if m in self.ab_bozuk:
                        self.assertNotIn(self.ab_bozuk[m], s.values())

    def test_yazim(self):
        for t, yanlis_mi in (('yz_var', True), ('yz_yok', False)):
            for q in self.tur(t):
                s = satirlar(q['kok'])
                uyan = [r for r, m in s.items() if (m in self.yz_yanlis) == yanlis_mi]
                self.assertEqual(uyan, [q['dogru']], q['kok'])
                for m in s.values():
                    if m in self.yz_yanlis:
                        self.assertNotIn(self.yz_yanlis[m], s.values())

    def test_iliski(self):
        for q in self.tur('il_var'):
            hedef = next(k for k, v in V1.ILISKI_AD.items() if f' {v} ilişkisi vardır?' in q['kok'])
            uyan = [r for r, m in satirlar(q['kok']).items() if self.iliski[m] == hedef]
            self.assertEqual(uyan, [q['dogru']], q['kok'])

    def test_oznel_nesnel(self):
        self.tek_dogru('oz_nesnel', lambda q, m: self.oznel[m] == 'N')
        self.tek_dogru('oz_oznel', lambda q, m: self.oznel[m] == 'O')

    def test_mecaz(self):
        self.tek_dogru('mz_mecaz', lambda q, m: self.mecaz[m] == 'M')
        self.tek_dogru('mz_gercek', lambda q, m: self.mecaz[m] == 'G')

    def test_turkce_dagilimi(self):
        """Sözel mantık sınavdaki payına yakın; dil bilgisi ve anlam türleri baskın değil ama geniş."""
        from collections import Counter
        c = Counter(q['konu'] for q in self.sorular)
        self.assertLess(c['Sözel Mantık'], 300)
        for konu in ('Anlatım Bozuklukları', 'Cümlede Anlam', 'Yazım', 'Noktalama', 'Cümle Ögeleri', 'Cümle Türleri'):
            self.assertGreater(c[konu], 40, konu)


if __name__ == '__main__':
    unittest.main()
