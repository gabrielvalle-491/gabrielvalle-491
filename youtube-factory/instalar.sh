#!/usr/bin/env bash
# Instalación en Linux/macOS. Requiere python3 (3.10+) y ffmpeg instalados.
set -e
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || { echo "Falta ffmpeg (Ubuntu: sudo apt install ffmpeg | macOS: brew install ffmpeg)"; exit 1; }
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
python fabrica.py iniciar
python fabrica.py diagnostico
