"""Render de fotogramas con Chromium (Playwright): solo se capturan los instantes que cambian."""
from __future__ import annotations

import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

from .templates import html_escena, md


class Navegador:
    def __init__(self, horizontal: bool = False):
        self.horizontal = horizontal
        self.size = {"width": 1920, "height": 1080} if horizontal else {"width": 1080, "height": 1920}

    def __enter__(self):
        self._pw = sync_playwright().start()
        self._b = self._pw.chromium.launch(args=["--disable-gpu", "--font-render-hinting=none"])
        self.page = self._b.new_page(viewport=self.size, device_scale_factor=1)
        self.cdp = self.page.context.new_cdp_session(self.page)
        return self

    def __exit__(self, *a):
        self._b.close()
        self._pw.stop()

    def cargar(self, html: str) -> dict:
        self.page.set_content(html, wait_until="load")
        self.page.evaluate("document.fonts.ready")
        return self.page.evaluate("setup()")

    def estado(self, t: float, beats: list[float], cap_html: str, cap_t: float) -> None:
        self.page.evaluate("([t,b,c,ct])=>setState(t,b,c,ct)", [t, beats, cap_html, cap_t])

    def captura(self, destino: Path) -> None:
        r = self.cdp.send("Page.captureScreenshot", {"format": "png", "optimizeForSpeed": True})
        destino.write_bytes(base64.b64decode(r["data"]))


def analizar(spec: dict, canal, cabecera: dict, horizontal: bool = False) -> list[dict]:
    """Carga cada escena y devuelve beats y desbordes de texto (para QA y para la línea de tiempo)."""
    out = []
    with Navegador(horizontal) as nav:
        for esc in spec["escenas"]:
            info = nav.cargar(html_escena(canal, esc["visual"], cabecera, horizontal))
            beats = {int(k): float(v) for k, v in info["beats"].items()}
            out.append({"n": (max(beats) + 1) if beats else 1, "dur": beats, "overflow": info["overflow"]})
    return out


def render(lt, spec: dict, canal, cabecera: dict, info_escenas: list[dict], carpeta: Path,
           fps: int = 30, horizontal: bool = False) -> Path:
    """Genera PNGs + lista concat de FFmpeg con duraciones exactas. Devuelve la ruta de la lista."""
    carpeta.mkdir(parents=True, exist_ok=True)
    for f in carpeta.glob("*.png"):
        f.unlink()
    total_frames = int(round(lt.duracion * fps))
    entradas = []  # (frame_index, png)
    n = 0
    with Navegador(horizontal) as nav:
        for esc, info in zip(lt.escenas, info_escenas):
            nav.cargar(html_escena(canal, esc.visual, cabecera, horizontal))
            f0, f1 = int(round(esc.inicio * fps)), int(round(esc.fin * fps))
            muestras = {f0}
            for b, ini_rel in enumerate(esc.beats):
                dur = info["dur"].get(b, 0.45)
                a = int(round((esc.inicio + ini_rel) * fps))
                muestras.update(range(a, a + int(dur * fps) + 2))
            for s in lt.subtitulos:
                a = int(round(s.inicio * fps))
                muestras.update(range(a, a + 5))
                muestras.add(int(round(s.fin * fps)))
            muestras = sorted(m for m in muestras if f0 <= m < min(f1, total_frames))
            for m in muestras:
                t_abs = m / fps
                sub = next((s for s in reversed(lt.subtitulos) if s.inicio <= t_abs + 1e-6 and s.fin > t_abs), None)
                cap_html = md(sub.texto) if sub else ""
                cap_t = (t_abs - sub.inicio) if sub else 0
                nav.estado(t_abs - esc.inicio, esc.beats, cap_html, cap_t)
                png = carpeta / f"{n:05d}.png"
                nav.captura(png)
                entradas.append((m, png))
                n += 1
    lista = carpeta / "concat.txt"
    lineas = []
    for k, (m, png) in enumerate(entradas):
        sig = entradas[k + 1][0] if k + 1 < len(entradas) else total_frames
        dur = max(1, sig - m) / fps
        lineas.append(f"file '{png.name}'\nduration {dur:.6f}")
    lineas.append(f"file '{entradas[-1][1].name}'")
    lista.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return lista


def portada(canal, visual: dict, cabecera: dict, destino: Path, horizontal: bool = False) -> None:
    """Captura el estado final de una escena (útil como portada/primer fotograma)."""
    with Navegador(horizontal) as nav:
        nav.cargar(html_escena(canal, visual, cabecera, horizontal))
        nav.estado(99, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "", 0)
        nav.captura(destino)
