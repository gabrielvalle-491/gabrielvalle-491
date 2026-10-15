"""Plantillas visuales HTML/CSS. Cada escena se dibuja con datos reales del guion.

Convenciones: los elementos con data-b="N" aparecen en el "beat" N de la escena
(sincronizado con la frase N de la narración). data-a define la animación.
"""
from __future__ import annotations

import base64
import html
import math
import re
from functools import lru_cache
from pathlib import Path

from ..config import ruta
from ..textnorm import fmt_num

RUNTIME = (Path(__file__).parent / "runtime.js").read_text(encoding="utf-8")


def esc(t) -> str:
    return html.escape(str(t), quote=True)


def md(t) -> str:
    """Texto con *resaltado* y [[hablado|pantalla]] -> HTML seguro."""
    t = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", lambda m: m.group(2), str(t))
    t = esc(t)
    t = re.sub(r"\*([^*]+)\*", r'<em class="hl">\1</em>', t)
    t = t.replace("\n", "<br>")
    return t


@lru_cache(maxsize=32)
def _font_face(nombre: str) -> str:
    carpeta = ruta("assets", "fonts", nombre)
    css = []
    for sub, rango in (("latin", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"),
                       ("latin-ext", "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF")):
        f = carpeta / f"{nombre}-{sub}-wght-normal.woff2"
        if f.exists():
            b64 = base64.b64encode(f.read_bytes()).decode()
            css.append(
                f"@font-face{{font-family:'{nombre}';font-style:normal;font-weight:100 900;"
                f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');unicode-range:{rango};}}"
            )
    return "\n".join(css)


def css_base(canal, horizontal: bool = False) -> str:
    p = canal.paleta
    f = canal.fuentes
    faces = "\n".join(_font_face(n) for n in {f["titulos"], f["cuerpo"], f["mono"]})
    W, H = (1920, 1080) if horizontal else (1080, 1920)
    claro = canal.datos["identidad"].get("subtitulos_claros", False)
    capfg, capst, capsh = (("#15201b", "rgba(255,255,255,.95)", "0 0 18px rgba(255,255,255,.9),0 3px 0 rgba(255,255,255,.9)") if claro
                           else ("#ffffff", "rgba(0,0,0,.55)", "0 4px 0 rgba(0,0,0,.55),0 0 22px rgba(0,0,0,.65)"))
    return faces + f"""
:root{{
  --bg:{p['fondo']};--bg2:{p['fondo2']};--fg:{p['texto']};--muted:{p['texto_suave']};
  --ac:{p['acento']};--ac2:{p['acento2']};--ok:{p['positivo']};--bad:{p['negativo']};
  --card:{p['tarjeta']};--line:{p['borde']};--acfg:{p.get('texto_sobre_acento', '#0b0b0b')};
  --fh:'{f['titulos']}',sans-serif;--fb:'{f['cuerpo']}',sans-serif;--fm:'{f['mono']}',monospace;
  --W:{W}px;--H:{H}px;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:var(--bg);color:var(--fg);font-family:var(--fb);
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}}
#bg{{position:absolute;inset:0;background:
   radial-gradient(1200px 900px at 85% -10%, color-mix(in srgb,var(--ac) 22%,transparent), transparent 60%),
   radial-gradient(1000px 900px at -10% 110%, color-mix(in srgb,var(--ac2) 18%,transparent), transparent 60%),
   linear-gradient(170deg,var(--bg2),var(--bg));}}
#grain{{position:absolute;inset:0;opacity:.07;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
#grid{{position:absolute;inset:0;opacity:.05;background-image:linear-gradient(var(--fg) 1px,transparent 1px),linear-gradient(90deg,var(--fg) 1px,transparent 1px);background-size:90px 90px;
   -webkit-mask-image:linear-gradient(180deg,#000 0%,transparent 75%)}}
#head{{position:absolute;top:150px;left:72px;right:72px;display:flex;align-items:center;gap:18px;font:700 30px/1 var(--fb);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
#head .pill{{background:var(--ac);color:var(--acfg);padding:12px 22px;border-radius:999px;letter-spacing:.04em}}
#head .ep{{margin-left:auto;font-family:var(--fm);font-weight:600;letter-spacing:0}}
#stage{{position:absolute;top:250px;left:72px;right:72px;height:860px;display:flex;flex-direction:column;justify-content:center;gap:34px}}
#cap{{position:absolute;left:50%;top:1170px;width:900px;transform:translateX(-50%);text-align:center;font:800 62px/1.18 var(--fh);
  color:{capfg};letter-spacing:-.01em;text-shadow:{capsh};-webkit-text-stroke:3px {capst};paint-order:stroke fill}}
#cap em{{font-style:normal;color:var(--ac)}}
em.hl{{font-style:normal;color:var(--ac)}}
.kicker{{font:700 34px/1.2 var(--fb);color:var(--ac);letter-spacing:.08em;text-transform:uppercase}}
.h1{{font:800 104px/1.02 var(--fh);letter-spacing:-.035em;height:auto;max-height:620px}}
.h2{{font:800 80px/1.06 var(--fh);letter-spacing:-.025em;max-height:300px}}
.h3{{font:700 54px/1.15 var(--fh);letter-spacing:-.01em}}
.p{{font:500 50px/1.3 var(--fb);color:var(--fg);max-height:520px}}
.muted{{color:var(--muted)}}
.small{{font:500 34px/1.3 var(--fb);color:var(--muted)}}
.card{{background:color-mix(in srgb,var(--card) 92%,transparent);border:2px solid var(--line);border-radius:34px;padding:40px 44px;box-shadow:0 30px 80px rgba(0,0,0,.35)}}
.mono{{font-family:var(--fm)}}
.row{{display:flex;gap:28px;align-items:stretch}}
.grow1{{flex:1}}
.src{{font:500 30px/1.3 var(--fb);color:var(--muted);border-left:6px solid var(--ac);padding-left:18px}}
.caret{{display:inline-block;width:.5em;height:1em;background:var(--ac);vertical-align:-0.12em;margin-left:4px}}
/* barras */
.bars{{display:flex;flex-direction:column;gap:30px}}
.bar .lab{{display:flex;justify-content:space-between;font:700 46px/1.1 var(--fb);margin-bottom:12px}}
.bar .lab b{{font-family:var(--fm);font-weight:700}}
.bar .track{{height:72px;border-radius:18px;background:color-mix(in srgb,var(--fg) 8%,transparent);overflow:hidden}}
.bar .fill{{height:100%;width:calc(var(--w) * var(--g,0));border-radius:18px;background:linear-gradient(90deg,color-mix(in srgb,var(--ac) 70%,var(--bg)),var(--ac))}}
.bar.alt .fill{{background:linear-gradient(90deg,color-mix(in srgb,var(--ac2) 60%,var(--bg)),var(--ac2))}}
.bar.dim .fill{{background:color-mix(in srgb,var(--fg) 30%,transparent)}}
/* planilla */
.sheet{{border-radius:26px;overflow:hidden;border:2px solid var(--line);background:#fbfbf8;color:#1d1d1f;box-shadow:0 30px 80px rgba(0,0,0,.4)}}
.fx{{display:flex;align-items:center;gap:18px;padding:20px 24px;background:#eef0ec;border-bottom:2px solid #d5d8d2;font:600 38px/1.2 var(--fm)}}
.fx .ref{{background:#fff;border:2px solid #cfd3cc;border-radius:10px;padding:6px 14px;min-width:96px;text-align:center}}
.fx .f{{font-style:italic;color:#7b7f78;font-family:var(--fb)}}
.fx .formula{{flex:1;white-space:nowrap;overflow:hidden;text-overflow:clip}}
table.g{{border-collapse:collapse;width:100%;font:500 40px/1.2 var(--fb)}}
table.g th{{background:#eef0ec;color:#6d716a;font:600 26px/1 var(--fm);padding:10px;border:1px solid #d9dcd5}}
table.g td{{padding:18px 18px;border:1px solid #e1e3de;white-space:nowrap;position:relative}}
table.g td.n{{text-align:right;font-family:var(--fm)}}
table.g tr.hdr td{{font-weight:800;background:#f3f4f0}}
table.g td .mk{{position:absolute;inset:-2px;border:5px solid var(--ac);background:color-mix(in srgb,var(--ac) 16%,transparent);opacity:var(--h,0);pointer-events:none}}
table.g td .mk.b2{{border-color:var(--ac2);background:color-mix(in srgb,var(--ac2) 16%,transparent)}}
table.g td.res{{font-weight:800;color:#0b0b0b}}
/* chips de formula */
.formula-big{{font:700 54px/1.3 var(--fm);word-break:break-all;background:var(--card);border:2px solid var(--line);border-radius:28px;padding:30px 34px}}
.tok{{border-radius:12px;padding:0 6px}}
.parts{{display:flex;flex-direction:column;gap:20px}}
.part{{display:flex;gap:22px;align-items:center;font:600 44px/1.22 var(--fb)}}
.part .k{{font:700 36px/1 var(--fm);padding:14px 18px;border-radius:16px;color:var(--acfg);min-width:150px;text-align:center}}
/* lista */
.list{{display:flex;flex-direction:column;gap:24px}}
.li{{display:flex;gap:26px;align-items:flex-start;font:650 52px/1.2 var(--fb)}}
.li .ic{{flex:none;width:76px;height:76px;border-radius:22px;display:grid;place-items:center;font:800 40px/1 var(--fh);background:var(--ac);color:var(--acfg)}}
.li .ic.x{{background:var(--bad);color:#fff}}
.li .ic.ok{{background:var(--ok);color:#0b0b0b}}
.li .tx{{padding-top:10px}}
.li .tx small{{display:block;font:500 32px/1.3 var(--fb);color:var(--muted);margin-top:8px}}
/* versus */
.vs{{display:flex;gap:26px}}
.vs .card{{flex:1;padding:34px 32px}}
.vs .t{{font:800 54px/1.08 var(--fh);margin-bottom:22px}}
.vs ul{{list-style:none;display:flex;flex-direction:column;gap:16px;font:500 40px/1.25 var(--fb)}}
.vs .card{{min-width:0;overflow-wrap:anywhere;hyphens:auto}}
.vs li{{display:flex;gap:12px;align-items:baseline}} .vs li::before{{flex:none}}
.vs li::before{{content:"";display:inline-block;width:14px;height:14px;border-radius:50%;background:var(--ac);margin-right:2px;transform:translateY(-.15em)}}
.vs .r li::before{{background:var(--ac2)}}
.vs .tag{{display:inline-block;font:700 26px/1 var(--fb);letter-spacing:.06em;text-transform:uppercase;padding:10px 16px;border-radius:999px;background:color-mix(in srgb,var(--fg) 10%,transparent);margin-bottom:18px}}
.verdict{{font:700 42px/1.25 var(--fb);text-align:center}}
/* mito */
.mito{{position:relative}}
.mito .lbl{{font:800 38px/1 var(--fb);letter-spacing:.12em;margin-bottom:18px}}
.mito .lbl.m{{color:var(--bad)}} .mito .lbl.r{{color:var(--ok)}}
.strike{{display:inline;text-decoration-line:line-through;text-decoration-thickness:.13em;text-decoration-skip-ink:none;
  text-decoration-color:color-mix(in srgb,var(--bad) calc(var(--s,0) * 100%),transparent)}}
/* pasos */
.steps{{display:flex;flex-direction:column;gap:22px}}
.step{{display:flex;gap:28px;align-items:center}}
.step .n{{flex:none;width:96px;height:96px;border-radius:50%;display:grid;place-items:center;font:800 48px/1 var(--fh);border:5px solid var(--ac);color:var(--ac)}}
.step .c{{font:700 50px/1.16 var(--fb)}}
.step .c small{{display:block;font:500 32px/1.3 var(--fb);color:var(--muted);margin-top:6px}}
/* prompt / codigo */
.prompt{{font:500 38px/1.42 var(--fm);white-space:pre-wrap;background:#0d1117;color:#e6edf3;border-radius:28px;padding:34px;border:2px solid var(--line);min-height:300px}}
.prompt .ph{{color:var(--acfg);background:var(--ac);border-radius:8px;padding:0 6px}}
.prompt .kw{{color:#ff7b72}} .prompt .st{{color:#a5d6ff}} .prompt .cm{{color:#8b949e}} .prompt .nu{{color:#79c0ff}}
.badge{{display:inline-flex;gap:12px;align-items:center;font:700 28px/1 var(--fb);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.badge i{{width:16px;height:16px;border-radius:50%;background:var(--ac)}}
/* numero grande */
.big{{font:800 200px/0.95 var(--fh);letter-spacing:-.05em;color:var(--ac);white-space:nowrap}}
.big.fit{{max-width:100%;height:220px;overflow:hidden}}
/* calculo */
.calc{{display:flex;flex-direction:column;gap:18px}}
.calc .l{{display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding:22px 30px;border-radius:22px;background:color-mix(in srgb,var(--card) 90%,transparent);border:2px solid var(--line)}}
.calc .l .a{{font:600 44px/1.2 var(--fb)}} .calc .l .b{{font:700 52px/1 var(--fm);color:var(--ac);white-space:nowrap}}
.calc .l small{{display:block;font:500 28px/1.2 var(--fb);color:var(--muted);margin-top:6px}}
.calc .res{{background:var(--ac);color:var(--acfg);border-color:transparent}} .calc .res .b{{color:var(--acfg)}}
/* quiz */
.opts{{display:flex;flex-direction:column;gap:22px}}
.opt{{display:flex;gap:24px;align-items:center;padding:28px 30px;border-radius:24px;border:3px solid var(--line);background:var(--card);font:700 48px/1.2 var(--fb)}}
.opt .L{{flex:none;width:70px;height:70px;border-radius:18px;display:grid;place-items:center;background:color-mix(in srgb,var(--fg) 12%,transparent);font:800 36px/1 var(--fh)}}
.opt.ok{{position:relative}}
.opt.ok::after{{content:"";position:absolute;inset:-3px;border-radius:24px;border:6px solid var(--ok);background:color-mix(in srgb,var(--ok) 14%,transparent);opacity:var(--h,0)}}
/* timeline */
.tl{{position:relative;display:flex;flex-direction:column;gap:30px;padding-left:60px}}
.tl::before{{content:"";position:absolute;left:18px;top:10px;bottom:10px;width:6px;border-radius:3px;background:color-mix(in srgb,var(--fg) 18%,transparent)}}
.ev{{position:relative}}
.ev::before{{content:"";position:absolute;left:-55px;top:10px;width:34px;height:34px;border-radius:50%;background:var(--ac);border:6px solid var(--bg)}}
.ev .d{{font:800 36px/1 var(--fm);color:var(--ac);margin-bottom:8px}} .ev .x{{font:600 46px/1.22 var(--fb)}}
/* donut */
.donut-wrap{{display:flex;flex-direction:column;align-items:center;gap:30px}}
.legend{{display:flex;flex-direction:column;gap:18px;width:100%}}
.legend .it{{display:flex;align-items:center;gap:20px;font:700 46px/1.2 var(--fb)}}
.legend .it i{{width:34px;height:34px;border-radius:10px;flex:none}}
.legend .it b{{margin-left:auto;font-family:var(--fm)}}
/* cierre */
.cta{{display:inline-flex;align-self:flex-start;align-items:center;gap:16px;background:var(--ac);color:var(--acfg);font:800 40px/1 var(--fb);padding:26px 34px;border-radius:999px}}
/* horizontal (videos largos) */
body.h #head{{top:56px;left:96px;right:96px}}
body.h #stage{{top:150px;left:96px;right:96px;height:740px}}
body.h #cap{{top:920px;width:1500px;font-size:50px}}
body.h .h1{{font-size:96px;max-height:520px}}
body.h .p{{font-size:50px;max-height:560px}}
body.h .h2{{font-size:84px}}
body.h .li{{font-size:58px}} body.h .li .tx small{{font-size:34px}}
body.h .step .c{{font-size:56px}} body.h .step .c small{{font-size:34px}}
body.h .part{{font-size:52px}} body.h .formula-big{{font-size:66px}}
body.h .sheet{{width:100%;max-width:1500px;align-self:center}}
body.h table.g{{font-size:38px}} body.h table.g td{{padding:9px 18px}} body.h table.g th{{padding:6px}}
body.h .fx{{padding:14px 22px;font-size:34px}}
body.h .prompt{{font-size:46px}}
body.h .vs ul{{font-size:46px}} body.h .vs .t{{font-size:60px}}
body.h .calc .l .a{{font-size:50px}} body.h .calc .l .b{{font-size:58px}}
/* ---- formato CURSO (lecciones horizontales) ---- */
#head.curso{{gap:22px}}
#head.curso .mod{{color:var(--fg);opacity:.75}}
#head.curso .caps{{margin-left:auto;display:flex;align-items:center;gap:10px;font:600 24px/1 var(--fm);letter-spacing:0}}
#head.curso .caps i{{width:46px;height:10px;border-radius:5px;background:color-mix(in srgb,var(--fg) 16%,transparent)}}
#head.curso .caps i.on{{background:var(--ac)}} #head.curso .caps i.now{{background:var(--ac2)}}
#head.curso .caps span{{margin-left:10px;color:var(--muted)}}
.cp{{display:grid;grid-template-columns:1.15fr 1fr;gap:64px;align-items:center}}
.cp .h1{{font-size:84px;max-height:420px}}
.cp .meta{{font:700 30px/1.3 var(--fb);color:var(--muted);margin-top:22px}}
.cp .obj .t{{font:800 34px/1.2 var(--fb);letter-spacing:.06em;text-transform:uppercase;color:var(--ac);margin-bottom:22px}}
body.h .cp .obj .li{{font-size:42px}} .cp .obj .li .ic{{width:58px;height:58px;font-size:30px;border-radius:16px}}
.dots{{display:flex;gap:12px;align-items:center;margin-top:34px}}
.dots i{{width:44px;height:14px;border-radius:7px;background:color-mix(in srgb,var(--fg) 14%,transparent)}}
.dots i.on{{background:color-mix(in srgb,var(--ac) 55%,transparent)}} .dots i.now{{background:var(--ac);width:88px}}
.dots span{{font:700 26px/1 var(--fm);color:var(--muted);margin-left:12px}}
.chap{{display:flex;flex-direction:column;justify-content:center;gap:26px}}
.chap .num{{font:800 230px/.9 var(--fh);letter-spacing:-.06em;color:var(--ac)}}
.chap .lab{{font:700 34px/1 var(--fm);color:var(--muted);letter-spacing:.04em;text-transform:uppercase}}
.chap .h1{{font-size:96px;max-height:360px}}
.chap .bar{{height:14px;border-radius:7px;background:color-mix(in srgb,var(--fg) 12%,transparent);overflow:hidden;max-width:900px}}
.chap .bar b{{display:block;height:100%;width:calc(var(--w) * var(--g,0));background:var(--ac);border-radius:7px}}
.ej{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
.ej .izq{{display:flex;flex-direction:column;gap:30px;align-items:flex-start}} .ej .der{{display:flex;flex-direction:column;gap:30px}}
.ej .pista .small{{margin-bottom:8px}} .ej .pista .p{{font-size:38px}}
.ej .tag{{display:inline-flex;gap:14px;align-items:center;font:800 30px/1 var(--fb);letter-spacing:.08em;text-transform:uppercase;background:var(--ac2);color:#111;padding:14px 22px;border-radius:999px}}
.ej .pausa{{display:inline-flex;gap:14px;align-items:center;font:700 30px/1 var(--fb);color:var(--muted);margin-left:18px}}
.ej .pausa i{{width:30px;height:34px;border-left:10px solid var(--ac2);border-right:10px solid var(--ac2)}}
.ej .h2{{font-size:76px;max-height:440px}}
.ej .steps .step .n{{width:76px;height:76px;font-size:36px;border-width:4px}} body.h .ej .steps .step .c{{font-size:44px}}
.chip{{display:inline-flex;gap:14px;align-items:center;font:600 28px/1.25 var(--fm);padding:16px 22px;border-radius:18px;border:2px dashed var(--ac);color:var(--fg);background:color-mix(in srgb,var(--ac) 8%,transparent)}}
.cc{{display:grid;grid-template-columns:1.2fr 1fr;gap:56px;align-items:center}}
.cc .h2{{font-size:66px}}
body.h .cc .list .li{{font-size:44px}} .cc .list .li .ic{{width:58px;height:58px;font-size:30px;border-radius:16px}}
.cc .next .t{{font:800 28px/1 var(--fb);letter-spacing:.08em;text-transform:uppercase;color:var(--ac);margin-bottom:18px}}
.cc .next .x{{font:800 52px/1.12 var(--fh);letter-spacing:-.02em}}
.cc .side{{display:flex;flex-direction:column;gap:28px}}
"""


# ---------------------------------------------------------------- plantillas

def _bloque_titulo(d, beat=0):
    out = ""
    if d.get("kicker"):
        out += f'<div class="kicker" data-b="{beat}" data-a="up">{md(d["kicker"])}</div>'
    if d.get("titulo"):
        out += f'<div class="h2 fit" data-b="{beat}" data-a="up" data-delay="0.06">{md(d["titulo"])}</div>'
    return out


def t_hook(d):
    out = ""
    if d.get("kicker"):
        out += f'<div class="kicker" data-b="0" data-a="up">{md(d["kicker"])}</div>'
    out += f'<div class="h1 fit" data-b="0" data-a="up" data-delay="0.05" data-min="60">{md(d["titulo"])}</div>'
    if d.get("numero") is not None:
        n = d["numero"]
        out += _contador(n, beat=d.get("beat_numero", 1))
    if d.get("sub"):
        out += f'<div class="p muted fit" data-b="{d.get("beat_sub", 1)}" data-a="up">{md(d["sub"])}</div>'
    return out


def _contador(n: dict, beat: int = 1) -> str:
    dec = int(n.get("decimales", 0))
    to = float(n["valor"])
    pre, suf = n.get("prefijo", ""), n.get("sufijo", "")
    final = esc(pre) + fmt_num(to, dec) + esc(suf)
    return (f'<div class="big fit" data-min="90" data-b="{beat}" data-a="count" data-dur="{n.get("dur", 1.1)}" '
            f'data-from="{n.get("desde", 0)}" data-to="{to}" data-dec="{dec}" data-pre="{esc(pre)}" data-suf="{esc(suf)}">{final}</div>')


def t_texto(d):
    out = _bloque_titulo(d)
    out += f'<div class="p fit" data-b="{d.get("beat_texto", 0 if not d.get("titulo") else 1)}" data-a="up">{md(d["texto"])}</div>'
    if d.get("nota"):
        out += f'<div class="small" data-b="{d.get("beat_nota", 1)}" data-a="up">{md(d["nota"])}</div>'
    return out


def t_numero(d):
    out = ""
    if d.get("antes"):
        out += f'<div class="h3 muted" data-b="0" data-a="up">{md(d["antes"])}</div>'
    out += _contador(d, beat=d.get("beat_numero", 0))
    if d.get("etiqueta"):
        out += f'<div class="h2 fit" data-b="{d.get("beat_etiqueta", 0)}" data-a="up" data-delay=".15">{md(d["etiqueta"])}</div>'
    if d.get("nota"):
        out += f'<div class="p muted fit" data-b="{d.get("beat_nota", 1)}" data-a="up">{md(d["nota"])}</div>'
    return out


def t_barras(d):
    items = d["items"]
    maximo = float(d.get("maximo") or max(float(i["valor"]) for i in items))
    out = _bloque_titulo(d)
    base = int(d.get("beat_inicio", 0))
    if d.get("todas_juntas"):
        base_beats = [base] * len(items)
    else:
        base_beats = [base + k for k in range(len(items))]
    bars = []
    for k, it in enumerate(items):
        w = max(0.02, float(it["valor"]) / maximo) * 100
        cls = "bar" + (" alt" if it.get("destacado") else "") + (" dim" if it.get("tenue") else "")
        txt = it.get("texto") or (d.get("prefijo", "") + fmt_num(float(it["valor"]), int(d.get("decimales", 0))) + d.get("sufijo", ""))
        b = base_beats[k]
        bars.append(
            f'<div class="{cls}" data-b="{b}" data-a="up"><div class="lab"><span>{md(it["etiqueta"])}</span><b>{esc(txt)}</b></div>'
            f'<div class="track"><div class="fill" style="--w:{w:.2f}%" data-b="{b}" data-a="grow" data-dur="0.9"></div></div></div>'
        )
    out += '<div class="bars">' + "".join(bars) + "</div>"
    if d.get("nota"):
        out += f'<div class="small" data-b="{d.get("beat_nota", base_beats[-1])}" data-a="up" data-delay=".3">{md(d["nota"])}</div>'
    return out


def t_linea(d):
    W, H, pad = 936, 640, 70
    series = d["series"]
    todos = [v for s in series for v in s["valores"]]
    vmin = float(d.get("minimo", min(0, min(todos))))
    vmax = float(d.get("maximo", max(todos))) * 1.08
    n = max(len(s["valores"]) for s in series)

    def xy(i, v):
        x = pad + (W - pad - 20) * (i / max(1, n - 1))
        y = H - pad - (H - 2 * pad) * ((v - vmin) / (vmax - vmin or 1))
        return x, y

    colores = ["var(--ac)", "var(--ac2)", "var(--muted)"]
    svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="overflow:visible">']
    for g in range(5):
        y = pad + (H - 2 * pad) * g / 4
        val = vmax - (vmax - vmin) * g / 4
        svg.append(f'<line x1="{pad}" x2="{W-20}" y1="{y:.1f}" y2="{y:.1f}" stroke="currentColor" stroke-opacity=".12" stroke-width="2"/>')
        svg.append(f'<text x="{pad-14}" y="{y+10:.1f}" text-anchor="end" font-size="26" fill="currentColor" fill-opacity=".55" font-family="var(--fm)">{esc(d.get("prefijo",""))}{fmt_num(val, int(d.get("decimales_eje",0)))}{esc(d.get("sufijo_eje",""))}</text>')
    etiquetas = d.get("etiquetas_x") or []
    for i, et in enumerate(etiquetas):
        if et == "":
            continue
        x, _ = xy(i, vmin)
        svg.append(f'<text x="{x:.1f}" y="{H-pad+44}" text-anchor="middle" font-size="26" fill="currentColor" fill-opacity=".6" font-family="var(--fm)">{esc(et)}</text>')
    for k, s in enumerate(series):
        pts = [xy(i, float(v)) for i, v in enumerate(s["valores"])]
        dpath = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        col = s.get("color") or colores[k % 3]
        b = s.get("beat", k)
        area = dpath + f" L{pts[-1][0]:.1f},{H-pad} L{pts[0][0]:.1f},{H-pad} Z"
        if k == 0 and d.get("area", True):
            svg.append(f'<path d="{area}" fill="{col}" fill-opacity=".10" data-b="{b}" data-a="fade" data-dur="1.4" data-delay=".3"/>')
        svg.append(f'<path d="{dpath}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" data-b="{b}" data-a="draw" data-dur="1.4" data-delay=".3"/>')
        lx, ly = pts[-1]
        fin = s.get("etiqueta_final") or (d.get("prefijo", "") + fmt_num(float(s["valores"][-1]), int(d.get("decimales", 0))) + d.get("sufijo", ""))
        svg.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="14" fill="{col}" data-b="{b}" data-a="pop" data-delay="1.5"/>')
        svg.append(f'<text x="{lx-10:.1f}" y="{ly-30:.1f}" text-anchor="end" font-size="40" font-weight="800" fill="{col}" font-family="var(--fm)" data-b="{b}" data-a="up" data-delay="1.55">{esc(fin)}</text>')
    svg.append("</svg>")
    out = _bloque_titulo(d)
    leyenda = ""
    if len(series) > 1:
        leyenda = '<div class="legend" style="flex-direction:row;flex-wrap:wrap;gap:26px">' + "".join(
            f'<div class="it" style="font-size:32px" data-b="{s.get("beat", k)}" data-a="up"><i style="background:{s.get("color") or colores[k % 3]}"></i>{md(s["nombre"])}</div>'
            for k, s in enumerate(series)) + "</div>"
    out += leyenda + '<div style="color:var(--fg)">' + "".join(svg) + "</div>"
    if d.get("nota"):
        out += f'<div class="small" data-b="{d.get("beat_nota", len(series))}" data-a="up">{md(d["nota"])}</div>'
    return out


def _letras(n):
    return [chr(65 + i) for i in range(n)]


def _parse_rango(r: str):
    m = re.match(r"([A-Z])(\d+)(?::([A-Z])(\d+))?$", r.strip())
    if not m:
        raise ValueError(f"Rango inválido: {r}")
    c1, f1 = ord(m.group(1)) - 65, int(m.group(2))
    c2, f2 = (ord(m.group(3)) - 65, int(m.group(4))) if m.group(3) else (c1, f1)
    return [(c, f) for c in range(min(c1, c2), max(c1, c2) + 1) for f in range(min(f1, f2), max(f1, f2) + 1)]


def t_planilla(d):
    filas = d["filas"]
    ncol = max(len(f) for f in filas)
    marcas = {}
    for k, r in enumerate(d.get("resaltar", [])):
        for celda in _parse_rango(r["rango"]):
            marcas.setdefault(celda, []).append((r.get("beat", k + 1), "b2" if r.get("alterno") else ""))
    res = d.get("resultado")
    res_celda = _parse_rango(res["celda"])[0] if res else None
    out = _bloque_titulo(d) if d.get("titulo") else ""
    fx_ref = esc(d.get("celda_formula", res["celda"] if res else ""))
    formula = d.get("formula", "")
    beat_f = d.get("beat_formula", 0)
    fx = (f'<div class="fx"><span class="ref">{fx_ref}</span><span class="f">fx</span>'
          f'<span class="formula" data-b="{beat_f}" data-a="type" data-dur="{max(0.6, len(formula) * 0.045):.2f}">{esc(formula)}</span></div>')
    head = "<tr><th></th>" + "".join(f"<th>{l}</th>" for l in _letras(ncol)) + "</tr>"
    cuerpo = []
    for i, fila in enumerate(filas, start=1):
        cls = ' class="hdr"' if (i == 1 and d.get("encabezado", True)) else ""
        celdas = [f"<th>{i}</th>"]
        for c in range(ncol):
            v = fila[c] if c < len(fila) else ""
            es_num = isinstance(v, (int, float)) or bool(re.match(r"^[\d\s.,$%\-+]+$", str(v)))
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                decs = d.get("decimales", 0)
                dec = decs[c] if isinstance(decs, list) and c < len(decs) else (decs if isinstance(decs, int) else 0)
                v = fmt_num(v, dec) if not (isinstance(v, int) and dec == 0 and abs(v) < 10000 and d.get("anios_sin_separador", True)) else str(v)
            mk = "".join(f'<span class="mk {cl}" data-b="{b}" data-a="hl"></span>' for b, cl in marcas.get((c, i), []))
            tdcls = ["n"] if es_num and str(v) else []
            if res_celda == (c, i):
                tdcls.append("res")
                if "n" not in tdcls and re.match(r"^[\d\s.,$%\-+\u00a0\u202f]+$", str(res["valor"])):
                    tdcls.append("n")
                v_html = f'<span data-b="{res.get("beat", 2)}" data-a="pop">{esc(res["valor"])}</span>'
            else:
                v_html = esc(v)
            celdas.append(f'<td class="{" ".join(tdcls)}">{v_html}{mk}</td>')
        cuerpo.append(f"<tr{cls}>" + "".join(celdas) + "</tr>")
    out += f'<div class="sheet" data-b="0" data-a="up">{fx}<table class="g fitw" data-min="22">{head}{"".join(cuerpo)}</table></div>'
    if d.get("nota"):
        out += f'<div class="small" data-b="{d.get("beat_nota", 1)}" data-a="up">{md(d["nota"])}</div>'
    return out


def t_formula(d):
    colores = ["var(--ac)", "var(--ac2)", "var(--ok)", "#f2c14e", "#c084fc"]
    # Resalta cada token en orden, de izquierda a derecha, sobre el texto original (nunca dentro del HTML ya generado)
    raw, f, cursor = d["formula"], "", 0
    for k, p in enumerate(d.get("partes", [])):
        i = raw.find(p["token"], cursor)
        if i < 0:
            i = raw.find(p["token"])
            if i < cursor:
                continue
        f += esc(raw[cursor:i]) + (f'<span class="tok" style="background:color-mix(in srgb,{colores[k%5]} 30%,transparent)">'
                                   f'{esc(p["token"])}</span>')
        cursor = i + len(p["token"])
    f += esc(raw[cursor:])
    out = _bloque_titulo(d)
    out += f'<div class="formula-big" data-b="0" data-a="up">{f}</div><div class="parts">'
    for k, p in enumerate(d.get("partes", [])):
        b = p.get("beat", k + 1)
        out += (f'<div class="part" data-b="{b}" data-a="left"><span class="k" style="background:{colores[k%5]}">{esc(p["token"])}</span>'
                f'<span>{md(p["explica"])}</span></div>')
    out += "</div>"
    if d.get("nota"):
        out += f'<div class="small" data-b="{d.get("beat_nota", len(d.get("partes", [])))}" data-a="up">{md(d["nota"])}</div>'
    return out


def t_lista(d):
    estilo = d.get("estilo", "num")
    out = _bloque_titulo(d)
    base = int(d.get("beat_inicio", 0))
    out += '<div class="list">'
    for k, it in enumerate(d["items"]):
        if isinstance(it, str):
            it = {"texto": it}
        ic = {"num": str(k + 1), "check": "✓", "x": "✕"}.get(it.get("estilo", estilo), str(k + 1))
        cls = {"check": "ok", "x": "x"}.get(it.get("estilo", estilo), "")
        det = f"<small>{md(it['detalle'])}</small>" if it.get("detalle") else ""
        out += (f'<div class="li" data-b="{it.get("beat", base + k)}" data-a="left" data-delay="{0.25 if k == 0 else 0}"><span class="ic {cls}">{ic}</span>'
                f'<span class="tx">{md(it["texto"])}{det}</span></div>')
    return out + "</div>"


def t_versus(d):
    def lado(x, cls, b):
        tag = f'<div class="tag">{md(x["etiqueta"])}</div>' if x.get("etiqueta") else ""
        larga = max((len(w) for i in x.get("items", []) for w in re.sub(r"[*\[\]|]", " ", str(i)).split()), default=0)
        tam = "" if larga <= 12 else (' style="font-size:34px"' if larga <= 15 else ' style="font-size:29px"')
        items = "".join(f"<li>{md(i)}</li>" for i in x.get("items", []))
        items = items.replace("<li>", f"<li{tam}>")
        return f'<div class="card {cls}" data-b="{b}" data-a="{"left" if cls=="l" else "right"}">{tag}<div class="t">{md(x["titulo"])}</div><ul>{items}</ul></div>'
    out = _bloque_titulo(d)
    out += f'<div class="vs">{lado(d["izq"], "l", d.get("beat_izq", 0))}{lado(d["der"], "r", d.get("beat_der", 1))}</div>'
    if d.get("veredicto"):
        out += f'<div class="verdict card" data-b="{d.get("beat_veredicto", 2)}" data-a="pop">{md(d["veredicto"])}</div>'
    return out


def t_mito(d):
    out = (f'<div class="card mito" data-b="0" data-a="up"><div class="lbl m">MITO</div>'
           f'<div class="h3"><span class="strike" data-b="{d.get("beat_tachar", 1)}" data-a="strike" data-dur=".6">{md(d["mito"])}</span></div></div>'
           f'<div class="card mito" data-b="{d.get("beat_realidad", 1)}" data-a="up" data-delay=".35" style="border-color:var(--ok)"><div class="lbl r">REALIDAD</div>'
           f'<div class="h3">{md(d["realidad"])}</div></div>')
    if d.get("fuente"):
        out += f'<div class="src" data-b="{d.get("beat_realidad", 1)}" data-a="up" data-delay=".6">Fuente: {md(d["fuente"])}</div>'
    return out


def t_pasos(d):
    out = _bloque_titulo(d)
    base = int(d.get("beat_inicio", 0))
    out += '<div class="steps">'
    for k, p in enumerate(d["pasos"]):
        if isinstance(p, str):
            p = {"titulo": p}
        det = f"<small>{md(p['detalle'])}</small>" if p.get("detalle") else ""
        out += f'<div class="step" data-b="{p.get("beat", base + k)}" data-a="left" data-delay="{0.25 if k == 0 else 0}"><span class="n">{k+1}</span><span class="c">{md(p["titulo"])}{det}</span></div>'
    return out + "</div>"


def _resaltar_prompt(t: str) -> str:
    t = esc(t)
    return re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', t)


def _resaltar_codigo(t: str, lenguaje: str) -> str:
    t = esc(t)
    t = re.sub(r"(#[^\n]*)", r'<span class="cm">\1</span>', t)
    t = re.sub(r"(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)", r'<span class="st">\1</span>', t)
    kws = r"\b(def|return|import|from|for|in|if|else|elif|while|print|True|False|None|with|as|SI|Y|O)\b"
    t = re.sub(kws, r'<span class="kw">\1</span>', t)
    return t


def t_prompt(d):
    out = _bloque_titulo(d)
    out += f'<div class="badge" data-b="0" data-a="up"><i></i>{esc(d.get("etiqueta", "Plantilla de prompt"))}</div>'
    dur = max(1.0, min(4.0, len(d["texto"]) * 0.018))
    out += f'<div class="prompt fit" data-min="26" style="max-height:640px" data-b="{d.get("beat_texto", 0)}" data-a="type" data-delay=".3" data-dur="{dur:.2f}">{_resaltar_prompt(d["texto"])}</div>'
    if d.get("nota"):
        out += f'<div class="small" data-b="{d.get("beat_nota", 1)}" data-a="up">{md(d["nota"])}</div>'
    return out


def t_codigo(d):
    out = _bloque_titulo(d)
    out += f'<div class="badge" data-b="0" data-a="up"><i></i>{esc(d.get("lenguaje", "código"))}</div>'
    dur = max(1.0, min(4.0, len(d["codigo"]) * 0.02))
    out += f'<div class="prompt fit" data-min="24" style="max-height:640px" data-b="{d.get("beat_codigo", 0)}" data-a="type" data-delay=".3" data-dur="{dur:.2f}">{_resaltar_codigo(d["codigo"], d.get("lenguaje",""))}</div>'
    if d.get("nota"):
        out += f'<div class="small" data-b="{d.get("beat_nota", 2)}" data-a="up">{md(d["nota"])}</div>'
    return out


def t_dato(d):
    out = ""
    if d.get("kicker"):
        out += f'<div class="kicker" data-b="0" data-a="up">{md(d["kicker"])}</div>'
    out += f'<div class="h2 fit" style="max-height:520px" data-b="0" data-a="up" data-delay=".05">{md(d["dato"])}</div>'
    if d.get("contexto"):
        out += f'<div class="p muted fit" style="max-height:300px" data-b="{d.get("beat_contexto", 1)}" data-a="up">{md(d["contexto"])}</div>'
    if d.get("fuente"):
        out += f'<div class="src" data-b="{d.get("beat_fuente", 0)}" data-a="up" data-delay=".3">Fuente: {md(d["fuente"])}</div>'
    return out


def t_calculo(d):
    out = _bloque_titulo(d)
    base = int(d.get("beat_inicio", 0))
    out += '<div class="calc">'
    for k, l in enumerate(d["lineas"]):
        nota = f"<small>{md(l['nota'])}</small>" if l.get("nota") else ""
        out += f'<div class="l" data-b="{l.get("beat", base + k)}" data-a="up"><span class="a">{md(l["izq"])}{nota}</span><span class="b">{esc(l["der"])}</span></div>'
    if d.get("resultado"):
        r = d["resultado"]
        out += f'<div class="l res" data-b="{r.get("beat", base + len(d["lineas"]))}" data-a="pop"><span class="a">{md(r["izq"])}</span><span class="b">{esc(r["der"])}</span></div>'
    return out + "</div>"


def t_pregunta(d):
    out = f'<div class="h2 fit" data-b="0" data-a="up">{md(d["pregunta"])}</div><div class="opts">'
    for k, o in enumerate(d["opciones"]):
        ok = k == d["correcta"]
        hl = f'<span style="display:contents" data-b="{d.get("beat_revelar", 2)}" data-a="hl"></span>' if ok else ""
        out += f'<div class="opt{" ok" if ok else ""}" data-b="{d.get("beat_opciones", 1)}" data-a="left" data-delay="{k*0.12:.2f}"><span class="L">{"ABCD"[k]}</span><span>{md(o)}</span></div>'
    out += "</div>"
    if d.get("explicacion"):
        out += f'<div class="p fit" style="max-height:220px" data-b="{d.get("beat_revelar", 2)}" data-a="up" data-delay=".2">{md(d["explicacion"])}</div>'
    return out


def t_timeline(d):
    out = _bloque_titulo(d)
    base = int(d.get("beat_inicio", 0))
    out += '<div class="tl">'
    for k, e in enumerate(d["eventos"]):
        out += f'<div class="ev" data-b="{e.get("beat", base + k)}" data-a="left"><div class="d">{esc(e["fecha"])}</div><div class="x">{md(e["texto"])}</div></div>'
    return out + "</div>"


def t_donut(d):
    segs = d["segmentos"]
    total = sum(float(s["valor"]) for s in segs)
    R, C = 210, 2 * math.pi * 210
    colores = ["var(--ac)", "var(--ac2)", "var(--ok)", "#f2c14e", "#c084fc"]
    base = int(d.get("beat_inicio", 0))
    acc = 0.0
    arcs = []
    for k, s in enumerate(segs):
        frac = float(s["valor"]) / total
        largo = C * frac
        b = s.get("beat", base + k)
        arcs.append(
            f'<circle cx="260" cy="260" r="{R}" fill="none" stroke="{colores[k%5]}" stroke-width="90" '
            f'stroke-dasharray="{largo:.1f} {C:.1f}" stroke-dashoffset="{-acc:.1f}" transform="rotate(-90 260 260)" data-b="{b}" data-a="fade" data-dur=".5"/>'
        )
        acc += largo
    centro = f'<text x="260" y="280" text-anchor="middle" font-size="64" font-weight="800" fill="currentColor" font-family="var(--fh)">{esc(d.get("centro",""))}</text>'
    svg = f'<svg width="520" height="520" viewBox="0 0 520 520" style="color:var(--fg)">{"".join(arcs)}{centro}</svg>'
    leyenda = '<div class="legend">' + "".join(
        f'<div class="it" data-b="{s.get("beat", base + k)}" data-a="left"><i style="background:{colores[k%5]}"></i>{md(s["etiqueta"])}<b>{esc(s.get("texto") or fmt_num(float(s["valor"])))}</b></div>'
        for k, s in enumerate(segs)) + "</div>"
    return _bloque_titulo(d) + f'<div class="donut-wrap"><div data-b="{base}" data-a="pop">{svg}</div>{leyenda}</div>'


def t_cierre(d):
    out = ""
    if d.get("titulo"):
        out += f'<div class="h2 fit" data-b="0" data-a="up">{md(d["titulo"])}</div>'
    if d.get("puntos"):
        out += '<div class="list">' + "".join(
            f'<div class="li" data-b="{d.get("beat_puntos", 0)}" data-a="left" data-delay="{0.15*k:.2f}"><span class="ic ok">✓</span><span class="tx" style="font-size:40px">{md(p)}</span></div>'
            for k, p in enumerate(d["puntos"])) + "</div>"
    if d.get("cta"):
        out += f'<div class="cta" data-b="{d.get("beat_cta", 1)}" data-a="pop">{md(d["cta"])}</div>'
    return out


# ---------------------------------------------------------------- formato CURSO

def _puntos_curso(n: int, total: int) -> str:
    return "".join(f'<i class="{"now" if k == n else ("on" if k < n else "")}"></i>' for k in range(1, total + 1))


def t_curso_portada(d):
    n, total = int(d.get("leccion", 1)), int(d.get("total", 1))
    obj = "".join(
        f'<div class="li" data-b="{d.get("beat_objetivos", 1) + (k if d.get("objetivos_en_beats") else 0)}" data-a="left" data-delay="{0 if d.get("objetivos_en_beats") else 0.15 * k:.2f}">'
        f'<span class="ic ok">✓</span><span class="tx">{md(o)}</span></div>'
        for k, o in enumerate(d.get("objetivos", [])))
    return (f'<div class="cp"><div>'
            f'<div class="kicker" data-b="0" data-a="up">{md(d.get("kicker") or f"Curso gratuito · Lección {n} de {total}")}</div>'
            f'<div class="h1 fit" data-min="54" data-b="0" data-a="up" data-delay=".06">{md(d["titulo"])}</div>'
            f'<div class="meta" data-b="0" data-a="up" data-delay=".12">{md(d.get("curso", ""))} · {md(d.get("modulo", ""))}</div>'
            f'<div class="dots" data-b="0" data-a="fade" data-delay=".2">{_puntos_curso(n, total)}<span>{n}/{total}</span></div>'
            f'</div><div class="card obj" data-b="{d.get("beat_objetivos", 1)}" data-a="right">'
            f'<div class="t">{md(d.get("titulo_objetivos", "En esta lección vas a aprender"))}</div><div class="list">{obj}</div></div></div>')


def t_capitulo(d):
    n, total = int(d.get("n", 1)), int(d.get("total", 1))
    sub = f'<div class="p muted fit" style="max-height:200px" data-b="{d.get("beat_sub", 0)}" data-a="up" data-delay=".25">{md(d["sub"])}</div>' if d.get("sub") else ""
    return (f'<div class="chap"><div class="num" data-b="0" data-a="pop">{n:02d}</div>'
            f'<div class="lab" data-b="0" data-a="up" data-delay=".1">Capítulo {n} de {total}</div>'
            f'<div class="h1 fit" data-min="54" data-b="0" data-a="up" data-delay=".15">{md(d["titulo"])}</div>{sub}'
            f'<div class="bar" data-b="0" data-a="fade"><b style="--w:{100 * n / max(1, total):.1f}%" data-b="0" data-a="grow" data-dur=".9" data-delay=".2"></b></div></div>')


def t_ejercicio(d):
    pasos = ""
    if d.get("pasos"):
        base = int(d.get("beat_pasos", 1))
        pasos = '<div class="steps">' + "".join(
            f'<div class="step" data-b="{base + k}" data-a="left"><span class="n">{k + 1}</span><span class="c">{md(p)}</span></div>'
            for k, p in enumerate(d["pasos"])) + "</div>"
    pista = (f'<div class="card pista" data-b="{d.get("beat_pista", 1)}" data-a="up"><div class="small">Pista</div>'
             f'<div class="p">{md(d["pista"])}</div></div>') if d.get("pista") else ""
    chip = (f'<div class="chip" data-b="0" data-a="up" data-delay=".3">Archivo: {esc(d["material"])}'
            f'{(" · hoja " + esc(d["hoja"])) if d.get("hoja") else ""}</div>') if d.get("material") else ""
    return (f'<div class="ej"><div class="izq"><div><span class="tag" data-b="0" data-a="pop">{esc(d.get("etiqueta", "Ejercicio"))}</span>'
            f'<span class="pausa" data-b="0" data-a="fade" data-delay=".3"><i></i>{esc(d.get("pausa", "Pausa el video y resuélvelo"))}</span></div>'
            f'<div class="h2 fit" data-min="40" data-b="0" data-a="up" data-delay=".1">{md(d["consigna"])}</div>{chip}</div>'
            f'<div class="der">{pasos}{pista}</div></div>')


def t_curso_cierre(d):
    puntos = "".join(
        f'<div class="li" data-b="{d.get("beat_puntos", 0)}" data-a="left" data-delay="{0.15 * k:.2f}"><span class="ic ok">✓</span><span class="tx">{md(p)}</span></div>'
        for k, p in enumerate(d.get("puntos", [])))
    mat = f'<div class="chip" data-b="{d.get("beat_material", 1)}" data-a="up">Material: {esc(d["material"])} (enlace en la descripción)</div>' if d.get("material") else ""
    cta = f'<div class="cta" data-b="{d.get("beat_cta", 1)}" data-a="pop" data-delay=".2">{md(d["cta"])}</div>' if d.get("cta") else ""
    return (f'<div class="cc"><div><div class="h2 fit" data-b="0" data-a="up">{md(d.get("titulo", "Resumen de la lección"))}</div>'
            f'<div class="list" style="margin-top:30px">{puntos}</div></div>'
            f'<div class="side"><div class="card next" data-b="{d.get("beat_siguiente", 1)}" data-a="right"><div class="t">Próxima lección</div>'
            f'<div class="x">{md(d.get("siguiente", ""))}</div></div>{mat}{cta}</div></div>')


PLANTILLAS = {
    "hook": t_hook, "texto": t_texto, "numero": t_numero, "barras": t_barras, "linea": t_linea,
    "planilla": t_planilla, "formula": t_formula, "lista": t_lista, "versus": t_versus, "mito": t_mito,
    "pasos": t_pasos, "prompt": t_prompt, "codigo": t_codigo, "dato": t_dato, "calculo": t_calculo,
    "pregunta": t_pregunta, "timeline": t_timeline, "donut": t_donut, "cierre": t_cierre,
    "curso_portada": t_curso_portada, "capitulo": t_capitulo, "ejercicio": t_ejercicio, "curso_cierre": t_curso_cierre,
}


def pagina(canal, escena_html: str, cabecera: dict, horizontal: bool = False) -> str:
    serie = esc(cabecera.get("serie", ""))
    ep = esc(cabecera.get("episodio", ""))
    marca = esc(cabecera.get("marca", ""))
    if cabecera.get("curso"):
        caps = "".join(f'<i class="{"now" if k == cabecera["cap_n"] else ("on" if k < cabecera["cap_n"] else "")}"></i>'
                       for k in range(1, int(cabecera["cap_total"]) + 1))
        head = (f'<div id="head" class="curso"><span class="pill">Curso · {esc(cabecera["curso"])}</span>'
                f'<span class="mod">Lección {cabecera["leccion"]}/{cabecera["total"]} · Módulo {cabecera["modulo_n"]}</span>'
                f'<span class="caps">{caps}<span>Cap. {cabecera["cap_n"]}/{cabecera["cap_total"]}</span></span></div>')
    else:
        head = f'<div id="head"><span class="pill">{serie or marca}</span><span>{marca if serie else ""}</span><span class="ep">{ep}</span></div>'
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css_base(canal, horizontal)}</style></head>'
            f'<body class="{"h" if horizontal else "v"}"><div id="bg"></div><div id="grid"></div><div id="grain"></div>{head}'
            f'<div id="stage">{escena_html}</div><div id="cap"></div><script>{RUNTIME}</script></body></html>')


def html_escena(canal, visual: dict, cabecera: dict, horizontal: bool = False) -> str:
    tipo = visual["plantilla"]
    if tipo not in PLANTILLAS:
        raise KeyError(f"Plantilla desconocida: {tipo}")
    cab = {**cabecera, **visual.get("_cab", {})}
    return pagina(canal, PLANTILLAS[tipo](visual.get("datos", {})), cab, horizontal)
