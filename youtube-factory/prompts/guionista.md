# Guía del guionista — Fábrica de contenido (Atajo IA / Celda Clara)

Esta guía define cómo se escribe cada ficha de video (`content/<canal>/<ID>.yaml`). La usa una
persona o un asistente de IA para producir nuevas tandas. Toda ficha se valida con
`python fabrica.py validar <ID>` antes de producirse.

## 1. Principios no negociables

1. **Valor original y concreto.** Cada Short enseña UNA cosa útil con un ejemplo específico y
   un resultado verificable. Nada de listas genéricas ni relleno.
2. **Español latinoamericano neutro con "tú".** Nunca voseo (tenés, podés, guardalo, mirá...).
   Evitar modismos locales salvo en ideas marcadas para un país.
3. **Cero invenciones.** No inventar estadísticas, testimonios, casos de éxito, credenciales
   ni experiencias personales ("en mi experiencia", "yo uso..."). El narrador no se presenta
   como persona ni como experto humano.
4. **Toda cifra mayor que 10 en la narración** debe estar respaldada por:
   - un `calculo` reproducible (expresión Python con `resultado`), o
   - una fuente con `url` real + campo `cifras` con esos números.
   Solo se citan URL que hayas visto realmente en resultados de búsqueda o documentación
   oficial. Si no puedes verificar algo, no lo afirmes: reformula o elimínalo.
5. **Riesgo financiero (Celda Clara):** educación general. Prohibido recomendar inversiones,
   productos financieros concretos, prometer rendimientos o decir "garantizado"/"sin riesgo".
   Las tasas de los ejemplos se declaran "ilustrativas".
6. **IA (Atajo IA):** no mostrar como real una respuesta que nadie generó. Si muestras una
   respuesta, debe haber sido generada de verdad por un asistente y rotularse "Respuesta de
   ejemplo generada con IA" (y aun así, la recomendación es verificar). Preferir mostrar el
   prompt y explicar qué revisar en la salida. Funciones de productos: solo las documentadas
   oficialmente, con "a la fecha" cuando puedan cambiar. Nunca inventar botones o menús.
7. **Clickbait honesto.** El título y el gancho prometen exactamente lo que el video entrega.
8. **Sin marcas ajenas como protagonistas visuales.** Se nombran productos cuando hace falta,
   pero no se usan logotipos (las plantillas no los incluyen).

## 2. Estructura de un Short

| Bloque | Duración | Qué hace |
|---|---|---|
| Gancho (escena 1) | 1-3 s | Pregunta, resultado, error o contraste. Primera frase ≤ 12 palabras ideal, ≤ 18 máx. La escena 1 es también la portada: debe entenderse sin audio. |
| Contexto/promesa | 2-5 s | Qué vas a aprender y por qué importa. Puede ir en la escena 1 o 2. |
| Desarrollo | 15-40 s | 2-4 escenas; cada una agrega información NUEVA (dato, paso, demostración). |
| Resolución | 3-8 s | Resultado concreto o regla práctica. |
| Cierre | 1-4 s | CTA breve y natural solo si aporta (guardar, probar, comentar algo específico). |

- Duración objetivo: la del calendario (`corta` 55-80 palabras, `media` 85-140). Nunca > 170.
- 4 a 6 escenas por Short. Varía el orden y las plantillas: no uses siempre hook → lista → cierre.
- Prohibido: saludos ("hola a todos"), presentación del canal, "en este video", "no olvides
  suscribirte" largo, conclusiones que repiten todo.

## 3. Sincronía voz ↔ imagen (importante)

La narración de cada escena se divide en frases (por `.`, `?`, `!`). **El elemento N de la
plantilla aparece cuando empieza la frase N** (beat N, empezando en 0).

- Listas, pasos, barras, cálculos, líneas de tiempo: escribe una frase por ítem, en el mismo
  orden. El título de la escena aparece junto con el primer ítem.
- `versus`: frase 1 → lado izquierdo, frase 2 → lado derecho, frase 3 → veredicto.
- `mito`: frase 1 → mito; frase 2 → se tacha y aparece la realidad.
- `pregunta`: frase 1 → pregunta, frase 2 → opciones, frase 3 → respuesta correcta + explicación.
- `planilla`: frase 1 → planilla + fórmula escribiéndose; frase 2 → rangos resaltados
  (`resaltar[0]` usa beat 1 por defecto); frase 3 → resultado (`resultado.beat`, por defecto 2).
