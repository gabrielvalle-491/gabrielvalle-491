from fabrica.research import leer_banco, puntuar, similitud


def test_similitud():
    assert similitud("Cómo usar BUSCARX en Excel", "Como usar buscarx en excel") > 0.9
    assert similitud("Presupuesto 50/30/20", "Inyección de prompts") < 0.3


def test_bancos_completos_y_puntaje_explicable():
    for c in ("canal_a", "canal_b"):
        banco = leer_banco(c)
        assert len(banco) >= 90
        p = puntuar(banco[0], banco)
        assert 0 < p["puntaje"] <= 100
        assert set(p["componentes"]) == {"demanda", "oportunidad", "competencia", "comercial", "demostracion", "costo"}


def test_calendario_variedad(tmp_path):
    import csv

    from fabrica.config import ruta
    for c in ("canal_a", "canal_b"):
        filas = [r for r in csv.DictReader(open(ruta("strategy", f"calendario_{c}.csv"), encoding="utf-8")) if r["formato"] == "short"]
        assert len(filas) == 90
        assert len({r["tema"] for r in filas}) == 90  # sin temas repetidos
        consecutivos = sum(1 for a, b in zip(filas, filas[1:]) if a["pilar"] == b["pilar"])
        assert consecutivos <= 5
        assert sum(1 for r in filas if r["fase"] == "aprendizaje") == 14
