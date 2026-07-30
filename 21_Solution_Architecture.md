# 21 — Solution Architecture

| Campo | Valor |
|---|---|
| Documento | 21_Solution_Architecture |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Autoría | Equipo de documentación DONEFIXER bajo dirección del Fundador (Pascasio Emmanuel Reynoso Reyes) |
| Precedencia | Documento 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 14 (Dominio), 11 (RF), 12 (RNF), 20 (EA), 24 (Backend), 25 (Datos), 26 (Multi-Tenant), 27 (Offline/Sync), 30 (Eventos) |

> **Convención de evidencia:** DC = Decisión Confirmada · SU = Supuesto · PD = Pendiente de Decisión. Toda afirmación relevante lleva su clasificación.

---

## 1. Propósito y alcance

Este documento integra las arquitecturas parciales ya aprobadas en borrador (datos, multi-tenant, sincronización, backend, eventos) en una **vista de solución única y coherente**: cómo los componentes de DONEFIXER se ensamblan en un sistema desplegable, observable y operable por un equipo inicial de una persona (N-10, PD). Donde un documento de capa define el *cómo interno* de su capa, este documento define el *cómo conjunto*: topología de despliegue, flujos de extremo a extremo, límites de responsabilidad entre componentes, observabilidad, ambientes y estrategia de evolución. (DC)

**Fuera de alcance:** código, DDL, manifiestos de infraestructura definitivos, endpoints finales (regla permanente del Fundador), y las decisiones N-1 (framework móvil) y N-2 (PowerSync Cloud vs. self-hosted), que permanecen abiertas. (DC)

---

## 2. Vista de solución — Etapa A (Fases 0–2)

La Etapa A es la arquitectura de lanzamiento y de los primeros pilotos. Su principio rector es **simplicidad operativa deliberada**: cada componente presente está justificado por uno o más RF/RNF; cada componente ausente tiene un criterio medible de activación registrado en su documento de capa. (DC)

### 2.1 Topología lógica

