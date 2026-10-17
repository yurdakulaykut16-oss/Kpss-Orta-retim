@echo off
REM KPSS Kamp - Python ile hizli baslatma (exe olmadan). Gerekli: Python 3.10+
chcp 65001 >nul
cd /d "%~dp0"
set "PY=py -3"
%PY% --version >nul 2>&1 || set "PY=python"
%PY% -c "import flask, tzdata" >nul 2>&1 || %PY% -m pip install -r requirements.txt
%PY% kpss_kamp.py
pause
