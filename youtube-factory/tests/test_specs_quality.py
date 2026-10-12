import pytest

from fabrica.metadata import descripcion_final, metadatos, puntuar_titulo
from fabrica.quality import revisar_guion
from fabrica.specs import listar_fichas, validar
from fabrica.timeline import _trozos

FICHAS = [f for f in listar_fichas() if not f["id"].endswith("TEST")]


@pytest.mark.parametrize("spec", FICHAS, ids=[f["id"] for f in FICHAS])
def test_fichas_validas_y_sin_criticos(spec):
    assert validar(spec) == []
    inf = revisar_guion(spec, FICHAS)
    assert not inf.criticos, inf.criticos


def test_metadatos_completos():
    spec = FICHAS[0]
    m = metadatos(spec)
    assert m["titulo"] and len(m["titulo"]) <= 100
    assert "voz sintética" in m["descripcion"]
    assert "<" not in descripcion_final(spec)
    assert m["publicar_en_utc"].endswith("Z")


def test_puntaje_titulo():
    bueno = puntuar_titulo("Pagar poco en la tarjeta: cuánto cuesta de verdad", ["tarjeta"])
    malo = puntuar_titulo("INCREÍBLE SECRETO", ["tarjeta"])
    assert bueno["puntaje"] > malo["puntaje"]


def test_subtitulos_no_parten_cifras():
    trozos = _trozos("En cinco años tendrías 1 403 y con US$ 1 000 al *7 % anual* terminas.")
    assert all("1 403" in t or "1 403" not in t for t in trozos)
    assert all(t.count("*") % 2 == 0 for t in trozos)