```
┌────────────────────────────────────────────────────────────────────┐
│                          CLIENTES                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Web App      │  │ PWA          │  │ App móvil nativa         │  │
│  │ (React, SPA) │  │ (mismo code- │  │ (framework PD N-1;       │  │
│  │              │  │  base React) │  │  SQLite local + SQLCipher│  │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬──────────────┘  │
│         └─────────────────┴──────────────────────┘                 │
└────────────────────────────┬───────────────────────────────────────┘
                             │ HTTPS (OIDC/OAuth 2.1, JWT con tenant claim)
┌────────────────────────────▼───────────────────────────────────────┐
│                       PLANO DE TENANT                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  API REST versionada (.NET 8, monolito modular)             │   │
│  │  Interfaces → Aplicación → Dominio puro → Infraestructura   │   │
│  │  + Módulo de sincronización (write-path con re-validación)  │   │
│  │  + Workers (outbox publisher, notificaciones, PM, reportes) │   │
│  └──────┬──────────────────┬──────────────────┬────────────────┘   │
│         │                  │                  │                    │
│  ┌──────▼───────┐   ┌──────▼───────┐   ┌──────▼───────┐            │
│  │ PostgreSQL   │   │ Redis        │   │ Almacenamiento│           │
│  │ 16+ (RLS,    │   │ (caché,      │   │ de objetos S3 │           │
│  │ pgvector,    │   │ colas, rate  │   │ (URLs firmadas│           │
│  │ ltree)       │   │ limiting)    │   │ + SHA-256)    │           │
│  └──────────────┘   └──────────────┘   └───────────────┘           │
│                                                                    │
│  PowerSync (N-2 PD: Cloud o self-hosted) — capa de replicación     │
│  PostgreSQL → SQLite de clientes móviles/PWA                       │
└────────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────────┐
│                    PLANO DE PLATAFORMA (separación permanente,     │
│                    ADR-012 v1.1)                                   │
│  Consola de Administración → Admin API independiente (auth,        │
│  authz, auditoría, versionado y límites propios) → esquema         │
│  `platform` en PostgreSQL                                          │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 Justificación componente por componente (trazabilidad obligatoria)

| Componente | Presente porque… | Trazabilidad | Evidencia |
|---|---|---|---|
| React Web App / PWA (un solo codebase) | Canal de administración, planificación, reportes; continuidad ligera sin reemplazar nativo | ADR-011 v1.1; RF-REQ-001 (PWA); RF-RPT / RF-PLT (capacidades web); RNF-USE / RNF-ACC | DC |
| App móvil nativa | Técnico de campo es usuario primario; Offline-First nativo | ADR-011; Doc 16 J-2; RNF-SYNC-003 (≥7 días offline / 200 operaciones) | DC (framework PD N-1) |
| .NET 8 monolito modular | Velocidad de desarrollo, testabilidad, extracción por métricas | Doc 24 (ADR-004/005); RNF-MNT | DC |
| PostgreSQL 16+ único sistema de registro | Integridad transaccional, RLS nativo, ltree, pgvector | Doc 25; C-3 (SRS); RNF-SEC | DC |
| Redis | Caché, colas ligeras, rate limiting sin estado en la app | Doc 24 §Workers; RNF-SCL-003 (rate limit por tenant); RNF-PERF-001 (presupuesto de latencia API) | DC |
| S3-compatible | Evidencias fotográficas, adjuntos, exportaciones | Doc 25 §Objetos; RF-WO-003 (evidencias) | DC |
| PowerSync | Replicación PostgreSQL→SQLite probada, SDKs Apache 2.0 | Doc 27 (ADR-002 revertido); RF-SYNC-001…010 | DC (modalidad PD N-2) |
| Consola + Admin API separadas | Separación de planos como principio arquitectónico permanente | ADR-012 v1.1 | DC |
| OIDC (proveedor de identidad) | Autenticación centralizada, MFA, claims de tenant | Doc 26 §Pipeline; RNF-SEC-005 (sesiones) | DC (proveedor: SU) |

### 2.3 Componentes diferidos a Etapa B (con criterio de activación)

| Componente | Criterio medible de activación | Documento fuente | Evidencia |
|---|---|---|---|
| ClickHouse (analítica) | >50M filas en tablas de hechos o p95 de dashboards >2 s | Doc 25 | DC |
| Kafka | >5 consumidores por evento o necesidad de replay histórico | Doc 30 (criterio E-2) | DC |
| Kubernetes | Falla del despliegue simple (p95, despliegues, recuperación) sostenido 2 trimestres | Doc 24 | DC |
| Servicio Python de ML | Casos de uso IA que excedan capacidad de APIs gestionadas + volumen que justifique costo | Doc 32 | DC |
| BD dedicada por tenant enterprise | Requisito contractual o regulatorio de cliente Enterprise | Doc 26 | DC |

---

## 3. Flujos de extremo a extremo

### 3.1 Flujo síncrono estándar (ej.: aprobar una solicitud)

1. Cliente envía `POST /v1/service-requests/{id}:approve` con JWT, `Idempotency-Key` y `If-Match: <version>`. (DC — Doc 29, AP-8)
2. Pipeline multi-tenant: validación JWT → membresía → `set_config('app.current_tenant', …, true)` en transacción → filtro de aplicación + política RLS. (DC — Doc 26, MT-4)
3. Capa de aplicación carga agregado, verifica permisos (RBAC+ABAC, Doc 19), invoca dominio puro.
4. Dominio aplica máquina de estados e invariantes (Doc 14); rechaza transiciones inválidas.
5. Infraestructura persiste con `version` incrementada; **evento de dominio se escribe en outbox dentro de la misma transacción**. (DC — Doc 30, EV-1)
6. Respuesta con nuevo `ETag`; worker publica el evento y despacha notificaciones. (DC)

**Criterio de aceptación del flujo:** ninguna mutación deja estado persistido sin su evento en outbox; prueba de fallo a mitad de transacción demuestra atomicidad. (DC)

### 3.2 Flujo offline → sincronización (el flujo definitorio del producto)

1. Técnico sin conectividad ejecuta operaciones sobre SQLite local; cada operación se registra con `operation_id` único, HLC y payload, en outbox local **dentro de la misma transacción local** que el cambio. (DC — Doc 27, SY-4)
2. La UI muestra el estado como **provisional** (regla de autoridad del backend, ADR-011 v1.1 texto literal del Fundador).
3. Al recuperar conectividad, el cliente transmite operaciones en orden; el servidor las procesa por write-path de sincronización: idempotencia por `operation_id` → re-validación de reglas críticas en servidor → veredicto **ACCEPT / ADJUST / REJECT** por operación. (DC — Doc 27, SY-8/SY-9)
4. Las réplicas confirmadas regresan al cliente vía replicación PowerSync; los veredictos ADJUST/REJECT son visibles y explicables al usuario (Doc 16 J-2, flujos OFF). (DC)
5. Conflictos se resuelven según la matriz normativa: deltas para stock, aditivo para evidencias, servidor autoritativo para estado de OT, cola humana para críticos; **jamás LWW silencioso en campos críticos**. (DC — Doc 14 §Matriz de conflictos)

**Criterio de aceptación:** la prueba normativa "modo avión" del Journey J-2 pasa de punta a punta, incluyendo convergencia tras 7 días offline con 200 operaciones acumuladas (RNF-SYNC-003). (DC)

### 3.3 Flujo de eventos hacia integraciones externas

Outbox → worker publisher → entrega de webhooks firmados (HMAC-SHA256, secreto rotativo, reintentos con backoff, consola de entregas visible para el tenant). (DC — Doc 28, IN-4)

### 3.4 Flujo de administración de plataforma

Acción en Consola → Admin API (autenticación y autorización independientes) → régimen de acciones críticas Fase 0-1 si aplica (MFA + reautenticación + motivo + log inmutable + confirmación explícita + rollback cuando sea posible) → ejecución sobre esquema `platform` → registro de auditoría con los 10 campos obligatorios. (DC — ADR-012 v1.1 §3.9)

---

## 4. Límites de responsabilidad entre componentes

| Responsabilidad | Dueño exclusivo | Prohibido a |
|---|---|---|
| Reglas de negocio críticas (autoridad final) | Dominio en backend (Doc 24) | Clientes (solo lógica provisional), integraciones, workers |
| Resolución de conflictos de sincronización | Módulo de sync del servidor (Doc 27) | Réplicas locales, PowerSync (transporta, no decide) |
| Aislamiento de tenant | Base de datos (RLS) + pipeline de aplicación, ambos (defensa en profundidad, Doc 26 MT-3) | La sola capa de aplicación nunca es suficiente |
| Emisión de eventos de dominio | Outbox transaccional (Doc 30 EV-1) | Publicación directa desde handlers |
| Autorización de acciones de plataforma | Admin API (ADR-012) | API de tenant |
| Decisión de IA en riesgo medio/alto | Humano, siempre (Doc 33) | Agentes IA (prohibición como ausencia de permisos) |

---

## 5. Observabilidad y operación (Etapa A)

**Principio:** un equipo de una persona solo puede operar lo que puede ver. La observabilidad no es Etapa B. (DC)

| Capacidad | Decisión | Trazabilidad | Evidencia |
|---|---|---|---|
| Logs estructurados | JSON con `trace_id`, `tenant_id`, `actor_id`, `operation_id` (cuando aplique) | RNF-OBS; Doc 24 | DC |
| Trazas distribuidas | OpenTelemetry desde Etapa A; backends intercambiables | RNF-OBS-002 | DC |
| Métricas de negocio | Además de métricas técnicas: tasa de éxito de sync (>99.9%/día, RNF-SYNC-001), tiempo de convergencia, cuota IA por tenant | Docs 27, 32 | DC |
| Alertas | Umbral + ausencia de señal (sync detenida, outbox creciente, error rate) | RNF-OBS-004 | DC |
| Salud del sistema | Endpoints de health/readiness; estado visible en Consola de Plataforma | ADR-012 §observabilidad | DC |
| Dashboard FinOps | Costo de IA por tenant contra línea roja (>30% del ingreso del tenant) | Doc 03 §11 bis; Doc 33 | DC |

---

## 6. Ambientes y estrategia de despliegue

| Ambiente | Propósito | Datos | Evidencia |
|---|---|---|---|
| Local | Desarrollo del fundador/equipo; stack completo vía contenedores | Sintéticos | DC |
| Staging | Réplica funcional para validación pre-release y pruebas de pilotos | Sintéticos + anonimizados | DC |
| Producción | Servicio real | Reales, clasificación de 4 niveles (Doc 25) | DC |

- **Despliegue Etapa A:** contenedores en un único proveedor cloud gestionado (PaaS/VM + servicios gestionados para PostgreSQL, Redis, S3). Proveedor específico: **PD** (depende de N-7 residencia/incorporación y de créditos cloud disponibles). (DC/PD)
- **Migraciones:** expand/contract obligatorio; rollback de cada release documentado antes de desplegar. (DC — Doc 25, C-11 del SRS)
- **Infraestructura como código:** SU — recomendada desde Etapa A por reproducibilidad con equipo mínimo; herramienta específica PD.

---

## 7. Alternativas evaluadas para la solución global

| Alternativa | Descripción | Razón de descarte/posposición | Evidencia |
|---|---|---|---|
| **A. Monolito modular + PostgreSQL único (elegida)** | Un backend, una BD, despliegue simple | — | DC |
| B. Microservicios desde el inicio | Servicios por bounded context | Sobrecarga operativa incompatible con equipo de 1 persona (N-10 PD); los bounded contexts se preservan como módulos internos (Doc 24) | DC descartada |
| C. Serverless (funciones) | API como funciones | Write-path de sync transaccional y workers de larga duración encajan mal; cold starts contra RNF-PER | DC descartada |
| D. Supabase/Firebase como backend | BaaS gestionado | Conflictos con autoridad de dominio propia, RLS compleja multi-capa y control del write-path (Docs 24, 27) | DC descartada |
| E. Multi-región activo-activo | Disponibilidad global | Sobredimensionado para Etapa A; RTO ≤4h/RPO ≤15min se cumplen con backups + réplica (Doc 12); Etapa C | DC pospuesta |

---

## 8. Riesgos de la solución

| Riesgo | Impacto | Mitigación | Evidencia |
|---|---|---|---|
| Dependencia de PowerSync como componente central de sync | Alto | N-2 abierto con fallback documentado (Zero); capa de abstracción de sync en clientes (Doc 27 §Alternativas) | DC |
| Complejidad del write-path de sincronización | Alto | 8 casos límite asignados a pruebas normativas; prueba J-2 como criterio de salida de Fase 1 | DC |
| Operación por una sola persona | Alto | Simplicidad deliberada, observabilidad desde Etapa A, régimen Fase 0-1 de acciones críticas | DC |
| Deriva entre documentación e implementación | Medio | C-1 del SRS: la documentación es la verdad; el código la implementa, nunca la redefine | DC |
| Escalado prematuro (presión por "crecer ya") | Medio | Todos los componentes Etapa B tienen criterios medibles; gobernanza trimestral de arquitectura (Doc 20) | DC |

---

## 9. Impacto operativo y evolución a 10 años

La solución de Etapa A está diseñada para que **ninguna decisión de lanzamiento bloquee la evolución**: los bounded contexts son módulos internos extraíbles; el outbox permite añadir Kafka sin cambiar productores; el esquema lógico por contextos permite mover datos a ClickHouse sin reescritura; la separación de planos es permanente; los contratos de API tienen versionado y deprecación de 12 meses (Doc 29 AP-2). El mapa de aplicaciones por etapas (A/B/C) del Doc 20 es el plan maestro que este documento detalla en su Etapa A. (DC)

---

## 10. Criterios de aceptación de este documento

1. Toda componente presente trazada a RF/RNF/ADR; toda componente ausente con criterio de activación. ✅
2. Flujos de extremo a extremo coherentes con los documentos de capa (24–27, 30). ✅
3. N-1 y N-2 permanecen abiertas; ninguna tecnología elegida por tendencia. ✅
4. Separación estricta dominio/aplicación/infraestructura y separación de planos respetadas. ✅
5. Sin código, sin DDL, sin endpoints definitivos. ✅

---

*Registro de cambios — v1.0: creación (Ola 3, documento 10 de 14).*

*v1.1 (2026-07-29) — Errata editorial AO-1 (autorizada por el Fundador, sin cambio de decisiones): identificadores de trazabilidad corregidos al catálogo oficial (RNF-SYNC-003, RNF-SYNC-001, RNF-SEC, RNF-SEC-005, RNF-SCL-003, RNF-PERF-001, RF-REQ-001, RF-WO-003). Auditada la coherencia del mapeo en cada fila.*
