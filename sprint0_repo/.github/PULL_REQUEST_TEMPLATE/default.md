<!-- Plantilla oficial de Pull Request (POL-EGM-05). Rechazo automático: pipeline rojo · secreto · cobertura bajo umbral · test RLS tocado sin ADR · docs rotas · autor=aprobador. -->
## Tipo y WP
`<tipo>(WP-<id>): ` — WP: #___

## Qué cambia y por qué

## Evidencias
- Pipeline: ___
- DoR del WP: ___
- Asistencia de IA en diseño relevante (POL-EGM-15): ☐ no aplica ☐ declarada: ___

## Checklist obligatorio
- [ ] ≤400 líneas netas o justificación
- [ ] Documentación sincronizada en este PR (POL-EGM-14)
- [ ] Verificación de integridad documental verde (si toca docs)
- [ ] SBOM diff sin dependencias nuevas injustificadas
- [ ] Observabilidad incluida (logs/métricas/alerta/runbook si aplica)
- [ ] Tests nuevos en CI; ningún `skip` sin ADR
- [ ] Migraciones (si hay): expand/contract + down + RLS/FORCE en tablas tenant nuevas
- [ ] Deuda incurrida: TD-<n> enlazada (si aplica)
