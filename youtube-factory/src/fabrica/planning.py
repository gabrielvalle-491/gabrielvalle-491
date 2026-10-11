"""Calendario de 90 días: fase de aprendizaje (14 días con hipótesis distintas) + distribución
variada del resto (sin repetir pilar, tipo ni serie en días consecutivos)."""
from __future__ import annotations

import csv
from datetime import date, timedelta

from .config import cargar_canal, ruta
from .research import actualizar_cola

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

# Diseño de la fase de aprendizaje: cada día prueba una combinación distinta.
APRENDIZAJE = [
    ("pregunta", "media", "tipografía + demo"),
    ("resultado", "corta", "demo"),
    ("error", "media", "comparación"),
    ("contraste", "corta", "comparación"),
    ("mito", "media", "tipografía"),
    ("pregunta", "corta", "demo"),
    ("resultado", "media", "gráfico"),
    ("error", "corta", "demo"),
    ("contraste", "media", "gráfico"),
    ("pregunta", "media", "lista"),
    ("resultado", "corta", "tipografía"),
    ("mito", "corta", "comparación"),
    ("error", "media", "lista"),
    ("contraste", "media", "demo"),
]
DURACION = {"corta": "20-32 s (≈55-80 palabras)", "media": "35-55 s (≈85-140 palabras)"}

LARGOS = {
    "canal_a": [
        ("Guía de prompts para el trabajo: estructura, ejemplos y errores", "prompts"),
        ("Automatizaciones sin código para una pyme: Forms, Gmail, Calendar y WhatsApp Business", "automatizacion"),
        ("IA sin humo: qué hace bien, qué hace mal y cómo verificar", "ia_sin_humo"),
        ("Atención al cliente con IA: reclamos, reseñas y preguntas frecuentes", "negocio"),
        ("Cómo funciona un modelo de lenguaje, sin tecnicismos", "conceptos"),
        ("Privacidad y seguridad al usar IA en el trabajo", "seguridad"),
        ("Apps Script desde cero: enviar correos desde una planilla", "automatizacion"),
        ("IA para buscar trabajo: CV, carta y entrevista", "empleo"),
        ("Ventas con IA: guiones, objeciones y seguimiento", "negocio"),
        ("Python para no programadores: automatizar archivos", "automatizacion"),
        ("Organiza tu semana con IA: prioridades, reuniones y tareas", "productividad"),
        ("Tu biblioteca de prompts: un sistema reutilizable", "prompts"),
    ],
    "canal_b": [
        ("Control de gastos completo en una planilla, de cero a resumen mensual", "dinero"),
        ("Las fórmulas que más se usan en una oficina", "formulas"),
        ("Presupuesto 50/30/20 paso a paso", "dinero"),
        ("Deudas en planilla: amortización, bola de nieve y avalancha", "dinero"),
        ("Inventario y stock con alertas automáticas", "trabajo"),
        ("Tablas dinámicas desde cero", "trabajo"),
        ("Interés compuesto, inflación y metas de ahorro: las cuentas claras", "dinero"),
        ("Errores de planilla que cuestan dinero y cómo evitarlos", "errores"),
        ("Excel vs Google Sheets: guía para elegir", "excel_vs_sheets"),
        ("Resumen de ventas mensual con tabla dinámica y gráficos", "trabajo"),
        ("Cotizaciones y control de cobros para freelancers", "trabajo"),
        ("Funciones dinámicas: BUSCARX, FILTRO, UNICOS y ORDENAR", "formulas"),
    ],
}


def _elegir(disponibles: list[dict], plan: list[dict], ok) -> dict:
    """Mejor candidata que respeta la variedad. Prioriza pilares con muchas ideas pendientes
    (evita que al final del trimestre queden muchas ideas del mismo pilar juntas)."""
    restantes = {}
    for i in disponibles:
        restantes[i["pilar"]] = restantes.get(i["pilar"], 0) + 1
    total = max(1, len(disponibles))
    for nivel in (2, 1, 0):  # relaja restricciones de a una si hace falta
        cand = [i for i in disponibles if ok(i, plan, nivel)]
        if cand:
            return max(cand, key=lambda i: i["puntaje"] + 60 * restantes[i["pilar"]] / total)
    return disponibles[0]


