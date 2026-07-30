# DONEFIXER — 27 · Offline & Synchronization Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)
> **Evidencia:** DC para el modelo de sincronización y resolución de conflictos (doc 14 §8, RF-SYNC-*, ADR-011 v1.1, AUD-00 §4 — todos aprobados o en gobierno); **PD-N2: la modalidad de operación de PowerSync (Cloud vs. self-hosted) permanece abierta por decisión del Fundador**; SU para umbrales y tuning.
> **Este documento define el contrato y la arquitectura de sincronización; no escribe código.**

---

## 1. Objetivo
Hacer del trabajo sin conectividad una propiedad confiable del sistema completo — cliente, protocolo, servidor y resolución de conflictos — cumpliendo los RF-SYNC-001…010 aprobados (doc 11) y la prueba de fuego J-2 (doc 16: OT completa en modo avión).

## 2. Alcance
Modelo conceptual, motor de sincronización (PowerSync, decisión revertida AUD-00 D-1), protocolo de push/pull, resolución de conflictos, archivos, seguridad local, observabilidad del sync y casos de borde.

## 3. Exclusiones
Implementación específica de cliente (doc 23 Mobile, framework PD-N1); modalidad de despliegue del motor (PD-N2); diseño físico de la BD local (doc 23/etapa DDL).

## 4. Decisiones confirmadas (DC)

| # | Decisión | Trazabilidad |
|---|---|---|
| SY-1 | **El dispositivo es la fuente de verdad local:** lecturas/escrituras primero en SQLite local (<100 ms p95, RNF-PERF-002) | AUD-00 §4, doc 11 RF-SYNC |
| SY-2 | **Outbox durable en la misma transacción local que el dato** | RF-SYNC-001 |
| SY-3 | **Motor: PowerSync** (decisión revertida con evidencia nueva: tier gratuito, Pro $49/mes, Open Edition FSL, SDKs Apache 2.0 Flutter/RN/Web/.NET, SOC2+HIPAA del vendor ene-2026) — **sujeto a ratificación del Fundador vía N-2** | AUD-00 D-1, fuentes fechadas jul-2026 |
| SY-4 | **La lógica de resolución de conflictos vive en nuestro backend de escrituras** (donde está el valor diferencial), no en el motor | AUD-00 D-1/F-3 |
| SY-5 | Autoridad del backend con lógica local provisional: **toda mutación se re-valida en el servidor al sincronizar** (estado, permisos, stock, SLA, versión) | ADR-011 v1.1 (texto del Fundador) |
| SY-6 | Operaciones idempotentes con `operation_id` UUID; deduplicación en servidor | RF-SYNC-002 |
| SY-7 | Versionado por fila + If-Match; stale-write detectado, no pisado | RF-SYNC-003, AUD-00 §4 |
| SY-8 | **Matriz de resolución por tipo de dato** (§8); conflictos críticos a cola humana; **LWW silencioso prohibido en campos críticos** | doc 14 §8, RF-SYNC-004 |
| SY-9 | Tombstones: "los borrados ganan"; retención PD | RF-SYNC, doc 25 DA-9 |
| SY-10 | Sync por **buckets declarativos por perfil** (el técnico no descarga el tenant) | RF-SYNC-006 |
| SY-11 | Archivos por canal separado: reanudable, hash SHA-256, prioridad metadatos>fotos>video | RF-SYNC-007 |
| SY-12 | Cifrado local SQLCipher + keystore/biometría; wipe remoto al revocar; dispositivo compartido con wipe entre usuarios | RF-SYNC-008/009 |
| SY-13 | Estado de sync siempre visible (pendiente/confirmado/ajustado/rechazado) | RF-SYNC-005, AUD-00 §12 |
| SY-14 | Ordenamiento causal con HLC + timestamp de servidor como referencia final | AUD-00 §4 |
| SY-15 | Motor propio solo como **exit strategy documentada** (si PowerSync depreca o cambia licencia) — patrón conocido, SDKs abiertos | AUD-00 §4 |

## 5. Decisiones pendientes (PD)
- **PD-N2 (bloqueante parcial):** PowerSync **Cloud** vs. **Open Edition self-hosted** vs. híbrido por etapa. Recomendación de auditoría (NO confirmada): Cloud en Fases 0–2, self-hosted evaluado en Etapa B por residency. Este documento se mantiene **agnóstico a la modalidad**: el contrato de sync no cambia entre ambas.
- PD-RETENCIÓN: purga de tombstones y de datos locales.
- PD-N1 (framework móvil): no afecta a este contrato (SDKs equivalentes en Flutter y RN).

