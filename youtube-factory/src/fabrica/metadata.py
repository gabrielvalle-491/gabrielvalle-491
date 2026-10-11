"""Metadatos de publicación (título, descripción con fuentes y divulgaciones, etiquetas) y
paquete de publicación por canal y fecha."""
from __future__ import annotations

import csv
import json
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import db
from .config import cargar_canal, cargar_canales, ruta
from .specs import listar_fichas

PALABRAS_CLICKBAIT = ["increíble", "no vas a creer", "secreto", "nadie te dice", "urgente", "impactante", "100%"]


def puntuar_titulo(t: str, palabras_clave: list[str]) -> dict:
    """Criterios explícitos: claridad (longitud), palabra clave, especificidad (cifra/objeto), sin clickbait."""
    p = 0
    razones = []
    n = len(t)
    if 35 <= n <= 70:
        p += 30; razones.append("longitud legible en móvil")
    elif n <= 100:
        p += 15; razones.append("longitud aceptable")
    tl = t.lower()
    if any(k.lower() in tl for k in palabras_clave):
        p += 30; razones.append("incluye palabra clave")
    if re.search(r"\d", t) or ":" in t:
        p += 15; razones.append("específico (cifra o estructura)")
    if not any(w in tl for w in PALABRAS_CLICKBAIT) and not t.isupper():
        p += 25; razones.append("sin clickbait ni mayúsculas")
    return {"titulo": t, "puntaje": p, "razones": razones}


def descripcion_final(spec: dict) -> str:
    canal = cargar_canal(spec["canal"])
    partes = [spec["descripcion"].strip()]
    nota = canal.datos.get("convenciones", {}).get("nota_separador")
    if nota and any(e["visual"]["plantilla"] in ("formula", "planilla") for e in spec["escenas"]):
        partes.append(nota)
    fuentes = []
    for f in spec.get("fuentes", []):
        if f.get("url"):
            fuentes.append(f"• {f.get('titulo') or f['url']}: {f['url']} (consultado {f.get('fecha_consulta', '')})")
        elif f.get("calculo") and f.get("resultado") is not None:
            fuentes.append(f"• Cálculo propio: {f['respalda']}")
    if fuentes:
        partes.append("Fuentes y cálculos:\n" + "\n".join(fuentes))
    enlaces = canal.datos.get("enlaces_afiliado") or {}
    usados = [k for k in spec.get("afiliados", []) if k in enlaces]
    if usados:
        partes.append("\n".join(f"• {k}: {enlaces[k]}" for k in usados) + "\n" + canal.datos["divulgacion_afiliados"])
    partes.append(canal.datos["descripcion_pie"].strip())
    partes.append(" ".join(spec.get("hashtags", [])[:4]))
    texto = "\n\n".join(p for p in partes if p)
    return texto.replace("<", "‹").replace(">", "›")  # YouTube no admite < > en descripciones


def fecha_publicacion(spec: dict) -> datetime:
    canal = cargar_canal(spec["canal"])
    hora = canal.datos["publicacion"]["hora_largo" if spec["formato"] == "largo" else "hora_short"]
    h, m = (int(x) for x in hora.split(":"))
    local = datetime.fromisoformat(str(spec["fecha"])).replace(hour=h, minute=m, tzinfo=timezone(timedelta(hours=-3)))
    return local


def metadatos(spec: dict) -> dict:
    canal = cargar_canal(spec["canal"])
    kws = spec.get("palabras_clave", [])
    candidatos = [spec["titulo"], *spec["titulos_alternativos"]]
    evaluados = sorted((puntuar_titulo(t, kws) for t in candidatos), key=lambda x: -x["puntaje"])
    pub = fecha_publicacion(spec)
    etiquetas = []
    for k in kws + [h.lstrip("#") for h in spec.get("hashtags", [])]:
        if k not in etiquetas and sum(len(e) + 1 for e in etiquetas) + len(k) < 450:
            etiquetas.append(k)
    return {
        "id": spec["id"], "canal": spec["canal"], "marca": canal.nombre, "formato": spec["formato"],
        "titulo": spec["titulo"], "titulos_alternativos": spec["titulos_alternativos"],
        "criterio_titulo": spec.get("criterio_titulo", ""), "evaluacion_titulos": evaluados,
        "descripcion": descripcion_final(spec), "etiquetas": etiquetas, "hashtags": spec.get("hashtags", []),
        "categoria_id": canal.datos["youtube"]["categoria_id"], "idioma": canal.datos["youtube"]["idioma"],
        "publicar_en_hora_argentina": pub.strftime("%Y-%m-%d %H:%M"),
        "publicar_en_utc": pub.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "comentario_fijado": spec.get("comentario_fijado", ""), "cta": spec.get("cta", ""),
        "declaracion_sintetica": spec.get("declaracion_sintetica", {}),
        "apto_para_ninos": canal.datos["youtube"]["apto_para_ninos"],
        "promocion_pagada": bool(spec.get("promocion_pagada", False)),
        "hipotesis": spec.get("hipotesis", ""), "pilar": spec.get("pilar"), "serie": spec.get("serie"),
        "tipo_editorial": spec.get("tipo_editorial"),
    }


