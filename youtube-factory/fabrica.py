#!/usr/bin/env python3
"""Punto de entrada: python fabrica.py <comando>. Ver README.md (INSTRUCTIVO)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fabrica.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
