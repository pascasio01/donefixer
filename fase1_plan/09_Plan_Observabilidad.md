# FASE 1 PRE-GO — 09: Plan de Observabilidad

**Norma:** DC-13 · Fuente: Doc 54 (golden signals, SLO/SLI, error budget, RB-01…08), Doc 62 (FinOps).

## 1. Logging Strategy

- Logs estructurados (JSON) con `tenant_id`, `operation_id` (cuando aplique sync), `trace_id`, nivel, componente, WP/módulo.
- **Prohibido** registrar: secretos, tokens, datos personales completos, payloads de evidencias.
- Retención por clase según Doc 54; logs de auditoría de seguridad según Doc 60/26.

## 2. Metrics Strategy (SLI por dominio)

| Dominio | SLI | SLO (Doc 54) | Fuente |
|---|---|---|---|
| API | disponibilidad, p95 latencia | según Doc 54 §SLO | Doc 54 |
| Sync | ops/s, p95 convergencia, tasa de veredictos REJECT, reintentos | convergencia <60 s p95 (RNF-SYNC-002); pérdida = 0 (RNF-SYNC-004) | Doc 27, Spike |
| DB | conexiones, locks, replicación WAL (requerido por canal sync) | Doc 28 | Doc 54 |
| Auth | logins fallidos/anomalías | Doc 29 | Doc 60 |
| Móvil | crash-free sessions, arranque, batería (telemetría opt-in) | RNF-MOB-001/003, RNF-PERF-004 | Doc 23 |
| FinOps | coste/tenant, coste IA/tenant (línea roja 30%) | Doc 62 | Doc 62 |

## 3. Tracing Strategy

- Traza distribuida de punta a punta: API → dominio → DB → outbox → publicador → canal sync `{{ADR-014}}` → veredicto.
- El `operation_id` de sync es atributo de span obligatorio en C1/C2 (depuración de conflictos, SY-9).

## 4. Dashboard Blueprint

| Dashboard | Audiencia | Contenido |
|---|---|---|
| Golden signals servicio | SRE | latencia, tráfico, errores, saturación por servicio |
| Sync health | SRE + producto | cola outbox, convergencia, veredictos por tipo, tenants con más conflictos |
| Negocio (KPI Doc 51) | Fundador/producto | uso por módulo, WOTC candidato (PD-2 sigue PD hasta aprobación) |
| FinOps | Fundador + SRE | coste por tenant, líneas rojas Doc 62, forecast |
| Seguridad | Security | intentos cross-tenant bloqueados (debe ser 0), anomalías auth, rotaciones pendientes |

## 5. Alert Blueprint

- Clasificación SEV (Doc 54): SEV-1 sync caído o pérdida de datos; SEV-2 degradación p95 > 2× SLO; SEV-3 warnings.
- Enrutado: SEV-1/2 → guardia + canal de incidentes; SEV-3 → revisión diaria.
- **Alertas FinOps como SEV-3 automático** (Doc 62); línea roja IA → SEV-2.
- Anti-ruido: toda alerta requiere runbook enlazado; alerta sin acción clara se elimina o se reclasifica.

## 6. Runbook Index (RB-* Doc 54, obligatorio por módulo en DoD)

RB-01 sync degradado · RB-02 outbox creciente · RB-03 RLS/anomalía de tenant · RB-04 DB saturada · RB-05 auth caído · RB-06 coste IA fuera de línea roja · RB-07 canal réplica `{{ADR-014}}` caído · RB-08 rollback de release. Cada runbook: síntomas, verificación, acción, escalado, criterio de cierre; ensayado en game days (WP-F4).
