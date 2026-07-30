# DONEFIXER — Constitución Técnica y de Producto: Índice Maestro de Documentación

> **Nombre oficial:** DONEFIXER
> **Categoría:** Enterprise Maintenance & Operations Platform (CMMS / EAM / Facility Management)
> **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Documento:** 00 — Índice Maestro y Constitución · **Versión:** 1.0 · Julio 2026
> **Estado:** Normativo. Este documento gobierna a todos los demás.
> **Regla de autoría:** la autoría del proyecto es exclusivamente de Pascasio Emmanuel Reynoso Reyes. Ningún documento de esta suite podrá atribuirla a otra persona ni cambiar el nombre DONEFIXER.
> **Regla de evidencia:** en toda la suite se distingue explícitamente entre **Decisión Confirmada (DC)**, **Supuesto (SU)** y **Pendiente de Decisión (PD)**. Ninguna estimación, recomendación o supuesto se presenta como hecho confirmado.

---

## 0. Estructura estándar obligatoria de cada documento

Todo documento de la suite (01–70) deberá contener, como mínimo y en este orden:

1. Objetivo
2. Alcance
3. Exclusiones
4. Decisiones confirmadas (con referencia al ADR o documento origen)
5. Decisiones pendientes (con propietario y fecha límite)
6. Supuestos
7. Dependencias (documentos y sistemas)
8. Riesgos (con probabilidad, impacto y mitigación)
9. Requisitos funcionales (identificados `RF-<MODULO>-###`)
10. Requisitos no funcionales (identificados `RNF-###`)
11. Seguridad
12. Privacidad
13. Accesibilidad
14. Pruebas (unitarias, integración, E2E, sync/offline, seguridad)
15. Métricas (de producto, técnicas y de negocio)
16. Criterios de aceptación
17. Definition of Done
18. Referencias cruzadas con otros documentos

Además: portada con nombre oficial, autoría, versión, estado (Borrador / En revisión / Aprobado / Normativo) y tabla de control de cambios. Los documentos de módulo (31–55) heredan los RNF globales del documento 08 y solo declaran excepciones o endurecimientos.

---

## A. Índice maestro definitivo

La suite se organiza en **9 volúmenes**. Los documentos heredados de la investigación previa (`/mnt/agents/output/donefixer/` — ahora renombrada conceptualmente a DONEFIXER) se absorben y quedan **superseded** por los documentos numerados correspondientes, sin perder contenido válido: todo dato confirmado migra a su documento canónico.

### Volumen I — Estrategia y Negocio

| # | Documento | Supersede a |
|---|---|---|
| 01 | Product Vision | Doc-02 §1 (investigación previa) |
| 02 | Product Charter | — (nuevo) |
| 03 | Business Model | Doc-01 §4 (precios de mercado) |
| 04 | Market and Competitor Research | Doc-01 completo |

### Volumen II — Requisitos y Experiencia

| # | Documento | Supersede a |
|---|---|---|
| 05 | Product Requirements Document (PRD) | Doc-02 §2–3 |
| 06 | Software Requirements Specification (SRS) | — (nuevo; formaliza RF/RNF) |
| 07 | Functional Requirements (catálogo global) | Doc-02 §4 (parcial) |
| 08 | Non-Functional Requirements (catálogo global) | Doc-03 §8, Doc-04 §5 |
| 09 | Roles and Permissions Matrix | Doc-02 §2, Doc-03 §7 (RBAC) |
| 10 | User Journeys | Doc-02 §2 |
| 11 | Information Architecture | — (nuevo) |

### Volumen III — Arquitectura

| # | Documento | Supersede a |
|---|---|---|
| 12 | Enterprise Architecture (vista de capas y gobierno) | Doc-03 §1–2, figura arquitectura |
| 13 | Architecture Decision Records (registro ADR-001…010+) | Doc-05 §2 |
| 14 | Web Architecture | Doc-03 §2 (React/TS) |
| 15 | Native Mobile Architecture | Doc-03 §2 (Flutter), §9 |
| 16 | Backend Architecture | Doc-03 §2 (.NET modular) |
| 17 | Data Architecture | Doc-02 §4, Doc-03 §8 (ADR-006/008) |
| 18 | Multi-Tenant Architecture | Doc-03 §3 (ADR-001) |
| 19 | Offline and Synchronization Architecture | Doc-03 §4 (ADR-002), figura sync |
| 20 | API and Integration Architecture | Doc-03 §7 (ADR-009) |
| 21 | Event and Workflow Architecture | Doc-03 §1.6, §6 (outbox, Kafka) |
| 22 | AI Architecture and Governance | Doc-03 §5 (ADR-007), Doc-04 §1.1–1.2 |

### Volumen IV — Seguridad, Privacidad y Cumplimiento

| # | Documento | Supersede a |
|---|---|---|
| 23 | Security Architecture | Doc-04 §1 |
| 24 | Privacy Program | Doc-04 §2 (GDPR/LGPD) |
| 25 | Legal and Compliance Framework | Doc-04 §2 |
| 26 | Identity and Access Management | Doc-03 §7 (SSO/SCIM), Doc-04 §1.1 |

### Volumen V — Experiencia y Diseño

| # | Documento | Supersede a |
|---|---|---|
| 27 | UX/UI Bible | — (nuevo; vacío detectado, ver §G) |
| 28 | Design System | — (nuevo) |
| 29 | Brand Guidelines | — (nuevo) |
| 30 | Accessibility Standard | — (nuevo; vacío detectado, ver §G) |

