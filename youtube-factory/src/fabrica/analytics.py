"""Analítica: métricas oficiales (YouTube Analytics API) o exportaciones de YouTube Studio, e informe semanal.

No se inventan métricas: si un dato no existe en la fuente, el informe lo dice. La curva de retención
completa y las "visualizaciones interesadas" pueden requerir exportación desde YouTube Studio.
"""
from __future__ import annotations

import csv
import statistics
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from . import db
from .config import cargar_canal, ruta
from .specs import listar_fichas

METRICAS_API = ["views", "estimatedMinutesWatched", "averageViewDuration", "averageViewPercentage",
                "likes", "comments", "shares", "subscribersGained", "subscribersLost"]

# Encabezados de exportaciones de YouTube Studio (inglés y español) → nombre interno
ALIAS = {
    "content": "youtube_id", "contenido": "youtube_id",
    "video title": "titulo", "título del video": "titulo", "titulo del video": "titulo",
    "views": "views", "visualizaciones": "views", "vistas": "views",
    "engaged views": "engagedViews", "visualizaciones interesadas": "engagedViews",
    "watch time (hours)": "watchHours", "tiempo de visualización (horas)": "watchHours",
    "average view duration": "averageViewDuration", "duración promedio de vista": "averageViewDuration",
    "duración media de las visualizaciones": "averageViewDuration",
    "average percentage viewed (%)": "averageViewPercentage", "porcentaje promedio visto (%)": "averageViewPercentage",
    "porcentaje medio visto (%)": "averageViewPercentage",
    "subscribers": "subscribersGained", "suscriptores": "subscribersGained",
    "subscribers gained": "subscribersGained", "suscriptores obtenidos": "subscribersGained",
    "likes": "likes", "me gusta": "likes", "comments added": "comments", "comentarios añadidos": "comments",
    "impressions": "impressions", "impresiones": "impressions",
    "impressions click-through rate (%)": "ctr", "tasa de clics de las impresiones (%)": "ctr",
    "estimated revenue (usd)": "estimatedRevenue", "ingresos estimados (usd)": "estimatedRevenue",
}


def _a_numero(v: str) -> float | None:
    v = (v or "").strip().replace(" ", "").replace(" ", "")
    if not v:
        return None
    if ":" in v:  # duración h:mm:ss o m:ss
        partes = [float(x) for x in v.split(":")]
        s = 0.0
        for p in partes:
            s = s * 60 + p
        return s
    v = v.replace("%", "")
    if "," in v and "." in v:
        v = v.replace(",", "")
    elif "," in v:
        v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def _mapa_youtube(canal: str) -> dict:
    with db.conectar() as con:
        return {r["youtube_id"]: r["video_id"] for r in con.execute(
            "SELECT video_id, youtube_id FROM publicaciones WHERE canal=? AND youtube_id IS NOT NULL", (canal,))}


def importar_csv_studio(canal: str, archivo: str) -> int:
    """Importa 'Datos de la tabla.csv' exportado de YouTube Studio > Analytics > Modo avanzado."""
    por_yt = _mapa_youtube(canal)
    por_titulo = {s["titulo"].strip().lower(): s["id"] for s in listar_fichas(canal)}
    hoy = date.today().isoformat()
    n = 0
    with open(archivo, encoding="utf-8-sig") as f, db.conectar() as con:
        for fila in csv.DictReader(f):
            norm = {ALIAS.get(k.strip().lower(), None): v for k, v in fila.items()}
            yt = (norm.get("youtube_id") or "").strip()
            vid = por_yt.get(yt) or por_titulo.get((norm.get("titulo") or "").strip().lower())
            if not vid:
                continue
            for k, v in norm.items():
                if k in (None, "youtube_id", "titulo"):
                    continue
                x = _a_numero(v)
                if x is not None:
                    con.execute("INSERT OR REPLACE INTO metricas VALUES (?,?,?,?,?,?)", (vid, yt, hoy, k, x, "studio_csv"))
                    n += 1
    return n


def actualizar_metricas(canal: str, dias: int = 28) -> int:
    from googleapiclient.discovery import build

    from .publishing import credenciales
    pubs = _mapa_youtube(canal)
    if not pubs:
        print("No hay videos publicados registrados por la API. Alternativa: exportá el CSV de Studio y usá --csv.")
        return 0
    yta = build("youtubeAnalytics", "v2", credentials=credenciales(canal), cache_discovery=False)
    fin = date.today()
    ini = fin - timedelta(days=dias)
    ids = list(pubs)
    n = 0
    for k in range(0, len(ids), 40):
        lote = ids[k:k + 40]
        r = yta.reports().query(ids="channel==MINE", startDate=ini.isoformat(), endDate=fin.isoformat(),
                                metrics=",".join(METRICAS_API), dimensions="video",
                                filters="video==" + ",".join(lote)).execute()
        cols = [c["name"] for c in r.get("columnHeaders", [])]
        with db.conectar() as con:
            for fila in r.get("rows", []):
                d = dict(zip(cols, fila))
                for m in METRICAS_API:
                    if m in d:
                        con.execute("INSERT OR REPLACE INTO metricas VALUES (?,?,?,?,?,?)",
                                    (pubs[d["video"]], d["video"], fin.isoformat(), m, float(d[m]), f"api_{dias}d"))
                        n += 1
    print(f"{n} valores de métricas guardados ({canal}, últimos {dias} días).")
    return n


