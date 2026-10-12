# Políticas de YouTube, APIs y licencias para la fábrica de Shorts

Fecha de consulta de todas las fuentes: **2026-10-11**.
Tabla de fuentes con IDs: `research/fuentes_politicas.csv`. Los IDs `[Pxx]` de este documento remiten a ella.

## Cómo se obtuvieron los datos (leer antes de usarlos)

- **No se pudo leer directamente ninguna página de `support.google.com`, `developers.google.com`, `blog.youtube`, `huggingface.co`, `ffmpeg.org` ni `fonts.google.com`.** WebFetch devolvió `getaddrinfo ENOTFOUND`, y `curl` a través del proxy de salida recibió `CONNECT tunnel failed, response 403`, es decir, la política de red de la organización lo bloquea.
- Por eso, en las secciones A, B y C los datos vienen de la **herramienta de búsqueda web** con filtro de dominio a los sitios oficiales. La herramienta devuelve extractos de esas páginas indexadas y un resumen. Lo que aparece "entre comillas" son **extractos devueltos por el buscador**, no copias que se hayan comprobado en la página en vivo. Antes de tomar una decisión de cumplimiento, alguien debe abrir la URL y comparar el texto.
- En la sección D, los archivos de licencia (`LICENSE`, `COPYING`, `README`, `pyproject.toml`) se descargaron **literalmente** de `raw.githubusercontent.com`, que sí era accesible. Son la fuente primaria oficial de cada repositorio. Las fichas de modelo (model cards) de Hugging Face no se pudieron abrir y se leyeron mediante el buscador.
- **Corrección a la petición original:** `support.google.com/youtube/answer/12504220` **no** es la página de contenido alterado o sintético. Es **"YouTube Shorts monetization policies"**. La página de divulgación de IA es **`answer/14328491`**, que hoy se titula **"Disclosing use of GenAI content"** y antes se llamaba "Disclosing use of altered or synthetic content".

---

## A. Políticas de monetización y contenido de YouTube

### A1. Contenido no auténtico (antes "contenido repetitivo") [P01]
- **URL:** https://support.google.com/youtube/answer/1311392 · consultada el 2026-10-11
- **Regla observada:**
  - El **15 de julio de 2025**, la política "repetitious content" se amplió ligeramente y pasó a llamarse **"inauthentic content"**, *"to better clarify this includes content that is repetitive or mass-produced"*.
  - YouTube dice que ese contenido *"has always been ineligible for monetization"*. No se trata de una restricción nueva.
  - La evaluación se hace **a nivel de canal**: si hay muchos vídeos que incumplen, se puede retirar la monetización de todo el canal.
  - Criterio: el espectador medio tiene que poder distinguir claramente un vídeo de otro. Compartir un formato está permitido, pero *"the substance of each video should be materially varied"*.
  - Se señala como infracción el contenido que parece *"produced using a template and that can be replicated at scale"*, incluido *"AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective"*.
  - Usar IA no es motivo de exclusión por sí mismo: los canales que usan IA pueden monetizar si cumplen las políticas.
- **Implicación práctica:** este es **el riesgo número 1** para una fábrica de Shorts con plantilla. Cada pieza debe aportar un **dato, ángulo o análisis distinto y verificable**, y el guion no puede ser solo una plantilla con variables cambiadas. Conviene variar la estructura visual y narrativa y añadir una perspectiva editorial propia. No hay que publicar en masa variaciones casi idénticas.

### A2. Contenido reutilizado [P01, P19]
- **URL:** https://support.google.com/youtube/answer/1311392 · 2026-10-11
- **Regla observada:**
  - La política **no cambió** en julio de 2025. Cubre comentarios, clips, compilaciones y reacciones.
  - No es monetizable el contenido que *"exclusively features readings of other materials you did not originally create, like text from websites or news feeds"*.
  - Sí es monetizable cuando hay comentario crítico, una aportación propia o una edición sustancial.
  - La política se aplica *"even if you have permission from the original creator"*.
- **Implicación práctica:** **no se pueden leer con TTS noticias ni artículos ajenos tal cual.** El guion tiene que ser una redacción original que sintetice varias fuentes y aporte contexto o interpretación. Las fuentes se citan, pero no se copian.

### A3. Personajes de IA que se presentan como expertos humanos (finanzas, salud, legal, política) [P01]
- **URL:** https://support.google.com/youtube/answer/1311392 · 2026-10-11
- **Regla observada:**
  - No se permite monetizar contenido de IA que *"presents itself as a human expert providing advice to viewers on topics such as health, legal issues, finances or politics"*. Los canales que lo suban *"will not be allowed to monetise"*.
  - Entre los ejemplos aparecen *"AI-generated podcast hosts offering financial guidance, investment tips, or wealth management advice"*. La lista no es exhaustiva.
- **Implicación práctica (crítica si el nicho es de finanzas):**
  - La voz TTS **no debe presentarse como un "asesor", "experto" o persona humana**.
  - Hay que usar un formato **informativo o educativo de datos** ("qué es la inflación", "cómo se calcula X"), **no consejos de inversión personalizados**, y añadir el aviso "contenido informativo, no es asesoramiento financiero".
  - No se debe crear un avatar humano ficticio con credenciales.