### Volumen VI — Módulos Funcionales y Portales

| # | Documento | Módulo de dominio origen (Doc-02 §4) |
|---|---|---|
| 31 | Work Order Module | Órdenes de trabajo |
| 32 | Asset and Equipment Module | Activos, jerarquía, medidores, códigos de falla |
| 33 | Facility and Property Operations Module | Sitios, zonas, espacios, capa FM |
| 34 | Preventive and Predictive Maintenance | Planes PM, triggers, ML predictivo |
| 35 | Inspection and Checklist Module | Rondas, inspecciones, procedimientos |
| 36 | Inventory and Parts Module | Inventario, almacenes, reorden |
| 37 | Supply and Procurement Module | Compras, requisiciones, facturas |
| 38 | Supplier Portal | Proveedores y contratos |
| 39 | Customer and Program Portals | Portal de solicitantes/inquilinos |
| 40 | Technician Portal | App móvil del técnico (vista funcional) |
| 41 | Supervisor and Manager Portals | Web de planificación y KPIs |
| 42 | Executive and Administration Portals | Portafolio, administración de tenant |
| 43 | Chat and Collaboration | Mensajería estilo frontline |
| 44 | Automatic Translation | i18n en tiempo real (ADR-010) |
| 45 | Voice, OCR and Computer Vision | Intake por voz/foto, evidencias |
| 46 | Documents and File Management | Adjuntos, manuales, S3 |
| 47 | Digital Signatures and Evidence | Firmas, evidencia legal, 21 CFR Part 11 (fase) |
| 48 | Notifications and Escalations | Notificaciones multicanal |
| 49 | Scheduling and Dispatch | Calendario, asignación, balanceo de carga |
| 50 | SLA and Priority Management | SLAs, prioridades, escalación de estados |
| 51 | Reporting and Analytics | OLAP, KPIs, dashboards, reportes programados |
| 52 | Automation Engine | Reglas de automatización + agentes IA operativos |
| 53 | Search and Knowledge Management | RAG, base de conocimiento, búsqueda global |
| 54 | Billing, Plans and SaaS Entitlements | Planes, feature flags por tenant, facturación SaaS |
| 55 | Audit and Compliance Evidence | Auditoría inmutable, evidencia SOC 2/ISO |

### Volumen VII — Plataforma de Ingeniería

| # | Documento | Supersede a |
|---|---|---|
| 56 | DevOps and CI/CD | Doc-04 §3.1 |
| 57 | Infrastructure as Code | Doc-03 §2 (K8s/Terraform) |
| 58 | Observability and SRE | Doc-04 §3.3 |
| 59 | Backup, DR and Business Continuity | Doc-04 §3.4 |
| 60 | Testing and Quality Engineering | Doc-04 §3.1 (calidad) |
| 61 | Performance Engineering | Doc-03 §8 (SLOs) |
| 62 | FinOps and Cost Management | Doc-04 §5 |
| 63 | Release and Deployment Strategy | Doc-03 §9, Doc-04 §3.2 |

### Volumen VIII — Operación Comercial y del Cliente

| # | Documento | Supersede a |
|---|---|---|
| 64 | Data Migration and Import Strategy | — (nuevo; vacío detectado, ver §G) |
| 65 | Customer Onboarding and Implementation | Doc-03 §9 (<7 días) |
| 66 | Support and Incident Management | — (nuevo) |
| 67 | App Store and Web Release Readiness | — (nuevo) |
| 68 | Documentation and Developer Handbook | — (nuevo) |

### Volumen IX — Gobierno de Entrega

| # | Documento | Supersede a |
|---|---|---|
| 69 | Roadmap and Delivery Plan | Doc-05 §1 |
| 70 | Production Readiness Review | — (nuevo; gate final) |

---

## B. Orden correcto de creación

El orden respeta las dependencias (§C). Dentro de cada ola, los documentos pueden elaborarse en paralelo; entre olas, no se inicia la siguiente sin aprobar la anterior.

**Ola 0 — Gobernanza (ya entregada):** 00 (este documento).

**Ola 1 — Verdad estratégica:** 04 (Mercado) → 01 (Visión) → 02 (Charter) → 03 (Modelo de negocio).
*Razón:* el modelo de negocio requiere precios de mercado verificados; la visión requiere la brecha competitiva confirmada.

**Ola 2 — Requisitos y personas:** 10 (Journeys) → 09 (Roles y permisos) → 05 (PRD) → 07 (RF) → 08 (RNF) → 06 (SRS) → 11 (Arquitectura de información).
*Razón:* los RF nacen de journeys y roles; el SRS formaliza; la IA de información ordena la navegación sobre los RF.

**Ola 3 — Arquitectura de fundaciones (irreversible):** 17 (Datos) → 18 (Multi-tenant) → 19 (Offline/Sync) → 16 (Backend) → 21 (Eventos/Workflow) → 20 (API/Integraciones) → 13 (ADRs, consolidando) → 12 (Enterprise Architecture, vista integradora) → 14 (Web) → 15 (Móvil) → 22 (IA y gobernanza).
*Razón:* datos, tenancy y sync son las tres decisiones irreversibles (ADRs 001/002/008); todo lo demás se apoya en ellas. El documento 13 registra formalmente lo decidido.

**Ola 4 — Confianza:** 23 (Seguridad) → 26 (IAM) → 24 (Privacidad) → 25 (Legal/Cumplimiento) → 55 (Auditoría y evidencia).

