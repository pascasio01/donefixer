# SPIKE FASE 2 — S1: Especificación (N-2 — PowerSync Cloud vs Self-Hosted)

**Versión:** 1.0 · **Fecha:** 2026-07-30 · **Estado:** DC (Carril A autorizado por DECISIÓN DEL FUNDADOR DC-01…DC-05)
**Norma:** MASTER PROMPT — Architecture Spike Enterprise v1.1 (DC-01) · EXENCIÓN-SPIKE-01 (vigente, no modificada)
**Clasificación de evidencia:** DC / SU / PD obligatoria en cada métrica, puntuación y conclusión.

---

## 1. Propósito y ámbito

Generar evidencia técnica **reproducible** para cerrar **N-2** (estrategia definitiva de sincronización: PowerSync Cloud vs PowerSync Self-Hosted) mediante el **ADR-014 definitivo**. 

**Fuera de alcance (prohibido):** construir producto, ampliar funcionalidades, modificar la arquitectura aprobada, implementar nuevas características, evaluar alternativas distintas de Cloud/Self-Hosted, cerrar N-1 (permanece PD), aprobar ADR-014 fase 1 como definitiva (registrada como DC-C, validación técnica preliminar del write-path).

**Naturaleza del trabajo:** todo lo producido es **documentación e infraestructura de evaluación** (código de investigación técnica). No es código de producción. Reutilización en producción solo por ADR expreso del Fundador.

## 2. Journey bajo prueba (idéntico a Fase 1)

**J-2:** Orden de Trabajo Offline → Edición → Adjuntar Evidencias → Sincronización → Conflictos → Resolución → Confirmación de usuario. No se agrega ningún otro flujo.

## 3. Entornos y variables controladas

| | Entorno A | Entorno B |
|---|---|---|
| Canal de réplica | PowerSync **Cloud** | PowerSync **Self-Hosted** (Docker) |
| PostgreSQL | Idéntico (misma versión, mismo schema, mismo seed) | Idéntico |
| Backend / Dominio / API | Write-path propio validado en Fase 1 (sin cambios) | Idéntico |
| Dataset | `seed_j2.sql` (2 tenants, mismos usuarios/roles/OTs) | Idéntico |
| RLS | `app_spike` + FORCE ROW LEVEL SECURITY | Idéntico |
| Casos de prueba | Misma batería, mismos criterios PASS/FAIL | Idénticos |

**Única variable permitida:** el servicio PowerSync (Cloud vs Self-Hosted). Cualquier otra diferencia invalida la comparación y se documenta como desviación.

## 4. Matriz de decisión oficial N-2 (DC-02)

| Criterio | Peso | Métricas que lo alimentan |
|---|---|---|
| **MDN2-1 Confiabilidad y consistencia de sincronización** | 30% | Idempotencia, veredictos exactos de conflicto, reconexión, pérdida de red, reinicio de servidor, recuperación automática, reintentos |
| **MDN2-2 Operación y mantenibilidad** | 20% | Instalación, configuración, actualizaciones, monitoreo, logs, backups, recuperación, mantenimiento, coste operativo |
| **MDN2-3 Rendimiento** | 15% | Tiempo de sync, latencia, throughput, recuperación, reconexión, CPU, memoria, red |
| **MDN2-4 Seguridad** | 15% | Credenciales, TLS, rotación de secretos, auditoría, superficie de ataque, aislamiento entre tenants |
| **MDN2-5 TCO** | 10% | Infraestructura, operación, licencias, escalabilidad de coste, personal requerido, riesgo operativo |
| **MDN2-6 Escalabilidad** | 5% | 10 / 100 / 1.000 / 10.000 usuarios (simulados donde sea necesario, clasificado SU) |
| **MDN2-7 Riesgo tecnológico** | 5% | Dependencia de proveedor, madurez, continuidad, reversibilidad |

- Escala de puntuación: 1–5 por criterio y alternativa.
- **Toda puntuación exige:** evidencia + métrica + justificación + referencia a la prueba (p. ej. `F2-CT-04`). Puntuación sin evidencia = inválida.
- La ponderación solo se ajusta con justificación técnica documentada y aprobación del Fundador.
- La matriz de Doc 23 §4 sigue aplicándose **exclusivamente a N-1** (DC-02).

## 5. Batería de pruebas (idéntica en ambos entornos)

Prefijo de casos: `F2-`. Capas: Unit (F2-UT), Integration (F2-IT), Offline (F2-OT), Conflict (F2-CT), Chaos (F2-CH), Recovery (F2-RT), Load (F2-LT), Failover (F2-FT), Long Running (F2-LR).

