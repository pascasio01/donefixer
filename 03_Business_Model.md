# DONEFIXER — 03 · Business Model

> **Nombre oficial:** DONEFIXER · **Categoría:** Enterprise Maintenance & Operations Platform
> **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 1, 2026-07-29)
> **Advertencia de integridad:** TODAS las cifras de este documento son **hipótesis (SU)** salvo los precios públicos de competidores citados con fuente (DC a su fecha). Nada aquí es una proyección financiera comprometida. Las hipótesis se validan o refutan en pilotos (registro §16).

---

## 1. Objetivo
Definir cómo DONEFIXER crea, entrega y captura valor: segmentos, planes, hipótesis de precios, canales, costos y unit economics preliminares, con trazabilidad total a la evidencia de mercado (doc 04) y a la visión (doc 01).

## 2. Alcance
Modelo SaaS B2B para CMMS/EAM/FM; LatAm inicial, EE. UU. posterior (DC estratégica). Incluye implementación, onboarding, soporte, servicios profesionales e integraciones como líneas de valor/costo.

## 3. Exclusiones
No es un plan financiero formal ni una valoración; no incluye estructura fiscal (PD N-7: país de incorporación); no constituye asesoría legal ni contable.

---

## 4. Segmentos de clientes

| Segmento | Descripción | Tamaño típico | Qué compra | Prioridad |
|---|---|---|---|---|
| **S1 — PyME industrial/operativa LatAm** | Planta, logística, hotelería, salud privada pequeña, retail con mantenimiento propio | 3–25 usuarios técnicos | Salir de Excel/WhatsApp; OTs, PM, evidencias | **Inicial (Fase 1–2)** |
| **S2 — Mid-market multi-sitio** | Cadenas, facility managers regionales, plantas con 2–20 sitios | 25–200 usuarios | Multi-sitio, proveedores, KPIs, IA agentiva | Fase 2–3 |
| **S3 — Enterprise / corporativo** | Corporativos, gobierno, salud grande, farma | 200+ usuarios | SSO/SCIM, residency, auditoría, SLAs, EAM completo | Fase 4–5 (requiere SOC 2) |
| **S4 — Facility Management como servicio (futuro)** | Empresas FM que operan para terceros | Variable | Multi-cliente, portales, SLAs por contrato | Fase 3+ (PD: modelo multi-cliente dentro de un tenant) |

## 5. Buyer personas vs. user personas

| Persona | Rol en la compra | Dolor | Objeción esperada |
|---|---|---|---|
| **Buyer: Gerente de Mantenimiento / Operaciones** | Decide en S1–S2 | KPIs tardíos, equipo apagando incendios | "Ya probamos un software y nadie lo usó" → respuesta: adopción frontline medible en piloto |
| **Buyer: Director/Propietario (S1)** | Aprueba el gasto | No ve el ROI; teme costos ocultos | "Excel es gratis" → respuesta: costo del downtime y del trabajo manual (hipótesis §11) |
| **Buyer: Gerente General / CFO (S2–S3)** | Aprueba contrato | Riesgo de proveedor nuevo sin certificaciones | "¿Tienen SOC 2?" → respuesta honesta: roadmap de cumplimiento (doc 38); venta enterprise solo cuando exista |
| **User: Técnico** | No decide, pero **veta con su no-adopción** | Herramientas lentas, sin señal, en inglés | "Esto es más trabajo para mí" → respuesta: ≤3 toques, offline total, voz/foto |
| **User: Supervisor** | Influencia fuerte | Cuadra horarios en papel | — |

## 6. Propuesta de valor por segmento
S1: *"Deja el Excel en una semana: tus técnicos reportan desde el celular, aunque no haya señal."* · S2: *"Todos tus sitios, proveedores y facturas en una sola verdad, con IA que hace el papeleo."* · S3: *"EAM enterprise sin implementación de 18 meses."* (Todas SU hasta validación con pilotos.)

