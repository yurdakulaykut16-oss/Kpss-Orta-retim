#!/usr/bin/env python3
"""Çalışan KPSS Kamp sunucusundan /tmp/kpss_test/ altına smoke için fixture çeker.

Kullanım:
    python3 app.py            # ayrı terminalde / bir süreçte çalışırken
    python3 araclar/refresh_fixtures.py
"""
import json
import os
import sys
import urllib.request

BASE = os.environ.get("KPSS_BASE", "http://127.0.0.1:5000")
OUT = "/tmp/kpss_test"

SABIT = {
    "/api/meta": "meta.json",
    "/api/program": "program.json",
    "/api/denemeler": "denemeler.json",
    "/api/konu-yeniden": "konu_yeniden.json",
}
DERSLER = ["tarih", "cografya", "vatandaslik", "turkce", "guncel"]


def al(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.load(r)


def main():
    os.makedirs(OUT, exist_ok=True)
    dosyalar = dict(SABIT)
    for d in DERSLER:
        dosyalar[f"/api/ders/{d}"] = f"ders_{d}.json"
        dosyalar[f"/api/sorular/{d}"] = f"sorular_{d}.json"
    for path, fn in dosyalar.items():
        data = al(path)
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(
            json.dumps(data, ensure_ascii=False))
    den = al("/api/denemeler")["denemeler"]
    for item in den:
        did = item["id"]
        data = al(f"/api/deneme/{did}")
        open(os.path.join(OUT, f"deneme_{did}.json"), "w", encoding="utf-8").write(
            json.dumps(data, ensure_ascii=False))
    print(f"fixture OK: {len(dosyalar)} api + {len(den)} deneme → {OUT}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("fixture alınamadı:", e, file=sys.stderr)
        sys.exit(1)
