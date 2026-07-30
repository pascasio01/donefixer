# Spike App React Native + Expo — J-2 (código de investigación, EXENCIÓN-SPIKE-01)

Segunda candidata N-1. Mismo flujo J-2, misma instrumentación, mismo contrato de adaptador — para que la comparativa con Flutter sea sobre **el mismo trabajo**.

## Estructura

- `app/index.tsx` — lista de OT asignadas + banner persistente de estado de sync (Doc 40 §9)
- `app/wo/[id].tsx` — ejecución offline J-2 completa
- `src/sync/outbox.ts` — outbox local en la misma transacción SQLite (SY-4), `operation_id` UUIDv7 + HLC
- `src/sync/hlc.ts` — Hybrid Logical Clock persistido (AsyncStorage)
- `src/sync/syncAdapter.ts` — interfaz `SyncAdapter` (MA-1): `DirectWritePathAdapter` (Spike) + `PowerSyncAdapter` (stub fase 2 N-2)
- `src/sync/verdicts.ts` — ACCEPT/ADJUST/REJECT → UI provisional/confirmado/conflicto + bandeja de atención
- `src/db.ts` — `expo-sqlite` + SQLCipher, bucket del técnico (SY-12)
- `src/metrics.ts` — instrumentación exportable a `harness/resultados.csv`

## Medición en dispositivo

1. `npx expo prebuild && npx expo run:android --variant release` en Android gama media física.
2. Guía: `../../harness/guia_metricas_dispositivo.md` (mismos pasos que Flutter para comparabilidad).
3. Guion J-2 en modo avión literal; exportar log de métricas.

## Comparabilidad (Doc 23 §4 — criterio "productividad", peso 15%)

Ambas apps implementan el mismo J-2. La Spike registrará: tiempo de implementación, LOC, complejidad, número de dependencias nativas directas y % de lógica compartible con web (RN comparte TypeScript con la Web App — dato relevante del criterio "compartición", peso 10%).
