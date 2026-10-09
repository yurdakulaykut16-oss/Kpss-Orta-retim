#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soru bankasından 10 günlük deneme setlerini üretir (data/denemeler.json).

Her gün için: 15 soruluk "Gün Sonu Denemesi" (gün içi %60 + karışık %40)
5. gün: Yarı Kamp Büyük Denemesi (50 soru)  |  10. gün: Final Genel Denemesi (50 soru)
"""
import json
import random
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

dagilim_mini = {"tarih": 4, "cografya": 3, "vatandaslik": 3, "turkce": 3, "guncel": 2}
dagilim_buyuk = {"tarih": 14, "cografya": 11, "vatandaslik": 9, "turkce": 11, "guncel": 5}

denemeler = []
for gun in range(1, 11):
    if gun == 5:
        ad, sure, dagilim = "Yarı Kamp Büyük Denemesi", 40, dagilim_buyuk
    elif gun == 10:
        ad, sure, dagilim = "Final Genel Denemesi", 40, dagilim_buyuk
    else:
        ad, sure, dagilim = f"{gun}. Gün Sonu Denemesi", 12, dagilim_mini

    secilen = []
    for ders, adet in dagilim.items():
        gunluk = [s for s in banka[ders] if s["gun"] == gun]
        karisik = [s for s in banka[ders] if s["gun"] < gun]
        random.shuffle(gunluk)
        random.shuffle(karisik)
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

    random.shuffle(secilen)
    denemeler.append({
        "id": f"DEN-{gun:02d}",
        "gun": gun,
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
