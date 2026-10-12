# Investigación de nichos: 2 canales faceless en español (LatAm + hispanos de EE. UU.)

- **Fecha de consulta de todas las fuentes:** 2026-10-11
- **Cliente:** residente en Villa Mercedes, San Luis, Argentina
- **Formato previsto:** Shorts diarios + video largo semanal opcional; voz TTS, visuales generados por computadora (HTML, gráficos, tipografía cinética, demos tipo pantalla), sin cámara ni rostro
- **Presupuesto:** USD 0–50/mes
- **Registro de evidencia:** `fuentes_investigacion.csv` (83 fuentes, IDs S01–S83). En este informe las citas aparecen como `[Sxx]`.

---

## 0. Resumen

**Selección recomendada:**

1. **Canal A: "IA aplicada y automatización para el trabajo y los negocios".** Nicho 2, que absorbe la parte "herramientas" del nicho 3. Puntaje 50/60, el más alto.
2. **Canal B: "Excel / Google Sheets para el trabajo y para administrar tu dinero".** Es el nicho 4 con una vertical de herramientas de finanzas personales tomada del nicho 1: presupuestos, calculadoras, comparadores y control de gastos, **sin recomendaciones de inversión**. El nicho 4 puro obtuvo 49/60 y el nicho 1 puro 46/60. El híbrido se estima en unos 49–50/60.

**Por qué esta combinación:**

- Los dos canales usan el **mismo pipeline visual**: planillas, gráficos y pantallas simuladas en HTML, más TTS.
- Se apoyan en **fuentes oficiales verificables**: documentación de Microsoft, Google y los proveedores de IA, y datos de bancos centrales.
- Tienen **riesgo controlable**: no son YMYL duro o se mantienen en su borde educativo.
- La monetización es complementaria:
  - El canal A gana con afiliados SaaS recurrentes.
  - El canal B gana con plantillas y cursos propios o de Hotmart, y con inventario publicitario de finanzas y educación.
- Coinciden con el perfil real del cliente, que automatiza Excel, PDF y procesos con Python e IA. Eso da autenticidad, que pesa frente a la política de "contenido inauténtico".

**Tres hallazgos críticos que condicionan la estrategia:**

1. **Los umbrales del YPP se duplican desde el 1-feb-2027 para solicitantes nuevos** [S06][S07][S08][S09]. Pasan a 8.000 horas válidas en 12 meses o 20 M de vistas de Shorts en 90 días; según la mayoría de las fuentes se mantienen los 1.000 suscriptores. Un canal que arranca en oct-2026 muy probablemente no llegue al umbral actual antes del 31-ene-2027 (estimación basada en [S77]: un canal faceless documentado tardó 157 días en llegar a 1.000 suscriptores). Por eso conviene planificar con el umbral nuevo:
   - El **video largo semanal deja de ser opcional**, porque las horas de Shorts no cuentan para las horas de visualización [S01].
   - Los **ingresos tempranos deben venir de afiliados**, de **YouTube Shopping con Mercado Libre desde 500 suscriptores** [S58] y de fan funding desde 500 suscriptores, cuyo umbral no cambia [S02][S08].
2. **El RPM de Shorts para audiencias latinoamericanas es casi simbólico.** Ejemplos: México 0,040 USD por 1.000 vistas frente a EE. UU. 0,328 [S15]. Además, los Shorts rinden apenas un 3–14% del RPM de un video largo [S14]. Los Shorts sirven para descubrimiento, no para facturar.
3. **El riesgo principal del formato no es el nicho sino la política de "contenido inauténtico"** [S39][S40]. Kapwing documenta que el español domina el "AI slop" más suscrito [S41], así que el algoritmo y los revisores están atentos a este idioma. La mitigación es que cada pieza aporte valor original: datos propios, demos reproducibles, plantillas descargables, guion no plantillado y variación de formato.

---

## 1. Metodología

1. **Búsqueda web** con la herramienta WebSearch: unas 60 consultas en español e inglés, algunas restringidas a dominios oficiales (`support.google.com`, `affiliate-program.amazon.com`).
2. **Registro de cada fuente** con URL, fecha de consulta, dato observado, tipo de fuente (oficial, medio, blog, herramienta u observación directa) y limitaciones (ver CSV).
3. **Separación explícita** entre:
   - **OBSERVADO:** dato presente en una fuente, citado como [Sxx].
   - **ESTIMACIÓN:** inferencia del analista, marcada "(E)".
4. **Matriz de 12 criterios** puntuados de 1 a 5, donde 5 es siempre lo mejor para el cliente. En competencia, riesgo y costo la escala está invertida: 5 = poca competencia, poco riesgo o bajo costo. Cada puntaje lleva justificación y confianza (alta, media o baja).
5. **Suma sin ponderar** sobre 60, más una lectura cualitativa de complementariedad entre pares de nichos.

## 2. Limitaciones (lectura obligatoria)

- **WebFetch falló en todos los dominios** (`getaddrinfo ENOTFOUND`), incluidos support.google.com, blog.google, outlierkit.com y thenextweb.com. El acceso directo por `curl` también fue bloqueado por el proxy del entorno (HTTP 403). **Por eso toda la evidencia proviene de los resúmenes y fragmentos que devuelve WebSearch, no de la lectura completa de cada página.** Eso implica dos riesgos:
  - errores del resumidor;
  - pérdida de contexto: fechas, notas al pie y metodología.
