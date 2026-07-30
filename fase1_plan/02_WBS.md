# FASE 1 PRE-GO — 02: Work Breakdown Structure (WBS)

**Norma:** DC-13 · Cada WP lleva los 16 campos obligatorios. Parametrización: `{{ADR-013}}` móvil, `{{ADR-014}}` sync. WP-00 = GO del Doc 70; ningún WP de construcción tiene ruta que lo evite.
**Convención de estimación:** en puntos ideales de ingeniería (1 pt ≈ 1 día). DoR/DoD completos en entregables 12 y doc. `DoR_DoD.md` — aquí se referencia la variante aplicable.

---

## WP-00 — Veredicto GO del Documento 70

| Campo | Valor |
|---|---|
| Objetivo | Autorización formal de inicio de desarrollo de producción |
| Dependencias | Cierre de N-1, N-2, PD-CLOUD, PD-IA-1, PD-4 (regla de ejecución DC-12) |
| Entradas | Expediente `gate_doc70/` completo; evidencias de spikes |
| Salidas | Veredicto firmado (GO / GO WITH CONDITIONS) |
| Riesgos | NO GO → replanificar según acciones requeridas |
| RF/RNF/ADR | — / — / todos los aprobados |
| DoR/DoD | Regla de ejecución DC-12 / Veredicto firmado por el Fundador |
| Pruebas | Verificación automática `verificacion_gate70.py` sin FAIL |
| Estimación | 5 pt (auditoría sobre expediente preparado) |
| Responsable | Comité Doc 70 + Fundador |
| Riesgos residuales | Condiciones del GO WITH CONDITIONS con responsable y fecha |

---

## F1-A — Fundaciones (Sprint 0; detalle operativo en entregable 05)

### WP-A1 — Organización del monorepo y tooling base
- **Objetivo:** estructura de repositorio, convenciones, linters, formateo, plantillas de PR/ADR.
- **Dependencias:** WP-00 · **Entradas:** Doc 00, Doc 47 · **Salidas:** repo inicializado con pipelines vacíos funcionando.
- **Riesgos:** bajo. · **RF/RNF/ADR:** — / RNF-MNT-001 / — · **Pruebas:** pipeline "hola mundo" verde.
- **Estimación:** 3 pt · **Responsable:** Principal DevOps · **Residuales:** —

### WP-A2 — Entornos (dev / staging) e IaC base
- **Objetivo:** entornos reproducibles, secrets manager, baseline de observabilidad.
- **Dependencias:** WP-A1 · **Salidas:** staging desplegable con un servicio mínimo.
- **RF/RNF/ADR:** — / RNF-AVL-001, RNF-SEC-004 / ADR-00x (cloud: **PD-CLOUD — parametrizado `{{PD-CLOUD}}`**)
- **Pruebas:** destroy+apply reproducible; runbook de aprovisionamiento.
- **Estimación:** 5 pt · **Responsable:** Principal Cloud · **Residuales:** coste FinOps monitorizado desde el día 1 (Doc 62).

### WP-A3 — Esqueleto de solución .NET 8 (sin lógica de negocio)
- **Objetivo:** solution layout (Domain/Application/Infrastructure/API), convenciones de código, analizadores, nullable strict.
- **Dependencias:** WP-A1 · **RF/RNF/ADR:** — / RNF-MNT-002 / Doc 21 · **Pruebas:** build + análisis estático verde.
- **Estimación:** 3 pt · **Responsable:** Principal Backend (.NET)

### WP-A4 — Esqueleto web React (sin lógica de negocio)
- **Dependencias:** WP-A1 · **RF/RNF/ADR:** — / RNF-PERF-003, RNF-ACC-001 / Doc 22, Doc 40 (tokens DS-*)
- **Estimación:** 3 pt · **Responsable:** Principal Web

### WP-A5 — Esqueleto móvil `{{ADR-013}}` — **PARAMETRIZADO**
- **Dependencias:** WP-A1 + **ADR-013 aprobado** · **RF/RNF/ADR:** — / RNF-MOB-001, RNF-PERF-004 / ADR-013, Doc 23
- **Estimación:** 3 pt (la estructura es idéntica en ambas variantes; solo cambia el toolchain) · **Responsable:** Principal Mobile
- **Riesgos:** instanciación prematura prohibida (DC-13).

---

## F1-B — Plataforma core

