from fabrica.textnorm import dividir_frases, fmt_num, sin_marcas, texto_hablado, texto_pantalla


def test_cifras_a_palabras():
    t = texto_hablado("Con US$ 1 000 al 7 % anual tienes *1 967*.")
    assert t == "Con mil dólares al siete por ciento anual tienes mil novecientos sesenta y siete."


def test_decimales_con_coma():
    assert "tres coma cinco por ciento" in texto_hablado("Sube 3,5 %.")


def test_doble_hablado_pantalla():
    s = "Usa [[buscar equis|BUSCARX]] ya."
    assert texto_hablado(s) == "Usa buscar equis ya."
    assert texto_pantalla(s) == "Usa BUSCARX ya."
    assert sin_marcas("Es *clave*.") == "Es clave."


def test_dividir_frases():
    assert dividir_frases("¿Sabías esto? Es *clave*. ¡Listo!") == ["¿Sabías esto?", "Es *clave*.", "¡Listo!"]


def test_formato_rae():
    assert fmt_num(1500) == "1500"  # 4 cifras sin separador
    assert fmt_num(1234567) == "1 234 567"
    assert fmt_num(3.5, 1) == "3,5"
