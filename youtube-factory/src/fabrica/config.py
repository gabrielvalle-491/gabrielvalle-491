"""Carga de configuración global y por canal."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]


def ruta(*partes: str) -> Path:
    return RAIZ.joinpath(*partes)


def _cargar_yaml(p: Path) -> dict:
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def cargar_env() -> None:
    """Lee .env (si existe) sin dependencias externas. Nunca imprime valores."""
    p = ruta(".env")
    if not p.exists():
        return
    for linea in p.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        k, v = linea.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


@dataclass
class Canal:
    clave: str
    datos: dict = field(repr=False)

    @property
    def nombre(self) -> str:
        return self.datos["marca"]["nombre"]

    @property
    def prefijo(self) -> str:
        return self.datos["prefijo_id"]

    @property
    def paleta(self) -> dict:
        return self.datos["identidad"]["paleta"]

    @property
    def fuentes(self) -> dict:
        return self.datos["identidad"]["tipografias"]

    @property
    def voz(self) -> dict:
        return self.datos["voz"]

    def dir_salida(self, *partes: str) -> Path:
        p = ruta("output", self.clave, *partes)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def dir_contenido(self) -> Path:
        return ruta("content", self.clave)


def cargar_global() -> dict:
    return _cargar_yaml(ruta("config", "global.yaml"))


def cargar_canales() -> dict[str, Canal]:
    canales = {}
    for p in sorted(ruta("config").glob("canal_*.yaml")):
        datos = _cargar_yaml(p)
        canales[p.stem] = Canal(p.stem, datos)
    return canales


def cargar_canal(clave: str) -> Canal:
    canales = cargar_canales()
    if clave not in canales:
        raise KeyError(f"Canal desconocido: {clave}. Disponibles: {', '.join(canales)}")
    return canales[clave]
