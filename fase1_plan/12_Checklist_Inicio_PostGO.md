# FASE 1 PRE-GO — 12: Checklist de Inicio de Desarrollo Post-GO

**Norma:** DC-13 · Se firma el **día 1 tras el GO** del Documento 70. Cualquier ítem sin marcar bloquea el inicio del primer WP de construcción.

## A. Gobernanza (verificación previa, automática donde se indica)

- [ ] Veredicto GO (o GO WITH CONDITIONS con condiciones registradas: responsable, fecha, riesgo) firmado por el Fundador.
- [ ] ADR-013 aprobado (o WPs móviles confirmados como parametrizados en espera).
- [ ] ADR-014 definitivo aprobado (o WPs de canal confirmados como parametrizados en espera).
- [ ] PD-CLOUD cerrada (o WP-A2 con alternativa aprobada vía ADR).
- [ ] Verificación automática de integridad del corpus: 0 FAIL (script gate_doc70).
- [ ] Verificación automática de integridad de `fase1_plan/`: 0 citas rotas (script `verificacion_fase1.py`).
- [ ] ADI al día: toda decisión tomada desde la aprobación de este plan está registrada.

## B. Entorno de ingeniería (Sprint 0 completado)

- [ ] Checklist Sprint 0 (entregable 05) firmado al 100%.
- [ ] Pipeline CI/CD con gates QG-1…QG-4 operativos (aunque los umbrales se activen por WP).
- [ ] Staging desplegando con rollback demostrado.
- [ ] Secrets manager operativo; 0 secretos en repo (escaneo en verde).
- [ ] Dashboards base + canal de alertas funcionando.

## C. Equipo

- [ ] Responsable asignado a cada WP activado del sprint 1 (WBS).
- [ ] Todo el equipo ha leído: Constitución (Doc 00), ADI, Registry, Doc 47 §gates, y el Master Prompt de Implementación Enterprise.
- [ ] Regla autor ≠ aprobador configurada (CODEOWNERS + protección de ramas).

## D. Primer WP

- [ ] WP-A1 cumple su Definition of Ready (dependencias satisfechas = solo WP-00; entradas disponibles; estimación aceptada; criterios de aceptación claros).
- [ ] PR plantilla con DoD enlazado; DoD de WP-A1 comprendido por el responsable.

## E. Definition of Ready (genérica — referencia para todos los WPs)

Un WP está Ready cuando: (1) todas sus dependencias están en Done; (2) su parametrización (si la tiene) está resuelta por ADR aprobado; (3) entradas documentales identificadas y vigentes; (4) threat model preliminar identificado (si toca seguridad); (5) estimación y responsable asignados; (6) criterios de aceptación y estrategia de pruebas explícitos.

## F. Definition of Done (genérica — referencia para todos los WPs)

Un WP está Done cuando: (1) gates QG-1…QG-4 verdes en su alcance; (2) cobertura y mutation según Doc 47; (3) tests en CI (no locales); (4) documentación sincronizada (ADR/RF/RNF/API/diagramas/changelog) + verificación de integridad en verde; (5) observabilidad del módulo desplegada (logs, métricas, alertas, runbook); (6) seguridad del módulo verificada (threat model cerrado, gates de seguridad); (7) PR aprobado por revisor distinto del autor; (8) riesgos residuales registrados en el registro correspondiente.

**Firmas día 1:** Principal Backend ____ · Principal DevOps ____ · Principal SRE ____ · Chief Software Architect ____
