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
*Razón:* el design system requiere tokens de marca; la biblia UX los aplica; la accesibili