### A4. Divulgación de contenido alterado o sintético (GenAI) [P02, P03, P04]
- **URL:** https://support.google.com/youtube/answer/14328491 (la `12504220` indicada era incorrecta) · 2026-10-11
- **Cuándo hay que divulgar (según los extractos):** contenido generado o alterado de forma significativa con IA **que parezca realista**, por ejemplo cuando:
  - *"Makes a real person appear to say or do something they didn't do"*
  - *"Alters footage of a real event or place"*
  - *"Generates a realistic scene that didn't actually occur"*
  - Otros ejemplos citados: hacer que parezca que alguien dio un consejo que no dio, y la **música generada con IA** (sobre todo si es el foco del vídeo).
- **Cuándo NO hace falta (según los extractos):**
  - Contenido **claramente irreal**: un unicornio, alguien flotando en el espacio con croma, o una animación de misil generada con IA dentro de un vídeo totalmente animado.
  - **Ediciones menores**: filtros de belleza, filtros de color o iluminación, desenfoque de fondo, mejora de audio grabado previamente.
  - **Asistencia de producción**: IA para *outline*, **guion**, **miniatura**, **título**, **infografía**, generación de ideas, subtítulos, *upscaling*, reparación de voz o audio, y *"cloning one's own voice to create voice overs or dubs"*.
  - El blog oficial [P03] añade: *"We won't require creators to disclose if generative AI was used for productivity, like generating scripts, content ideas, or automatic captions."*
- **Narración TTS genérica:** la página **no menciona la "narración TTS" por su nombre** en ningún extracto obtenido.
  - La regla se basa en el **realismo** y en si hace que **una persona real** parezca decir algo que no dijo.
  - Una voz sintética genérica que narra hechos reales sobre gráficos generados (barras, mapas, tipografía) **no aparece en la lista de casos obligatorios**. Los gráficos e infografías generados figuran explícitamente como exentos.
  - Esto es una **interpretación**, no una frase literal de la política.
  - **Nunca** se debe clonar o imitar la voz de una persona real ni generar imágenes realistas de personas o sucesos reales.
- **Cómo se divulga:**
  - En Studio, durante la subida, se marca "Sí" en "AI use" / "Altered content".
  - Por API, con el campo `status.containsSyntheticMedia` (ver B6).
  - La divulgación *"won't limit a video's audience or impact its eligibility to earn money"*.
  - Si no se divulga de forma reiterada, YouTube puede aplicar la etiqueta manualmente o imponer penalizaciones.
- **Etiquetado automático (desde mayo de 2026) [P04]:** si el creador no divulga y los sistemas de YouTube detectan *"significant photorealistic AI use"*, YouTube aplica la etiqueta automáticamente. El creador puede corregirla en Studio.
- **Implicación práctica:**
  - La fábrica debe registrar en los metadatos de cada vídeo qué activos son de IA y si alguno es **fotorrealista**.
  - Por defecto: si hay **solo TTS genérico + gráficos o animación no realistas**, `containsSyntheticMedia=false`. Si hay **cualquier imagen o vídeo fotorrealista generado, o música generada como foco**, `containsSyntheticMedia=true`.
  - Ante la duda, conviene divulgar, porque no penaliza el alcance ni la monetización.

### A5. Requisitos de acceso al YPP [P05, P06]
- **URL:** https://support.google.com/youtube/answer/72851 y https://support.google.com/youtube/answer/12843009 · 2026-10-11
- **Regla observada (vigente hoy):**
  - **YPP estándar:** 1.000 suscriptores y además **4.000 horas de visualización públicas válidas en 12 meses** o **10 millones de vistas válidas de Shorts en 90 días**. Las horas de Shorts vistas en el feed de Shorts no cuentan para las 4.000 horas.
  - **YPP ampliado (fan funding y Shopping):** 500 suscriptores, 3 subidas públicas en 90 días, y 3.000 horas en 12 meses o 3 millones de vistas de Shorts en 90 días.
  - Otros requisitos: cuenta de AdSense vinculada, verificación en dos pasos y cumplir las políticas.
- **Cambio anunciado para el 1 de febrero de 2027 [P06, P07]:**
  - Los **nuevos** creadores necesitarán 1.000 suscriptores y además **8.000 horas en 365 días** o **20 millones de vistas de Shorts en 90 días**. Quien ya esté en el YPP no se ve afectado.
  - Los creadores deberán aceptar los términos actualizados antes del 31 de enero de 2027.
- **Implicación práctica:** el objetivo de vistas de Shorts debe planificarse con los umbrales de 2027 si el canal no entra en el YPP antes del 1 de febrero de 2027.

### A6. Reparto de ingresos de Shorts [P07]
- **URL:** https://support.google.com/youtube/answer/12504220 · 2026-10-11
- **Regla observada:**
  - Los ingresos por anuncios entre Shorts del feed se agrupan cada mes en un fondo que se usa para pagar a creadores y licencias musicales.
  - Si el Short usa música de socios, una parte va a música según el número de pistas.
  - El creador monetizado **conserva el 45 % de lo que se le asigna**, use música o no.
