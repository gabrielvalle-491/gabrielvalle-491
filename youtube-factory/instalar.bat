@echo off
chcp 65001 >nul
echo === Instalación de la Fábrica de contenido ===
where python >nul 2>nul || (echo Falta Python. Instálalo desde https://www.python.org/downloads/ marcando "Add python.exe to PATH" y vuelve a ejecutar. & pause & exit /b 1)
where ffmpeg >nul 2>nul || (echo Instalando FFmpeg con winget... & winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements)
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt || (echo Error instalando paquetes & pause & exit /b 1)
python -m playwright install chromium
python fabrica.py iniciar
python fabrica.py diagnostico
echo.
echo Listo. Si FFmpeg se acaba de instalar, cierra esta ventana y abre una nueva antes de usar fabrica.bat
pause
