# FASE 1 PRE-GO — 06: Plan de CI/CD

**Norma:** DC-13 · Fuentes: Doc 47 (gates), Doc 54 (SRE), Doc 60 (seguridad), Doc 62 (FinOps).

## 1. Estrategia de ramas (trunk-based con rama de desarrollo)

| Rama | Propósito | Protección |
|---|---|---|
| `main` | Producción (releases etiquetadas) | Solo merge desde `release/*` o `hotfix/*`, 2 aprobaciones, gates verdes |
| `develop` | Integración continua → staging | 1 aprobación, gates verdes |
| `feature/WP-<id>-<slug>` | Trabajo de un WP | PR obligatorio, autor ≠ aprobador |
| `release/x.y` | Endurecimiento de release | Solo fixes, gates completos |
| `hotfix/x.y.z` | Corrección urgente en producción | Proceso de incidente (Doc 54), postmortem obligatorio |

## 2. Pipeline (etapas, en orden; cada una bloquea la siguiente)

1. **Commit:** commitlint, escaneo de secretos (gitleaks o equivalente).
2. **Build:** compilación + análisis estático (warnings = errores) por stack afectado.
3. **Unit + dominio:** tests rápidos (<5 min); cobertura con umbral QG-2 (Doc 47) — **falla el build si baja**.
4. **Integridad documental:** si el PR toca `/docs` o `docs/` enlazados: verificación automática del corpus (IDs, referencias, familias prohibidas).
5. **Contract tests:** esquemas de API (Doc 24) y contratos de eventos (Doc 25).
6. **Integration:** PostgreSQL real en servicio de CI (misma versión mayor), migraciones up/down, **test de ataque RLS** (0 filas cross-tenant), idempotencia del write-path.
7. **Security:** SAST, análisis de dependencias + SBOM diff (Doc 60), escaneo de imagen si aplica.
8. **E2E (staging):** journeys críticos incl. **suite J-2 portada de la Spike** (modo avión, conflictos, veredictos) — obligatoria en `develop` antes de cualquier release.
9. **Performance (release):** budgets MA-8 / RNF-PERF-*; sync 200 ops contra umbral RNF-SYNC-003.
10. **Accessibility (release):** auditoría automática WCAG sobre journeys críticos (Doc 40).
11. **Deploy:** staging automático; producción manual con aprobación (ver §4).

## 3. Quality gates automáticos (mapeo Doc 47)

| Gate | Dónde se aplica | Umbral |
|---|---|---|
| QG-1 (estático) | etapa 2 | 0 errores de análisis |
| QG-2 (cobertura/mutation) | etapa 3 | umbrales de Doc 47 por módulo |
| QG-3 (integración/contrato/seguridad) | etapas 5–7 | 100% contract tests, 0 vulnerabilidades críticas/altas nuevas |
| QG-4 (E2E/performance/accesibilidad) | etapas 8–10 | suites verdes + budgets cumplidos |

## 4. Despliegues y rollback

- **Estrategia:** despliegue a staging automático en merge a `develop`; producción por release etiquetada con aprobación del responsable del área + SRE.
- **Migraciones DB:** expand/contract (ver Plan de Migraciones) — **nunca destructivas en el mismo despliegue** que el código que deja de usar el esquema viejo.
- **Rollback:** aplicación = redeploy de la imagen anterior (<15 min, ensayado en WP-F4); DB = migración contract diferida (el rollback de app nunca requiere rollback destructivo de DB); sync/canal `{{ADR-014}}` = procedimiento del Anexo de Reproducibilidad Fase 2.
- **Feature flags:** para cambios de riesgo en módulos (SU-FLAGS sigue SU — si se adopta, vía ADR).
- **Criterios de disparo de rollback:** error rate > umbral SLO durante 10 min, p95 sync > 2× budget, fallo del test de humo post-deploy.

## 5. Artefactos y trazabilidad

- Todo artefacto versionado (semver) + SBOM publicado + provenance del build.
- Todo release enlaza: WPs incluidos, ADRs afectados, resultado de gates, changelog (Doc 51 KPIs de ingeniería se alimentan del pipeline: lead time, change failure rate, Doc 54 DORA).
