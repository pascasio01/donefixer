# EGM — 12: Índice de Políticas Operativas

**Norma:** DC-14 · Catálogo único. Toda política nueva se registra aquí antes de aplicarse; ninguna duplica normas del corpus (regla DC-14).

| ID | Política | Fuente normativa | Sección EGM | Verificación | Frecuencia | Estado |
|---|---|---|---|---|---|---|
| POL-EGM-01 | Modelo de ejecución y ciclo de vida del WP | `fase1_plan/02,03` | §1 | pipeline + protección ramas | por WP | Activa |
| POL-EGM-02 | Definition of Ready | `fase1_plan/12` §E | §2 | plantilla + chequeo IDs | por WP | Activa |
| POL-EGM-03 | Definition of Done | `fase1_plan/12` §F; Doc 47 | §3 | pipeline + checklist | por WP | Activa |
| POL-EGM-04 | Git governance | `fase1_plan/06` §1 | §4 | commitlint + ramas protegidas | continua | Activa |
| POL-EGM-05 | Pull request governance | `fase1_plan/06` §2 | §5 | required checks + CODEOWNERS | por PR | Activa |
| POL-EGM-06 | ADR governance | ADI; Constitución r.5 | §6 | manual + integridad | por evento | Activa |
| POL-EGM-07 | Database governance | `fase1_plan/10`; Doc 26 | §7 | linter migraciones + test RLS | por migración | Activa |
| POL-EGM-08 | Security governance | `fase1_plan/08`; Doc 60 | §8 | etapa 7 pipeline | continua | Activa |
| POL-EGM-09 | Testing governance | `fase1_plan/07`; Doc 47 | §9 | CI por capas | por PR/nocturna/release | Activa |
| POL-EGM-10 | Observability governance | `fase1_plan/09`; Doc 54 | §10 | checklist PR + revisión SRE | por WP + trimestral | Activa |
| POL-EGM-11 | Release governance | `fase1_plan/06,11`; Doc 54 | §11 | checklist firmado + pipeline | por release | Activa |
| POL-EGM-12 | Incident governance | Doc 54 | §12 | revisión SRE | por incidente + mensual | Activa |
| POL-EGM-13 | Technical debt governance | Doc 47/51; Constitución r.5 | §13 | revisión mensual (métrica §17) | continua | Activa |
| POL-EGM-14 | Documentation governance | Doc 00; Registry; VERIFICACION | §14 | CI de integridad | por PR | Activa |
| POL-EGM-15 | AI governance durante desarrollo | Doc 33 §4; Doc 32 | §15 | checklist PR + revisión humana | por PR | Activa |
| POL-EGM-16 | Quality gates | Doc 47 (umbrales) | §16 + `09_Matriz_Quality_Gates.md` | CI | continua | Activa |
| POL-EGM-17 | Métricas de ingeniería | Doc 51/54 | §17 + `10_Matriz_Metricas_Ingenieria.md` | dashboard | continua + mensual | Activa |
| POL-EGM-18 | Auditoría continua | `gate_doc70/`; Doc 60/54 | §18 + `11_Plan_Auditoria_Continua.md` | calendario + CI | según plan | Activa |
