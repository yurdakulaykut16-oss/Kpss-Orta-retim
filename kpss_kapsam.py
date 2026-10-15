"""Soru servisinin kapalı-varsayılan geçmiş KPSS konu kapsamı.

Konu örnekleri bankadaki yıl/oturum etiketli kayıtlardır. Konu eşleştirmesi,
özgün sorunun geçmişte sorulduğunu veya her alt bilgisinin aynı sınavda
bulunduğunu ileri sürmez; bağımsız kitapçık doğrulaması yerine geçmez.
Ham banka korunur. Yeni/değişmiş/onaysız kayıt çözüm API'sine geçmez.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POLICY_PATH = 'data/kpss_kapsam.json'
SUBJECTS = ('tarih', 'cografya', 'vatandaslik', 'turkce', 'guncel')


def record_hash(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def read_policy(root=ROOT):
    policy = json.loads((root / POLICY_PATH).read_text(encoding='utf-8'))
    if policy.get('version') != 1 or policy.get('mode') != 'gecmis-kpss-konulari':
        raise ValueError('Geçersiz KPSS konu kapsamı')
    return policy


def filter_bank(bank, policy):
    """Disk yazmadan kayıt özetini, konu onayını ve dayanaklarını doğrula.

    Etiket tek başına onay değildir. Dayanak sorusu başka dersten alınamaz.
    Dayanağın değişmesi o konuyu da onaysız bırakır. İnceleme bekleyen
    soruların soru metinleri kapsam raporuna veya aktif API'ye konmaz.
    """
    index = {}
    for ders, rows in bank.items():
        for s in rows:
            if s['id'] in index or s['ders'] != ders:
                raise ValueError('Banka kimliği/dersi tutarsız')
            index[s['id']] = s
    topics = policy['topics']
    # Aynı yılın hangi oturumunun yapıldığını tahmin etme: konu dayanakları
    # yalnız inceleme yılından önceki tamamlanmış yıllardan seçilir.
    last_reference_year = int(policy['review_date'][:4]) - 1
    valid = {}
    for key, topic in topics.items():
        refs = topic.get('references', [])
        valid[key] = bool(refs) and topic['ders'] in SUBJECTS
        for ref in refs:
            s = index.get(ref['id'])
            valid[key] = valid[key] and bool(
                s and s['ders'] == topic['ders'] and
                re.fullmatch(r'20\d{2}-KPSS(?: (?:Lisans|Ön Lisans|Ortaöğretim))?', s.get('kaynak', '')) and
                int(s['kaynak'][:4]) <= last_reference_year and
                s['kaynak'] == ref['kaynak'] and record_hash(s) == ref['sha256']
            )
    active = {d: [] for d in bank}
    excluded = {}
    for ders, rows in bank.items():
        for s in rows:
            review = policy['questions'].get(s['id'])
            reason = None
            if review is None:
                reason = 'Yeni kayıt: konu kapsamı incelemesi yapılmadı.'
            elif review.get('sha256') != record_hash(s):
                reason = 'İçerik değişti: konu kapsamı yeniden incelenmeli.'
            elif review.get('status') != 'aktif':
                reason = review.get('reason', 'Konu dayanağı inceleme bekliyor.')
            else:
                keys = review.get('topics', [])
                if not keys or len(keys) != len(set(keys)) or any(
                    not valid.get(k) or topics[k]['ders'] != ders for k in keys
                ):
                    reason = 'Konu örneği eksik, değişmiş veya başka derse ait.'
            if reason:
                excluded[s['id']] = dict(ders=ders, gerekce=reason)
                continue
            references = {r['id']: r for k in keys for r in topics[k]['references']}
            active[ders].append({**s, 'kpss_kapsam': dict(
                konular=[dict(id=k, ad=topics[k]['ad']) for k in keys],
                ornekler=[dict(id=r['id'], kaynak=r['kaynak']) for r in references.values()],
                tur='konu-eslestirmesi',
            )})
    counts = {d: dict(arsiv=len(bank[d]), aktif=len(active[d]), bekleyen=len(bank[d])-len(active[d]))
              for d in bank}
    report = dict(mode=policy['mode'], aciklama=policy['notice'], dersler=counts,
                  aktif=sum(len(r) for r in active.values()),
                  bekleyen=len(excluded), bekleyen_kayitlar=excluded)
    return active, report


def project_exams(exams, raw_bank, active_bank):
    """Denemeleri salt bellekte, ders dağılımını koruyarak aktif havuza yansıt.

    Arşivdeki/saklanmış sonuçlardaki kimlikler değişmez. Aktif olmayan veya
    tekrarlanan bir soru yerine aynı dersten başka onaylı kayıt seçilir.
    Yeterli onaylı soru yoksa kapsam dışı soruyla doldurmak yerine hata verir.
    """
    raw = {s['id']: s for rows in raw_bank.values() for s in rows}
    approved = {s['id']: s for rows in active_bank.values() for s in rows}
    result = copy.deepcopy(exams)
    for exam in result['denemeler']:
        old_ids = exam['sorular']
        if any(sid not in raw for sid in old_ids):
            raise ValueError(f"Deneme arşivinde bilinmeyen soru: {exam['id']}")
        # Kullanılabilir özgün seçimleri önce rezerve et; bir değiştirme
        # daha sonraki geçerli soruyu yanlışlıkla tüketmesin.
        reserved = set(old_ids) & approved.keys()
        seen = set()
        new_ids = []
        for slot, sid in enumerate(old_ids):
            if sid in approved and sid not in seen:
                chosen = sid
            else:
                original = raw[sid]
                candidates = [s for s in active_bank[original['ders']]
                              if s['id'] not in seen and s['id'] not in reserved]
                if not candidates:
                    raise ValueError(f"{exam['id']}: onaylı aynı ders sorusu yetersiz")
                def rank(s):
                    return (s['gun'] != original['gun'],
                            not bool(re.match(r'^\d{4}-KPSS', s['kaynak'])),
                            hashlib.sha256(f"{exam['id']}:{slot}:{s['id']}".encode()).hexdigest())
                chosen = min(candidates, key=rank)['id']
            seen.add(chosen)
            new_ids.append(chosen)
        exam['sorular'] = new_ids
        exam['kapsam_degisen_soru'] = sum(a != b for a, b in zip(old_ids, new_ids))
    return result
