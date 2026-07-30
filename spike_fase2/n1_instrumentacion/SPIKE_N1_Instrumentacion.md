# N-1 — Paquete de Instrumentación de Medición en Dispositivo Real (DC-10)

**Versión:** 1.0 · **Fecha:** 2026-07-30 · **Estado:** Preparación autorizada por DC-10 — no modifica arquitectura, no es código de producción, no altera la comparativa N-2.
**Objetivo:** dejar lista TODA la instrumentación, documentación y procedimiento para que la evaluación N-1 (Flutter vs React Native + Expo) se ejecute **inmediatamente después de completar N-2**, en dispositivos reales.
**Marco:** matriz Doc 23 §4 (exclusiva de N-1, DC-02) — sync/SQLite 25%, rendimiento 20%, capacidades nativas 15%, productividad 15%, web/código 10%, talento 10%, riesgo 5%. Cierre vía **ADR-013** con aprobación del Fundador.

---

## 1. Estado de las apps candidatas (ya existen de la Fase 1)

| App | Ruta | Contenido actual |
|---|---|---|
| Flutter | `spike/mobile_flutter/` | `lib/sync/outbox.dart` (outbox local en la misma transacción SQLite, SY-4), `lib/sync/sync_adapter.dart` (MA-1: `SyncAdapter` + `DirectWritePathAdapter` + stub `PowerSyncAdapter`), `newOp` con UUIDv7 |
| RN + Expo | `spike/mobile_rn/` | `src/sync/outbox.ts` (mismo contrato, UUIDv7 propio) |

**Trabajo de instrumentación pendiente (este paquete):** pantallas mínimas J-2 idénticas en ambas, logger de métricas exportable, y guion de medición. Todo con el contrato de operaciones ya validado contra el write-path (Fase 1, 15/15 PASS).

## 2. Instrumentación obligatoria (idéntica en ambas apps)

### 2.1 Logger de métricas (`MetricsLogger`)
Contrato único — mismo CSV de salida en ambas:

```
timestamp_ms, evento, detalle, valor, unidad
```

Eventos canónicos: `cold_start_start`, `first_interactive`, `wo_open`, `j2_offline_start`, `j2_step` (con nombre de paso), `airplane_off`, `sync_first_op_sent`, `sync_last_verdict`, `sync_verdict` (por operación: verdict + reason), `mem_rss_mb`, `export_done`. Botón "Exportar log" → archivo CSV compartible. **Sin este logger la medición no es reproducible y la métrica se clasifica SU.**

### 2.2 Pantallas mínimas J-2 (mismo flujo, mismo copy)
1. Login (usuario de la Spike) → 2. Lista con 1 OT asignada → 3. Detalle OT: checklist (4 ítems), nota, adjuntar 3 fotos, firma, consumir 2 repuestos, botón "Cierre provisional" → 4. Bandeja "Requiere tu atención" (veredictos rechazados/ajustados con razón en lenguaje claro, SY-9) → 5. Botón "Exportar log".

### 2.3 Outbox + adapter (ya implementados)
Reutilizar tal cual: `executeLocalWithOutbox` (misma transacción) + `SyncAdapter` (MA-1). La decisión N-1 **no afecta** al write-path ni al modelo de sync (hallazgo DC de la Fase 1).

## 3. Procedimiento de medición (dispositivo real)

Prerequisitos: 1 dispositivo Android físico de gama media (el MISMO para ambas apps — recomendado: 4–6 GB RAM, Android 12+), ADB, backend Spike accesible por Wi-Fi local, Battery Historian (opcional pero recomendado).

**Secuencia (idéntica por app, orden: Flutter primero, RN después; mismo día, misma red):**
1. Build release (prohibido comparar debug).
2. Instalar, matar proceso, medir **arranque en frío ×3** (logcat `Displayed` / logger propio).
3. Guion J-2 modo avión (Guía §2, pasos 1–6).
4. `adb shell dumpsys meminfo` en reposo y tras J-2; `adb shell top` durante sync.
5. Tamaño del APK; `cloc` del código; dependencias nativas en pubspec/package.json.
6. Batería: 2 h de uso mixto J-2 + sync periódica (Battery Historian; sin wakelocks, RNF-MOB-003).
7. Exportar CSV del logger → anexar a resultados.

Todas las cifras van a `RESULTADOS_N1.csv` (columnas: `metrica, flutter, rn, unidad, clasificacion, evidencia`) y al **Anexo de Reproducibilidad N-1** (misma plantilla que Fase 2, REGLA ADICIONAL del Fundador aplicada por analogía: sin anexo, la métrica no fundamenta ADR-013).

## 4. Puntuación de la matriz Doc 23 §4

| Criterio | Peso | Evidencia que lo alimenta |
|---|---|---|
| Integración sync/SQLite | 25% | Fase 1 (outbox + adapter ya portados a ambos) + comportamiento J-2 en dispositivo |
| Rendimiento gama media | 20% | arranque, apertura OT, jank, memoria, CPU, batería |
| Capacidades nativas | 15% | cámara/firma/GPS en J-2; dependencias nativas directas |
| Productividad | 15% | horas de implementación registradas, LOC, hot-reload, depuración |
| Compartición código/web | 10% | análisis documentado de la porción compartible |
| Talento/longevidad | 10% | análisis documentado (con fuentes y fecha — SU, no DC) |
| Riesgo de plataforma | 5% | análisis documentado |

Regla de decisión (análoga a N-2): cada nota 1–5 exige evidencia + métrica + justificación + referencia. ADR-013 se entrega como **borrador**; el cierre de N-1 es decisión expresa del Fundador.

## 5. Entregables del paquete (este Carril de preparación)

| # | Entregable | Estado |
|---|---|---|
| 1 | Este documento (especificación de instrumentación) | ✅ |
| 2 | `INSTRUMENTACION/MetricsLogger.dart` + `MetricsLogger.ts` (contrato único) | ✅ |
| 3 | `INSTRUMENTACION/RESULTADOS_N1.csv` (plantilla) + `ANEXO_Reproducibilidad_N1.md` | ✅ |
| 4 | Guía de medición en dispositivo (Fase 1, `spike/harness/guia_metricas_dispositivo.md`) — referenciada, sin cambios | ✅ |
| 5 | Checklist de ejecución día-de-medición (§3) | ✅ |

**Pendiente (requiere dispositivo físico, externo al sandbox):** implementar las pantallas J-2 finales en ambas apps (el sync core ya está) y ejecutar §3. Estimación: 1–2 días por app + 1 día de medición comparativa.

## 6. Trazabilidad y límites

EXENCIÓN-SPIKE-01 (código de investigación técnica) · DC-10 (alcance y prioridad) · DC-02 (matriz Doc 23 §4 exclusiva de N-1) · Doc 23 §4 (ponderación) · MA-1/MA-8 (Doc 23) · SY-4/SY-5/SY-9 (Doc 22) · RNF-PERF-004, RNF-MOB-003, RNF-SYNC-002. **No se ejecuta medición N-1 hasta completar N-2** (DC-10: "inmediatamente después").
