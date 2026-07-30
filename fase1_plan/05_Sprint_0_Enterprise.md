# FASE 1 PRE-GO — 05: Sprint 0 Enterprise

**Norma:** DC-13 · Sprint 0 = preparación técnica completa del entorno de desarrollo. **No contiene lógica de negocio.** Criterio de salida: este checklist firmado al 100%.

## 1. Repositorio y convenciones

- [ ] Monorepo creado con estructura: `/backend` (.NET 8), `/web` (React), `/mobile` (`{{ADR-013}}`), `/infra`, `/docs` (enlace al corpus), `/.github` o equivalente CI.
- [ ] Convención de ramas (ver Plan CI/CD §1): `main` protegida, `develop`, `feature/WP-<id>-<slug>`, `release/x.y`, `hotfix/x.y.z`.
- [ ] Conventional Commits obligatorio (commitlint en CI): `feat|fix|chore|docs|test|perf|refactor(scope): …` con `WP-<id>` en el scope.
- [ ] Plantillas: PR (con checklist DoD), ADR (formato del ADI), issue técnico, incidente.
- [ ] Linters/formateo por stack: dotnet format + analyzers (nullable strict, TreatWarningsAsErrors en CI), ESLint+Prettier (web), análisis estático móvil `{{ADR-013}}`.
- [ ] `CODEOWNERS` por área (backend, web, mobile, infra, docs) — regla: autor ≠ aprobador.
- [ ] Verificación de integridad documental en CI: script del corpus corre en PRs que toquen `/docs`.

## 2. Entornos e infraestructura

- [ ] Cuentas/proyectos cloud `{{PD-CLOUD}}` aprovisionados (dev, staging).
- [ ] IaC base (módulo de red, base de datos, secrets manager, registry de artefactos).
- [ ] Secrets manager operativo; **ningún secreto en el repo** (escaneo en CI, Doc 60).
- [ ] PostgreSQL 16 en staging con `wal_level=logical` (requerido por sync), rol de aplicación **no privilegiado** (lección Spike: superuser bypassa RLS).
- [ ] Política de backups activada desde el primer día (aunque no haya datos).

## 3. Pipeline base (sin gates de negocio aún)

- [ ] Pipeline CI: build + análisis estático + tests vacíos + escaneo de secretos + SBOM.
- [ ] Despliegue continuo a staging de un servicio mínimo ("hola mundo") con rollback demostrado.
- [ ] Dashboard FinOps del entorno (coste de staging visible desde el día 1, Doc 62).

## 4. Observabilidad base

- [ ] Stack de logs/métricas/trazas seleccionado según Doc 54 y desplegado en staging.
- [ ] Dashboards núcleo (golden signals) con datos del servicio mínimo.
- [ ] Canal de alertas + rotación de guardia definida (aunque sea una persona, Doc 54).

## 5. Calidad y seguridad base

- [ ] Umbrales de cobertura configurados (Doc 47 QG-2) — fallan el build si no se cumplen desde el primer WP.
- [ ] Quality gates QG-1…QG-4 cableados en CI (aunque los umbrales se activen por WP).
- [ ] Test de ataque RLS plantilla en el repositorio de tests (listo para WP-B2).

## 6. Equipo y proceso

- [ ] Responsables por WP asignados (WBS, columna Responsable).
- [ ] Calendario de sprints + ceremonias mínimas (planning, review de gates, retro técnica).
- [ ] Acceso del equipo a: repo, entornos, dashboards, gestor de secretos, corpus documental.
- [ ] Onboarding documentado: cómo leer el corpus, el ADI y el Registry antes del primer WP.

## 7. Activaciones pendientes (bloqueadas por gobernanza, no por técnica)

| Activación | Requiere | Acción al aprobarse |
|---|---|---|
| Toolchain móvil en CI | ADR-013 | Instanciar WP-A5 con la variante aprobada (mismo checklist) |
| Servicio de réplica en staging | ADR-014 definitivo | Aplicar configuración del Anexo de Reproducibilidad Fase 2 |
| Cuentas cloud definitivas | PD-CLOUD | Aprovisionar WP-A2 |

**Firma de cierre del Sprint 0:** Principal DevOps + Principal Backend + Principal SRE. Fecha: ____