def _texto_publicacion(m: dict) -> str:
    ds = m["declaracion_sintetica"]
    marcar_ia = "SÍ" if ds.get("decision") == "declarar" else ("REVISAR" if ds.get("decision") == "revisar" else "No requerido (verificar)")
    return f"""VIDEO {m['id']} · {m['marca']} · {m['formato'].upper()}
Programar para: {m['publicar_en_hora_argentina']} (hora de Argentina, UTC-3)

TÍTULO (copiar):
{m['titulo']}

DESCRIPCIÓN (copiar):
{m['descripcion']}

ETIQUETAS (copiar, separadas por coma):
{', '.join(m['etiquetas'])}

COMENTARIO PARA FIJAR:
{m['comentario_fijado']}

CASILLAS EN YOUTUBE STUDIO:
- Público: "No, no es contenido para niños"
- Contenido alterado o sintético (IA): {marcar_ia} — motivo: {ds.get('motivo', '')}
- Promoción pagada: {'SÍ' if m['promocion_pagada'] else 'No'}
- Subtítulos: el video ya los trae incrustados; opcionalmente subí el archivo .srt (Español latinoamericano)

Títulos alternativos para pruebas futuras:
- """ + "\n- ".join(m["titulos_alternativos"]) + "\n"


def exportar(canal: str | None = None, desde: str | None = None, hasta: str | None = None, incluir_revision: bool = False) -> dict:
    canales = [canal] if canal else list(cargar_canales())
    resumen = {}
    for c in canales:
        ch = cargar_canal(c)
        base = ruta("paquetes", c)
        base.mkdir(parents=True, exist_ok=True)
        estados = {v["id"]: v for v in db.listar_videos(c)}
        filas, pendientes = [], []
        for spec in listar_fichas(c):
            if spec["id"].endswith("TEST"):
                continue
            f = str(spec["fecha"])
            if (desde and f < desde) or (hasta and f > hasta):
                continue
            v = estados.get(spec["id"], {})
            estado = v.get("estado", "sin_producir")
            video = ch.dir_salida("videos") / f"{spec['id']}.mp4"
            if estado != "aprobado" and not (incluir_revision and estado == "revision"):
                pendientes.append({"id": spec["id"], "fecha": f, "estado": estado,
                                   "motivo": (json.loads(v["qa_detalle"])[:3] if v.get("qa_detalle") else v.get("error") or "no producido")})
                continue
            m = metadatos(spec)
            carpeta = base / f"{f}_{spec['id']}"
            carpeta.mkdir(parents=True, exist_ok=True)
            shutil.copy2(video, carpeta / f"{spec['id']}.mp4")
            for ext, sub in (("srt", "subtitles"), ("vtt", "subtitles"), ("png", "thumbnails")):
                src = ch.dir_salida(sub) / f"{spec['id']}.{ext}"
                if src.exists():
                    shutil.copy2(src, carpeta / (f"portada.png" if ext == "png" else f"{spec['id']}.{ext}"))
            (carpeta / "PUBLICAR.txt").write_text(_texto_publicacion(m), encoding="utf-8")
            (carpeta / "metadatos.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
            filas.append({"fecha_hora_ar": m["publicar_en_hora_argentina"], "id": spec["id"], "formato": spec["formato"],
                          "titulo": m["titulo"], "carpeta": carpeta.name, "qa": v.get("qa_puntaje"),
                          "marcar_ia": m["declaracion_sintetica"].get("decision", ""), "estado": estado})
        filas.sort(key=lambda r: r["fecha_hora_ar"])
        with open(base / "PROGRAMACION.csv", "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=["fecha_hora_ar", "id", "formato", "titulo", "carpeta", "qa", "marcar_ia", "estado"])
            w.writeheader()
            w.writerows(filas)
        with open(base / "PENDIENTES.csv", "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=["id", "fecha", "estado", "motivo"])
            w.writeheader()
            for p in pendientes:
                w.writerow({**p, "motivo": "; ".join(p["motivo"]) if isinstance(p["motivo"], list) else p["motivo"]})
        resumen[c] = {"listos": len(filas), "pendientes": len(pendientes), "carpeta": str(base)}
        print(f"{c}: {len(filas)} listos para programar, {len(pendientes)} pendientes → {base}")
    return resumen