- **Desde el 1 de febrero de 2027:**
  - Para cobrar cada mes del *Shorts Creator Pool* hará falta mantener **10 millones de vistas válidas de Shorts en los 90 días anteriores** (periodo que termina el día 15 del mes previo). Si no se alcanza, el canal **no sale del YPP**.
  - Habrá anuncios dirigidos con un 45 % directo y Premium al 45 %.
- **Implicación práctica:**
  - **Evitar música de socios en los Shorts** (usar música propia o libre sin Content ID), porque reduce la parte del fondo que corresponde a ese Short.
  - El modelo de ingresos de un canal pequeño solo de Shorts es débil a partir de 2027. Conviene combinarlo con vídeos largos o afiliación.

### A7. Duración y formato de los Shorts [P08, P09, P10, P41]
- **URL:** https://support.google.com/youtube/answer/15424877 y el blog *"Tall updates coming to Shorts"* · 2026-10-11
- **Regla observada:**
  - Desde el 15 de octubre de 2024 se pueden subir Shorts de **hasta 3 minutos** con relación de aspecto **cuadrada o vertical**.
  - Para los vídeos subidos **desde el 8 de diciembre de 2025**, todo vídeo cuadrado o vertical de ≤3 min **se clasifica como Short** (antes había una excepción para algunos canales de música). Para que no sea Short hay que usar una relación más ancha, como 16:9.
  - Resolución: la ayuda de Shorts habla de un **máximo de 1080p**. La cifra 1080×1920 (9:16) aparece solo en la documentación de Google Ads [P10], no en la ayuda de YouTube.
  - Miniatura de Shorts: 9:16, recomendada **2160×3840**, mínimo 640 px de alto. En escritorio se admiten JPG/PNG de hasta 50 MB. Subir una miniatura personalizada de Short es posible **solo desde YouTube Studio en ordenador** y con la cuenta verificada.
- **Implicación práctica:** renderizar en **1080×1920, 9:16, entre 20 y 60 s** (≤180 s como límite duro). Validar automáticamente que la duración sea ≤179 s y la relación 9:16.

### A8. Codificación recomendada para subidas [P11]
- **URL:** https://support.google.com/youtube/answer/1722171 · 2026-10-11
- **Regla observada:**
  - Contenedor **MP4** con el *moov atom* al principio (*faststart*) y sin *edit lists*.
  - Vídeo **H.264 High Profile**, progresivo, CABAC, 4:2:0, VBR, sin límite de bitrate. Referencia SDR 1080p: **8 Mbps** a 24/25/30 fps y **12 Mbps** a 48/50/60 fps.
  - Mantener la tasa de fotogramas original y desentrelazar si hace falta.
  - Audio **AAC-LC** (u Opus) a **48 kHz**: 384 kbps en estéreo, 128 kbps en mono.
- **Implicación práctica:**
  - FFmpeg: `-c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 -b:v 8M -maxrate 10M -bufsize 16M -c:a aac -ar 48000 -b:a 384k -movflags +faststart`.
  - Advertencia: `libx264` es GPL y su uso obliga a que el FFmpeg resultante sea GPL (ver D7).

### A9. Pautas para anunciantes (advertiser-friendly) [P12]
- **URL:** https://support.google.com/youtube/answer/6162278 · 2026-10-11
- **Regla observada:**
  - Hay tres resultados posibles: ingresos por anuncios completos, limitados ("icono amarillo") o sin ingresos.
  - El creador rellena un cuestionario de autocertificación en "Ad suitability" al subir el vídeo. Si lo hace con precisión de forma constante, YouTube confía más en su valoración que en los sistemas automáticos. Las inexactitudes graves y repetidas pueden llevar a revisar la elegibilidad en el YPP.
  - Se mencionan actualizaciones de marzo de 2026 (contenido impactante) y octubre de 2026 (contenido de interés público). No se verificaron en detalle.
- **Implicación práctica:**
  - La autocertificación **solo existe en Studio**; no se encontró documentación de un campo equivalente en la Data API. **La hace el humano.**
  - Hay que evitar lenguaje sensacionalista sobre catástrofes financieras, imágenes impactantes y palabrotas.

### A10. Temas financieros (YMYL), estafas y prácticas engañosas [P13, P14, P15]
- **URL:** https://support.google.com/youtube/answer/2801973 y https://support.google.com/youtube/answer/9229980 · 2026-10-11
- **Regla observada:**
  - Está prohibido promocionar esquemas para hacerse rico rápido, promesas de ganancias exageradas o pagos concretos, esquemas piramidales o de *cash gifting*, y "garantizar rendimientos".
  - **Metadatos engañosos:** no se permiten títulos, miniaturas o descripciones *"to trick users into believing the content is something it is not"*, ni que anuncien algo que el vídeo no muestra. Ejemplo: una miniatura con un famoso que no aparece en el vídeo.
  - Una miniatura que infringe se elimina y puede acarrear un *strike*. La primera infracción suele quedarse en advertencia.
  - La política de spam prohíbe además usar herramientas automatizadas o IA para producir en masa contenido similar con cambios mínimos.
  - Los revisores del YPP examinan el título, la miniatura y la descripción.
