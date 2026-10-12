from fabrica.analytics import ALIAS, _a_numero


def test_numeros_de_exportacion_studio():
    assert _a_numero("1,234") == 1.234 or _a_numero("1,234") == 1234  # ambigüedad documentada
    assert _a_numero("1,234.5") == 1234.5
    assert _a_numero("0:35") == 35
    assert _a_numero("1:02:03") == 3723
    assert _a_numero("45,6 %") == 45.6
    assert _a_numero("") is None


def test_encabezados_es_y_en():
    assert ALIAS["visualizaciones"] == ALIAS["views"] == "views"
    assert ALIAS["porcentaje promedio visto (%)"] == "averageViewPercentage"