## 7. Modelo SaaS y planes (hipótesis de diseño — SU; anclada en precios verificados del mercado, doc 04 §7)

| Plan | Precio hipotético (SU) | Contenido | Ancla de mercado (DC) |
|---|---|---|---|
| **Gratis** | $0 | OTs ilimitadas, 1 sitio, 3 usuarios, solicitantes ilimitados, app offline | MaintainX/Fiix/Limble tienen plan gratis [^27^][^29^][^30^] |
| **Profesional** | **$25–35/usuario/mes** (LatAm) / $35–45 (EE. UU. futuro) | Multi-sitio básico, PM por medidor, inventario, KPIs automáticos, **copiloto IA con cuota**, WhatsApp intake | Bajo Fiix Basic $45 y MaintainX Essential ~$20–65 [^29^][^27^] |
| **Business** | **$50–60/usuario/mes** | Proveedores, compras/facturas con agente IA, portales, automatización, API, i18n completo | Bajo Fiix Pro $75 con IA incluida vs. Fiix que cobra IA desde $75 [^31^] |
| **Enterprise** | Por sitio/contrato (custom) | SSO/SCIM, residency, auditoría avanzada, SLAs, EAM, soporte prioritario | Custom en todo el mercado [^27^] |

**Reglas del modelo (DC de diseño):** (1) los **solicitantes nunca pagan asiento** — motor viral interno; (2) la IA **se incluye con cuotas desde Profesional** — corregida la contradicción F-2 de auditoría con límites por plan (AUD-00 D-7); (3) **no competir por debajo del rango** — la diferenciación es offline+IA+LatAm, no precio (doc 04 §12); (4) precios regionales por país, revisión trimestral contra competidores.

*Decisión requerida del Fundador (PD): aprobar rangos y moneda(s) de lanzamiento; validar disposición de pago real en entrevistas de pilotaje.*

## 8. Implementación y onboarding (SU hasta doc 64)
Objetivo: cliente S1 operativo en **<7 días** (benchmark de mercado cloud [^30^], adoptado como meta, no promesa contractual — H-23 AUD-00). Palancas: importador Excel/CSV (doc 63), plantillas por industria, catálogos precargados, onboarding guiado en app. Implementación asistida de pago opcional para S2+ (servicio profesional, §11).

## 9. Soporte (SU hasta doc 65)
Fase 1: soporte por el Fundador, horario declarado honestamente en ToS de piloto (PD N-9); chat/email; base de conocimiento bilingüe. Fase 2+: soporte en español/portugués con SLA por plan. Nunca prometer 24/7 sin poder cumplirlo (principio §9 del Charter).

## 10. Integraciones como línea de valor
API pública y webhooks desde Business (mercado las cobra en planes altos [^27^]); conectores ERP contables regionales (PD: cuáles, por país) en Fase 4; WhatsApp Business API como canal (costo por conversación Meta — costear en FinOps, H-25).

## 11. Costos y líneas de ingreso adicionales
**Ingresos:** suscripciones (principal), implementación asistida S2+, servicios profesionales (migración histórica, integraciones a medida — acotados para no convertirse en consultora), overage de IA.
**Costos (SU, detalle en doc 60):** infra Etapa A $150–500/mes; LLM API (variable, con cuotas); WhatsApp/SMS/email; stores ($99/año Apple + $25 Google); herramientas; legal por jurisdicción (PD N-3); soporte; auditorías SOC 2 en Etapa B (~$20–50K/año, SU); personal futuro (PD N-10).

## 11 bis. Sensibilidad de precios y estructura de costos (ampliación exigida por aprobación condicional Ola 1)

> **Todas las cifras de esta sección son SU (hipótesis de planificación)** salvo los costos de terceros citados con fuente y fecha. No son proyecciones financieras. Cada hipótesis tiene su mecanismo de validación.

### 11 bis.1 Sensibilidad de precios (SU)

