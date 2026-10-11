# Fichas que conviene verificar a mano antes de publicar

Lista generada a partir de los informes de los guionistas: el sistema valida cálculos y riesgos de forma automática,
pero las rutas de menú de aplicaciones de terceros cambian y no siempre tienen documentación oficial accesible.

| ID | Qué verificar | Motivo |
|---|---|---|
| A-026 | Ruta del "mensaje de ausencia" en WhatsApp Business | No se encontró página oficial de faq.whatsapp.com; el guion evita rutas exactas ("el nombre puede variar según versión") |
| A-019 | Nombre en español del asistente "Texto en columnas" (Delimitado → Punto y coma) | Documentación consultada en inglés |
| A-013 | Límite de destinatarios diarios de MailApp (cuentas personales) | Cuota que Google puede cambiar; el guion dice "a la fecha" |
| A-004 | Ruta Configuración > Personalización en ChatGPT | Interfaz cambiante; el guion dice "a la fecha" |
| B-023 | Opción "Centrar en la selección" (Formato de celdas > Alineación) | Solo respaldo en artículo antiguo de Microsoft y guías de terceros |
| B-020 | FECHANUMERO (Latinoamérica) vs VALFECHA (España) | Nombre de función según configuración regional |
| B-013 | Nombre "Relleno rápido" y atajo Ctrl + E en Excel en español | Documentación consultada en inglés |
| B-014 | Texto del aviso del triángulo verde ("Convertir en número") | No se confirmó el texto exacto del menú; el guion lo describe sin nombrar el botón |
| B-007 | Nombre de TEXTJOIN en Google Sheets en español | Se usó el nombre en inglés |
| A-035 | Explicación causal de alucinaciones (OpenAI, "Why language models hallucinate") | Leída solo en resultados de búsqueda |
| A-039 | Resumen de NIST SP 1270 (sesgo técnico, humano y sistémico) | Leído solo en resúmenes |
| A-041 | "100 tokens ≈ 75 palabras en inglés" y relación tokens-conteo de letras | Explicación parcial; se mantiene "puede fallar" |
| A-045 | Preprint arXiv 2603.03299 citado como fuente | Confirmar disponibilidad y contenido |
| A-046 | Guía de OpenAI sobre modelos de razonamiento ("a la fecha") | Puede haber cambiado |
| A-047 | Limitaciones de lectura de imágenes según ayuda de OpenAI | Varias versiones de la página |
| A-040 | "Comillas triples" (curso DeepLearning.AI) | La fuente oficial verificada habla de etiquetas XML |
| A-049 | Cifras del Foro Económico Mundial 2025 (170 M, 92 M, 78 M, 22 %, "cerca del 40 %") | Proyecciones; revisar contra el informe original |
| A-053 | Ayuda de OpenAI "Does ChatGPT tell the truth?" | Citada desde resumen de búsqueda |
| A-055 | Contrastes vos/tú y computador/computadora por país | Revisión por hablantes de cada país recomendada |
| A-057 | Técnica "hazme preguntas antes de responder" | Sin fuente; probar en dos asistentes |
| A-058 | Temperatura como ajuste de la API ("a la fecha") | Documentación cambiante |
| A-060 | Windows + H (dictado) en Windows 11 | Probar el atajo (10 s) |
| A-061 | Disponibilidad de modelos por plataforma | Cambia con frecuencia |
| A-063 | 26 % de aciertos, 9 % falsos positivos y retiro del clasificador de OpenAI (20-jul-2023) | Visto en resumen de búsqueda; revisar el original |
| A-052 | Script Python de renombrado en Windows/macOS | Probado solo en Linux (modo simulación por defecto) |
| B-049 | Equivalencias VLOOKUP=BUSCARV, COUNTIFS=CONTAR.SI.CONJUNTO, NETWORKDAYS=DIAS.LAB | Comprobar en un Excel en español |
| B-052 | GOOGLEFINANCE("CURRENCY:USDMXN") y demora de hasta 20 min | Probar la fórmula en una hoja real |
| B-053 | Menús Insertar > gráfico de barras apiladas en español | No verificado en interfaz en español |
| B-056 | Roles y botón Compartir en Sheets (cuenta personal vs Workspace) | Puede variar |
| B-057 | DIAS.LAB cuenta ambos extremos; resultado esperado 7 | Probar con las fechas del ejemplo |
| B-060 | Disponibilidad de TRADUCIR/STOCKHISTORY en Excel | Cambia por versión |
| B-061 | La validación no siempre actúa sobre datos pegados | Sin página oficial |
| B-063 | Inicio > Formato condicional > Barras de datos (nombres en español) | Ayuda consultada en inglés |
| B-034 | Tasas generales de IVA: MX 16 %, CO 19 %, CL 19 %, AR 21 % | Confirmar el día de publicar |
| B-035 | Menús Vista > Inmovilizar paneles (Excel) y Ver > Inmovilizar (Sheets) | Nombres de menú |
| B-038 | Intereses totales bola de nieve 961,32 vs avalancha 698,15 | Replicar en una planilla |
| B-039 | Formato `0,0." k"` (coma decimal) vs `0.0," k"` (punto decimal) | Probar en ambas configuraciones |
| B-040 | Historial de versiones (Excel en OneDrive; Sheets "Última edición") | Probar con cuentas reales |
| B-043 | =TEXTO(A2;"dddd, d ""de"" mmmm") → "lunes, 5 de enero" | Probar en Excel y Sheets en español |
| B-044 | INT.EFECTIVO(24%;12) = 26,82 % | Verificar nombre de la función en español |
| B-047 | Regla 50/30/20 | Fuente no oficial; se presenta como guía popular |
| B-048 | Insertar > Segmentación (Excel); "control de filtros" (Sheets) | Nombres según plataforma |
