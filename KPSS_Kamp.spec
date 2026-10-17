# -*- mode: python ; coding: utf-8 -*-
# PyInstaller tarifi: tek dosyalık KPSS_Kamp.exe (Windows) üretir.
#   Windows:  exe_olustur.bat   (veya: py -m PyInstaller --noconfirm --clean KPSS_Kamp.spec)
#   Çıktı:    dist/KPSS_Kamp.exe
# Uygulamanın çalışırken okuduğu bütün içerik (arayüz, soru bankası, konu anlatımları,
# program, denemeler, kapsam ve hedef ayarları) exe'nin içine gömülür. data/kaynaklar
# (soru üretim kaynakları) ve data/ilerleme (kişisel ilerleme) gömülmez.
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

KOK = Path(SPECPATH)
VERI = KOK / 'data'

datas = [(str(KOK / 'static'), 'static'),
         (str(VERI / 'sorular'), 'data/sorular'),
         (str(VERI / 'dersler'), 'data/dersler')]
for ad in ('program.json', 'denemeler.json', 'konu_yeniden.json',
           'kpss_kapsam.json', 'calisma_hedefleri.json'):
    datas.append((str(VERI / ad), 'data'))
# Windows'ta sistem saat dilimi veritabanı yoktur; "Europe/Istanbul" için tzdata paketi gömülür.
datas += collect_data_files('tzdata')

a = Analysis(
    [str(KOK / 'kpss_kamp.py')],
    pathex=[str(KOK)],
    binaries=[],
    datas=datas,
    hiddenimports=['app', 'kpss_kapsam', 'calisma_hedefi'] + collect_submodules('tzdata'),
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='KPSS_Kamp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=True,
)
