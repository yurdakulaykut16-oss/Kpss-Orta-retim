#!/usr/bin/env python3
"""1500'lük parti: editoryal cevap türetme, sabit plan ve güvenli aktarım.

Cevaplar üreticinin truth/answer çıktısına güvenmeden, kökteki yargılar
editörün doğru/yanlış çiftlerine eşlenerek hesaplanır. Bu hesap bilgi
çiftlerinin dış dünyadaki doğruluğunu veya KPSS güçlüğünü kanıtlamaz.
"""
import collections
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from parti_1500_uret import ROOT, PLAN, FILES, SUBJECTS, build, read_editor, digest, create_plan
from soru_yukselt import main, yukseltilen_banka

ANSWERS = {
    (True,False,False):'Yalnız I', (False,True,False):'Yalnız II',
    (False,False,True):'Yalnız III', (True,True,False):'I ve II',
    (True,False,True):'I ve III', (False,True,True):'II ve III',
    (True,True,True):'I, II ve III',
}


class Parti1500Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output, cls.audit = build(ROOT)
        cls.rows = {r[0]:r for rows in cls.output.values() for r in rows}
        cls.plan = json.loads((ROOT / PLAN).read_text())
        cls.groups = {g['key']:g for g in read_editor(ROOT)}
        cls.bank = {s['id']:s for d in SUBJECTS for s in
                    map(json.loads, (ROOT/f'data/sorular/{d}.jsonl').read_text().splitlines())}

    def test_300er_soru_1306_yenileme_194_ekleme(self):
        self.assertEqual({d:len(r) for d,r in self.output.items()}, dict.fromkeys(SUBJECTS,300))
        self.assertEqual(len(self.rows),1500)
        targets = self.plan['targets']
        self.assertEqual(sum(t['new'] for t in targets),194)
        self.assertEqual(sum(not t['new'] for t in targets),1306)
        self.assertEqual(collections.Counter(t['ders'] for t in targets if t['new']),
                         {'tarih':71,'turkce':76,'guncel':47})
        self.assertEqual(len(self.bank),2865)

    def test_tekrar_uretim_tsv_ile_ayni(self):
        for d,rows in self.output.items():
            actual=[l.split('|') for l in (ROOT/'data/kaynaklar'/FILES[d]).read_text().splitlines()
                    if l and not l.startswith('#')]
            self.assertEqual(actual,rows)
        self.assertEqual(build(ROOT),(self.output,self.audit))

    def test_her_cevabi_kokten_bagimsiz_turet(self):
        for sid,row in self.rows.items():
            with self.subTest(sid=sid):
                group=self.groups[self.audit[sid]['group']]
                truth_by_text={text:yes for good,bad,why in group['facts']
                               for text,yes in ((good,True),(bad,False))}
                lines=row[2].split(r'\n')
                truths=tuple(truth_by_text[l.split('. ',1)[1]] for l in lines[:-1])
                if len(truths)==3:
                    expected=ANSWERS[truths]
                else:
                    self.assertEqual(len(truths),5)
                    looking_for_false=lines[-1].endswith('yanlıştır?')
                    matching=[i+1 for i,t in enumerate(truths) if t != looking_for_false]
                    self.assertEqual(len(matching),1)
                    expected=f'{matching[0]}. değerlendirme'
                self.assertEqual(row[3],expected)
                self.assertEqual(row[3:8].count(expected),1)
                self.assertEqual(self.bank[sid]['siklar'][self.bank[sid]['dogru']],expected)

    def test_salt_sira_veya_dogruluk_deseni_varyanti_yok(self):
        seen=collections.defaultdict(set)
        for sid,proof in self.audit.items():
            key=tuple(sorted(proof['indices']))
            self.assertNotIn(key,seen[proof['group']],sid)
            seen[proof['group']].add(key)
        self.assertEqual(len({r[2] for r in self.rows.values()}),1500)

    def test_tum_bilgiler_kullaniliyor_turler_ve_siklar_var(self):
        used=collections.defaultdict(set)
        modes=collections.Counter()
        for proof in self.audit.values():
            used[proof['group']].update(proof['indices'])
            modes[proof['mode']]+=1
        for k,g in self.groups.items():
            self.assertEqual(used[k],set(range(len(g['facts']))),k)
        self.assertEqual(modes,{'combo':899,'negative':306,'positive':295})
        for d,rows in self.output.items():
            positions=collections.Counter(self.bank[r[0]]['dogru'] for r in rows)
            self.assertEqual(set(positions),set(range(5)))
            self.assertTrue(all(35 <= n <= 90 for n in positions.values()))

    def test_kaynaklar_onceki800_ve_kalan10_degismedi(self):
        self.assertEqual(len(self.plan['untouched']),1365)
        for sid,sha in self.plan['untouched'].items():
            self.assertEqual(digest(self.bank[sid]),sha,sid)
        protected=[s for s in self.bank.values() if s['kaynak'] not in
                   ('KPSS formatında','Çıkmış KPSS sorusudur (yeniden düzenlendi)')]
        self.assertEqual(len(protected),555)
        self.assertTrue(all(s['id'] in self.plan['untouched'] for s in protected))

    def test_plan_son_icerik_ve_konu_eslesmesi(self):
        for t in self.plan['targets']:
            s=self.bank[t['id']]
            self.assertEqual((s['id'],s['ders'],s['gun'],s['konu']),
                             (t['id'],t['ders'],t['gun'],t['konu']))
            self.assertEqual(digest(s),t['after'])
            self.assertEqual(s['kok'],self.rows[t['id']][2].replace(r'\n','\n'))
            self.assertEqual(s['kaynak'],'KPSS formatında')
            self.assertEqual(len(set(s['siklar'])),5)
        bank,counts=yukseltilen_banka(ROOT)
        self.assertEqual(sum(counts.values()),2300)
        self.assertEqual({s['id']:s for d,(_,rs) in bank.items() for s in rs},self.bank)

    def fixture(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root=Path(tmp.name)
        shutil.copytree(ROOT/'data/sorular',root/'data/sorular')
        (root/'data/kaynaklar').mkdir()
        shutil.copy(ROOT/PLAN,root/PLAN)
        for p in (ROOT/'data/kaynaklar').glob('yukselt_*.tsv'):
            shutil.copy(p,root/'data/kaynaklar'/p.name)
        return root

    def snapshot(self,root):
        return {p.name:p.read_bytes() for p in (root/'data/sorular').glob('*.jsonl')}

    def test_plan_uzerine_yazilmaz(self):
        with self.assertRaisesRegex(ValueError,'zaten var'):
            create_plan(ROOT)

    def test_yeni_id_kayipsa_plan_tek_kopya_ekler(self):
        root=self.fixture()
        t=next(t for t in self.plan['targets'] if t['new'])
        path=root/f'data/sorular/{t["ders"]}.jsonl'
        rows=[json.loads(l) for l in path.read_text().splitlines()]
        path.write_text('\n'.join(json.dumps(s,ensure_ascii=False) for s in rows if s['id']!=t['id'])+'\n')
        before=self.snapshot(root)
        bank,_=yukseltilen_banka(root)
        added=[s for s in bank[t['ders']][1] if s['id']==t['id']]
        self.assertEqual(added,[self.bank[t['id']]])
        self.assertEqual(before,self.snapshot(root))  # saf fonksiyon diske yazmaz

    def test_son_tsv_hatasinda_hicbir_bankaya_yazma_yok(self):
        root=self.fixture()
        p=root/'data/kaynaklar'/FILES['guncel']
        text=p.read_text(); lines=text.splitlines();lines[-1]+=' İçeriğe beklenmeyen ek.'
        p.write_text('\n'.join(lines)+'\n')
        before=self.snapshot(root)
        with self.assertRaisesRegex(ValueError,'uyuşmazlığı'):
            main(root)
        self.assertEqual(before,self.snapshot(root))

    def test_plan_gercek_cikmis_korumasini_asamaz(self):
        root=self.fixture()
        plan=json.loads((root/PLAN).read_text())
        protected=next(s for s in self.bank.values() if s['kaynak'].startswith('2024-KPSS'))
        target=next(t for t in plan['targets'] if t['ders']==protected['ders'])
        target.update(id=protected['id'], before=digest(protected), gun=protected['gun'])
        (root/PLAN).write_text(json.dumps(plan,ensure_ascii=False))
        before=self.snapshot(root)
        with self.assertRaisesRegex(ValueError,'değiştirilemez'):
            main(root)
        self.assertEqual(before,self.snapshot(root))

    def test_beklenmeyen_yerel_duzenleme_sessizce_ezilmez(self):
        root=self.fixture()
        t=self.plan['targets'][0]
        p=root/f'data/sorular/{t["ders"]}.jsonl'
        rows=[json.loads(l) for l in p.read_text().splitlines()]
        next(s for s in rows if s['id']==t['id'])['kok']='Kullanıcının yerel düzeltmesi'
        p.write_text('\n'.join(json.dumps(s,ensure_ascii=False) for s in rows)+'\n')
        before=self.snapshot(root)
        with self.assertRaisesRegex(ValueError,'beklenmeyen içerik'):
            main(root)
        self.assertEqual(before,self.snapshot(root))


if __name__=='__main__':
    unittest.main()
