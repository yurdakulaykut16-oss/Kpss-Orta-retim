#!/usr/bin/env python3
"""Bilgi tablolarından (araclar/bilgi_veri/<ders>.py) tekrarsız KPSS soruları üretir.

Her ders modülü elle derlenmiş, yüksek güvenli bilgi tabloları (olay–yıl,
kavram–tanım, il–bölge, ülke–başkent, deyim–anlam vb.) ve bunlardan soru kuran
`uret(rng)` fonksiyonu içerir. Çeldiriciler aynı tablodaki başka kayıtlardan
seçilir; doğru cevap tablo kaydının kendisidir. Üretilen satırlar
data/kaynaklar/yeni_parti_16_<ders>.tsv dosyasına, *-YS-0651'den başlayan
kimliklerle yazılır ve araclar/ek_yeni_sorular.py ile bankaya eklenir.

Kurallar:
- Soru kökü (question_key) bankadaki ve önceki partilerdeki hiçbir kökle aynı olamaz;
  aynı kök üretilirse atlanır (aynı soru iki kez gelmez).
- Beş şık büyük/küçük harf duyarsız olarak birbirinden farklı olmalıdır.
- Deterministiktir: aynı tablolar aynı dosyayı üretir.

Kullanım:
    python3 araclar/bilgi_soru_uret.py tarih [--hedef 1600]
    python3 araclar/bilgi_soru_uret.py hepsi
"""
import argparse
import importlib
import random
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'araclar'))
from kpss_kapsam import question_key  # noqa: E402

PREFIX = {'tarih': 'TAR', 'cografya': 'COG', 'vatandaslik': 'VAT', 'turkce': 'TUR', 'guncel': 'GUN'}
# 7 test günü × 400 = 2800 test kökü için gereken yeni soru sayısı (bkz. README)
HEDEF = {'tarih': 1600, 'cografya': 1639, 'vatandaslik': 1650, 'turkce': 1562, 'guncel': 1650}
BASLANGIC = 651
CIKTI = 'yeni_parti_16_{}.tsv'


# Dersler için tek bilgi soran soru türlerinin toplam üst sınırı (Türkçe kendi KOTA'sını kullanır).
BASIT_TAVAN = 360
AKIL_ONEK = ('oncul', 'sirala', 'esle')

def mevcut_kokler(ders=None):
    keys = set()
    import json
    for f in (ROOT / 'data/sorular').glob('*.jsonl'):
        for line in f.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                r = json.loads(line)
                p = r.get('id', '').split('-')
                # Bu üreticinin kendi eski çıktısı (YS-0651+) yeniden üretilirken sayılmaz.
                if len(p) == 3 and p[1] == 'YS' and p[2].isdigit() and int(p[2]) >= BASLANGIC:
                    continue
                keys.add(question_key(r))
    for tsv in (ROOT / 'data/kaynaklar').glob('yeni_parti_*.tsv'):
        # yeni_parti_16 çıktılarından yalnız PREFIX sırasında bu dersten ÖNCE gelen derslerinkiler
        # sayılır (ör. Tarih'te çıkan eser sorusu Güncel'de tekrar üretilmez). Sabit sıra sayesinde
        # dersler sırayla yeniden üretildiğinde sonuç kararlıdır.
        if tsv.name.startswith('yeni_parti_16_'):
            sira = list(PREFIX)
            diger = tsv.stem[len('yeni_parti_16_'):]
            if ders not in sira or diger not in sira or sira.index(diger) >= sira.index(ders):
                continue
        for line in tsv.read_text(encoding='utf-8').splitlines():
            if line.strip() and not line.startswith('#'):
                p = line.split('|')
                if len(p) == 10:
                    keys.add(question_key({'kok': p[3].strip().replace(r'\n', '\n')}))
    return keys


def temiz(x):
    x = re.sub(r'\s+', ' ', str(x)).strip()
    if '|' in x:
        raise ValueError('| karakteri kullanılamaz: ' + x)
    return x


