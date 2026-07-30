# EGM — 10: Matriz de Métricas de Ingeniería

**Norma:** DC-14 (POL-EGM-17) · Fuentes de umbrales: Doc 51 (KPIs), Doc 54 (DORA/SLO) — no redefinidos aquí. Datos automáticos desde pipeline + observabilidad; nunca encuestas manuales.

| Métrica | Definición operativa | Fuente de datos | Umbral de alerta | Frecuencia |
|---|---|---|---|---|
| Lead Time | commit → producción (p50) | pipeline (timestamps) | > 5 días (SU inicial, recalibrar tras S2) | continua |
| Cycle Time | In Progress → Done (p50) | board + pipeline | > duración de sprint | continua |
| Deployment Frequency | despliegues a producción/semana | pipeline | < 1 (tras F1-B) | semanal |
| Change Failure Rate | % releases que causan incidente o rollback | releases + incidentes | > 15% (Doc 54 DORA) | mensual |
| MTTR | detección → servicio restaurado (SEV-1/2) | registro de incidentes | > 1 h (SEV-1) | mensual |
| Cobertura de pruebas | por módulo, según QG-2 | CI | < umbral Doc 47 | por PR |
| Densidad de defectos | defectos abiertos / KLOC por módulo | tracker | tendencia creciente 2 sprints | mensual |
| Deuda técnica | TD-<n> abiertas y envejecimiento | backlog técnico | > 10 abiertas o > 60 días sin tocar | mensual |
| Vulnerabilidades abiertas | por severidad y edad | SAST/dependencias | crítica/alta > 0 sin SLA | semanal |
| Cumplimiento de SLO | % dentro de SLO por SLI (Doc 54) | observabilidad | error budget consumido > 50% antes de mitad de ventana | continua |

**Uso:** revisión mensual en retro técnica; métrica en alerta dos periodos seguidos → acción con responsable registrada (TD-<n> o WP). **Prohibido** usar métricas individuales para evaluación personal de rendimiento (métricas de sistema, no de personas — criterio Doc 51).
