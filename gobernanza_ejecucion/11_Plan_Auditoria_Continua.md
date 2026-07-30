# EGM — 11: Plan de Auditoría Continua

**Norma:** DC-14 (POL-EGM-18) · Patrón heredado de `gate_doc70/` (verificación automática + informe). Hallazgo que toca seguridad, RLS, sync o prohibiciones IA = **bloqueo**, no observación. Hallazgo repetido en 2 auditorías consecutivas → escala a ADR o al Fundador.

| Auditoría | Frecuencia | Alcance | Verificador automático | Informe |
|---|---|---|---|---|
| Arquitectura | Trimestral | Consistencia docs 21–33 entre sí y con ADIs; WPs ejecutados vs. documentado | verificación de integridad + revisión CEA/CSA | Informe con hallazgos H-<n> y acciones |
| Seguridad | Mensual (automática continua) | Gates de seguridad, rotaciones cumplidas, SBOM, dependencias, test RLS | etapa 7 pipeline + registro de rotaciones | Informe SEC |
| Calidad | Mensual | QG-1…4 cumplidos, cobertura, mutation, excepciones (debe ser 0 sin ADR) | reportes CI | Informe QA |
| Observabilidad | Trimestral | SLI/SLO activos, alertas con runbook (100%), game days realizados | plataforma de observabilidad | Informe SRE |
| Documentación | Continua (CI) + revisión mensual | Integridad: IDs, referencias, duplicados, enlaces, DC/SU/PD | `verificacion_gate70.py` + checks de PR | Automático en CI; revisión TW mensual |
| Gobernanza | Trimestral | ADI sincronizado, PDs al día, EGM aplicado (muestreo de PRs/WPs), RACI respetada | revisión CEA | Informe de gobernanza al Fundador |
| Dependencias | Mensual | SBOM diff acumulado, versiones EOL, licencias | análisis de dependencias CI | Informe SEC/DO |
| Cumplimiento | Trimestral | G-6 del Gate (privacidad, retención, licencias, marca) hasta revisión legal externa | checklist manual CMP | Informe CMP al Fundador |

**Formato de informe (único para todas):** alcance · método · hallazgos (ID, severidad, evidencia, referencia documental) · acciones (responsable, fecha) · estado de acciones anteriores · firma del responsable de la auditoría. Archivados en el repositorio de gobernanza.