def sec(dogru, havuz, rng, n=4, haric=()):
    """dogru'dan ve birbirinden farklı n çeldirici seç (casefold)."""
    gor = {dogru.casefold(), *(h.casefold() for h in haric)}
    aday = []
    for h in havuz:
        if h.casefold() not in gor:
            gor.add(h.casefold())
            aday.append(h)
    if len(aday) < n:
        return None
    return rng.sample(aday, n)


def uret(ders, hedef=None, yaz=True):
    mod = importlib.import_module(f'bilgi_veri.{ders}')
    rng = random.Random(f'bilgi-{ders}-2026')
    kokler = mevcut_kokler(ders)
    turlu = OrderedDict()
    atlanan = Counter()
    for q in mod.uret(rng):
        if q is None:
            continue
        kok = temiz(q['kok'])
        k = question_key({'kok': kok})
        opts = [temiz(q['dogru']), *map(temiz, q['yanlis'])]
        if len(opts) != 5 or len({o.casefold() for o in opts}) != 5:
            atlanan['sik'] += 1
            continue
        if k in kokler:
            atlanan['tekrar_kok'] += 1
            continue
        kokler.add(k)
        z = int(q.get('z', 2))
        turlu.setdefault(q['tur'], []).append(
            (q['konu'], str(z if z in (2, 3) else 2), kok, *opts, temiz(q['gerekce'])))
    # Türler arasında dengeli seçim: her türden sırayla bir soru al.
    toplam = sum(len(v) for v in turlu.values())
    hedef = hedef or HEDEF[ders]
    # KOTA: türün en çok kaç soru vereceği; AGIRLIK: her turda türden kaç soru alınacağı.
    kota = getattr(mod, 'KOTA', {})
    agirlik = getattr(mod, 'AGIRLIK', {})
    for t, v in turlu.items():
        rng.shuffle(v)
        if t in kota:
            del v[kota[t]:]
    # Tek bilgi soran (akıl yürütme gerektirmeyen) türler toplamda BASIT_TAVAN ile sınırlanır;
    # kalan yer öncüllü / sıralama / eşleştirme sorularıyla dolar (sınav düzeyi).
    tavan = getattr(mod, 'BASIT_TAVAN', BASIT_TAVAN)
    if tavan is not None:
        basit = [t for t in turlu if not t.startswith(AKIL_ONEK) and t not in kota]
        n_basit = sum(len(turlu[t]) for t in basit)
        if n_basit > tavan:
            for t in basit:
                del turlu[t][max(1, len(turlu[t]) * tavan // n_basit):]
    toplam = sum(len(v) for v in turlu.values())
    secilen, konum = [], {t: 0 for t in turlu}
    while len(secilen) < min(hedef, toplam):
        for t, kq in turlu.items():
            for _ in range(agirlik.get(t, 1)):
                if konum[t] < len(kq) and len(secilen) < hedef:
                    secilen.append(kq[konum[t]])
                    konum[t] += 1
    rng.shuffle(secilen)
    satirlar = [f'# {ders}: bilgi tablosu tabanlı sorular (araclar/bilgi_soru_uret.py ile üretildi; '
                f'kaynak tablo araclar/bilgi_veri/{ders}.py). Elle düzenlemeyin; tabloyu düzenleyip yeniden üretin.']
    for n, row in enumerate(secilen):
        sid = f'{PREFIX[ders]}-YS-{BASLANGIC + n:04d}'
        satirlar.append('|'.join([sid, *row]))
    if yaz:
        (ROOT / 'data/kaynaklar' / CIKTI.format(ders)).write_text('\n'.join(satirlar) + '\n', encoding='utf-8')
    return dict(ders=ders, uretilen=toplam, yazilan=len(secilen), hedef=hedef,
                turler={k: len(v) for k, v in turlu.items()},
                secilen=dict(Counter(t for t, kq in turlu.items() for _ in range(konum[t]))),
                atlanan=dict(atlanan))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('ders', choices=[*PREFIX, 'hepsi'])
    ap.add_argument('--hedef', type=int)
    ap.add_argument('--kuru', action='store_true', help='dosya yazmadan say')
    a = ap.parse_args()
    for d in (PREFIX if a.ders == 'hepsi' else [a.ders]):
        print(uret(d, a.hedef, not a.kuru))
