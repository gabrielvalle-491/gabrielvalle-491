# Estrategia de videos largos

**Decisión:** un video largo semanal por canal desde la semana 2, es decir, 12 por canal en el trimestre (ver los calendarios).

**Por qué:** las horas de visualización del YPP solo cuentan en videos largos (ver `monetizacion.md`). Los largos además
convierten mejor a suscripción y a afiliados.

**Cómo, sin sacrificar calidad:** cada largo **amplía los Shorts de su pilar** que hayan demostrado interés. Un largo
**no** es una compilación de Shorts: es una guía completa con ejemplos nuevos, el paso a paso entero y una plantilla o
prompt descargable. El formato técnico ya está soportado (16:9, 1920×1080, mismas plantillas y control de calidad,
miniatura de 1280×720).

**Estado:** los temas y las fechas están planificados (`L01`-`L12` en `strategy/calendario_canal_*.csv`). Los guiones
de los largos se escriben **después de ver los datos de los primeros Shorts del pilar**, usando la misma guía
(`prompts/guionista.md`, con 8 a 14 escenas de 40-60 s cada una). Escribir los 24 ahora, sin datos, iría contra el
principio de "producir por aprendizaje".

**Producir un largo:** crear `content/<canal>/<ID>.yaml` con `formato: largo` y ejecutar
`python fabrica.py producir <ID>`.
