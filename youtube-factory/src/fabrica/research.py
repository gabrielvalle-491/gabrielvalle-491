"""Investigación editorial: banco de ideas, puntaje explicable, deduplicación y registro de fuentes.

Honestidad metodológica: sin acceso a datos privados ni a una API de tendencias, los puntajes de
demanda por idea son ESTIMACIONES basadas en la evidencia por pilar (research/investigacion_nichos.md).
Si configurás YOUTUBE_API_KEY, el comando 'investigar' agrega señales públicas reales (resultados y
vistas de búsquedas en YouTube) y las registra con fecha.
"""
from __future__ import annotations

import csv
import json
import math
import os
import re
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

from . import db
from .config import cargar_canales, ruta

# Evidencia agregada por pilar (1-5). Fuente: research/investigacion_nichos.md (matriz y hallazgos).
PILARES = {
    "canal_a": {
        "prompts":        {"demanda": 5, "competencia": 3, "comercial": 4, "conf": "media"},
        "ia_sin_humo":    {"demanda": 4, "competencia": 4, "comercial": 3, "conf": "media"},
        "negocio":        {"demanda": 4, "competencia": 4, "comercial": 5, "conf": "media"},
        "automatizacion": {"demanda": 4, "competencia": 4, "comercial": 5, "conf": "media"},
        "conceptos":      {"demanda": 4, "competencia": 3, "comercial": 3, "conf": "baja"},
        "seguridad":      {"demanda": 3, "competencia": 4, "comercial": 3, "conf": "baja"},
        "herramientas":   {"demanda": 5, "competencia": 2, "comercial": 5, "conf": "media"},
        "puente_excel":   {"demanda": 4, "competencia": 4, "comercial": 4, "conf": "media"},
        "productividad":  {"demanda": 4, "competencia": 3, "comercial": 3, "conf": "baja"},
        "empleo":         {"demanda": 4, "competencia": 3, "comercial": 3, "conf": "media"},
        "historia":       {"demanda": 3, "competencia": 4, "comercial": 1, "conf": "baja"},
    },
    "canal_b": {
        "formulas":        {"demanda": 5, "competencia": 3, "comercial": 3, "conf": "media"},
        "dinero":          {"demanda": 5, "competencia": 3, "comercial": 4, "conf": "media"},
        "errores":         {"demanda": 4, "competencia": 4, "comercial": 3, "conf": "baja"},
        "trabajo":         {"demanda": 4, "competencia": 3, "comercial": 4, "conf": "media"},
        "excel_vs_sheets": {"demanda": 3, "competencia": 4, "comercial": 3, "conf": "baja"},
        "quiz":            {"demanda": 3, "competencia": 4, "comercial": 2, "conf": "baja"},
        "historia":        {"demanda": 2, "competencia": 5, "comercial": 1, "conf": "baja"},
    },
}
FACILIDAD_PLANTILLA = {"planilla": 5, "formula": 5, "calculo": 5, "barras": 5, "linea": 5, "donut": 5, "prompt": 5,
                       "codigo": 4, "versus": 4, "pasos": 4, "lista": 4, "timeline": 4, "pregunta": 4, "mito": 4,
                       "dato": 3, "texto": 3, "hook": 4, "cierre": 4}
PESOS = {"demanda": 0.30, "oportunidad": 0.20, "competencia": 0.15, "comercial": 0.15, "demostracion": 0.15, "costo": 0.05}
CAMPOS_IDEA = ["n", "pilar", "serie", "tipo", "tema", "angulo", "plantillas", "mercado"]


