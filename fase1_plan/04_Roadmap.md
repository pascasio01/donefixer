# FASE 1 PRE-GO — 04: Roadmap de Implementación

**Norma:** DC-13 · Secuenciación orientativa (sprints de 2 semanas). El camino crítico pasa por la rama sync/móvil (parametrizada por ADR-013/014).

| Sprint | Contenido principal | WPs | Salida verificable |
|---|---|---|---|
| S0 (2 sem) | Fundaciones | WP-A1…A5 (A5 solo si ADR-013 ya aprobado; si no, queda listo para activar) | Checklist Sprint 0 firmado |
| S1 | Plataforma core I | WP-B1, WP-B2, WP-B5 | RLS + outbox verdes en staging |
| S2 | Plataforma core II | WP-B3, WP-B4, WP-B6 | Auth/RBAC + golden signals |
| S3 | Sync I | WP-C1 (+ ADR de reutilización del código de Spike) | Suite J-2 portada: 15/15 en CI |
| S4 | Sync II | WP-C2, WP-C3 (requieren ADR-014/ADR-013) | J-2 modo avión en dispositivo, staging |
| S5 | Sync III + inicio módulos | WP-C4, WP-D2, WP-D5 | Bandeja de veredictos funcional |
| S6 | Módulos I | WP-D1 | OT core E2E |
| S7 | Módulos II | WP-D3, WP-D4 | Inventario + solicitudes E2E |
| S8–S9 | Experiencias | WP-E1, WP-E2, WP-E3 | Journeys web y móvil E2E |
| S10 | Endurecimiento I | WP-F1, WP-F3 | Budgets y WCAG en verde |
| S11 | Endurecimiento II | WP-F2, WP-F4, WP-F5 | Pentest interno, DR ensayado, FinOps |
| — | **H-5 Release candidate Fase 1** | — | Gates Doc 47/54/60 verdes |

**Dependencias externas al plan (no controlables por el equipo):**
- ADR-013: necesario a más tardar al final de S0 para no retrasar A5 (camino crítico).
- ADR-014 definitivo: necesario antes de S4.
- `{{PD-CLOUD}}`: necesario antes de WP-A2 (S0/S1). Si no está, A2 se ejecuta con la alternativa provisional documentada y el ADR posterior migra — **solo si el Fundador lo aprueba vía ADR**; de lo contrario A2 espera.

**Recalibración:** tras S2 se mide velocidad real y se re-estima el resto (Doc 51). Esta hoja no compromete fechas comerciales: es un plan de ingeniería SU.