## 6. Supuestos (SU)
Latencia de convergencia <60 s con red estable (RNF-SYNC-002); bucket típico de técnico <50 MB sin fotos (calibrar en pilotos); las políticas de background de iOS/Android limitan el sync periódico (restricciones del OS, AUD-00 §3 — el sync ocurre al abrir la app, al ejecutar acciones y en ventanas del OS).

## 7. Arquitectura del pipeline (nivel de componentes)

```
CLIENTE (app nativa / PWA reducida)
 ├── SQLite local (cifrado) — lecturas/escrituras de la UI
 ├── Outbox (misma transacción) — cola durable de operaciones
 ├── Sync SDK (PowerSync) — pull de deltas del bucket, subida de archivos por canal aparte
 └── Upload queue (metadatos>fotos>video, reanudable, hash)

CANAL
 └── PowerSync Service (Cloud o self-hosted — PD-N2)
      └── Lee el WAL de PostgreSQL (logical replication) y materializa buckets por reglas declarativas

SERVIDOR DONEFIXER (autoridad)
 ├── Write API de sync: recibe lotes de operaciones del outbox
 │    ├── Autentica dispositivo + deduplica (operation_id)
 │    ├── Orden causal (HLC + dependencias)
 │    └── RE-VALIDA por operación: permisos (doc 19), máquina de estados (doc 14 §7.2),
 │        versión If-Match, invariantes (stock, SLA) → ACEPTA / AJUSTA / RECHAZA
 ├── Conflict Resolver: matriz por tipo (§8); críticos → cola humana con ambos valores
 ├── Resultado al cliente: confirmado / ajustado (con valor final) / rechazado (con motivo)
 └── Outbox de eventos: todo cambio aceptado emite evento de dominio (doc 30)
```

**Flujo de pull:** el servicio de sync mantiene el estado del bucket por dispositivo; el cliente avanza por cursor (delta). **Flujo de push:** el cliente envía lotes desde su outbox con backoff exponencial + jitter; el servidor procesa en orden causal por entidad.

## 8. Matriz de resolución de conflictos (normativa — doc 14 §8 aprobado)

| Tipo de dato | Estrategia | Quién decide | Ejemplo |
|---|---|---|---|
| Estado de OT, asignación | Servidor autoritativo + máquina de estados; transición inválida → ajuste o rechazo | Sistema + humano si ambiguo | Técnico A completa offline; B canceló la OT → cierre a cola de revisión |
| Campos críticos financieros (costos cerrados, facturas) | Inmutables; correcciones por contra-asiento | Servidor | Nunca sobrescritura |
| Contadores (stock, lecturas de medidor) | **Deltas** (`increment_by`) | Servidor (suma converge) | Dos técnicos consumen 1 uds. offline → stock −2 |
| Evidencias, fotos, firmas, notas | **Aditivas** (conjunto); nunca sobrescribir | — | Ambas fotos persisten |
| Catálogos del tenant (texto descriptivo, mismo autor) | LWW por campo con versión + aviso en UI | Servidor | Descripción de activo editada en dos sesiones del mismo usuario |
| Borrados | Tombstones ("borrados ganan") | Servidor | Edición concurrente de un registro borrado → se descarta la edición, se informa |
| Texto largo colaborativo simultáneo | CRDT (Yjs/Automerge) — **aplastado a Etapa B** | AUD-00 E-7 | Procedimientos coeditados |

## 9. Casos de borde normativos (→ pruebas doc 47)

1. **Dispositivo compartido:** cambio de usuario → wipe del bucket anterior + descarga del nuevo; sin mezcla de datos (RF-SYNC-008).
2. **Revocación con outbox lleno:** se descarta el outbox del usuario revocado y se hace wipe; el servidor rechaza cualquier operación posterior de ese dispositivo/usuario.
3. **Reloj del dispositivo erróneo:** HLC + sello de servidor; la UI muestra "fecha del servidor" en auditoría.
4. **Subida de foto interrumpida al 90%:** reanudación por offset; deduplicación por hash si se reintenta completa.
5. **7 días offline / 200 operaciones:** convergencia completa, sin pérdida, en <60 s una vez estable la red (RNF-SYNC-002/003).
6. **Disco lleno:** protección del outbox (nunca se sacrifica para caché), aviso al usuario, purga de caché no esencial.
7. **Bucket que crece demasiado:** reglas de sync por sitio/rol revisables por el Tenant Admin; límite configurable (RNF-MOB-004).
8. **Actualización de app con cambio de esquema local:** migraciones locales versionadas; sync reanudable tras migración (expand/contract también en cliente).

