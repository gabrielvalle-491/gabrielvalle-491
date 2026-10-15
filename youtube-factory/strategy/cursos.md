# Videos largos en formato CURSO

**Decisión (2026-10-15, a pedido del dueño de los canales):** los 12 videos largos de cada canal dejan de ser guías
sueltas y pasan a ser **un curso gratuito de 12 lecciones**, una por semana, en el mismo horario que tenían los largos
(Atajo IA: martes 19:00; Celda Clara: jueves 19:00, hora de Argentina).

| Canal | Curso | Módulos (4 lecciones cada uno) |
|---|---|---|
| Atajo IA | **IA para tu trabajo, desde cero** (`cursos/canal_a.yaml`) | Fundamentos · IA en el día a día · IA para un negocio |
| Celda Clara | **Excel y Google Sheets desde cero** (`cursos/canal_b.yaml`) | Fundamentos · Organizar y analizar · Proyectos reales |

## Por qué un curso y no guías sueltas

1. **Horas de visualización.** Para entrar al Programa de Socios hacen falta horas de videos largos (ver
   `monetizacion.md`); las vistas de Shorts en el feed no suman horas. Una serie numerada invita a mirar la lección
   siguiente: cada lección termina con la tarjeta "Próxima lección" y la lista de reproducción del curso.
2. **Búsqueda permanente.** "Curso de Excel desde cero" o "curso de IA desde cero" son búsquedas que no caducan,
   a diferencia de las noticias de herramientas.
3. **Puente con los Shorts.** Cada lección amplía temas que los Shorts ya tocaron; los Shorts pueden enlazar a la
   lección relacionada como "video relacionado".
4. **Activo reutilizable.** El temario, los ejercicios y los archivos de práctica son la base de una versión
   ampliada o con certificado en una plataforma de cursos más adelante (decisión tuya; no se contrató nada).

## Qué tiene cada lección (lo controla el validador)

- 16:9, 8-12 min, voz y gráficos de la fábrica, subtítulos y miniatura 1280×720.
- **Portada** con número de lección, módulo, objetivos ("En esta lección vas a aprender…") y barra de progreso del curso.
- **Cabecera de curso** en todas las escenas: curso, lección N/12, módulo y capítulo actual con barra de capítulos.
- **3-5 capítulos** con pantalla de capítulo; sus tiempos reales del render se escriben en la descripción como
  marcas de tiempo (YouTube pide que la primera sea 0:00, al menos tres, en orden y —según guías de terceros— de al
  menos 10 s cada una; la fábrica controla las cuatro cosas).
- **Ejercicio** con "Pausa el video", pasos, pista y **archivo de práctica**; luego la **solución**.
- **Cierre** con repaso, próxima lección y material.
- **Material:** Celda Clara → `.xlsx` con hoja Práctica y hoja Solución; las fórmulas se escriben como en Excel en
  español y se traducen al formato interno del archivo (Excel las muestra en el idioma de cada persona). Si
  LibreOffice está instalado, la fábrica recalcula el archivo y compara cada resultado con el esperado. Las funciones
  que LibreOffice 24.2 no calcula (BUSCARX, FILTRAR, UNICOS, ORDENAR…) quedan marcadas "sin verificar" en lugar de
  aprobarse a ciegas. Atajo IA → `.txt` con los prompts del ejercicio y una lista de control.

## Lo que hay que hacer a mano (una vez por curso o por lección)

1. Crear en YouTube Studio una **lista de reproducción pública** por curso con el nombre del curso. Pegar su enlace
   en `enlace_lista` del temario (aparece en cada descripción). Opcional: activar `publicacion.gestionar_listas` para
   que la API agregue cada lección a la lista (pide un permiso adicional de YouTube; ver `docs/AUTORIZAR_YOUTUBE.md`).
2. Subir el archivo de práctica de cada lección a tu Google Drive con acceso "cualquier persona con el enlace" y
   pegar el enlace en `enlace_material`. **Sin ese enlace la lección no se exporta como lista ni se publica**: queda en
   `PENDIENTES.csv` con el motivo.
3. Los capítulos dependen de que el canal tenga habilitadas las funciones intermedias/avanzadas de YouTube
   (verificación por teléfono). Si no aparecen, revisar eso en Studio.

## YouTube "Cursos" (producto oficial)

YouTube tiene un producto llamado Courses (cursos gratuitos o pagos dentro de YouTube), pero según la cobertura
disponible se lanzó en beta en pocos países (EE. UU., Corea del Sur, India) y para creadores seleccionados; no
encontramos confirmación de que esté disponible en Argentina. Por eso el curso se arma con una **lista de
reproducción** normal. Si más adelante YouTube habilita Courses para el canal, las lecciones ya tienen la estructura.

## Producción

- Escribir: `prompts/guionista_curso.md` (estructura, sincronía, material, fuentes).
- `fabrica.bat validar A-L02` → `fabrica.bat producir A-L02` → `fabrica.bat exportar`.
- `fabrica.bat curso` muestra el temario y el estado de cada lección; `--materiales` regenera y verifica los archivos.
- Estado al 2026-10-15: módulo 1 escrito en ambos canales; lección 1 de cada curso producida y controlada
  (ver `reports/control_final.md` y el PR). Las lecciones 5-12 se escriben con los datos de retención del módulo 1.

## Fuentes

- Capítulos de video (YouTube Help): https://support.google.com/youtube/answer/9884579
- Cuota de la API (playlistItems.insert = 50 unidades): https://developers.google.com/youtube/v3/determine_quota_cost
- Lanzamiento de YouTube Courses en beta (cobertura de prensa, 2022-2023): https://analyticsindiamag.com/youtube-enters-indian-edtech-with-courses/
