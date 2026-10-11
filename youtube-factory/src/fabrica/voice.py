"""Síntesis de voz local con caché. Motor por defecto: Kokoro-82M (Apache-2.0) vía kokoro-onnx.

Cada frase se sintetiza por separado: así conocemos su duración exacta y los subtítulos
quedan sincronizados por construcción (no se adivinan tiempos).
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import threading
from pathlib import Path

import numpy as np
import soundfile as sf

from .config import cargar_global, ruta

SR = 24000
_LOCK = threading.Lock()
_KOKORO = None


class ErrorVoz(RuntimeError):
    pass


def _kokoro():
    global _KOKORO
    with _LOCK:
        if _KOKORO is None:
            cfg = cargar_global()["voz"]
            modelo, voces = ruta(cfg["modelo"]), ruta(cfg["voces"])
            if not modelo.exists() or not voces.exists():
                raise ErrorVoz(
                    "Falta el modelo de voz Kokoro. Ejecutá: python fabrica.py iniciar "
                    f"(se esperaba {modelo.name} y {voces.name} en la carpeta models/)"
                )
            from kokoro_onnx import Kokoro
            _KOKORO = Kokoro(str(modelo), str(voces))
        return _KOKORO


def estilo_voz(voz_cfg: dict):
    """Devuelve el nombre de voz o una mezcla ponderada (voz propia del canal)."""
    mezcla = voz_cfg.get("mezcla")
    if not mezcla:
        return voz_cfg["voz"]
    k = _kokoro()
    total = sum(mezcla.values())
    return sum(k.get_voice_style(n) * (w / total) for n, w in mezcla.items())


def recortar_silencio(audio: np.ndarray, umbral_db: float = -42.0, margen_s: float = 0.03) -> np.ndarray:
    if audio.size == 0:
        return audio
    env = np.abs(audio)
    umbral = 10 ** (umbral_db / 20) * max(env.max(), 1e-9)
    idx = np.where(env > umbral)[0]
    if idx.size == 0:
        return audio[:0]
    m = int(margen_s * SR)
    return audio[max(0, idx[0] - m): min(audio.size, idx[-1] + m)]


def _clave_cache(motor: str, voz_cfg: dict, texto: str) -> str:
    h = hashlib.sha1(json.dumps([motor, voz_cfg, texto], sort_keys=True, ensure_ascii=False).encode())
    return h.hexdigest()[:20]


def sintetizar(texto: str, voz_cfg: dict) -> tuple[np.ndarray, Path, bool]:
    """Sintetiza una frase. Devuelve (audio, ruta_wav, vino_de_cache)."""
    cfg = cargar_global()["voz"]
    motor = voz_cfg.get("motor", cfg["motor"])
    cache = ruta("data", "cache", "tts")
    cache.mkdir(parents=True, exist_ok=True)
    destino = cache / f"{_clave_cache(motor, voz_cfg, texto)}.wav"
    if destino.exists():
        audio, _ = sf.read(destino, dtype="float32")
        return audio, destino, True
    if motor == "kokoro":
        k = _kokoro()
        audio, sr = k.create(
            texto, voice=estilo_voz(voz_cfg), speed=float(voz_cfg.get("velocidad", 1.0)),
            lang=cfg.get("idioma_fonetico", "es-419"),
        )
        if sr != SR:
            raise ErrorVoz(f"Frecuencia inesperada {sr}")
    elif motor == "piper":
        audio = _piper(texto, voz_cfg)
    elif motor == "espeak":
        audio = _espeak(texto, voz_cfg)
    else:
        raise ErrorVoz(f"Motor de voz desconocido: {motor}")
    audio = recortar_silencio(np.asarray(audio, dtype="float32"))
    if audio.size < SR * 0.2:
        raise ErrorVoz(f"La voz quedó vacía o demasiado corta para: {texto[:60]}")
    pico = np.abs(audio).max()
    if pico > 0:
        audio = audio * (0.89 / pico)  # -1 dBFS por frase; el volumen final se normaliza después
    sf.write(destino, audio, SR, subtype="PCM_16")
    return audio, destino, False


def _piper(texto: str, voz_cfg: dict) -> np.ndarray:
    modelo = ruta(voz_cfg["modelo_piper"])
    if not modelo.exists():
        raise ErrorVoz(f"No existe el modelo Piper {modelo}")
    tmp = ruta("data", "cache", "tts", "_piper_tmp.wav")
    r = subprocess.run(
        ["python", "-m", "piper", "-m", str(modelo), "-f", str(tmp)],
        input=texto.encode("utf-8"), capture_output=True, timeout=120,
    )
    if r.returncode != 0:
        raise ErrorVoz(r.stderr.decode("utf-8", "ignore")[-500:])
    audio, sr = sf.read(tmp, dtype="float32")
    if sr != SR:
        idx = np.linspace(0, len(audio) - 1, int(len(audio) * SR / sr))
        audio = np.interp(idx, np.arange(len(audio)), audio).astype("float32")
    return audio


def _espeak(texto: str, voz_cfg: dict) -> np.ndarray:
    """Solo para pruebas sin modelo: voz robótica. El control de calidad la marca como no publicable."""
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe:
        raise ErrorVoz("espeak-ng no está instalado")
    tmp = ruta("data", "cache", "tts", "_espeak_tmp.wav")
    subprocess.run([exe, "-v", "es-419", "-w", str(tmp), texto], check=True, timeout=60)
    audio, sr = sf.read(tmp, dtype="float32")
    idx = np.linspace(0, len(audio) - 1, int(len(audio) * SR / sr))
    return np.interp(idx, np.arange(len(audio)), audio).astype("float32")