- **Implicación práctica:**
  - Un validador automático de títulos y miniaturas debe asegurar que **todo lo que se promete aparece en el vídeo**, y bloquear las palabras "garantizado", "seguro", "hazte rico" y los porcentajes de rentabilidad prometidos.
  - No usar caras de personas reales.

### A11. Promoción pagada y afiliación [P16, P17]
- **URL:** https://support.google.com/youtube/answer/154235 y https://support.google.com/youtube/answer/17596007 · 2026-10-11
- **Regla observada:**
  - Si el vídeo contiene contenido de marca, patrocinio, *product placement* o recomendación pagada, hay que marcar en Studio la casilla *"My video contains paid promotion like a product placement, sponsorship, or endorsement"*. YouTube muestra entonces un aviso durante 10 s al principio del vídeo.
  - Si no se declara, el contenido puede eliminarse.
  - El creador y la marca son responsables de cumplir la ley local (FTC o su equivalente).
  - **No se encontró ninguna regla oficial que diga explícitamente que un enlace de afiliado, por sí solo, obliga a marcar la casilla.** La definición incluye "otras relaciones comerciales". La guía del programa de afiliados de Shopping remite a las políticas de contenido de marca y a la guía de la FTC o equivalente.
- **Implicación práctica:**
  - Si hay enlaces de afiliado, poner en la descripción un **aviso explícito de afiliación**.
  - Si existe un acuerdo con una marca, como producto gratis o pago, **el humano marca la casilla de promoción pagada** (por API se recomienda verificar manualmente; no se encontró un campo documentado en los extractos).

### A12. Biblioteca de audio de YouTube [P18]
- **URL:** https://support.google.com/youtube/answer/3376882 · 2026-10-11
- **Regla observada:**
  - La biblioteca está en YouTube Studio.
  - Las pistas con licencia **Creative Commons** obligan a acreditar al artista en la descripción; YouTube ofrece un texto para copiar.
  - Las pistas con licencia estándar no requieren atribución.
  - Según los extractos de los términos, la música es para usarla en vídeos propios, que se pueden monetizar en YouTube. No se puede distribuir la música de forma independiente.
  - No se encontró una regla explícita sobre el uso en otras plataformas.
- **Implicación práctica:**
  - Guardar el ID de la pista y su tipo de licencia en el manifiesto del vídeo.
  - Si la pista es CC, insertar automáticamente la atribución en la descripción.
  - La descarga tiene que hacerla el humano desde Studio, porque no hay API.

---

## B. YouTube Data API v3

### B1. Coste de cuota de `videos.insert` (hay contradicciones) [P20, P21, P22]
- **URLs:** https://developers.google.com/youtube/v3/determine_quota_cost, https://developers.google.com/youtube/v3/docs/videos/insert, https://developers.google.com/youtube/v3/revision_history · 2026-10-11
- **Regla observada:**
  - **Historial de revisiones, 4 de diciembre de 2025:** la documentación y la calculadora se actualizaron para reflejar que el coste de subir un vídeo pasa *"from approximately 1600 units to approximately 100 units"*.
  - **Historial de revisiones, 1 de junio de 2026:** se introducen cubos de cuota granulares, empezando por `videos.insert` y `search.list`. *"API calls to the videos.insert and search.list methods will be charged to their own respective quota buckets. API calls to all other methods will be charged to the existing quota bucket."*
  - **Referencia de `videos.insert` (actual):** *"A call to this method has a quota cost of 1 unit in the Video Uploads quota bucket"*, con un límite por defecto de **100 llamadas al día**.
  - **Contradicción:** según el buscador, algún fragmento de la calculadora sigue mencionando "1600". No se pudo abrir la página en vivo.
- **Implicación práctica:**
  - Con la documentación vigente, la fábrica puede subir **hasta unos 100 vídeos al día por proyecto** con la cuota por defecto, en un cubo separado.
  - El resto de llamadas (`thumbnails.set`, `videos.update`, `captions.insert`, `playlistItems.insert`) gasta los 10.000 unidades diarias compartidas.
  - Hay que **verificar en Google Cloud Console → APIs → YouTube Data API v3 → Quotas** qué cubos tiene realmente el proyecto.
  - Escenario conservador (modelo antiguo de 1600 por subida): unas 6 subidas al día.

### B2. Cuota por defecto y otros costes [P20, P23, P24, P25]
- La cuota por defecto es de **10.000 unidades al día** para los métodos del cubo común. Se reinicia a medianoche, hora del Pacífico.
- Toda petición cuesta al menos 1 unidad, aunque falle.
- Para ampliar la cuota hay que pasar una auditoría de cumplimiento (formulario *Quota Extension*).
- Costes por llamada:

| Método | Coste |
|---|---|
| `thumbnails.set` | **50** |
| `videos.update` | **50** |
| `captions.insert` | **400** |
| `playlistItems.insert` | 50 |
| `videos.list` | 1 |
| `search.list` | 1 por llamada en su propio cubo, 100 al día desde junio de 2026 |

