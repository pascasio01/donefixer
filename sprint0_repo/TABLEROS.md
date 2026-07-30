# Tableros de trabajo (Sprint 0)

**Norma:** POL-EGM-01 · Estados = los del ciclo de vida del WP (EGM §1). Se implementan en la herramienta de proyectos elegida (GitHub Projects o equivalente) con estas columnas y reglas exactas.

## 1. Tablero Backlog

Columnas: `Backlog → Ready → (bloqueados)`.
- Entra todo WP de la WBS (28 WPs de `fase1_plan/02`).
- Pasa a **Ready** solo con DoR firmada en el issue (POL-EGM-02) — la columna se audita en la revisión semanal.
- Subcolumna visual: `Parametrizado (esperando ADR-013 / ADR-014 / PD-CLOUD)` — WPs A5, C2, C3, E2 y A2 parcial.

## 2. Tablero Sprint

Columnas: `Ready → In Progress → In Review → Gates → Done`.
- WIP limit: 1 WP por persona en In Progress; 2 por persona en In Review.
- Un WP no se mueve a Gates manualmente: lo hace el pipeline (verde) + aprobación del PR.
- Bloqueado = etiqueta roja con causa y fecha; bloqueos > 3 días se escalan al responsable de área.

## 3. Tablero Release

Columnas: `Candidatos → release/x.y abierta → Endurecimiento (QG-4) → Publicada → Verificada en producción`.
- Cada tarjeta = un release con su checklist maestro (`gobernanza_ejecucion/06`) adjunto y firmado.
- Métricas automáticas del tablero alimentan la matriz de métricas (EGM 10): lead time, deployment frequency, change failure rate.

## Reglas transversales

- Ninguna tarjeta existe sin WP-<id> o TD-<n> o incidente asociado.
- El tablero es consecuencia del pipeline, no un sistema paralelo: si difieren, el pipeline manda.
