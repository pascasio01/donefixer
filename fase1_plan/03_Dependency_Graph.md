# FASE 1 PRE-GO — 03: Dependency Graph

**Norma:** DC-13 · **WP-00 es la raíz obligatoria: ningún WP de construcción tiene ruta que lo evite.**
Nodos parametrizados: `{{ADR-013}}` (móvil), `{{ADR-014}}` (sync), `{{PD-CLOUD}}` (nube) — bloquean su subgrafo hasta la aprobación formal correspondiente.

## Grafo (mermaid)

```mermaid
graph TD
  WP00[WP-00 GO Doc 70] --> A1[WP-A1 Monorepo/tooling]
  A1 --> A2[WP-A2 Entornos/IaC {{PD-CLOUD}}]
  A1 --> A3[WP-A3 Esqueleto .NET]
  A1 --> A4[WP-A4 Esqueleto web]
  A1 --> A5[WP-A5 Esqueleto móvil {{ADR-013}}]
  A2 --> B1[WP-B1 Esquema PG + migraciones]
  A3 --> B1
  B1 --> B2[WP-B2 Multi-tenancy RLS]
  B2 --> B3[WP-B3 Autenticación]
  B3 --> B4[WP-B4 Autorización RBAC]
  B1 --> B5[WP-B5 Outbox/eventos]
  A2 --> B6[WP-B6 Observabilidad base]
  A3 --> B6
  B2 --> C1[WP-C1 Write-path sync]
  B5 --> C1
  C1 --> C2[WP-C2 Canal réplica {{ADR-014}}]
  A5 --> C3[WP-C3 Outbox móvil {{ADR-013}}]
  C2 --> C3
  C1 --> C4[WP-C4 Conflictos + bandeja]
  C1 --> D1[WP-D1 Órdenes de Trabajo]
  C4 --> D1
  B4 --> D2[WP-D2 Activos]
  C1 --> D3[WP-D3 Inventario]
  B4 --> D4[WP-D4 Solicitudes]
  B4 --> D5[WP-D5 Usuarios/equipos]
  D1 --> E1[WP-E1 Web journeys]
  D2 --> E1
  D4 --> E1
  D5 --> E1
  C3 --> E2[WP-E2 Móvil journeys {{ADR-013}}]
  D1 --> E2
  A4 --> E3[WP-E3 Design System]
  A5 --> E3
  E1 --> F1[WP-F1 Performance CI]
  E2 --> F1
  B2 --> F2[WP-F2 Seguridad/pentest]
  B3 --> F2
  E1 --> F3[WP-F3 Accesibilidad]
  E3 --> F3
  B6 --> F4[WP-F4 DR/game days]
  B6 --> F5[WP-F5 FinOps]
```

## Tabla de dependencias (verificación mecánica)

| WP | Depende de | Parametrización |
|---|---|---|
| WP-A1 | WP-00 | — |
| WP-A2 | WP-A1 | `{{PD-CLOUD}}` |
| WP-A3 | WP-A1 | — |
| WP-A4 | WP-A1 | — |
| WP-A5 | WP-A1 | `{{ADR-013}}` |
| WP-B1 | WP-A2, WP-A3 | — |
| WP-B2 | WP-B1 | — |
| WP-B3 | WP-B2 | — |
| WP-B4 | WP-B3 | — |
| WP-B5 | WP-B1 | — |
| WP-B6 | WP-A2, WP-A3 | — |
| WP-C1 | WP-B2, WP-B5 | — |
| WP-C2 | WP-C1 | `{{ADR-014}}` |
| WP-C3 | WP-A5, WP-C2 | `{{ADR-013}}` + `{{ADR-014}}` |
| WP-C4 | WP-C1 | — |
| WP-D1 | WP-C1, WP-C4 | — |
| WP-D2 | WP-B4 | — |
| WP-D3 | WP-C1 | — |
| WP-D4 | WP-B4 | — |
| WP-D5 | WP-B4 | — |
| WP-E1 | WP-D1, WP-D2, WP-D4, WP-D5 | — |
| WP-E2 | WP-C3, WP-D1 | `{{ADR-013}}` |
| WP-E3 | WP-A4, WP-A5 | — |
| WP-F1 | WP-E1, WP-E2 | — |
| WP-F2 | WP-B2, WP-B3 | — |
| WP-F3 | WP-E1, WP-E3 | — |
| WP-F4 | WP-B6 | — |
| WP-F5 | WP-B6 | — |

**Verificación anti-evasión de WP-00:** todo nodo excepto WP-00 tiene al menos un camino desde WP-00 (comprobado por inspección del grafo: WP-A1 es el único hijo directo y todos descienden de él). **Camino crítico:** WP-00 → A1 → A2/A3 → B1 → B2 → C1 → C2 → C3 → E2 → F1 (la rama móvil/sync, por depender de ADR-013/014).
