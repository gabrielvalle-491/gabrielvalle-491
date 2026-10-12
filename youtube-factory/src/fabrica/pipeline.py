"""Ejecución por lotes: concurrencia limitada, reintentos, reanudación y registro de errores."""
from __future__ import annotations

import json
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed

from . import db
from .config import cargar_global
from .specs import buscar_ficha, listar_fichas


def _trabajo(vid: str, forzar: bool) -> dict:
    from .quality import evaluar_y_registrar
    from .render import producir
    g = cargar_global()
    intentos = int(g["concurrencia"]["reintentos"]) + 1
    ultimo = None
    for k in range(intentos):
        try:
            spec = buscar_ficha(vid)
            t = producir(spec, forzar=forzar or k > 0)
            qa = evaluar_y_registrar(spec)
            return {"id": vid, "ok": True, "omitido": t.get("omitido", False), "estado": qa["estado"],
                    "puntaje": qa["puntaje"], "motivos": qa["motivos"][:5], "segundos": t.get("segundos_produccion")}
        except Exception as e:  # noqa: BLE001
            ultimo = f"{type(e).__name__}: {e}"
            db.registrar_evento(vid, "produccion", f"intento {k+1}/{intentos} falló: {ultimo}\n{traceback.format_exc()[-1500:]}", "error")
            time.sleep(1)
    db.upsert_video(vid, estado="error", error=ultimo)
    return {"id": vid, "ok": False, "estado": "error", "error": ultimo}


def producir_lote(ids: list[str] | None = None, canal: str | None = None, desde: str | None = None,
                  hasta: str | None = None, forzar: bool = False, paralelo: int | None = None,
                  formato: str | None = "short", progreso=print) -> list[dict]:
    g = cargar_global()
    if ids is None:
        fichas = listar_fichas(canal)
        ids = [f["id"] for f in fichas
               if (not desde or str(f["fecha"]) >= desde) and (not hasta or str(f["fecha"]) <= hasta)
               and (not formato or f["formato"] == formato) and not f["id"].endswith("TEST")]
    n = paralelo or int(g["concurrencia"]["render_paralelo"])
    resultados = []
    progreso(f"Produciendo {len(ids)} videos con {n} en paralelo...")
    with ProcessPoolExecutor(max_workers=n) as ex:
        futuros = {ex.submit(_trabajo, vid, forzar): vid for vid in ids}
        for k, fut in enumerate(as_completed(futuros), start=1):
            r = fut.result()
            resultados.append(r)
            marca = "✔" if r.get("estado") == "aprobado" else ("•" if r.get("ok") else "✘")
            extra = f"{r.get('puntaje', '')}" if r.get("ok") else r.get("error", "")[:120]
            progreso(f"[{k}/{len(ids)}] {marca} {r['id']} {r.get('estado')} {extra}")
    return sorted(resultados, key=lambda r: r["id"])


def resumen(resultados: list[dict]) -> str:
    est = {}
    for r in resultados:
        est[r.get("estado")] = est.get(r.get("estado"), 0) + 1
    return json.dumps(est, ensure_ascii=False)