## 10. Seguridad del sync
Autenticación por dispositivo+usuario (tokens de sync revocables); transporte TLS 1.3; validación de integridad de operaciones (firma del lote); rate limit por dispositivo; registro inmutable de rechazos y resoluciones (RF-AUD); **el sync nunca es vía para saltarse permisos**: cada operación re-valida autorización en el servidor (SY-5).

## 11. Observabilidad del sync (el sync es el producto — AUD-00)
Métricas por dispositivo/tenant: lag de sync, tamaño y edad máxima del outbox, conflictos por tipo y resolución, éxito diario (RNF-SYNC-001 >99.9%), reintentos, bytes por red. Consola de plataforma con lista de dispositivos desfasados (ADR-012 §3.7). Alerta por síntoma: "técnico X lleva 5 días sin sincronizar".

## 12. Alternativas evaluadas (regla Ola 3)

| Alternativa | Estado/fecha | Costo operativo | Estrategia de reemplazo | Veredicto |
|---|---|---|---|---|
| **PowerSync (elegida, sujeta a N-2)** | Maduro; SOC2+HIPAA vendor ene-2026; SDKs abiertos (jul-2026) | Bajo (Cloud) / Medio (self-host) | Exit strategy propia documentada (SY-15); patrón abierto | **Adoptar** |
| Motor propio | — | **Alto** (6–12 meses de ingeniería especializada) | — | Solo exit strategy |
| ElectricSQL | CVE-2026-40906 (SQLi crítica, 2026); long-polling frágil reportado | Medio | — | Descartada |
| Zero (Rocicorp) | Buena reputación de producción (2026) | Medio | Mismo patrón | Fallback documentado |
| WatermelonDB | Mantenida; sync DIY | Alto (todo propio) | — | Fallback si RN |
| Realm/MongoDB Device Sync | **Deprecado sept-2024** | — | — | Descartado (DC) |

## 13. Estrategia de evolución
Fase 1: buckets por sitio/rol, sync bajo demanda + ventanas OS → Fase 2–3: priorización inteligente por contexto (próximas OT primero), pre-descarga predictiva (SU), CRDT colaborativo (E-7) → Etapa C: residency por región (si N-2 self-host lo requiere). Cada cambio con ADR y pruebas de chaos actualizadas.

## 14. Riesgos
| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Pérdida de trabajo de campo | Baja (con SY-1/2) | **Crítico** | Outbox transaccional + chaos tests + RNF-SYNC-004 (objetivo 0, postmortem si ocurre) |
| Dependencia del vendor PowerSync | Media | Alto | SY-15 exit strategy; verificación trimestral de licencia/términos |
| Conflictos mal resueltos erosionan confianza | Media | Alto | Cola humana + visibilidad total (SY-13) + métricas por tipo |
| Costo de red/storage por evidencias | Media | Medio | Compresión, priorización, ciclo de vida (doc 60) |

## 15. Métricas
RNF-SYNC-001…006 (aprobados doc 12) + conflictos/1.000 OTs + edad del outbox más viejo + % resoluciones humanas <48 h.

## 16. Criterios de aceptación
1. Pipeline completo cliente→servidor→cliente con re-validación. ✅ 2. Matriz de conflictos normativa sin LWW silencioso en críticos. ✅ 3. Casos de borde asignados a pruebas. ✅ 4. PD-N2 explícita y documento agnóstico a ella. ✅ 5. Alternativas con costo y reemplazo. ✅

## 17. Referencias cruzadas
Depende de: 14, 11 (RF-SYNC), 12 (RNF-SYNC), 25, 26, ADR-011 v1.1, AUD-00 §4. Alimenta: 23 (mobile), 24 (backend write path), 30 (eventos), 47 (chaos tests), 54/55 (observabilidad), 60 (FinOps N-2).

## 18. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). Arquitectura completa de sync con PowerSync (sujeto a N-2), pipeline con re-validación, matriz de conflictos normativa, 8 casos de borde, observabilidad del sync |
