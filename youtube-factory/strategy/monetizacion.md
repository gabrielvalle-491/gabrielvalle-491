# Plan de monetización (los dos canales)

> **No hay ingresos garantizados.** Este documento separa los **datos observados**, marcados (O) con su fuente en
> `research/investigacion_nichos.md`, de las **estimaciones**, marcadas (E). Reemplazá las estimaciones por tus datos reales
> de YouTube Studio a medida que existan.

## 1. Restricciones que condicionan todo
- **YPP (O):** hoy pide 1.000 suscriptores y además 4.000 horas de videos largos en 12 meses o 10 M de vistas de Shorts en 90 días.
- **Cambio anunciado (O, fuentes secundarias, verificar):** desde el 1-feb-2027 los solicitantes nuevos necesitarían 8.000 horas o 20 M de vistas de Shorts. Por eso **los videos largos son un pilar y no un extra**: las vistas en el feed de Shorts no suman horas.
- **RPM de Shorts en LatAm (O):** ~0,04 USD por 1.000 vistas en México, frente a ~0,33 en EE. UU. **Los Shorts sirven para descubrimiento, no para facturar.**
- **RPM de video largo (O/E):** medianas medidas de ~2 USD en Business & Finance y ~2,3 USD en Tech. Para audiencia latinoamericana se planifica con 0,5–3 USD (E).
- **Contenido inauténtico (O):** si se detecta producción masiva y repetitiva, puede retirarse la monetización de todo el canal. La fábrica mitiga ese riesgo con guiones originales, variedad de plantillas y estructuras, cálculos propios, control de duplicados y revisión humana.

## 2. Vías por canal
| Vía | Atajo IA | Celda Clara | Condiciones de acceso (verificar antes de usar) |
|---|---|---|---|
| Publicidad YouTube | Sí, después del YPP | Sí, después del YPP | Umbrales del YPP; AdSense paga a Argentina por transferencia o Western Union; cargar el formulario W-8BEN |
| Afiliados SaaS | **Principal** | Secundaria | PartnerStack (paga vía Airwallex o PayPal), Hostinger y Canva: cada programa aprueba por su cuenta y algunos tienen restricciones por país |
| Mercado Libre Afiliados / YouTube Shopping | Secundaria | **Sí** (útiles de oficina y tecnología) | En AR, programa lanzado en nov-2025 (al inicio solo para monotributistas). Shopping desde 500 suscriptores en MX y AR (fechas por confirmar) |
| Productos digitales propios | Biblioteca de prompts | **Plantillas de planilla** | Hotmart acepta productores de Argentina; también se puede usar una tienda propia |
| Membresías y Super Thanks | Desde 500 suscriptores | Desde 500 suscriptores | YPP ampliado |
| Patrocinios | Herramientas de productividad o IA | Software de gestión o finanzas educativas | Siempre declarados con la casilla de promoción pagada |

**Enlaces de afiliado:** `config/canal_*.yaml → enlaces_afiliado` está **vacío a propósito**. Solo se completa con enlaces
reales aprobados. Una ficha los usa con `afiliados: [clave]`, y la divulgación se agrega sola a la descripción.

## 3. Escenarios a 12 meses (E: todos los números son supuestos explícitos)
| Supuesto | Conservador | Intermedio | Optimista |
|---|---|---|---|
| Vistas mensuales de Shorts por canal (mes 12) | 30.000 | 250.000 | 1.500.000 |
| Vistas mensuales de videos largos por canal (mes 12) | 1.500 | 10.000 | 50.000 |
| ¿Entra al YPP en 12 meses? | No | Probable en meses 9-12 | Sí, en meses 5-8 |
| RPM de Shorts (USD por 1.000) | 0 (sin YPP) | 0,04 | 0,06 |
| RPM de video largo (USD por 1.000) | 0 (sin YPP) | 1,0 | 2,5 |
| Clics a afiliados (% de vistas de largos) | 0,5 % | 1 % | 1,5 % |
| Conversión del afiliado | 2 % | 3 % | 4 % |
| Comisión promedio (USD) | 10 | 15 | 20 |
| Ventas de plantillas por mes (Celda Clara) | 0-2 × USD 5 | 10 × USD 7 | 60 × USD 9 |
| **Ingreso mensual estimado por canal (mes 12)** | **≈ USD 0-15** | **≈ USD 25-90** | **≈ USD 300-900** |

Cómo se calcula (intermedio, un canal):
- Shorts: 250.000 / 1.000 × 0,04 = USD 10.
- Videos largos: 10.000 / 1.000 × 1,0 = USD 10.
- Afiliados: 10.000 × 1 % × 3 % × 15 = USD 45.
- Plantillas: hasta USD 70 en Celda Clara.

La comisión de Hotmart reduce el ingreso por plantillas.

**Lo que todavía no se sabe:**
- la geografía real de la audiencia;
- la retención real;
- la tasa de aprobación de los programas de afiliados;
- el RPM real del canal;
- la conversión de las plantillas.

El informe semanal (`python fabrica.py informe <canal>`) se diseñó para medir eso.

## 4. Orden recomendado
1. **Días 1-30:** publicar, medir y no monetizar todavía. Crear la cuenta de Hotmart y postular a programas de afiliados (lo hace el humano).
2. **Días 30-60:** primera plantilla propia de Celda Clara (control de gastos o cotizaciones) y una biblioteca de prompts para Atajo IA. Agregar los enlaces reales a la configuración.
3. **Días 60-90:** según el informe semanal, más videos largos en los pilares con mejor retención. Postular a Mercado Libre Afiliados si aplica.
4. **Fiscal (Argentina):** facturar con Factura E y consultar a un contador antes del primer cobro. Esto no es asesoramiento.