- **Implicación práctica:** por cada Short, una subida + `thumbnails.set` (50) + `captions.insert` (400) + añadir a lista (50) ≈ **500 unidades del cubo común**, es decir, unos **20 Shorts al día** con 10.000 unidades si se suben subtítulos. Sin subtítulos (quemados en el vídeo), unos 100. Consejo: **quemar los subtítulos en el vídeo** y no usar `captions.insert` salvo que haga falta.

### B3. Bloqueo a privado en proyectos sin verificar [P26, P27]
- **URL:** https://developers.google.com/youtube/v3/docs/videos/insert, https://developers.google.com/youtube/v3/revision_history (entrada del 28 de julio de 2020) y https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits · 2026-10-11
- **Redacción oficial (frase exacta encontrada por el buscador):** *"All videos uploaded via the videos.insert endpoint from unverified API projects created after 28 July 2020 will be restricted to private viewing mode. To lift this restriction, each project must undergo an audit to verify compliance with the Terms of Service."*
  - Los creadores que suben con un cliente sin verificar reciben un correo que les explica que el vídeo está bloqueado como privado.
  - Los proyectos creados antes del 28 de julio de 2020 no están afectados.
- **Implicación práctica:**
  - **Hasta que el proyecto de Google Cloud pase la auditoría, todo lo que se suba por API quedará en privado y no se podrá publicar ni programar como público.**
  - Hay dos opciones: (a) solicitar la auditoría *"YouTube API Services – Audit and Quota Extension"* lo antes posible, o (b) usar la API solo para subir en privado y que el **humano publique o programe en Studio**.
  - `publishAt` no sirve mientras el proyecto no esté auditado.

### B4. Programación: `status.privacyStatus=private` + `status.publishAt` [P28]
- **URL:** https://developers.google.com/youtube/v3/docs/videos · 2026-10-11
- **Regla observada:**
  - `publishAt` solo se puede fijar si el vídeo es **privado** y **nunca se ha publicado**.
  - En `videos.update` hay que reenviar también `privacyStatus=private`.
  - Una fecha en el pasado hace que el vídeo se publique de inmediato. Un valor inválido devuelve el error `400 invalidPublishAt`.
- **Implicación práctica:** usar ISO 8601 en UTC y validar que la fecha sea futura. Solo funciona con un proyecto auditado (ver B3).

### B5. Campos de idioma y de "creado para niños" [P28, P29]
- `snippet.defaultLanguage` es el idioma del título y la descripción. Admite códigos ISO 639-1 o idiomas de la aplicación; en los extractos no aparece BCP-47, que sí se usa en `captions`.
- `snippet.defaultAudioLanguage` es el idioma de la pista de audio.
- `status.selfDeclaredMadeForKids` es un booleano que se puede escribir en insert y update. `status.madeForKids` es de solo lectura y refleja la determinación efectiva.
- **Implicación práctica:**
  - Enviar siempre `defaultLanguage="es"` (o `es-419`, comprobando que lo acepte) y `defaultAudioLanguage="es"`.
  - Enviar siempre `selfDeclaredMadeForKids=false` si el público no son niños. Es obligatorio declararlo por COPPA.

### B6. `status.containsSyntheticMedia`: el campo existe [P30, P22]
- **URL:** https://developers.google.com/youtube/v3/docs/videos y el historial de revisiones (30 de octubre de 2024) · 2026-10-11
- **Regla observada:**
  - Es un booleano en `video.status`, añadido el **30 de octubre de 2024**, que se puede fijar en `videos.insert` y `videos.update`.
  - Sirve para indicar que el vídeo contiene contenido alterado o sintético realista: personas reales que dicen o hacen algo que no hicieron, sucesos o lugares reales alterados, o escenas realistas que no ocurrieron.
- **Implicación práctica:** la fábrica lo rellena automáticamente según el manifiesto de activos (ver A4).

### B7. Ámbitos (scopes) de OAuth [P31, P32]
- `https://www.googleapis.com/auth/youtube.upload`: suficiente para `videos.insert`.
- `youtube.readonly`: lectura de la cuenta.
- `youtube` o `youtube.force-ssl`: gestión completa (`videos.update`, `thumbnails.set`, `captions.insert`).
- `yt-analytics.readonly`: métricas de actividad.
- `yt-analytics-monetary.readonly`: ingresos y anuncios. Según los extractos del historial de revisiones de septiembre de 2026, en los informes de canal solo devuelve datos si el canal está en el YPP; si no, responde **403**. Hay que confirmarlo.
- **Implicación práctica:** pedir el mínimo necesario, que es `youtube.upload` + `youtube.force-ssl` (miniaturas y metadatos) + `yt-analytics.readonly`. El ámbito monetario solo se añade cuando el canal esté en el YPP.

