# SPIKE S-2/S-3 — Informe Técnico: Backend Mínimo y Evaluación de Sincronización

| Campo | Valor |
|---|---|
| Documento | SPIKE_S2_S3_Informe_Tecnico |
| Versión | 1.0 |
| Estado | Entregado — bajo EXENCIÓN-SPIKE-01; pendiente de revisión del Fundador |
| Evidencia | `spike/harness/resultados.csv` (15 métricas) + suite reproducible (`spike/harness/test_j2_e2e.py`) + 15 unit tests .NET (`spike/tests/`) |
| Fecha de ejecución | 2026-07-30 |

> **Código de investigación técnica.** Nada de lo aquí construido es código de producción ni se reutilizará salvo ADR (condición EXENCIÓN-SPIKE-01).

---

## 1. Qué se construyó (S-2)

| Componente | Tecnología | Fidelidad a la Constitución |
|---|---|---|
| Backend mínimo (.NET 8 minimal API) | `spike/backend/` | Estructura de capas Doc 24: dominio puro (`Domain/WorkOrderStateMachine.cs`, `Hlc`) sin infraestructura; aplicación (`Application/SyncWritePath.cs`); infraestructura (`Infrastructure/Database.cs`) |
| PostgreSQL 16.2 real | pgserver (binarios oficiales) | RLS por tenant con **FORCE ROW LEVEL SECURITY + rol de aplicación no privilegiado** (Doc 26 MT-3/MT-4: `set_config` transaccional) |
| Esquema mínimo J-2 | `spike/harness/schema.sql` | tenants, users, work_orders (state, version, deleted_at), wo_items, evidences (sha256, hlc), stock_movements (delta, operation_id UNIQUE), sync_operations (veredictos), outbox_events (EV-1) |
| Write-path de sync | .NET + espejo Python para medición | SY-4/5/6/8/9/10: idempotencia por `operation_id`, HLC, re-validación de autoridad, veredictos ACCEPT/ADJUST/REJECT, tombstones |
| Harness de medición | `spike/harness/` | Suite E2E reproducible con los 7 pasos de J-2 y las 8 suites obligatorias del Master Prompt |

**Compilación:** backend .NET compila limpio (0 errores). **Unit tests:** 15/15 PASS — máquina de estados canónica completa y HLC incluyendo el caso normativo de reloj atrasado.

## 2. Resultados medidos (S-3 parcial: write-path y modelo de sincronización)

### 2.1 Flujo J-2 canónico end-to-end — PASS

El escenario ejecutado fue el más duro del Journey: el técnico completa 13 operaciones offline (4 checklist + nota + 3 fotos + firma + 2 consumos delta + 2 transiciones hasta Completada) **mientras el supervisor cancela la OT en el servidor**. Veredictos obtenidos al sincronizar:

| Operaciones | Veredicto | Razón (visible al usuario) | Conforme a |
|---|---|---|---|
| 5 (checklist, nota) | ACCEPT | — | SY-9 |
| 4 evidencias (fotos+firma) | REJECT | `wo-Cancelada-immutable-evidence` | RF-WO-003 + matriz Doc 14 |
| 2 consumos stock | REJECT | `wo-Cancelada-no-consumption` | Matriz Doc 14 (deltas solo en OT viva) |
| 2 transiciones (→EnProgreso, →Completada) | REJECT | `server-state-Cancelada-authoritative` | **Servidor autoritativo en estado OT — jamás LWW silencioso** (Doc 14; RNF-SYNC-005) |

**Conclusión de comportamiento:** la matriz de conflictos funciona exactamente como fue aprobada. Ningún dato del técnico se perdió: todos los rechazos quedaron registrados en `sync_operations` con razón — la base de la bandeja "Requiere tu atención" del Doc 40 §9.

### 2.2 Suites obligatorias — resultados

| Suite | Resultado | Métrica clave | Target aprobado |
|---|---|---|---|
| Offline (J-2 completo) | ✅ PASS | 13/13 operaciones capturadas en outbox local | Doc 16 |
| Idempotencia (SY-5) | ✅ PASS | reenvío del lote completo → 100% `duplicate-replayed`, cero efectos duplicados | RF-SYNC |
| Stock delta idempotente | ✅ PASS | 2 movimientos tras doble sync (no 4) | Doc 14 (nunca `set`) |
| Aislamiento multi-tenant (RNF-SEC-006) | ✅ PASS | lectura cruzada Tenant B→A: **0 filas**; escritura cruzada: **reject** (wo-not-found por RLS) | Doc 26 |
| Tombstones ("borrados ganan") | ✅ PASS | edición post-borrado rechazada | Doc 14 |
| Recovery (interrupción a mitad de lote) | ✅ PASS | reintento con lote completo: primera op `duplicate-replayed`, resto procesadas sin duplicar | Doc 27 |
| Performance / throughput | ✅ PASS | **200 ops en 84.5 ms — 2.366 ops/s** | RNF-SYNC-002 (<60 s) con 3 órdenes de magnitud de margen |
| Outbox transaccional (EV-1) | ✅ PASS | 222 eventos / 221 operaciones (1:1 atomicidad; +1 por evento de seed) | Doc 30 |
| Unit tests dominio | ✅ 15/15 PASS | transiciones ilegales rechazadas; HLC con reloj atrasado correcto | Doc 14, SY-6 |

