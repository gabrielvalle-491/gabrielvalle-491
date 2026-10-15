# Guía para escribir una lección de curso (video largo 16:9)

Complementa `prompts/guionista.md` (principios, marcado, plantillas y fuentes valen igual). Aquí solo
lo que cambia en las lecciones de los cursos de `cursos/canal_a.yaml` y `cursos/canal_b.yaml`.

## 1. Qué es una lección

- Un video horizontal de **5 a 10 minutos** (1 000-1 900 palabras de narración: la voz lee unas 190-200 palabras por minuto; el validador acepta
  800-2 600). Una sola idea central, explicada de cero, con un ejemplo que se construye durante
  el video y **una práctica** que la persona hace con un archivo.
- El temario manda: título, objetivos y orden salen de `cursos/<canal>.yaml`. La ficha solo dice
  `curso: <id del curso>` y usa el mismo `id` de la lección (`A-L02`, `B-L03`…). No copies el título
  ni los objetivos en la portada: se inyectan solos.
- Español neutro con **tú**. Nunca voseo (ni en el comentario fijado).

## 2. Estructura obligatoria (el validador la controla)

1. **`curso_portada`** (primera escena): primera frase = gancho con el resultado de la lección;
   después bienvenida breve y los objetivos dichos en una frase. `datos: {beat_objetivos: N}` con
   N = índice de la frase en la que nombras los objetivos.
2. **3 a 5 capítulos.** Cada capítulo empieza con una escena `capitulo` cuya narración es solo el
   título del capítulo (p. ej. `"Datos y formato."`) y que lleva `capitulo: "Título"` en la escena.
   Los capítulos se convierten en las marcas de tiempo de YouTube (0:00, mínimo 3, ≥ 10 s cada uno).
   La introducción (portada + 1-2 escenas) es el capítulo 0:00 automático.
3. Dentro de cada capítulo, **2 a 4 escenas** de contenido con las plantillas de siempre (planilla,
   fórmula, pasos, versus, lista, mito, prompt, código, cálculo, barras…). Varía las plantillas.
4. Un capítulo final **"Práctica"** con:
   - **`ejercicio`**: `consigna` (≤ 45 caracteres), `pasos` (3-4, ≤ 40 caracteres), opcional `pista`
     y `hoja`. La narración dice qué descargar, qué hacer paso a paso y "Pausa el video…".
   - Una escena de **solución** o de "qué deberías notar".
5. **`curso_cierre`** (última escena): `titulo`, 3 `puntos` de repaso, `cta`. La narración repasa,
   anuncia la próxima lección por su tema y despide ("…nos vemos en la lección N").
   Usa `beat_siguiente` y `beat_cta` para que la tarjeta de próxima lección y el botón aparezcan
   cuando los nombras. La tarjeta "Próxima lección" y el nombre del material se completan solos.

## 3. Sincronía (lo que más se nota en un video largo)

Cada frase (separada por `.`, `?` o `!`) es un beat, empezando en 0. **Antes de cerrar cada escena,
numera sus frases** y ajusta `beat_inicio`, `beat_der`, `beat_veredicto`, `beat_tachar`,
`beat_realidad`, `beat_pasos`, `beat_nota`, `resaltar[].beat`, `resultado.beat` o `beat` por ítem,
para que cada elemento aparezca cuando la voz lo nombra. Error típico: una lista con frase
introductoria ("Tres errores típicos.") necesita `beat_inicio: 1`.

## 4. Pantalla horizontal

- El escenario mide 1 728 × 740 px. Listas y pasos: máximo 4 ítems (con `detalle` corto).
  Planillas: hasta 9 filas y 4 columnas. Versus: máximo 3 ítems por lado.
- Escenas de 15 a 45 s. Si una idea necesita más, divídela en dos escenas con visuales distintos.
- `python fabrica.py validar <ID>` dibuja cada escena y avisa si algo se sale por abajo o por el costado.

## 5. Material de práctica (`materiales:`)

- **Celda Clara:** un `.xlsx` con hoja `Práctica` (datos + celdas vacías donde va la respuesta;
  `instrucciones` en una frase, que se escriben al costado de la tabla) y hoja `Solución` (las fórmulas resueltas). Las fórmulas se escriben
  **como en Excel en español** (`=SUMA(C2:C8)`, `;` entre argumentos, coma decimal): la fábrica las
  traduce al formato interno del archivo y Excel o Sheets las muestran en el idioma de cada persona.
  La tabla siempre empieza en A1, así que las celdas que dice el video son las mismas del archivo.
  En `verificar` pon el valor esperado de cada celda resuelta: la fábrica recalcula el archivo con
  LibreOffice y compara.
  Cada número que la narración dice en voz alta necesita `calculo` en `fuentes` (como en los Shorts).
- **Atajo IA:** un `.txt` (`tipo: texto`) con los prompts del ejercicio listos para copiar,
  variables en `[CORCHETES]`, la advertencia de no pegar datos personales y una lista de control.
- Nombre: `LeccionNN_practica.xlsx` / `LeccionNN_prompts.txt`.
- El enlace público lo agrega el usuario en `cursos/<canal>.yaml` (`enlace_material`) después de
  subir el archivo a su Drive. Mientras falte, la lección no se publica (queda en PENDIENTES).

## 6. Fuentes y exactitud

Igual que en los Shorts: cada afirmación verificable con `url` oficial (soporte de Microsoft o
Google, centros de ayuda de OpenAI, Google, Anthropic o Microsoft), cada cifra > 10 respaldada,
ejemplos con datos ficticios declarados. Nada de funciones de productos que no puedas respaldar con
una fuente de este año. Si un dato depende de la versión o del plan, dilo ("en Microsoft 365").

## 7. Lista de control de la lección

- [ ] `curso_portada` primero, `curso_cierre` último, `ejercicio` presente, 3-5 capítulos.
- [ ] 1 000-1 900 palabras; escenas de 15-45 s; plantillas variadas.
- [ ] Beats revisados frase por frase.
- [ ] Material con `verificar` (xlsx) o prompts listos (txt).
- [ ] Sin voseo, sin promesas, sin datos inventados; fuentes con `respalda`.
- [ ] `python fabrica.py validar <ID>` → OK sin críticos.
