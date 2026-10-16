#!/usr/bin/env python3
"""Elle yazılmış yeni soru partileri (data/kaynaklar/yeni_parti_*.tsv).

Her satır kendi kökü, beş seçeneği ve gerekçeli çözümüyle ayrı bir sorudur;
otomatik varyant üretilmez. Yalnız şık sırası id'ye bağlı olarak deterministik
karıştırılır. Sütunlar (| ile):

    id | konu | zorluk | kök | doğru | yanlış1 | yanlış2 | yanlış3 | yanlış4 | gerekçe

- id: TAR-YS-0001, COG-YS-…, VAT-YS-…, TUR-YS-…, GUN-YS-… (ön ek dersi belirler)
- konu: bankadaki konu başlığı; kpss_kapsam.json içindeki bir konu takma adı olmalı
- kökte satır sonu için \\n yazılır
- yeni_parti_16_<ders>.tsv dosyaları elle yazılmaz; araclar/bilgi_soru_uret.py ile
  araclar/bilgi_veri/<ders>.py bilgi tablolarından üretilir ve 'bilgi-tablosu' etiketi alır

Kullanım:
    python3 araclar/ek_yeni_sorular.py --onayla   # kapsam onaylarını yazar
    python3 araclar/soru_yukselt.py               # bankaya ekler (soru_yukselt bunu çağırır)
"""
import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kpss_kapsam import record_hash, question_key  # noqa: E402

PATTERN = 'yeni_parti_*.tsv'
PREFIX = {'TAR': 'tarih', 'COG': 'cografya', 'VAT': 'vatandaslik', 'TUR': 'turkce', 'GUN': 'guncel'}
REASON = ('Elle yazılmış yeni soru partisi; belirtilen geçmiş KPSS konu alanında incelendi. '
          'Birebir çıkmış soru değildir.')


def topic_map(root=ROOT):
    policy = json.loads((root / 'data/kpss_kapsam.json').read_text(encoding='utf-8'))
    result = {}
    for key, t in policy['topics'].items():
        for alias in t.get('aliases', []):
            result[(t['ders'], alias)] = key
    return result


def build(root=ROOT):
    files = sorted((root / 'data/kaynaklar').glob(PATTERN))
    records, keys, seen_roots = [], {}, set()
    if not files:  # parti yoksa kapsam dosyasına gerek yok (izole test kökleri)
        return records, keys
    topics = topic_map(root)
    for tsv in files:
        for no, line in enumerate(tsv.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip() or line.startswith('#'):
                continue
            where = f'{tsv.name}:{no}'
            p = [x.strip() for x in line.split('|')]
            if len(p) != 10 or not all(p):
                raise ValueError(f'{where}: 10 dolu alan gerekir ({len(p)})')
            sid, konu, z, stem, correct, *rest = p
            parts = sid.split('-')
            ders = PREFIX.get(parts[0])
            if not ders or len(parts) != 3 or parts[1] != 'YS' or not parts[2].isdigit():
                raise ValueError(f'{where}: geçersiz id {sid}')
            if sid in keys:
                raise ValueError(f'{where}: yinelenen id {sid}')
            if (ders, konu) not in topics:
                raise ValueError(f'{where}: konu kapsamda yok: {ders}|{konu}')
            if z not in ('2', '3'):
                raise ValueError(f'{where}: zorluk 2 veya 3 olmalı')
            options = [correct, *rest[:4]]
            if len({x.casefold() for x in options}) != 5:
                raise ValueError(f'{where}: beş farklı şık gerekir')
            random.Random(sid + '-yeni-parti').shuffle(options)
            n = int(parts[2])
            s = dict(id=sid, ders=ders, gun=1 + (n - 1) % 10, konu=konu, zorluk=int(z),
                     kok=stem.replace(r'\n', '\n'), siklar=options, dogru=options.index(correct),
                     kaynak='KPSS formatında',
                     etiketler=['ozgun', 'yeni-parti'] + (['bilgi-tablosu'] if tsv.name.startswith('yeni_parti_16_') else []),
                     cozumler=[dict(yontem='KPSS mantığı ile çözüm', metin=rest[4])])
            root_key = question_key(s)
            if root_key in seen_roots:
                raise ValueError(f'{where}: aynı kök partide iki kez var')
            seen_roots.add(root_key)
            records.append(s)
            keys[sid] = topics[(ders, konu)]
    return records, keys


def add_to_bank(root, by_ders, index):
    records, _ = build(root)
    existing_roots = {question_key(s) for sid, s in index.items() if not sid.split('-')[1:2] == ['YS']}
    for s in records:
        if s['id'] in index:
            if index[s['id']] != s:
                # Bilgi tablosu üreticisinin çıktısı (yeni_parti_16_*) tablodan yeniden üretilebilir:
                # aynı kimlikli kayıt yeni içerikle yerinde değiştirilir. Elle yazılmış partiler korunur.
                if 'bilgi-tablosu' not in s['etiketler'] or 'bilgi-tablosu' not in index[s['id']].get('etiketler', []):
                    raise ValueError('Yeni parti kaydı beklenmeyen içerikle değişti: ' + s['id'])
                rows = by_ders[s['ders']][1]
                rows[next(i for i, r in enumerate(rows) if r['id'] == s['id'])] = s
                index[s['id']] = s
            continue
        if question_key(s) in existing_roots:
            raise ValueError('Yeni parti kökü bankadaki bir soruyla aynı: ' + s['id'])
        index[s['id']] = s
        by_ders[s['ders']][1].append(s)


def approve(root=ROOT):
    """Kayıt özetleriyle kapsam onayı yazar; başka kayıtlara dokunmaz."""
    records, keys = build(root)
    path = root / 'data/kpss_kapsam.json'
    policy = json.loads(path.read_text(encoding='utf-8'))
    changed = 0
    for s in records:
        entry = dict(sha256=record_hash(s), status='aktif', topics=[keys[s['id']]], reason=REASON)
        if policy['questions'].get(s['id']) != entry:
            policy['questions'][s['id']] = entry
            changed += 1
    original = path.read_text(encoding='utf-8')
    indent = 2 if original.startswith('{\n  "') else 1
    text = json.dumps(policy, ensure_ascii=False, indent=indent) + ('\n' if original.endswith('\n') else '')
    if text != original:
        path.write_text(text, encoding='utf-8')
    return len(records), changed


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--onayla', action='store_true', help='kapsam onaylarını data/kpss_kapsam.json içine yaz')
    args = ap.parse_args()
    if args.onayla:
        total, changed = approve()
        print(f'{total} yeni soru; {changed} kapsam kaydı güncellendi')
    else:
        records, _ = build()
        from collections import Counter
        print(len(records), dict(Counter(s['ders'] for s in records)))