- **No hubo acceso a Google Trends**, ni a su interfaz ni a una API. Las señales de tendencia vienen de artículos sobre "El Año en Búsquedas" [S48][S49] y de estudios citados por medios [S26].
- **No hubo acceso a YouTube Analytics privado, a la YouTube Data API ni a Social Blade o vidIQ con login.** Los números de suscriptores son de herramientas de terceros con fechas distintas. Son órdenes de magnitud, no cifras exactas.
- **No hay datos públicos medidos de RPM para canales en español por nicho y país.** Los datos medidos disponibles [S13][S14][S15] mezclan idiomas y vienen de la cartera de clientes de una empresa (AIR), lo que introduce sesgo de selección. Las tablas de RPM por nicho que circulan son modeladas o autorreportadas [S19].
- **WebSearch está indexado desde EE. UU.**, lo que puede sesgar los resultados hacia fuentes en inglés.
- **Normativa argentina** (BCRA, ARCA, monotributo): cambia con frecuencia y las fuentes se contradicen [S70][S71]. Este informe **no es asesoramiento contable ni legal**.
- **Programas de afiliados:** no fue posible abrir las páginas oficiales de términos. Amazon Associates (elegibilidad de residentes argentinos) y Notion (si acepta nuevos afiliados) quedan **sin confirmar**.

---

## 3. Contexto de monetización (común a todos los nichos)

### 3.1 Programa de Socios de YouTube (YPP) desde Argentina

**Disponibilidad**

- Argentina está en la lista de países del YPP [S03].
- El YPP ampliado figura como totalmente desplegado en Argentina [S04].

**Requisitos vigentes al 2026-10-11** [S01][S02]

| Nivel | Requisitos | Qué habilita |
|---|---|---|
| Ampliado | 500 suscriptores + 3 subidas públicas en 90 días + (3.000 h en 12 meses o 3 M de vistas de Shorts en 90 días) | Membresías, Super Thanks, Super Chat y Shopping. No incluye reparto de anuncios. |
| Completo | 1.000 suscriptores + (4.000 h públicas válidas en 12 meses o 10 M de vistas válidas de Shorts en 90 días) | Reparto de anuncios y de YouTube Premium |

Las horas de Shorts vistas en el feed de Shorts no cuentan para las 4.000 h [S01].

**Cambio anunciado el 10-ago-2026, efectivo el 1-feb-2027** [S06][S07][S08][S09]

- Los solicitantes nuevos necesitarán **8.000 h o 20 M de vistas de Shorts en 90 días**. Algunos medios no mencionan el requisito de suscriptores; la mayoría dice que siguen siendo 1.000.
- Los miembros actuales no se ven afectados en la admisión.
- Según fuentes secundarias, se necesitarán **10 M de vistas de Shorts por cada 90 días para seguir cobrando del Creator Pool de Shorts**. Las fuentes discrepan sobre el alcance.
- Los umbrales de fan funding y Shopping no cambian [S08].

**Implicación (E):** con Shorts diarios de un canal nuevo en español, llegar a 20 M de vistas en 90 días es improbable en el primer semestre. **La vía realista es acumular 8.000 h con videos largos.** Por ejemplo, 8.000 h equivalen a unas 96.000 vistas de 5 minutos promedio de visualización en 12 meses (E, aritmética simple). Por eso el video semanal debería ser un **pilar** y no algo opcional, y conviene sumar listas de reproducción y videos "evergreen" de búsqueda.

**Shorts** [S05]

- Los ingresos por anuncios de los Shorts van a un Creator Pool.
- Primero se descuenta la licencia musical. Si un Short usa una pista, la mitad de sus ingresos va a música. **Implicación (E): no usar música con licencia en Shorts no sube la tasa del 45%, pero evita diluir el pool.** Lo más simple es narración TTS con efectos propios o música libre generada.
- El creador recibe el 45% de lo que se le asigna según su cuota de vistas.

### 3.2 RPM y CPM: separar video largo y Shorts

| Métrica | Dato | Tipo | Fuente |
|---|---|---|---|
| RPM mediano global de video largo, todas las temáticas | ~2,30 USD | Medido, muestra de AIR | [S13] |
| RPM de video largo, Education & Science | 10,22 USD (mediana) | Medido | [S13] |
| RPM de video largo, Gadgets & Tech | 2,33 USD (mediana); solo 34% de vistas monetizadas | Medido | [S13] |
| RPM de video largo, Business & Finance | 2,01 USD (mediana; P75 5,17); direccional porque hay menos de 10 canales | Medido | [S13] |
| RPM de video largo, finanzas en tablas modeladas | 5–17 USD (orientado a EE. UU.) | Modelado | [S20] |
| RPM de video largo, canal argentino de deportes con 70K suscriptores | 1,40 USD promedio (0,50 a 2,00) | Caso real (medio) | [S21] |
| RPM de video largo, finanzas con audiencia mexicana | "puede superar 10 USD" | Afirmación periodística | [S80] |
| CPM de México | ~1,52 USD mediano (0,57–8,54); otra cifra: 1,82 o 0,91 | Blog de proveedor, contradictorio | [S16][S17] |
| CPM de Argentina | 1,10 o 0,55 USD (contradictorio) | Blog de proveedor | [S17] |
| RPM de Shorts por país (datos 2025) | EE. UU. 0,328 · Canadá 0,165 · Brasil 0,045 · **México 0,040** USD/1.000 | Medido (AIR) | [S15] |
| RPM de Shorts frente a video largo | 3–14% del RPM largo; 11–34K vistas de Shorts ≈ 1K vistas largas | Medido (AIR) | [S14] |
| Señal relativa de Argentina | El RPM musical (Art Tracks) de Argentina es el más bajo de LatAm | Otra métrica (música) | [S18] |

**Lectura (E):**