**Ola 5 — Experiencia:** 29 (Marca) → 28 (Design System) → 27 (UX/UI Bible) → 30 (Accesibilidad).
*Razón:* el design system requiere tokens de marca; la biblia UX los aplica; la accesibilidad norma ambos (WCAG).

**Ola 6 — Módulos:** en orden de valor y dependencia de dominio:
31 (OTs) → 32 (Activos) → 34 (PM/Predictivo) → 35 (Inspecciones) → 49 (Scheduling) → 50 (SLA) → 36 (Inventario) → 37 (Compras) → 38 (Proveedores) → 33 (Facility) → 39 (Portal cliente) → 40–42 (Portales técnicos/supervisión/ejecutivo) → 43 (Chat) → 44 (Traducción) → 45 (Voz/OCR/Visión) → 46 (Documentos) → 47 (Firmas) → 48 (Notificaciones) → 51 (Reporting) → 52 (Automatización) → 53 (Búsqueda/Conocimiento) → 54 (Billing/Entitlements).

**Ola 7 — Plataforma de ingeniería:** 56 → 57 → 58 → 59 → 60 → 61 → 62 → 63.

**Ola 8 — Operación comercial:** 64 → 65 → 66 → 67 → 68.

**Ola 9 — Entrega:** 69 (Roadmap, actualizado) → 70 (Production Readiness Review) → **autorización para programar**.

---

## C. Dependencias entre documentos

Reglas de dependencia explícitas (un documento no puede declararse "Aprobado" si sus predecesores no lo están):

| Documento | Depende de (bloqueantes) | Alimenta a |
|---|---|---|
| 03 Business Model | 04 | 54, 69 |
| 05 PRD | 01, 04, 10 | 06, 07, todos los módulos 31–55 |
| 07 RF globales | 05, 09, 10 | 06, módulos, 60 (pruebas) |
| 08 RNF globales | 05 | Todos (los módulos heredan) |
| 17 Data Architecture | 05, 07 | 18, 19, 16, 51, 64 |
| 18 Multi-Tenant | 17 | 19, 20, 23, 54, 59 |
| 19 Offline/Sync | 17, 18 | 15, 31–42 (todo módulo con datos de campo) |
| 20 API/Integraciones | 16, 18, 21 | 52, 53, 65, 68 |
| 21 Eventos/Workflow | 16, 17 | 48, 51, 52, 58 |
| 22 IA y Gobernanza | 20, 21, 23, 24 | 43, 44, 45, 49, 52, 53 |
| 23 Seguridad | 18, 20 | 24, 25, 26, 55, 60, 67, 70 |
| 26 IAM | 23 | 09 (matriz), 54 |
| 28 Design System | 29 | 27, 14, 15, 40–42 |
| 30 Accesibilidad | 28 (parcial) | 27, 14, 15, 60, 67, 70 |
| 31–55 Módulos | 05, 07, 08, 17, 18, 19, 20 (+22 si usan IA) | 51, 60, 70 |
| 54 Billing/Entitlements | 03, 18, 26 | 65, 69 |
| 56–63 Plataforma | 12, 16, 23 | 63, 70 |
| 64 Migración | 17, 18 | 65 |
| 65 Onboarding | 54, 64, 11 | 66, 69 |
| 69 Roadmap | 03, 05, todas las olas 1–7 | 70 |
| 70 PRR | **Todos los anteriores aprobados** | Autorización para escribir código |

**Cadena crítica (camino más largo):** 04 → 01 → 05 → 07 → 17 → 19 → módulos → 51 → 70. Esta cadena determina la fecha mínima de inicio de programación.

---

## D. Entregables de cada fase

| Fase / Ola | Entregables | Criterio de cierre de la ola |
|---|---|---|
| **0** | Documento 00 aprobado | Firmado por el Fundador |
| **1** | 01–04: visión, charter, modelo de negocio, investigación canónica | Ningún dato de mercado sin fuente; pricing hipotético marcado como SU |
| **2** | 05–11: PRD, SRS, RF/RNF numerados, matriz de roles, journeys, IA de información | Trazabilidad RF↔journey al 100%; cada RF tiene criterio de aceptación |
| **3** | 12–22: arquitectura completa + ADRs formales | Las 3 decisiones irreversibles (tenancy, sync, datos) aprobadas; sin PD abiertas en fundaciones |
| **4** | 23–26, 55: seguridad, IAM, privacidad, legal, auditoría | Modelo de amenazas completo; biblioteca unificada de controles definida |
| **5** | 27–30: marca, design system, biblia UX, accesibilidad WCAG 2.2 AA | Tokens y componentes base definidos; estándar de accesibilidad normativo |
| **6** | 31–55: 25 documentos de módulo | Cada módulo con RF/RNF propios, pruebas definidas, DoD y referencias cruzadas |
| **7** | 56–63: plataforma de ingeniería | Pipelines, IaC, SLOs, DR y FinOps especificados |
| **8** | 64–68: migración, onboarding, soporte, store readiness, handbook | Plan de migración desde competidores (Fiix/MaintainX/UpKeep/Excel) definido |
| **9** | 69–70: roadmap final y Production Readiness Review | Checklist PRR 100% verde → **autorización formal para programar** |

---

## E. Criterios que deben cumplirse antes de comenzar a programar (Definition of Ready del proyecto)