- `formula`: frase 1 → fórmula; frases siguientes → cada parte explicada.
- Si una escena tiene más elementos que frases, los que sobran se reparten en la última frase.
- Puedes forzar con `beats_frase: [0, 0, 1, 2]` (índice de frase para cada beat).

## 4. Marcado de texto

- `*palabra*` → resaltada en color de acento (subtítulos y textos en pantalla). Úsalo con
  moderación: 1-3 por escena, en la palabra clave.
- `[[texto hablado|texto en pantalla]]` → para que la voz diga una cosa y el subtítulo muestre
  otra. Ej.: `[[buscar equis|BUSCARX]]`, `[[A dos|A2]]`.
- Cifras en la narración: escríbelas con espacio fino para miles (`1 500`), coma decimal (`3,5`),
  `%` y `US$` cuando es dólar. La fábrica las convierte a palabras para la voz.
- Nombres de funciones de Excel en mayúsculas (`BUSCARX`, `SUMAR.SI.CONJUNTO`): el léxico del
  canal define su pronunciación. Si aparece una nueva, agrega `[[pronunciación|FUNCIÓN]]`.
- Celdas en la narración: escríbelas como se dicen (`la celda B dos`) o con `[[be dos|B2]]`.

## 5. Plantillas visuales disponibles (`visual.plantilla` y `visual.datos`)

Todos los textos admiten `*resaltado*`. Campos entre paréntesis son opcionales.

| Plantilla | Datos |
|---|---|
| `hook` | `titulo`, (`kicker`), (`sub`), (`numero`: {`valor`, `prefijo`, `sufijo`, `decimales`, `desde`}) — `beat_sub`/`beat_numero` por defecto 1 |
| `texto` | `texto`, (`titulo`), (`kicker`), (`nota`) |
| `numero` | `valor`, (`prefijo`, `sufijo`, `decimales`, `desde`), (`antes`), (`etiqueta`), (`nota`) — contador animado |
| `barras` | `items`: [{`etiqueta`, `valor`, (`texto`), (`destacado`), (`tenue`)}], (`titulo`), (`prefijo`, `sufijo`, `decimales`), (`maximo`), (`nota`), (`todas_juntas`) |
| `linea` | `series`: [{`nombre`, `valores`: [números], (`etiqueta_final`)}], (`etiquetas_x`), (`titulo`), (`prefijo`, `sufijo_eje`, `decimales`), (`nota`), (`minimo`, `maximo`) |
| `planilla` | `filas`: [[celdas]] (fila 1 = encabezados), (`formula`), (`celda_formula`), (`resaltar`: [{`rango`: "B2:B5", (`beat`), (`alterno`)}]), (`resultado`: {`celda`, `valor`, (`beat`)}), (`decimales`: int o lista por columna), (`titulo`), (`nota`) |
| `formula` | `formula` (texto exacto, p. ej. `=BUSCARX(A2;D:D;E:E)`), `partes`: [{`token`, `explica`}], (`titulo`), (`nota`) |
| `lista` | `items`: [texto o {`texto`, (`detalle`), (`estilo`)}], (`estilo`: num/check/x), (`titulo`), (`kicker`) |
| `versus` | `izq`/`der`: {`titulo`, `items`: [...], (`etiqueta`)}, (`veredicto`), (`titulo`) |
| `mito` | `mito`, `realidad`, (`fuente`) |
| `pasos` | `pasos`: [texto o {`titulo`, (`detalle`)}], (`titulo`) |
| `prompt` | `texto` (los `[CORCHETES]` se resaltan como variables), (`etiqueta`), (`titulo`), (`nota`) |
| `codigo` | `codigo`, (`lenguaje`), (`titulo`), (`nota`) |
| `dato` | `dato`, (`contexto`), (`fuente`), (`kicker`) |
| `calculo` | `lineas`: [{`izq`, `der`, (`nota`)}], (`resultado`: {`izq`, `der`}), (`titulo`) |
| `pregunta` | `pregunta`, `opciones` (2-4), `correcta` (índice desde 0), (`explicacion`) |
| `timeline` | `eventos`: [{`fecha`, `texto`}], (`titulo`) |
| `donut` | `segmentos`: [{`etiqueta`, `valor`, (`texto`)}], (`centro`), (`titulo`) |
| `cierre` | (`titulo`), (`puntos`: [...]), (`cta`) |

