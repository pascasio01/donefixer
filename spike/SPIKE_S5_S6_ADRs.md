# SPIKE S-5/S-6 — Benchmark, Matriz de Decisión y ADR-013 / ADR-014

| Campo | Valor |
|---|---|
| Documento | SPIKE_S5_S6_ADRs |
| Versión | 1.0 |
| Estado | Entregado — pendiente de revisión y aprobación del Fundador (condición EXENCIÓN-SPIKE-01: N-1 y N-2 solo se cierran con su aprobación tras los resultados) |
| Fecha | 2026-07-30 |

---

## 1. Benchmark obtenido (evidencia dura de la Spike)

| Métrica | Valor medido | Target aprobado | Margen |
|---|---|---|---|
| Latencia sync, lote 13 ops (J-2) | **9.84 ms** | <60 s p95 (RNF-SYNC-002) | ~6.000× |
| Throughput write-path | **2.366 ops/s** (200 ops en 84.5 ms) | 200 ops convergiendo sin pérdida (RNF-SYNC-003) | holgado |
| Captura local de 13 operaciones | 0.17 ms | <100 ms/lectura (RNF-PERF-002) | cumplido |
| Idempotencia de lote completo | 100% duplicate-replayed, 0 efectos duplicados | RF-SYNC | exacto |
| Aislamiento cross-tenant (RLS + FORCE + rol app) | 0 filas leídas, reject en escritura | RNF-SEC-006 | exacto |
| Atomicidad outbox (EV-1) | 222 eventos / 221 operaciones | 1:1 | exacto |
| Tombstones / recovery / stock delta | PASS / PASS / PASS | Doc 14/27 | exacto |
| Unit tests dominio .NET | 15/15 | Doc 14, SY-6 | exacto |

**Conclusión del benchmark:** el riesgo técnico nº 1 del proyecto (AUD-00 R1: "construir el write-path propio de conflictos") queda **desmitificado con evidencia**: es implementable, correcto y sobrado de rendimiento para la dimensión Etapa A (50 tenants, RNF-SCL-001).

## 2. Estado de las decisiones

### 2.1 N-1 (framework móvil) — evidencia: **INSUFICIENTE para cerrar**

| Criterio (Doc 23 §4) | Peso | Evidencia disponible | Brecha |
|---|---|---|---|
| Integración sync/SQLite | 25% | Adaptador MA-1 implementado en ambas; contrato validado contra write-path real | Falta medir SDK PowerSync real en ambos |
| Rendimiento gama media | 20% | Ninguna medible (sin dispositivo) | Toda (guía lista) |
| Capacidades nativas | 15% | Código de cámara/firma/SQLCipher escrito en ambas | Falta validar en hardware |
| Productividad | 15% | Ambas apps implementadas en la Spike (LOC y tiempo registrables al completar) | Falta medición en dispositivo |
| Compartición con web | 10% | **Dato objetivo:** RN comparte TypeScript con la Web App (Doc 22); Flutter requiere Dart (tokens compartibles, lógica no) | Evaluar en ADR |
| Talento/longevidad | 10% | Datos de mercado (documentados en N-1) | Actualizar al decidir |
| Riesgo plataforma | 5% | Licencias revisadas (Flutter BSD, RN MIT, Expo MIT) | — |

**Veredicto de evidencia:** la Spike aporta el adaptador MA-1 validado en ambos frameworks (el criterio de mayor peso queda **destrabado arquitectónicamente**: ambos integran bien el modelo de sync), pero **faltan las métricas de dispositivo** (20% del peso) y la validación nativa (15%). Conforme a la regla del Fundador, **N-1 permanece PD**.

### 2.2 N-2 (estrategia de sincronización) — evidencia: **PARCIAL — decisión dividida**

- ✅ **Decidible con evidencia:** el **write-path propio** (lógica de conflicto en servidor con veredictos) es el componente correcto — medido y verificado (§1). Esto confirma AUD-00 D-1 ("el valor vive en la lógica de conflicto del backend").
- ❌ **No decidible aún:** PowerSync **Cloud vs. self-hosted** (requiere canal real no disponible en este entorno) ni la **confirmación empírica del SDK** en dispositivo.

## 3. ADR propuestos (para aprobación del Fundador)

### ADR-013 — N-1 Framework móvil: **NO EMITIR — permanece PD**