1. **G1 — Gobernanza:** documentos 00–04 en estado Aprobado; regla de evidencia (DC/SU/PD) aplicada sin excepciones.
2. **G2 — Requisitos:** 05–11 aprobados; todo RF tiene ID, criterio de aceptación, prioridad (MoSCoW) y trazabilidad a un journey; los RNF globales tienen valores numéricos (latencias, disponibilidad, RPO/RTO, WCAG).
3. **G3 — Fundaciones arquitectónicas:** 17, 18, 19 aprobados sin PD abiertas; ADRs 001–010 formalizados en el documento 13; diagrama de capas (12) validado contra módulos.
4. **G4 — Confianza:** modelo de amenazas (23) y programa de privacidad (24) aprobados; decisión de ruta SOC 2/ISO con fechas (25).
5. **G5 — Dominio congelado v1:** entidades canónicas, máquina de estados de OT, glosario ES/EN y convención `tenant_id`/`version`/tombstones aprobadas; cambios posteriores solo vía ADR nuevo.
6. **G6 — Entorno:** IaC del entorno de desarrollo especificada (57) y pipeline CI/CD diseñado (56), aunque aún no implementados.
7. **G7 — DoD global aprobada:** incluye pruebas de sync/offline obligatorias para todo módulo de campo, revisión de seguridad, accesibilidad y actualización documental.
8. **G8 — Autorización:** el documento 70 (PRR) lo firma el Fundador, Pascasio Emmanuel Reynoso Reyes. Sin esa firma, no se escribe código de producción.

---

## F. Riesgos que podrían hacer fracasar el proyecto

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | **Subestimar el motor de sync offline** (la pieza más difícil del sistema; Realm/Device Sync fue deprecado en 2024 — DC) | Alta | Crítico | Prototipo de sync en Fase 0 con simulador de chaos offline en CI (doc 19 y 60) antes que cualquier módulo |
| R2 | **Documentar en vez de validar:** 70 documentos sin un piloto real | Media | Crítico | Ola 9 exige 3–5 pilotos comprometidos (heredado del roadmap previo — DC); los journeys (10) se validan con técnicos reales |
| R3 | **Sobre-alcance:** construir EAM/FM antes de dominar CMMS | Alta | Alto | Disciplina de fases del roadmap (heredada — DC); la PRR (70) bloquea módulos fuera de fase |
| R4 | **Guerra de precios / planes gratuitos de competidores** (MaintainX y Limble tienen plan gratis — DC) | Media | Alto | Diferenciación en offline, IA agentiva y LatAm (español, WhatsApp) — DC de investigación, no competir en precio |
| R5 | **IA commoditizada por los líderes** antes del lanzamiento | Media | Medio | Apostar a agentes gobernados con auditoría (diferenciador confirmado por la investigación de Facilio — DC) |
| R6 | **Fundador único como cuello de botella** (autoría y ejecución concentradas) | Alta | Alto | Esta suite existe precisamente para hacer el conocimiento transferible; documento 68 (handbook) y ADRs reducen el bus-factor |
| R7 | **Deuda de cumplimiento:** posponer SOC 2 y perder ventas enterprise (restricción de adopción confirmada — DC) | Media | Alto | Biblioteca unificada de controles desde el día uno (doc 25/55); evidencia automatizada |
| R8 | **Costos de IA destruyendo el margen** | Media | Medio | Gateway multi-modelo con routing por costo (ADR-007 — DC); FinOps (62) con costo por tenant como métrica |
| R9 | **Cambios de regulación de datos en LatAm** | Media | Medio | Programa de privacidad (24) con residencia de datos opcional y tier híbrido de tenancy (ADR-001 — DC) |
| R10 | **Fatiga de perfeccionismo:** nunca declarar "listo para programar" | Media | Crítico | Criterios E1–E8 objetivos y binarios; PRR con checklist cerrado, no abierto |

---

## G. Elementos faltantes detectados en la investigación anterior

La investigación previa es sólida en mercado, arquitectura y dominio, pero tenía **vacíos que esta suite corrige**. Ninguno invalida decisiones confirmadas; todos se asignan a documentos:

