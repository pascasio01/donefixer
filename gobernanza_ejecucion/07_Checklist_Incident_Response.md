# EGM — 07: Checklist Maestro de Incident Response

**Norma:** DC-14 (POL-EGM-12) · Clasificación SEV y plantilla de postmortem en Doc 54 (no se redefinen aquí).

## Detección y declaración

- [ ] Incidente declarado con SEV asignado (criterio Doc 54) y canal/registro abierto.
- [ ] Guardia + responsable de área notificados (SEV-1/2: inmediato; SEV-1: también Fundador).
- [ ] Merges congelados si el incidente afecta a producción y hay cambios en curso.

## Respuesta

- [ ] Runbook RB-* correspondiente localizado y ejecutado (toda alerta tiene runbook — si no existe, es un defecto a registrar).
- [ ] ¿Criterio de disparo de rollback cumplido? (`fase1_plan/11` §2) → ejecutar rollback, no "arreglar en caliente".
- [ ] Timeline del incidente registrado (hora de detección, acciones, verificaciones).
- [ ] Comunicación interna con plantilla (SEV-1/2): impacto, estado, siguiente actualización.

## Cierre

- [ ] Golden signals estables; verificación de ausencia de pérdida de datos (sync: pérdida = 0, RNF-SYNC-004).
- [ ] Postmortem sin culpa (plantilla Doc 54): causa raíz, timeline, qué funcionó, qué no.
- [ ] Acciones correctivas con responsable y fecha cada una; registradas como TD-<n> o WP según corresponda.
- [ ] Runbook actualizado con lo aprendido; si la lección cambia una norma → ADR.
- [ ] Métricas actualizadas: MTTR, change failure rate (automático desde el registro).

**Firmas:** Guardia ____ · Responsable área ____ · Postmortem revisado por SRE ____
