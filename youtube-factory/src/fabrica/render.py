"""Producción de un video de principio a fin (con estados, caché y registro)."""
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

import soundfile as sf

from . import db
from .audio import SR as SR_AUDIO, ffmpeg, generar_musica, mezclar, pista_efectos
from .config import cargar_global, ruta
from .specs import canal_de, huella, validar
from .subtitles import escribir_srt, escribir_vtt
from .timeline import construir
from .visuals import frames
from .voice import SR as SR_VOZ


def cabecera(spec: dict, canal) -> dict:
    return {"serie": spec.get("serie", ""), "episodio": spec.get("episodio", ""), "marca": canal.nombre}


def musica_canal(canal) -> Path:
    cfg = canal.datos.get("musica", {})
    destino = ruta("assets", "music", f"{canal.clave}.wav")
    if not destino.exists():
        generar_musica(destino, tonica=cfg.get("tonica", "D"), modo=cfg.get("modo", "menor"),
                       bpm=int(cfg.get("bpm", 84)), semilla=int(cfg.get("semilla", 7)), brillo=float(cfg.get("brillo", 1.0)))
    return destino


def producir(spec: dict, forzar: bool = False) -> dict:
    """Genera video, subtítulos, portada y metadatos técnicos. Devuelve un resumen."""
    g = cargar_global()
    vid = spec["id"]
    canal = canal_de(spec)
    horizontal = spec["formato"] == "largo"
    rcfg = g["render"]["largo" if horizontal else "short"]
    fps = int(rcfg["fps"])
    t0 = time.time()
    errores = validar(spec)
    if errores:
        db.upsert_video(vid, canal=spec["canal"], formato=spec["formato"], fecha=str(spec["fecha"]),
                        titulo=spec.get("titulo"), estado="error", error="; ".join(errores))
        raise ValueError(f"{vid}: ficha inválida: " + "; ".join(errores))
    h = huella(spec)
    previo = db.obtener_video(vid)
    final = canal.dir_salida("videos") / f"{vid}.mp4"
    if (not forzar and previo and previo.get("spec_hash") == h and final.exists()
            and previo.get("estado") in ("render_ok", "aprobado", "revision")):
        return {"id": vid, "omitido": True, "motivo": "sin cambios desde el último render"}

    db.upsert_video(vid, canal=spec["canal"], formato=spec["formato"], fecha=str(spec["fecha"]),
                    titulo=spec["titulo"], estado="guion_ok", spec_hash=h, error=None,
                    intentos=(previo or {}).get("intentos", 0) + 1)
    trabajo = ruta("output", "_trabajo", vid)
    if trabajo.exists():
        shutil.rmtree(trabajo)
    trabajo.mkdir(parents=True)
    cab = cabecera(spec, canal)

    info = frames.analizar(spec, canal, cab, horizontal)
    lt = construir(spec, canal, info, max_palabras=int(canal.datos.get("subtitulos", {}).get("max_palabras", 4)))
    voz_wav = trabajo / "voz.wav"
    sf.write(voz_wav, lt.voz, SR_VOZ, subtype="PCM_16")
    db.upsert_video(vid, estado="voz_ok", duracion_s=round(lt.duracion, 2))
    db.registrar_evento(vid, "voz", f"{len(lt.frases)} frases, {lt.frases_cache} desde caché, {lt.duracion:.1f}s")

    transiciones = [e.inicio for e in lt.escenas[1:]]
    apariciones = [e.inicio + b for e in lt.escenas for b in e.beats[1:]]
    sfx = pista_efectos(lt.duracion, transiciones, apariciones)
    sfx_wav = trabajo / "sfx.wav"
    sf.write(sfx_wav, sfx, SR_AUDIO, subtype="PCM_16")
    audio_final = trabajo / "audio.wav"
    loud = mezclar(voz_wav, musica_canal(canal), sfx_wav, lt.duracion, audio_final,
                   g["render"]["musica_db"], g["render"]["sfx_db"], g["render"]["lufs_objetivo"], g["render"]["pico_verdadero_db"])

    lista = frames.render(lt, spec, canal, cab, info, trabajo / "frames", fps=fps, horizontal=horizontal)
    db.upsert_video(vid, estado="fotogramas_ok")

    tmp = trabajo / "video.mp4"
    ffmpeg([
        "-f", "concat", "-safe", "0", "-i", str(lista), "-i", str(audio_final),
        "-vf", f"fps={fps},format=yuv420p", "-c:v", "libx264", "-preset", g["render"]["preset"],
        "-crf", str(g["render"]["crf"]), "-profile:v", "high", "-tune", "stillimage",
        "-g", str(fps * 2), "-bf", "2", "-c:a", "aac", "-b:a", g["render"]["audio_bitrate"], "-ar", str(g["render"]["audio_hz"]),
        "-movflags", "+faststart", "-t", f"{lt.duracion:.3f}", str(tmp),
    ], timeout=1800)
    shutil.move(tmp, final)
    escribir_srt(lt, canal.dir_salida("subtitles") / f"{vid}.srt")
    escribir_vtt(lt, canal.dir_salida("subtitles") / f"{vid}.vtt")
    # Portada = estado final de la primera escena (es también el primer fotograma estable)
    frames.portada(canal, spec["escenas"][0]["visual"], cab, canal.dir_salida("thumbnails") / f"{vid}.png", horizontal)
    tecnico = {
        "id": vid, "duracion_s": round(lt.duracion, 3), "frases": len(lt.frases), "subtitulos": len(lt.subtitulos),
        "escenas": [{"inicio": round(e.inicio, 3), "fin": round(e.fin, 3), "beats": [round(b, 3) for b in e.beats],
                     "plantilla": e.visual["plantilla"]} for e in lt.escenas],
        "desbordes_texto": [o for i in info for o in i["overflow"]],
        "loudnorm_medido": loud, "fotogramas_unicos": len(list((trabajo / "frames").glob("*.png"))),
        "tts_cache": lt.frases_cache, "spec_hash": h, "segundos_produccion": round(time.time() - t0, 1),
        "texto_hablado": [f.hablado for f in lt.frases],
    }
    (trabajo / "tecnico.json").write_text(json.dumps(tecnico, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.copy(trabajo / "tecnico.json", canal.dir_salida("metadata") / f"{vid}.tecnico.json")
    # liberar espacio: los fotogramas se pueden regenerar
    shutil.rmtree(trabajo / "frames", ignore_errors=True)
    db.upsert_video(vid, estado="render_ok", duracion_s=round(lt.duracion, 2),
                    segundos_produccion=tecnico["segundos_produccion"])
    db.registrar_evento(vid, "render", f"listo en {tecnico['segundos_produccion']}s")
    return tecnico