- Para un canal en español con audiencia mayoritaria de MX, CO, AR y CL, un rango razonable de planificación de **RPM de video largo es 0,5–3 USD**. Puede ser algo mayor en finanzas o software si capta audiencia de EE. UU. o México.
- El **RPM de Shorts esperable es de 0,02–0,06 USD por 1.000 vistas**.
- Ejemplo ilustrativo (E): 1 M de vistas de Shorts al mes con audiencia latinoamericana ≈ 20–60 USD. 20.000 vistas largas al mes ≈ 10–60 USD.
- **Los afiliados y productos propios pesan más que AdSense en el primer año.**

**Hispanos de EE. UU.:**

- AIR afirma que el CPM hispano de EE. UU. "rivaliza" con el inglés [S17]. Es marketing de un proveedor de traducción, sin datos.
- En contra:
  - El 54% de los hispanos de EE. UU. se informa principalmente en inglés y solo el 21% principalmente en español [S75].
  - En el primer trimestre de 2025 menos del 1% del gasto digital del comercio online fue a sitios en español [S76].
- Conclusión (E): la audiencia hispana de EE. UU. es una **ventaja posible pero no garantizada**. Los temas que la atraen naturalmente sirven para capturar geografía de alto RPM. Por ejemplo, la diferencia de 8x en RPM de Shorts entre EE. UU. y México [S15] justifica incluir temas como:
  - "Excel/IA para tu trabajo o negocio en EE. UU."
  - herramientas en inglés explicadas en español.

### 3.3 Cobro y fiscalidad desde Argentina (nivel alto, no es asesoramiento)

**Cobro de AdSense**

- Disponibles: transferencia bancaria (wire) [S11] y Western Union Quick Cash en USD, con hasta 7.500 USD por pago y sin comisión de Google [S10].
- No disponible: EFT [S11].
- La conversión depende del banco receptor.

**Retención de impuestos de EE. UU.** [S12]

- Hay que cargar el W-8BEN en AdSense antes del 10 de diciembre.
- Sin ese formulario, Google puede retener **hasta el 24% de los ingresos mundiales**.
- Con el formulario, la retención es del 0–30% solo sobre lo generado por espectadores de EE. UU.
- Las fuentes se contradicen sobre si existe un tratado Argentina–EE. UU. vigente [S81]. **Estimación: no lo hay, y por lo tanto la retención sería del 30% sobre los ingresos de espectadores de EE. UU.** Hay que verificarlo en la lista oficial de tratados del IRS.

**Régimen cambiario (BCRA)** [S70]

- Com. A 8226 (abr-2025): liberó la compra de divisas a personas humanas.
- Com. A 8330 (sep-2025): eliminó el tope anual de 36.000 USD de la excepción de liquidación para exportadores de servicios.
- Com. A 8417 (abr-2026): exceptuó a las personas humanas de ingresar y liquidar los cobros de exportaciones, con condiciones.
- Hay que verificar el texto vigente con un contador.

**ARCA (ex-AFIP) y monotributo** [S71][S72]

- Los ingresos de AdSense, YouTube y afiliados del exterior se tratan como **exportación de servicios con Factura E**, en USD o en pesos al tipo de cambio comprador del BNA del día anterior.
- Hay contradicciones sobre si esos ingresos suman al tope de la categoría del monotributo. **Consultar a un contador antes del primer cobro.**
- Dato de contexto: "ARCA" fue la segunda búsqueda en tendencia de Argentina en 2025 [S49].

**Billeteras y medios de cobro**

- **Payoneer:** opera en Argentina; retiro a banco local en ARS o USD con comisión de hasta 2% [S67].
- **PayPal:** funciona con restricciones y comisiones propias [S68].
- **Wise:** disponible con limitaciones, por ejemplo sin tarjeta física [S69].
- **Mercado Pago:** es donde Mercado Libre acredita las comisiones de afiliados [S56].

### 3.4 Afiliados y sponsors accesibles desde Argentina

| Programa | ¿Acepta residentes en AR? | Pago | Comisión | Fuente / confianza |
|---|---|---|---|---|
| **Mercado Libre Afiliados y Creadores (AR)** | Sí. Lanzado el 13-nov-2025; al inicio solo para monotributistas; expansión nacional anunciada en mar-2026 | Mercado Pago | Hasta 15% según categoría | [S56][S57], alta |
| **Mercado Libre Afiliados (MX, CL, BR)** | Existe en esos países; la cuenta local probablemente sea requisito (E) | Mercado Pago local | No se encontró la tabla vigente de MX | [S56], media |
| **YouTube Shopping con Mercado Libre (MX y AR)** | Sí, desde jun-2026, para canales elegibles con 500+ suscriptores | Vía programa | La fija cada comercio | [S58][S59], media (fechas discrepantes) |
| **Hotmart** | Sí. Retiro a cuenta local; hay una tarifa de conversión por normativa del BCRA | Cuenta bancaria local | Hasta 80% (la define el productor) | [S61][S62], media |
| **PartnerStack (red de muchos SaaS)** | Depósito vía Airwallex con Argentina en la lista; PayPal en 200+ países | Airwallex, PayPal, Stripe | Según el SaaS | [S64], media |
| **Notion** | Vía PartnerStack; **un tercero dice que está cerrado a nuevos afiliados a mediados de 2026** | PayPal, Stripe | Terceros citan 50% durante 12 meses (no confirmado) | [S63], baja |
| **Hostinger** | No hay lista oficial de países; posibles rechazos por compliance | PayPal, transferencia, saldo | Mínimo de 50–100 USD según programa | [S65], media |
| **Canva** | Abierto globalmente según directorios | PayPal, transferencia | Hasta 36 USD por Pro según directorios | [S66], baja |
| **Amazon Associates (EE. UU.)** | **No confirmado.** Transferencia internacional solo a bancos de EE. UU., Reino Unido o la Eurozona; resto por cheque o gift card | Transferencia, cheque, gift card | — | [S60], baja. Poco útil para audiencia LatAm (E) |
| **Sponsors tech en español** | Existen (por ejemplo, códigos de NordVPN en canales en español) | — | No hay tarifas públicas | [S79][S83], baja |

