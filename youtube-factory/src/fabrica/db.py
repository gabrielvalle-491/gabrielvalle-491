"""Base de datos SQLite: estados de trabajos, eventos, ideas, fuentes, métricas y publicaciones."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .config import ruta

ESQUEMA = """
CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY,
    canal TEXT NOT NULL,
    formato TEXT NOT NULL,
    fecha TEXT,
    titulo TEXT,
    estado TEXT NOT NULL DEFAULT 'planificado',
    spec_hash TEXT,
    intentos INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    duracion_s REAL,
    qa_puntaje REAL,
    qa_detalle TEXT,
    costo_usd REAL DEFAULT 0,
    segundos_produccion REAL,
    actualizado TEXT
);
CREATE TABLE IF NOT EXISTS eventos (
    n INTEGER PRIMARY KEY AUTOINCREMENT,
    momento TEXT NOT NULL,
    video_id TEXT,
    etapa TEXT,
    nivel TEXT,
    mensaje TEXT
);
CREATE TABLE IF NOT EXISTS ideas (
    id TEXT PRIMARY KEY,
    canal TEXT NOT NULL,
    titulo TEXT NOT NULL,
    pilar TEXT,
    puntaje REAL,
    detalle TEXT,
    fuente TEXT,
    estado TEXT NOT NULL DEFAULT 'en_cola',
    creado TEXT
);
CREATE TABLE IF NOT EXISTS fuentes (
    url TEXT PRIMARY KEY,
    fecha_consulta TEXT,
    tema TEXT,
    dato TEXT,
    limitaciones TEXT
);
CREATE TABLE IF NOT EXISTS metricas (
    video_id TEXT NOT NULL,
    youtube_id TEXT,
    fecha TEXT NOT NULL,
    metrica TEXT NOT NULL,
    valor REAL,
    origen TEXT,
    PRIMARY KEY (video_id, fecha, metrica, origen)
);
CREATE TABLE IF NOT EXISTS publicaciones (
    video_id TEXT PRIMARY KEY,
    canal TEXT NOT NULL,
    canal_youtube_id TEXT,
    youtube_id TEXT,
    publicar_en TEXT,
    estado TEXT,
    respuesta TEXT,
    actualizado TEXT
);
"""

ESTADOS = (
    "planificado", "guion_ok", "voz_ok", "fotogramas_ok", "render_ok",
    "aprobado", "revision", "error", "publicado", "programado",
)


def ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ruta_db() -> Path:
    p = ruta("data", "factory.db")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


@contextmanager
def conectar(path: Path | None = None):
    con = sqlite3.connect(path or ruta_db(), timeout=30)
    con.row_factory = sqlite3.Row
    con.executescript(ESQUEMA)
    try:
        yield con
        con.commit()
    finally:
        con.close()


def registrar_evento(video_id: str | None, etapa: str, mensaje: str, nivel: str = "info") -> None:
    with conectar() as con:
        con.execute(
            "INSERT INTO eventos (momento, video_id, etapa, nivel, mensaje) VALUES (?,?,?,?,?)",
            (ahora(), video_id, etapa, nivel, mensaje[:4000]),
        )


def upsert_video(vid: str, **campos) -> None:
    campos["actualizado"] = ahora()
    with conectar() as con:
        existe = con.execute("SELECT 1 FROM videos WHERE id=?", (vid,)).fetchone()
        if existe:
            sets = ", ".join(f"{k}=?" for k in campos)
            con.execute(f"UPDATE videos SET {sets} WHERE id=?", (*campos.values(), vid))
        else:
            campos.setdefault("estado", "planificado")
            cols = ", ".join(["id", *campos])
            qs = ", ".join("?" * (len(campos) + 1))
            con.execute(f"INSERT INTO videos ({cols}) VALUES ({qs})", (vid, *campos.values()))


def obtener_video(vid: str) -> dict | None:
    with conectar() as con:
        fila = con.execute("SELECT * FROM videos WHERE id=?", (vid,)).fetchone()
        return dict(fila) if fila else None


def listar_videos(canal: str | None = None, estado: str | None = None) -> list[dict]:
    q, args = "SELECT * FROM videos WHERE 1=1", []
    if canal:
        q += " AND canal=?"
        args.append(canal)
    if estado:
        q += " AND estado=?"
        args.append(estado)
    q += " ORDER BY fecha, id"
    with conectar() as con:
        return [dict(r) for r in con.execute(q, args).fetchall()]


def guardar_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)
