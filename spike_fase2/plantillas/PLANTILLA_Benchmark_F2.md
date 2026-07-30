# Plantilla — Benchmark completo F2 (Entregable 2)

**Entorno:** A (Cloud) / B (Self-Hosted) · **Fecha:** ____ · **Ejecutor:** ____ · **Anexo de Reproducibilidad:** ☐ adjunto (obligatorio)

## 1. Rendimiento (MDN2-3, 15%)

| Métrica | A | B | Δ% | Clasif | Evidencia (ref. prueba/archivo) |
|---|---|---|---|---|---|
| Tiempo sync 13 ops J-2 (ms) | | | | DC | F2-IT-01 |
| Latencia canal p50 / p95 / p99 (ms) | | | | DC | medicion.py latencia |
| Throughput 10 / 100 / 1.000 u (ops/s) | | | | DC | F2-LT-01/02/03 |
| Throughput 10.000 u simulados (ops/s) | | | | SU | F2-LT-04 |
| Tiempo de recuperación (s) | | | | DC | F2-RT-01 |
| Tiempo de reconexión p50/p95 (s) | | | | DC | F2-CH-01/03 |
| CPU servicio (prom/pico %) | | | | DC/SU | F2-LR-01 |
| Memoria (prom/pico MB) | | | | DC/SU | F2-LR-01 |
| Red (MB tx/rx por 1.000 ops) | | | | DC/SU | medicion.py recursos |

## 2. Confiabilidad (MDN2-1, 30%)

| Prueba | A | B | Evidencia |
|---|---|---|---|
| Idempotencia (reenvío 13/13) | | | F2-IT-01 |
| Veredictos de conflicto exactos (CT-01…05) | | | F2-CT-* |
| Corte de red a mitad de sync: 0 duplicados | | | F2-CH-01 |
| Reinicio del servidor: reanudación | | | F2-CH-02 |
| Flapping 10 ciclos: convergencia | | | F2-CH-03 |
| Long running 2 h: memoria estable ±10% | | | F2-LR-01 |

## 3. Operación (MDN2-2, 20%)

| Aspecto | A (Cloud) | B (Self-Hosted) | Evidencia |
|---|---|---|---|
| Instalación (tiempo, pasos) | | | guía + log |
| Configuración inicial | | | |
| Actualizaciones de versión | | | |
| Monitoreo incluido | | | |
| Logs (acceso, retención) | | | |
| Backups / restauración | | | F2-RT-01 |
| Mantenimiento recurrente (h/mes est.) | | | |
| Coste operativo (h-persona) | | | TCO |

## 4. Seguridad (MDN2-4, 15%)

| Aspecto | A | B | Evidencia |
|---|---|---|---|
| Gestión de credenciales | | | |
| TLS (extremo a extremo) | | | |
| Rotación de secretos | | | |
| Auditoría disponible | | | |
| Superficie de ataque | | | |
| Aislamiento entre tenants | | | F2-IT-01 RLS |

## 5. Escalabilidad (MDN2-6, 5%) y Riesgo (MDN2-7, 5%)

| Carga | A | B | Clasif |
|---|---|---|---|
| 10 / 100 / 1.000 u | | | DC |
| 10.000 u (simulados) | | | SU |
