# DONEFIXER — 01 · Product Vision

> **Nombre oficial:** DONEFIXER · **Categoría:** Enterprise Maintenance & Operations Platform
> **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 1, 2026-07-29)
> **Evidencia:** DC = confirmado · SU = supuesto · PD = pendiente de decisión · INF = inferencia. Toda afirmación de mercado remite al doc 04 (fuente canónica).

---

## 1. Objetivo
Declarar el problema, los usuarios, la visión temporal, la propuesta de valor y los límites de DONEFIXER, de modo que cualquier decisión futura pueda evaluarse contra una sola pregunta: **¿esto acerca al producto a su visión o lo aleja?**

## 2. Alcance
Producto completo en horizonte 10 años: CMMS → EAM → Facility Operations, LatAm primero, EE. UU. y otros mercados después (DC del Fundador).

## 3. Exclusiones
No define requisitos (doc 09–12), ni arquitectura (docs 20–33), ni planes comerciales detallados (doc 03). No promete disponibilidad, certificaciones ni capacidades no construidas.

---

## 4. El problema central

**Declaración del problema (soportada por doc 04):**

Los equipos de mantenimiento y operaciones viven una fractura triple:

1. **El trabajo ocurre donde el software no funciona.** Sótanos, cuartos mecánicos, techos, plantas con mala conectividad. Los CMMS móviles líderes ofrecen offline *parcial* (verificado, doc 04 §7–8): el técnico improvisa — papel, fotos sueltas, memoria — y el dato se pierde o se degrada. Sin dato confiable no hay KPIs, ni predictivo, ni IA: es la falla fundacional de la que dependen todas las demás (INF soportada: la adopción frontline determina la calidad del dato, doc 04 §2.3 investigación previa).
2. **El trabajo administrativo consume al equipo operativo.** Triage de solicitudes, asignación, conciliación de facturas de proveedores, reportes de fin de mes: los líderes mid-market no los resuelven estructuralmente (DC, doc 04 §8), y la IA que los resolvería está encerrada en planes enterprise [^31^][^27^].
3. **Las herramientas no hablan el idioma del equipo.** Ni el literal (inglés-only o traducciones pobres; WhatsApp ignorado como canal operativo en LatAm) ni el figurado (interfaces que exigen capacitación para un técnico con guantes a 40 °C).

El resultado medible en la industria (SU, referencias doc 04 §5 investigación previa): la mayoría de las plantas opera con OEE del 55–65% frente al 85% world-class, y una fracción significativa calcula sus KPIs manualmente con semanas de retraso.

**Quién lo sufre hoy:** el técnico (herramientas hostiles), el supervisor (datos tardíos), el gerente (KPIs inventados), el director (decisiones de CapEx a ciegas) y el solicitante (reporta y nunca sabe qué pasó).

---

## 5. Usuarios a los que servimos

Los siete perfiles operativos (detalle en docs 15/16/19): técnico de campo (usuario primario), planificador/despachador, supervisor/gerente de mantenimiento, solicitante, proveedor/contratista, administrador de activos, director de portafolio. **Regla de diseño permanente (DC): cuando dos usuarios compiten por una decisión de producto, gana el técnico de campo** — porque de su adopción depende la calidad del dato del que vive todo el sistema (INF soportada, doc 04).

## 6. Visión a 3, 5 y 10 años

### Visión a 3 años (2029)
Ser el CMMS de referencia en español: la herramienta que un equipo de mantenimiento latinoamericano adopta sin capacitación, que funciona sin internet de ciclo completo, y que devuelve a cada gerente sus KPIs (MTTR, MTBF, PM compliance) calculados solos. Pilotos convertidos en clientes de pago recurrentes en 2+ países LatAm; IA asistiva incluida en planes medios; migración desde Excel en horas. *(Resultados medibles en doc 08 North Star Metrics y doc 69 Roadmap.)*

### Visión a 5 años (2031)
Ser la plataforma de operaciones multi-sitio de LatAm: inventario→compras→proveedores→facturas conciliado por agentes con auditoría; mantenimiento disparado por condición real (IoT) en clientes industriales; expansión a Brasil (PT) y Caribe (FR/HT); SOC 2 Type II obtenido (no aspirado) abriendo ventas enterprise.

### Visión a 10 años (2036)
Una plataforma global de Enterprise Maintenance & Operations: EAM completo (TCO, CapEx, predictivo), Facility Operations multi-portafolio, presencia en EE. UU. y otros mercados, ecosistema de integraciones — con la misma base arquitectónica diseñada hoy, sin reescrituras (el dominio y las decisiones de fundación ya lo contemplan; verificable en docs 14, 25–27 y 69).

**Declaración de visión en una frase:**
> *Que ningún trabajo de mantenimiento vuelva a perderse entre el papel, el WhatsApp y la mala conectividad — y que el trabajo administrativo lo haga la máquina, con auditoría.*

## 7. Propuesta de valor

