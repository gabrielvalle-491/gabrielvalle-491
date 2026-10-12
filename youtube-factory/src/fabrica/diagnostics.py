"""Diagnóstico del entorno, puesta en marcha inicial e informe de costos."""
from __future__ import annotations

import importlib
import os
import platform
import shutil
import subprocess
import sys
import urllib.request

from . import db
from .config import cargar_canales, cargar_global, ruta

MODELOS = {
    "kokoro-v1.0.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
}
PAQUETES = ["yaml", "numpy", "soundfile", "playwright", "kokoro_onnx", "num2words", "spylls", "jinja2"]
OPCIONALES = ["googleapiclient", "google_auth_oauthlib"]


def _ok(cond: bool, texto: str, ayuda: str = "") -> bool:
    print(("  ✔ " if cond else "  ✘ ") + texto + ("" if cond or not ayuda else f"\n      → {ayuda}"))
    return cond


def diagnostico() -> int:
    g = cargar_global()
    fallos = 0
    print("Sistema:", platform.system(), platform.release(), "| Python", sys.version.split()[0], "| CPU:", os.cpu_count())
    print("\nProgramas:")
    fallos += not _ok(sys.version_info >= (3, 10), "Python 3.10 o superior", "Instalá Python 3.11+ desde python.org")
    for exe in ("ffmpeg", "ffprobe"):
        fallos += not _ok(shutil.which(exe) is not None, exe, "Instalá FFmpeg (ver README, paso 1)")
    if shutil.which("ffmpeg"):
        filtros = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
        for f in ("loudnorm", "sidechaincompress", "ebur128", "silencedetect", "blackdetect"):
            fallos += not _ok(f" {f} " in filtros, f"FFmpeg filtro {f}")
    print("\nPaquetes de Python:")
    for p in PAQUETES:
        try:
            importlib.import_module(p)
            _ok(True, p)
        except ImportError:
            fallos += not _ok(False, p, "Ejecutá: pip install -r requirements.txt")
    for p in OPCIONALES:
        try:
            importlib.import_module(p)
            _ok(True, f"{p} (opcional, para publicar)")
        except ImportError:
            print(f"  · {p} no instalado (opcional: pip install -r requirements-youtube.txt)")
    print("\nNavegador para dibujar escenas:")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            b.close()
        _ok(True, "Chromium (Playwright)")
    except Exception as e:  # noqa: BLE001
        fallos += not _ok(False, f"Chromium (Playwright): {str(e)[:120]}", "Ejecutá: python -m playwright install chromium")
    print("\nModelos y recursos:")
    for nombre in MODELOS:
        p = ruta("models", nombre)
        fallos += not _ok(p.exists() and p.stat().st_size > 1_000_000, f"modelo de voz {nombre}", "Ejecutá: python fabrica.py iniciar")
    for c in cargar_canales().values():
        for fam in set(c.fuentes.values()):
            fallos += not _ok(any(ruta("assets", "fonts", fam).glob("*.woff2")), f"tipografía {fam} ({c.nombre})")
    _ok(ruta("assets", "diccionario", "es.dic").exists(), "diccionario ortográfico español")
    print("\nEspacio y permisos:")
    libre = shutil.disk_usage(ruta()).free / 1e9
    fallos += not _ok(libre > 5, f"espacio libre: {libre:.1f} GB (recomendado > 5 GB para 180 videos)")
    try:
        t = ruta("data", ".prueba_escritura")
        t.parent.mkdir(exist_ok=True)
        t.write_text("ok")
        t.unlink()
        _ok(True, "permiso de escritura en la carpeta del proyecto")
    except OSError:
        fallos += not _ok(False, "permiso de escritura", "Mové la carpeta a Documentos o ejecutá como tu usuario")
    print("\nSeguridad:")
    gi = ruta(".gitignore").read_text(encoding="utf-8") if ruta(".gitignore").exists() else ""
    _ok("secrets/" in gi and ".env" in gi, "credenciales excluidas de Git (.env, secrets/)")
    _ok(not g["publicacion"]["auto_publicar"], "publicación automática DESACTIVADA (se publica solo tras tu revisión)")
    print("\nPresupuesto:")
    print(f"  Servicios pagos usados: ninguno (USD 0). Tope configurado: USD {g['presupuesto']['mensual_usd']}/mes.")
    print("  " + informe_costos(breve=True))
    print("\nResultado:", "TODO LISTO" if not fallos else f"{fallos} problema(s) a resolver (ver flechas →)")
    return 1 if fallos else 0


