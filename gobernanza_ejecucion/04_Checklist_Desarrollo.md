# EGM — 04: Checklist Maestro de Desarrollo (por WP)

**Norma:** DC-14 (POL-EGM-01/02/03). Se adjunta al issue del WP. Firma: responsable del WP + revisor.

## Al iniciar (DoR, POL-EGM-02)

- [ ] WP-<id> existe en la WBS con sus 16 campos completos.
- [ ] Dependencias del grafo en Done (verificado contra board).
- [ ] Parametrización resuelta por ADR aprobado (si el WP la tiene) — ADR-___ citado.
- [ ] RF citados existen en Doc 11 · RNF en Doc 12 (verificación automática verde).
- [ ] Criterios de aceptación y estrategia de pruebas según matriz (`fase1_plan/07`).
- [ ] Threat model preliminar si toca seguridad (Doc 60).
- [ ] Riesgos y estimación registrados.

## Durante

- [ ] Rama `feature/WP-<id>-<slug>` · commits convencionales con WP-<id>.
- [ ] Pipeline verde en cada push; sin commits directos a develop/main.
- [ ] Documentación se modifica en el mismo PR que el código (POL-EGM-14).
- [ ] Ningún secreto introducido (escaneo verde).

## Al cerrar (DoD, POL-EGM-03)

- [ ] Pruebas de todas las capas ● de la matriz en CI, verdes.
- [ ] Cobertura y mutation según Doc 47 (sin excepciones sin ADR).
- [ ] Gates de seguridad verdes; threat model cerrado.
- [ ] Observabilidad: logs/métricas/trazas + dashboard + alerta con runbook enlazado.
- [ ] Documentación sincronizada + verificación de integridad verde.
- [ ] PR aprobado por revisor ≠ autor; evidencias enlazadas en el issue.
- [ ] Deuda técnica (si se incurrió): TD-<n> registrada con fecha objetivo.
- [ ] Riesgos residuales actualizados en el WBS.

**Firmas:** Responsable WP ____ · Revisor ____ · Fecha ____
