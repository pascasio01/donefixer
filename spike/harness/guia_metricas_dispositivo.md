# Guía de Medición en Dispositivo Real — Spike N-1 (EXENCIÓN-SPIKE-01)

> Las métricas de dispositivo (arranque, memoria, CPU, batería, tamaño de binario) **no pueden medirse en el entorno de desarrollo de la Spike** (sin emulador/hardware). Esta guía permite ejecutarlas de forma idéntica en ambas candidatas para una comparativa justa (ponderación Doc 23 §4: rendimiento 20%, productividad 15%).

## 0. Preparación común

| Paso | Flutter | RN + Expo |
|---|---|---|
| Build release | `flutter build apk --release` | `npx expo run:android --variant release` |
| Dispositivo | Android gama media física (mismo para ambas) | igual |
| Backend | Backend mínimo de la Spike corriendo accesible por red local | igual |

## 1. Métricas a registrar (mismo formato para ambas — registrar en `resultados.csv`)

| Métrica | Cómo medirla | Target de referencia |
|---|---|---|
| Arranque en frío a pantalla útil | 3 mediciones con app matada; promedio | ≤2 s (RNF-PERF-004 ref.) |
| Apertura de OT (datos locales) | Tap en OT → detalle interactivo | <1 s (RNF-PERF-004) |
| Jank en scroll de checklist | `flutter: DevTools performance overlay` / `RN: Perf Monitor` | sin drops sostenidos |
| Memoria RSS en reposo / tras J-2 | `adb shell dumpsys meminfo <pkg>` | registrar |
| CPU durante sync de 200 ops | `adb shell top` muestreado | registrar |
| Batería | Battery Historian (2 h de uso mixto J-2 + sync periódica) | sin wakelocks (RNF-MOB-003) |
| Tamaño del binario release | `ls -la` del APK | registrar |
| Convergencia sync 200 ops | log de la app: primera op enviada → último veredicto | <60 s p95 (RNF-SYNC-002) |
| Tiempo de implementación del J-2 | horas registradas por el implementador | registrar |
| LOC (sin contar tests) | `cloc lib/ · cloc src/ app/` | registrar |
| Dependencias nativas directas | count en pubspec/package.json | registrar |

## 2. Guion J-2 idéntico para ambas (modo avión literal)

1. Login, abrir OT asignada (con red).
2. **Modo avión ON.**
3. Checklist completo (4 ítems) → nota → 3 fotos → firma → consumir 2 repuestos → **cierre provisional**.
4. (Coordinado) Supervisor cancela la OT en el backend.
5. **Modo avión OFF** → sync automática.
6. Verificar: veredictos visibles por operación; bandeja "Requiere tu atención" con las 8 operaciones rechazadas esperadas (evidencias/consumos/transiciones sobre OT cancelada); razones en lenguaje claro.
7. Exportar log de métricas (botón en la app) → adjuntar a `resultados.csv`.

## 3. Regla de comparabilidad

Misma red, mismo dispositivo, mismo backend, mismo guion, mismo formato de registro. Cualquier desviación se anota en la columna `target` como nota. **Prohibido comparar builds debug.**
