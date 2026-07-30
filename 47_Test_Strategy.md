# 47 — Test Strategy

| Campo | Valor |
|---|---|
| Documento | 47_Test_Strategy |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Precedencia | Doc 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 12 (RNF), 27 (8 casos normativos sync), 26 (matriz de ataques MT), 19 (matriz de roles), 16 (Journeys), 43 (MS-0 §17), MASTER_PROMPT §TESTING; AO-5 |

> **Regla de oro (MASTER_PROMPT, DC):** ningún módulo se considera terminado hasta completar todas las capas aplicables: unit, integration, contract, E2E, security, performance, offline, sync-conflict, accessibility, chaos, DR validation, backup-restore validation.

---

## 1. Pirámide y propósito por capa

| Capa | Alcance | Propietario lógico | Herramientas tipo |
|---|---|---|---|
| Unit | Dominio puro, validaciones provisionales, HLC, outbox, máquina de estados | Módulo | xUnit/Vitest/framework test del móvil (N-1 PD) |
| Integration | Módulo + PostgreSQL/RLS/Redis/S3 reales (contenedores) | Módulo | Testcontainers |
| Contract | OpenAPI (Doc 29) y esquemas de eventos (Doc 30) — productor/consumidor | Plataforma | Contract testing + validación de esquemas |
| E2E | Journeys J-1…J-9 por canal | Producto | Playwright (web), E2E dispositivo (móvil) |
| Security | Matriz de ataques MT (Doc 26), OWASP ASVS, authz por rol | Seguridad | Suites + SAST/DAST (RNF-SEC-007) |
| Performance | Presupuestos §4 | Performance | k6 / Lighthouse CI / profiling |
| Offline | J-2 literal, captura web con cola, degradación IA | Producto | Modo avión real/simulado |
| Sync-conflict | Matriz normativa completa + 8 casos Doc 27 | Plataforma | Harness de conflictos |
| Accessibility | axe CI + lector de pantalla en flujos críticos | Producto | axe + NVDA/TalkBack/VoiceOver |
| Chaos | Red intermitente, kill de proceso, caída de dependencias | SRE | Chaos harness en staging |
| DR validation | RTO ≤4h / RPO ≤15 min ensayados | SRE | Ejercicio trimestral (Doc 54) |
| Backup-restore | Restauración real con acta | SRE | **AO-5: trimestral (RNF-AVL-004)** |

## 2. Quality Gates (QG)

| Gate | Criterio | Bloquea |
|---|---|---|
| QG-1 Merge | Unit+integration verdes; cobertura núcleo ≥80% (RNF-MNT-001); 0 N+1 (RNF-PERF-005); SAST/SCA sin críticas; **tests de aislamiento multi-tenant 100% (RNF-SEC-006)**; axe sin críticas | Merge a main |
| QG-2 Release candidata | Contract tests verdes; E2E de journeys afectados; performance budgets en CI; security gates §5; migration expand/contract verificada con rollback ensayado | Deploy a staging |
| QG-3 Producción | Chaos + offline + sync-conflict de la release; DR/backup-restore al día (<1 trimestre); Production Verification §7 en staging | Deploy a producción |
| QG-4 Activación de agente IA | Golden-set del caso de uso superando umbral (RNF-AI-007); prohibiciones verificadas como tests de permisos (RNF-AI-003); FinOps de cuota configurado | Activación por caso de uso |

## 3. Cobertura mínima

| Ámbito | Mínimo | Nota |
|---|---|---|
| Dominio puro (reglas críticas) | 100% de ramas de la máquina de estados OT y de la matriz de conflictos | La cobertura aquí no es negociable (DC) |
| Núcleo de módulos | ≥80% (RNF-MNT-001, SU) | Calidad > porcentaje: tests triviales no cuentan |
| Clientes web/móvil | Flujos críticos cubiertos por E2E; stores/casos de uso con unit | WA-10/MA-10 |
| Matriz de roles | Toda transición OT × rol probada (permitida y denegada) | Doc 19 |

## 4. Performance Budgets (entrada a CI)

| Presupuesto | Valor | Fuente |
|---|---|---|
| API lectura p95 | <500 ms | RNF-PERF-001 |
| Carga inicial web p95 (4G) | <3 s; ≤200 KB JS gzip primer paint | RNF-PERF-003; WA-9 |
| Apertura OT local | <1 s | RNF-PERF-004 |
| Lectura local SQLite | <100 ms p95 | RNF-PERF-002 |
| Búsqueda FTS local | ≤300 ms p95 | MA-8 (aclaración AO-3) |
| Convergencia sync (red estable) | <60 s p95 | RNF-SYNC-002 |
| Copiloto IA | <5 s p95 | RNF-AI-006 |

## 5. Security Gates

- SAST/SCA/secretos/DAST en pipeline con bloqueo en severidad crítica (RNF-SEC-007).
- Batería de aislamiento multi-tenant: 100% pasando, bloquea merge (RNF-SEC-006) — matriz de ataques del Doc 26 automatizada.
- Tests de autorización: toda operación del Doc 29 probada con rol permitido y denegado.
- Tests de prohibiciones IA como tests de permisos (RNF-AI-003): la Service Account sin permiso recibe 403 — no "se le pide no hacerlo".
- Pentest externo antes de lanzamiento público y anual (RNF-SEC-008, SU).

## 6. Mutation Testing

Aplicable cuando: dominio puro y módulo de sync alcancen cobertura estable (Etapa A tardía). Objetivo: mutation score ≥70% en paquetes de reglas críticas (máquina de estados, conflictos, HLC). Herramienta: Stryker (web) / equivalente .NET (SU — evaluar en Fase 1; no es gate de Etapa A inicial, se activa por ADR si el equipo lo adopta). (SU)

## 7. Production Verification (post-deploy, staging→producción)

1. Smoke de journeys críticos (J-1, J-2, J-8) contra producción con tenant de verificación.
2. Verificación de migración: estado expand correcto, rollback plan cargado.
3. Verificación de sync: reloj de convergencia y lag por dispositivo dentro de SLO (RNF-SYNC-002/006).
4. Verificación de observabilidad: alertas disparan en canal correcto (Doc 54); trazas con `tenant_id` al 100% (RNF-OBS-001).
5. Verificación FinOps: costos IA registrándose por tenant (RNF-AI-004).
6. Acta de verificación firmada en el changelog de release. (DC)

## 8. Pruebas normativas de sincronización (heredadas del Doc 27, vinculantes)

Los 8 casos límite (doble completado de OT, stock concurrente offline, tombstone vs. edición, wipe+relogin, dispositivo compartido, evidencia con binario interrumpido, HLC con reloj atrasado, operación duplicada por reintento) son **tests permanentes del repositorio**; modificar la matriz de conflictos exige actualizar estos tests en el mismo cambio. (DC)

## 9. Datos de prueba

Sintéticos por defecto; anonimizados de pilotos solo con consentimiento; clasificación de datos aplicada también en ambientes no productivos (Doc 25); prohibido copiar producción a local (RNF-PRV-001). (DC)

## 10. Criterios de aceptación del documento

1. Incluye los 7 elementos de la ampliación obligatoria (gates, cobertura, mutation, budgets, security gates, accessibility gates, production verification). ✅
2. Hereda y formaliza las 12 capas del MASTER_PROMPT §TESTING. ✅
3. AO-5 (restauración trimestral) integrada. ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación (Ola 4, documento 3 de 8) con las ampliaciones obligatorias del Fundador.*
