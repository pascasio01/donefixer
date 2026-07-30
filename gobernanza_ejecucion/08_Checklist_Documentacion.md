# EGM — 08: Checklist Maestro de Documentación

**Norma:** DC-14 (POL-EGM-14) · La documentación es la única fuente de verdad (Constitución). Se aplica a todo PR que toque `/docs`, ADI, Registry o documentos del corpus.

## Antes de escribir

- [ ] ¿La norma ya existe? → **referenciar documento + sección; no duplicar** (regla de no duplicación DC-14).
- [ ] ¿Requiere decisión nueva? → va por ADR (POL-EGM-06), no por edición directa.
- [ ] ¿Cambia un umbral, requisito o criterio técnico? → **prohibido desde el EGM**; requiere ADR + aprobación del Fundador.

## En el PR

- [ ] Documentación actualizada en el mismo PR que el código que cambia el comportamiento.
- [ ] Todo ID citado existe en Registry/Doc 11/Doc 12/ADI (verificación automática verde).
- [ ] Cero familias prohibidas (anti-errata del Registry).
- [ ] IDs nuevos solo vía Registry (no se inventan en el documento).
- [ ] Trazabilidad DC/SU/PD correcta en toda afirmación nueva.
- [ ] Changelog del documento actualizado (versión + fecha + resumen).
- [ ] Enlaces internos verificados (automático).
- [ ] Si deriva de un ADR: el ADR está citado y aprobado.

## Después del merge

- [ ] Verificación de integridad del corpus completa: 0 errores bloqueantes.
- [ ] ADI sincronizado si había decisión nueva.
- [ ] Artefactos dependientes revisados (WBS, checklists, gate_doc70) si el cambio los afecta.

**Regla bloqueante:** ningún PR de documentación se mergea con errores de integridad (instrucción del Fundador, aprobación de Auditoría — permanente).
