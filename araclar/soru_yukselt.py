#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data/kaynaklar/yukselt_*.tsv dosyalarındaki yeniden yazılmış soruları
bankada yerinde günceller (aynı id, aynı konu/gün; yeni kök/şık/çözüm/zorluk).

TSV sütunları (| veya tab ile):
id | zorluk | kok | dogru_metni | y1 | y2 | y3 | y4 | cozum | kaynak?

- kaynak sütunu verilirse güncellenir, verilmezse eski kaynak korunur.
- Çözüm: "KPSS mantığı ile çözüm" yöntemiyle kaydedilir.
- Şıklar deterministik olarak karıştırılır (aynı id için hep aynı sıra).

Çalıştırma: python3 araclar/soru_yukselt.py
"""
import random
import re
import sys
from pathlib import Path
import json

KOK = Path(__file__).resolve().parent.parent
VERI = KOK / "data"
KAYNAKLAR = VERI / "kaynaklar"
ON_EK_DERS = {"TAR": "tarih", "COG": "cografya", "VAT": "vatandaslik", "TUR": "turkce", "GUN": "guncel"}


def tsv_dosyalari():
    return sorted(KAYNAKLAR.glob("yukselt_*.tsv"))


def main():
    kayitlar = {}
    by_ders = {}
    for d in set(ON_EK_DERS.values()):
        yol = VERI / "sorular" / f"{d}.jsonl"
        satirlar = [json.loads(l) for l in yol.read_text(encoding="utf-8").splitlines() if l.strip()]
        by_ders[d] = (yol, satirlar)
        for s in satirlar:
            kayitlar[s["id"]] = s

    guncellenen = 0
    eksik = []
    for tsv in tsv_dosyalari():
        for sat in tsv.read_text(encoding="utf-8").splitlines():
            sat = sat.rstrip("\n")
            if not sat.strip() or sat.startswith("#"):
                continue
            p = sat.split("\t") if "\t" in sat else sat.split("|")
            if len(p) < 9:
                print(f"[!] kısa satır ({tsv.name}): {sat[:60]}")
                continue
            sid, zorluk, kok, dogru, y1, y2, y3, y4, cozum = p[:9]
            yeni_kaynak = p[9].strip() if len(p) > 9 and p[9].strip() else None
            if sid not in kayitlar:
                eksik.append(sid)
                continue
            s = kayitlar[sid]
            rng = random.Random(f"{sid}-yukselt")
            dogru_t = dogru.strip()
            siklar = [dogru_t, y1.strip(), y2.strip(), y3.strip(), y4.strip()]
            rng.shuffle(siklar)
            s["kok"] = kok.strip()
            s["zorluk"] = int(zorluk)
            s["siklar"] = siklar
            s["dogru"] = siklar.index(dogru_t)
            s["cozumler"] = [{"yontem": "KPSS mantığı ile çözüm", "metin": cozum.strip()}]
            if yeni_kaynak:
                s["kaynak"] = yeni_kaynak
            guncellenen += 1

    if eksik:
        print(f"[!] bulunamayan id ({len(eksik)}): {', '.join(eksik[:10])}{' ...' if len(eksik) > 10 else ''}")
    for d, (yol, satirlar) in by_ders.items():
        yol.write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in satirlar) + "\n", encoding="utf-8")
        print(f"{d:12} {len(satirlar)} kayıt yazıldı")
    print(f"GÜNCELLENEN: {guncellenen}")


if __name__ == "__main__":
    sys.exit(main())