---

## 4. Hallazgos por nicho

### Nicho 1: Finanzas personales, educación financiera y herramientas para administrar dinero

**Demanda (observado)**

- Según Google, las búsquedas de términos financieros en YouTube en LatAm crecieron un 47% anual desde 2015. El 65% de los espectadores tiene entre 18 y 34 años y el 55% son mujeres [S26]. Es un dato de 2023 y antiguo.
- Think with Google identifica 9 formatos de educación financiera que funcionan en YouTube, empezando por los tutoriales de operaciones básicas [S27].
- Global Findex 2025: el ahorro por dinero móvil está en aumento, con un 73% de adultos de la región con cuenta según medios [S55].

**Competencia (observado)**

- Aprendiz Financiero tiene ~1,61 M de suscriptores [S23] y Camino Financiero ~159K [S24].
- **Ya existen canales faceless de finanzas en español que se venden en Flippa**, como uno de 17K suscriptores con formato tipo audiolibro [S25]. El formato faceless de finanzas no es novedoso.

**Monetización (observado)**

- Las tablas modeladas ponen a finanzas en el primer lugar [S20], y un medio dice que con audiencia mexicana puede superar los 10 USD de RPM [S80].
- Pero el dato medido de AIR da una mediana de 2,01 USD para Business & Finance, por debajo de Tech y de Educación [S13], aunque con muestra chica.

**Riesgo (observado)**

- Es un tema YMYL [S47].
- La política de estafas de YouTube prohíbe las promesas de enriquecimiento rápido [S44].
- En Argentina, promocionar plataformas cripto no registradas ante la CNV tiene riesgo legal [S46].
- Reportes de 2026 mencionan como no monetizables los "personajes de IA que dan consejos sobre temas sensibles" [S39]. Es un dato no verificado en fuente primaria, pero relevante para una voz TTS que hable de dinero.

**Producción (E):** es ideal para gráficos: interés compuesto, inflación por país, simuladores de presupuesto y comparativas.

**Ángulo Argentina (E)**

- Temas como el dólar blue, el cepo, el plazo fijo o el monotributo tienen demanda local [S49], pero **limitan el alcance internacional y caen en el CPM más bajo de la región** [S17][S18][S21].
- Además, quedan obsoletos rápidamente.
- Conviene tratarlos como una lista de reproducción secundaria, no como eje.

### Nicho 2: IA aplicada, software y automatización para negocios

**Demanda (observado)**

- "Gemini" fue la segunda búsqueda en tendencia de México en 2025; DeepSeek y NotebookLM también destacaron [S48].
- El español es uno de los principales idiomas no ingleses en ChatGPT [S50]. México figura entre los países que más subieron en uso por habitante en el primer trimestre de 2026 [S51].
- El 63% de las empresas de AR, CL, CO, MX y PE ya incorporó herramientas de IA, pero el 58% en nivel básico. El 97% de los trabajadores quiere capacitación en IA [S53].
- SAP: el 55% de los decisores latinoamericanos planea aumentar la inversión en IA [S54].
- LinkedIn 2026: la alfabetización en IA es la habilidad en auge [S52].
- Las guías de nichos mencionan IA y tutoriales como el nicho de más crecimiento [S78], aunque con metodología débil.

**Competencia (observado)**

- Los grandes divulgadores de IA en español están mayormente en España y se basan en la persona: DotCSV ~914K [S28] y Xavier Mitjana ~317–370K [S29].
- (E) Hay un **hueco** en "IA práctica para pymes y trabajadores latinoamericanos" con flujos reproducibles: WhatsApp, facturas, planillas, atención al cliente.

**Monetización (observado)**

- RPM mediano medido de Tech: 2,33 USD, con solo el 34% de vistas monetizadas [S13]. AdSense es moderado.
- Los **afiliados SaaS recurrentes** son la palanca principal. PartnerStack paga a Argentina vía Airwallex [S64] y Hostinger por PayPal [S65].

**Riesgo (E)**

- Bajo en lo regulatorio.
- Riesgo de exageración o desinformación y de obsolescencia rápida.
- Riesgo de "contenido inauténtico" si se hacen listas genéricas de "10 herramientas de IA" [S39][S40].

**Producción (E):**

- Las demos "tipo pantalla" pueden generarse en HTML: chats simulados, flujos de automatización y comparativas de tiempo antes y después.
- Las capturas de interfaces reales requieren cuentas, aunque los planes gratuitos suelen bastar.
- Hay que cuidar la precisión de las interfaces y el uso de marcas.

### Nicho 3: Tecnología práctica, apps y herramientas digitales

**Demanda (observado)**

- YouTube llega al 76,3% de los internautas de México [S74].
- Los Shorts superan los 200 mil millones de vistas diarias [S73], aunque con el conteo de vistas cambiado en marzo de 2025.

**Competencia (observado):** muy fragmentada, con muchos canales chicos y medianos por país (México, Colombia) [S35] además de los grandes canales con presentador. (E) Los consejos de celular son contenido muy commoditizado. El formato sin rostro no puede hacer unboxing ni reseñas de producto creíbles.

**Monetización (observado)**