| # | Vacío / inconsistencia | Severidad | Documento que lo resuelve |
|---|---|---|---|
| G-01 | **Discrepancia de nombre:** la investigación decía "DONEFIXER"; el nombre oficial es **DONEFIXER** | Alta (marca/legal) | 00 (este), 29 (marca). Se adopta DONEFIXER en toda la suite |
| G-02 | **Accesibilidad ausente:** ningún estándar WCAG, pese a ser requisito enterprise/legal en muchos mercados | Alta | 30 (Accessibility Standard — WCAG 2.2 AA como SU, pendiente confirmar nivel) |
| G-03 | **UX/UI y Design System no investigados:** solo principios ("≤3 toques"), sin sistema de diseño, tokens ni guía de marca | Alta | 27, 28, 29 |
| G-04 | **Estrategia de migración de datos inexistente:** cómo importar desde Excel, Fiix, MaintainX, UpKeep (clave de adopción: Limble gana migrando desde hojas de cálculo — DC de mercado) | Alta | 64 |
| G-05 | **Onboarding/implementación sin detalle:** la meta "<7 días" (SU de mercado) no tenía proceso | Media | 65 |
| G-06 | **Soporte y gestión de incidentes al cliente no definidos** | Media | 66 |
| G-07 | **Billing/entitlements no diseñados:** el modelo de precios era direccional (SU); faltan planes, límites por plan, feature flags comerciales | Alta | 54, 03 |
| G-08 | **Módulos funcionales sin especificación individual:** el modelo de dominio define entidades pero no requisitos por módulo | Alta | 31–55 |
| G-09 | **Chat/colaboración mencionado como lección de mercado (MaintainX) pero sin módulo propio** | Media | 43 |
| G-10 | **Traducción automática:** i18n decidida (ADR-010 — DC) pero sin estrategia de traducción en tiempo real para equipos multilingües | Media | 44 |
| G-11 | **Voz/OCR/visión por computadora:** citada como capacidad IA sin módulo ni requisitos | Media | 45 |
| G-12 | **Firmas digitales y valor legal de la evidencia:** la evidencia fotográfica estaba definida; su validez legal (incl. 21 CFR Part 11) no | Media | 47, 25 |
| G-13 | **Release readiness de stores** (revisión Apple/Google, privacidad de apps, etiquetas de datos) | Media | 67 |
| G-14 | **Testing de sync como disciplina:** citado en ADRs pero sin programa de ingeniería de calidad | Alta | 60 |
| G-15 | **FinOps:** principio de costo por tenant sin programa | Baja | 62 |
| G-16 | **Performance engineering:** SLOs definidos pero sin metodología de pruebas de carga/capacidad | Media | 61 |
| G-17 | **Production Readiness Review:** no existía gate formal previo a código | Alta | 70 |
| G-18 | **Handbook de desarrollador y documentación viva** | Baja | 68 |
| G-19 | **Supuestos no marcados como tales en la investigación previa** (p. ej., "TCO 18% menor con Flutter", benchmarks de burbuja en el mapa competitivo, estimaciones de precios regionales): son **SU**, no DC | Media | Cada documento los re-etiqueta al migrarlos |
| G-20 | **Business Model sin estructura formal** (LTV, CAC, canales, márgenes) | Alta | 03 |

---

## Registro de aprobaciones oficiales del Fundador

| Elemento | Estado | Fecha |
|---|---|---|
| **Ola 1** (docs 01–04 v1.2) | ✅ APROBADA (definitiva, 2026-07-29) | Base estratégica oficial |
| **ADR-011 v1.1** (multicanal, autoridad backend) | ✅ APROBADO con modificaciones | 2026-07-29 |
| **ADR-012 v1.1** (Platform Administration Console) | ✅ APROBADO con ajustes | 2026-07-29 |
| **DC-00** (nombre oficial DONEFIXER) | ✅ APROBADO | 2026-07-29 |
| Sistema DC/SU/PD · Trazabilidad · Gobierno por ADR · Proceso FEP | ✅ APROBADOS | 2026-07-29 |
| **Ola 2** (11 documentos: 15, 16, 17, 13, 14, 19, 09, 11, 12, 10, 18) | ✅ APROBADA (oficial, 2026-07-29) | Contrato funcional oficial |
| **Ola 3** (14 documentos: 25, 26, 27, 24, 30, 29, 28, 31, 20, 21, 22, 23, 32, 33) | ✅ APROBADA (oficial, 2026-07-29) | Arquitectura oficial del proyecto |
| **Auditoría Integral de Arquitectura** (AUDITORIA_INTEGRAL_ARQUITECTURA_2026-07) | ✅ APROBADA (2026-07-29) | AO-1…AO-4 ejecutadas; AO-5/AO-6 aprobadas como planificación Ola 4 |
| **ADI** (Architecture Decision Index) · **Canonical Identifier Registry** · **Verificación de Integridad Documental** | ✅ CREADOS (2026-07-29) | Instrucciones adicionales 1–3 del Fundador |
| **Ola 4** (docs 40, 43, 47, 51, 54, 60, 62, 70) | ✅ APROBADA (oficial, 2026-07-29) | Incorporada a la documentación oficial; reglas permanentes 1–4 registradas |
| **MASTER_PROMPT_Implementacion_Enterprise_v1.0** | ✅ ADOPTADO como estándar normativo de implementación (2026-07-29) | Condicionado a PD bloqueantes y al Gate del Doc 70 |
| **MASTER_PROMPT_Architecture_Spike_v1.0 + EXENCIÓN-SPIKE-01** | ✅ APROBADA (DC, 2026-07-29) con 8 condiciones del Fundador | Autoriza código de **investigación técnica** solo para J-2; no es producción ni MVP; Doc 70 intacto |

## Condiciones permanentes del proyecto (impuestas por el Fundador, 2026-07-29)

1. Toda decisión futura deberá mantener trazabilidad.
2. Ningún supuesto podrá convertirse en decisión confirmada sin aprobación expresa del Fundador.
3. Toda afirmación técnica o de mercado deberá indicar su nivel de evidencia.
4. Los ADR podrán reabrirse únicamente mediante nueva evidencia verificable.
5. La arquitectura deberá evolucionar por etapas, evitando sobrearquitectura prematura.
6. **La documentación será la fuente de verdad del proyecto; el código deberá implementarla, no redefinirla.**

