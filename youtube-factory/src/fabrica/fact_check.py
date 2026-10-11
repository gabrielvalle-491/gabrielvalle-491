"""Exactitud y riesgo: cálculos reproducibles, cifras con respaldo, frases prohibidas, voseo y ortografía."""
from __future__ import annotations

import ast
import math
import operator
import re
from functools import lru_cache

from .config import ruta
from .textnorm import sin_marcas

# ---------------------------------------------------------------- evaluación segura de cálculos
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos, ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv}
_FUNCS = {"round": round, "abs": abs, "min": min, "max": max, "sum": sum, "log": math.log, "log10": math.log10,
          "exp": math.exp, "sqrt": math.sqrt, "ceil": math.ceil, "floor": math.floor, "len": len}


def _excel_round(x, n=0):
    """REDONDEAR de Excel: la mitad se aleja de cero (distinto del round() bancario de Python)."""
    m = 10 ** n
    return math.copysign(math.floor(abs(x) * m + 0.5) / m, x)


def _pago(tasa, nper, va, vf=0, tipo=0):
    if tasa == 0:
        return -(va + vf) / nper
    f = (1 + tasa) ** nper
    return -(tasa * (va * f + vf)) / ((1 + tasa * tipo) * (f - 1))


def _vf(tasa, nper, pago, va=0, tipo=0):
    if tasa == 0:
        return -(va + pago * nper)
    f = (1 + tasa) ** nper
    return -(va * f + pago * (1 + tasa * tipo) * (f - 1) / tasa)


def _va(tasa, nper, pago, vf=0, tipo=0):
    if tasa == 0:
        return -(vf + pago * nper)
    f = (1 + tasa) ** nper
    return -(vf + pago * (1 + tasa * tipo) * (f - 1) / tasa) / f


def _nper(tasa, pago, va, vf=0, tipo=0):
    if tasa == 0:
        return -(va + vf) / pago
    z = pago * (1 + tasa * tipo) / tasa
    return math.log((-vf + z) / (va + z)) / math.log(1 + tasa)


_FUNCS.update({"REDONDEAR": _excel_round, "PAGO": _pago, "VF": _vf, "VA": _va, "NPER": _nper})


def evaluar(expr: str):
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.operand))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUNCS:
            return _FUNCS[n.func.id](*[ev(a) for a in n.args])
        if isinstance(n, (ast.List, ast.Tuple)):
            return [ev(e) for e in n.elts]
        raise ValueError(f"expresión no permitida: {ast.dump(n)[:80]}")
    return ev(ast.parse(expr, mode="eval"))


def _num(s) -> float:
    if isinstance(s, (int, float)):
        return float(s)
    t = str(s).replace(" ", "").replace(" ", "").replace(" ", "").replace("US$", "").replace("$", "").replace("%", "")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    return float(t)


def verificar_calculos(spec: dict) -> list[dict]:
    out = []
    for f in spec.get("fuentes", []):
        if not f.get("calculo"):
            continue
        r = {"calculo": f["calculo"], "respalda": f.get("respalda", "")}
        try:
            valor = evaluar(f["calculo"])
            r["valor"] = valor
            if "resultado" in f:
                esperado = _num(f["resultado"])
                tol = max(abs(esperado) * 0.005, 0.011)
                r["ok"] = abs(float(valor) - esperado) <= tol
                r["esperado"] = esperado
            else:
                r["ok"] = True
        except Exception as e:  # noqa: BLE001
            r["ok"] = False
            r["error"] = str(e)
        out.append(r)
    return out


# ---------------------------------------------------------------- cifras sin respaldo
_RE_CIFRA = re.compile(r"(?<![\w#])(\d{1,3}(?:[ .  ]\d{3})+|\d+)(?:,(\d+))?")


def cifras_texto(texto: str) -> set[float]:
    out = set()
    for m in _RE_CIFRA.finditer(texto):
        try:
            out.add(_num(m.group(0)))
        except ValueError:
            pass
    return out


def cifras_sin_respaldo(spec: dict) -> list[float]:
    """Cifras > 10 mencionadas en la narración que no aparecen en cálculos, 'cifras' declaradas ni datos visuales."""
    narr = " ".join(e["narracion"] for e in spec["escenas"])
    narr = re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", narr)
    menc = set()
    for m in _RE_CIFRA.finditer(narr):
        txt = m.group(0)
        try:
            c = _num(txt)
        except ValueError:
            continue
        es_anio = re.fullmatch(r"(19|20)\d\d", txt) is not None
        if c > 10 and not es_anio:
            menc.add(c)
    respaldadas = set()
    for f in spec.get("fuentes", []):
        for c in f.get("cifras", []) or []:
            try:
                respaldadas.add(round(_num(c), 2))
            except ValueError:
                pass
        if f.get("calculo"):
            try:
                v = evaluar(f["calculo"])
                for x in (v if isinstance(v, list) else [v]):
                    respaldadas.update({round(float(x), 2), round(float(x)), math.floor(float(x)), math.ceil(float(x))})
            except Exception:  # noqa: BLE001
                pass
        if f.get("resultado") is not None:
            try:
                respaldadas.add(round(_num(f["resultado"]), 2))
            except ValueError:
                pass
    return sorted(c for c in menc if round(c, 2) not in respaldadas and round(c) not in respaldadas)