Escenarios por plan Profesional, cliente S1 típico de 10 asientos, con tres niveles de adopción de add-ons. La variable sensible no es el precio de lista sino la **relación precio/adopción**: un precio 20% menor con adopción igual genera menos ingreso sin reducir costo de servicio — por eso la palanca de diseño es la adopción, no el descuento (INF).

| Escenario | Precio/asiento/mes | 10 asientos (MRR/cliente) | Efecto esperado | Riesgo |
|---|---|---|---|---|
| Conservador | $20 | $200 | Máxima conversión; posible percepción de "barato = menor" | Margen fino si soporte/IA suben; ancla a la baja difícil de revertir |
| **Base (recomendado SU)** | **$28** | **$280** | Equilibrio conversión/margen; bajo Fiix $45 y MaintainX Premium $65 (DC doc 04) | Validar disposición de pago (HV-1) |
| Aspiracional | $40 | $400 | Margen alto si el valor se demuestra | Churn de precio en S1 LatAm; requiere ROI documentado en piloto |

**Reglas de sensibilidad (DC de diseño comercial):** (1) nunca bajar precio para cerrar una venta — bajar alcance o dar período extendido de prueba; (2) subidas de precio solo con 60+ días de aviso y clientes existentes protegidos 12 meses (grandfathering); (3) el plan gratis nunca compite con el de pago (límite de 1 sitio y 3 usuarios); (4) precio por país según paridad de poder adquisitivo, revisado trimestralmente contra competidores (doc 04).

### 11 bis.2 Costos de soporte (SU)

| Fase | Modelo | Costo estimado | Hipótesis clave |
|---|---|---|---|
| Fase 1 (5–30 clientes) | Fundador directo (N-9: A+B ligero) | $0–100/mes herramientas | 1 ticket/cliente/semana × 20 min = carga asumible hasta ~30 clientes |
| Fase 2 (30–100) | + FAQ asistido IA, base de conocimiento bilingüe | $100–400/mes | IA resuelve 40–60% de FAQs (validar; sin IA en compromisos con clientes — doc 33) |
| Fase 3 (100+) | Primera contratación de soporte o soporte compartido | $1.5–4K/mes (N-10) | Costo de soporte objetivo: **≤8% del MRR** |
| Enterprise (Fase 5) | Soporte prioritario con SLA | Incluido en precio enterprise | SLA solo con capacidad real de cumplirlo (regla Charter §9) |

**Métrica de control:** costo de soporte por cliente/mes y tickets por cliente/mes; si tickets/cliente no **bajan** con cada release, el producto está generando trabajo en lugar de eliminarlo (señal de calidad, no solo de costo).

### 11 bis.3 Costos de IA (SU — los más volátiles del modelo)

Estructura de costo por caso de uso (routing por costo, ADR-007):

| Caso de uso | Modelo | Costo unitario estimado (SU) | Presupuesto/tenant/mes (Profesional) |
|---|---|---|---|
| Triage de solicitudes, clasificación | Modelo pequeño | $0.0005–0.002/solicitud | ~$1–3 |
| Resúmenes de OT, notas de voz→texto | Modelo pequeño | $0.001–0.01/OT | ~$2–5 |
| Copiloto (consultas NL con RAG) | Modelo medio | $0.01–0.05/consulta | ~$5–15 (con cuota) |
| Agente: validación de facturas | Modelo grande | $0.05–0.30/factura | Plan Business |
| Generación de procedimientos | Modelo grande, bajo volumen | $0.10–0.50/procedimiento | Plan Business |

**Mecanismos de contención (DC):** cuotas por plan con overage de pago; routing al modelo más barato que supere el umbral de calidad del golden-set (doc 33); caché de respuestas para consultas repetidas; opt-out por tenant. **Línea roja FinOps (heredada de criterio de fracaso del Charter):** costo de IA >30% del ingreso por tenant de forma sostenida → rediseño del modelo de IA o de precios. **Métrica primera clase:** costo de IA por tenant/mes visible en la consola de plataforma (ADR-012 §3.7).

