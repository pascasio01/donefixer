> Expediente de cierre de PDs bloqueantes (G-0 del Doc 70). Material preparado; la decisión y la evidencia externa corresponden al Fundador. Subordinado a DC-01…DC-15. Nada de esto autoriza código de producción.

# 01 · Ficha de decisión — PD-CLOUD (proveedor cloud)

**Qué decide:** proveedor cloud de producción para Etapa A (PostgreSQL gestionado, cómputo, red, observabilidad, backups).
**Lo que NO decide:** la arquitectura (ya aprobada) ni la modalidad de PowerSync (eso es N-2/ADR-014).

## Criterios del corpus que aplican
- ADR-003: PostgreSQL como base única → el proveedor debe ofrecer PostgreSQL 16 gestionado con `wal_level=logical` (requisito de réplica lógica para sync).
- ADR-002: escrituras vía backend propio → cómputo para monolito .NET 8 (contenedores).
- RNF-SCL-002 / ADR-001: camino de aislamiento multi-tenant sin rediseño.
- Doc 62 (FinOps): TCO y límites de coste; N-7 (residencia fiscal) condiciona facturación/regiones.
- DC-14/EGM: rollback y portabilidad (evitar lock-in irreversible).

## Opciones (parametrizadas, sin instanciar)
| Opción | Encaje con criterios | Riesgo principal |
|---|---|---|
| A — Hiperescalar mayor (AWS/Azure/GCP) | Máximo encaje; PostgreSQL gestionado con réplica lógica en los tres | Coste/complejidad; requiere disciplina FinOps |
| B — Cloud europeo especializado (p. ej. OVH/Scaleway/Hetzner) | Cumple PostgreSQL gestionado (verificar réplica lógica por plan); ventaja RGPD/residencia | Catálogo gestionado más corto; madurez de algunos servicios |
| C — Plataforma Postgres-centric (p. ej. Neon/Supabase/Crunchy) | PostgreSQL de primer nivel, branching, réplica lógica (verificar) | Cómputo del backend como servicio separado; dependencia de un proveedor más joven |

## Datos que debe adjuntar la decisión (para reproducibilidad)
Precio por entorno (dev/staging/prod), SLA, regiones disponibles, soporte de `wal_level=logical` y PITR, coste estimado 12/24 meses (Doc 62).

## Formato de cierre
Una vez firmada: registrar en ADI + Índice Maestro; sustituir `{{PD-CLOUD}}` en `sprint0_repo/infra` y `fase1_plan`; actualizar `08_Plan_Seguridad.md` (inventario de secretos del proveedor). Decisión = **DC-16** si el Fundador la emite (cambia parametrización del corpus).
