# EGM — 09: Matriz de Quality Gates

**Norma:** DC-14 (POL-EGM-16) · **Umbrales definidos en Doc 47 — esta matriz NO los redefine; los mapea a fases del WP y controles de CI.**

| Gate | Fase del WP | Contenido (Doc 47) | Control automático (etapa pipeline, `fase1_plan/06`) | Override |
|---|---|---|---|---|
| QG-1 Estático | In Progress → In Review | Análisis estático, convenciones, warnings=errores | Etapa 2 (build) | Ninguno |
| QG-2 Cobertura/Mutation | In Review | Cobertura dominio 90%+/app 80%+/infra 70%+; mutation en C1/B2/D1 | Etapa 3 (unit) — falla el build | Ninguno (excepción solo vía ADR) |
| QG-3 Integración/Contrato/Seguridad | In Review → Gates | Contract tests 100%, migraciones up/down, **test de ataque RLS**, SAST/dependencias/SBOM, escaneo de secretos | Etapas 5–7 | Ninguno |
| QG-4 E2E/Performance/Accesibilidad | Gates → Done | **Suite J-2 portada**, journeys críticos, budgets MA-8/RNF-PERF-*, WCAG auditoría | Etapas 8–10 (develop/release) | Ninguno |

**Gates permanentes indesactivables (requieren ADR para tocarse):** suite J-2 de sync · test de ataque RLS · linter de migraciones RLS/FORCE · escaneo de secretos · verificación de integridad documental.

**Regla:** ningún WP avanza de estado sin el gate de su fase en verde. Los gates los ejecuta CI; no existe override humano fuera de incidente declarado con ADR posterior (POL-EGM-16).