### 11 bis.4 Costos de implementación (SU)

| Tipo | S1 autoservicio | S2 asistida | S3 enterprise |
|---|---|---|---|
| Esfuerzo | 2–4 h del cliente con importador + plantillas | 2–5 días del equipo DONEFIXER | 4–12 semanas + integraciones |
| Costo para DONEFIXER | ~$0 marginal | $500–2K/cliente (tiempo) | $10–50K/proyecto |
| Se cobra | No (incluido) | Sí: $1–5K (SU) | Sí: cotización |
| Hipótesis a validar | HV-6 (migración Excel <1 día decide la compra) | ROI de la implementación asistida ≥3× | Venta enterprise cubre implementación y deja margen |

**Regla:** la implementación asistida es un **servicio acotado con precio de lista**, nunca consultoría abierta — el riesgo mortal de los SaaS pequeños es convertirse en consultora que financia el producto con horas (INF de patrones del sector).

### 11 bis.5 Márgenes estimados por plan (SU)

| Plan | Ingreso/asiento | Costo variable/asiento (infra+IA+soporte+mensajería) | Margen bruto estimado |
|---|---|---|---|
| Gratis | $0 | $0.50–2 | Negativo (inversión de adquisición; techo presupuestado en FinOps) |
| Profesional $28 | $28 | $3–7 | **75–89%** |
| Business $55 | $55 | $6–12 | **78–89%** |
| Enterprise | Contrato | Negociado con margen mínimo 70% | ≥70% (regla) |

**Supuestos declarados:** infra Etapa A $150–500/mes amortizada entre clientes; IA con cuotas dentro de presupuesto; soporte dentro del 8% MRR; sin WhatsApp masivo aún (costo por conversación Meta se añade como variable cuando HV-5 se valide). **Sensibilidad:** el margen es más vulnerable al costo de IA y al soporte que a la infraestructura — por eso ambos tienen líneas rojas y métricas propias.

---

## 12. Unit economics preliminares (hipótesis SU — NINGÚN dato real aún)

| Métrica | Hipótesis | Cómo se valida |
|---|---|---|
| ARPU mensual S1 | $150–400/cliente/mes (5–15 asientos × $25–35) | Primeras 10 ventas |
| Gross margin SaaS | 75–85% (infra Etapa A baja; IA con cuotas) | FinOps mensual real |
| CAC S1 | $200–800 (canales orgánicos/directos, §13) | Medición desde el día 1 |
| LTV (churn 2–4%/mes asumido) | 12–30 meses de vida × ARPU × margen | Real solo con 12 meses de datos |
| LTV/CAC objetivo | >3 antes de escalar gasto comercial | Gate para inversión en marketing |
| Churn aceptable | <3%/mensual en S1 (SU de referencia SaaS B2B) | Cohorte real |

**Escenario de viabilidad mínima (SU ilustrativo, no proyección):** 50 clientes S1 × $250/mes ≈ $12.5K MRR, con costos Etapa A <$1K/mes + herramientas ≈ margen bruto >80% y punto de equilibrio operativo alcanzable con equipo mínimo. Este escenario existe para demostrar que el modelo **puede** ser viable a pequeña escala — no afirma que ocurrirá.

## 13. Canales de adquisición (prioridad por costo)

1. **Pilotos directos del Fundador** (red profesional, asociaciones de mantenimiento locales) — canal dominante Fase 1.
2. **Contenido técnico bilingüe** (guías de MTTR/PM/migración desde Excel) — SEO LatAm de baja competencia (INF).
3. **Plan gratuito + solicitantes ilimitados** como expansión interna bottom-up (patrón observado en MaintainX [^27^]).
4. **Alianzas:** consultoras de mantenimiento, proveedores de repuestos, cámaras de industria (PD).
5. **Pago:** no antes de LTV/CAC validado (gate §12).

