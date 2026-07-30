# EGM — 05: Checklist Maestro de Pull Request

**Norma:** DC-14 (POL-EGM-05). Rechazo automático si: pipeline rojo · secreto detectado · cobertura bajo umbral · test de ataque RLS desactivado/modificado sin ADR · citas documentales rotas · autor = aprobador.

## Obligatorio en todo PR

- [ ] Título: `<tipo>(WP-<id>): descripción` (Conventional Commits).
- [ ] Tamaño ≤400 líneas netas de diff o justificación de división imposible.
- [ ] Descripción: qué cambia, por qué, enlace al WP/issue y a la DoR.
- [ ] Pipeline completo verde (build, unit, contract, integration, security, E2E si aplica).
- [ ] Diff de documentación sincronizada incluido (RF/RNF/SRS/API/diagramas/changelog según corresponda).
- [ ] Verificación de integridad documental verde (si toca docs).
- [ ] SBOM diff sin dependencias nuevas injustificadas; licencias compatibles.
- [ ] Observabilidad del cambio incluida (logs/métricas/alerta/runbook si aplica).
- [ ] Tests nuevos/actualizados cubren el cambio; sin tests desactivados (`skip`) sin ADR.
- [ ] Migraciones (si hay): expand/contract, down verificado, RLS+FORCE en tablas de tenant nuevas.
- [ ] Declaración de asistencia de IA si el diseño relevante se apoyó en IA (POL-EGM-15, transparencia).
- [ ] Deuda técnica incurrida: TD-<n> enlazada (si aplica).

## Aprobaciones

- [ ] develop: 1 aprobación de CODEOWNER del área.
- [ ] main: 2 aprobaciones (CODEOWNERS) + gates de release.
- [ ] Autor ≠ aprobador (técnico, no honor).

**Evidencias enlazadas:** pipeline ___ · issue WP ___ · TD (si aplica) ___