### 2.3 Hallazgo de ingeniería relevante (documentado para producción)

La primera corrida mostró "aislamiento multi-tenant FAIL": el rol **superuser** de PostgreSQL *bypasea* RLS. La corrección — rol de aplicación sin privilegios + `FORCE ROW LEVEL SECURITY` — es exactamente la defensa en profundidad del Doc 26 MT-3, y la Spike **la validó empíricamente**: con el rol correcto, el ataque cross-tenant devuelve 0 filas y reject. **Recomendación registrada para ADR futuro de producción:** la app nunca conecta con el rol owner; CI debe incluir este ataque (ya está en RNF-SEC-006 y ahora hay evidencia de por qué).

## 3. Evaluación N-2 (estrategia de sincronización) — evidencia y límites

### 3.1 Evidencia obtenida

1. **El modelo de sincronización aprobado (outbox local + write-path con re-validación + veredictos) es viable y performante** sobre PostgreSQL 16 real: throughput de ~2.400 ops/s por conexión en hardware modesto de sandbox, con la lógica de conflicto completa en el servidor (que es donde vive el valor, AUD-00 D-1).
2. **El write-path es agnóstico del transporte de réplica**: PowerSync, Zero o réplica propia solo mueven datos; la decisión de conflicto quedó demostrada como independiente del motor (compatible con el adaptador MA-1 y la exit strategy de ADR-002).
3. **RLS multi-tenant verificada en el write-path** — el requisito más delicado de PowerSync self-hosted (compartir el mismo PostgreSQL con políticas).

### 3.2 Evidencia NO obtenida (declarado; afecta el cierre de N-2)

| Evidencia faltante | Razón | Consecuencia |
|---|---|---|
| PowerSync self-hosted real (Docker) | Sin Docker ni red a registries en este entorno (verificado) | No hay medición del canal de réplica PowerSync (lag, buckets, SDK móvil) |
| PowerSync Cloud | Requiere cuenta (gratuita) que solo el Fundador puede crear | Sin comparativa Cloud vs. self-hosted medida |
| SDK PowerSync en Flutter/RN | Sin emulador/dispositivo | La integración móvil del motor de sync queda sin medir |

### 3.3 Conclusión S-3 (honesta)

La Spike produjo evidencia suficiente para afirmar que **la arquitectura de sincronización (write-path + conflictos + RLS) es correcta e independiente del motor** — pero **NO produjo evidencia suficiente para cerrar N-2 (Cloud vs. self-hosted)**: esa decisión depende de medir el canal PowerSync real (lag de réplica, buckets, operación self-hosted, costo a 50 tenants) que este entorno no puede ejecutar. Conforme a la regla del Fundador ("si la evidencia resulta insuficiente, ambas decisiones permanecerán abiertas"), **N-2 permanece PD** con un plan de cierre concreto (§5).

## 4. Recomendación técnica parcial

- **ADR-014 (N-2): NO emitir todavía.** En su lugar, cerrar la mitad decidible: ver ADR-014 propuesto en `SPIKE_S5_S6_ADRs.md` como **"ADR-014 fase 1"**: confirma el write-path propio como componente definitivo (era el riesgo nº 1) y deja la elección Cloud/self-hosted como "ADR-014 fase 2" condicionada a la medición del canal PowerSync real (criterios ya definidos en Doc 27 y N-2).
- El plan de cierre de N-2 requiere: (a) cuenta PowerSync Cloud del Fundador (gratuita); (b) un entorno con Docker (local del Fundador o VM cloud de prueba) para self-hosted; (c) ~1 semana de medición con la misma suite J-2.

## 5. Plan de cierre de N-2 (inputs para el Fundador)

| Paso | Acción | Quién | Esfuerzo |
|---|---|---|---|
| 1 | Crear cuenta PowerSync Cloud (free tier) + instancia de prueba | Fundador | 30 min |
| 2 | Levantar PowerSync Open Edition (Docker) contra PostgreSQL | Fundador/VM | 2 h |
| 3 | Ejecutar la suite J-2 contra ambos modos (lag, throughput, buckets por perfil SY-12) | Conjunto | 2–3 días |
| 4 | Evaluar operación self-hosted (backups, upgrades, monitoreo) vs. Cloud ($49/mes Pro) con Doc 62 | Conjunto | 1 día |
| 5 | ADR-014 fase 2 con la evidencia | Equipo → Fundador | 1 día |

---

*Registro de cambios — v1.0 (2026-07-30): S-2 completo (backend + evidencia), S-3 parcial con N-2 declaradamente insuficiente → permanece PD.*
