# Fábrica de contenido YouTube — Atajo IA + Celda Clara

Sistema automatizado y gratuito para investigar, escribir, narrar, animar, revisar y empaquetar Shorts
originales para **dos canales independientes**. Opera desde Villa Mercedes (San Luis, Argentina) y apunta
a Latinoamérica y la audiencia hispana de EE. UU.

| Canal | Nicho | Tono |
|---|---|---|
| **Atajo IA** (`canal_a`) | IA aplicada y automatización para el trabajo y las pymes | Práctico, sin humo, voz masculina sintética |
| **Celda Clara** (`canal_b`) | Excel y Google Sheets para el trabajo y el dinero (educativo, sin recomendaciones de inversión) | Claro y calmo, voz femenina sintética |

Por qué esos dos nichos: `research/investigacion_nichos.md` (matriz de 12 criterios y 83 fuentes).
Políticas de YouTube, API y licencias: `research/politicas_y_apis.md`.

---

## Instalación (una sola vez, en Windows)
1. Instala **Python 3.11 o superior** desde https://www.python.org/downloads/ (marca "Add python.exe to PATH").
2. Copia la carpeta `youtube-factory` a tu PC, por ejemplo a `Documentos\youtube-factory`. Es una carpeta nueva, separada de tus otros proyectos.
3. Haz doble clic en **`instalar.bat`**. Instala FFmpeg, los paquetes, el navegador interno y el modelo de voz (~350 MB). Al final muestra un diagnóstico.

En Linux o macOS usa `./instalar.sh` y luego `./fabrica.sh <comando>`.

## Uso diario: abre una terminal en la carpeta y usa `fabrica.bat <comando>`

| Quiero... | Comando |
|---|---|
| Revisar que todo funcione | `fabrica.bat diagnostico` |
| Actualizar la investigación de temas | `fabrica.bat investigar` |
| (Re)generar el calendario de 90 días | `fabrica.bat calendario --inicio 2026-10-19` |
| Revisar guiones antes de producir | `fabrica.bat validar` |
| Producir el lote (reanuda donde quedó) | `fabrica.bat producir` o `fabrica.bat producir --canal canal_b --desde 2026-10-19 --hasta 2026-10-31` |
| Producir un video puntual | `fabrica.bat producir B-014` |
| Ver en qué estado está cada video | `fabrica.bat estado --detalle` |
| Volver a controlar la calidad | `fabrica.bat revisar` |
| Regenerar videos con error o en revisión | `fabrica.bat regenerar` |
| Armar el paquete para programar | `fabrica.bat exportar` |
| Conectar un canal con YouTube (opcional) | `fabrica.bat autorizar canal_a` |
| Subir y programar (opcional; simula si no agregas `--confirmar`) | `fabrica.bat publicar canal_a --desde 2026-10-19 --hasta 2026-10-25` |
| Cargar métricas | `fabrica.bat metricas canal_a` (API) o `fabrica.bat metricas canal_a --csv "Datos de la tabla.csv"` (exportación de Studio) |
| Informe semanal | `fabrica.bat informe canal_a` |
| Ver costos | `fabrica.bat costos` |

## Publicar (lo más simple)
1. `fabrica.bat exportar` crea `paquetes/canal_a/` y `paquetes/canal_b/`, con una carpeta por video llamada `AAAA-MM-DD_ID`.
2. Cada carpeta trae el **video**, la **portada**, los **subtítulos (.srt)** y un **`PUBLICAR.txt`**. Ese archivo tiene el título, la descripción con fuentes, las etiquetas, el comentario para fijar, la fecha y hora sugeridas y las casillas que debes marcar en YouTube Studio (incluida la de **contenido sintético**).
3. `PROGRAMACION.csv` lista todo en orden. `PENDIENTES.csv` lista lo que no pasó el control y por qué.
4. En YouTube Studio: **Crear → Subir video**, pega los datos de `PUBLICAR.txt` y en **Visibilidad** elige **Programar** con la fecha indicada.

## Qué garantiza el control de calidad
Ningún video pasa a "aprobado" por el solo hecho de existir. `fabrica.bat revisar` mide y registra:
- **Técnica:** 1080×1920 (o 1920×1080), H.264 yuv420p, 30 fps, AAC 48 kHz estéreo, duración y tamaño.
- **Audio:** volumen ≈ −14 LUFS, pico ≤ −1 dBFS, sin silencios largos y voz completa (velocidad plausible).
- **Imagen:** sin pantallas negras y sin textos desbordados.
- **Subtítulos:** sincronizados, ordenados, legibles e idénticos a la narración.
- **Exactitud:** cada cifra de la narración tiene un cálculo reproducible o una fuente, y los cálculos se recalculan con las mismas fórmulas que Excel (PAGO, VF, VA, NPER, REDONDEAR).
- **Riesgo:** sin promesas ("garantizado", "sin riesgo"), sin recomendaciones de inversión, sin voseo, sin credenciales ni experiencias inventadas.
- **Ortografía:** diccionario Hunspell es más términos del proyecto.
- **Originalidad:** similitud con el resto de la biblioteca por debajo del umbral, título coherente con el contenido, licencias documentadas, declaración de contenido sintético evaluada y metadatos completos.

