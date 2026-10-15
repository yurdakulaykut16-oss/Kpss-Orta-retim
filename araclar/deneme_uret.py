#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soru bankasından 10 deneme setini üretir (data/denemeler.json).

Soru seçimi bankadaki 10 modüle göre yapılır (her modül için 15 soruluk mini
deneme: modül içi %60 + önceki modüller %40; 5. ve 10. modül 50 soruluk büyük
deneme). Kamp 17–24 Ekim'e (8 gün) indirildiği için denemeler program günlerine
PROGRAM_GUNU eşlemesiyle dağıtılır: 15–16 Ekim'in iki mini denemesi 1. güne
(17 Ekim), büyük denemeler 4. güne (20 Ekim) ve 8. güne (24 Ekim, final provası).
"""
import json
import random
import re
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
VERI = KOK / "data"
DERSLER = ["tarih", "cografya", "vatandaslik", "turkce", "guncel"]
random.seed(20261025)  # sabit tohum -> tekrar üretildiğinde aynı denemeler

banka = {d: [] for d in DERSLER}
for d in DERSLER:
    for satir in (VERI / "sorular" / f"{d}.jsonl").read_text(encoding="utf-8").splitlines():
        satir = satir.strip()
        if not satir or satir.startswith("#"):
            continue
        banka[d].append(json.loads(satir))

# Yeni deneme üretiminde de kapsam kapısını atlama. Sırf hedef sayıyı
# doldurmak için onaysız soru kullanılamaz.
import sys
sys.path.insert(0, str(KOK))
from kpss_kapsam import filter_bank, read_policy
banka, _kapsam = filter_bank(banka, read_policy(KOK))

dagilim_mini = {"tarih": 4, "cografya": 3, "vatandaslik": 3, "turkce": 3, "guncel": 2}
dagilim_buyuk = {"tarih": 14, "cografya": 11, "vatandaslik": 9, "turkce": 11, "guncel": 5}

# modül -> program günü (8 günlük kamp)
PROGRAM_GUNU = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 8}
ADLAR = {1: "1. Gün Denemesi A (15 Ekim içeriği)", 2: "1. Gün Denemesi B (16 Ekim içeriği)",
         9: "Final Günü Mini Denemesi"}

denemeler = []
for gun in range(1, 11):
    if gun == 5:
        ad, sure, dagilim = "Yarı Kamp Büyük Denemesi", 40, dagilim_buyuk
    elif gun == 10:
        ad, sure, dagilim = "Final Genel Denemesi", 40, dagilim_buyuk
    else:
        ad = ADLAR.get(gun, f"{PROGRAM_GUNU[gun]}. Gün Sonu Denemesi")
        sure, dagilim = 12, dagilim_mini

    secilen = []
    for ders, adet in dagilim.items():
        baslangic = len(secilen)
        def oncelikle(pool):
            # çıkmış KPSS soruları öncelikli (deneme gerçek sınav sorularıyla olsun)
            cikmislar = [s for s in pool if re.match(r'^\d{4}-KPSS$', s.get('kaynak', ''))]
            digerleri = [s for s in pool if s not in cikmislar]
            return cikmislar + digerleri

        gunluk = [s for s in banka[ders] if s["gun"] == gun]
        karisik = [s for s in banka[ders] if s["gun"] < gun]
        random.shuffle(gunluk)
        random.shuffle(karisik)
        gunluk = oncelikle(gunluk)
        karisik = oncelikle(karisik)
        # %60 bu gün, %40 önceki günler (tekrar amaçlı)
        d_gun = min(len(gunluk), round(adet * 0.6))
        secilen.extend([s["id"] for s in gunluk[:d_gun]])
        kalan = adet - d_gun
        secilen.extend([s["id"] for s in karisik[:kalan]])
        # yeterse değilse aynı günden tamamla
        eksik = adet - (d_gun + min(len(karisik), kalan))
        if eksik > 0:
            ek = [s["id"] for s in gunluk[d_gun: d_gun + eksik]]
            secilen.extend(ek)
        # Gün/önceki gün havuzu daraldığında yalnız onaylı aynı ders
        # kayıtlarıyla tamamla; tekrar veya kapsam dışı yedek kullanma.
        eksik = adet - (len(secilen) - baslangic)
        if eksik > 0:
            yedek = [s for s in banka[ders] if s['id'] not in secilen]
            random.shuffle(yedek)
            if len(yedek) < eksik:
                raise ValueError(f'{gun}. gün {ders}: yeterli onaylı soru yok')
            secilen.extend(s['id'] for s in oncelikle(yedek)[:eksik])

    random.shuffle(secilen)
    denemeler.append({
        "id": f"DEN-{gun:02d}",
        "gun": PROGRAM_GUNU[gun],
        "ad": ad,
        "sure_dk": sure,
        "tur": "buyuk" if gun in (5, 10) else "mini",
        "odak": "Gün içi konular %60, önceki günler %40" if gun not in (5, 10) else "Genel prova",
        "sorular": secilen,
    })

cikti = {"denemeler": denemeler}
(VERI / "denemeler.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(denemeler)} deneme üretildi:",
      {d['id']: len(d['sorular']) for d in denemeler})
