# Herramientas de calidad — configuración por stack (Sprint 0)

**Fuente:** Doc 47 (QG-1/QG-2), POL-EGM-04/08. Todas corren en CI (`.github/workflows/ci.yml`) y en local (`scripts/dev_check.sh`).

## Backend (.NET 8)

| Herramienta | Configuración | Regla |
|---|---|---|
| Nullable + analyzers | `Directory.Build.props`: `<Nullable>enable</Nullable>`, `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` (en CI) | QG-1: 0 warnings |
| dotnet format | `.editorconfig` raíz (convenciones C#) | `--verify-no-changes` en CI |
| Analyzers de seguridad | `Microsoft.CodeAnalysis.NetAnalyzers` (reglas CA de seguridad elevadas a error) | SAST complementario (etapa 7) |
| Cobertura | coverlet vía `dotnet test --collect` | QG-2 (Doc 47): dominio 90+/app 80+/infra 70+ |

## Web (React/TS)

| Herramienta | Configuración | Regla |
|---|---|---|
| ESLint | `web/.eslintrc`: typescript-eslint strict + react-hooks + jsx-a11y (accesibilidad, Doc 40) | 0 errores |
| Prettier | `.prettierrc` raíz | verificación en CI |
| TypeScript | `strict: true` | build bloqueante |
| Auditoría a11y | axe en E2E (etapa 10) | WCAG 2.2 AA (Doc 40) |

## Mobile (`{{ADR-013}}` — parametrizado)

La cadena de análisis se instancia al aprobarse ADR-013: `flutter analyze --fatal-warnings` (Flutter) o ESLint+TypeScript strict (RN). Misma regla QG-1: 0 errores.

## Transversales

| Herramienta | Propósito | Gate |
|---|---|---|
| commitlint | Conventional Commits + WP-<id> | etapa 1, bloqueante |
| gitleaks (o equivalente) | escaneo de secretos | etapa 1, bloqueante |
| `tools/lint-migrations/check_rls.sh` | RLS+FORCE+policy en toda tabla tenant nueva | etapa 6, **indesactivable** |
| `tools/ci/rls_attack_test.sh` | 0 filas cross-tenant con rol de app | etapa 6, **indesactivable** |
| SBOM + análisis de dependencias | supply chain (Doc 60) | etapa 7 |
| `tools/ci/docs_integrity.py` | integridad documental (IDs, familias prohibidas, enlaces) | etapa 4, bloqueante en PRs de docs |
