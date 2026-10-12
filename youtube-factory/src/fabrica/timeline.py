"""Línea de tiempo: voz por frase -> tiempos exactos de escenas, beats y subtítulos."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np

from .config import cargar_global
from .textnorm import dividir_frases, texto_hablado, texto_pantalla
from .voice import SR, sintetizar


@dataclass
class Frase:
    escena: int
    pantalla: str
    hablado: str
    inicio: float
    fin: float
    audio: np.ndarray = field(repr=False)
    cache: bool = False


@dataclass
class Subtitulo:
    inicio: float
    fin: float
    texto: str  # puede contener *resaltado*


@dataclass
class Escena:
    indice: int
    inicio: float
    fin: float
    beats: list[float]  # tiempos relativos al inicio de la escena
    visual: dict


@dataclass
class LineaTiempo:
    frases: list[Frase]
    escenas: list[Escena]
    subtitulos: list[Subtitulo]
    duracion: float
    voz: np.ndarray = field(repr=False)
    frases_cache: int = 0


def _trozos(texto: str, max_palabras: int = 4) -> list[str]:
    """Divide una frase en bloques cortos de subtítulo respetando la puntuación."""
    # mantener unidas las cifras con separador de miles ("1 403") y "US$ 100"
    texto = re.sub(r"(?<=\d)[ \u202f](?=\d{3}\b)", "\u00a0", texto)
    texto = re.sub(r"(US\$|\$)\s(?=\d)", "\\1\u00a0", texto)
    texto = re.sub(r"(?<=\d)\s(?=%)", "\u00a0", texto)
    palabras = [w for w in texto.split(" ") if w]
    trozos, actual = [], []
    for p in palabras:
        actual.append(p)
        limpia = p.strip("*")
        corte_puntuacion = limpia.endswith((",", ";", ":", ".", "?", "!", "…")) and len(actual) >= 2
        if len(actual) >= max_palabras or corte_puntuacion:
            trozos.append(" ".join(actual))
            actual = []
    if actual:
        if trozos and len(actual) == 1 and len(trozos[-1].split()) < max_palabras + 1:
            trozos[-1] += " " + actual[0]
        else:
            trozos.append(" ".join(actual))
    return _balancear_marcas(trozos)


def _balancear_marcas(trozos: list[str]) -> list[str]:
    """Si un *resaltado* quedó partido entre dos trozos, lo cierra y lo reabre."""
    out, abierto = [], False
    for t in trozos:
        if abierto:
            t = "*" + t
        n = t.count("*")
        abierto = n % 2 == 1
        if abierto:
            t = t + "*"
        out.append(t)
    return out


def _peso(t: str) -> float:
    h = texto_hablado(t)
    return len(re.sub(r"[^\wáéíóúñü]", "", h, flags=re.I)) + 3


def construir(spec: dict, canal, beats_por_escena: list[dict] | None = None, max_palabras: int = 4) -> LineaTiempo:
    cfg = cargar_global()["voz"]
    p_frase, p_escena = float(cfg["pausa_frase_s"]), float(cfg["pausa_escena_s"])
    lexico = canal.datos.get("lexico", {})
    t = 0.12
    frases: list[Frase] = []
    trozos_voz = [np.zeros(int(SR * t), dtype="float32")]
    escenas_t = []
    cache = 0
    for i, esc in enumerate(spec["escenas"]):
        inicio_escena = t
        for j, fr in enumerate(dividir_frases(esc["narracion"])):
            hablado = texto_hablado(fr, lexico)
            audio, _, en_cache = sintetizar(hablado, canal.voz)
            cache += en_cache
            dur = len(audio) / SR
            frases.append(Frase(i, texto_pantalla(fr), hablado, t, t + dur, audio, en_cache))
            trozos_voz.append(audio)
            t += dur
            pausa = p_frase + (0.08 if fr.rstrip().endswith("?") else 0)
            trozos_voz.append(np.zeros(int(SR * pausa), dtype="float32"))
            t += pausa
        if i < len(spec["escenas"]) - 1:
            extra = p_escena - p_frase
            trozos_voz.append(np.zeros(int(SR * extra), dtype="float32"))
            t += extra
        escenas_t.append((inicio_escena, t))
    cola = float(spec.get("cola_s", 0.7))
    trozos_voz.append(np.zeros(int(SR * cola), dtype="float32"))
    t += cola
    voz = np.concatenate(trozos_voz)
    duracion = len(voz) / SR

    escenas = []
    for i, (ini, fin) in enumerate(escenas_t):
        # la imagen entra un instante antes que la voz
        ini_v = 0.0 if i == 0 else max(0.0, ini - 0.08)
        fin_v = escenas_t[i + 1][0] - 0.08 if i + 1 < len(escenas_t) else duracion
        fr_esc = [f for f in frases if f.escena == i]
        n_beats = (beats_por_escena[i]["n"] if beats_por_escena else 1)
        beats = _tiempos_beats(spec["escenas"][i], fr_esc, ini_v, fin_v, n_beats)
        if i == 0:
            beats[0] = -5.0  # el primer fotograma ya muestra el gancho completo (portada en el feed)
        escenas.append(Escena(i, ini_v, fin_v, beats, spec["escenas"][i]["visual"]))

    subs: list[Subtitulo] = []
    for f in frases:
        trozos = _trozos(f.pantalla, max_palabras)
        pesos = [_peso(x) for x in trozos]
        total = sum(pesos)
        c = f.inicio
        for tr, w in zip(trozos, pesos):
            d = (f.fin - f.inicio) * w / total
            subs.append(Subtitulo(c, c + d, tr))
            c += d
    # cada subtítulo permanece hasta que empieza el siguiente si el hueco es corto
    for a, b in zip(subs, subs[1:]):
        if b.inicio - a.fin < 0.35:
            a.fin = b.inicio
    return LineaTiempo(frases, escenas, subs, duracion, voz, cache)


def _tiempos_beats(esc: dict, frases, ini_v: float, fin_v: float, n: int) -> list[float]:
    """Beat k empieza con la frase k. Si hay más beats que frases se reparten en la última.
    Se puede forzar con 'beats': [segundos relativos] o 'beats_frase': [índices de frase]."""
    if esc.get("beats"):
        return [float(x) for x in esc["beats"]]
    if not frases:
        return [0.0] * n
    if esc.get("beats_frase"):
        return [max(0.0, frases[min(k, len(frases) - 1)].inicio - ini_v) for k in esc["beats_frase"]]
    tiempos = [0.0]
    for k in range(1, n):
        if k < len(frases):
            tiempos.append(max(0.0, frases[k].inicio - ini_v - 0.05))
        else:
            ult = frases[-1]
            resto = n - len(frases) + 1
            paso = (ult.fin - ult.inicio) / (resto + 0.5)
            tiempos.append(ult.inicio - ini_v + paso * (k - len(frases) + 1))
    return tiempos
