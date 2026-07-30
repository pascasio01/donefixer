# DONEFIXER — 30 · Event Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)

---

## 1. Objetivo
Definir los eventos de dominio como frontera duradera del sistema — el contrato que sobrevivirá a refactorizaciones internas y que alimenta sync, webhooks, KPIs, IA y futuras integraciones (ADR-009: "eventos primero").

## 2. Alcance
Catálogo de eventos, esquema y versionado, transporte (outbox + cola ligera en Etapa A), consumidores, garantías y evolución a bus dedicado (Kafka, Etapa B por criterio E-2).

## 3. Exclusiones
Implementación de consumidores específicos (specs doc 43); streaming IoT (Fase 4); infraestructura (doc 52).

## 4. Decisiones confirmadas (DC)

| # | Decisión | Trazabilidad |
|---|---|---|
| EV-1 | **Todo cambio de estado del dominio emite evento** con esquema versionado | ADR-009 (aprobado), doc 14 §7.7 |
| EV-2 | **Outbox transaccional:** evento y escritura OLTP en el mismo commit (atómicos) | AUD-00 §4, doc 24 BK-5 |
| EV-3 | **Transporte Etapa A: cola ligera** (tabla outbox + workers, o Redis); **Kafka aplazado a Etapa B** con criterio: >5 consumidores o necesidad de replay/CDC a OLAP | AUD-00 E-2, condición permanente 5 |
| EV-4 | Todo evento porta: `event_id`, `event_type` (versionado, p. ej. `work_order.completed.v1`), `tenant_id`, `occurred_at` (servidor), `operation_id` (idempotencia, enlaza con sync), `schema_version`, payload | doc 14 §7.7, doc 26 MT-7 |
| EV-5 | **Esquema registry con compatibilidad hacia atrás**; cambios incompatibles = nuevo `event_type` con versión | ADR-009 |
| EV-6 | Consumidores idempotentes (procesamiento al menos una vez + deduplicación por `event_id`) | AUD-00 §4 |
| EV-7 | Eventos como fuente para: KPIs/rollups, notificaciones, webhooks salientes, auditoría, IA (evaluación), futura CDC a OLAP | ADR-006, doc 24 |

## 5. Decisiones pendientes (PD)
Broker de Etapa B (Kafka vs. Redpanda vs. servicio gestionado — se decide al activar E-2, SU) · retención de eventos (PD-RETENCIÓN).

## 6. Supuestos (SU)
Volumen Etapa A <5K eventos/día/tenant grande — la cola ligera sobra; el replay histórico no es requisito hasta OLAP.

## 7. Catálogo de eventos núcleo (semilla aprobada en doc 14 §7.7, ampliada)

| Contexto | Eventos (v1) |
|---|---|
| Solicitudes | `service_request.created` · `service_request.triaged` · `service_request.linked_duplicate` |
| Órdenes | `work_order.approved` · `work_order.assigned` · `work_order.status_changed` · `work_order.completed` · `work_order.verified` · `work_order.closed` · `work_order.cancelled` |
| PM | `pm_plan.work_order_generated` |
| Activos | `asset.created` · `asset.moved` · `asset.deactivated` · `meter.reading_recorded` |
| Inventario | `stock.moved` · `stock.reorder_triggered` · `stock.discrepancy_detected` |
| Compras | `purchase.approved` · `receipt.recorded` · `invoice.received` · `invoice.flagged` · `invoice.resolved` |
| Inspecciones | `finding.created` · `round.completed` |
| Gobernanza | `sla.breached` · `escalation.triggered` · `evidence.attached` · `sync.conflict_queued` · `ai.decision_recorded` |

## 8. Pipeline de eventos (Etapa A)

```
Transacción de dominio → [dato + evento en outbox, mismo commit] → Worker dispatcher
   → consumidores internos (KPIs, notificaciones, webhooks) con deduplicación
   → marca processed_at; fallos → reintento con backoff → dead-letter con alerta
```
**Garantías:** al menos una vez + idempotencia del consumidor (EV-6); orden por agregado (partición por `aggregate_id` cuando el broker lo soporte; en cola ligera, dispatcher secuencial por agregado); **ningún consumidor escribe directamente en el agregado de otro contexto** — reacciona vía comandos a la capa de aplicación (doc 24 BK-2).

## 9. Alternativas evaluadas

| Alternativa | Costo operativo | Cuándo sería correcta | Veredicto |
|---|---|---|---|
| **Outbox + cola ligera (elegida Etapa A)** | Bajo | Ahora: <5 consumidores, sin replay | **Etapa A** |
| Kafka/Redpanda | Alto (cluster, especialidad) | Etapa B: >5 consumidores, replay, CDC a ClickHouse (E-2) | Aplazado por criterio |
| RabbitMQ | Medio | Equivalente a cola ligera con más operación | Descartado (sin ventaja decisiva en A) |
| Event sourcing completo | Muy alto | No requerido por el dominio (el estado se materializa) | Descartado |
| Sin eventos (llamadas directas) | Bajo aparente | Acopla módulos y rompe BK-3 | Prohibido (EV-1) |

## 10. Estrategia de evolución
El catálogo crece por contexto con revisión del glosario (doc 13); la migración a broker (Etapa B) no cambia productores ni consumidores (el outbox/dispatcher se reemplaza tras la misma interfaz — estrategia de reemplazo); CDC a OLAP consumirá los mismos eventos o el WAL (doc 25 §7.2).

## 11. Riesgos
| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Evento y dato divergen (sin outbox en algún camino) | Media | Alto | Regla EV-2 + test: toda mutación tiene su evento (convención verificada en CI) |
| Consumidor lento acumula cola | Media | Medio | Métrica de lag + alerta (doc 54); escalado del worker |
| Cambio de esquema rompe consumidores | Media | Medio | EV-5 + registry + tests de contrato |
| Dead-letter sin vigilancia | Media | Medio | Alerta obligatoria + runbook (doc 55) |

## 12. Métricas
Eventos/día por tipo · lag del dispatcher · tasa de dead-letter · % mutaciones con evento (objetivo 100%).

## 13. Criterios de aceptación
1. Catálogo núcleo por contexto. ✅ 2. Pipeline con garantías explícitas (atómico, idempotente, ordenado por agregado). ✅ 3. Kafka aplazado con criterio medible. ✅ 4. Estrategia de reemplazo sin tocar consumidores. ✅

## 14. Referencias cruzadas
Depende de: 14, 24, 25, ADR-006/009. Alimenta: 28 (webhooks), 29 (API), 32 (IA evaluación), 51 (KPIs), 54 (observabilidad), 47 (tests de contrato).

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). Catálogo v1 por contexto, pipeline outbox+cola ligera con garantías, Kafka aplazado por criterio E-2, registry con compatibilidad |
