#!/usr/bin/env python3
"""500'lük partinin sayısı, tekrar üretimi ve cevap türetme testleri.

Bilgi tablolarının doğruluğu editoryaldir; testler ölçme güçlüğünün aday
verileriyle kalibrasyonu veya harici kaynak doğrulaması yerine geçmez.
"""
import collections
import json
import unittest
from pathlib import Path

from parti_500_uret import build, FILES

ROOT = Path(__file__).resolve().parent.parent


def independent_answer(truths):
    selected = [str(i) for i, yes in enumerate(truths, 1) if yes]
    mapping = {'1': 'I', '2': 'II', '3': 'III'}
    if len(selected) == 1:
        return 'Yalnız ' + mapping[selected[0]]
    if len(selected) == 3:
        return 'I, II ve III'
    return ' ve '.join(mapping[x] for x in selected)


class Parti500Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = build(ROOT)
        cls.review=json.loads((ROOT/'data/kaynaklar/kalite_01_inceleme.json').read_text())['questions']
        cls.quality={l.split('|')[0]:l.split('|') for l in (ROOT/'data/kaynaklar/kalite_01.tsv').read_text().splitlines() if l and not l.startswith('#')}
        cls.config = json.loads((ROOT / 'data/kaynaklar/parti_500_editor.json').read_text())
        cls.rows = {r[0]: r for rows in cls.output.values() for r in rows}
        cls.bank = {}
        for d in FILES:
            for s in map(json.loads, (ROOT / f'data/sorular/{d}.jsonl').read_text().splitlines()):
                cls.bank[s['id']] = s

    def test_her_dersten_100_farkli_id(self):
        self.assertEqual({d: len(r) for d, r in self.output.items()}, dict.fromkeys(FILES, 100))
        self.assertEqual(len(self.rows), 500)
        self.assertEqual(len({r[2] for r in self.rows.values()}), 500)

    def test_dosyalar_tekrar_uretilebilir(self):
        for d, rows in self.output.items():
            path = ROOT / 'data/kaynaklar' / FILES[d]
            actual = [line.split('|') for line in path.read_text().splitlines()
                      if line.strip() and not line.lstrip().startswith('#')]
            self.assertEqual([self.quality.get(r[0],r) for r in rows], actual)

    def test_banka_cevap_ve_satir_sonlari(self):
        for sid, r in self.rows.items():
            with self.subTest(sid=sid):
                s = self.review[sid]['before'] if sid in self.review else self.bank[sid]
                self.assertEqual(s['kaynak'], 'KPSS formatında')
                self.assertEqual(s['kok'], r[2].replace(r'\n', '\n'))
                self.assertEqual(s['siklar'][s['dogru']], r[3])
                self.assertEqual(len(set(s['siklar'])), 5)
                self.assertNotIn('cikmis', s['etiketler'])

    def test_oncul_cevaplari_bagimsiz_hesaplanir(self):
        for g in self.config:
            mode = g.get('mode', 'pairs')
            canon = {f[0]: f[1] for f in g['facts']}
            if mode == 'context':
                for sid, f in zip(g['ids'], g['facts']):
                    self.assertEqual(self.rows[sid][2], f[0])
                    self.assertEqual(self.rows[sid][3], f[1])
                continue
            for sid in g['ids']:
                with self.subTest(group=g['key'], sid=sid):
                    row = self.rows[sid]
                    lines = row[2].split(r'\n')
                    if len(lines) == 2:  # Doğrudan kavram eşleştirmesi
                        self.assertEqual(row[3], canon[lines[0]])
                        self.assertNotIn(canon[lines[0]], row[4:8])
                        continue
                    self.assertEqual(len(lines), 4)
                    truths = []
                    for line, label in zip(lines[:3], ('I. ', 'II. ', 'III. ')):
                        self.assertTrue(line.startswith(label))
                        value = line[len(label):]
                        if mode == 'judgement':
                            truths.append(bool(canon[value]))
                        else:
                            lhs, rhs = value.split(' → ')
                            truths.append(canon[lhs] == rhs)
                    self.assertEqual(row[3], independent_answer(truths))

    def test_ayni_onculler_sadece_yer_degistirerek_tekrarlanmaz(self):
        for g in self.config:
            seen = set()
            for sid in g['ids']:
                lines = self.rows[sid][2].split(r'\n')
                if len(lines) != 4:
                    continue
                if g.get('mode') == 'judgement':
                    fingerprint = tuple(sorted(l.split('. ', 1)[1] for l in lines[:3]))
                else:
                    fingerprint = tuple(sorted(l.split('. ', 1)[1].split(' → ')[0] for l in lines[:3]))
                self.assertNotIn(fingerprint, seen, (g['key'], sid))
                seen.add(fingerprint)

    def test_konu_ve_id_plani(self):
        keys = set()
        for g in self.config:
            self.assertNotIn(g['key'], keys)
            keys.add(g['key'])
            self.assertEqual(len(g['ids']), 10)
            for sid in g['ids']:
                self.assertEqual(self.bank[sid]['ders'], g['ders'])
                self.assertIn(self.bank[sid]['konu'], g['topics'])


if __name__ == '__main__':
    unittest.main()
