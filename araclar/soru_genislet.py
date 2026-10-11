#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data/kaynaklar/yeni_sorular.tsv'yi (parça dosyaları) soru bankasına ekler.

TSV sütunları (tab ile ayrılmış):
ders | konu | gun | zorluk | kok | dogru | y1 | y2 | y3 | y4 | cozum1 | cozum2?

Çalıştırma: python3 araclar/soru_genislet.py
Tekrarlı çalışmaz: aynı kok + ders varsa atlar.
"""
import json
import random
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
VERI = KOK / "data"
KAYNAKLAR = VERI / "kaynaklar"
DERSLER = ["tarih", "cografya", "vatandaslik", "turkce", "guncel"]
ON_EK = {"tarih": "TAR", "cografya": "COG", "vatandaslik": "VAT", "turkce": "TUR", "guncel": "GUN"}
rnd = random.Random(20261025)

def slug(s):
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    s = s.translate(tr).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "konu"

def mevcut(d):
    yol = VERI / "sorular" / f"{d}.jsonl"
    satirlar = [json.loads(l) for l in yol.read_text(encoding="utf-8").splitlines() if l.strip()] if yol.exists() else []
    return yol, satirlar

def tsv_dosyalari():
    return sorted(KAYNAKLAR.glob("yeni_sorular_*.tsv"))

def main():
    toplam_ek = 0
    for d in DERSLER:
        yol, satirlar = mevcut(d)
        max_no = 0
        koklar = set()
        for s in satirlar:
            m = re.search(r"(\d+)$", s["id"])
            if m:
                max_no = max(max_no, int(m.group(1)))
            koklar.add(s["kok"].strip().lower())
        eklenen = []
        for tsv in tsv_dosyalari():
            for sat in tsv.read_text(encoding="utf-8").splitlines():
                sat = sat.rstrip("\n")
                if not sat.strip() or sat.startswith("#"):
                    continue
                p = sat.split("\t") if "\t" in sat else sat.split("|")
                if len(p) < 11:
                    print(f"[!] kısa satır ({tsv.name}): {sat[:60]}")
                    continue
                sd, konu, gun, zorluk, kok, dogru, y1, y2, y3, y4, c1 = p[:11]
                c2 = p[11] if len(p) > 11 and p[11].strip() else None
                kaynak = p[12] if len(p) > 12 and p[12].strip() else "KPSS formatında"
                if sd != d:
                    continue
                if kok.strip().lower() in koklar:
                    continue
                max_no += 1
                siklar = [dogru, y1, y2, y3, y4]
                rnd.shuffle(siklar)
                kayit = {
                    "id": f"{ON_EK[d]}-{max_no:04d}",
                    "ders": d,
                    "gun": int(gun),
                    "konu": konu,
                    "zorluk": int(zorluk),
                    "kaynak": kaynak,
                    "kok": kok,
                    "siklar": siklar,
                    "dogru": siklar.index(dogru),
                    "cozumler": [{"yontem": "Bilgi ile çözüm", "metin": c1}]
                    + ([{"yontem": "Kısa yol / eleme", "metin": c2}] if c2 else []),
                    "etiketler": sorted(
                        {slug(konu), slug(kok.split()[0] if kok.split() else "soru")}
                        | ({"cikmis"} if kaynak != "KPSS formatında" else set())
                    ),
                }
                eklenen.append(kayit)
                koklar.add(kok.strip().lower())
        if eklenen:
            with open(yol, "a", encoding="utf-8") as f:
                for s in eklenen:
                    f.write(json.dumps(s, ensure_ascii=False) + "\n")
        toplam_ek += len(eklenen)
        yeni_top = len(satirlar) + len(eklenen)
        print(f"{d:12} +{len(eklenen):3d}  → toplam {yeni_top}")
    print(f"EKLENEN: {toplam_ek}")

if __name__ == "__main__":
    sys.exit(main())