## Control de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0 | 2026-07-29 | Pascasio Emmanuel Reynoso Reyes (Fundador) — elaborado con asistencia de IA | Creación del índice maestro, olas, dependencias, criterios E, riesgos F y vacíos G. Absorbe la investigación previa sin eliminar decisiones válidas; adopción oficial del nombre DONEFIXER |
| 1.1 | 2026-07-29 | Ídem | DC-00 de corrección nominal aplicada globalmente (DONEFIXER como única grafía) |
| 1.2 | 2026-07-29 | Ídem | **Registro de aprobaciones oficiales** (Ola 1 definitiva, ADR-011 v1.1, ADR-012) e incorporación de las **6 condiciones permanentes** del proyecto |
| 1.3 | 2026-07-29 | Ídem | Aprobación oficial y definitiva reconfirmada con 5 reglas permanentes (documentación como fuente de verdad; DC solo por ADR/decisión formal; evidencia DC/SU/PD; irreversibles solo con evidencia; código implementa, no sustituye). Ola 2 construida en el orden aprobado con instrucciones 7–10 incorporadas (docs 15/16 v1.1) |

---

*Documento normativo de la suite DONEFIXER. Siguiente paso autorizado: Ola 1 (documentos 04, 01, 02, 03). No se escribirá código de producción hasta la aprobación del documento 70.*

| 1.4 | 2026-07-29 | Ídem | **APROBACIÓN OFICIAL OLA 2** (11 documentos). Registro de condiciones permanentes de la Ola 2 y autorización de la Ola 3 (14 documentos arquitectónicos) con reglas: trazabilidad a RF/RNF, prohibición de tecnología por tendencia, PD abiertas (N-1/N-2), separación dominio/aplicación/infraestructura |
| 1.5 | 2026-07-29 | Ídem | **OLA 3 ENTREGADA** (14 documentos arquitectónicos completos, en el orden autorizado). Nueva PD registrada: PD-IA-1 (proveedor/modelo LLM, Doc 32 §9). Pendiente de aprobación expresa del Fundador |
| 1.6 | 2026-07-29 | Ídem | **APROBACIÓN OFICIAL OLA 3** (14 documentos). Registro de las 5 condiciones permanentes de la Ola 3 (trazabilidad; justificación de tecnología en 5 elementos; PD abiertas incl. PD-IA-1; cambios con ADR; evolución sin complejidad prematura). Condición previa a Ola 4: **Auditoría Integral de Arquitectura** con entrega A–E, sujeta a aprobación expresa |
| 1.7 | 2026-07-29 | Ídem | **APROBACIÓN DE LA AUDITORÍA INTEGRAL + EJECUCIÓN AO-1…AO-4**: corrección de 25 identificadores rotos en Docs 21/22/23 (v1.1); lista de prohibiciones IA unificada con identificadores P-33-1…7 (Docs 19 v1.3 / 33 v1.1); aclaración de métrica FTS local (Doc 23); creado `ADR-001-010_Registro.md`. **Creados por instrucción del Fundador:** ADI, Canonical Identifier Registry y proceso obligatorio de Verificación de Integridad Documental. Autorizada la planificación formal de la Ola 4 |
| 1.8 | 2026-07-29 | Ídem | **MASTER_PROMPT_Implementacion_Enterprise_v1.0 adoptado** como estándar normativo de implementación (condicionado a PD bloqueantes y al Gate del Doc 70). **OLA 4 ENTREGADA** (docs 40, 43, 47, 51, 54, 60, 62, 70) con todas las ampliaciones obligatorias; AO-5 integrada (Doc 47/54); AO-6 atendida sin resolver PD (PD-2 propuesta en Doc 51; PD-RETENCIÓN y SU-FLAGS con análisis en Doc 62). Verificación de Integridad Documental ejecutada: **0 errores bloqueantes** |
| 1.9 | 2026-07-29 | Ídem | **APROBACIÓN OFICIAL OLA 4** (8 documentos). Reglas permanentes refrendadas: gate del Doc 70 + PD bloqueantes como doble condición de código; respeto a contratos documentales; tecnología solo con trazabilidad; desviaciones vía ADR. Autorizada la planificación de la siguiente fase documental |
| 1.10 | 2026-07-29 | Ídem | **EXENCIÓN-SPIKE-01 aprobada (DC)**: autoriza Architecture Spike N-1/N-2 (solo flujo J-2) como código de investigación técnica, con 8 reglas permanentes (no modificar docs/ADRs aprobados, no ampliar alcance, código experimental separado, métricas y resultados reproducibles). Entregables S-1…S-6 autorizados. Cierre de N-1/N-2 sujeto a revisión y aprobación del Fundador tras la Spike |
| 1.11 | 2026-07-30 | Ídem | **SPIKE EJECUTADA Y ENTREGADA** (S-1…S-6): backend mínimo .NET 8 + PostgreSQL 16 real (RLS con FORCE + rol de aplicación); suite J-2 E2E **15/15 métricas PASS, 0 FAIL** (veredictos correctos ante conflicto servidor, idempotencia, tombstones, recovery, aislamiento cross-tenant, 2.366 ops/s, outbox 1:1); 15/15 unit tests .NET; apps Flutter y RN/Expo del flujo J-2 con adaptador MA-1 + guía de medición en dispositivo. **Resultado: N-1 permanece PD (faltan métricas de dispositivo); N-2 dividido: ADR-014 fase 1 propuesta (write-path propio confirmado como definitivo), fase 2 (Cloud vs. self-hosted) permanece PD.** Pendiente revisión y aprobación del Fundador |

## Condiciones permanentes de la Ola 3 (impuestas por el Fundador, 2026-07-29)

1. Toda decisión arquitectónica permanecerá trazada a PRD, RF, RNF, SRS, Domain Model o ADR aprobados.
2. Ninguna tecnología se incorporará sin justificar: problema que resuelve, alternativas evaluadas, trade-offs, costo operativo, criterio de evolución o reemplazo.
3. Las decisiones PD (incluyendo N-1, N-2, PD-IA-1 y las restantes) permanecerán abiertas hasta resolución formal.
4. Toda modificación futura de la arquitectura requerirá trazabilidad completa y, cuando corresponda, un ADR.
5. La arquitectura permanecerá evolutiva, evitando complejidad prematura.

