# GATE 70 — Checklist (expediente operativo, DC-12)

**Estado del expediente:** Preparado para ejecución. Cada criterio: fuente · sección · evidencia · método (AUTO = `verificacion_gate70.py` / MANUAL = comité) · **estado actual real** (2026-07-30).
Leyenda de estado: ✅ cumplido y verificable hoy · ⏳ depende de PD/spike pendiente · 🔲 no evaluado aún (se evalúa en la auditoría final).

## G-0 Regla de ejecución (bloqueante, AUTO)

| ID | Criterio | Fuente | Método | Estado actual |
|---|---|---|---|---|
| G0-1 | N-1 cerrada (ADR-013 aprobado) | ADI §4 | AUTO | ⏳ PD (medición en dispositivo pendiente) |
| G0-2 | N-2 cerrada (ADR-014 definitivo) | ADI §4 | AUTO | ⏳ PD (Carril B pendiente de precondiciones) |
| G0-3 | PD-CLOUD cerrada | ADI §4 | AUTO | ⏳ PD (depende de N-7) |
| G0-4 | PD-IA-1 cerrada | ADI §4; Doc 32 §9 | AUTO | ⏳ PD |
| G0-5 | PD-4 cerrada (idiomas) | ADI §4; Docs 01/11 | AUTO | ⏳ PD |
| G0-6 | Toda decisión bloqueante con evidencia reproducible | Spike/Anexos | AUTO+MANUAL | ⏳ (parcial: write-path tiene evidencia Fase 1; N-1/N-2 sin cerrar) |

**Cualquier ⏳ en G-0 → NO GO automático (no se continúa).**

## G-1 Gobernanza (AUTO)

| ID | Criterio | Fuente | Método | Estado actual |
|---|---|---|---|---|
| G1-1 | Constitución vigente, changelog completo | Doc 00 | AUTO | ✅ v1.13 |
| G1-2 | ADI sincronizado (toda DC/PD registrada) | ADI v1.2 | AUTO | ✅ DC-01…DC-12 registradas |
| G1-3 | Registry de IDs canónico; cero familias prohibidas en corpus | REGISTRY; anti-errata | AUTO | ✅ verificado 2026-07-30 |
| G1-4 | Integridad documental: cero IDs rotos/duplicados/huérfanos | VERIFICACION_INTEGRIDAD | AUTO | ✅ última ejecución sin errores bloqueantes |
| G1-5 | EXENCIÓN-SPIKE-01 activa y cumplida (código experimental separado) | ADI §6 | MANUAL | ✅ |
| G1-6 | Trazabilidad: todo artefacto cita documento fuente | corpus | AUTO | ✅ |

## G-2 Arquitectura — consistencia cruzada (14 dominios, AUTO+MANUAL)

| ID | Dominio | Fuente principal | Método | Estado actual |
|---|---|---|---|---|
| G2-01 | Backend | Doc 21 | MANUAL | 🔲 (doc aprobado Ola 3; evaluación de consistencia en auditoría) |
| G2-02 | Mobile | Doc 23 + spike N-1 | MANUAL | ⏳ (N-1 abierta) |
| G2-03 | Web | Doc 22 | MANUAL | 🔲 |
| G2-04 | Offline | Doc 27 + spike Fase 1 | AUTO (evidencia) | ✅ parcial — write-path validado 15/15 |
| G2-05 | Sync | Doc 27 + spike Fase 2 | AUTO (evidencia) | ⏳ (N-2 abierta) |
| G2-06 | Seguridad (diseño) | Docs 29/60 | MANUAL | 🔲 |
| G2-07 | Observabilidad | Doc 54 | MANUAL | 🔲 |
| G2-08 | FinOps | Doc 62 | MANUAL | 🔲 |
| G2-09 | AI | Docs 32/33 (P-33-1…7 canónicas) | AUTO (consistencia docs 19↔33) | ✅ AO-2 verificado |
| G2-10 | Multi-tenancy | Doc 26 (MT-3/MT-4) + spike (RLS/superuser) | AUTO (evidencia) | ✅ parcial — hallazgo incorporado |
| G2-11 | API | Doc 24 | MANUAL | 🔲 |
| G2-12 | Eventos | Doc 25 (EV-1 outbox) + spike | AUTO (evidencia) | ✅ parcial |
| G2-13 | PostgreSQL | Doc 28 + spike (16.2 real) | AUTO (evidencia) | ✅ parcial |
| G2-14 | RLS | Doc 26 + spike (FORCE RLS validado) | AUTO (evidencia) | ✅ parcial — 0 filas cross-tenant |

