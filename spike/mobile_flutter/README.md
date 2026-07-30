# Spike App Flutter — J-2 (código de investigación, EXENCIÓN-SPIKE-01)

App candidata para la evaluación N-1. Implementa **exactamente** el flujo J-2 canónico con instrumentación de métricas.

## Qué contiene

- `lib/main.dart` — shell: lista de OT asignadas + banner de estado de sync persistente (Doc 40 §9: `color.sync.*`)
- `lib/wo_detail.dart` — ejecución offline: checklist, nota, fotos, firma, consumos, cierre provisional
- `lib/sync/outbox.dart` — outbox local en la **misma transacción SQLite** que el cambio (SY-4): `operation_id` UUIDv7 + HLC + payload
- `lib/sync/hlc.dart` — Hybrid Logical Clock (SY-6) con persistencia en `shared_preferences`
- `lib/sync/sync_adapter.dart` — **adaptador único de sync (MA-1)**: interfaz `SyncAdapter` con dos implementaciones previstas: `PowerSyncAdapter` (cuando N-2 lo habilite) y `DirectWritePathAdapter` (usado en la Spike: POST /sync/operations del backend mínimo)
- `lib/sync/verdicts.dart` — procesamiento de ACCEPT/ADJUST/REJECT → estados visuales provisional/confirmado/conflicto + bandeja "Requiere tu atención" (SY-9, Doc 40 §9)
- `lib/db.dart` — SQLite + SQLCipher (`sqlcipher_flutter_libs`), esquema réplica limitado al bucket del técnico (SY-12)
- `lib/metrics.dart` — instrumentación: timestamps por operación, latencias, log para `harness/resultados.csv`

## Cómo medir (en dispositivo real — fuera de este entorno)

1. `flutter pub get` y ejecutar en Android gama media física.
2. Seguir `../../harness/guia_metricas_dispositivo.md`: arranque en frío ×3, memoria, CPU, batería (Battery Historian), tamaño APK release.
3. Ejecutar el guion J-2 en modo avión literal y exportar el log de métricas (botón "Exportar métricas" en la app).

## Estado de la Spike

Código completo del flujo J-2 contra `DirectWritePathAdapter`. `PowerSyncAdapter` queda como stub documentado hasta la fase 2 de N-2 (cuenta Cloud / self-hosted).
