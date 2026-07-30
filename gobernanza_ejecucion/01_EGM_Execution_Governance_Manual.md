# EXECUTION GOVERNANCE MANUAL (EGM) — DONEFIXER

**Versión:** 1.0 · **Fecha:** 2026-07-30 · **Norma:** DC-14
**Naturaleza:** manual operativo de ejecución. **No es fuente de requisitos ni de arquitectura**; operacionaliza el corpus existente.
**Jerarquía:** subordinado a Constitución → Documento 70 → ADRs aprobados → DC-01…DC-13. En caso de conflicto, prevalecen dichos documentos.
**Regla de no duplicación:** cuando una política ya existe en el corpus, este manual la **referencia (documento + sección)** y solo describe el procedimiento operativo para aplicarla. No modifica umbrales, requisitos, criterios técnicos ni decisiones arquitectónicas.
**Formato de política (obligatorio):** Fuente normativa · Evidencia requerida · Responsable · Método de verificación · Automatización posible · Frecuencia de control. Identificadores: `POL-EGM-xx` (índice completo en `12_Indice_Politicas.md`).

---

## 1. Modelo de ejecución (POL-EGM-01)

**Fuente:** `fase1_plan/02_WBS.md`, `fase1_plan/03_Dependency_Graph.md`, DC-13.

**Ciclo de vida del WP:** `Backlog → Ready (DoR) → In Progress → In Review (PR) → Gates → Done (DoD) → Released → In Production`. Estados prohibidos: saltarse Ready (no se puede abrir rama `feature/` sin DoR firmada en el PR inicial) y Done sin gates (el pipeline lo impide técnicamente).

**Flujo:** Backlog (WBS) → Sprint Plan → rama `feature/WP-<id>` → PR con checklist → gates QG-1…QG-4 → merge a `develop` → staging → release → producción.

**Evidencias requeridas por transición:** Ready: plantilla DoR en el issue · In Progress: rama con nombre convencional · In Review: PR con checklist completo · Done: pipeline verde + documentación sincronizada · Released: tag + changelog · In Production: verificación post-deploy (test de humo + golden signals).

**Responsable:** el responsable técnico del WP (WBS); el gate lo ejecuta CI, no personas. **Verificación:** automática (pipeline + protección de ramas). **Frecuencia:** por WP.

## 2. Definition of Ready (POL-EGM-02)

**Fuente:** `fase1_plan/12_Checklist_Inicio_PostGO.md` §E (genérica), WBS por WP.

**Criterios mínimos para abrir trabajo:** (1) dependencias en Done según grafo; (2) parametrización resuelta por ADR aprobado si aplica (`{{ADR-013}}`, `{{ADR-014}}`, `{{PD-CLOUD}}`); (3) RF y RNF relacionados vigentes en Doc 11/12 (verificación automática contra Registry); (4) ADRs relacionados aprobados en ADI; (5) riesgos identificados; (6) criterios de aceptación definidos; (7) estrategia de pruebas definida según matriz (`fase1_plan/07`); (8) threat model preliminar si toca seguridad (Doc 60).

**Procedimiento:** el responsable completa la plantilla DoR en el issue del WP; el revisor asignado la valida; sin esa validación, la protección de ramas no permite abrir `feature/`. **Evidencia:** plantilla DoR firmada en el issue. **Verificación:** manual + chequeo automático de existencia de RF/RNF/ADR citados. **Frecuencia:** por WP.

## 3. Definition of Done (POL-EGM-03)

**Fuente:** `fase1_plan/12_Checklist_Inicio_PostGO.md` §F; umbrales en Doc 47 (QG-1…QG-4) — **no se modifican aquí**.

**Criterios mínimos:** código implementado según MS-* (Doc 43) · pruebas aprobadas en CI (no locales) · seguridad validada (gates §8) · observabilidad implementada (§10) · documentación sincronizada (§14) · code review aprobado por revisor ≠ autor · quality gates superados · evidencia registrada (enlace al pipeline verde + artefactos en el issue del WP).

**Procedimiento:** merge solo cuando el pipeline está verde y el checklist de PR está completo; el WP pasa a Done en el board cuando además la documentación sincronizada está mergeada. **Evidencia:** pipeline + PR + commit de docs. **Verificación:** automática (pipeline) + checklist. **Frecuencia:** por WP.

## 4. Git Governance (POL-EGM-04)