### B8. Caducidad del refresh token en modo "Testing" [P33]
- **URL:** https://developers.google.com/identity/protocols/oauth2 y https://support.google.com/cloud/answer/15549945 · 2026-10-11
- **Regla observada:**
  - Si la app es de tipo *External* y está en estado de publicación **"Testing"**, *"Authorizations by a test user will expire seven days from the time of consent"*, y los refresh tokens de acceso *offline* también caducan.
  - Excepción: las apps que solo piden `openid`, `email` y `profile`.
  - Hay un límite de 100 usuarios de prueba y de **100 refresh tokens por cuenta y client ID**: al superarlo se invalida el más antiguo sin aviso.
  - En producción, los tokens caducan si se revocan o si pasan unos 6 meses sin usarse.
- **Implicación práctica:**
  - Con la app en "Testing", **el humano tendrá que volver a autorizar cada 7 días**.
  - Para operar sin intervención hay que pasar la app a **"In production"**. Con ámbitos sensibles o restringidos de YouTube eso implica la **verificación de la app de OAuth** de Google, que es un proceso distinto de la auditoría de la API de YouTube (B3).
  - La fábrica debe detectar `invalid_grant` y avisar al humano.

### B9. Varios canales o cuentas de marca con una sola cuenta de Google [P34, P40]
- **URL:** https://support.google.com/youtube/answer/3046356 y https://support.google.com/youtube/answer/4642409 · 2026-10-11
- **Regla observada:**
  - Una cuenta de Google puede gestionar varios canales vinculados a cuentas de marca, **hasta 100**, y cambiar entre ellos sin cerrar sesión.
  - Los roles de las cuentas de marca se están sustituyendo por los permisos del canal en Studio.
- **No verificado:** la documentación oficial de la Data API que se encontró **no describe** el paso de elegir canal o cuenta de marca durante el consentimiento de OAuth. Solo documenta `prompt=select_account` (que elige la cuenta) y `channels.list?mine=true` (que devuelve el canal asociado al token).
- **Implicación práctica:**
  - Se necesita **un refresh token por canal**.
  - Después de cada autorización, llamar a `channels.list(part=id,snippet, mine=true)` y **comprobar que el `channelId` coincide con el esperado** antes de subir nada.
  - Hay que guardar los tokens separados por canal.

### B10. Guía de subida [P35]
- **URL:** https://developers.google.com/youtube/v3/guides/uploading_a_video y https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol · 2026-10-11
- **Regla observada:**
  - El ejemplo `upload_video.py` usa `MediaFileUpload(resumable=True)` y reintentos con *exponential backoff*. Está en **sintaxis de Python 2**.
  - Protocolo reanudable: `POST .../upload/youtube/v3/videos?uploadType=resumable&part=...` y después `PUT` del binario a la URI de sesión.
  - Tamaño máximo de archivo: 256 GB.
- **Implicación práctica:** portar el ejemplo a Python 3 con `google-api-python-client` y `google-auth-oauthlib`, y añadir reintentos ante 5xx y errores de red.

---

## C. YouTube Analytics API y Reporting API

### C1. Métricas [P36, P37]
- **URL:** https://developers.google.com/youtube/analytics/metrics y https://developers.google.com/youtube/analytics/channel_reports · 2026-10-11
- Métricas principales confirmadas: `views`, `engagedViews` (vistas que pasan del primer fotograma o que se inician con un clic o toque), `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`, `subscribersGained`, `subscribersLost`, `likes`, `dislikes`, `comments`, `shares` y `estimatedRevenue`.
- `estimatedRevenue` requiere `yt-analytics-monetary.readonly` y la pertenencia al YPP (ver B7).

### C2. Dimensiones [P38]
- `day`, `video` y **`creatorContentType`**, esta última añadida el 15 de diciembre de 2022 con los valores `SHORTS`, `VIDEO_ON_DEMAND`, `LIVE_STREAM` y `STORY`, y datos desde el 1 de enero de 2019. Es opcional en los informes por tiempo, demografía y fuentes de tráfico.
- **Implicación práctica:** filtrar o segmentar con `creatorContentType==SHORTS` para aislar el rendimiento de los Shorts.

### C3. Retención (curva de audiencia) [P37, P38]
- Informe con la dimensión **`elapsedVideoTimeRatio`** y las métricas **`audienceWatchRatio`** y `relativeRetentionPerformance`.
- Exige el filtro `video==ID`, **con un solo vídeo por llamada**, y devuelve 100 puntos (de 0,01 a 1,0). Filtro opcional: `audienceType==ORGANIC`.
- **Implicación práctica:** la curva de retención **sí está disponible por API**, a razón de una llamada por vídeo. No hace falta exportarla de Studio.

### C4. Impresiones y CTR: Reporting API (por lotes) [P39]
- **URL:** https://developers.google.com/youtube/reporting/v1/reports/channel_reports · 2026-10-11
- El **15 de enero de 2026** se añadieron los informes de alcance **`channel_reach_basic_a1`** (`video_thumbnail_impressions`, `video_thumbnail_impressions_ctr`) y `channel_reach_combined_a1` (por fuente de tráfico y dispositivo).
- Son **solo por lotes**: se crea un *job* con `jobs.create` y se descargan informes diarios.
- En la Analytics API se llaman `videoThumbnailImpressions` y `videoThumbnailImpressionsClickRate`.
- **Implicación práctica:**
  - Crear el *job* de Reporting el **primer día**, porque los informes se generan desde la creación del *job* en adelante; el histórico previo es limitado.
  - Lo que siga sin estar en ninguna API (por ejemplo, la autocertificación, ciertas vistas de Studio como "deslizado/visto" del feed de Shorts si no aparece en los informes) se exporta manualmente desde Studio. **No se ha verificado qué métricas exactas de Studio faltan.**