## Reglas de gobierno documental (impuestas por el Fundador, 2026-07-29, con la aprobación de la Auditoría)

1. **Canonical Identifier Registry** (`REGISTRY_Canonical_Identifiers.md`) es la única fuente oficial de identificadores; citar un ID inexistente es error de integridad.
2. **ADI** (`ADI_Architecture_Decision_Index.md`) consolida toda decisión arquitectónica con estado, dependencias, reversibilidad e impacto.
3. **Verificación de Integridad Documental** (`VERIFICACION_INTEGRIDAD_DOCUMENTAL.md`) es obligatoria antes de aprobar cualquier ola futura: referencias cruzadas, IDs inexistentes, duplicados, enlaces rotos, inconsistencias DC/SU/PD, documentos huérfanos, trazabilidad incompleta. **Ninguna ola podrá aprobarse con errores de integridad.**
4. Erratas editoriales tipo AO-1…AO-4 (sin cambio de decisiones, ADRs, tecnologías, RF/RNF ni Domain Model) se registran en el changelog del documento afectado.

## Reglas permanentes de la Ola 4 (impuestas por el Fundador, 2026-07-29)

1. Mantener trazabilidad completa.
2. No resolver decisiones PD mediante implementación (las PD bloquean el componente afectado).
3. No introducir tecnologías sin justificación documentada.
4. No degradar la arquitectura aprobada.
5. Toda desviación se registra mediante ADR.
6. **Solo el Documento 70 emite el veredicto GO / GO WITH CONDITIONS / NO GO**; ningún código de producción comienza sin GO o GO WITH CONDITIONS aprobado por el Fundador **y sin resolver las PD bloqueantes del componente correspondiente** (refrendado en la aprobación de la Ola 4).
7. Toda implementación respeta arquitectura, dominio y contratos documentales aprobados; ninguna tecnología se añade sin trazabilidad documental; toda desviación se registra mediante ADR (refrendado en la aprobación de la Ola 4).

---

## Registro de cambios (continuación)

**v1.12 (2026-07-30)** — DECISIÓN DEL FUNDADOR sobre Spike Fase 2 (N-2):
- **DC-01:** Master Prompt — Architecture Spike Enterprise v1.1 adoptado como estándar normativo de la Fase 2; ámbito exclusivo N-2; no modifica Constitución, EXENCIÓN-SPIKE-01 ni Doc 70.
- **DC-02:** matriz de decisión independiente para N-2 (Confiabilidad 30 / Operación 20 / Rendimiento 15 / Seguridad 15 / TCO 10 / Escalabilidad 5 / Riesgo 5); la matriz de Doc 23 §4 queda exclusiva de N-1.
- **DC-03:** Carril A autorizado y ejecutado — paquete `spike_fase2/` (especificación, harness parametrizable, scripts de medición, plantillas benchmark/TCO/matriz/anexo, guías y configuración reproducible). Documentación e infraestructura de evaluación; **no código de producción**. Batería verificada en modo CONTROL: 6/6 casos PASS, 0 FAIL, 15 métricas.
- **DC-04:** Carril B condicionado a cuenta PowerSync Cloud + entorno Docker self-hosted + credenciales; N-2 permanece **PD**.
- **DC-05:** ADR-014 fase 1 reclasificada como **DC-C** (validación técnica preliminar del write-path), pendiente de la Fase 2 completa y del cierre formal de N-2.
- **REGLA ADICIONAL (permanente):** Anexo de Reproducibilidad obligatorio; sin él, ninguna métrica fundamenta el cierre de N-2.
- Verificación de integridad documental ejecutada sobre los nuevos artefactos: sin IDs rotos ni referencias inexistentes.

**v1.13 (2026-07-30)** — DECISIÓN DEL FUNDADOR sobre Fase 2B:
- **DC-06:** Master Prompt Spike v1.2 adoptado como norma de ejecución del Carril B, condicionado al cumplimiento íntegro de precondiciones; no modifica Constitución, EXENCIÓN-SPIKE-01, Doc 70 ni DC-01…DC-05.
- **DC-07:** detención por precondiciones no cumplidas = mecanismo de gobernanza, no retraso; prohibida cualquier comparación mientras no estén completas.
- **DC-08:** `spike_fase2/SPIKE_F2B_Precondiciones.md` registrado como documento de control operativo de la Fase 2B.
- **DC-09:** habilitación de entornos = actividad externa al sandbox; Carril B inicia solo con ambos validados.
- **DC-10:** mientras Carril B pendiente, solo actividades sin cambios de arquitectura, sin código de producción, sin alterar la comparativa N-2; prioridad: instrumentación de medición N-1 en dispositivos reales.
- Estado oficial: EXENCIÓN-SPIKE-01 activa · Fase 1 completada · Carril A completado · Carril B pendiente de precondiciones · N-1 PD · N-2 PD · ADR-014 DC-C · Doc 70 único gate de producción.