**Fuente:** `fase1_plan/06_Plan_CICD.md` §1 (estrategia de ramas y convenciones — este manual no las redefine).

**Procedimiento operativo:** nombres de rama `feature|fix|chore/WP-<id>-<slug>`, `release/x.y`, `hotfix/x.y.z` · commits Conventional Commits con `WP-<id>` en scope (commitlint en CI) · versionado semver en tags `vX.Y.Z` firmados · releases desde `release/x.y` con changelog generado de commits · hotfix solo con incidente SEV abierto y postmortem posterior obligatorio (§12).
**Evidencia:** historial git + tags. **Verificación:** commitlint + protección de ramas (automática). **Frecuencia:** continua.

## 5. Pull Request Governance (POL-EGM-05)

**Fuente:** `fase1_plan/06_Plan_CICD.md` §2 (pipeline), Doc 47.

**Política:** tamaño recomendado ≤400 líneas netas de diff (mayor → justificar en el PR o dividir); **checklist maestro de PR obligatorio** (`05_Checklist_PR.md`); revisiones mínimas: 1 aprobación para `develop` (CODEOWNER del área), 2 para `main`; requisitos: pipeline verde completo, DoD §3, diff de documentación sincronizada incluido; **rechazo automático:** pipeline rojo, secretos detectados, cobertura por debajo del umbral, test de ataque RLS desactivado o modificado sin ADR, citas documentales rotas (verificación de integridad), autor = aprobador.
**Evidencia:** PR con checklist + checks de CI. **Verificación:** automática (required checks + CODEOWNERS). **Frecuencia:** por PR.

## 6. ADR Governance (POL-EGM-06)

**Fuente:** ADI (registro y flujo), Constitución regla 5 (toda desviación vía ADR).

**Cuándo crear:** nueva tecnología, desviación de arquitectura aprobada, cambio de contrato público, decisión con coste operativo significativo, reutilización de código de Spike en producción (EXENCIÓN-SPIKE-01 regla 8). **Cuándo modificar:** nunca se reescribe un ADR aprobado — se crea uno nuevo que lo supersedes y el ADI enlaza ambos. **Prohibido:** crear ADR para eludir gates, para cerrar PDs sin evidencia, o retroactivamente para justificar código ya mergeado. **Flujo:** borrador con plantilla del ADI → revisión de arquitectura → **aprobación del Fundador** → registro en ADI con estado → actualización de documentos afectados en el mismo PR. **Impacto documental:** todo ADR aprobado actualiza Registry/ADI y dispara revisión de WPs parametrizados que dependan de él.
**Evidencia:** ADR en ADI + PR de sincronización. **Verificación:** manual + verificación de integridad. **Frecuencia:** por evento.

## 7. Database Governance (POL-EGM-07)

**Fuente:** `fase1_plan/10_Plan_Migraciones.md` (expand/contract, orden, seeds, WAL), Doc 26 (RLS), lección empírica Spike (superuser bypassa RLS).

**Procedimiento:** migraciones versionadas e inmutables, aplicadas solo por pipeline; expand/contract obligatorio; **toda tabla con `tenant_id` nace con policy + FORCE ROW LEVEL SECURITY en la misma migración** (linter de migraciones en CI — gate automático); aplicación con rol no privilegiado siempre; test cross-tenant tras cada migración que toque tablas de tenant; seeds solo en dev/staging; datos de prueba con factories, prohibido estado compartido entre tests.
**Evidencia:** historial de migraciones + pipeline. **Verificación:** linter de migraciones + test de ataque RLS (automáticos). **Frecuencia:** por migración.

## 8. Security Governance (POL-EGM-08)

**Fuente:** `fase1_plan/08_Plan_Seguridad.md` (threat model por módulo, gates, inventario de secretos), Doc 60 (SBOM, rotación ≤90 d, supply chain).

**Procedimiento:** secretos solo en gestor con auditoría; rotación ≤90 d con ensayo (WP-F2); dependencias: nueva dependencia exige justificación en PR + verificación de licencia + SBOM diff; SAST en cada PR, DAST por release; vulnerabilidades: crítica/alta nueva = bloqueo de merge, media = ticket con SLA (Doc 60); supply chain: provenance de build + SBOM publicado por release.
**Evidencia:** SBOM por release, informe SAST/DAST, registro de rotaciones. **Verificación:** automática (etapa 7 pipeline). **Frecuencia:** continua + ensayo trimestral de rotación.