def _metricas_por_video(canal: str) -> dict:
    out = defaultdict(dict)
    with db.conectar() as con:
        for r in con.execute("SELECT m.* FROM metricas m JOIN videos v ON v.id=m.video_id WHERE v.canal=? ORDER BY m.fecha", (canal,)):
            out[r["video_id"]][r["metrica"]] = r["valor"]  # el último valor gana
    return out


def informe_semanal(canal: str, fin: str | None = None) -> str:
    ch = cargar_canal(canal)
    fin_d = date.fromisoformat(fin) if fin else date.today()
    ini_d = fin_d - timedelta(days=6)
    fichas = {s["id"]: s for s in listar_fichas(canal)}
    met = _metricas_por_video(canal)
    con_datos = {k: v for k, v in met.items() if k in fichas and v.get("views") is not None}
    semana = [s for s in fichas.values() if ini_d.isoformat() <= str(s["fecha"]) <= fin_d.isoformat()]
    lineas = [f"# Informe semanal · {ch.nombre} · {ini_d} a {fin_d}", ""]
    lineas.append(f"Videos planificados en la semana: {len(semana)}. Videos con métricas disponibles (total): {len(con_datos)}.")
    lineas.append("")
    if len(con_datos) < 3:
        lineas += [
            "## 1. Qué funcionó", "Evidencia insuficiente: hay menos de 3 videos con métricas. No se sacan conclusiones.", "",
            "## 2. Qué no funcionó", "Evidencia insuficiente.", "",
            "## 3. Evidencia", "Cargá métricas con `python fabrica.py metricas " + canal + "` (API) o `--csv archivo.csv` (exportación de Studio).", "",
        ]
        grupos = {}
    else:
        def grupo(attr):
            g = defaultdict(list)
            for vid, m in con_datos.items():
                s = fichas[vid]
                clave = s.get(attr) or "?"
                g[clave].append(m)
            return g
        grupos = {a: grupo(a) for a in ("pilar", "tipo_editorial", "serie")}
        med_global = statistics.median(m["views"] for m in con_datos.values())
        ret = [m.get("averageViewPercentage") for m in con_datos.values() if m.get("averageViewPercentage") is not None]
        med_ret = statistics.median(ret) if ret else None
        mejores, peores = [], []
        for attr, g in grupos.items():
            for clave, ms in g.items():
                if len(ms) < 3:
                    continue  # muestra mínima
                v = statistics.median(m["views"] for m in ms)
                r = [m.get("averageViewPercentage") for m in ms if m.get("averageViewPercentage") is not None]
                fila = (attr, clave, len(ms), v, statistics.median(r) if r else None)
                (mejores if v >= med_global * 1.25 else peores if v <= med_global * 0.75 else []).append(fila)
        fmt = lambda f: f"- **{f[0]} = {f[1]}** (n={f[2]}): mediana {f[3]:.0f} vistas" + (f", {f[4]:.0f} % visto" if f[4] else "")
        lineas += ["## 1. Qué funcionó", *(fmt(f) for f in mejores)] if mejores else ["## 1. Qué funcionó", "Ningún grupo con n≥3 supera en 25 % la mediana."]
        lineas += ["", "## 2. Qué no funcionó", *(fmt(f) for f in peores)] if peores else ["", "## 2. Qué no funcionó", "Ningún grupo con n≥3 queda 25 % por debajo de la mediana."]
        lineas += ["", "## 3. Evidencia",
                   f"Mediana de vistas del canal: {med_global:.0f}" + (f"; mediana de % visto: {med_ret:.0f} %" if med_ret else "; % visto no disponible"),
                   "Criterio: solo se comparan grupos con al menos 3 videos; diferencias < 25 % se consideran ruido. "
                   "Videos con menos de 7 días pueden estar subestimados."]
        lineas += ["", "Detalle por video:", "", "| ID | Fecha | Pilar | Tipo | Vistas | % visto | Subs |", "|---|---|---|---|---|---|---|"]
        for vid, m in sorted(con_datos.items()):
            s = fichas[vid]
            lineas.append(f"| {vid} | {s['fecha']} | {s['pilar']} | {s['tipo_editorial']} | {m.get('views', 0):.0f} | "
                          f"{m.get('averageViewPercentage', float('nan')):.0f} | {m.get('subscribersGained', 0):.0f} |")
        lineas.append("")
    lineas += ["## 4. Qué conviene repetir",
               ("Los grupos de la sección 1 (aumentar su frecuencia en el próximo lote, sin repetir temas)." if grupos else
                "Mantener la mezcla planificada hasta tener datos.")]
    lineas += ["", "## 5. Qué conviene dejar de producir",
               ("Los grupos de la sección 2, salvo que tengan valor estratégico (búsqueda, afiliados)." if grupos else
                "Nada por ahora: sin evidencia no se descarta ningún formato.")]
    prox = [s for s in fichas.values() if fin_d.isoformat() < str(s["fecha"]) <= (fin_d + timedelta(days=7)).isoformat()]
    lineas += ["", "## 6. Hipótesis para la semana siguiente"]
    lineas += [f"- {s['id']} ({s['fecha']}): {s.get('hipotesis', '')}" for s in sorted(prox, key=lambda x: str(x["fecha"]))] or ["- (no hay videos planificados)"]
    lineas += ["", "> Las métricas no se mezclan entre canales: cada canal tiene audiencia distinta.",
               "> La fábrica nunca borra ni modifica publicaciones automáticamente."]
    texto = "\n".join(lineas)
    destino = ruta("reports", f"semanal_{canal}_{fin_d}.md")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(texto, encoding="utf-8")
    return texto + f"\n\n(Guardado en {destino})"
