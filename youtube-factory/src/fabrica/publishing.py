"""Publicación con la API oficial de YouTube (opcional). Dos perfiles independientes, uno por canal.

Seguridad:
- OAuth con el flujo oficial (se abre tu navegador). Nunca se piden contraseñas ni códigos en el chat.
- Credenciales en secrets/ (excluido de Git). Un token por canal.
- Antes de subir se verifica que el token corresponde al canal configurado (evita publicar en el canal equivocado).
- Por defecto SIMULA. Solo sube con --confirmar y AUTO_PUBLICAR=1 o publicacion.auto_publicar: true.
- Nunca se marca "programado" sin confirmación de la API.

Limitaciones oficiales a tener en cuenta (ver research/politicas_y_apis.md):
- Proyectos de API no verificados (creados después del 28-jul-2020): los videos subidos quedan PRIVADOS
  hasta pasar una auditoría de Google. En ese caso la fábrica sube en privado y tú programas en Studio.
- La cuota diaria es limitada: la fábrica cuenta unidades y respeta un límite diario de subidas.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime, timezone
from pathlib import Path

from . import db
from .config import cargar_canal, cargar_global, ruta
from .metadata import metadatos
from .specs import listar_fichas

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
# Agregar videos a la lista del curso necesita un permiso más amplio: solo se pide si lo activás
# (publicacion.gestionar_listas: true en config/global.yaml). Si no, la lista se arma a mano en Studio.
SCOPE_LISTAS = "https://www.googleapis.com/auth/youtube.force-ssl"


def scopes() -> list[str]:
    return SCOPES + ([SCOPE_LISTAS] if cargar_global()["publicacion"].get("gestionar_listas") else [])
# Costos de cuota (unidades). Verificados en la documentación al 2026-10-11; confirma en Google Cloud Console.
COSTO = {"playlistItems.insert": 50, "videos.insert": 100, "channels.list": 1, "videos.list": 1, "thumbnails.set": 50, "captions.insert": 400}


class ErrorPublicacion(RuntimeError):
    pass


def _token_path(canal: str) -> Path:
    d = Path(os.environ.get("YOUTUBE_TOKEN_DIR", ruta("secrets", "tokens")))
    if not d.is_absolute():
        d = ruta(str(d))
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{canal}.json"


def _client_secret() -> Path:
    p = Path(os.environ.get("YOUTUBE_CLIENT_SECRET_FILE", "secrets/client_secret.json"))
    p = p if p.is_absolute() else ruta(str(p))
    if not p.exists():
        raise ErrorPublicacion(
            f"No encuentro el archivo de cliente OAuth en {p}. Seguí la guía docs/AUTORIZAR_YOUTUBE.md "
            "(crear proyecto en Google Cloud, habilitar YouTube Data API v3, crear credencial 'App de escritorio').")
    return p


def credenciales(canal: str, interactivo: bool = False):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    tp = _token_path(canal)
    creds = Credentials.from_authorized_user_file(str(tp), scopes()) if tp.exists() else None
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:  # noqa: BLE001 — token revocado o caducado (modo Testing: 7 días)
            creds = None
    if not creds or not creds.valid:
        if not interactivo:
            raise ErrorPublicacion(f"El canal {canal} no está autorizado o el permiso caducó. Ejecutá: python fabrica.py autorizar {canal}")
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(str(_client_secret()), scopes())
        print("Se abrirá tu navegador. Elegí la cuenta/canal correcto y aceptá los permisos.")
        creds = flow.run_local_server(port=0, prompt="consent")
    tp.write_text(creds.to_json(), encoding="utf-8")
    try:
        os.chmod(tp, 0o600)
    except OSError:
        pass
    return creds


def servicio(canal: str, interactivo: bool = False):
    from googleapiclient.discovery import build
    return build("youtube", "v3", credentials=credenciales(canal, interactivo), cache_discovery=False)


def _registrar_cuota(unidades: int, operacion: str) -> int:
    hoy = date.today().isoformat()
    with db.conectar() as con:
        con.execute("CREATE TABLE IF NOT EXISTS cuota (dia TEXT, operacion TEXT, unidades INTEGER)")
        con.execute("INSERT INTO cuota VALUES (?,?,?)", (hoy, operacion, unidades))
        return con.execute("SELECT COALESCE(SUM(unidades),0) FROM cuota WHERE dia=?", (hoy,)).fetchone()[0]


def canal_autorizado(canal: str) -> dict:
    yt = servicio(canal)
    r = yt.channels().list(part="id,snippet", mine=True).execute()
    _registrar_cuota(COSTO["channels.list"], "channels.list")
    items = r.get("items", [])
    if len(items) != 1:
        raise ErrorPublicacion(f"La autorización devolvió {len(items)} canales; se esperaba exactamente 1.")
    return {"id": items[0]["id"], "titulo": items[0]["snippet"]["title"]}


def autorizar(canal: str) -> dict:
    cfg = cargar_canal(canal)
    servicio(canal, interactivo=True)
    info = canal_autorizado(canal)
    esperado = cfg.datos["youtube"].get("channel_id")
    print(f"Autorizado: «{info['titulo']}» (id {info['id']})")
    if esperado and esperado != info["id"]:
        _token_path(canal).unlink(missing_ok=True)
        raise ErrorPublicacion(f"Ese canal NO es el configurado para {canal} ({esperado}). Se borró el token. Repetí eligiendo el canal correcto.")
    if not esperado:
        p = ruta("config", f"{canal}.yaml")
        texto = p.read_text(encoding="utf-8").replace('channel_id: ""', f'channel_id: "{info["id"]}"', 1)
        p.write_text(texto, encoding="utf-8")
        print(f"Guardé el id del canal en config/{canal}.yaml. A partir de ahora solo se publicará en «{info['titulo']}».")
    return info


def _verificar_destino(canal: str) -> dict:
    cfg = cargar_canal(canal)
    esperado = cfg.datos["youtube"].get("channel_id")
    if not esperado:
        raise ErrorPublicacion(f"Falta youtube.channel_id en config/{canal}.yaml. Ejecutá: python fabrica.py autorizar {canal}")
    info = canal_autorizado(canal)
    if info["id"] != esperado:
        raise ErrorPublicacion(f"BLOQUEADO: el token de {canal} corresponde a «{info['titulo']}» ({info['id']}), no a {esperado}.")
    return info


def subir(spec: dict, simular: bool = True) -> dict:
    canal = spec["canal"]
    ch = cargar_canal(canal)
    m = metadatos(spec)
    video = ch.dir_salida("videos") / f"{spec['id']}.mp4"
    publish_at = datetime.fromisoformat(m["publicar_en_utc"].replace("Z", "+00:00"))
    if publish_at <= datetime.now(timezone.utc):
        raise ErrorPublicacion(f"{spec['id']}: la fecha {m['publicar_en_hora_argentina']} ya pasó; actualizá el calendario.")
    cuerpo = {
        "snippet": {"title": m["titulo"], "description": m["descripcion"], "tags": m["etiquetas"],
                    "categoryId": m["categoria_id"], "defaultLanguage": m["idioma"], "defaultAudioLanguage": m["idioma"]},
        "status": {"privacyStatus": "private", "publishAt": m["publicar_en_utc"],
                   "selfDeclaredMadeForKids": bool(m["apto_para_ninos"]),
                   "containsSyntheticMedia": m["declaracion_sintetica"].get("decision") == "declarar"},
    }
    from .cursos import MARCA_ENLACE
    if MARCA_ENLACE in m["descripcion"]:
        raise ErrorPublicacion(f"{spec['id']}: falta el enlace del material de práctica (cursos/{canal}.yaml → enlace_material).")
    if simular:
        return {"id": spec["id"], "simulado": True, "titulo": m["titulo"], "publishAt": m["publicar_en_utc"], "archivo": str(video)}
    from googleapiclient.http import MediaFileUpload
    _verificar_destino(canal)
    yt = servicio(canal)
    req = yt.videos().insert(part="snippet,status", body=cuerpo,
                             media_body=MediaFileUpload(str(video), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    _registrar_cuota(COSTO["videos.insert"], "videos.insert")
    yid = resp.get("id")
    st = resp.get("status", {})
    if not yid:
        raise ErrorPublicacion(f"La API no devolvió id de video: {json.dumps(resp)[:300]}")
    programado = st.get("publishAt") is not None and st.get("privacyStatus") == "private"
    if spec["formato"] == "largo":
        portada = ch.dir_salida("thumbnails") / f"{spec['id']}.jpg"
        if portada.exists():
            from googleapiclient.http import MediaFileUpload as MFU
            yt.thumbnails().set(videoId=yid, media_body=MFU(str(portada), mimetype="image/jpeg")).execute()
            _registrar_cuota(COSTO["thumbnails.set"], "thumbnails.set")
    lista = _lista_curso(spec)
    if lista:
        try:
            yt.playlistItems().insert(part="snippet", body={"snippet": {"playlistId": lista, "position": max(0, _n_leccion(spec) - 1),
                                                                        "resourceId": {"kind": "youtube#video", "videoId": yid}}}).execute()
            _registrar_cuota(COSTO["playlistItems.insert"], "playlistItems.insert")
        except Exception as e:  # noqa: BLE001 — la subida ya se hizo; solo falta la lista (se agrega a mano en Studio)
            db.registrar_evento(spec["id"], "publicacion", f"no se pudo agregar a la lista del curso: {e}", "aviso")
    estado = "programado" if programado else "subido_privado"
    with db.conectar() as con:
        con.execute("INSERT OR REPLACE INTO publicaciones VALUES (?,?,?,?,?,?,?,?)",
                    (spec["id"], canal, ch.datos["youtube"]["channel_id"], yid, st.get("publishAt"), estado,
                     json.dumps(resp, ensure_ascii=False)[:4000], db.ahora()))
    db.upsert_video(spec["id"], estado=estado)
    nota = "" if programado else " (la API no confirmó la programación: revisá en Studio; los proyectos no verificados quedan en privado)"
    db.registrar_evento(spec["id"], "publicacion", f"{estado} youtube_id={yid}{nota}")
    return {"id": spec["id"], "youtube_id": yid, "estado": estado, "publishAt": st.get("publishAt"), "nota": nota}


def _n_leccion(spec: dict) -> int:
    from .cursos import leccion_de
    return int((leccion_de(spec) or {}).get("n", 1))


def _lista_curso(spec: dict) -> str | None:
    """Id de la lista de reproducción del curso, solo si el usuario activó la gestión de listas
    (requiere el permiso adicional youtube.force-ssl, ver docs/AUTORIZAR_YOUTUBE.md)."""
    if not spec.get("curso") or not cargar_global()["publicacion"].get("gestionar_listas"):
        return None
    from .cursos import temario
    return (temario(spec["canal"]) or {}).get("lista_youtube_id") or None


def publicar_lote(canal: str, desde: str | None, hasta: str | None, simular: bool = True, limite: int | None = None) -> list[dict]:
    g = cargar_global()
    permitido = g["publicacion"].get("auto_publicar") or os.environ.get("AUTO_PUBLICAR") == "1"
    if not simular and not permitido:
        raise ErrorPublicacion("La publicación automática está desactivada. Activala en config/global.yaml "
                               "(publicacion.auto_publicar: true) o con AUTO_PUBLICAR=1 en .env, después de revisar el lote.")
    limite = limite or int(g["publicacion"]["limite_diario_subidas"])
    ya = {r["video_id"] for r in _publicaciones(canal)}
    aprobados = {v["id"] for v in db.listar_videos(canal, "aprobado")}
    out = []
    for spec in listar_fichas(canal):
        f = str(spec["fecha"])
        if spec["id"] in ya or spec["id"] not in aprobados or (desde and f < desde) or (hasta and f > hasta):
            continue
        if len(out) >= limite:
            print(f"Límite diario de {limite} subidas alcanzado. Continuá mañana.")
            break
        try:
            r = subir(spec, simular=simular)
        except ErrorPublicacion as e:
            r = {"id": spec["id"], "error": str(e)}
        out.append(r)
        print(("[SIMULACIÓN] " if simular else "") + json.dumps(r, ensure_ascii=False))
    if simular:
        print("\nNada se subió. Para subir de verdad: python fabrica.py publicar", canal, "--confirmar")
    return out


def _publicaciones(canal: str) -> list[dict]:
    with db.conectar() as con:
        return [dict(r) for r in con.execute("SELECT * FROM publicaciones WHERE canal=?", (canal,)).fetchall()]
