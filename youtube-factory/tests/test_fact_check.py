import pytest

from fabrica.fact_check import cifras_sin_respaldo, evaluar, riesgos_texto, verificar_calculos


def test_funciones_financieras_como_excel():
    assert round(evaluar("PAGO(0.02, 12, -1000)"), 2) == 94.56
    assert round(evaluar("NPER(0.04, -50, 1000)"), 2) == 41.04
    assert round(evaluar("VF(0.07, 10, 0, -1000)"), 2) == 1967.15
    assert evaluar("REDONDEAR(2.5, 0)") == 3.0  # la mitad se aleja de cero, como Excel


def test_evaluador_seguro_rechaza_codigo():
    with pytest.raises(ValueError):
        evaluar("__import__('os').system('echo x')")


def test_calculo_incorrecto_detectado():
    r = verificar_calculos({"fuentes": [{"calculo": "2+2", "resultado": 5, "respalda": "x"}]})
    assert r[0]["ok"] is False


def test_cifras_sin_respaldo_y_anios():
    spec = {"escenas": [{"narracion": "En 1979 hubo 1 967 casos y 3 870 más."}],
            "fuentes": [{"calculo": "1000*1.07**10", "respalda": "x"}]}
    assert cifras_sin_respaldo(spec) == [3870.0]


def test_riesgos_y_voseo():
    spec = {"titulo": "Rendimiento garantizado", "descripcion": "", "escenas": [{"narracion": "Mirá esto y guardalo."}]}
    r = " ".join(riesgos_texto(spec))
    assert "garantía" in r and "voseo" in r