---

## D. Licencias de las dependencias [L01–L14]

| Componente | Licencia observada | Fuente (fecha de consulta: 2026-10-11) | Nota práctica |
|---|---|---|---|
| **Kokoro-82M** (pesos) | **Apache-2.0**. README: *"With Apache-licensed weights, Kokoro can be deployed anywhere from production environments to personal projects."* | github.com/hexgrad/kokoro (`LICENSE`, `README.md`, `pyproject.toml`) leídos literalmente. La ficha de HF `hexgrad/Kokoro-82M` está bloqueada; según copias, declara `apache-2.0` y entrenamiento con audio de dominio público o con licencia permisiva | Uso comercial permitido. Conservar el aviso de la licencia. Para español, la librería `kokoro` usa `misaki` con *fallback* a **espeak-ng (GPL-3.0)** |
| **kokoro-onnx** | **MIT** (*"kokoro-onnx: MIT · kokoro model: Apache 2.0"*) | github.com/thewh1teagle/kokoro-onnx `LICENSE` y `README.md` | Depende de **`phonemizer` (GPL-3.0, verificado en bootphon/phonemizer `LICENSE`)** y de `espeakng-loader` (MIT), que carga espeak-ng (GPL-3.0) |
| **Piper** (motor) | El repositorio antiguo `rhasspy/piper` es **MIT**, pero está archivado (*"Development has moved: https://github.com/OHF-Voice/piper1-gpl"*). El actual `OHF-Voice/piper1-gpl` es **GPL-3.0** e incorpora espeak-ng | `LICENSE.md` y `COPYING` leídos literalmente | El uso interno en un servidor para generar audio no obliga a publicar el código; la GPL afecta a la **distribución** del software. El audio generado no es obra derivada del código |
| Voces Piper: política general | *"The MODEL_CARD file for each voice contains important licensing information. Piper is intended for personal use and text to speech research only; we do not impose any additional restrictions on voice models. Some voices may have restrictive licenses"* | `OHF-Voice/piper1-gpl/docs/VOICES.md`, leído literalmente | Revisar cada `MODEL_CARD` |
| **es_MX-claude-high** | La MODEL_CARD declara **Apache-2.0**. Dataset: un Space de HF (HirCoir/Piper-TTS-Spanish), sin documentar el origen de las grabaciones | MODEL_CARD en HF, leída mediante el buscador | La licencia la declara quien subió la voz; el origen de los datos de voz no está acreditado. **Riesgo medio** |
| **es_MX-ald-medium** | La MODEL_CARD tiene el campo de licencia **mal formado** (*"http://u nlicense.org"*, que parece apuntar a la Unlicense). Ajuste fino a partir de `es_ES-davefx-medium` | MODEL_CARD en HF, leída mediante el buscador | **No verificado**: hay que revisar a mano la licencia de la voz base davefx |
| **es_AR-daniela-high** | Dataset **OpenSLR 61** con licencia **CC BY-SA 4.0** | MODEL_CARD en HF, leída mediante el buscador | Uso comercial permitido, **con atribución** (y *ShareAlike* sobre la obra derivada; conviene dar crédito en la descripción del canal o del vídeo) |
| **espeak-ng** | **GPL-3.0 o posterior** (*"released under the GPL version 3 or later license"*) | `espeak-ng/espeak-ng` `README.md` y `COPYING`, leídos literalmente | Mismo criterio que Piper: no distribuir binarios cerrados que lo enlacen |
| **Inter** (fuente) | **SIL OFL 1.1** | `rsms/inter/LICENSE.txt`, leído literalmente | Se puede usar en vídeos e incrustar. No se puede vender la fuente por separado |
| **Montserrat** (Google Fonts) | **SIL OFL 1.1** | `google/fonts/ofl/montserrat/OFL.txt`, leído literalmente | Todas las fuentes de la carpeta `ofl/` de google/fonts son OFL; verificar cada familia |
| **FFmpeg** | **LGPL v2.1+** por defecto. Con `--enable-gpl` pasa a **GPL v2+**. *"libx264 … libx265 … are under GPL version 2 … When combining them with FFmpeg, FFmpeg needs to be licensed as GPL as well"* | `FFmpeg/FFmpeg/LICENSE.md`, leído literalmente | El uso interno de un binario GPL para codificar no impone nada al vídeo producido. Solo importa si se **distribuye** el binario |
| **Playwright** | **Apache-2.0** | `microsoft/playwright/LICENSE`, leído literalmente | Sin restricciones relevantes |
| **YouTube Audio Library** | Ver A12: atribución obligatoria si la pista es CC; uso dentro de los vídeos; no se puede distribuir la música por separado | support.google.com/youtube/answer/3376882 (mediante el buscador) | Guardar la licencia por pista |