## 9. Testing Governance (POL-EGM-09)

**Fuente:** `fase1_plan/07_Plan_Testing.md` (matriz 8 capas × WP), Doc 47 (umbrales QG-2).

**Procedimiento:** las capas obligatorias por WP son las de la matriz (●); ninguna puede eliminarse sin ADR; la **suite J-2 portada de la Spike** y el **test de ataque RLS** son gates permanentes en CI; cobertura por módulo según Doc 47; mutation testing en C1/B2/D1; E2E móvil críticos en dispositivo real (CI nocturno).
**Evidencia:** reportes de CI por capa. **Verificación:** automática. **Frecuencia:** por PR (rápidas) / nocturna (completas) / por release (performance + accesibilidad).

## 10. Observability Governance (POL-EGM-10)

**Fuente:** `fase1_plan/09_Plan_Observabilidad.md` (SLI/SLO, dashboards, alertas, RB-01…08), Doc 54.

**Procedimiento:** todo módulo nuevo entrega en el mismo WP: logs estructurados (con `tenant_id`, `trace_id`, `operation_id` en sync), métricas SLI, spans de traza, entrada de dashboard, alerta con runbook enlazado (alerta sin runbook = PR incompleto); correlation IDs obligatorios end-to-end; runbooks RB-* actualizados y ensayados en game days (WP-F4).
**Evidencia:** panel del módulo + runbook mergeado. **Verificación:** checklist de PR + revisión SRE. **Frecuencia:** por WP + game day trimestral.

## 11. Release Governance (POL-EGM-11)

**Fuente:** `fase1_plan/06_Plan_CICD.md` §4, `fase1_plan/11_Plan_Rollback.md`, Doc 54.

**Criterios para publicar:** gates completos verdes en `release/x.y`, suite J-2 verde, DAST limpio de críticos, SBOM publicado, changelog, checklist maestro de Release (`06_Checklist_Release.md`) firmado por responsable de área + SRE. **Estrategia:** canary para cambios de riesgo en sync/auth; blue/green para servicios stateless cuando la infraestructura `{{PD-CLOUD}}` lo permita; feature flags solo si SU-FLAGS se resuelve vía ADR (sigue SU). **Rollback:** según `fase1_plan/11` — ensayado, con criterios de disparo objetivos. **Versionado:** semver + tag firmado + SBOM.
**Evidencia:** release firmada + artefactos. **Verificación:** checklist + pipeline. **Frecuencia:** por release.

## 12. Incident Governance (POL-EGM-12)

**Fuente:** Doc 54 (clasificación SEV, plantilla postmortem, RB-01…08).

**Procedimiento:** clasificación SEV según Doc 54 (no se redefine); escalado: SEV-1/2 → guardia + responsable de área + comunicación interna inmediata; comunicación con plantilla de incidente; **postmortem sin culpa obligatorio** para SEV-1/2 con acciones, responsables y fechas; lecciones aprendidas alimentan runbooks y, si implican cambio de norma, ADR.
**Evidencia:** registro de incidente + postmortem + acciones cerradas. **Verificación:** revisión SRE semanal de incidentes y acciones. **Frecuencia:** por incidente + revisión mensual.

## 13. Technical Debt Governance (POL-EGM-13)

**Fuente:** Doc 47 (calidad), Doc 51 (métricas), Constitución regla 5.

**Qué constituye deuda:** atajo consciente que viola DoD parcial sin romper gates (p. ej. cobertura justa en el umbral, TODO sin WP, runbook genérico). **Registro:** entrada en el backlog técnico con ID `TD-<n>`, causa, impacto, WP que la generó. **Aprobación:** incurrir en deuda exige justificación en el PR y aceptación del responsable de área — la deuda que afecte a seguridad, RLS, sync o prohibiciones IA **está prohibida** (no es deuda, es bloqueo). **Priorización:** revisión mensual; toda deuda tiene fecha objetivo o se escala a arquitectura. **Eliminación:** se cierra con PR que referencia el TD-<n> y verifica que el gate afectado queda en verde pleno.
**Evidencia:** registro TD + PR de cierre. **Verificación:** revisión mensual (métrica §17). **Frecuencia:** continua.

## 14. Documentation Governance (POL-EGM-14)