| Para | Propuesta | Evidencia de la brecha |
|---|---|---|
| Técnico | Ciclo completo de OT sin internet, ≤3 toques por tarea, sin capacitación | Offline parcial en todos los directos verificados (doc 04 §7) |
| Supervisor/Gerente | KPIs automáticos al cerrar cada OT; cero reportes manuales | Benchmarks de la industria calculados a mano (SU, doc 04 §5) |
| Solicitante | Reportar por WhatsApp/portal gratis y ver el estado | Portal/WhatsApp ❌ en líderes mid-market (DC, doc 04 §8) |
| Gerencia/Finanzas | Facturas de proveedores validadas por agente IA con auditoría | Vacío estructural en MaintainX/Fiix (DC) |
| Director | Rollup multi-sitio/portafolio sin plan enterprise de 6 cifras | Multi-sitio débil en mid-market (DC) |

## 8. Diferenciación (defendible, no cosmética)

1. **Offline-first de ciclo completo** validado en campo (difícil de copiar: es arquitectura, no feature).
2. **IA agentiva gobernada** (triage, asignación, facturas, reportes) con auditoría por decisión, incluida con cuotas desde planes medios.
3. **LatAm nativo:** español/PT/FR/HT, WhatsApp como intake, precios y soporte regionales.
4. **Migración desde Excel en horas** como arma de adopción (doc 63).
5. **Solicitantes ilimitados gratuitos** como motor viral interno.
*Advertencia de integridad:* la diferenciación 1, 2 y 4 no existe hasta construirla y validarla (SU). Esta visión no declara superioridad actual sobre nadie; declara el plan para alcanzarla.

## 9. Principios del producto (orden de precedencia — DC)

1. **El técnico primero** (mobile-first): si no lo usa el técnico, no existe el dato.
2. **Offline-first:** sin conectividad no hay excusa para perder trabajo.
3. **IA como capa de asistencia gobernada, nunca autoridad autónoma** (lista de prohibiciones en doc 33).
4. **Un dato, una verdad** (multi-tenant nativo, KPIs desde la operación real).
5. **Opinionated por defecto, configurable al escalar:** adopción en días, no meses.
6. **Diseñar para prevenir, detectar, contener, recuperar y aprender de fallos** — nunca prometer ausencia de errores (regla de integridad de la suite).

## 10. North Star

**North Star Metric candidata (PD — la decide el Fundador con datos de pilotos):**
> **Órdenes de trabajo completadas por semana con evidencia completa y sincronización exitosa.**

*Fundamento:* captura adopción frontline + calidad del dato + valor entregado en una sola cifra; la mueven técnicos (adopción), el producto (offline/sync) y la IA (menos fricción administrativa). *Alternativas:* OTs/semana (sin calidad), tiempo de ciclo solicitud→cierre (más lenta de mover), % de mantenimiento planificado (madura solo en clientes avanzados). *Métricas de apoyo y guardarraíles en doc 08.*

## 11. Outcomes esperados (hipótesis a validar en pilotos — SU)

| Outcome del cliente | Métrica | Hipótesis |
|---|---|---|
| Menos tiempo de reparación | MTTR | −20% en 6 meses de uso |
| Menos trabajo administrativo | Horas/semana del supervisor | −30% |
| Mejor cumplimiento preventivo | PM compliance | ≥85% sostenido |
| Solicitantes informados | % solicitudes con seguimiento sin llamada | ≥90% |
| Datos confiables | % OTs cerradas con evidencia completa | ≥80% |

*Ninguna es promesa contractual; son las hipótesis que los pilotos de Fase 1 deben confirmar o refutar (criterio de salida de fase, doc 69).*

## 12. Límites del producto

DONEFIXER **no es ni será** (hasta nueva decisión del Fundador): un ERP completo (se integra, no reemplaza); un sistema de nómina/RRHH (gestiona turnos y habilidades, no nómina); una plataforma BIM/CAD (almacena documentos, no modela); un sistema de gestión de seguridad EHS completo (gestiona permisos de trabajo e incidentes de mantenimiento, no programas EHS); un proveedor de hardware de sensores (es sensor-agnóstico por diseño — lección documentada de UpKeep, doc 04 §8).

## 12 bis. Qué NO será DONEFIXER (exclusiones explícitas anti-expansión)

> Sección exigida por la aprobación condicional de la Ola 1. Propósito: blindar el producto contra la expansión descontrolada del alcance — el riesgo R3 de la auditoría. Cada exclusión es **vinculante** hasta que el proceso de evaluación de funcionalidades del Charter (doc 02 §10 bis) la modifique con evidencia.

**DONEFIXER NO será:**