# ---------------------------------------------------------------- riesgo y estilo
FRASES_RIESGO = [
    (r"\bgarantizad[oa]s?\b", "promesa de garantía"),
    (r"\bsin riesgo\b", "afirma ausencia de riesgo"),
    (r"\bhacerte rico\b|\bhacerse rico\b|\bvolverte millonario\b", "promesa de riqueza"),
    (r"\bcompra (esta|estas) acci", "recomendación de inversión"),
    (r"\binvierte en\b", "recomendación de inversión directa"),
    (r"\bte recomiendo invertir\b", "recomendación de inversión"),
    (r"\bnadie te dice\b|\bel secreto que\b|\bte están ocultando\b", "clickbait engañoso"),
    (r"\b100 ?% (seguro|efectivo)\b", "afirmación absoluta"),
    (r"\bsoy (contador|abogado|médico|asesor)\b", "credencial inventada"),
    (r"\ben mi experiencia\b|\byo uso esto todos los días\b", "experiencia personal inventada"),
    (r"\bcura\b|\bdiagn[oó]stico\b", "salud"),
]
VOSEO = r"\b(tenés|podés|querés|sabés|hacé|mirá|fijate|probá|guardalo|guardala|usá|escribí|pedí|poné|vos|decí|elegí|andá|vení|sos|aprendé|seguí|compartí|contame|dejá|calculá|sumá|copiá|pegá|buscá|abrí|creá)\b"


def riesgos_texto(spec: dict) -> list[str]:
    texto = " ".join([spec.get("titulo", ""), spec.get("descripcion", ""), *[e["narracion"] for e in spec["escenas"]]])
    out = []
    excepciones = spec.get("excepciones_riesgo") or {}  # {motivo: justificación revisada}
    for patron, motivo in FRASES_RIESGO:
        if re.search(patron, texto, flags=re.I):
            if motivo in excepciones and len(str(excepciones[motivo])) >= 20:
                continue  # excepción explícita y justificada (queda registrada en la ficha)
            out.append(motivo)
    if re.search(VOSEO, texto, flags=re.I):
        out.append("voseo rioplatense: usar tú para español neutro (" +
                   ", ".join(sorted(set(m.group(0).lower() for m in re.finditer(VOSEO, texto, flags=re.I)))) + ")")
    return out


@lru_cache(maxsize=1)
def _diccionario():
    from spylls.hunspell import Dictionary
    d = Dictionary.from_files(str(ruta("assets", "diccionario", "es")))
    extra = set()
    p = ruta("assets", "diccionario", "palabras_extra.txt")
    for linea in p.read_text(encoding="utf-8").splitlines():
        if linea and not linea.startswith("#"):
            extra.add(linea.strip().lower())
    return d, extra


def textos_visibles(spec: dict) -> list[str]:
    out = [spec.get("titulo", ""), spec.get("descripcion", "")]
    for e in spec["escenas"]:
        out.append(sin_marcas(e["narracion"]))

        def recorrer(x):
            if isinstance(x, str):
                out.append(sin_marcas(x))
            elif isinstance(x, dict):
                for k, v in x.items():
                    if k not in ("formula", "codigo", "plantilla", "celda", "rango", "celda_formula", "texto") or k == "texto":
                        recorrer(v)
            elif isinstance(x, list):
                for v in x:
                    recorrer(v)
        recorrer(e.get("visual", {}).get("datos", {}))
    return out


def ortografia(spec: dict, extra_spec: list[str] | None = None) -> list[str]:
    d, extra = _diccionario()
    extra = extra | {w.lower() for w in (extra_spec or [])} | {w.lower() for w in spec.get("palabras_validas", [])}
    desconocidas = set()
    for t in textos_visibles(spec):
        t = re.sub(r"https?://\S+|\b[\w.-]+\.(?:com|org|net|gov|edu|io|ai|es|ar|mx)\b\S*|#\w+|\[[^\]]*\]|=[A-Z][^\s]*", " ", t)
        for w in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ.]*[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]|[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", t):
            w = w.strip(".")
            if len(w) < 3 or w.lower() in extra or w.isupper():
                continue
            if not (d.lookup(w) or d.lookup(w.lower())):
                desconocidas.add(w)
    return sorted(desconocidas)


def revisar(spec: dict) -> dict:
    calc = verificar_calculos(spec)
    return {
        "calculos": calc,
        "calculos_fallidos": [c for c in calc if not c.get("ok")],
        "cifras_sin_respaldo": cifras_sin_respaldo(spec),
        "riesgos": riesgos_texto(spec),
        "palabras_dudosas": ortografia(spec),
        "fuentes_url": [f["url"] for f in spec.get("fuentes", []) if f.get("url")],
    }