| ID | Prueba | Criterio PASS |
|---|---|---|
| F2-UT-01 | Write-path: máquina de estados, HLC, idempotencia (suite Fase 1 portada) | 15/15 verde |
| F2-IT-01 | Sync J-2 nominal: 13 operaciones end-to-end vía canal PowerSync | 13/13 aplicadas, veredictos correctos |
| F2-OT-01 | Offline completo: edición + evidencias sin red → reconexión → sync | Cero pérdida, orden preservado |
| F2-CT-01 | Conflicto simultáneo (supervisor cancela vs técnico completa) | Veredicto server-authoritative exacto |
| F2-CT-02 | Conflictos múltiples (≥5 clientes sobre la misma OT) | Sin duplicados, sin LWW silencioso |
| F2-CT-03 | Conflictos cruzados (estado + evidencia + stock sobre misma OT) | Matriz de conflictos respetada |
| F2-CT-04 | Conflicto de eliminación (tombstone vs edición concurrente) | "Deletes win", tombstone propagado |
| F2-CT-05 | Conflicto de edición (mismo campo, dos clientes offline) | Veredicto ADJUST/REJECT visible al usuario |
| F2-CH-01 | Corte de red a mitad de sync (kill conexión) | Recuperación sin corrupción |
| F2-CH-02 | Reinicio del servidor PowerSync durante sync | Reanudación automática, cero duplicados |
| F2-CH-03 | Pérdida temporal intermitente (flapping 10 ciclos) | Sync converge, sin estados inconsistentes |
| F2-RT-01 | Restauración desde backup + reanudación de sync | Continuidad desde checkpoint |
| F2-LT-01 | Carga: 10 usuarios concurrentes | Métricas registradas |
| F2-LT-02 | Carga: 100 usuarios | Métricas registradas |
| F2-LT-03 | Carga: 1.000 usuarios (simulados) | Métricas registradas |
| F2-LT-04 | Carga: 10.000 usuarios (simulados) — clasificación SU | Métricas + limitaciones declaradas |
| F2-FT-01 | Failover del canal de réplica | RTO medido, cero pérdida confirmada |
| F2-LR-01 | Long running: 2 h de sync continuo con churn de red | Sin fugas (memoria estable ±10%), cero errores no recuperados |

## 6. Métricas obligatorias y formato

Todas en `resultados_f2.csv` con columnas: `caso_id, entorno(A|B), metrica, valor, unidad, p50, p95, p99, clasificacion(DC|SU|PD), evidencia_ref`. Métricas: tiempo de sincronización, latencia (p50/p95/p99), throughput (ops/s), tiempo de recuperación, tiempo de reconexión, CPU, memoria, red (bytes tx/rx).

## 7. Criterios de aceptación (del Master Prompt v1.1)

La Fase 2 solo se declara completa si: (1) todas las pruebas se ejecutaron sobre **ambos** entornos; (2) las métricas son reproducibles (Anexo de Reproducibilidad obligatorio — REGLA ADICIONAL); (3) existe evidencia suficiente para diferenciar objetivamente; (4) la recomendación está respaldada por datos; (5) ADR-014 puede cerrarse sin incertidumbres técnicas relevantes. **Si la evidencia no diferencia objetivamente, N-2 permanece PD y se documenta por qué.**

## 8. Entregables (10, del Master Prompt v1.1)

1. Informe técnico comparativo · 2. Benchmark completo · 3. Resultados brutos · 4. Scripts de medición · 5. Configuración reproducible de ambos entornos · 6. Matriz de decisión oficial puntuada · 7. Riesgos de cada alternativa · 8. TCO comparativo · 9. Recomendación técnica fundamentada · 10. Borrador de ADR-014 definitivo. **Todos se presentan al Fundador antes de cualquier cierre de N-2.**

## 9. Plan de ejecución

- **Carril A (este paquete, sandbox):** especificación, harness adaptado, scripts, plantillas, guías, configuración parametrizable. Entregable para revisión antes de Carril B.
- **Carril B (condicionado, DC-04):** cuenta PowerSync Cloud + Docker self-hosted + credenciales. Ejecución de la batería en ambos entornos → entregables 1–10.
- **N-2 permanece PD** hasta completar ambas fases y emitir ADR-014 definitivo (DC-04).

## 10. Limitaciones conocidas (declaradas por adelantado)

- Escalabilidad 10.000 usuarios: simulada → clasificación SU, nunca DC.
- Cloud: depende de la red real hacia el servicio gestionado; se registrará latencia de red base del entorno de medición y se declarará en el Anexo.
- Self-Hosted: rendimiento depende del hardware del Fundador; se documentará en el Anexo (hardware utilizado).
- Sin Anexo de Reproducibilidad, **ninguna métrica** fundamenta el cierre de N-2 (REGLA ADICIONAL).

---
*Trazabilidad: EXENCIÓN-SPIKE-01 · MASTER PROMPT Spike v1.1 (DC-01) · DECISIÓN DEL FUNDADOR DC-01…DC-05 · Doc 23 (N-2) · Doc 26 (MT-3/MT-4) · SPIKE_S1…S6 (Fase 1).*
