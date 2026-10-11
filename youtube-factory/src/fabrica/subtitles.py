"""Subtítulos SRT y VTT (para subir como subtítulos cerrados además de los quemados en el video)."""
from __future__ import annotations

from pathlib import Path

from .textnorm import sin_marcas


def _ts(seg: float, sep: str) -> str:
    ms = int(round(seg * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def bloques_por_frase(lt) -> list[tuple[float, float, str]]:
    """Para subtítulos cerrados conviene una frase por bloque (más legible que trozos de 4 palabras)."""
    out = []
    for f in lt.frases:
        texto = sin_marcas(f.pantalla)
        if len(texto) > 84:  # partir frases largas en dos líneas/bloques
            palabras = texto.split()
            mitad = len(palabras) // 2
            m = f.inicio + (f.fin - f.inicio) * (len(" ".join(palabras[:mitad])) / len(texto))
            out.append((f.inicio, m, " ".join(palabras[:mitad])))
            out.append((m, f.fin, " ".join(palabras[mitad:])))
        else:
            out.append((f.inicio, f.fin, texto))
    return out


def escribir_srt(lt, destino: Path) -> Path:
    lineas = []
    for i, (a, b, t) in enumerate(bloques_por_frase(lt), start=1):
        lineas += [str(i), f"{_ts(a, ',')} --> {_ts(b, ',')}", t, ""]
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


def escribir_vtt(lt, destino: Path) -> Path:
    lineas = ["WEBVTT", ""]
    for a, b, t in bloques_por_frase(lt):
        lineas += [f"{_ts(a, '.')} --> {_ts(b, '.')}", t, ""]
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


def leer_srt(path: Path) -> list[tuple[float, float, str]]:
    def p(ts):
        h, m, r = ts.split(":")
        s, ms = r.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    out = []
    for bloque in path.read_text(encoding="utf-8").strip().split("\n\n"):
        ls = bloque.splitlines()
        if len(ls) >= 3:
            a, b = ls[1].split(" --> ")
            out.append((p(a), p(b), " ".join(ls[2:])))
    return out