def normalizar(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", t)


STOP = set("de la el en y a los las un una para con por que se del al lo como mas o es tu te su sus sin vs".split())


def tokens(t: str) -> list[str]:
    return [w for w in normalizar(t).split() if w not in STOP and len(w) > 2]


def similitud(a: str, b: str) -> float:
    """Coseno de bolsa de palabras + bigramas de caracteres (robusto a variaciones menores)."""
    def vec(t):
        tk = tokens(t)
        c = Counter(tk)
        s = " ".join(tk)
        c.update(s[i:i + 4] for i in range(max(0, len(s) - 3)))
        return c
    va, vb = vec(a), vec(b)
    num = sum(va[k] * vb[k] for k in va.keys() & vb.keys())
    den = math.sqrt(sum(v * v for v in va.values())) * math.sqrt(sum(v * v for v in vb.values()))
    return num / den if den else 0.0


def leer_banco(canal: str) -> list[dict]:
    p = ruta("research", "ideas", f"{canal}.txt")
    ideas = []
    for linea in p.read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.startswith("#"):
            continue
        partes = [x.strip() for x in linea.split("|")]
        d = dict(zip(CAMPOS_IDEA, partes))
        d["n"] = int(d["n"])
        d["plantillas"] = d["plantillas"].split(",")
        d["canal"] = canal
        ideas.append(d)
    return ideas


def puntuar(idea: dict, banco: list[dict], senales: dict | None = None) -> dict:
    """Puntaje 0-100 con desglose. 'senales' puede traer datos públicos reales de la API."""
    pil = PILARES[idea["canal"]].get(idea["pilar"], {"demanda": 3, "competencia": 3, "comercial": 3, "conf": "baja"})
    otras = [i for i in banco if i is not idea]
    max_sim = max((similitud(idea["tema"] + " " + idea["angulo"], o["tema"] + " " + o["angulo"]) for o in otras), default=0)
    oportunidad = 5 - 3 * max_sim  # un ángulo muy parecido a otro reduce la oportunidad
    if idea["tipo"] in ("experimento", "contraintuitivo", "caso_practico"):
        oportunidad += 0.5
    demostracion = sum(FACILIDAD_PLANTILLA.get(p, 3) for p in idea["plantillas"]) / len(idea["plantillas"])
    demanda = pil["demanda"]
    fuente_demanda = "estimada por pilar (investigacion_nichos.md)"
    if senales and senales.get("vistas_mediana"):
        # señal pública real: mediana de vistas de los primeros resultados de búsqueda
        demanda = min(5, max(1, round(math.log10(max(10, senales["vistas_mediana"])) - 1, 1)))
        fuente_demanda = f"API YouTube {senales.get('fecha')}: mediana {senales['vistas_mediana']} vistas"
    comp = {"demanda": demanda, "oportunidad": min(5, oportunidad), "competencia": pil["competencia"],
            "comercial": pil["comercial"], "demostracion": demostracion, "costo": 5}
    total = sum(comp[k] * PESOS[k] for k in PESOS) / 5 * 100
    if idea.get("mercado") == "ar":
        total -= 4  # menor alcance internacional y CPM (ver investigación §7)
    return {"puntaje": round(total, 1), "componentes": {k: round(v, 2) for k, v in comp.items()},
            "similitud_maxima": round(max_sim, 2), "confianza": pil["conf"], "fuente_demanda": fuente_demanda}


def actualizar_cola(canal: str) -> list[dict]:
    banco = leer_banco(canal)
    hoy = date.today().isoformat()
    salida = []
    with db.conectar() as con:
        for idea in banco:
            p = puntuar(idea, banco, _senales_guardadas(canal, idea))
            iid = f"{canal}-idea-{idea['n']:03d}"
            existente = con.execute("SELECT estado FROM ideas WHERE id=?", (iid,)).fetchone()
            estado = existente["estado"] if existente else "en_cola"
            con.execute(
                "INSERT OR REPLACE INTO ideas (id, canal, titulo, pilar, puntaje, detalle, fuente, estado, creado) VALUES (?,?,?,?,?,?,?,?,?)",
                (iid, canal, idea["tema"], idea["pilar"], p["puntaje"], json.dumps({**idea, **p}, ensure_ascii=False),
                 "banco editorial", estado, hoy))
            salida.append({**idea, **p, "id_idea": iid, "estado": estado})
    salida.sort(key=lambda x: -x["puntaje"])
    out = ruta("research", f"cola_ideas_{canal}.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_idea", "puntaje", "confianza", "pilar", "serie", "tipo", "tema", "angulo", "demanda", "oportunidad",
                    "competencia", "comercial", "demostracion", "similitud_maxima", "fuente_demanda", "estado"])
        for s in salida:
            c = s["componentes"]
            w.writerow([s["id_idea"], s["puntaje"], s["confianza"], s["pilar"], s["serie"], s["tipo"], s["tema"], s["angulo"],
                        c["demanda"], c["oportunidad"], c["competencia"], c["comercial"], c["demostracion"],
                        s["similitud_maxima"], s["fuente_demanda"], s["estado"]])
    return salida


