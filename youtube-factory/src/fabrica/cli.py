"""Interfaz de comandos en español. Uso: python fabrica.py <comando> [opciones]"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from .config import cargar_env


def cmd_validar(a):
    from .quality import revisar_guion
    from .specs import buscar_ficha, canal_de, listar_fichas
    from .render import cabecera
    from .visuals.frames import analizar
    fichas = [buscar_ficha(i) for i in a.ids] if a.ids else [f for f in listar_fichas(a.canal) if not f["id"].endswith("TEST")]
    biblioteca = listar_fichas()
    malos = 0
    for spec in fichas:
        inf = revisar_guion(spec, biblioteca)
        fallos = [i for i in inf.items if not i["ok"]]
        desbordes = []
        if not inf.criticos or a.visual:
            try:
                info = analizar(spec, canal_de(spec), cabecera(spec, canal_de(spec)), spec["formato"] == "largo")
                desbordes = [o for i in info for o in i["overflow"]]
            except Exception as e:  # noqa: BLE001
                desbordes = [f"error al dibujar: {e}"]
        estado = "OK" if not inf.criticos and not desbordes else "REVISAR"
        malos += estado != "OK"
        print(f"{spec['id']}: {estado} ({inf.puntaje:.0f}/100)")
        for f in fallos:
            print(f"   - {'CRÍTICO ' if f['critico'] else ''}{f['control']}: {f['detalle'][:300]}")
        for d in desbordes:
            print(f"   - CRÍTICO texto desbordado: {d}")
    print(f"\n{len(fichas) - malos}/{len(fichas)} fichas sin problemas críticos.")
    return 1 if malos else 0


def cmd_producir(a):
    from .pipeline import producir_lote, resumen
    r = producir_lote(ids=a.ids or None, canal=a.canal, desde=a.desde, hasta=a.hasta, forzar=a.forzar,
                      paralelo=a.paralelo, formato=None if a.ids else a.formato)
    print("Resumen:", resumen(r))


def cmd_revisar(a):
    from .quality import evaluar_y_registrar
    from .specs import buscar_ficha, listar_fichas
    fichas = [buscar_ficha(i) for i in a.ids] if a.ids else [f for f in listar_fichas(a.canal) if not f["id"].endswith("TEST")]
    biblioteca = listar_fichas()
    for spec in fichas:
        r = evaluar_y_registrar(spec, biblioteca)
        print(f"{spec['id']}: {r['estado']} ({r['puntaje']:.0f}/100)")
        for m in r["motivos"]:
            print("   -", m[:240])


def cmd_regenerar(a):
    from . import db
    from .pipeline import producir_lote, resumen
    ids = a.ids or [v["id"] for v in db.listar_videos(a.canal) if v["estado"] in ("error", "revision")]
    if not ids:
        print("No hay videos fallidos ni en revisión.")
        return
    r = producir_lote(ids=ids, forzar=True, paralelo=a.paralelo)
    print("Resumen:", resumen(r))


def cmd_estado(a):
    from . import db
    vids = db.listar_videos(a.canal)
    cont = {}
    for v in vids:
        cont[v["estado"]] = cont.get(v["estado"], 0) + 1
    print(json.dumps(cont, ensure_ascii=False, indent=2))
    if a.detalle:
        for v in vids:
            print(f"{v['id']:8} {v['fecha']} {v['estado']:12} {v['qa_puntaje'] or '':>5} {(v['titulo'] or '')[:60]}")


def cmd_investigar(a):
    from .research import actualizar_cola, investigar_api, registrar_fuentes_csv
    cargar_env()
    for c in ([a.canal] if a.canal else ["canal_a", "canal_b"]):
        print(c, investigar_api(c, a.maximo))
        cola = actualizar_cola(c)
        print(f"  cola priorizada: research/cola_ideas_{c}.csv ({len(cola)} ideas). Top 5:")
        for i in cola[:5]:
            print(f"   {i['puntaje']:5.1f}  {i['tema']}")
    print("Fuentes registradas en la base:", registrar_fuentes_csv())


def cmd_calendario(a):
    from .planning import generar
    inicio = date.fromisoformat(a.inicio)
    for c in ([a.canal] if a.canal else ["canal_a", "canal_b"]):
        f = generar(c, inicio, a.dias)
        print(f"{c}: {sum(1 for x in f if x['formato']=='short')} Shorts y {sum(1 for x in f if x['formato']=='largo')} largos → strategy/calendario_{c}.csv")


def cmd_diagnostico(a):
    from .diagnostics import diagnostico
    return diagnostico()


def cmd_iniciar(a):
    from .diagnostics import iniciar
    return iniciar()


def cmd_exportar(a):
    from .metadata import exportar
    exportar(a.canal, a.desde, a.hasta, incluir_revision=a.incluir_revision)


def cmd_autorizar(a):
    from .publishing import autorizar
    cargar_env()
    autorizar(a.canal)


def cmd_publicar(a):
    from .publishing import publicar_lote
    cargar_env()
    publicar_lote(a.canal, a.desde, a.hasta, simular=not a.confirmar, limite=a.limite)


def cmd_metricas(a):
    from .analytics import actualizar_metricas, importar_csv_studio
    cargar_env()
    if a.csv:
        print("Filas importadas:", importar_csv_studio(a.canal, a.csv))
    else:
        actualizar_metricas(a.canal, a.dias)


def cmd_informe(a):
    from .analytics import informe_semanal
    print(informe_semanal(a.canal, a.fin))


def cmd_costos(a):
    from .diagnostics import informe_costos
    print(informe_costos())


def main(argv=None):
    p = argparse.ArgumentParser(prog="fabrica", description="Fábrica de contenido para YouTube (Atajo IA / Celda Clara)")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(nombre, fn, ayuda):
        s = sub.add_parser(nombre, help=ayuda, description=ayuda)
        s.set_defaults(fn=fn)
        return s

    s = add("diagnostico", cmd_diagnostico, "Revisa dependencias, modelos, espacio en disco, permisos y presupuesto")
    s = add("iniciar", cmd_iniciar, "Primera puesta en marcha: descarga el modelo de voz, crea carpetas y la base de datos")
    s = add("investigar", cmd_investigar, "Actualiza la cola priorizada de ideas (y señales públicas si hay YOUTUBE_API_KEY)")
    s.add_argument("--canal"); s.add_argument("--maximo", type=int, default=20)
    s = add("calendario", cmd_calendario, "Genera el calendario de 90 días por canal")
    s.add_argument("--canal"); s.add_argument("--inicio", default="2026-10-19"); s.add_argument("--dias", type=int, default=90)
    s = add("validar", cmd_validar, "Valida guiones (ficha, cálculos, riesgos, ortografía, textos que desbordan) sin renderizar")
    s.add_argument("ids", nargs="*"); s.add_argument("--canal"); s.add_argument("--visual", action="store_true")
    s = add("producir", cmd_producir, "Produce videos (voz, imagen, subtítulos, control de calidad). Reanuda donde quedó")
    s.add_argument("ids", nargs="*"); s.add_argument("--canal"); s.add_argument("--desde"); s.add_argument("--hasta")
    s.add_argument("--formato", default="short"); s.add_argument("--forzar", action="store_true"); s.add_argument("--paralelo", type=int)
    s = add("revisar", cmd_revisar, "Corre de nuevo los controles de calidad sobre videos ya producidos")
    s.add_argument("ids", nargs="*"); s.add_argument("--canal")
    s = add("regenerar", cmd_regenerar, "Vuelve a producir los videos con error o en revisión")
    s.add_argument("ids", nargs="*"); s.add_argument("--canal"); s.add_argument("--paralelo", type=int)
    s = add("estado", cmd_estado, "Muestra cuántos videos hay en cada estado")
    s.add_argument("--canal"); s.add_argument("--detalle", action="store_true")
    s = add("exportar", cmd_exportar, "Arma el paquete de publicación por canal y fecha (solo aprobados)")
    s.add_argument("--canal"); s.add_argument("--desde"); s.add_argument("--hasta"); s.add_argument("--incluir-revision", action="store_true")
    s = add("autorizar", cmd_autorizar, "Conecta un canal con la API oficial de YouTube (flujo OAuth en tu navegador)")
    s.add_argument("canal")
    s = add("publicar", cmd_publicar, "Sube y programa videos aprobados. Por defecto SIMULA; usa --confirmar para subir")
    s.add_argument("canal"); s.add_argument("--desde"); s.add_argument("--hasta"); s.add_argument("--confirmar", action="store_true")
    s.add_argument("--limite", type=int)
    s = add("metricas", cmd_metricas, "Descarga métricas (API de YouTube Analytics) o importa un CSV exportado de YouTube Studio")
    s.add_argument("canal"); s.add_argument("--dias", type=int, default=28); s.add_argument("--csv")
    s = add("informe", cmd_informe, "Genera el informe semanal por canal (qué funcionó, qué no, próximas hipótesis)")
    s.add_argument("canal"); s.add_argument("--fin")
    s = add("costos", cmd_costos, "Informe de costos medidos y estimados")
    a = p.parse_args(argv)
    cargar_env()
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
