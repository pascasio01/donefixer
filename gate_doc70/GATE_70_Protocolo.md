# GATE 70 — Protocolo de la Auditoría Production Readiness (Documento 70)

**Versión:** 1.0 · **Fecha:** 2026-07-30 · **Estado:** Preparado para ejecución (DC-12) — **NO es la ejecución del Gate, NO es auditoría parcial, NO emite veredicto oficial.**
**Norma:** MASTER PROMPT — Production Readiness Gate Enterprise v1.0, adoptado como estándar normativo oficial del Documento 70 (**DC-11**).
**Ámbito:** este protocolo operacionaliza el Master Prompt sin redefinir criterios. La auditoría final solo puede iniciarse cuando la REGLA DE EJECUCIÓN (DC-12) se cumpla: N-1, N-2, PD-CLOUD, PD-IA-1 y PD-4 cerradas, con evidencia reproducible en todas las decisiones bloqueantes.

## 1. Mapeo norma → corpus canónico (fuente de evidencia por sección)

| Sección del Gate | Documentos fuente | Verificación principal |
|---|---|---|
| Gobernanza | Doc 00 (Constitución), ADI, REGISTRY_Canonical_Identifiers, VERIFICACION_INTEGRIDAD_DOCUMENTAL, registros DC/SU/PD (ADI §4–5), EXENCIÓN-SPIKE-01 (ADI §6) | script `verificacion_gate70.py` V-1…V-8 + revisión manual |
| Decisiones pendientes | ADI §4 (PD abiertas: N-1…N-10, PD-2…PD-CLOUD) | automático: toda PD bloqueante abierta → condición de NO GO |
| Arquitectura (14 dominios) | Docs 21 (solución), 22 (web), 23 (mobile), 24 (API), 25 (eventos), 26 (multi-tenancy/RLS), 27 (offline/sync), 28 (PostgreSQL), 29 (seguridad), 30 (observabilidad), 31 (FinOps), 32/33 (IA) | consistencia cruzada + trazabilidad RF/RNF/ADR |
| Seguridad | Doc 60 (STRIDE, SBOM, rotación ≤90 d), Doc 26 (RLS/MT-3/MT-4), Doc 29 | checklist manual + evidencia de spike (hallazgo RLS/superuser) |
| Calidad | Doc 47 (QG-1…QG-4, 12 capas), Doc 40 (WCAG), Doc 54 (DR/backup-restore) | manual + automático de gates definidos |
| Operación | Doc 54 (SLO/SLI/error budget, RB-01…08, runbooks, postmortem), Doc 62 (FinOps: alertas, capacity, ciclo de vida) | manual |
| Legal | Docs 03/12 (privacidad/retención), Doc 60 (cumplimiento), PD-RETENCIÓN (abierta — informativa) | manual; marca/residencia = criterios a validar |
| Reproducibilidad | Spike Fase 1 (S-2/S-3 informe, resultados.csv), Fase 2 (Anexo obligatorio), N-1 (Anexo N-1) | automático: toda decisión crítica con anexo |
| Mobile / Sync / Offline | Doc 23 + evidencia spike (Fase 1: 15/15 métricas; Fase 2B pendiente), N-1 instrumentación | evidencia de spikes, no documentos |

## 2. Flujo de la auditoría final (cuando proceda)

1. **Paso 0 — Regla de ejecución (DC-12):** verificar cierre formal de N-1, N-2, PD-CLOUD, PD-IA-1, PD-4. Si alguna abierta → **detener, veredicto NO GO** (causa: PD bloqueante; el Master Prompt lo manda).
2. **Paso 1 — Verificación automática:** `verificacion_gate70.py` sobre el corpus (integridad, PDs, IDs, trazabilidad, reproducibilidad registrada).
3. **Paso 2 — Evaluación por áreas:** comité evalúa las 12 áreas con la Matriz de Cumplimiento (cada celda: Estado, Evidencia, Referencia documental, Riesgo residual, Recomendación).
4. **Paso 3 — Riesgos residuales:** actualización del registro.
5. **Paso 4 — Veredicto:** exactamente uno de GO / GO WITH CONDITIONS / NO GO en el formato de `GATE_70_Veredicto.md`. GO WITH CONDITIONS: cada condición con responsable, fecha objetivo, riesgo — y **ninguna condición puede tocar integridad de datos, aislamiento de tenants, seguridad, sync ni prohibiciones de IA** (Doc 70, Ola 4). NO GO: causa, impacto, evidencia, acción requerida.
6. **Paso 5 — Aprobación del Fundador:** el veredicto solo es oficial tras su firma. El comité emite; el Fundador autoriza (Constitución, regla 6).

## 3. Estados del expediente

- **Preparado para ejecución** ← estado actual (2026-07-30). Estado informativo de preparación; NO es veredicto.
- **En ejecución** → solo tras cumplir la regla de ejecución.
- **Veredicto oficial emitido** → tras pasos 1–5.

## 4. Reglas inviolables (del Master Prompt, DC-11)

No asumir información faltante · No cerrar decisiones pendientes sin evidencia · No modificar Constitución ni ADRs aprobados · No emitir GO sin evidencia documental y técnica verificable · Toda conclusión reproducible y trazable · No se admiten criterios sin referencia documental (DC-12, regla de trazabilidad).