El puntaje mínimo es 85/100 y no puede haber fallos críticos. Lo que no pasa queda en "revisión", con el motivo exacto en `output/<canal>/metadata/<ID>.qa.json`.

## Cómo está hecho
```
youtube-factory/
├─ fabrica.py / fabrica.bat / instalar.bat      ← comandos
├─ config/        global.yaml · canal_a.yaml · canal_b.yaml  (marca, paleta, voz, horarios, léxico)
├─ research/      investigación, fuentes (CSV), banco de ideas y cola priorizada
├─ strategy/      estrategia por canal, monetización, calendarios de 90 días y lotes
├─ prompts/       guía del guionista (para escribir nuevas tandas con una persona o una IA)
├─ content/       un guion por video (YAML): narración, escenas, fuentes, metadatos
├─ src/fabrica/   módulos: research · planning · specs · fact_check · voice · timeline
│                 visuals (plantillas HTML) · audio · render · subtitles · quality
│                 metadata · publishing · analytics · pipeline · diagnostics · cli
├─ assets/        tipografías OFL, diccionario, música original generada
├─ output/        videos, subtítulos, portadas y metadatos por canal
├─ paquetes/      paquete final para programar (se genera con exportar)
├─ data/          factory.db (estados, eventos, ideas, fuentes, métricas, publicaciones)
├─ reports/       informes semanales y de control final
├─ tests/         pruebas unitarias y de integración (python -m pytest)
└─ docs/          AUTORIZAR_YOUTUBE.md y notas técnicas
```

**Proceso de cada video:**
1. Guion YAML.
2. Validación (ficha, cálculos, cifras, riesgos, ortografía, desbordes).
3. Voz frase por frase con Kokoro-82M local, con caché.
4. Línea de tiempo exacta: los subtítulos y las animaciones se sincronizan con la duración real de cada frase.
5. Escenas HTML dibujadas por Chromium, capturando solo los instantes que cambian.
6. Música y efectos generados por código (licencia propia).
7. Mezcla con compresión lateral y normalización a −14 LUFS en dos pasadas.
8. FFmpeg (H.264 + AAC, faststart).
9. Control de calidad.
10. Exportación.

**Reanudación y errores:** cada etapa queda registrada en `data/factory.db`. Si algo falla, se reintenta 2 veces y luego queda en "error" con el detalle. `producir` saltea lo que ya está hecho y sin cambios (huella del guion). Si editas un guion, solo se vuelve a producir ese video.

## Costos
Todo es local y gratuito: voz, render, música y API de YouTube dentro de la cuota gratuita. **No se contrató ningún servicio.**
`fabrica.bat costos` estima la electricidad: en la prueba, unos 100 s de cómputo por Short, es decir, centavos de dólar por todo el lote.

## Siguientes tandas (después de los 90 días o para reemplazar temas)
1. Agrega ideas en `research/ideas/canal_x.txt`, o importa preguntas de comentarios con la función `importar_ideas_csv`.
2. `fabrica.bat investigar` (prioriza ideas y deduplica) y luego `fabrica.bat calendario --inicio <fecha>`.
3. Escribe los guiones con `prompts/guionista.md`. Puedes pedírselo a un asistente de IA con `prompts/encargo_lote.md`.
4. `fabrica.bat validar`, luego `fabrica.bat producir` y luego `fabrica.bat exportar`.

## Lo que solo tú puedes hacer
1. **Crear los dos canales** (nombres y handles sugeridos en `strategy/canal_*.md`; verifica que estén disponibles).
2. Revisar los videos del paquete y programarlos, o autorizar la API con `docs/AUTORIZAR_YOUTUBE.md`.
3. En YouTube Studio, marcar **"contenido alterado o sintético: Sí"** donde `PUBLICAR.txt` lo indica (voz sintética realista).
4. Postular a programas de afiliados y Hotmart, y cargar **solo enlaces reales aprobados** en `config/canal_*.yaml`.
5. Al activar AdSense: cargar el W-8BEN y consultar a un contador por Factura E y el monotributo.

## Licencias de lo que usa la fábrica
- Kokoro-82M: Apache-2.0. kokoro-onnx: MIT. Usa phonemizer y espeak-ng, que son GPL-3.0; eso no impone licencia a los videos.
- Tipografías: SIL OFL 1.1 (licencias en `assets/fonts/*/LICENSE.txt`).
- Diccionario es: GPL/LGPL/MPL (`assets/diccionario/LICENSE.txt`).
- Playwright: Apache-2.0. FFmpeg con libx264: GPL.
- La música y los efectos los genera el código del proyecto.
