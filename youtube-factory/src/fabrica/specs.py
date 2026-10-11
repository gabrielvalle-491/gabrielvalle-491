"""Guiones (fichas de video) en YAML: carga, validación y huella para caché/versionado."""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import yaml

from .config import Canal, cargar_canales, ruta
from .textnorm import dividir_frases
from .visuals.templates import PLANTILLAS

CAMPOS_OBLIGATORIOS = [
    "id", "canal", "fecha", "formato", "pilar", "serie", "tipo_editorial", "idea", "objetivo",
    "publico", "hipotesis", "gancho", "titulo", "titulos_alternativos", "descripcion", "cta",
    "hashtags", "escenas", "fuentes", "riesgos",
]
TIPOS_EDITORIALES = {
    "tutorial", "error_comun", "comparacion", "experimento", "caso_practico", "contraintuitivo",
    "mito", "historia", "herramienta", "serie_episodica", "quiz",
}


class ErrorFicha(ValueError):
    pass


def cargar(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    spec["_ruta"] = str(path)
    return spec


def huella(spec: dict) -> str:
    limpio = {k: v for k, v in spec.items() if not k.startswith("_") and k not in ("estado",)}
    return hashlib.sha1(json.dumps(limpio, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]


def narracion_completa(spec: dict) -> str:
    return " ".join(e["narracion"].strip() for e in spec["escenas"])


def validar(spec: dict) -> list[str]:
    """Devuelve lista de errores (vacía si la ficha es válida)."""
    err = []
    for c in CAMPOS_OBLIGATORIOS:
        if c not in spec or spec[c] in (None, "", []):
            err.append(f"falta el campo '{c}'")
    if err:
        return err
    if spec["formato"] not in ("short", "largo"):
        err.append("formato debe ser 'short' o 'largo'")
    if spec["tipo_editorial"] not in TIPOS_EDITORIALES:
        err.append(f"tipo_editorial inválido: {spec['tipo_editorial']}")
    if len(spec["titulos_alternativos"]) < 3:
        err.append("se requieren 3 títulos alternativos")
    if len(spec["titulo"]) > 100:
        err.append("el título supera 100 caracteres (límite de YouTube)")
    if len(spec["descripcion"]) > 4800:
        err.append("descripción demasiado larga")
    try:
        date.fromisoformat(str(spec["fecha"]))
    except ValueError:
        err.append("fecha inválida (usar AAAA-MM-DD)")
    for i, e in enumerate(spec["escenas"]):
        if not e.get("narracion"):
            err.append(f"escena {i+1}: falta narración")
        v = e.get("visual") or {}
        if v.get("plantilla") not in PLANTILLAS:
            err.append(f"escena {i+1}: plantilla desconocida '{v.get('plantilla')}'")
    for f in spec["fuentes"]:
        if not f.get("url") and not f.get("calculo"):
            err.append("cada fuente necesita 'url' o 'calculo' (cálculo propio reproducible)")
        if not f.get("respalda"):
            err.append(f"fuente sin campo 'respalda': {f.get('url') or f.get('calculo')}")
    if spec["formato"] == "short":
        palabras = len(narracion_completa(spec).split())
        if palabras > 190:
            err.append(f"narración demasiado larga para un Short ({palabras} palabras)")
        if palabras < 40:
            err.append(f"narración demasiado corta ({palabras} palabras)")
    return err


def listar_fichas(canal: str | None = None) -> list[dict]:
    canales = [canal] if canal else list(cargar_canales())
    out = []
    for c in canales:
        for p in sorted(ruta("content", c).glob("*.yaml")):
            out.append(cargar(p))
    return sorted(out, key=lambda s: (str(s.get("fecha")), s.get("id")))


def buscar_ficha(vid: str) -> dict:
    for c in cargar_canales():
        p = ruta("content", c, f"{vid}.yaml")
        if p.exists():
            return cargar(p)
    raise ErrorFicha(f"No existe la ficha {vid}")


def frases_escena(escena: dict) -> list[str]:
    return dividir_frases(escena["narracion"])


def canal_de(spec: dict) -> Canal:
    return cargar_canales()[spec["canal"]]