### WP-B1 — Esquema PostgreSQL base + migraciones
- **Objetivo:** DDL núcleo (tenants, users, roles), estrategia de migraciones (ver entregable 10).
- **Dependencias:** WP-A2, WP-A3 · **RF/RNF/ADR:** RF-TEN-001 / RNF-SEC-006, RNF-MNT-003 / Doc 28, Doc 26
- **Pruebas:** migración up/down en CI; verificación de integridad de esquema.
- **Estimación:** 4 pt · **Responsable:** Principal Database

### WP-B2 — Multi-tenancy con RLS (rol no privilegiado + FORCE RLS)
- **Objetivo:** `app.current_tenant` transaccional (MT-4), rol de aplicación sin privilegios (**lección empírica de la Spike: superuser bypassa RLS**), test de ataque cross-tenant obligatorio en CI.
- **Dependencias:** WP-B1 · **RF/RNF/ADR:** RF-TEN-002 / RNF-SEC-006 / Doc 26 (MT-3/MT-4), SPIKE_S2_S3
- **Pruebas:** test de ataque RLS (0 filas cross-tenant) + intento de bypass con rol de app.
- **Estimación:** 4 pt · **Responsable:** Principal Database + Principal Security

### WP-B3 — Autenticación (servicio de identidad, sesiones, revocación)
- **Dependencias:** WP-B2 · **RF/RNF/ADR:** RF-USR-001 / RNF-SEC-001, RNF-SEC-005 / Doc 29
- **Estimación:** 6 pt · **Responsable:** Principal Backend + Principal Security

### WP-B4 — Autorización (RBAC + permisos por módulo)
- **Dependencias:** WP-B3 · **RF/RNF/ADR:** RF-USR-002 / RNF-SEC-002 / Doc 29, Doc 43 (MS-0)
- **Estimación:** 5 pt · **Responsable:** Principal Backend

### WP-B5 — Outbox + bus de eventos interno
- **Objetivo:** outbox transaccional (EV-1), publicador, consumidores base, DLQ.
- **Dependencias:** WP-B1 · **RF/RNF/ADR:** RF-PLT-001 / RNF-AVL-002 / Doc 25 (EV-1)
- **Pruebas:** cero pérdida bajo kill del publicador (chaos, portado de la Spike).
- **Estimación:** 5 pt · **Responsable:** Principal Backend

### WP-B6 — Observabilidad base (logs, métricas, trazas, dashboards núcleo)
- **Dependencias:** WP-A2, WP-A3 · **RF/RNF/ADR:** — / RNF-OBS-001…003 / Doc 54 (golden signals, SLO)
- **Estimación:** 4 pt · **Responsable:** Principal SRE

---

## F1-C — Sync y offline (corazón validado por la Spike)

### WP-C1 — Write-path de sincronización (port de la Spike a producción)
- **Objetivo:** idempotencia por `operation_id`, HLC, re-validación servidor (ADR-011 v1.1), veredictos ACCEPT/ADJUST/REJECT, tombstones — **portado del código de investigación validado, no reescrito desde cero** (reutilización autorizada solo vía ADR expreso del Fundador, EXENCIÓN-SPIKE-01 regla 8 — incluir ese ADR en este WP).
- **Dependencias:** WP-B2, WP-B5 · **RF/RNF/ADR:** RF-WO-003 / RNF-SYNC-001…005 / ADR-011 v1.1, ADR-014 fase 1 (DC-C), Doc 27
- **Pruebas:** suite J-2 de la Spike portada: 15/15 verde + chaos + idempotencia en CI.
- **Estimación:** 8 pt · **Responsable:** Principal Backend · **Residuales:** confirmación de ADR-014 fase 1 en el cierre de N-2.

### WP-C2 — Canal de réplica `{{ADR-014}}` — **PARAMETRIZADO**
- **Objetivo:** integración del canal aprobado (Cloud o Self-Hosted) tras el MA-1 del lado servidor, sync rules por tenant, checkpoints.
- **Dependencias:** WP-C1 + **ADR-014 definitivo aprobado** · **RF/RNF/ADR:** RF-PLT-002 / RNF-SYNC-002, RNF-SEC-006 / ADR-014, Doc 26, Doc 27
- **Pruebas:** la batería F2 de la Spike portada (F2-IT/CT/CH/LT) sobre el entorno de staging.
- **Estimación:** 8 pt · **Responsable:** Principal Backend + Principal DevOps
- **Riesgos:** instanciación prematura prohibida; configuración según Anexo de Reproducibilidad Fase 2.