**Recomendación registrada (NO confirmada):** ejecutar la medición en dispositivo (guía `harness/guia_metricas_dispositivo.md`, ~1 semana con ambas apps ya construidas) y entonces emitir ADR-013. La Spike ya redujo la incertidumbre al criterio de rendimiento nativo y al SDK de PowerSync; ambos frameworks pasaron el criterio de mayor peso (integración de sync vía adaptador).
**Dato nuevo de la Spike para la decisión:** la elección de framework **no afecta** al write-path ni al modelo de sync (probado), lo que elimina el mayor riesgo de escoger "mal" el framework: el adaptador MA-1 permite cambiar de framework sin reescribir la lógica de sincronización.

### ADR-014 — N-2 Estrategia de sincronización: **FASE 1 propuesta (para aprobar ahora)**

> **ADR-014 (fase 1) — Write-path de sincronización propio, confirmado con evidencia.**
> **Estado propuesto:** DC (sujeto a aprobación del Fundador).
> **Decisión:** la lógica de sincronización con autoridad en servidor (idempotencia por `operation_id`, HLC, re-validación de dominio, veredictos ACCEPT/ADJUST/REJECT, matriz de conflictos del Doc 14, outbox transaccional) es un **componente definitivo del producto**, implementado en el backend propio — no delegada a ningún motor de réplica.
> **Evidencia:** benchmark §1 de este documento (suite J-2 completa, 15 métricas, 0 FAIL; 15/15 unit tests).
> **Consecuencia:** reduce N-2 a una decisión de **transporte de réplica** (PowerSync Cloud / self-hosted / Zero), no de lógica — el escenario de menor riesgo, con exit strategy preservada (ADR-002).
> **Fase 2 (permanece PD):** elección del canal de réplica tras medición real (plan §5 del Informe S-2/S-3: cuenta Cloud + self-hosted en Docker + suite J-2 en ambos).

## 4. Riesgos residuales

| Riesgo | Nivel | Mitigación |
|---|---|---|
| SDK PowerSync con problemas en el framework elegido | Medio | Medir en fase 2 antes de cerrar N-1 definitivamente (orden: fase 2 de N-2 alimenta ADR-013) |
| Métricas de dispositivo desfavorables a ambos candidatos | Bajo | Kotlin Multiplatform/nativo dual siguen como candidatos documentados (Doc 23 §4) |
| Costo PowerSync Cloud a escala | Bajo | Línea roja FinOps (Doc 62) + exit strategy self-hosted |
| Licencia FSL de PowerSync Open Edition cambia | Bajo | Exit strategy documentada (ADR-002); write-path propio ya confirmado |

## 5. Criterios de aceptación para cerrar N-1 y N-2 (propuestos)

**N-1 se cierra cuando:** (a) métricas de dispositivo de ambas apps registradas en `resultados.csv` según la guía; (b) matriz Doc 23 §4 puntuada con evidencia por criterio; (c) ADR-013 aprobado por el Fundador.
**N-2 se cierra cuando:** (a) suite J-2 ejecutada contra PowerSync Cloud y self-hosted con lag/throughput/buckets medidos; (b) evaluación operativa self-hosted vs. costo Cloud (Doc 62); (c) ADR-014 fase 2 aprobado por el Fundador.

## 6. Plan de transición hacia producción

1. **Aprobación del Fundador** de este informe y de ADR-014 fase 1 (si procede).
2. **Fase 2 de N-2** (canal PowerSync real) — 1 semana, requiere cuenta Cloud y Docker (entorno del Fundador o VM).
3. **Medición N-1 en dispositivo** — 1 semana con las apps ya construidas.
4. **ADR-013 + ADR-014 fase 2** → N-1 y N-2 cerradas.
5. El código de la Spike se **archiva como investigación** (no se reutiliza en producción salvo ADR); el backend de producción se escribe nuevo conforme a los docs 24/43 con el write-path ya diseñado y ahora validado.
6. **Doc 70 (PRR):** con N-1/N-2 cerradas y PD-CLOUD resuelta (N-7), la Fase 1 puede presentarse al gate.

---

*Registro de cambios — v1.0 (2026-07-30): S-5 benchmark + S-6 ADR-013 (no emitir, PD) / ADR-014 fase 1 (propuesta DC) / plan de transición.*