**Fuente:** Doc 00 (Constitución: la documentación es la única fuente de verdad), Registry, `VERIFICACION_INTEGRIDAD_DOCUMENTAL.md`.

**Cuándo actualizar:** en el mismo PR que el código que cambia comportamiento documentado; nunca después. **Qué documentos:** RF/RNF afectados, SRS, API (Doc 24), diagramas, changelog del módulo, y ADI/Registry si hay decisión nueva (vía ADR, §6). **Sincronización con ADR:** toda modificación derivada de un ADR lo cita. **Trazabilidad:** prohibido introducir IDs nuevos fuera del Registry; familias prohibidas = error bloqueante. **Verificación automática de integridad:** corre en CI en todo PR que toque documentación (IDs, referencias, duplicados, enlaces); **ningún PR de docs se mergea con errores de integridad** (instrucción del Fundador, aprobación de Auditoría).
**Evidencia:** diff de docs en el PR + verificación verde. **Verificación:** automática. **Frecuencia:** por PR.

## 15. AI Governance During Development (POL-EGM-15)

**Fuente:** Doc 33 §4 (P-33-1…7, canónicas), Doc 32 (GA-1…7), Master Prompt Implementación (IA como Service Account sin privilegios).

**Uso permitido (del producto en desarrollo):** funciones IA permitidas por Doc 32 con cite-or-abstain, sin decisiones autónomas (P-33). **Uso prohibido:** eludir prohibiciones P-33, datos reales de tenants en prompts, IA con privilegios de escritura directa en producción. **Uso de IA como herramienta de desarrollo (copilot):** permitido con **revisión humana obligatoria** — todo código generado por IA pasa el mismo PR/gates que el humano; el autor del PR es responsable pleno del contenido; **prohibido** pegar en herramientas externas secretos, datos de tenants o documentación marcada como interna confidencial. **Evidencia de decisiones asistidas:** si una decisión de diseño relevante se apoyó en IA, se declara en el PR (transparencia, no vergüenza).
**Verificación:** checklist de PR + revisión humana. **Frecuencia:** por PR.

## 16. Quality Gates (POL-EGM-16)

**Fuente:** Doc 47 (QG-1…QG-4, umbrales — inmodificables aquí), `fase1_plan/06_Plan_CICD.md` §3 (mapeo a etapas).

**Matriz operativa completa:** `09_Matriz_Quality_Gates.md`. Regla única: **ningún WP avanza de estado sin superar el gate de su fase**; los gates los ejecuta CI y no tienen override humano salvo incidente declarado con ADR posterior.
**Evidencia:** pipeline. **Verificación:** automática. **Frecuencia:** continua.

## 17. Métricas de Ingeniería (POL-EGM-17)

**Fuente:** Doc 51 (KPIs), Doc 54 (DORA, SLO).

**Matriz completa:** `10_Matriz_Metricas_Ingenieria.md` — Lead Time, Cycle Time, Deployment Frequency, Change Failure Rate, MTTR, cobertura, densidad de defectos, deuda técnica (TD abiertos/envejecidos), vulnerabilidades abiertas, cumplimiento de SLO; cada una con definición, fuente de datos, umbral de alerta y frecuencia. Los datos salen del pipeline y de la plataforma de observabilidad — **no de encuestas manuales**.
**Evidencia:** dashboard de ingeniería. **Verificación:** revisión mensual en retro técnica. **Frecuencia:** continua + revisión mensual.

## 18. Auditoría Continua (POL-EGM-18)

**Fuente:** `gate_doc70/` (patrón de verificación), Doc 60, Doc 54.

**Plan completo:** `11_Plan_Auditoria_Continua.md` — 8 auditorías (arquitectura, seguridad, calidad, observabilidad, documentación, gobernanza, dependencias, cumplimiento) con frecuencia, alcance, verificador automático e informe tipo. Hallazgos: se registran como TD-<n> o como bloqueo si tocan áreas protegidas; repetición de un hallazgo en dos auditorías consecutivas escala a ADR o al Fundador.
**Evidencia:** informes de auditoría archivados. **Verificación:** calendario + verificaciones automáticas permanentes en CI. **Frecuencia:** según plan (mensual/trimestral).

---

*Registro de cambios — v1.0 (2026-07-30): creación bajo DC-14. Manual operativo; no crea requisitos ni arquitectura; subordinado a Constitución → Doc 70 → ADRs → DC-01…DC-13.*
