# FASE 1 PRE-GO — 07: Plan de Testing

**Norma:** DC-13 · Fuente: Doc 47 (12 capas, QG-1…QG-4). Matriz por WP — las capas obligatorias se marcan ●, las opcionales ○, las no aplicables —.

## 1. Matriz de pruebas por WP

| WP | Unit | Integration | Contract | E2E | Performance | Security | Accessibility | Chaos |
|---|---|---|---|---|---|---|---|---|
| A1–A5 (esqueletos) | ● | ○ | — | — | — | ● (escaneo) | — | — |
| B1 (esquema) | ● | ● (migraciones up/down) | — | — | — | ● | — | — |
| B2 (RLS) | ● | ● | — | ● (cross-tenant E2E) | — | ● (**ataque RLS obligatorio**) | — | ○ |
| B3 (auth) | ● | ● | ● | ● | ○ | ● (sesiones, revocación) | — | — |
| B4 (RBAC) | ● | ● | ● | ● | — | ● (privesc) | — | — |
| B5 (outbox) | ● | ● | ● (eventos) | — | ○ | — | — | ● (kill publicador) |
| B6 (observabilidad) | ○ | ● | — | — | — | — | — | ○ |
| C1 (write-path) | ● (matriz de estados 100%) | ● | ● | ● (**J-2 portada**) | ● (200 ops, RNF-SYNC-003) | ● | — | ● (cortes, reinicios) |
| C2 (canal {{ADR-014}}) | ● | ● | ● | ● (batería F2 portada) | ● | ● (TLS, tokens) | — | ● (F2-CH portados) |
| C3 (outbox móvil {{ADR-013}}) | ● | ● | — | ● (modo avión dispositivo) | ● (arranque, batería) | ● (SQLCipher, RNF-SEC-003) | — | ○ |
| C4 (conflictos) | ● | ● | — | ● | — | — | ● (bandeja legible) | — |
| D1 (OT) | ● | ● | ● | ● | ● | ● | ● | — |
| D2–D5 | ● | ● | ● | ○ | ○ | ● | ○ | — |
| E1/E2 (journeys) | ● | — | — | ● | ● (budgets) | ● | ● (WCAG) | — |
| E3 (Design System) | ● (snapshot/tokens) | — | — | ○ | — | — | ● | — |
| F1–F5 (endurecimiento) | — | ● | — | ● | ● | ● | ● | ● |

## 2. Reglas transversales

- **Suite J-2 de la Spike portada** es un gate permanente en CI (etapa 8 del pipeline): cualquier regresión de sync bloquea el merge. Es la conversión de la evidencia de investigación en control de calidad de producción.
- **Test de ataque RLS** (intentar leer/escribir cross-tenant con el rol de aplicación) es obligatorio y no puede desactivarse sin ADR.
- **Idempotencia:** todo endpoint de escritura tiene test de reenvío idéntico (reenvío = mismo resultado, cero efectos duplicados).
- **Mutation testing** por módulos core (C1, B2, D1) con umbral de Doc 47.
- **Cobertura mínima:** dominio 90%+; aplicación 80%+; infraestructura 70%+ (Doc 47 QG-2).
- **Datos de prueba:** factories por tenant; prohibido compartir estado entre tests (aislamiento como en producción).
- **Dispositivo real:** E2E móvil críticos se ejecutan en granja de dispositivos o dispositivo físico en CI nocturno (gama media, como la medición N-1).

## 3. Definición de hecho (extracto de DoD, completo en `12_Checklist_Inicio_PostGO.md`)

Un WP está Done cuando: gates QG-1…QG-4 verdes en su alcance, cobertura cumplida, tests nuevos en CI (no locales), documentación sincronizada (ADR/RF/RNF/API/changelog), observabilidad del módulo desplegada, y PR aprobado por un revisor distinto del autor.
