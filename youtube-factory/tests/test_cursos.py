"""Formato CURSO: temarios, capítulos, traducción de fórmulas y material de práctica."""
import shutil

import pytest

from fabrica import cursos
from fabrica.config import cargar_canal
from fabrica.specs import buscar_ficha, validar
from fabrica.visuals.templates import html_escena


def test_temarios_completos():
    for canal in ("canal_a", "canal_b"):
        ls = cursos.lecciones(canal)
        assert len(ls) == 12
        assert [x["n"] for x in ls] == list(range(1, 13))
        assert len({x["modulo_n"] for x in ls}) == 3
        for x in ls:
            assert x["titulo"] and len(x["objetivos"]) >= 3 and x.get("pilar")


def test_leccion_de_y_siguiente():
    lec = cursos.leccion_de(buscar_ficha("B-L01"))
    assert lec["n"] == 1 and lec["total"] == 12 and lec["modulo_n"] == 1
    assert lec["siguiente"]["id"] == "B-L02"


@pytest.mark.parametrize("es,en", [
    ("=SUMA(C2:C8)", "=SUM(C2:C8)"),
    ("=SI(B2>1000;\"Alto\";\"Bajo\")", "=IF(B2>1000,\"Alto\",\"Bajo\")"),
    ("=SUMAR.SI(A2:A9;\"Luz\";C2:C9)", "=SUMIF(A2:A9,\"Luz\",C2:C9)"),
    ("=REDONDEAR(B2*1,07;2)", "=ROUND(B2*1.07,2)"),
    ("=PAGO(5%/12;12;-1000)", "=PMT(5%/12,12,-1000)"),
    ("=BUSCARX(A2;D:D;E:E)", "=_xlfn.XLOOKUP(A2,D:D,E:E)"),
    ("=SI.ERROR(BUSCARV(A2;D:E;2;FALSO);\"\")", "=IFERROR(VLOOKUP(A2,D:E,2,FALSE),\"\")"),
    ("=\"a;b\"&SUMA(A1;A2)", "=\"a;b\"&SUM(A1,A2)"),
    ("texto suelto", "texto suelto"),
])
def test_formula_a_excel(es, en):
    assert cursos.formula_a_excel(es) == en


def test_funcion_desconocida():
    with pytest.raises(cursos.ErrorFormula):
        cursos.formula_a_excel("=INVENTADA(A1)")


def test_capitulos_desde_tiempos_reales():
    spec = buscar_ficha("B-L01")
    caps_idx = cursos.indices_capitulos(spec)
    assert caps_idx[0] == (0, "Introducción") and len(caps_idx) >= 4
    n = len(spec["escenas"])
    tec = {"duracion_s": 20.0 * n, "escenas": [{"inicio": 20.0 * i} for i in range(n)]}
    caps = cursos.capitulos(spec, tec)
    assert caps[0]["inicio"] == 0 and not cursos.validar_capitulos(caps)
    txt = cursos.texto_capitulos(caps)
    assert txt.splitlines()[0].startswith("0:00 ") and "*" not in txt


def test_capitulos_invalidos():
    assert cursos.validar_capitulos([{"inicio": 0, "fin": 5, "titulo": "a"}])  # menos de 3 y < 10 s


def test_lecciones_validas():
    for vid in ("A-L01", "B-L01"):
        assert validar(buscar_ficha(vid)) == []


def test_leccion_sin_estructura_falla():
    spec = buscar_ficha("B-L01")
    spec["escenas"] = [e for e in spec["escenas"] if e["visual"]["plantilla"] != "ejercicio"]
    assert any("ejercicio" in e for e in validar(spec))


def test_plantillas_curso_en_short_fallan():
    spec = buscar_ficha("B-010")
    spec["escenas"][0]["visual"] = {"plantilla": "capitulo", "datos": {"titulo": "x"}}
    assert any("plantillas de curso" in e for e in validar(spec))


def test_preparar_inyecta_datos_y_cabecera():
    s = cursos.preparar(buscar_ficha("B-L01"))
    v0 = s["escenas"][0]["visual"]
    assert v0["datos"]["leccion"] == 1 and v0["datos"]["objetivos"]
    assert v0["_cab"]["curso"] == "Excel desde cero"
    html = html_escena(cargar_canal("canal_b"), v0, {"marca": "Celda Clara"}, True)
    assert "Lección 1/12" in html and "Cap. 1/" in html
    cierre = s["escenas"][-1]["visual"]["datos"]
    assert cierre["siguiente"].startswith("Lección 2:") and cierre["material"].endswith(".xlsx")


def test_descripcion_con_marca_de_enlace_pendiente():
    from fabrica.metadata import descripcion_final
    d = descripcion_final(buscar_ficha("B-L01"))
    assert "Lección 1 de 12" in d and cursos.MARCA_ENLACE in d


@pytest.mark.skipif(not (shutil.which("soffice") or shutil.which("libreoffice")), reason="LibreOffice no instalado")
def test_material_xlsx_verificado(tmp_path):
    spec = buscar_ficha("B-L01")
    mat = spec["materiales"][0]
    destino = tmp_path / mat["archivo"]
    cursos.crear_xlsx(mat, cargar_canal("canal_b"), destino)
    assert cursos.verificar_xlsx(mat, destino)["estado"] == "ok"
    malo = dict(mat, hojas=[dict(mat["hojas"][1], verificar={"C9": 1})])
    cursos.crear_xlsx(malo, cargar_canal("canal_b"), destino)
    assert cursos.verificar_xlsx(malo, destino)["estado"] == "error"
