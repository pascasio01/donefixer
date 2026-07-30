# FASE 1 PRE-GO — 01: Master Build Plan

**Versión:** 1.0 · **Fecha:** 2026-07-30 · **Norma:** DC-13 (subordinada a Constitución → Doc 70 → ADRs → DC-01…DC-12)
**Estado:** PRE-GO — planificación. **No autoriza código de producción.** Todo WP de construcción depende de WP-00 (GO del Documento 70).

## 1. Objetivo

Plan íntegro, trazable y verificable para que el desarrollo de producción comience **el mismo día del GO** sin redefinir arquitectura, procesos ni estándares.

## 2. Estructura de fases internas

| Fase interna | Contenido | Criterio de entrada | Criterio de salida |
|---|---|---|---|
| **F1-A Fundaciones** (Sprint 0) | Repositorios, tooling, entornos, pipeline CI/CD, convenciones, esqueleto de solución sin lógica de negocio | WP-00 (GO) | Sprint 0 checklist firmado (entregable 05) |
| **F1-B Plataforma core** | Auth, autorización, multi-tenancy + RLS, PostgreSQL base, outbox/eventos, observabilidad base | F1-A | WPs F1-B-* en Done (DoD + gates) |
| **F1-C Sync y offline** | Write-path, outbox móvil, canal de réplica `{{ADR-014}}`, veredictos | F1-B | J-2 E2E verde en CI con gates de sync |
| **F1-D Módulos de negocio** | Órdenes de trabajo, activos, inventario, solicitudes (MS-* Doc 43) | F1-C | Módulos con cobertura y gates en verde |
| **F1-E Web + móvil** | App web (Doc 22), app móvil `{{ADR-013}}` | F1-D (en paralelo parcial según grafo) | Journeys críticos E2E |
| **F1-F Endurecimiento** | Performance, seguridad, accesibilidad, DR, game days | F1-E | Gates de Doc 47/54/60 en verde; listo para siguiente fase de producto |

## 3. Hitos

| Hito | Definición | Verificación |
|---|---|---|
| H-0 | GO del Doc 70 | Veredicto firmado por el Fundador |
| H-1 | Fundaciones listas | Sprint 0 checklist 100% |
| H-2 | Plataforma core operativa en staging | Tests E2E auth/RLS/outbox verdes |
| H-3 | J-2 completo en staging (sync real) | Suite J-2 de la Spike portada a producción: verde |
| H-4 | Módulos Fase 1 completos | DoD + cobertura + gates por módulo |
| H-5 | Release candidate Fase 1 | Gates de endurecimiento + runbooks ensayados |

## 4. Equipo y responsables (roles del Master Prompt Fase 1)

Un responsable técnico por WP (ver WBS). Regla: el responsable de un WP no aprueba su propio PR (Code Review Checklist).

## 5. Parametrización obligatoria (DC-13)

| Variable | Afecta a | Se instancia con |
|---|---|---|
| `{{ADR-013}}` | WPs F1-E móvil, tooling móvil del Sprint 0, CI móvil | ADR-013 aprobado (Flutter o RN+Expo) |
| `{{ADR-014}}` | WPs F1-C canal de réplica, infra de sync, CI/CD de sync | ADR-014 definitivo (PowerSync Cloud o Self-Hosted) |

**Prohibido instanciar estas variables antes de la aprobación formal de cada ADR.** Los WPs parametrizados se planifican completos en estructura y se activan al instante del ADR correspondiente.

## 6. Riesgos del plan (resumen; detalle en WBS por WP)

- R-P1: retraso de ADR-013/014 → mitigación: todo lo no parametrizado avanza igual (F1-A/B/D parcial).
- R-P2: subestimación de sync en producción real → mitigación: evidencia Spike Fase 1/2 como base de estimación; budgets MA-8.
- R-P3: deriva documentación↔código → mitigación: WP de documentación sincronizada en cada DoD + verificación de integridad en CI.

## 7. Trazabilidad

Constitución regla 6 · Doc 70 (WP-00) · DC-13 · Docs 21–33 (arquitectura) · Doc 43 (MS-*) · Doc 47 (gates) · Doc 54 (SRE) · Doc 60 (seguridad) · Doc 62 (FinOps) · ADI (ADRs).
