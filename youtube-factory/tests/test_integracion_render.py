"""Prueba de integración: produce un video corto real y verifica los controles técnicos.
Requiere modelo de voz y Chromium; se omite si faltan (ejecutar: python fabrica.py iniciar)."""
import pytest

from fabrica.config import ruta


@pytest.mark.skipif(not ruta("models", "kokoro-v1.0.onnx").exists(), reason="falta el modelo de voz")
def test_video_piloto_pasa_controles():
    from fabrica.quality import revisar_video
    from fabrica.specs import buscar_ficha
    spec = buscar_ficha("B-002")
    video = ruta("output", "canal_b", "videos", "B-002.mp4")
    if not video.exists():
        from fabrica.render import producir
        producir(spec, forzar=True)
    inf = revisar_video(spec)
    tecnicos = [i for i in inf.items if i["control"].startswith(("resolución", "códec", "30 fps", "audio AAC", "volumen", "subtítulos"))]
    assert tecnicos and all(i["ok"] for i in tecnicos), [i for i in tecnicos if not i["ok"]]
