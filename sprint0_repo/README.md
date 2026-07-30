# DONEFIXER — Monorepo (Sprint 0)

**Estado:** Sprint 0 — estructura definitiva sin lógica de negocio (Master Prompt Sprint 0 Execution v1.0; materializa `fase1_plan/05`, DC-13; operado según EGM, DC-14).
**Parametrización (no instanciar hasta ADR aprobado):** `mobile/` ← **ADR-013** · canal de réplica de sync en infra ← **ADR-014** · proveedor cloud en `infra/` ← **PD-CLOUD**.

## Estructura

```
/backend            .NET 8 — Domain / Application / Infrastructure / Api (Doc 21)
  /src/DoneFixer.Domain          Dominio puro: máquina de estados OT (Doc 14), HLC, veredictos (ADR-011 v1.1)
  /src/DoneFixer.Application     Casos de uso, write-path sync (Doc 27), puertos
  /src/DoneFixer.Infrastructure  PostgreSQL (Doc 28), RLS (Doc 26), outbox (Doc 25)
  /src/DoneFixer.Api             API (Doc 24)
  /tests                         DomainTests / ApplicationTests / IntegrationTests / ContractTests (Doc 47)
/web                React — Doc 22; /design-system ← tokens DS-* (Doc 40)
/mobile             {{ADR-013}} — Flutter o RN+Expo (NO instanciar antes de ADR-013)
/infra              IaC {{PD-CLOUD}} · /env (plantillas por entorno) · /modules
/docs               /adr (plantilla) · /rfc (plantilla) — el corpus canónico vive en donefixer/ (este repo lo referencia)
/tools              /ci (scripts de gates) · /lint-migrations (linter RLS/FORCE — POL-EGM-07)
/scripts            utilidades de desarrollo (sin lógica de negocio)
.github             /workflows (CI) · plantillas oficiales (PR, issues)
```

## Convenciones

- **Carpetas:** kebab-case (web, infra, scripts), PascalCase en .NET (`DoneFixer.*`), camelCase en paquetes TS.
- **Nombres de rama:** `feature|fix|chore/WP-<id>-<slug>` · `release/x.y` · `hotfix/x.y.z` (POL-EGM-04).
- **Commits:** Conventional Commits con `WP-<id>` en scope — commitlint obligatorio.
- **Migraciones DB:** `backend/src/DoneFixer.Infrastructure/Migrations/V####__nombre.sql` — inmutables, expand/contract, **toda tabla con tenant_id nace con policy + FORCE RLS** (linter en CI).

## Reglas de este repositorio

1. Sin lógica de negocio hasta WP correspondiente con DoR firmada (POL-EGM-02).
2. La documentación canónica NO se duplica aquí: se referencia (`/docs/README.md` enlaza al corpus).
3. Ningún secreto en el repo (escaneo en CI, POL-EGM-08).
4. WP-00 = GO del Documento 70: los WPs de construcción se activan tras el GO (DC-13).