def _descargar(url: str, destino) -> None:
    tmp = destino.with_suffix(destino.suffix + ".parcial")
    with urllib.request.urlopen(url, timeout=60) as r, open(tmp, "wb") as f:
        total = int(r.headers.get("Content-Length", 0))
        hecho = 0
        while True:
            bloque = r.read(1 << 20)
            if not bloque:
                break
            f.write(bloque)
            hecho += len(bloque)
            if total:
                print(f"\r    {destino.name}: {hecho * 100 // total} %", end="", flush=True)
    print()
    tmp.replace(destino)


def iniciar() -> int:
    print("1/4 Carpetas y base de datos...")
    for d in ("models", "data", "logs", "reports", "secrets/tokens", "output", "paquetes"):
        ruta(d).mkdir(parents=True, exist_ok=True)
    with db.conectar():
        pass
    print("2/4 Modelo de voz Kokoro-82M (Apache-2.0, ~350 MB, una sola vez)...")
    for nombre, url in MODELOS.items():
        p = ruta("models", nombre)
        if p.exists() and p.stat().st_size > 1_000_000:
            print(f"    {nombre}: ya está")
            continue
        _descargar(url, p)
    print("3/4 Música original de cada canal...")
    from .render import musica_canal
    for c in cargar_canales().values():
        print("   ", musica_canal(c).name)
    print("4/4 Registro de fuentes de investigación...")
    from .research import registrar_fuentes_csv
    print(f"    {registrar_fuentes_csv()} fuentes cargadas")
    print("\nListo. Siguiente paso: python fabrica.py diagnostico")
    return 0


def informe_costos(breve: bool = False) -> str:
    g = cargar_global()["presupuesto"]
    vids = [v for v in db.listar_videos() if v.get("segundos_produccion")]
    seg = sum(v["segundos_produccion"] for v in vids)
    kwh = seg / 3600 * g["potencia_pc_w"] / 1000
    usd = kwh * g["costo_kwh_usd"]
    prom = seg / len(vids) if vids else 0
    est_180 = prom * 180 / 3600 * g["potencia_pc_w"] / 1000 * g["costo_kwh_usd"]
    if breve:
        return (f"Electricidad estimada: {len(vids)} videos producidos, {seg/3600:.2f} h de cómputo ≈ USD {usd:.3f}. "
                f"Lote de 180 Shorts ≈ USD {est_180:.2f}.")
    return "\n".join([
        "# Informe de costos",
        "",
        "| Concepto | Costo | Tipo |",
        "|---|---|---|",
        "| Voz (Kokoro local) | USD 0 | medido: sin API |",
        "| Imágenes y animación (Chromium local) | USD 0 | medido: sin API |",
        "| Música y efectos (generados por código) | USD 0 | medido |",
        "| Montaje (FFmpeg) | USD 0 | medido |",
        "| API de YouTube (cuota gratuita) | USD 0 | según documentación oficial |",
        f"| Electricidad ({len(vids)} videos, {seg/3600:.2f} h) | USD {usd:.3f} | estimado: {g['potencia_pc_w']} W × USD {g['costo_kwh_usd']}/kWh |",
        f"| Proyección 180 Shorts | USD {est_180:.2f} | estimado (promedio {prom:.0f} s por video) |",
        "",
        f"Tope mensual configurado: USD {g['mensual_usd']}. Ningún servicio pago está activado.",
    ])
