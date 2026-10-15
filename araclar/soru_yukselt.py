#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Özgün pratik sorularını id üzerinden yerinde yeniler.

Sütunlar (| veya tab):
id | zorluk | kok | dogru_metni | y1 | y2 | y3 | y4 | cozum | kaynak?

Çıkmış ve kitap soruları korumalıdır. Tüm girişler doğrulanmadan hiçbir
banka dosyasına yazılmaz. Aynı girdiler tekrar çalıştırıldığında sonuç aynıdır.
"""
import json
import random
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
DERSLER = ("tarih", "cografya", "vatandaslik", "turkce", "guncel")
OZGUN_KAYNAK = "KPSS formatında"
ESKI_ETIKET = "Çıkmış KPSS sorusudur (yeniden düzenlendi)"


def yukseltilen_banka(kok):
    """Doğrula ve bellekte güncelle; bu fonksiyon dosyaya yazmaz."""
    by_ders, kayitlar = {}, {}
    for ders in DERSLER:
        yol = kok / "data" / "sorular" / f"{ders}.jsonl"
        rows = [json.loads(line) for line in yol.read_text(encoding="utf-8").splitlines() if line.strip()]
        by_ders[ders] = (yol, rows)
        for soru in rows:
            if soru["id"] in kayitlar:
                raise ValueError(f"Bankada yinelenen id: {soru['id']}")
            kayitlar[soru["id"]] = soru

    gorulen = set()
    sayilar = dict.fromkeys(DERSLER, 0)
    for tsv in sorted((kok / "data" / "kaynaklar").glob("yukselt_*.tsv")):
        for no, line in enumerate(tsv.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            p = [x.strip() for x in line.split("\t" if "\t" in line else "|")]
            yer = f"{tsv.name}:{no}"
            if len(p) not in (9, 10) or not all(p[:9]):
                raise ValueError(f"{yer}: 9 dolu alan ve isteğe bağlı kaynak gerekir")
            sid, zorluk, soru_koku, dogru, *kalan = p[:9]
            yanlislar, cozum = kalan[:4], kalan[4]
            if sid not in kayitlar:
                raise ValueError(f"{yer}: bulunamayan id {sid}")
            if sid in gorulen:
                raise ValueError(f"{yer}: yinelenen yükseltme id'si {sid}")
            gorulen.add(sid)
            soru = kayitlar[sid]
            # Önce mevcut kaynak kontrol edilir; kaynak sütunuyla koruma aşılamaz.
            if soru.get("kaynak") not in (OZGUN_KAYNAK, ESKI_ETIKET):
                raise ValueError(f"{yer}: çıkmış/kitap/kaynaklı soru değiştirilemez ({sid})")
            if len(p) == 10 and p[9] not in ("", OZGUN_KAYNAK):
                raise ValueError(f"{yer}: özgün soru gerçek kaynak adıyla etiketlenemez")
            if zorluk not in ("2", "3"):
                raise ValueError(f"{yer}: zorluk 2 veya 3 olmalı")
            siklar = [dogru, *yanlislar]
            if len(set(x.casefold() for x in siklar)) != 5:
                raise ValueError(f"{yer}: beş farklı seçenek gerekir")
            random.Random(f"{sid}-yukselt").shuffle(siklar)
            soru.update(
                kok=soru_koku.replace(r'\n', '\n'), zorluk=int(zorluk), siklar=siklar,
                dogru=siklar.index(dogru), kaynak=OZGUN_KAYNAK,
                cozumler=[{"yontem": "KPSS mantığı ile çözüm", "metin": cozum}],
                etiketler=[t for t in soru.get("etiketler", []) if t != "cikmis"],
            )
            sayilar[soru["ders"]] += 1

    # Yeniden yazılmış kökler başka bir kayıtla çakışmasın.
    koklar = {}
    for sid, soru in kayitlar.items():
        anahtar = (soru["ders"], soru["kok"].strip().casefold())
        if anahtar in koklar and (sid in gorulen or koklar[anahtar] in gorulen):
            raise ValueError(f"Yinelenen soru kökü: {koklar[anahtar]}, {sid}")
        koklar[anahtar] = sid
    return by_ders, sayilar


def main(kok=KOK):
    by_ders, sayilar = yukseltilen_banka(kok)
    for ders, (yol, rows) in by_ders.items():
        metin = "\n".join(json.dumps(s, ensure_ascii=False) for s in rows) + "\n"
        if yol.read_text(encoding="utf-8") != metin:
            yol.write_text(metin, encoding="utf-8")
        print(f"{ders:12} {sayilar[ders]:3} özgün soru yenilendi")
    print(f"GÜNCELLENEN: {sum(sayilar.values())}")


if __name__ == "__main__":
    main()
