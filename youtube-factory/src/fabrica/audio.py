"""Audio original: música de fondo procedural y efectos sutiles generados por código.

No se usa música de terceros: todo se sintetiza aquí, así que la licencia es propia y no hay
riesgo de reclamos por derechos de autor de bibliotecas ajenas.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000
NOTAS = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}


def _freq(semitonos_desde_a4: float) -> float:
    return 440.0 * 2 ** (semitonos_desde_a4 / 12)


def _lowpass(x: np.ndarray, corte_hz: float) -> np.ndarray:
    a = np.exp(-2 * np.pi * corte_hz / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # filtro de un polo (suficiente para suavizar el pad)
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def generar_musica(destino: Path, tonica: str = "D", modo: str = "menor", bpm: int = 84,
                   compases_por_acorde: int = 2, semilla: int = 7, brillo: float = 1.0) -> Path:
    """Pad ambiental + arpegio suave + bajo. Loop perfecto de 4 acordes."""
    rng = np.random.default_rng(semilla)
    base = NOTAS[tonica] - 12  # octava 3
    if modo == "menor":
        prog = [[0, 3, 7, 10], [-4, 0, 3, 7], [-9, -5, -2, 3], [-2, 2, 5, 9]]  # i - VI - III - VII
    else:
        prog = [[0, 4, 7, 11], [7, 11, 14, 17], [9, 12, 16, 19], [5, 9, 12, 16]]  # I - V - vi - IV
    beat = 60 / bpm
    dur_acorde = beat * 4 * compases_por_acorde
    n_acorde = int(dur_acorde * SR)
    total = n_acorde * len(prog)
    t = np.arange(n_acorde) / SR
    L = np.zeros(total, dtype=np.float64)
    R = np.zeros(total, dtype=np.float64)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur_acorde - t) / 1.0).clip(0, 1)
    for k, acorde in enumerate(prog):
        seg = slice(k * n_acorde, (k + 1) * n_acorde)
        pad_l = np.zeros(n_acorde)
        pad_r = np.zeros(n_acorde)
        for nota in acorde:
            f = _freq(base + nota)
            for det, pan in ((-0.07, 0.8), (0.07, 0.2)):
                ff = f * 2 ** (det / 12)
                ph = rng.uniform(0, 2 * np.pi)
                onda = np.sin(2 * np.pi * ff * t + ph) + 0.25 * np.sin(4 * np.pi * ff * t + ph) * brillo
                pad_l += onda * pan
                pad_r += onda * (1 - pan)
        bajo = np.sin(2 * np.pi * _freq(base + acorde[0] - 12) * t) * 0.9
        L[seg] += (pad_l * 0.16 + bajo * 0.35) * env
        R[seg] += (pad_r * 0.16 + bajo * 0.35) * env
        # arpegio en corcheas
        paso = beat / 2
        n_paso = int(paso * SR)
        tt = np.arange(n_paso) / SR
        notas_arp = [acorde[i % len(acorde)] + 12 for i in (0, 1, 2, 3, 2, 1, 3, 2)]
        for j in range(int(dur_acorde / paso)):
            if rng.random() < 0.18:
                continue
            f = _freq(base + notas_arp[j % len(notas_arp)])
            pluck = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) * 0.10
            a = k * n_acorde + j * n_paso
            b = min(a + n_paso, total)
            pan = 0.35 + 0.3 * (j % 2)
            L[a:b] += pluck[: b - a] * pan
            R[a:b] += pluck[: b - a] * (1 - pan)
    L = _lowpass(L, 2600 * brillo)
    R = _lowpass(R, 2600 * brillo)
    est = np.stack([L, R], axis=1)
    rms = np.sqrt(np.mean(est ** 2))
    est = est * (10 ** (-18 / 20) / max(rms, 1e-9))
    est = np.clip(est, -0.98, 0.98)
    destino.parent.mkdir(parents=True, exist_ok=True)
    sf.write(destino, est.astype("float32"), SR, subtype="PCM_16")
    return destino


def _pop(f0=1200.0, f1=600.0, dur=0.07):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 55)


def _whoosh(dur=0.32, semilla=1):
    rng = np.random.default_rng(semilla)
    n = int(dur * SR)
    ruido = rng.standard_normal(n)
    t = np.arange(n) / SR
    env = np.sin(np.pi * t / dur) ** 2
    corte = np.linspace(400, 3200, n)
    y = np.empty(n)
    acc = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * corte[i] / SR)
        acc = (1 - a) * ruido[i] + a * acc
        y[i] = acc
    return y * env * 1.6


def pista_efectos(duracion: float, transiciones: list[float], apariciones: list[float]) -> np.ndarray:
    pista = np.zeros(int(duracion * SR) + SR, dtype=np.float64)
    wh, pop = _whoosh(), _pop()
    for t in transiciones:
        a = int(max(0, t - 0.12) * SR)
        pista[a:a + len(wh)] += wh[: len(pista) - a] * 0.35
    for t in apariciones:
        a = int(t * SR)
        pista[a:a + len(pop)] += pop[: len(pista) - a] * 0.18
    return pista[: int(duracion * SR)].astype("float32")


def ffmpeg(args: list[str], timeout: int = 900) -> subprocess.CompletedProcess:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-y", *args], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError("FFmpeg falló: " + r.stderr[-1500:])
    return r


def mezclar(voz_wav: Path, musica_wav: Path, sfx_wav: Path, duracion: float, destino: Path,
            musica_db: float, sfx_db: float, lufs: float, tp: float) -> dict:
    """Mezcla voz + música (con compresión lateral) + efectos y normaliza a LUFS objetivo en dos pasadas."""
    mezcla = destino.with_name("mezcla_previa.wav")
    filtro = (
        f"[0:a]aresample={SR},pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,asplit=2[v1][v2];"
        f"[1:a]atrim=0:{duracion:.3f},volume={musica_db}dB,afade=t=in:d=0.6,afade=t=out:st={max(0, duracion-1.4):.3f}:d=1.3[m];"
        f"[m][v2]sidechaincompress=threshold=0.04:ratio=5:attack=25:release=350[md];"
        f"[2:a]aresample={SR},pan=stereo|c0=c0|c1=c0,volume={sfx_db}dB[s];"
        f"[v1][md][s]amix=inputs=3:normalize=0:duration=first[out]"
    )
    ffmpeg(["-i", str(voz_wav), "-stream_loop", "-1", "-i", str(musica_wav), "-i", str(sfx_wav),
            "-filter_complex", filtro, "-map", "[out]", "-t", f"{duracion:.3f}", "-ar", str(SR), str(mezcla)])
    r = ffmpeg(["-i", str(mezcla), "-af", f"loudnorm=I={lufs}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"])
    medido = json.loads(re.findall(r"\{[^{}]+\}", r.stderr)[-1])
    filtro2 = (f"loudnorm=I={lufs}:TP={tp}:LRA=11:measured_I={medido['input_i']}:measured_TP={medido['input_tp']}:"
               f"measured_LRA={medido['input_lra']}:measured_thresh={medido['input_thresh']}:offset={medido['target_offset']}:linear=true")
    ffmpeg(["-i", str(mezcla), "-af", filtro2, "-ar", str(SR), str(destino)])
    mezcla.unlink(missing_ok=True)
    return medido
