#!/usr/bin/env python3
"""5 x 300 özgün çalışma sorusu; editoryal karar çiftlerinden üretim.

Aynı bilgi kümesi, doğruluk deseni veya şık sırası değiştirilerek ikinci kez
kullanılmaz. Bir kümedeki farklı bilgilerle yeni kümeler kurmak mümkündür;
bunlar 1500 ayrı elle yazılmış senaryo veya psikometrik kalibrasyon değildir.
--plan yalnızca ilk hedef planını oluşturur; normal kullanım TSV üretir.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

from parti_500_uret import combo, rng_for, PATTERNS

ROOT = Path(__file__).resolve().parent.parent
SUBJECTS = ('tarih', 'cografya', 'vatandaslik', 'turkce', 'guncel')
FILES = {d: f'yukselt_{i}_{d}_300.tsv' for i, d in enumerate(SUBJECTS, 20)}
EDITOR = 'data/kaynaklar/parti_1500_editor.txt'
PLAN = 'data/kaynaklar/parti_1500_plan.json'
SOURCES = ('KPSS formatında', 'Çıkmış KPSS sorusudur (yeniden düzenlendi)')


def digest(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def read_editor(root=ROOT):
    groups = []
    for no, line in enumerate((root / EDITOR).read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            ders, topic = line[1:].split('|')
            groups.append(dict(key=f'{ders}-{sum(g["ders"] == ders for g in groups)+1}',
                               ders=ders, konu=topic, facts=[]))
        else:
            fields = line.split('|')
            if len(fields) != 3 or not all(fields) or not groups:
                raise ValueError(f'Editör satırı {no}: doğru, yanlış, gerekçe gerekir')
            if fields[0] == fields[1]:
                raise ValueError(f'Aynı doğru/yanlış önerme: {no}')
            groups[-1]['facts'].append(fields)
    # Ek dosya her modüle bir uygulama/çıkarım yargısı ekler. Aynı soru
    # sayısına dahildir; ayrı bir parti veya yeni id üretmez.
    by_topic = {(g['ders'], g['konu']): g for g in groups}
    extras = root / 'data/kaynaklar/parti_1500_senaryolar.txt'
    seen_extra = set()
    for no, line in enumerate(extras.read_text().splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        fields = line.split('|')
        if len(fields) != 5 or not all(fields):
            raise ValueError(f'Senaryo {no}: beş dolu alan gerekir')
        key = tuple(fields[:2])
        if key not in by_topic or key in seen_extra:
            raise ValueError(f'Senaryo grubu eksik/tekrarlı: {key}')
        seen_extra.add(key)
        by_topic[key]['facts'].append(fields[2:])
    if seen_extra != set(by_topic):
        raise ValueError('Her modüle bir uygulama yargısı gerekir')
    for d in SUBJECTS:
        modules = [g for g in groups if g['ders'] == d]
        if not modules:
            raise ValueError(f'Eksik ders: {d}')
        for i, g in enumerate(modules):
            g['count'] = 300 // len(modules) + (i < 300 % len(modules))
            if len(g['facts']) < 8:
                raise ValueError(f'En az 8 karar çifti: {g["key"]}')
            sentences = [s for f in g['facts'] for s in f[:2]]
            if len(set(sentences)) != len(sentences):
                raise ValueError(f'Tekrarlanan editoryal önerme: {g["key"]}')
    return groups


def old_manifest_ids(root):
    ids = set()
    for path in (root / 'data/kaynaklar').glob('yukselt_*.tsv'):
        if path.name in FILES.values():
            continue
        for line in path.read_text().splitlines():
            if line.strip() and not line.startswith('#'):
                ids.add(line.split('\t' if '\t' in line else '|')[0])
    return ids


def create_plan(root=ROOT):
    path = root / PLAN
    if path.exists():
        raise ValueError('Sabit plan zaten var; üzerine yazılmaz')
    groups = read_editor(root)
    used = old_manifest_ids(root)
    bank = {d: [json.loads(l) for l in (root / f'data/sorular/{d}.jsonl').read_text().splitlines() if l]
            for d in SUBJECTS}
    all_ids = {s['id'] for rows in bank.values() for s in rows}
    targets = []
    for d in SUBJECTS:
        remaining = [s for s in bank[d] if s['id'] not in used and s['kaynak'] in SOURCES]
        # Coğrafya ve vatandaşlıkta 300 sınırı nedeniyle 6+4 kayıt sonraya kalır.
        selected = remaining[:300]
        extra = max(0, 300-len(selected))
        prefix = {'tarih':'TAR', 'cografya':'COG', 'vatandaslik':'VAT', 'turkce':'TUR', 'guncel':'GUN'}[d]
        for i in range(extra):
            sid = f'{prefix}-YENI-{i+1:04}'
            if sid in all_ids:
                raise ValueError(f'Yeni id çakışması: {sid}')
            selected.append(dict(id=sid, ders=d, gun=1+(i % 2), konu='',
                                 kaynak=SOURCES[0], etiketler=[]))
        # Önce eski konuya uyan kayıtlar, sonra kalan özgün kayıtlar.
        for g in (g for g in groups if g['ders'] == d):
            chosen = [s for s in selected if s['konu'] == g['konu']][:g['count']]
            chosen += [s for s in selected if s not in chosen][:g['count']-len(chosen)]
            for s in chosen:
                selected.remove(s)
                new = s['id'] not in all_ids
                targets.append(dict(id=s['id'], ders=d, gun=s['gun'], group=g['key'],
                                    konu=g['konu'], old_konu=s['konu'], new=new,
                                    before=None if new else digest(s)))
        if selected:
            raise ValueError('Atanmayan hedef')
    target_ids = {t['id'] for t in targets}
    untouched = {s['id']: digest(s) for rows in bank.values() for s in rows if s['id'] not in target_ids}
    plan = dict(version=1, baseline='119d02b', targets=targets, untouched=untouched)
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n')
    return plan


def make_question(g, n, used):
    rng = rng_for('quality1500:'+g['key']+':'+str(n))
    # Üç öncül; beş yargıdan doğruyu bulma; beş yargıdan yanlışı bulma.
    mode = ('combo', 'negative', 'combo', 'positive', 'combo')[n % 5]
    size = 3 if mode == 'combo' else 5
    candidates = [c for c in itertools.combinations(range(len(g['facts'])), size) if c not in used]
    if not candidates:
        raise ValueError('Farklı içerik kümesi kalmadı: '+g['key'])
    chosen = rng.choice(candidates)
    used.add(chosen)
    indices = list(chosen)
    rng.shuffle(indices)
    if mode == 'combo':
        patterns = list(PATTERNS)
        rng_for('1500-pattern:'+g['key']).shuffle(patterns)
        truth = patterns[(n // 5 * 3 + (0,0,1,0,2)[n % 5]) % 7]
    else:
        wanted = rng.randrange(5)
        truth = tuple((i != wanted) if mode == 'negative' else (i == wanted) for i in range(5))
    labels = ('I', 'II', 'III') if mode == 'combo' else ('1', '2', '3', '4', '5')
    statements, solutions = [], []
    for label, i, yes in zip(labels, indices, truth):
        good, bad, why = g['facts'][i]
        statements.append(good if yes else bad)
        solutions.append(f'{label}: '+('Doğru. ' if yes else 'Yanlış. Doğrusu: '+good+' ')+why)
    if mode == 'combo':
        stem = '\n'.join(f'{label}. {text}' for label, text in zip(labels, statements))
        stem += '\nYukarıdaki değerlendirmelerden hangileri doğrudur?'
        correct = combo(truth)
        wrongs = rng.sample([combo(p) for p in PATTERNS if p != truth], 4)
        z = 3
    else:
        stem = ('Aşağıdaki değerlendirmelerden hangisi '+('yanlıştır?' if mode == 'negative' else 'doğrudur?'))
        correct = statements[wanted]
        wrongs = [s for i, s in enumerate(statements) if i != wanted]
        # Çözümdeki 1–5 atıfları kökteki yargılardır; şıkların A–E
        # sırasına bağlı değildir. Şık karışınca açıklama bozulmaz.
        z = 2
    if mode != 'combo':
        # Tek köklü fakat farklı seçenek kümeli maddeleri bankanın kök tekillik
        # kuralına uydurmak için seçenekleri köke taşımak yerine alan bağlamı ver.
        # Sorulara yapay sıra numarası eklenmez: beş bilgi kökte de okunur,
        # seçenekler bu yargıların numaralarıdır; böylece içerik kökün parçasıdır.
        stem = '\n'.join(f'{i+1}. {s}' for i, s in enumerate(statements))+'\n'+stem.replace('Aşağıdaki', 'Yukarıdaki')
        correct = f'{wanted+1}. değerlendirme'
        wrongs = [f'{i+1}. değerlendirme' for i in range(5) if i != wanted]
    return z, stem, correct, wrongs, ' '.join(solutions), dict(mode=mode, indices=indices, truth=list(truth))


def build(root=ROOT):
    groups = read_editor(root)
    plan = json.loads((root / PLAN).read_text())
    by_group = {}
    for t in plan['targets']:
        by_group.setdefault(t['group'], []).append(t)
    output = {d: [] for d in SUBJECTS}
    audit = {}
    stems = set()
    for g in groups:
        targets = by_group[g['key']]
        if len(targets) != g['count']:
            raise ValueError('Plan/editör sayısı uyumsuz')
        used = set()
        for n, t in enumerate(targets):
            z, stem, correct, wrongs, solution, evidence = make_question(g, n, used)
            if stem in stems:
                raise ValueError('Tekrarlanan kök')
            stems.add(stem)
            row = [t['id'], str(z), stem.replace('\n', r'\n'), correct, *wrongs, solution]
            if len(set(row[3:8])) != 5 or any('|' in s or '\t' in s or '\n' in s or not s for s in row):
                raise ValueError('Geçersiz madde')
            output[t['ders']].append(row)
            audit[t['id']] = dict(group=g['key'], **evidence)
    if {d:len(v) for d,v in output.items()} != dict.fromkeys(SUBJECTS, 300):
        raise ValueError('Her dersten tam 300 gerekir')
    if len({r[0] for v in output.values() for r in v}) != 1500:
        raise ValueError('1500 tekil id gerekir')
    return output, audit


def final_record(base, target, row):
    import random
    s = copy.deepcopy(base)
    options = row[3:8].copy()
    random.Random(f'{target["id"]}-yukselt').shuffle(options)
    s.update(id=target['id'], ders=target['ders'], gun=target['gun'], konu=target['konu'],
             kok=row[2].replace(r'\n', '\n'), zorluk=int(row[1]), siklar=options,
             dogru=options.index(row[3]), kaynak=SOURCES[0],
             cozumler=[dict(yontem='KPSS mantığı ile çözüm', metin=row[8])],
             etiketler=[x for x in s.get('etiketler', []) if x != 'cikmis'])
    return s


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    if args.plan:
        create_plan()
    output, audit = build()
    plan = json.loads((ROOT / PLAN).read_text())
    bank = {s['id']: s for d in SUBJECTS for s in
            map(json.loads, (ROOT / f'data/sorular/{d}.jsonl').read_text().splitlines())}
    rows = {r[0]:r for v in output.values() for r in v}
    for target in plan['targets']:
        base = bank.get(target['id'], {})
        after = digest(final_record(base, target, rows[target['id']]))
        if target.get('after') not in (None, after):
            raise ValueError('Sabit içerik değişti: plan ve editör birlikte incelenmeli')
        target['after'] = after
    (ROOT / PLAN).write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n')
    for d, result in output.items():
        (ROOT / 'data/kaynaklar' / FILES[d]).write_text(
            '# Özgün editoryal değerlendirme soruları; kitap/ÖSYM alıntısı değildir.\n'+
            '\n'.join('|'.join(r) for r in result)+'\n')
        print(d, len(result))
    print('Yeni:', sum(t['new'] for t in plan['targets']), 'Yenilenen:', sum(not t['new'] for t in plan['targets']))


if __name__ == '__main__':
    main()
