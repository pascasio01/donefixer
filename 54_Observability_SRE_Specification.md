# 54 — Observability & SRE Specification

| Campo | Valor |
|---|---|
| Documento | 54_Observability_SRE_Specification |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Precedencia | Doc 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 12 (RNF-AVL/OBS/SYNC), 21 §5, 26 (noisy neighbor), 27 (lag sync), 33 (FinOps alertas), 47 (QG-3); MASTER_PROMPT (Observability Ready) |

---

## 1. Stack y modelo de telemetría (DC)

OpenTelemetry de extremo a extremo (trazas, métricas, logs correlacionados) con backends intercambiables (Doc 21 §5). Correlación obligatoria: `trace_id`, `tenant_id`, `actor_id`, `operation_id` cuando aplique (RNF-OBS-001/003). `tenant_id` como atributo en el 100% de requests — habilita métricas por tenant y detección de noisy neighbor (RNF-SCL-003). (DC)

## 2. Golden Signals por servicio

| Servicio | Latencia | Tráfico | Errores | Saturación |
|---|---|---|---|---|
| API tenant | p95 por endpoint (RNF-PERF-001) | rpm por tenant | 5xx rate | CPU/mem, pool de conexiones |
| Write-path sync | Veredicto por operación | ops/s por dispositivo | REJECT rate, reintentos | Outbox depth, cola de conflictos |
| Réplica PowerSync | Lag de replicación | bytes/ops replicadas | Fallos de canal | Lag por dispositivo (RNF-SYNC-006) |
| PostgreSQL | Slow queries | TPS | Deadlocks, errores | Conexiones, WAL, disco |
| AI Gateway | Latencia copiloto (<5 s, RNF-AI-006) | requests por caso de uso | Fallos proveedor, abstenciones | Tokens/s, costo/minuto |
| Workers | Duración por job | jobs/min | Fallos, reintentos | Backlog outbox |

## 3. SLI / SLO / Error Budget

| SLI | SLO (interno, no contractual) | Error budget mensual | Fuente |
|---|---|---|---|
| Disponibilidad API | 99.5% | ~3.6 h/mes | RNF-AVL-001 |
| Éxito de sync diario por dispositivo | >99.9% | <0.1% dispositivos-día | RNF-SYNC-001 |
| Convergencia sync | <60 s p95 | 5% de ventanas | RNF-SYNC-002 |
| Latencia API lectura | <500 ms p95 | 5% de requests | RNF-PERF-001 |
| Copiloto IA | <5 s p95 | 5% | RNF-AI-006 |

**Política de error budget:** consumido >50% antes de mitad del mes → congelar features de riesgo y priorizar confiabilidad (decisión registrada en Consola). Consumido 100% → solo trabajo de confiabilidad hasta recuperación. (DC)

## 4. Dashboards

| Dashboard | Audiencia | Contenido |
|---|---|---|
| Salud de plataforma | Fundador/SRE | Golden signals, SLOs, error budget restante |
| Sync & offline | SRE/Producto | Éxito diario, lag por dispositivo, cola de conflictos, veredictos por causa |
| Negocio | Fundador | KPIs Doc 51 §3 (activación, WAU técnicos, churn pilotos) |
| FinOps | Fundador | Costo por tenant, costo IA vs. línea roja 30%, presupuesto infra (Doc 62) |
| Estado del servicio (tenant) | P-C1 (Consola tenant) | Su consumo, su sync, su cuota IA (RNF-AI-004) |

## 5. Alert Routing

| Severidad | Canal | Tiempo de respuesta esperado | Ejemplos |
|---|---|---|---|
| P1 (crítica) | Push/llamada al on-call (fundador en Etapa A) | ≤30 min | API caída, pérdida de datos (RNF-SYNC-004), brecha de aislamiento tenant |
| P2 (alta) | Chat/correo urgente | ≤4 h | Error budget quemándose rápido, lag de sync sostenido, outbox creciendo |
| P3 (informativa) | Digest diario | Revisión diaria | Degradación IA por tenant, cuota >80%, certificado por vencer |

Regla: alertas por **síntoma** con runbook enlazado, no por causa especulativa (RNF-OBS-004); toda alerta sin acción posible se elimina o se convierte en métrica. (DC)

## 6. Runbooks (mínimos de Etapa A)

RB-01 API caída / health failing · RB-02 Lag de sync elevado · RB-03 Outbox detenido o creciendo · RB-04 Aislamiento tenant sospechoso (contención inmediata: revocar, congelar, auditar) · RB-05 Proveedor LLM caído (degradación IA, RNF-AI-005) · RB-06 Costo IA desbordado (throttle de cuota) · RB-07 Restauración desde backup · RB-08 Rollback de release. Cada runbook: síntomas, diagnóstico, acciones, escalación, cierre. (DC)

## 7. Incident Classification

| Clase | Definición | Ejemplo |
|---|---|---|
| SEV-1 | Pérdida/corrupción de datos o brecha de seguridad/aislamiento | Fuga cross-tenant |
| SEV-2 | Función núcleo inutilizable para ≥1 tenant | Sync detenido |
| SEV-3 | Degradación con workaround | Copiloto lento |
| SEV-4 | Sin impacto de usuario visible | Métrica anómala |

Toda SEV-1/SEV-2 exige postmortem (§8). SEV-1 por pérdida de datos: postmortem obligatorio aunque el impacto sea cero (RNF-SYNC-004). (DC)

## 8. Postmortem Template (normativo)

1. Resumen (qué pasó, impacto, duración, tenants afectados) · 2. Línea de tiempo (detección→mitigación→resolución) · 3. Causa raíz (técnica, sin culpa — blameless) · 4. Qué detectó/falló en observabilidad · 5. Acciones correctivas (responsable + fecha, trazadas en Consola) · 6. Lecciones y cambios a runbooks/tests · 7. Registro en el changelog del documento afectado. Prohibido: postmortems sin acciones o con culpables personales. (DC)

## 9. DR y continuidad

RTO ≤4 h / RPO ≤15 min (RNF-AVL-002/003, SU); restauración ensayada **trimestralmente con acta** (RNF-AVL-004, AO-5 integrada); ejercicio de DR trimestral alternando escenarios (restore completo, restore point-in-time, pérdida de región lógica). Backups cifrados (RNF-SEC-002) fuera de la cuenta primaria. (DC)

## 10. Operación con equipo de una persona (N-10 PD)

On-call único con: alertas P1 únicamente accionables, runbooks ejecutables paso a paso, status page pre-lanzamiento (RNF-OBS-005, SU), y comunicación de incidentes a tenants desde la Consola (ADR-012). Cualquier SLO que exija respuesta 24/7 humana se declara inviable y se revisa (precedente: relajación 99.9→99.5%, AUD-00 §14). (DC)

## 11. Criterios de aceptación del documento

1. Incluye los 9 elementos de la ampliación obligatoria. ✅
2. SLOs coherentes con RNF-AVL/SYNC/PERF/AI (verificado contra catálogo). ✅
3. AO-5 integrada (§9). ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación (Ola 4, documento 5 de 8) con las ampliaciones obligatorias del Fundador.*