### WP-C3 — Outbox móvil y adapter MA-1 `{{ADR-013}}` — **PARAMETRIZADO**
- **Objetivo:** outbox local en la misma transacción SQLite (SY-4), cola con reintentos, UI de veredictos (SY-9).
- **Dependencias:** WP-A5 ({{ADR-013}}), WP-C2 ({{ADR-014}}) · **RF/RNF/ADR:** RF-WO-001 / RNF-SYNC-003, RNF-MOB-002 / ADR-013, ADR-014, Doc 23 (MA-1/MA-2)
- **Pruebas:** J-2 modo avión literal en dispositivo (criterio de salida de la Spike, portado).
- **Estimación:** 8 pt · **Responsable:** Principal Mobile

### WP-C4 — Resolución de conflictos y bandeja "Requiere tu atención"
- **Dependencias:** WP-C1 · **RF/RNF/ADR:** RF-WO-004, RF-WO-005 / RNF-SYNC-005, RNF-USE-004 / Doc 27, Doc 40
- **Estimación:** 5 pt · **Responsable:** Principal Backend + Principal UX

---

## F1-D — Módulos de negocio (Doc 43, plantilla MS-0 de 17 campos)

### WP-D1 — Módulo Órdenes de Trabajo (core)
- **Dependencias:** WP-C1, WP-C4 · **RF:** RF-WO-001…008 · **RNF:** RNF-PERF-005, RNF-USE-001 · **ADR:** ADR-011 v1.1
- **Pruebas:** máquina de estados (matriz Doc 14) 100% cubierta; evidencias inmutables en OT cancelada/cerrada.
- **Estimación:** 10 pt · **Responsable:** Principal Backend + Principal Mobile/Web

### WP-D2 — Módulo Activos
- **Dependencias:** WP-B4 · **RF:** RF-AST-001…004 · **RNF:** RNF-PERF-005 · **Estimación:** 7 pt

### WP-D3 — Módulo Inventario (deltas, nunca `set`)
- **Dependencias:** WP-C1 · **RF:** RF-INV-001…004 · **RNF:** RNF-SYNC-004 · **Regla:** consumos idempotentes por `operation_id` UNIQUE (validado en Spike).
- **Estimación:** 7 pt

### WP-D4 — Módulo Solicitudes (intake + QR)
- **Dependencias:** WP-B4 · **RF:** RF-REQ-001…003, RF-WO-006 · **Estimación:** 5 pt

### WP-D5 — Módulo Usuarios y equipos
- **Dependencias:** WP-B4 · **RF:** RF-USR-001…003 · **Estimación:** 5 pt

*(Los 8 módulos restantes de Doc 43 se planifican en Fase 2 de producto — fuera del alcance Fase 1.)*

---

## F1-E — Experiencias

### WP-E1 — App web: journeys Fase 1 (Doc 22, WA-*)
- **Dependencias:** WP-D1…D5 · **RNF:** RNF-PERF-003, RNF-ACC-001 · **Estimación:** 12 pt · **Responsable:** Principal Web

### WP-E2 — App móvil `{{ADR-013}}`: journeys Fase 1 — **PARAMETRIZADO**
- **Dependencias:** WP-C3, WP-D1 · **RNF:** RNF-PERF-004, RNF-MOB-003, RNF-USE-001 · **Estimación:** 14 pt

### WP-E3 — Design System aplicado (tokens DS-*, estados offline/vacío/error/carga/permiso)
- **Dependencias:** WP-A4/A5 · **Fuente:** Doc 40 · **Estimación:** 6 pt · **Responsable:** Principal UX + Principal Accessibility

---

## F1-F — Endurecimiento

### WP-F1 — Performance: presupuestos MA-8 verificados en CI
- **Dependencias:** WP-E1, WP-E2 · **RNF:** RNF-PERF-001…005 · **Estimación:** 5 pt

### WP-F2 — Seguridad: pentest interno, SBOM, rotación de secretos ensayada
- **Dependencias:** todos los F1-B · **Fuente:** Doc 60 · **Estimación:** 6 pt

### WP-F3 — Accesibilidad: auditoría WCAG 2.2 AA sobre journeys críticos
- **Dependencias:** WP-E1, WP-E3 · **Fuente:** Doc 40 · **Estimación:** 4 pt

### WP-F4 — DR/Backup-restore ensayado + game days con runbooks RB-01…08
- **Dependencias:** WP-B6 · **Fuente:** Doc 54 · **Estimación:** 5 pt

### WP-F5 — FinOps: dashboards de coste por tenant + línea roja IA monitorizada
- **Dependencias:** WP-B6 · **Fuente:** Doc 62 · **Estimación:** 3 pt

---

**Total estimado Fase 1:** ~133 pt ideales (sin contar WP-00). **Nota honesta:** estimación de planificación SU — se recalibra tras los dos primeros sprints reales con velocidad medida, según Doc 51.
