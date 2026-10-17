@echo off
REM ============================================================
REM  KPSS Kamp - KPSS_Kamp.exe olusturucu (Windows)
REM  Gerekli: Python 3.10+ (python.org, kurulumda "Add to PATH")
REM  Cikti   : bu klasorde KPSS_Kamp.exe
REM ============================================================
chcp 65001 >nul
cd /d "%~dp0"

set "PY=py -3"
%PY% --version >nul 2>&1 || set "PY=python"
%PY% --version >nul 2>&1 || (
  echo Python bulunamadi. https://www.python.org/downloads/ adresinden kurun ^(Add to PATH secili olsun^).
  pause & exit /b 1
)

echo [1/3] Gerekli paketler kuruluyor...
%PY% -m pip install --upgrade pip >nul
%PY% -m pip install -r requirements.txt pyinstaller || (echo Paket kurulumu basarisiz. & pause & exit /b 1)

echo [2/3] KPSS_Kamp.exe olusturuluyor (1-3 dakika surebilir)...
%PY% -m PyInstaller --noconfirm --clean KPSS_Kamp.spec || (echo Exe olusturulamadi. & pause & exit /b 1)

echo [3/3] Exe proje klasorune kopyalaniyor...
copy /Y "dist\KPSS_Kamp.exe" "KPSS_Kamp.exe" >nul

echo.
echo Tamamlandi: %CD%\KPSS_Kamp.exe
echo Cift tiklayarak calistirabilirsiniz. Ilerleme KPSS_Kamp_ilerleme klasorunde saklanir.
pause