- RPM de Tech 2,33 USD con 34% de vistas monetizadas [S13].
- **YouTube Shopping con Mercado Libre** [S58] es una ventaja para gadgets en México y Argentina.
- Amazon es poco útil desde Argentina [S60].

**Evaluación (E):** se superpone con el nicho 2. Conviene **absorber su mejor parte** (apps y herramientas para productividad y negocio) en el canal A, en lugar de abrirlo como canal propio.

### Nicho 4: Empleo, habilidades profesionales y productividad (Excel y Google Sheets en español)

**Demanda (observado)**

- Hay canales de Excel en español con gran audiencia: Microsoft Excel a Todo Nivel ~325K [S30] y El Inge Francisco, del que una fuente cita más de 913K [S31].
- LinkedIn 2026 destaca el análisis de datos [S52].
- La demanda de capacitación en IA (97%) se cruza con la ofimática [S53].

**Competencia (observado + E)**

- Los grandes canales se basan en el profesor y en tutoriales largos de pantalla [S30][S31]. La cola larga es chica, por ejemplo un canal de 2,4K [S32].
- (E) Hay espacio para **Shorts de fórmula en 30 segundos con animación celda por celda** y plantillas descargables. Es un formato visual que los competidores con pantalla grabada no ofrecen.

**Monetización (observado)**

- Plantillas propias o de terceros vía Hotmart, con comisión de afiliado de hasta 80% [S61].
- El RPM medido de "Education & Science" es de 10,22 USD [S13], pero no está claro que los tutoriales de Excel se clasifiquen así, y la muestra no es hispana. Confianza baja.

**Riesgo (E):** muy bajo. Las fórmulas son verificables de forma determinística: se pueden testear automáticamente antes de publicar.

**Ajuste con el cliente (observado en el README del repositorio):** su perfil es "Data & AI Automation · Excel / PDF workflows", con proyectos de limpieza de Excel, dashboards de KPI y extracción de PDF a Excel. Tiene experiencia real que aportar.

### Nicho 5: Negocios digitales, ventas y emprendimiento

**Competencia (observado):** EmprendeAprendiendo tiene más de 2 M de suscriptores [S33], Emprendetube ~129K [S34] y Carlos Estratega ~453K [S82]. El nicho está saturado de "gurús".

**Riesgo (observado):** la política de estafas sobre "hacerse rico rápido" [S44] y el estigma de los gurús. Las afirmaciones de ingresos son difíciles de verificar (E).

**Monetización (observado):** Hotmart [S61], Hostinger [S65] y Mercado Libre [S56] dan una buena intención comercial, pero (E) la credibilidad sin rostro ni casos propios es baja.

**Evaluación (E):** sirve más como **tema transversal del canal A** (IA para vender, automatizar atención al cliente) que como canal propio.

### Nicho 6a (adicional): Curiosidades y ciencia explicada

- **Demanda:** alta. Hay canales grandes como QuantumFracture (más de 1 M) y SuperCurioso (~524K) [S36].
- **Problema:** los canales de **"AI slop" en español** dominan esta categoría [S41], y es la más expuesta a la política de contenido inauténtico [S39][S40].
- **Monetización:** casi sin afiliados ni intención comercial.
- **Conclusión:** descartado por riesgo y por falta de complementariedad comercial.

### Nicho 6b (adicional): Inglés para hispanohablantes

**Demanda (observado):** EF EPI 2025 ubica a México en el puesto 103 ("muy bajo") y a Colombia en el 76 ("bajo"). Argentina está en el puesto 26, la mejor de la región [S38]. Hay demanda en México y Colombia, y menos en Argentina.

**Competencia (observado):** canales grandes como Amigos Ingleses (más de 1,5 M) y EngVid (más de 2 M) [S37], en general con profesor visible.

**Evaluación (E)**

- Es excelente para tipografía cinética y de riesgo muy bajo, pero tiene RPM bajo y afiliados no verificados.
- **El cliente declara inglés "basic" en su README**, lo que eleva el riesgo de errores de pronunciación o de uso con TTS sin un revisor nativo.
- Queda como alternativa de reserva.

---

## 5. Matriz de evaluación (1–5; 5 = mejor para el cliente)

Notación: **O** = basado en dato observado; **E** = estimación del analista. Confianza: A = alta, M = media, B = baja.

### 5.1 Tabla resumen

| Criterio | N1 Finanzas | N2 IA/automatización | N3 Tech/apps | N4 Excel/productividad | N5 Negocios digitales | N6a Curiosidades | N6b Inglés |
|---|---|---|---|---|---|---|---|
| 1. Demanda | 5 | 5 | 4 | 4 | 4 | 5 | 4 |
| 2. Competencia (invertida) | 2 | 3 | 2 | 3 | 2 | 1 | 3 |
| 3. Diferenciación de un canal nuevo | 3 | 4 | 2 | 4 | 2 | 2 | 3 |
| 4. Retención y compartibilidad | 4 | 4 | 4 | 3 | 3 | 5 | 4 |
| 5. Potencial de RPM | 4 | 3 | 3 | 3 | 3 | 3 | 2 |
| 6. Afiliados, sponsors y productos | 3 | 5 | 3 | 4 | 4 | 1 | 3 |
| 7. Intención comercial | 4 | 5 | 4 | 3 | 5 | 1 | 3 |
| 8. Facilidad de demos visuales originales | 5 | 4 | 3 | 5 | 3 | 3 | 5 |
| 9. Fuentes confiables disponibles | 4 | 4 | 4 | 5 | 3 | 4 | 4 |
| 10. Riesgo (invertido) | 2 | 4 | 4 | 5 | 2 | 2 | 5 |
| 11. Costo de producción (invertido) | 5 | 4 | 4 | 5 | 5 | 4 | 4 |
| 12. Capacidad de contenido para 90 días | 5 | 5 | 5 | 5 | 4 | 5 | 5 |
| **TOTAL /60** | **46** | **50** | **42** | **49** | **40** | **36** | **45** |
| Ranking | 3 | **1** | 5 | **2** | 6 | 7 | 4 |

