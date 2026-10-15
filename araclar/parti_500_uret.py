#!/usr/bin/env python3
"""Editoryal bilgi tablolarından 5 x 100 özgün yeniden yazım üretir.

Bilgi tabloları elle hazırlanmıştır; dış kaynaktan/kitaptan alıntı değildir.
Eşleştirme öncülleri, cümle değerlendirmeleri ve bağlam soruları kullanılır.
Şıkları yeniden sıralayarak aynı öncül kümesi ikinci soru sayılmaz.
Çalıştırma TSV üretir; bankaya uygulamak için soru_yukselt.py çalıştırılır.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'data/kaynaklar/parti_500_editor.json'
FILES = {d: f'yukselt_{i}_{d}_100.tsv' for i, d in enumerate(
    ('tarih', 'cografya', 'vatandaslik', 'turkce', 'guncel'), 15)}
LETTERS = ('I', 'II', 'III')
PATTERNS = tuple(itertools.product((False, True), repeat=3))[1:]


def combo(pattern):
    selected = [x for x, yes in zip(LETTERS, pattern) if yes]
    if len(selected) == 1:
        return 'Yalnız ' + selected[0]
    if len(selected) == 3:
        return 'I, II ve III'
    return ' ve '.join(selected)


def rng_for(key):
    return random.Random(hashlib.sha256(key.encode()).hexdigest())


def wrong_pool(group, lhs, canonical):
    override = group.get('wrong_answers', {}).get(lhs)
    if override is not None:
        return sorted(set(override) - {canonical})
    if 'types' in group:
        ix = next(i for i, f in enumerate(group['facts']) if f[0] == lhs)
        kind = group['types'][ix]
        values = [f[1] for f, k in zip(group['facts'], group['types']) if k == kind]
        values += group.get('distractors', {}).get(kind, [])
        return sorted(set(values) - {canonical})
    return sorted(set(f[1] for f in group['facts']) - {canonical})


def question(group, n, used):
    rng = rng_for(group['key'] + str(n))
    mode = group.get('mode', 'pairs')
    facts = group['facts']
    # Bağlam okuma sorularında her metin yalnızca bir kez kullanılır.
    if mode == 'context':
        stem, answer, explanation = facts[n]
        options = list(dict.fromkeys(f[1] for f in facts if f[1] != answer))
        wrongs = rng.sample(options, 4)
        return 2, stem, answer, wrongs, explanation

    # İki doğrudan kavram sorusu, sekiz çok öncüllü soru; ikili karar
    # tabloları ise yalnızca öncüllü değerlendirme soruları üretir.
    if mode == 'pairs' and n % 5 == 4 and len(set(f[1] for f in facts)) >= 5:
        order = list(range(len(facts)))
        rng_for(group['key']).shuffle(order)
        lhs, answer = facts[order[n // 5]]
        stem = f'{lhs}\nBu açıklama için doğru eşleştirme aşağıdakilerden hangisidir?'
        pool = wrong_pool(group, lhs, answer)
        if len(pool) >= 4:
            wrongs = rng.sample(pool, 4)
            explanation = f'Doğru eşleştirme: {lhs} → {answer}. ' + group.get('note', '')
            return 2, stem, answer, wrongs, explanation

    # Tekrarlanan öncül kümelerini (sıraları değişse bile) reddet.
    for attempt in range(1000):
        indices = rng.sample(range(len(facts)), 3)
        fingerprint = tuple(sorted(indices))
        if fingerprint not in used:
            used.add(fingerprint)
            break
    else:
        raise ValueError(f"Yetersiz farklı öncül kümesi: {group['key']}")
    pattern_order = list(PATTERNS)
    rng_for(group['key'] + '-answer-pattern').shuffle(pattern_order)
    target = pattern_order[n % len(pattern_order)]
    if mode == 'judgement':
        # İstenen özellik gerçekten var/yok olarak editörce işaretlenir.
        indices = []
        for yes in target:
            pool = [i for i, f in enumerate(facts) if bool(f[1]) == yes and i not in indices]
            indices.append(rng.choice(pool))
        # Bu türde de salt sıralama varyantlarına izin verme.
        for _ in range(1000):
            fp = ('judgement', *sorted(indices))
            if fp not in used:
                used.add(fp)
                break
            indices = []
            for yes in target:
                pool = [i for i, f in enumerate(facts) if bool(f[1]) == yes and i not in indices]
                indices.append(rng.choice(pool))
        else:
            raise ValueError('Tekrarlanan cümle kümesi')
        statements = [facts[i][0] for i in indices]
        solution = [f'{label}. {facts[i][2]}' for label, i in zip(LETTERS, indices)]
        ending = group['prompt']
    else:
        statements, solution = [], []
        for label, i, yes in zip(LETTERS, indices, target):
            lhs, canonical = facts[i]
            alternatives = wrong_pool(group, lhs, canonical)
            if not alternatives:
                raise ValueError(f'Çeldirici eksik: {lhs}')
            rhs = canonical if yes else rng.choice(alternatives)
            statements.append(f'{lhs} → {rhs}')
            solution.append(f'{label}. {"Doğru" if yes else "Yanlış"}: {lhs} → {canonical}.')
        ending = 'Yukarıdaki eşleştirmelerden hangileri doğrudur?'
    stem = '\n'.join(f'{label}. {s}' for label, s in zip(LETTERS, statements)) + '\n' + ending
    answer = combo(target)
    others = [combo(p) for p in PATTERNS if p != target]
    return 3, stem, answer, rng.sample(others, 4), ' '.join(solution) + ' ' + group.get('note', '')


def build(root=ROOT):
    cfg = json.loads((root / 'data/kaynaklar/parti_500_editor.json').read_text())
    output_names = set(FILES.values())
    used_ids = set()
    for tsv in (root / 'data/kaynaklar').glob('yukselt_*.tsv'):
        if tsv.name in output_names:
            continue
        for line in tsv.read_text().splitlines():
            if line.strip() and not line.lstrip().startswith('#'):
                used_ids.add(line.split('\t' if '\t' in line else '|')[0])
    bank = {}
    for ders in FILES:
        bank[ders] = [json.loads(l) for l in (root / f'data/sorular/{ders}.jsonl').read_text().splitlines() if l.strip()]
    result = {d: [] for d in FILES}
    all_stems, group_keys = set(), set()
    for g in cfg:
        if g['key'] in group_keys:
            raise ValueError('Yinelenen grup anahtarı')
        group_keys.add(g['key'])
        if len(g['facts']) < 6 or g['count'] > len(g['facts']) and g.get('mode') == 'context':
            raise ValueError('Yetersiz bilgi tablosu')
        if g.get('mode', 'pairs') == 'pairs':
            if len({f[0] for f in g['facts']}) != len(g['facts']):
                raise ValueError('Aynı açıklamaya farklı yanıt atanamaz')
        ders = g['ders']
        by_id = {s['id']: s for s in bank[ders]}
        ids = g.get('ids', [])
        if len(ids) != g['count'] or len(set(ids)) != len(ids):
            raise ValueError(f"Hedef id listesi eksik/tekrarlı: {g['key']}")
        candidates = []
        for sid in ids:
            s = by_id.get(sid)
            if not s or sid in used_ids or s['konu'] not in g['topics'] or s.get('kaynak') not in (
                'KPSS formatında', 'Çıkmış KPSS sorusudur (yeniden düzenlendi)'):
                raise ValueError(f"Korumalı, eksik veya uyumsuz hedef: {sid}")
            candidates.append(s)
        fingerprints = set()
        for n, old in enumerate(candidates[:g['count']]):
            z, stem, correct, wrongs, explanation = question(g, n, fingerprints)
            if stem in all_stems:
                raise ValueError('Tekrarlanan soru kökü')
            all_stems.add(stem)
            used_ids.add(old['id'])
            row = [old['id'], str(z), stem, correct, *wrongs, explanation.strip()]
            # TSV tek satırdır; kökteki satır sonları taşınabilir biçimde
            # saklanır ve soru_yukselt.py tarafından geri açılır.
            row = [s.replace('\n', r'\n').strip() for s in row]
            if any('|' in s or '\t' in s or not s for s in row):
                raise ValueError('Geçersiz alan')
            if len(set(row[3:8])) != 5:
                raise ValueError('Şıklar tekil olmalıdır')
            result[ders].append(row)
    if any(len(rows) != 100 for rows in result.values()):
        raise ValueError(f"Her dersten 100 olmalı: { {d: len(r) for d,r in result.items()} }")
    return result


def main():
    result = build()
    for ders, rows in result.items():
        path = ROOT / 'data/kaynaklar' / FILES[ders]
        path.write_text('# Elle hazırlanmış bilgi tablolarından özgün soru yeniden yazımı.\n' +
                        '\n'.join('|'.join(row) for row in rows) + '\n')
        print(f'{ders}: {len(rows)} soru → {path.name}')


if __name__ == '__main__':
    main()
