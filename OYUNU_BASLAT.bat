@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Sweet Odyssey

py -3 -c "import sys; raise SystemExit(sys.version_info < (3,11))" >nul 2>&1
if not errorlevel 1 (
    py -3 app.py %*
    if errorlevel 1 goto failed
    exit /b 0
)
python -c "import sys; raise SystemExit(sys.version_info < (3,11))" >nul 2>&1
if not errorlevel 1 (
    python app.py %*
    if errorlevel 1 goto failed
    exit /b 0
)
echo Python 3.11 veya uzeri bulunamadi.
echo Python kuruluysa app.py dosyasini Python ile acabilir,
echo veya klasorde terminal acip python app.py yazabilirsiniz.
echo Indirme: https://www.python.org/downloads/windows/
goto failed

:failed
echo.
echo Oyun baslatilamadi. Yukaridaki aciklamayi kontrol edin.
pause
exit /b 1
