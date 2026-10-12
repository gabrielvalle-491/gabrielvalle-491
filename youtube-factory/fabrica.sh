#!/usr/bin/env bash
cd "$(dirname "$0")"
[ -d .venv ] && . .venv/bin/activate
python3 fabrica.py "$@"