## 14. Riesgos comerciales

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Disposición de pago LatAm menor a la hipótesis | Media | Crítico | Validar precio en pilotos ANTES de fijar planes; plan gratis generoso |
| Ciclo de venta largo incluso en S1 | Media | Alto | Onboarding <7 días, prueba sin fricción |
| Churn por no-adopción del técnico | Media | Crítico | Adopción frontline como métrica de salud del cliente |
| Costo de IA erosiona margen | Media | Medio | Cuotas, routing por costo, overage (doc 60) |
| Dependencia del Fundador como vendedor único | Alta | Alto | Documentar playbook de venta; canal 3 (producto viral) reduce dependencia |
| Competidor copia WhatsApp/offline | Media | Medio | Velocidad + barreras de datos (doc 04 §9) |

## 15. Estrategia de expansión
Tierra y expansión: plan gratis → Profesional por adopción → Business por proveedores/IA → Enterprise por compliance. Geográfica: país origen → 1–2 LatAm (PD-3) → Brasil/Caribe (Fase 3, PT/FR/HT) → EE. UU. (Fase 5, con SOC 2 obtenido y mercado hispanohablante de técnicos como puente — hipótesis H-VAL de doc 04 §5.2). Vertical: horizontal hasta Etapa C; verticales solo con cliente ancla (doc 01 §13).

## 16. Hipótesis que requieren validación (registro H-VAL)

| # | Hipótesis | Validación | Fecha límite |
|---|---|---|---|
| HV-1 | S1 paga $25–35/usuario/mes en LatAm | Entrevistas + primeras ventas piloto | Fin Fase 1 |
| HV-2 | Adopción frontline >80% alcanzable en pilotos | Métrica de producto | Fin Fase 1 |
| HV-3 | Solicitantes gratis generan expansión interna | Tracking de conversión | Fase 2 |
| HV-4 | IA con cuota en Profesional mantiene margen ≥75% | FinOps real por tenant | Fase 2–3 |
| HV-5 | WhatsApp intake triplica velocidad de reporte vs. portal | A/B en pilotos | Fase 1–2 |
| HV-6 | Migración Excel <1 día decide la compra | Entrevistas de cierre | Fase 1 |
| HV-7 | Mercado hispanohablante EE. UU. como puente | Pilotos con empresas US hispanas | Fase 4–5 |

## 17. Decisiones requeridas del Fundador (PD consolidadas)
PD-1 Rangos de precios y moneda(s) · PD-3 Países de pilotaje · PD N-3 Presupuesto legal · PD N-4 Procesador de pagos (Stripe vs. regional) · PD N-7 País de incorporación (bloquea fiscalidad y residencia de datos) · PD N-9 Modelo de soporte Fase 1 · PD N-10 Solo o con contrataciones.

## 18. Referencias cruzadas
Depende de: 04 (evidencia de precios/mercado), 01 (visión/segmentos), 02 (restricciones), AUD-00 (FinOps D-7, H-25, H-28). Alimenta: 05 Business→08 North Star, 43 spec billing (módulo 40 del índice), 54 entitlements, 60 FinOps, 64 onboarding, 65 soporte, 69 roadmap.

## 19. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 1). Planes con anclas de mercado verificadas; contradicción IA/margen resuelta con cuotas (AUD-00 D-7); todas las cifras propias etiquetadas SU con registro de validación HV |
| 1.1 | 2026-07-29 | **Ampliación por aprobación condicional Ola 1:** nueva §11 bis — sensibilidad de precios (3 escenarios), costos de soporte, costos de IA por caso de uso con línea roja FinOps, costos de implementación, márgenes estimados por plan. Todo clasificado SU con mecanismos de validación |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 1** por el Fundador. Base estratégica oficial; no congelado: futuras modificaciones por gobierno documental (evidencia, trazabilidad, ADR, versionado, motivo) |