## G-3 Seguridad (MANUAL salvo indicación)

| ID | Criterio | Fuente | Estado actual |
|---|---|---|---|
| G3-1 | Threat model STRIDE por flujo | Doc 60 §STRIDE | 🔲 (definido; validación en auditoría) |
| G3-2 | Zero Trust / Least Privilege / Defense in Depth | Docs 29/60; Master Prompt Implementación | 🔲 |
| G3-3 | RLS con rol no privilegiado (lección spike: superuser bypassa RLS) | Doc 26 + SPIKE_S2_S3 | ✅ evidencia spike |
| G3-4 | Secrets: rotación ≤90 d, gestión | Doc 60 | 🔲 |
| G3-5 | TLS extremo a extremo | Docs 21/29 | 🔲 |
| G3-6 | Auditoría | Docs 26/54/60 | 🔲 |
| G3-7 | Supply chain / SBOM | Doc 60 | 🔲 |
| G3-8 | Gestión de vulnerabilidades + gobernanza de dependencias | Doc 60 | 🔲 |

## G-4 Calidad (MANUAL + AUTO de gates)

| ID | Criterio | Fuente | Estado actual |
|---|---|---|---|
| G4-1 | Estrategia de pruebas (12 capas) | Doc 47 | 🔲 |
| G4-2 | Quality gates QG-1…QG-4 definidos y medibles | Doc 47 | ✅ definidos (aprobado Ola 4) |
| G4-3 | Cobertura + mutation score con umbrales | Doc 47 | ✅ definidos |
| G4-4 | Performance budgets (MA-8, web, sync) | Docs 23/22/47 | ✅ definidos |
| G4-5 | Accesibilidad WCAG 2.2 AA | Doc 40 | ✅ definido |
| G4-6 | Disaster Recovery / Backup-Restore probado | Doc 54 | ⏳ (definido; prueba real en Carril B F2-RT-01) |

## G-5 Operación (MANUAL)

| ID | Criterio | Fuente | Estado actual |
|---|---|---|---|
| G5-1 | Golden signals + SLI/SLO + error budget | Doc 54 | ✅ definidos |
| G5-2 | Dashboards + alert routing + runbooks RB-01…08 | Doc 54 | ✅ definidos |
| G5-3 | Clasificación de incidentes SEV + postmortem | Doc 54 | ✅ definidos |
| G5-4 | Capacity planning + FinOps (alertas, ciclo de vida storage) | Doc 62 | ✅ definidos |
| G5-5 | Coste IA < 30% revenue tenant (línea roja) | Doc 62; Doc 33 GA | ✅ definido |

## G-6 Legal / Cumplimiento (MANUAL)

| ID | Criterio | Fuente | Estado actual |
|---|---|---|---|
| G6-1 | Términos y privacidad | Docs 03/12 | 🔲 (borradores documentales; revisión legal externa pendiente) |
| G6-2 | Licencias de terceros compatibles | Doc 60 (SBOM) | 🔲 |
| G6-3 | Marca | Doc 03 | 🔲 |
| G6-4 | Retención de datos (plataforma) | PD-RETENCIÓN | ⏳ PD informativa abierta |
| G6-5 | Residencia de datos | Doc 26; PD-CLOUD | ⏳ ligada a PD-CLOUD |

## G-7 Reproducibilidad (AUTO)

| ID | Criterio | Fuente | Estado actual |
|---|---|---|---|
| G7-1 | Write-path/sync: evidencia Fase 1 completa (15/15, datos brutos, scripts) | SPIKE_S2_S3 + harness | ✅ |
| G7-2 | N-2: Anexo de Reproducibilidad Fase 2 | spike_fase2 | ⏳ (pendiente Carril B) |
| G7-3 | N-1: Anexo de Reproducibilidad dispositivo | n1_instrumentacion | ⏳ (pendiente medición) |
| G7-4 | Toda decisión crítica con métricas + datos brutos + scripts | ADI ↔ spikes | ⏳ parcial |

**Resumen de estado actual (informativo, NO veredicto):** ✅ 17 · ⏳ 11 · 🔲 14. La auditoría final re-evaluará todo con el corpus cerrado.

> Registro (2026-07-30): **DC-15** adoptada — Master Prompt Enterprise Production Implementation v1.0 (POST-GO) incorporado como especificación oficial de ejecución de WPs post-Gate, en **estado inerte** hasta veredicto GO. No altera criterios G-0…G-42 ni la regla de ejecución; se registra como referencia para la fase posterior al Gate.
