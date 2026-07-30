# SPIKE F2B — Control de Precondiciones (documento de control operativo, DC-08)

**Versión:** 1.0 · **Fecha:** 2026-07-30 · **Norma:** Master Prompt Spike v1.2 (DC-06)
**Regla:** ninguna comparación entre alternativas mientras las precondiciones no estén completas (DC-07). Este documento se mantiene sincronizado con el ADI y el Índice Maestro.

## 1. Checklist de precondiciones (obligatorio antes de ejecutar la batería)

| # | Precondición | Verificación (cómo) | Estado | Evidencia |
|---|---|---|---|---|
| P-1 | PowerSync Cloud operativo | `curl -H "Authorization: Bearer $PS_TOKEN" $PS_ENDPOINT/write-checkpoint2` responde JSON | ❌ Pendiente (habilitación externa, DC-09) | — |
| P-2 | PowerSync Self-Hosted operativo | `curl $PS_ENDPOINT/probe/liveness` responde OK | ❌ Pendiente (Docker en máquina del Fundador) | — |
| P-3 | PostgreSQL idéntico en ambos | Misma versión (`SELECT version()`), mismo `schema.sql` aplicado, hash de DDL registrado | ✅ Listo para verificar (schema y seed J-2 validados en CONTROL) | batería CONTROL 6/6 PASS (2026-07-30) |
| P-4 | Backend/write-path idéntico | Mismo harness `harness_f2/` sin modificaciones; hash de archivos | ✅ Validado | `resultados_f2.csv` (CONTROL) |
| P-5 | Dataset idéntico | Seed J-2 aplicado en ambos; conteo de filas por tabla registrado | ⏳ Se verifica al levantar entornos | — |
| P-6 | Variables de entorno configuradas | `entorno_a_cloud.env` y `entorno_b_selfhosted.env` completos (endpoint + token, sin secretos en docs) | ⏳ Plantillas listas; faltan valores reales | — |
| P-7 | Versiones registradas | Servicio Cloud (dashboard) e imagen self-hosted (tag exacto) anotadas | ⏳ Al levantar entornos | — |
| P-8 | Anexo de Reproducibilidad iniciado | Plantilla copiada a `SPIKE_F2B_Anexo_Reproducibilidad.md` con secciones 1–3 abiertas | ✅ Plantilla disponible | `plantillas/PLANTILLA_Anexo_Reproducibilidad.md` |

## 2. Protocolo de ejecución (una vez P-1…P-8 en ✅)

1. Verificación cruzada de precondiciones (este documento, firmado con fecha).
2. Batería idéntica y en el mismo orden sobre A y B: `test_j2_f2.py` → `medicion.py latencia` → chaos → carga (10/100/1.000/10.000 SU) → recovery → failover → long-running.
3. Registro continuo: cada métrica con fecha/hora UTC, hardware, SO, versiones, script, datos brutos y logs (Master Prompt v1.2 §REPRODUCIBILIDAD).
4. Entregables 1–10 del Master Prompt v1.2, incluido borrador de ADR-014. **No se emite decisión definitiva; el cierre de N-2 requiere aprobación expresa del Fundador.**

## 3. Historial de estado

| Fecha | Evento |
|---|---|
| 2026-07-30 | Carril A completado (DC-03). Precondiciones verificadas: NO CUMPLIDAS → ejecución detenida conforme al Master Prompt v1.2; detención confirmada como mecanismo de gobernanza, no retraso (DC-07). |