---

## Lista de control

### Qué controla automáticamente la fábrica
1. **Formato:** 1080×1920, 9:16, H.264 High, yuv420p, 30 fps, unos 8 Mbps, AAC-LC a 48 kHz, `+faststart`. Duración ≤179 s (objetivo de 20 a 60 s).
2. **Originalidad (anti "contenido no auténtico"):**
   - Comprobar la similitud entre guiones nuevos e históricos (por ejemplo, embeddings) y bloquear los que superen un umbral.
   - Rotar estructuras, aperturas (*hooks*) y estilos visuales.
   - Exigir en cada guion un dato o fuente nuevo y un análisis propio.
3. **Prohibición de lectura literal:** comprobar que el guion no reproduce texto de las fuentes (n-gramas con el texto fuente por debajo de un umbral).
4. **Guardarraíles para temas financieros:**
   - No presentar la voz como experto humano.
   - Lista negra de expresiones ("garantizado", "rentabilidad asegurada", "hazte rico", promesas de porcentajes).
   - Aviso "no es asesoramiento financiero" en la descripción.
5. **Coherencia de metadatos:** todo lo que dicen el título y la miniatura aparece en el guion o el vídeo. Sin caras de famosos ni personas reales.
6. **Manifiesto de IA:** registrar cada activo (TTS, gráficos, imágenes) y si es fotorrealista. Fijar `status.containsSyntheticMedia` (por defecto `false` con TTS genérico + gráficos; `true` si hay cualquier imagen o vídeo realista generado o música generada como foco).
7. **Campos de la API:** `selfDeclaredMadeForKids=false`, `defaultLanguage` y `defaultAudioLanguage`, categoría, etiquetas, `privacyStatus=private` y `publishAt` (solo con un proyecto auditado).
8. **Cuota:** contador por cubo (subidas y cubo común de 10.000 unidades). Presupuesto de unas 500 unidades por Short si se suben subtítulos. Parar antes del límite. Reinicio a medianoche, hora del Pacífico.
9. **OAuth:**
   - Un token por canal.
   - Comprobar `channels.list(mine=true)` frente al ID esperado antes de subir.
   - Detectar `invalid_grant` (caducidad de 7 días en modo Testing) y avisar.
10. **Licencias:**
    - Registro de voz y modelo con su licencia.
    - Atribución automática en la descripción para voces CC BY-SA (es_AR-daniela) y música CC de la biblioteca de audio.
    - Bloquear la voz `es_MX-ald` hasta que alguien verifique su licencia.
11. **Analítica:**
    - Consultas diarias a la Analytics API (`views`, `engagedViews`, `averageViewPercentage`, `subscribersGained`… con `creatorContentType==SHORTS`).
    - Retención con una llamada por vídeo.
    - *Job* de Reporting `channel_reach_basic_a1` para impresiones y CTR.
12. **Aviso de afiliación** en la descripción si hay enlaces de afiliado.

### Qué debe hacer el humano
1. **Solicitar la auditoría de la API de YouTube** (formulario *Audit and Quota Extension*). Hasta que se apruebe, todo lo que se suba por API queda en **privado** y hay que **publicar o programar en Studio**.
2. **Verificar la app de OAuth** y pasarla a "In production", o aceptar que hay que volver a autorizar **cada 7 días** en modo Testing.
3. **Comprobar en Cloud Console** los cubos y límites de cuota reales (hay contradicción entre 1 unidad en el cubo de subidas y 1600 o unas 100 unidades).
4. **Revisar la página de divulgación de IA en vivo** (answer/14328491) y confirmar el criterio para TTS + gráficos. En casos dudosos, marcar "Altered or synthetic content: Sí" en Studio.
5. **Rellenar la autocertificación "Ad suitability"** en Studio para cada vídeo monetizado (no hay campo de API documentado).
6. **Marcar la promoción pagada** en Studio si existe cualquier acuerdo con una marca, producto gratis o patrocinio.
7. **Revisar el contenido** antes de publicar (al menos por muestreo), sobre todo en temas financieros: exactitud de los datos, que no haya consejos personalizados y que la miniatura no engañe.
8. **Descargar la música** de la biblioteca de audio desde Studio y anotar su licencia.
9. **Subir miniaturas personalizadas de Shorts** desde Studio en ordenador, si se quieren, ya que la ayuda indica que solo está disponible ahí. Validar si `thumbnails.set` funciona con Shorts.
10. **Verificar manualmente** las licencias marcadas como no verificadas (`es_MX-ald-medium` y la voz base davefx, y el origen de los datos de `es_MX-claude-high`).
11. **Aceptar los nuevos términos del YPP antes del 31 de enero de 2027** y replantear la estrategia de ingresos ante los umbrales de 2027 (10 millones de vistas en 90 días para cobrar del fondo de Shorts; 20 millones para entrar al YPP por la vía Shorts).
12. **Cuentas:** asegurarse de que la cuenta de Google que autoriza es gestora o propietaria de cada canal de marca, y tener activada la verificación en dos pasos y AdSense.