**v1.14 (2026-07-30)** — DECISIÓN DEL FUNDADOR sobre el Gate de producción:
- **DC-11:** Master Prompt — Production Readiness Gate Enterprise v1.0 = estándar normativo oficial del Documento 70 (especificación de la auditoría de Production Readiness; no modifica Constitución, Doc 70, ADRs ni DC-01…DC-10).
- **DC-12:** Carril Gate ejecutado — expediente operativo en `gate_doc70/`: Protocolo, Checklist (42 criterios trazados), Matriz de Cumplimiento (12 áreas, estado real), Registro de Riesgos (RR-01…10), plantilla de Veredicto y `verificacion_gate70.py` (8/8 comprobaciones, 0 FAIL). Estado del expediente: **"Preparado para ejecución"** — no es veredicto.
- Regla de ejecución: la auditoría del Doc 70 solo inicia con N-1, N-2, PD-CLOUD, PD-IA-1 y PD-4 cerradas y evidencia reproducible en toda decisión bloqueante.

**v1.15 (2026-07-30)** — DC-13 — FASE 1 IMPLEMENTACIÓN ENTERPRISE (PRE-GO): Master Prompt Fase 1 v1.0 adoptado como estándar oficial de preparación de la implementación; autorizado el paquete `fase1_plan/` (12 entregables). WP-00 = GO del Doc 70 (sin rutas que lo eviten); WPs de móvil y sync parametrizados por ADR-013/ADR-014, no instanciables antes de su aprobación. **Jerarquía: DC-13 subordinada a Constitución → Documento 70 → ADRs aprobados → DC-01…DC-12.** No autoriza código de producción, implementaciones parciales, cambios arquitectónicos, nuevos ADR ni cierre de PDs.

**v1.16 (2026-07-30)** — DC-14 — EXECUTION GOVERNANCE MANUAL (EGM): adoptado como manual operativo oficial de la ejecución diaria del desarrollo. **Es manual de ejecución, no fuente de requisitos ni de arquitectura; operacionaliza el corpus existente con regla de no duplicación (referencia fuente + sección + solo procedimiento).** Autorizado el paquete `gobernanza_ejecucion/` (12 entregables) con verificación automática de integridad obligatoria. Jerarquía: subordinado a Constitución → Doc 70 → ADRs → DC-01…DC-13. Estructura de gobernanza de alto nivel: **completa**. El trabajo principal pasa a ser ejecutar el plan conforme a ella.

**v1.17 (2026-07-30)** — SPRINT 0 ENTERPRISE EXECUTION (materialización ejecutable del Sprint 0 aprobado en DC-13; no es norma nueva): paquete `sprint0_repo/` creado — estructura definitiva de monorepo (backend .NET 8 por capas, web, mobile `{{ADR-013}}` parametrizado, infra `{{PD-CLOUD}}`), pipeline CI definitivo de 11 etapas con gates indesactivables (suite J-2, test ataque RLS, linter migraciones RLS/FORCE, escaneo de secretos, integridad documental), plantillas de entorno y secretos (rol de app no privilegiado), 6 plantillas oficiales (PR, Work Package, Bug, Hotfix, ADR, RFC), herramientas de calidad por stack, tableros, protección de ramas y onboarding técnico. Sin lógica de negocio; parametrización ADR-013/ADR-014/PD-CLOUD intacta. Verificación de integridad del paquete: PASS (citas resueltas, 0 familias prohibidas). **Declarado por el Fundador: no crear más documentos de gobernanza salvo necesidad real durante la ejecución; el foco pasa a cerrar N-1, N-2, PD-CLOUD, PD-IA-1 y PD-4, ejecutar el Doc 70 y comenzar la implementación.**

**v1.18 (2026-07-30)** — WP-UX-ART autorizado como **entregable PRE-GO vinculado a DC-13/DC-14** (no como DC-15: distinción aprobada por el Fundador — DC = cambia la gobernanza; WP/entregable = ejecuta una decisión ya aprobada; DC-15 reservado para decisión que cambie el corpus). Paquete `ux_artifact/`: mapa de navegación, user flows, inventario de pantallas, biblioteca de componentes (derivada del DS aprobado), especificaciones visuales, catálogo de estados, **prototipo HTML estático navegable** ("Design Artifact PRE-GO — no reutilizable como código de producción sin autorización posterior"), manual UX/UI, fichas de validación por pantalla y checklists (consistencia, accesibilidad, handoff). Verificación automática de integridad obligatoria.

**v1.19 (2026-07-30)** — DC-15 — ADOPCIÓN DEL MASTER PROMPT ENTERPRISE PRODUCTION IMPLEMENTATION v1.0 (POST-GO): adoptado como especificación operativa oficial de la ejecución de todos los Work Packages posteriores al Production Readiness Gate. **No crea una nueva capa jerárquica: la jerarquía del corpus permanece igual; DC-15 únicamente incorpora la especificación.** No modifica arquitectura, Constitución, ADRs ni Documento 70; no autoriza desarrollo antes del GO. DC-15a adopción; DC-15b **estado inerte** hasta veredicto compatible del Doc 70 (antes: sin código de producción, sin WPs de implementación, sin uso como autorización); DC-15c precedencia de interpretación: Constitución → Documento 70 → ADRs → DCs → Master Prompt POST-GO; DC-15d parametrización {{ADR-013}}/{{ADR-014}} obligatoria mientras N-1/N-2 estén abiertos; DC-15e patrones (CQRS, Repository…) solo donde el corpus los apruebe — sin aprobación universal; DC-15f registro en ADI + Índice Maestro con verificación de integridad. Resultado: separación completa planificación PRE-GO (DC-13) / autorización (Doc 70) / ejecución POST-GO (DC-15).