1. **Un ERP ni una suite financiera.** No contabilidad general, no tesorería, no facturación fiscal completa. Se integra con los ERPs que el cliente ya tiene; la frontera es: DONEFIXER gestiona la operación, el ERP registra la contabilidad.
2. **Un sistema de RRHH/nómina.** Gestiona turnos, habilidades y disponibilidad de técnicos en tanto afectan al despacho; nunca nómina, evaluación de desempeño ni expediente laboral.
3. **Una plataforma EHS completa.** Gestiona permisos de trabajo, LOTO e incidentes vinculados a mantenimiento; no programas de seguridad ocupacional, gestión ambiental ni salud ocupacional integrales.
4. **Un BIM/CAD ni herramienta de ingeniería.** Almacena y vincula documentos técnicos; no modela geometría ni edita planos.
5. **Un fabricante de hardware.** Sin sensores propios, sin gateways propios. Sensor-agnóstico por diseño permanente (lección documentada de UpKeep y Tractian — doc 04 §8 bis). Si el mercado exige hardware, se integra, no se fabrica.
6. **Un CRM de ventas ni una plataforma de marketing.** El portal de solicitantes gestiona solicitudes de servicio, no oportunidades comerciales.
7. **Una herramienta de gestión de proyectos generalista** (tipo Asana/Jira). Los "proyectos" en DONEFIXER son conjuntos de OTs con presupuesto de mantenimiento, no gestión de proyectos de conocimiento.
8. **Una red social ni plataforma de mensajería general.** El chat es contextual al trabajo (OT, activo, sitio); no canales sociales ni comunicación libre entre usuarios sin contexto operativo.
9. **Un proveedor de servicios de mantenimiento.** DONEFIXER no ejecuta mantenimiento ni compite con sus clientes facility managers; los habilita.
10. **Una plataforma de e-learning.** Checklists y procedimientos sirven al trabajo; no gestión de cursos ni certificaciones formativas.
11. **Un producto gratuito con publicidad.** El plan gratis es una inversión de adquisición con límites claros, nunca financiado por publicidad ni por venta de datos (prohibido además por privacidad — doc 36).
12. **Un clon de nadie.** Se estudian patrones de los líderes; no se copian interfaces, textos ni identidad (principio Charter §7.3).

**Mecanismo de defensa:** toda propuesta de funcionalidad que entre en conflicto con esta lista se rechaza por defecto; revertir una exclusión exige el proceso formal del Charter §10 bis con evidencia de demanda (≥5 clientes o pipeline material) + análisis de impacto en arquitectura y roadmap + ADR. **La lista de exclusiones es tan importante como el roadmap:** define lo que DONEFIXER puede llegar a ser precisamente porque declara lo que jamás intentará ser.

## 13. Exclusiones iniciales (Fases 0–2)

Marketplace de integraciones, despliegue on-premise, 21 CFR Part 11, CRDT colaborativo en tiempo real, gemelos digitales, AR, verticales reguladas, EE. UU. como mercado. Cada exclusión tiene su criterio de activación en el roadmap (doc 69) y en la auditoría (AUD-00 §E).

## 14. Métricas de esta visión

Además de la North Star: adopción frontline semanal (>80% en pilotos — criterio de fase), éxito de sincronización (>99.9%/día), % OTs creadas por canales automáticos (IA/PM/IoT) ≥30% en Fase 3, NPS de técnicos >50, churn de logos (doc 03), costo de IA por tenant dentro de presupuesto (doc 60).

## 15. Riesgos de la visión

| Riesgo | Mitigación |
|---|---|
| Visión demasiado amplia para un equipo pequeño | Fases estrictas; la visión es 10 años, la ejecución es CMMS primero (doc 69) |
| Diferenciadores copiados por líderes con más recursos | Velocidad + barreras de datos/red (doc 04 §9) + offline, el más difícil de copiar |
| Hipótesis de outcomes refutadas por pilotos | Criterios de salida honestos: pivotar o matar features, nunca maquillar métricas |
| Dependencia de un solo fundador | Esta suite documental + ADRs + handbook (doc 67) |

## 16. Decisiones pendientes (PD)

| # | Decisión | Bloquea |
|---|---|---|
| PD-1 | Aprobar posicionamiento (doc 04 §12) | Doc 03 |
| PD-2 | Confirmar North Star Metric definitiva | Doc 08 |
| PD-3 | Países exactos de pilotaje | Docs 03, 64 |
| PD-4 | Idiomas de lanzamiento Fase 1 (recomendación auditoría: ES+EN) | Doc 13, módulos |
| PD-5 | Validación de outcomes con pilotos reales (Fase 1) | Doc 69 criterio de salida |

## 17. Referencias cruzadas
Depende de: 04 (mercado — fuente de toda evidencia externa), 00 (gobernanza), AUD-00. Alimenta: 02 (Charter), 03 (Business Model), 05–08, 09 (PRD), 15/16 (personas/journeys), 69 (Roadmap).

## 18. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Versión canónica Ola 1. Hereda principios de la investigación previa; añade límites, exclusiones, North Star candidata, outcomes como hipótesis SU, PDs explícitas. Nombre oficial DONEFIXER |
| 1.1 | 2026-07-29 | **Ampliación por aprobación condicional Ola 1:** nueva §12 bis "Qué NO será DONEFIXER" — 12 exclusiones vinculantes anti-expansión con mecanismo de defensa vinculado al FEP del Charter |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 1** por el Fundador. Base estratégica oficial; no congelado: futuras modificaciones por gobierno documental (evidencia, trazabilidad, ADR, versionado, motivo) |
