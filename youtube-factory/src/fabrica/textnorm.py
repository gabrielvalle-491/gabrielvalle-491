"""Normalización de texto para narración (TTS) y subtítulos.

Convenciones del guion:
- *palabra*  -> se resalta en subtítulos; se narra normal.
- [[texto hablado|texto en pantalla]] -> se narra lo primero y se muestra lo segundo.
- Las cifras se convierten a palabras para la voz (p. ej. "1 500" -> "mil quinientos").
"""
from __future__ import annotations

import re

from num2words import num2words

# Léxico de pronunciación: términos en inglés, siglas y marcas frecuentes.
LEXICO_BASE = {
    r"\bIA\b": "i a",
    r"\bChatGPT\b": "chat yi pi ti",
    r"\bGPT\b": "yi pi ti",
    r"\bExcel\b": "éxcel",
    r"\bGoogle Sheets\b": "gúgol shits",
    r"\bSheets\b": "shits",
    r"\bGoogle\b": "gúgol",
    r"\bYouTube\b": "yutub",
    r"\bShorts\b": "shorts",
    r"\bPDF\b": "pe de efe",
    r"\bCSV\b": "ce ese uve",
    r"\bURL\b": "u erre ele",
    r"\bAPI\b": "a pe i",
    r"\bapps\b": "aps",
    r"\bapp\b": "ap",
    r"\bonline\b": "onláin",
    r"\bemail\b": "imeil",
    r"\bmail\b": "meil",
    r"\bprompt\b": "prompt",
    r"\bprompts\b": "prompts",
    r"\bWhatsApp\b": "guatsap",
    r"\bsoftware\b": "sófguer",
    r"\bfreelance\b": "frilans",
    r"\bfreelancer\b": "frilanser",
    r"\bNotion\b": "nóushon",
    r"\bCanva\b": "canva",
    r"\bUSD\b": "dólares",
    r"\bUS\$": "dólares ",
    r"\bTNA\b": "te ene a",
    r"\bTEA\b": "te e a",
    r"\bCAT\b": "cat",
    r"\bETF\b": "i ti ef",
    r"\bETFs\b": "i ti efs",
    r"\bKPI\b": "ka pe i",
    r"\bPC\b": "pe ce",
    r"\bOK\b": "okey",
    r"\bWi-Fi\b": "uaifai",
    r"\bSaaS\b": "sas",
    r"\bCV\b": "ce uve",
    r"\bLinkedIn\b": "linkedin",
}

_RE_MARCA = re.compile(r"\*([^*]+)\*")
_RE_DOBLE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")


def texto_hablado(texto: str, lexico: dict | None = None) -> str:
    t = _RE_DOBLE.sub(lambda m: m.group(1), texto)
    t = _RE_MARCA.sub(lambda m: m.group(1), t)
    t = numeros_a_palabras(t)
    for patron, rep in {**LEXICO_BASE, **(lexico or {})}.items():
        t = re.sub(patron, rep, t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def texto_pantalla(texto: str) -> str:
    """Texto para subtítulos: conserva marcas *resaltado* y usa la forma visual."""
    t = _RE_DOBLE.sub(lambda m: m.group(2), texto)
    return re.sub(r"\s+", " ", t).strip()


def sin_marcas(texto: str) -> str:
    return _RE_MARCA.sub(lambda m: m.group(1), texto_pantalla(texto))


def _entero(n: int) -> str:
    s = num2words(n, lang="es")
    # "uno" delante de sustantivo suena raro en cifras sueltas: se deja tal cual.
    return s


def _numero(txt: str) -> str:
    """Convierte '1 500', '1.500', '3,5', '12' a palabras. Miles con espacio o punto; decimal con coma."""
    limpio = txt.replace(" ", " ").replace(" ", " ")
    if "," in limpio:
        ent, dec = limpio.split(",", 1)
    else:
        ent, dec = limpio, ""
    ent = ent.replace(" ", "").replace(".", "")
    if not ent.isdigit():
        return txt
    palabras = _entero(int(ent))
    if dec and dec.isdigit():
        if len(dec) <= 2 and not dec.startswith("0"):
            palabras += " coma " + _entero(int(dec))
        else:
            palabras += " coma " + " ".join(_entero(int(d)) for d in dec)
    return palabras


_RE_NUM = re.compile(r"(?<![\w])(\d{1,3}(?:[ .  ]\d{3})+|\d+)(?:,(\d+))?")


def numeros_a_palabras(t: str) -> str:
    # Moneda: "$1 000" / "US$ 1 000" -> "mil dólares" sólo si se indica explícitamente con US$
    n = r"(\d{1,3}(?:[ .\u202f\u00a0]\d{3})+(?:,\d+)?|\d+(?:,\d+)?)"
    t = re.sub(r"US\$\s?" + n, lambda m: _numero(m.group(1)) + " dólares", t)
    t = re.sub(n + r"\s?%", lambda m: _numero(m.group(1)) + " por ciento", t)
    t = re.sub(r"(\d+)\s?[xX×]\b", lambda m: _numero(m.group(1)) + " veces", t)

    def rep(m):
        base = m.group(1)
        dec = m.group(2)
        return _numero(base + ("," + dec if dec else ""))

    return _RE_NUM.sub(rep, t)


def dividir_frases(texto: str) -> list[str]:
    """Divide en frases conservando los signos. No corta dentro de [[...]]."""
    protegido = _RE_DOBLE.sub(lambda m: m.group(0).replace(".", "․").replace("?", "？"), texto)
    partes = re.split(r"(?<=[.!?…])\s+(?=[¿¡A-ZÁÉÍÓÚÑ0-9*\[])", protegido.strip())
    return [p.replace("․", ".").replace("？", "?").strip() for p in partes if p.strip()]


def fmt_num(valor: float, decimales: int = 0, miles: str = " ", decimal: str = ",") -> str:
    """Formato recomendado por la RAE: espacio fino para miles, coma decimal."""
    s = f"{valor:,.{decimales}f}"
    s = s.replace(",", "§").replace(".", decimal).replace("§", miles)
    # La RAE no separa números de 4 cifras
    ent = s.split(decimal)[0]
    if len(ent.replace(miles, "")) == 4:
        s = s.replace(miles, "", 1)
    return s