def _senales_guardadas(canal: str, idea: dict) -> dict | None:
    p = ruta("research", "senales", f"{canal}.json")
    if not p.exists():
        return None
    datos = json.loads(p.read_text(encoding="utf-8"))
    return datos.get(str(idea["n"]))


def investigar_api(canal: str, maximo: int = 20) -> dict:
    """Señales públicas reales vía YouTube Data API (search.list = 100 unidades por consulta).
    Requiere YOUTUBE_API_KEY. Sin clave, registra la limitación y no inventa nada."""
    clave = os.environ.get("YOUTUBE_API_KEY")
    registro = ruta("research", "senales")
    registro.mkdir(parents=True, exist_ok=True)
    if not clave:
        msg = "Sin YOUTUBE_API_KEY: no se consultaron señales públicas. Puntajes de demanda = estimación por pilar."
        db.registrar_evento(None, "investigar", msg, "aviso")
        return {"estado": "limitado", "mensaje": msg}
    import statistics

    import requests
    banco = leer_banco(canal)
    p = registro / f"{canal}.json"
    datos = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    consultadas = 0
    for idea in banco:
        if str(idea["n"]) in datos or consultadas >= maximo:
            continue
        q = idea["tema"]
        r = requests.get("https://www.googleapis.com/youtube/v3/search", timeout=30, params={
            "part": "id", "q": q, "type": "video", "relevanceLanguage": "es", "maxResults": 10, "key": clave,
            "publishedAfter": f"{date.today().year - 1}-01-01T00:00:00Z"})
        r.raise_for_status()
        ids = [it["id"]["videoId"] for it in r.json().get("items", [])]
        vistas = []
        if ids:
            r2 = requests.get("https://www.googleapis.com/youtube/v3/videos", timeout=30,
                              params={"part": "statistics", "id": ",".join(ids), "key": clave})
            r2.raise_for_status()
            vistas = [int(v["statistics"].get("viewCount", 0)) for v in r2.json().get("items", [])]
        datos[str(idea["n"])] = {"consulta": q, "fecha": date.today().isoformat(), "resultados": len(ids),
                                 "vistas_mediana": int(statistics.median(vistas)) if vistas else 0}
        consultadas += 1
    p.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"estado": "ok", "consultadas": consultadas, "unidades_estimadas": consultadas * 101}


def importar_ideas_csv(canal: str, archivo: Path) -> int:
    """Agrega ideas nuevas (p. ej. preguntas repetidas en comentarios) al banco, evitando duplicados."""
    banco = leer_banco(canal)
    n = max(i["n"] for i in banco)
    nuevas = 0
    lineas = []
    with open(archivo, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            texto = fila["tema"] + " " + fila.get("angulo", "")
            if any(similitud(texto, b["tema"] + " " + b["angulo"]) > 0.6 for b in banco):
                continue
            n += 1
            nuevas += 1
            lineas.append("|".join([str(n), fila.get("pilar", "general"), fila.get("serie", "General"), fila.get("tipo", "tutorial"),
                                    fila["tema"], fila.get("angulo", ""), fila.get("plantillas", "hook,texto,cierre"), fila.get("mercado", "latam")]))
            banco.append({"tema": fila["tema"], "angulo": fila.get("angulo", "")})
    if lineas:
        with open(ruta("research", "ideas", f"{canal}.txt"), "a", encoding="utf-8") as f:
            f.write("\n".join(lineas) + "\n")
    return nuevas


def registrar_fuentes_csv() -> int:
    """Carga los CSV de fuentes de investigación en la base de datos (registro de fuentes)."""
    n = 0
    with db.conectar() as con:
        for nombre in ("fuentes_investigacion.csv", "fuentes_politicas.csv"):
            p = ruta("research", nombre)
            if not p.exists():
                continue
            with open(p, encoding="utf-8") as f:
                for fila in csv.DictReader(f):
                    con.execute("INSERT OR REPLACE INTO fuentes (url, fecha_consulta, tema, dato, limitaciones) VALUES (?,?,?,?,?)",
                                (fila.get("url"), fila.get("fecha_consulta"), fila.get("tema"), fila.get("dato_observado"), fila.get("limitaciones")))
                    n += 1
    return n


def canales_disponibles() -> list[str]:
    return list(cargar_canales())