Límites prácticos de texto en pantalla (vertical): títulos ≤ 45 caracteres; ítems de lista
≤ 40; filas de planilla ≤ 6 y columnas ≤ 4 (celdas ≤ 14 caracteres); prompts ≤ 260 caracteres;
código ≤ 10 líneas de ≤ 34 caracteres. El validador avisa si algo desborda.

**Celda Clara:** las fórmulas usan `;` como separador de argumentos y coma decimal. Las
celdas numéricas se cargan como números (no texto). Si la planilla muestra un resultado,
ese resultado debe estar respaldado con un `calculo`.

## 6. Esquema de la ficha (YAML)

```yaml
id: B-001
canal: canal_b
fecha: 2026-10-19
formato: short
serie: Tu dinero en una planilla
episodio: "#01"               # opcional, aparece arriba a la derecha
pilar: dinero
tipo_editorial: contraintuitivo   # tutorial|error_comun|comparacion|experimento|caso_practico|contraintuitivo|mito|historia|herramienta|serie_episodica|quiz
idea: "Una frase con la idea central"
objetivo: "Qué debe lograr el video (aprendizaje + objetivo de canal)"
publico: "Persona concreta que lo necesita"
hipotesis: "Copiar del calendario"
gancho: "Primera frase exacta"
duracion_objetivo: "35-55 s"
titulo: "Título principal (≤ 70 caracteres ideal, máx. 100)"
titulos_alternativos: ["Variante 1", "Variante 2", "Variante 3"]
criterio_titulo: "Por qué se eligió el principal (claridad, palabra clave, curiosidad legítima)"
descripcion: |
  2-4 líneas: qué se aprende + contexto. Sin promesas exageradas.
cta: "Llamada a la acción breve"
comentario_fijado: "Pregunta o recurso útil para fijar (opcional)"
hashtags: ["#Excel", "#FinanzasPersonales"]   # 2-4, pertinentes
palabras_clave: ["presupuesto", "planilla de gastos"]
escenas:
  - narracion: "Frase 1. Frase 2."
    visual:
      plantilla: hook
      datos: {titulo: "...", kicker: "..."}
    edicion: "Indicación breve opcional (ritmo, énfasis)"
fuentes:
  - url: "https://support.microsoft.com/..."       # solo URLs vistas realmente
    titulo: "Nombre de la página"
    fecha_consulta: 2026-10-11
    respalda: "Qué afirmación respalda"
    cifras: [16]                                    # números de la narración que respalda
  - calculo: "round(1000*1.07**10, 2)"             # Python seguro: + - * / ** round abs min max sum log exp sqrt REDONDEAR PAGO VF VA NPER
    resultado: 1967.15
    respalda: "Saldo tras 10 años al 7 %"
riesgos:
  derechos: "bajo — todo el material visual es generado por el canal"
  exactitud: "medio — ..."
  monetizacion: "bajo — ..."
recursos:
  - nombre: "Música de fondo original generada por la fábrica"
    licencia: "propia"
declaracion_sintetica:
  decision: "declarar"        # declarar | no_requerida | revisar
  motivo: "Voz sintética realista; gráficos no realistas. Se declara por prudencia."
costo_estimado_usd: 0
palabras_validas: []           # términos correctos que el diccionario no conoce
```

## 7. Lista de control antes de entregar una ficha

- [ ] La primera frase engancha y la escena 1 se entiende sin audio.
- [ ] Cada escena agrega información nueva; no hay frases de relleno.
- [ ] Cada cifra > 10 tiene cálculo o fuente con `cifras`.
- [ ] Sin voseo, sin promesas, sin experiencias inventadas, sin recomendaciones de inversión.
- [ ] Título = lo que el video entrega; tres alternativas con ángulos distintos.
- [ ] Hashtags 2-4; descripción breve y útil.
- [ ] `python fabrica.py validar <ID>` sin errores críticos.
