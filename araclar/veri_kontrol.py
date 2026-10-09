#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Veri bütünlüğü kontrolü: soru bankası, program, deneme referansları."""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
VERI = KOK / "data"
DERSLER = ["tarih", "cografya", "vatandaslik", "turkce", "guncel"]
hata = 0
toplam = 0
index = {}

for d in DERSLER:
    yol = VERI / "sorular" / f"{d}.jsonl"
    if not yol.exists():
        print(f"[!] {yol} yok")
        hata += 1
        continue
    seen = set()
    for i, satir in enumerate(yol.read_text(encoding="utf-8").splitlines(), 1):
        satir = satir.strip()
        if not satir or satir.startswith("#"):
            continue
        toplam += 1
        try:
            s = json.loads(satir)
        except Exception as e:
            print(f"[!] {d}.jsonl:{i} JSON hatası: {e}")
            hata += 1
            continue
        for alan in ("id", "ders", "gun", "konu", "kok", "siklar", "dogru", "etiketler"):
            if alan not in s:
                print(f"[!] {d}:{i} eksik alan {alan}")
                hata += 1
        if s.get("id") in seen:
            print(f"[!] {d}:{i} yinelenen id {s.get('id')}")
            hata += 1
        seen.add(s.get("id"))
        if s.get("ders") != d:
            print(f"[!] {d}:{i} ders alanı {s.get('ders')} != {d}")
            hata += 1
        if not isinstance(s.get("siklar"), list) or len(s["siklar"]) != 5:
            print(f"[!] {d}:{i} şık sayısı 5 değil")
            hata += 1
        if not (isinstance(s.get("dogru"), int) and 0 <= s["dogru"] <= 4):
            print(f"[!] {d}:{i} dogru alanı geçersiz")
            hata += 1
        index[s.get("id")] = s

# program
program = json.loads((VERI / "program.json").read_text(encoding="utf-8"))
for g in program["gunler"]:
    for ds in g["dersler"]:
        if ds["ders"] not in DERSLER:
            print(f"[!] program gun {g['no']}: bilinmeyen ders {ds['ders']}")
            hata += 1

# denemeler
denemeler = json.loads((VERI / "denemeler.json").read_text(encoding="utf-8"))
for dn in denemeler["denemeler"]:
    for sid in dn["sorular"]:
        if sid not in index:
            print(f"[!] deneme {dn['id']}: soru yok {sid}")
            hata += 1

# ders markdown
for d in DERSLER:
    yol = VERI / "dersler" / f"{d}.md"
    if not yol.exists():
        print(f"[!] {yol} yok")
        hata += 1
        continue
    metin = yol.read_text(encoding="utf-8")
    gunler = [int(x) for x in __import__("re").findall(r"^# GUN (\d+)", metin, __import__("re").M)]
    if sorted(gunler) != list(range(1, 11)):
        print(f"[!] {d}.md gün başlıkları 1-10 değil: {gunler}")
        hata += 1

print(f"\nToplam soru: {toplam}, benzersiz id: {len(index)}")
print("HATA YOK ✔" if hata == 0 else f"{hata} hata bulundu ✘")
sys.exit(1 if hata else 0)
