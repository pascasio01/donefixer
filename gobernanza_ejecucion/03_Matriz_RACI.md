# EGM — 03: Matriz RACI

**Norma:** DC-14 · R=Responsable (ejecuta), A=Accountable (responde, único), C=Consultado, I=Informado.
Roles: CEA (Chief Enterprise Architect), CSA (Chief Software Architect), BE (Principal Backend), FE (Principal Web/Frontend), ME (Principal Mobile), DBA (Principal Database), CLD (Principal Cloud), DO (Principal DevOps), SRE (Principal SRE), SEC (Principal Security), QA (Principal QA Director), AIG (Principal AI Governance), CMP (Principal Compliance), TW (Principal Technical Writer), **FUND (Fundador)**.

| Actividad | R | A | C | I |
|---|---|---|---|---|
| Ejecutar WP (construcción) | según WBS (BE/FE/ME/…) | CSA | CEA, QA | resto |
| Aprobar PR (develop) | CODEOWNER del área | CSA | QA | — |
| Aprobar PR (main) | 2 CODEOWNERS | CSA | SEC | — |
| Crear ADR (borrador) | quien propone | CEA | CSA, afectados | todos |
| **Aprobar ADR** | — | **FUND** | CEA, CSA | todos |
| Migración de base de datos | DBA | CSA | SEC, DO | SRE |
| Revisión de threat model de WP | SEC | CEA | CSA, BE | QA |
| Rotación de secretos | SEC + DO | SEC | CLD | SRE |
| Release (checklist + publicación) | DO + responsable área | SRE | QA, SEC | todos |
| Rollback | DO | SRE | DBA | todos |
| Gestión de incidente SEV-1/2 | SRE (guardia) | SRE | responsable área | FUND (SEV-1) |
| Postmortem | SRE + involucrados | SRE | QA | todos |
| Registrar deuda técnica TD-<n> | autor del WP | responsable área | CSA | — |
| Eliminar deuda técnica | según backlog | responsable área | — | CSA |
| Actualización documental (mismo PR) | autor del WP | TW | afectados | — |
| Verificación de integridad documental | automática (CI) | TW | — | todos |
| Aprobación de uso de IA en producto (nueva función) | AIG | CEA | SEC, CMP | FUND |
| Auditoría continua (informes) | según plan §18 | CEA | todos | FUND |
| **Veredicto Documento 70** | comité | **FUND** | todos | — |
| Cierre de PDs (N-1, N-2, PD-*) | quien aporta evidencia | **FUND** | CEA, CSA | todos |

Reglas: una fila = un solo A; el Fundador es A solo donde la gobernanza lo exige (ADRs, veredicto Doc 70, cierre de PDs, funciones IA nuevas); las actividades ejecutadas por CI llevan R="automática" con A humano asignado.
