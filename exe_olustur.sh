#!/usr/bin/env bash
# KPSS Kamp - macOS/Linux icin tek dosyalik calistirilabilir uretir (dist/KPSS_Kamp).
# Not: PyInstaller capraz derleme yapmaz; Windows .exe icin exe_olustur.bat'i Windows'ta calistirin.
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt pyinstaller
python3 -m PyInstaller --noconfirm --clean KPSS_Kamp.spec
echo "Tamamlandi: dist/KPSS_Kamp"
