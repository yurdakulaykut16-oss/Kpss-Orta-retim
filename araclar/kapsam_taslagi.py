#!/usr/bin/env python3
"""Yeni/değişmiş sorular için ONAYSIZ kapsam taslağı hazırlar.

Konu etiketi ancak aday önerir; aktif izin vermez. Üretim kapsam dosyasını
veya bankayı yazmaz. İnceleme sonrası konu ve dayanaklarla ayrı onay gerekir.
python3 araclar/kapsam_taslagi.py --output /tmp/kapsam_taslak.json
"""
import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kpss_kapsam import read_policy, record_hash, SUBJECTS, POLICY_PATH


def draft(bank, policy):
    result = copy.deepcopy(policy)
    result['questions'] = {}
    for ders, rows in bank.items():
        for s in rows:
            old = policy['questions'].get(s['id'])
            sha = record_hash(s)
            if old and old.get('sha256') == sha:
                result['questions'][s['id']] = copy.deepcopy(old)
            else:
                candidates = [key for key,t in policy['topics'].items()
                              if t['ders'] == ders and s['konu'] in t.get('aliases', [])]
                result['questions'][s['id']] = dict(
                    sha256=sha, status='beklemede', topics=[], aday_konular=candidates,
                    reason='Yeni/değişmiş içerik: konu başlığı otomatik onay değildir; inceleme gerekir.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    destination = args.output.resolve()
    bank_dir = (ROOT / 'data/sorular').resolve()
    if destination == (ROOT / POLICY_PATH).resolve() or bank_dir in destination.parents:
        parser.error('Üretim kapsamına veya soru bankasına taslak yazılamaz')
    if destination.exists():
        parser.error('Var olan dosyanın üzerine yazılmaz; yeni bir taslak yolu seçin')
    bank = {d: [json.loads(l) for l in (ROOT/f'data/sorular/{d}.jsonl').read_text().splitlines() if l]
            for d in SUBJECTS}
    args.output.write_text(json.dumps(draft(bank, read_policy(ROOT)), ensure_ascii=False, indent=2)+'\n')
    print('Taslak hazır; yeni/değişmiş kayıtlar aktif değildir:', args.output)


if __name__ == '__main__':
    main()