Sensibilidad (E): si se pondera al doble el RPM y el criterio de afiliados, el orden de los tres primeros no cambia:

- N2: 50 + 3 + 5 = 58
- N1: 46 + 4 + 3 = 53
- N4: 49 + 3 + 4 = 56

Si se pondera al doble el riesgo, N1 cae (46 + 2 = 48) y N4 sube (49 + 5 = 54).

### 5.2 Justificación por celda

#### N1: Finanzas personales

| # | Pts | Justificación | O/E | Conf. |
|---|---|---|---|---|
| 1 | 5 | Crecimiento sostenido de búsquedas financieras en YouTube en LatAm [S26]; audiencia joven; Findex muestra más gente con cuentas y ahorro digital [S55] | O (dato antiguo) | M |
| 2 | 2 | Canales grandes [S23][S24] y faceless de finanzas ya existentes y vendidos [S25] | O | M |
| 3 | 3 | Diferenciarse con comparativas por país y simuladores es posible, pero muchos hacen "finanzas con gráficos" | E | B |
| 4 | 4 | El dinero es un tema universal y compartible; los formatos tutoriales funcionan [S27] | O+E | B |
| 5 | 4 | El RPM modelado es el más alto [S20][S80]; el medido es moderado [S13]; los anunciantes financieros de LatAm (bancos y fintech) están activos (E) | O contradictorio | B |
| 6 | 3 | Los afiliados financieros están fragmentados por país y regulados; brokers y cripto conllevan riesgo CNV [S46]; los cursos de Hotmart sí son una opción [S61] | O+E | M |
| 7 | 4 | La audiencia busca abrir cuentas, comparar y elegir productos | E | M |
| 8 | 5 | Gráficos, simuladores y tablas son el formato nativo del pipeline | E | A |
| 9 | 4 | Hay estadística oficial (bancos centrales, Banco Mundial [S55]), pero las reglas varían por país y cambian | O+E | M |
| 10 | 2 | YMYL [S47]; política de estafas [S44]; riesgo regulatorio en Argentina [S46]; posible restricción a "personajes de IA aconsejando temas sensibles" [S39] | O | A |
| 11 | 5 | Datos y gráficos gratuitos | E | A |
| 12 | 5 | Cientos de conceptos × países × herramientas | E | A |

#### N2: IA aplicada y automatización

| # | Pts | Justificación | O/E | Conf. |
|---|---|---|---|---|
| 1 | 5 | Gemini y DeepSeek en la cima de búsquedas de México [S48]; el español es un idioma top en ChatGPT [S50]; 63% de las empresas usan IA y 97% de los trabajadores quiere capacitarse [S53]; SAP [S54] | O | M |
| 2 | 3 | Los referentes grandes están en España y se basan en la persona [S28][S29]; el hueco "pyme LatAm práctica" es una estimación | O+E | B |
| 3 | 4 | Flujos reproducibles con métricas de antes y después; experiencia real del cliente (README) | E | M |
| 4 | 4 | La novedad y el "mirá lo que hace esta herramienta" funcionan bien en Shorts | E | B |
| 5 | 3 | Mediana medida de Tech 2,33 USD con 34% de vistas monetizadas [S13]; CPM B2B de software potencialmente mayor (E) | O+E | B |
| 6 | 5 | SaaS con afiliados recurrentes; PartnerStack paga a Argentina [S64]; Hostinger [S65]; Canva [S66] | O | M |
| 7 | 5 | La audiencia busca adoptar o comprar herramientas | E | M |
| 8 | 4 | Interfaces simuladas en HTML, diagramas de flujo, capturas automatizadas; requiere cuidado con la fidelidad de las interfaces | E | M |
| 9 | 4 | Documentación oficial y changelogs [S50][S51]; información que envejece rápido | O+E | M |
| 10 | 4 | Riesgo regulatorio bajo; riesgo de exageración y de "contenido inauténtico" en listas genéricas [S39][S40] | O+E | M |
| 11 | 4 | Los planes gratuitos suelen bastar; algunas demos piden planes pagos | E | M |
| 12 | 5 | Lanzamientos constantes, más casos de uso por oficio | E | A |

#### N3: Tecnología práctica y apps

| # | Pts | Justificación | O/E | Conf. |
|---|---|---|---|---|
| 1 | 4 | Uso masivo de YouTube y Shorts [S73][S74] | O | M |
| 2 | 2 | Muy fragmentado y competido [S35] | O+E | B |
| 3 | 2 | Sin rostro no hay unboxing ni reseñas creíbles; los consejos son commodity | E | M |
| 4 | 4 | Los consejos rápidos se comparten | E | B |
| 5 | 3 | Tech 2,33 USD con 34% de vistas monetizadas [S13] | O | M |
| 6 | 3 | YouTube Shopping con Mercado Libre [S58] suma; Amazon poco útil desde Argentina [S60] | O | M |
| 7 | 4 | Intención de compra de gadgets y apps | E | M |
| 8 | 3 | Requiere capturas de apps y dispositivos reales | E | M |
| 9 | 4 | Documentación oficial | E | M |
| 10 | 4 | Riesgo bajo; marcas e interfaces de terceros | E | M |
| 11 | 4 | Se necesitan dispositivos o cuentas | E | M |
| 12 | 5 | Flujo constante de temas | E | A |

