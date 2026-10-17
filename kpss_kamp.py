#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KPSS Kamp — masaüstü başlatıcı (KPSS_Kamp.exe bu dosyadan üretilir).

Çift tıklayınca:
  1. Sunucuyu yalnızca bu bilgisayarda (127.0.0.1) başlatır,
  2. Varsayılan tarayıcıda uygulamayı açar,
  3. Pencere kapatılınca sunucu da kapanır.

Uygulama zaten açıksa ikinci bir sunucu başlatmaz, sadece tarayıcıyı açar.
İlerleme exe'nin yanındaki "KPSS_Kamp_ilerleme" klasöründe saklanır.

Python ile de çalışır:  python kpss_kamp.py
Ortam değişkenleri: KPSS_PORT (varsayılan 5000), KPSS_ILERLEME_DIZINI.
Seçenek: --tarayici-acma  (tarayıcıyı otomatik açmaz; test için)
"""
from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time
import urllib.request
import webbrowser

VARSAYILAN_PORT = 5000
YEDEK_PORTLAR = range(5001, 5021)


def _port_bos(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def _kpss_calisiyor_mu(port: int) -> bool:
    """Portta zaten KPSS Kamp sunucusu varsa True (ikinci kopyayı açmamak için)."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/meta", timeout=2) as r:
            return "sinav" in json.loads(r.read().decode("utf-8"))
    except Exception:
        return False


def _bekle_ve_cik(mesaj: str, kod: int = 0) -> None:
    print(mesaj)
    if getattr(sys, "frozen", False) and sys.stdin and sys.stdin.isatty():
        try:
            input("Kapatmak için Enter'a basın...")
        except EOFError:
            pass
    sys.exit(kod)


def main() -> None:
    # Eski Windows konsollarında Türkçe karakterler hata vermesin.
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(errors="replace")
        except Exception:
            pass
    tarayici = "--tarayici-acma" not in sys.argv
    tercih = int(os.environ.get("KPSS_PORT") or VARSAYILAN_PORT)

    print("=" * 60)
    print("  KPSS Kamp — Ortaöğretim (18–24 Ekim, sınav 25 Ekim 2026)")
    print("=" * 60)

    if not _port_bos(tercih) and _kpss_calisiyor_mu(tercih):
        url = f"http://127.0.0.1:{tercih}/"
        print(f"Uygulama zaten açık: {url}")
        if tarayici:
            webbrowser.open(url)
        time.sleep(2)
        return

    port = tercih if _port_bos(tercih) else next((p for p in YEDEK_PORTLAR if _port_bos(p)), None)
    if port is None:
        _bekle_ve_cik(f"{tercih}–{YEDEK_PORTLAR[-1]} arasındaki portların hepsi dolu. Diğer programları kapatıp tekrar deneyin.", 1)
    if port != tercih:
        print(f"Uyarı: {tercih} portu başka bir program tarafından kullanılıyor; {port} kullanılacak.")
        print("(Tarayıcı kayıtları porta bağlıdır; mümkünse hep aynı portu kullanın.)")

    print("İçerik yükleniyor (soru bankası, konu anlatımları, program)...")
    try:
        import app as sunucu
        from werkzeug.serving import make_server

        sunucu.her_seyi_yukle()
        toplam = sum(len(v) for v in sunucu.her_seyi_yukle()["sorular"].values())
        httpd = make_server("127.0.0.1", port, sunucu.app, threaded=True)
    except Exception as hata:  # pragma: no cover - kullanıcıya okunur hata göstermek için
        _bekle_ve_cik(f"Uygulama başlatılamadı: {hata!r}", 1)

    url = f"http://127.0.0.1:{port}/"
    print(f"{toplam} soru yüklendi.")
    print(f"İlerleme klasörü: {sunucu.ILERLEME}")
    print(f"Uygulama adresi : {url}")
    print("Bu pencere açık kaldığı sürece uygulama çalışır. Kapatmak için pencereyi kapatın (veya Ctrl+C).")
    if tarayici:
        threading.Timer(1.0, webbrowser.open, args=(url,)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Uygulama kapatıldı.")


if __name__ == "__main__":
    main()