def generar(canal_clave: str, inicio: date, dias: int = 90, fijos: int = 0) -> list[dict]:
    """fijos = cantidad de Shorts iniciales del calendario actual que se conservan (ya guionados)."""
    canal = cargar_canal(canal_clave)
    cola = actualizar_cola(canal_clave)
    disponibles = list(cola)  # ordenadas por puntaje
    plan: list[dict] = []
    if fijos:
        previos = [r for r in leer(canal_clave) if r["formato"] == "short"][:fijos]
        por_id = {i["id_idea"]: i for i in disponibles}
        for r in previos:
            idea = por_id[r["id_idea"]]
            disponibles.remove(idea)
            plan.append({**idea, "fase": r["fase"], "gancho_tipo": r["gancho_tipo"],
                         "duracion_objetivo": r["duracion_objetivo"], "hipotesis": r["hipotesis"]})

    def ok(idea, previos, nivel=2):
        if not previos:
            return True
        a = previos[-1]
        if idea["pilar"] == a["pilar"]:
            return False
        if nivel >= 1 and idea["tipo"] == a["tipo"]:
            return False
        if nivel >= 2 and any(idea["serie"] == p["serie"] for p in previos[-2:]):
            return False
        return True

    # Fase de aprendizaje: la mejor idea de cada pilar distinto, en rotación
    usados_pilares = []
    for k, (gancho, dur, visual) in enumerate(APRENDIZAJE[: min(14, dias)]):
        if k < len(plan):
            continue
        candidatas = [i for i in disponibles if i["pilar"] not in usados_pilares[-4:] and ok(i, plan)
                      and i["componentes"]["demanda"] >= 4]
        idea = candidatas[0] if candidatas else disponibles[0]
        disponibles.remove(idea)
        usados_pilares.append(idea["pilar"])
        plan.append({**idea, "fase": "aprendizaje", "gancho_tipo": gancho, "duracion_objetivo": DURACION[dur],
                     "hipotesis": f"Gancho '{gancho}' + duración {dur} + visual '{visual}': comparar % visto y "
                                  f"vistas a 7 días contra la media de la fase de aprendizaje."})
    # Resto: puntaje + restricciones de variedad
    while len(plan) < dias and disponibles:
        idea = _elegir(disponibles, plan, ok)
        disponibles.remove(idea)
        plan.append({**idea, "fase": "produccion", "gancho_tipo": "libre", "duracion_objetivo": DURACION["media"],
                     "hipotesis": f"Formato '{idea['tipo']}' en pilar '{idea['pilar']}': rendimiento frente a la media "
                                  f"del pilar (aplicar lo aprendido en la fase de aprendizaje)."})
    filas = []
    for k, it in enumerate(plan):
        f = inicio + timedelta(days=k)
        filas.append({
            "id": f"{canal.prefijo}-{k+1:03d}", "canal": canal_clave, "formato": "short", "fecha": f.isoformat(),
            "dia": DIAS[f.weekday()], "hora_ar": canal.datos["publicacion"]["hora_short"], "fase": it["fase"],
            "pilar": it["pilar"], "serie": it["serie"], "tipo": it["tipo"], "tema": it["tema"], "angulo": it["angulo"],
            "plantillas": ",".join(it["plantillas"]), "mercado": it.get("mercado", "latam"),
            "gancho_tipo": it["gancho_tipo"], "duracion_objetivo": it["duracion_objetivo"],
            "hipotesis": it["hipotesis"], "puntaje_idea": it["puntaje"], "id_idea": it["id_idea"],
        })
    # Videos largos: semanales desde la semana 2 (necesarios para horas de visualización)
    dia_largo = DIAS.index(canal.datos["publicacion"]["dia_largo"])
    f = inicio + timedelta(days=7)
    while f.weekday() != dia_largo:
        f += timedelta(days=1)
    for j, (tema, pilar) in enumerate(LARGOS[canal_clave]):
        fecha = f + timedelta(days=7 * j)
        if (fecha - inicio).days >= dias:
            break
        filas.append({
            "id": f"{canal.prefijo}-L{j+1:02d}", "canal": canal_clave, "formato": "largo", "fecha": fecha.isoformat(),
            "dia": DIAS[fecha.weekday()], "hora_ar": canal.datos["publicacion"]["hora_largo"], "fase": "largo",
            "pilar": pilar, "serie": "Guía completa", "tipo": "tutorial", "tema": tema,
            "angulo": "Amplía los Shorts del mismo pilar con ejemplos completos y descargable", "plantillas": "",
            "mercado": "latam", "gancho_tipo": "resultado", "duracion_objetivo": "6-10 min",
            "hipotesis": "Los videos largos aportan horas de visualización (requisito del YPP) y suscriptores por vista mayores que los Shorts.",
            "puntaje_idea": "", "id_idea": "",
        })
    filas.sort(key=lambda r: (r["fecha"], r["formato"]))
    out = ruta("strategy", f"calendario_{canal_clave}.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    return filas


def leer(canal_clave: str) -> list[dict]:
    p = ruta("strategy", f"calendario_{canal_clave}.csv")
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))