#### N4: Excel, Sheets y productividad

| # | Pts | Justificación | O/E | Conf. |
|---|---|---|---|---|
| 1 | 4 | Canales de Excel en español de cientos de miles de suscriptores [S30][S31]; habilidades de datos en auge [S52] | O | M |
| 2 | 3 | Competidores establecidos en formato largo; cola larga chica [S32] | O+E | B |
| 3 | 4 | Animación celda por celda y plantillas descargables: formato distinto del screencast | E | M |
| 4 | 3 | Más "guardar" que "compartir"; tráfico de búsqueda evergreen | E | B |
| 5 | 3 | Educación medida alta [S13], pero no aplicable con certeza; audiencia LatAm | O+E | B |
| 6 | 4 | Plantillas y cursos (Hotmart hasta 80% [S61]); SaaS de productividad [S64] | O | M |
| 7 | 3 | Intención de aprender que se convierte en compra de plantillas o cursos | E | M |
| 8 | 5 | Las planillas se renderizan perfecto en HTML; las fórmulas se pueden verificar con código | E | A |
| 9 | 5 | Documentación oficial de Microsoft y Google; resultados testeables | E | A |
| 10 | 5 | No es YMYL; sin restricciones de anunciantes | E | A |
| 11 | 5 | Herramientas gratuitas (Sheets, LibreOffice, HTML) | E | A |
| 12 | 5 | Cientos de funciones × casos laborales | E | A |

#### N5: Negocios digitales y emprendimiento

| # | Pts | Justificación | O/E | Conf. |
|---|---|---|---|---|
| 1 | 4 | Canales de millones [S33] | O | M |
| 2 | 2 | Saturación [S33][S34][S82] | O | M |
| 3 | 2 | Sin casos propios ni rostro, la credibilidad es baja | E | M |
| 4 | 3 | Motivacional, con retención variable | E | B |
| 5 | 3 | Business & Finance 2,01 USD [S13] | O | B |
| 6 | 4 | Hotmart [S61], Hostinger [S65], Mercado Libre [S56] | O | M |
| 7 | 5 | Alta intención de compra de herramientas y cursos | E | M |
| 8 | 3 | Temas abstractos; los gráficos de embudos son parciales | E | M |
| 9 | 3 | Afirmaciones de ingresos no verificables | E | M |
| 10 | 2 | Política de "hacerse rico rápido" [S44] | O | M |
| 11 | 5 | Bajo | E | A |
| 12 | 4 | Riesgo de repetición | E | M |

#### N6a: Curiosidades y ciencia

| # | Pts | Justificación | O/E | Conf. |
|---|---|---|---|---|
| 1 | 5 | Canales de más de 1 M [S36] | O | M |
| 2 | 1 | Saturación de "AI slop" en español [S41] | O | M |
| 3 | 2 | Difícil destacar sin un presentador o narrador con identidad | E | M |
| 4 | 5 | Muy compartible | E | M |
| 5 | 3 | Educación y ciencia medidas alto [S13], pero las curiosidades tienden a entretenimiento | O+E | B |
| 6 | 1 | Casi sin afiliados | E | M |
| 7 | 1 | Baja | E | M |
| 8 | 3 | Necesita ilustración o b-roll | E | M |
| 9 | 4 | Hay fuentes científicas | E | M |
| 10 | 2 | Máxima exposición a la política de contenido inauténtico [S39][S40][S41] | O | M |
| 11 | 4 | Hay que producir imágenes | E | M |
| 12 | 5 | Infinito | E | A |

#### N6b: Inglés para hispanohablantes

| # | Pts | Justificación | O/E | Conf. |
|---|---|---|---|---|
| 1 | 4 | Nivel bajo en México y Colombia [S38]; canales grandes [S37] | O | M |
| 2 | 3 | Profesores con rostro dominan [S37] | O+E | B |
| 3 | 3 | La tipografía cinética encaja, pero sin profesor visible se pierde confianza | E | B |
| 4 | 4 | Formatos tipo "frases que decís mal" | E | B |
| 5 | 2 | Educación con audiencia LatAm; sin datos | E | B |
| 6 | 3 | Hay afiliados de apps de idiomas, pero no se verificaron | E | B |
| 7 | 3 | Media | E | B |
| 8 | 5 | Visual basado en texto | E | A |
| 9 | 4 | Hay diccionarios y corpus | E | M |
| 10 | 5 | Riesgo bajo | E | A |
| 11 | 4 | Requiere TTS bilingüe de calidad y un revisor (el cliente declara inglés básico) | O (README) + E | M |
| 12 | 5 | Infinito | E | A |

---

## 6. Selección final: los dos nichos complementarios

### Canal A: IA aplicada y automatización para el trabajo y los negocios (N2 + lo mejor de N3 y N5)

**Propuesta:** "Automatizá tu trabajo y tu negocio con IA, paso a paso". Flujos reproducibles para pymes, freelancers y empleados de LatAm y para hispanos de EE. UU.:

- responder clientes;
- procesar facturas y PDF;
- resumir reuniones;
- generar reportes;
- comparar herramientas con pruebas propias.

**Por qué:**

- Es el puntaje más alto (50).
- Tiene demanda observada y en crecimiento [S48][S50][S53][S54] y afiliados SaaS que pagan a Argentina [S64][S65].
- Los temas no dependen del país, así que tiene alcance pan-latinoamericano y potencial en EE. UU.

**Diferenciación (E):**

- Cada video resuelve un problema concreto con un resultado medible: "de 2 horas a 5 minutos".
- Incluye un archivo o prompt descargable.
- Evita las listas genéricas de "10 IA que no conocías".

