# FASE 1 PRE-GO — 11: Plan de Rollback

**Norma:** DC-13 · Fuente: Doc 54 (SRE), Doc 60. Rollback ensayado en WP-F4 (game days), no improvisado en incidente.

## 1. Por capa

| Capa | Mecanismo | Objetivo de tiempo | Responsable |
|---|---|---|---|
| Aplicación (backend/web) | Redeploy de la imagen/artefacto anterior (inmutable, con SBOM) | < 15 min | Principal DevOps |
| Base de datos | Nunca destructivo: expand/contract (entregable 10). Rollback de código compatible con esquema expandido. Contract diferido al release siguiente | N/A por diseño | Principal Database |
| Canal sync `{{ADR-014}}` | Procedimiento del Anexo de Reproducibilidad Fase 2 (checkpoints; reanudación sin pérdida validada en F2-RT-01) | según evidencia Fase 2 | Principal DevOps |
| Configuración/flags | Reversión de flag (si SU-FLAGS se adopta vía ADR) | < 5 min | Principal SRE |
| Migración contract fallida | Restauración desde backup previo a la migración (ensayado) | RTO ≤4 h / RPO ≤15 min (Doc 12) | Principal Database |

## 2. Criterios de disparo (cualquiera basta)

- Test de humo post-deploy fallido.
- Error rate > umbral SLO durante 10 min continuados.
- p95 de convergencia sync > 2× budget (RNF-SYNC-002) durante 15 min.
- Fallo del test de ataque RLS en staging post-migración.
- Detección de pérdida de datos (debe ser 0, RNF-SYNC-004) → **SEV-1 + rollback inmediato + congelar releases**.

## 3. Procedimiento (resumen del runbook RB-08)

1. Declarar incidente y congelar merges (Doc 54, clasificación SEV).
2. Rollback de la capa afectada según §1; verificar test de humo y golden signals.
3. Comunicación interna según plantilla de incidente.
4. Postmortem sin culpa obligatorio (plantilla Doc 54) con acciones y responsables antes de reintentar el release.

## 4. Lo que NO es rollback

- Borrar datos de sync para "empezar limpio": prohibido (pérdida de datos = 0). La recuperación de sync es por checkpoints y tombstones, nunca por purga.
- Editar producción a mano: todo cambio pasa por pipeline (auditoría, Doc 60).
