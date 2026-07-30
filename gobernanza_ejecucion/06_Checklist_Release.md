# EGM — 06: Checklist Maestro de Release

**Norma:** DC-14 (POL-EGM-11). Firma conjunta: responsable de área + SRE. Sin este checklist firmado no hay publicación.

## Criterios de publicación

- [ ] Rama `release/x.y` con gates completos verdes (QG-1…QG-4).
- [ ] **Suite J-2 portada verde** en staging (sync — gate permanente).
- [ ] Test de ataque RLS verde tras última migración.
- [ ] DAST sin hallazgos críticos/altos.
- [ ] SBOM publicado + provenance del build.
- [ ] Changelog generado y revisado (WPs incluidos, ADRs afectados, migraciones).
- [ ] Migraciones: expand/contract verificado; backup previo a cualquier contract (ensayado en WP-F4).
- [ ] Dashboards y alertas del alcance del release actualizados; runbooks RB-* al día.
- [ ] FinOps: coste estimado del release dentro de presupuesto (Doc 62).
- [ ] Estrategia de despliegue elegida: canary (sync/auth/riesgo) / blue-green (stateless, si `{{PD-CLOUD}}` lo permite) / estándar.
- [ ] Plan de rollback identificado (capa afectada, mecanismo, tiempo objetivo — `fase1_plan/11`).

## Publicación

- [ ] Tag `vX.Y.Z` firmado.
- [ ] Deploy ejecutado por pipeline (nunca manual).
- [ ] Test de humo post-deploy verde + golden signals estables 30 min.
- [ ] Ventana de observación canary (si aplica) completada sin criterios de disparo de rollback.

## Post-publicación

- [ ] WPs del release marcados Released → In Production tras verificación.
- [ ] Métricas de ingeniería actualizadas (deployment frequency, lead time — automático).
- [ ] Anuncio interno con enlace al changelog.

**Firmas:** Responsable área ____ · SRE ____ · Fecha/hora UTC ____