### Canal B: Excel y Google Sheets para el trabajo y para administrar tu dinero (N4 + vertical de herramientas de N1)

**Propuesta:** fórmulas, plantillas y "minisistemas" en planilla:

- control de gastos;
- presupuesto 50/30/20;
- simulador de deuda;
- calculadora de interés compuesto;
- inventario;
- facturación;
- dashboards.

Alrededor del 60% del contenido es laboral y alrededor del 40% es de dinero personal (E).

**Por qué:**

- N4 obtuvo 49 puntos, con el mejor perfil de riesgo, costo y verificabilidad.
- La vertical de dinero agrega la **intención comercial y la mayor demanda de finanzas** (N1) sin entrar en recomendaciones de inversión, que es donde se concentra el riesgo YMYL y regulatorio [S44][S46][S47].

**Monetización:**

- Plantillas propias, vendidas vía Hotmart o en una tienda propia.
- Cursos de afiliados [S61].
- YouTube Shopping y Mercado Libre para insumos de oficina y tecnología [S58].

### Complementariedad entre A y B

| Dimensión | Canal A (IA) | Canal B (Sheets y dinero) | Sinergia |
|---|---|---|---|
| Audiencia | Trabajadores y pymes que adoptan IA | Trabajadores y personas que organizan trabajo y dinero | Mucho solapamiento, lo que permite promoción cruzada y listas compartidas |
| Monetización principal | Afiliados SaaS recurrentes | Productos digitales propios (plantillas) y anuncios de educación y finanzas | Fuentes de ingreso diversificadas |
| Categoría publicitaria | Software y tecnología | Educación y finanzas | Si una categoría cae, la otra sostiene |
| Pipeline visual | Interfaces simuladas, flujos, chats en HTML | Planillas animadas, gráficos | El mismo motor HTML, charts y TTS |
| Puente de contenido | "Usá IA para escribir fórmulas" | "Planilla que se alimenta con IA" | Episodios espejo entre canales |
| Riesgo | Bajo a medio | Bajo | Ninguno en YMYL duro |

### Lo que NO se recomienda

- **Finanzas de inversión, cripto o "trading"** como eje: riesgo de CNV, YMYL y políticas de estafa [S44][S46].
- **Curiosidades:** saturación de "AI slop" en español [S41].
- **Emprendimiento genérico:** gurús y saturación [S33][S44].

---

## 7. Argentina específica frente a pan-LatAm

1. **Por defecto, español neutro pan-latinoamericano**:
   - montos en USD o "tu moneda";
   - ejemplos que roten entre México, Colombia, Chile y Argentina;
   - México primero por tamaño de audiencia [S74] y por tener un RPM de Shorts relativamente mejor que Brasil o Argentina [S15][S18].
2. **Temas solo argentinos** (dólar blue, cepo, plazo fijo, monotributo, ARCA): tienen demanda local (ARCA fue la segunda búsqueda en tendencia de 2025 [S49]), pero hay tres razones para limitarlos:
   - **reducen el alcance internacional**;
   - **caen en el CPM más bajo de la región** [S17][S18][S21];
   - **caducan rápido**.

   Usarlos como lista de reproducción secundaria del canal B (por ejemplo, "monotributo en una planilla") y no más del ~10% del calendario (E).
3. **Hispanos de EE. UU.:** son una ventaja posible y no la base [S75][S76]. Incluir piezas del tipo "herramientas y planillas para trabajar o emprender en EE. UU." para atraer geografía de alto RPM [S15].
4. **Infraestructura de cobro desde Argentina:**
   - AdSense por wire o Western Union [S10][S11];
   - W-8BEN antes del 10 de diciembre [S12];
   - Factura E y consulta a un contador [S71];
   - Mercado Pago para Mercado Libre [S56];
   - Payoneer o PayPal para SaaS [S64][S67][S68].

---

## 8. Mitigación de riesgos de plataforma (aplica a ambos canales)

- **Contenido inauténtico** [S39][S40]:
  - variar formatos (tutorial, caso, comparativa, error común, desafío);
  - variar las plantillas visuales;
  - guiones con datos y pruebas propias;
  - nada de "relleno" generado en masa;
  - revisar manualmente antes de publicar.
- **Divulgación de IA** [S42][S43]:
  - los visuales no realistas (gráficos, interfaces simuladas) no requieren etiqueta;
  - el anuncio original de YouTube cita como ejemplo que requiere divulgación "generar sintéticamente la voz de una persona para narrar un video" [S42];
  - **si la voz TTS suena realista, marcar "Sí" en el campo de uso de IA de YouTube Studio y declarar "voz generada con IA" en la descripción**. La etiqueta no afecta recomendaciones ni monetización [S43], así que el costo de declarar es bajo (E);
  - no simular personas reales.
- **Música:** evitar pistas con licencia en los Shorts para no ceder el 50% al pool de música [S05].
- **Exactitud:** en el canal B, cada fórmula debe pasar un test automático antes de publicarse. En el canal A, fechar las versiones de las herramientas en pantalla.

---

## 9. Datos que conviene medir en los primeros 90 días (para reemplazar estimaciones)

1. Distribución geográfica de la audiencia (porcentaje de MX, AR, CO, CL y EE. UU.) en YouTube Studio.
2. RPM real de Shorts y de videos largos por canal, apenas se habilite la monetización.
3. Clics y conversiones por afiliado, usando un link con UTM por video.
4. Retención media de los Shorts según formato visual (planilla animada, interfaz simulada, tipografía cinética).
5. Horas de visualización acumuladas por mes frente a la meta de 8.000 horas en 12 meses.
