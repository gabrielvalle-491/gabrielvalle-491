"""Control de calidad. Ningún video llega a 'aprobado' solo porque el archivo existe:
se mide imagen, audio, sincronía, subtítulos, exactitud, riesgo, originalidad y metadatos."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from . import db
from .config import cargar_global, ruta
from .fact_check import revisar
from .research import similitud, tokens
from .specs import canal_de, listar_fichas, narracion_completa, validar
from .subtitles import leer_srt
from .textnorm import sin_marcas


def ffprobe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-500:])
    return json.loads(r.stdout)


def _ff_stderr(args: list[str]) -> str:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", *args], capture_output=True, text=True, timeout=600)
    return r.stderr


def medir_audio(path: Path) -> dict:
    err = _ff_stderr(["-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"])
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    sil = _ff_stderr(["-i", str(path), "-af", "silencedetect=noise=-45dB:d=1.0", "-f", "null", "-"])
    silencios = [(float(a), float(b)) for a, b in zip(re.findall(r"silence_start: (-?[\d.]+)", sil),
                                                      re.findall(r"silence_end: ([\d.]+)", sil))]
    return {"lufs": float(i[-1]) if i else None, "pico_db": float(tp[-1]) if tp else None, "silencios": silencios}


def medir_negro(path: Path) -> list[tuple[float, float]]:
    err = _ff_stderr(["-i", str(path), "-vf", "blackdetect=d=0.3:pix_th=0.03:pic_th=0.98", "-an", "-f", "null", "-"])
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err)]


class Informe:
    def __init__(self):
        self.items: list[dict] = []

    def add(self, nombre: str, ok: bool, detalle: str = "", peso: int = 5, critico: bool = False):
        self.items.append({"control": nombre, "ok": bool(ok), "detalle": detalle, "peso": peso, "critico": critico})

    @property
    def puntaje(self) -> float:
        return max(0.0, 100.0 - sum(i["peso"] for i in self.items if not i["ok"]))

    @property
    def criticos(self) -> list[dict]:
        return [i for i in self.items if not i["ok"] and i["critico"]]


def revisar_guion(spec: dict, biblioteca: list[dict] | None = None) -> Informe:
    """Controles que no necesitan el video (se pueden correr antes de producir)."""
    g = cargar_global()
    inf = Informe()
    err = validar(spec)
    inf.add("ficha completa y válida", not err, "; ".join(err), 30, True)
    if err:
        return inf
    fc = revisar(spec)
    inf.add("cálculos reproducibles correctos", not fc["calculos_fallidos"],
            "; ".join(f"{c['calculo']} → {c.get('valor', c.get('error'))} (esperado {c.get('esperado')})" for c in fc["calculos_fallidos"]), 25, True)
    inf.add("cifras de la narración con respaldo", not fc["cifras_sin_respaldo"],
            "sin respaldo: " + ", ".join(str(c) for c in fc["cifras_sin_respaldo"]), 15, True)
    inf.add("sin frases de riesgo ni voseo", not fc["riesgos"], "; ".join(fc["riesgos"]), 20, True)
    inf.add("ortografía (diccionario es + términos del proyecto)", len(fc["palabras_dudosas"]) <= 2,
            "dudosas: " + ", ".join(fc["palabras_dudosas"]), 6)
    inf.add("al menos una fuente verificable o cálculo propio", bool(spec.get("fuentes")), "", 15, True)
    # coherencia título-contenido
    cuerpo = " ".join([narracion_completa(spec), json.dumps([e["visual"] for e in spec["escenas"]], ensure_ascii=False)])
    tit = set(tokens(spec["titulo"]))
    comunes = tit & set(tokens(cuerpo))
    inf.add("título coherente con el contenido", len(comunes) >= max(1, min(2, len(tit) // 3)),
            f"palabras del título presentes: {sorted(comunes)}", 10, True)
    # declaración de contenido sintético y licencias
    ds = spec.get("declaracion_sintetica") or {}
    inf.add("declaración de contenido sintético evaluada", bool(ds.get("decision")), str(ds), 5)
    recursos = spec.get("recursos", [])
    inf.add("recursos externos con licencia documentada", all(r.get("licencia") for r in recursos),
            ", ".join(r.get("nombre", "?") for r in recursos if not r.get("licencia")), 15, True)
    # originalidad frente a la biblioteca
    if biblioteca is None:
        biblioteca = listar_fichas()
    propia = narracion_completa(spec)
    peores = sorted(((similitud(propia, narracion_completa(o)), o["id"]) for o in biblioteca if o["id"] != spec["id"]), reverse=True)[:1]
    lim = float(g["calidad"]["similitud_maxima"])
    if peores:
        inf.add("diferenciación frente a la biblioteca", peores[0][0] <= lim, f"más parecido: {peores[0][1]} ({peores[0][0]:.2f})", 20, True)
    gancho = re.split(r"(?<=[.?!])\s", sin_marcas(spec["escenas"][0]["narracion"]))[0]
    inf.add("gancho en la primera frase (≤ 18 palabras)", len(gancho.split()) <= 18, gancho, 4)
    return inf


def revisar_video(spec: dict, biblioteca: list[dict] | None = None) -> Informe:
    g = cargar_global()
    canal = canal_de(spec)
    vid = spec["id"]
    inf = revisar_guion(spec, biblioteca)
    video = canal.dir_salida("videos") / f"{vid}.mp4"
    if not video.exists() or video.stat().st_size < 50_000:
        inf.add("archivo de video generado", False, str(video), 100, True)
        return inf
    try:
        pr = ffprobe(video)
    except Exception as e:  # noqa: BLE001
        inf.add("archivo reproducible (ffprobe)", False, str(e), 100, True)
        return inf
    inf.add("archivo reproducible (ffprobe)", True)
    v = next((s for s in pr["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
    largo = spec["formato"] == "largo"
    W, H = (1920, 1080) if largo else (1080, 1920)
    inf.add("resolución y relación de aspecto", v and int(v["width"]) == W and int(v["height"]) == H,
            f"{v and v['width']}x{v and v['height']}", 30, True)
    inf.add("códec H.264 yuv420p", v and v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p", f"{v and v['codec_name']} {v and v.get('pix_fmt')}", 15, True)
    fps = eval(v["r_frame_rate"]) if v else 0  # noqa: S307 (formato "30/1" de ffprobe)
    inf.add("30 fps constantes", abs(fps - 30) < 0.01, str(fps), 10, True)
    inf.add("audio AAC 48 kHz estéreo", a and a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2,
            f"{a and a['codec_name']} {a and a['sample_rate']} {a and a['channels']}", 15, True)
    dur = float(pr["format"]["duration"])
    if largo:
        inf.add("duración de video largo (4-15 min)", 240 <= dur <= 900, f"{dur:.1f}s", 10)
    else:
        inf.add("duración de Short (≤ 60 s objetivo, ≤ 180 s límite)", g["calidad"]["short_min_s"] <= dur <= g["calidad"]["short_max_s"],
                f"{dur:.1f}s", 15, dur > 180)
    inf.add("tamaño razonable (< 256 GB y > 0)", 0 < video.stat().st_size < 256e9, f"{video.stat().st_size/1e6:.1f} MB", 5, True)
    au = medir_audio(video)
    inf.add("volumen integrado ≈ -14 LUFS", au["lufs"] is not None and abs(au["lufs"] - g["render"]["lufs_objetivo"]) <= 1.5,
            f"{au['lufs']} LUFS", 8)
    inf.add("sin saturación (pico ≤ -1 dBFS)", au["pico_db"] is not None and au["pico_db"] <= -0.9, f"pico {au['pico_db']} dBFS", 8)
    largos_sil = [s for s in au["silencios"] if (s[1] - s[0]) > 1.2 and s[1] < dur - 0.3]
    inf.add("sin silencios largos en medio", not largos_sil, str(largos_sil), 10, True)
    negros = medir_negro(video)
    inf.add("sin pantallas negras", not negros, str(negros), 20, True)
    tec_p = canal.dir_salida("metadata") / f"{vid}.tecnico.json"
    tec = json.loads(tec_p.read_text(encoding="utf-8")) if tec_p.exists() else {}
    inf.add("textos dentro de su caja (sin desbordes)", not tec.get("desbordes_texto"), str(tec.get("desbordes_texto")), 10, True)
    inf.add("duración del archivo = línea de tiempo", tec and abs(tec.get("duracion_s", 0) - dur) < 0.25,
            f"archivo {dur:.2f}s vs plan {tec.get('duracion_s')}", 10, True)
    # voz completa: cada frase hablada, velocidad plausible
    hablado = " ".join(tec.get("texto_hablado", []))
    cps = len(hablado) / max(1, dur)
    inf.add("voz completa (velocidad 9-20 caracteres/s)", 9 <= cps <= 20, f"{cps:.1f} car/s", 15, True)
    # subtítulos
    srt = canal.dir_salida("subtitles") / f"{vid}.srt"
    if srt.exists():
        bloques = leer_srt(srt)
        mono = all(b[0] < b[1] for b in bloques) and all(x[1] <= y[0] + 1e-3 for x, y in zip(bloques, bloques[1:]))
        texto_srt = " ".join(b[2] for b in bloques)
        sim = similitud(texto_srt, sin_marcas(narracion_completa(spec)))
        inf.add("subtítulos sincronizados y ordenados", mono and bloques and bloques[-1][1] <= dur + 0.05, f"{len(bloques)} bloques", 15, True)
        inf.add("subtítulos = narración", sim > 0.9, f"similitud {sim:.2f}", 15, True)
        inf.add("subtítulos legibles (≤ 84 caracteres por bloque)", all(len(b[2]) <= 84 for b in bloques), "", 4)
    else:
        inf.add("subtítulos generados", False, str(srt), 20, True)
    portada = canal.dir_salida("thumbnails") / f"{vid}.png"
    inf.add("portada/primer fotograma generado", portada.exists() and portada.stat().st_size > 10_000, str(portada.name), 5)
    inf.add("coste registrado", True, "USD 0 en servicios (todo local); electricidad estimada en el informe de costos", 0)
    return inf


def evaluar_y_registrar(spec: dict, biblioteca: list[dict] | None = None) -> dict:
    g = cargar_global()
    inf = revisar_video(spec, biblioteca)
    canal = canal_de(spec)
    aprobado = inf.puntaje >= g["calidad"]["puntaje_minimo"] and not inf.criticos
    estado = "aprobado" if aprobado else "revision"
    motivos = [f"{i['control']}: {i['detalle']}" for i in inf.items if not i["ok"]]
    datos = {"id": spec["id"], "puntaje": inf.puntaje, "estado": estado, "criticos": inf.criticos,
             "motivos": motivos, "controles": inf.items}
    (canal.dir_salida("metadata") / f"{spec['id']}.qa.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    db.upsert_video(spec["id"], estado=estado, qa_puntaje=inf.puntaje, qa_detalle=json.dumps(motivos, ensure_ascii=False))
    db.registrar_evento(spec["id"], "qa", f"{estado} ({inf.puntaje:.0f}/100) " + "; ".join(motivos)[:900],
                        "info" if aprobado else "aviso")
    return datos


def informe_control_final() -> str:
    """Control final de la biblioteca: aprobados, pendientes con motivo y estadísticas reales."""
    import statistics

    from .config import cargar_canales
    lineas = ["# Control final de la biblioteca", ""]
    for clave, canal in cargar_canales().items():
        fichas = [f for f in listar_fichas(clave) if not f["id"].endswith("TEST")]
        vids = {v["id"]: v for v in db.listar_videos(clave)}
        aprob = [f for f in fichas if vids.get(f["id"], {}).get("estado") == "aprobado"]
        pend = [f for f in fichas if f not in aprob]
        durs = [vids[f["id"]]["duracion_s"] for f in aprob if vids[f["id"]].get("duracion_s")]
        segs = [vids[f["id"]]["segundos_produccion"] for f in aprob if vids[f["id"]].get("segundos_produccion")]
        lineas += [f"## {canal.nombre} ({clave})", "",
                   f"- Guiones: {len(fichas)} · **aprobados: {len(aprob)}** · pendientes: {len(pend)}"]
        if durs:
            lineas.append(f"- Duración de los aprobados: mín {min(durs):.1f} s · mediana {statistics.median(durs):.1f} s · máx {max(durs):.1f} s")
        if segs:
            lineas.append(f"- Tiempo de producción por video (mediana): {statistics.median(segs):.0f} s")
        tipos = {}
        for f in fichas:
            tipos[f["tipo_editorial"]] = tipos.get(f["tipo_editorial"], 0) + 1
        lineas.append("- Mezcla editorial: " + ", ".join(f"{k} {v}" for k, v in sorted(tipos.items(), key=lambda x: -x[1])))
        lineas += ["", "| ID | Fecha | Estado | QA | Título / motivo |", "|---|---|---|---|---|"]
        for f in fichas:
            v = vids.get(f["id"], {})
            est = v.get("estado", "sin_producir")
            det = f["titulo"]
            if est != "aprobado":
                motivos = json.loads(v["qa_detalle"]) if v.get("qa_detalle") else [v.get("error") or "no producido todavía"]
                det = "; ".join(m for m in motivos if m)[:180]
            lineas.append(f"| {f['id']} | {f['fecha']} | {est} | {v.get('qa_puntaje') or ''} | {det.replace('|', '/')} |")
        lineas.append("")
    lineas += ["Ver también `reports/verificar_antes_de_publicar.md` (verificaciones manuales recomendadas).", ""]
    texto = "\n".join(lineas)
    ruta("reports", "control_final.md").write_text(texto, encoding="utf-8")
    return texto
