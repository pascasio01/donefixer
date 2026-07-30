# 51 — KPI & Metrics Framework

| Campo | Valor |
|---|---|
| Documento | 51_KPI_Metrics_Framework |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Precedencia | Doc 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 01 (visión), 03 (modelo de negocio, HV-1…7), 09 (métricas de salida por fase), 12 (RNF-FIN/OBS), 30 (EV-7), 33 (FinOps IA); AO-6 (PD-2) |

> **Convención:** DC · SU · PD. Este documento propone la resolución de **PD-2 (North Star metric)** — queda PD hasta decisión expresa del Fundador.

---

## 1. Arquitectura de métricas (tres planos)

| Plano | Para quién | Fuente de datos | Latencia |
|---|---|---|---|
| **Producto (tenant)** | P-X1, P-M1, P-S1: KPIs operativos de mantenimiento | Vistas materializadas + réplica (ADR-006) | ≤1 h |
| **Negocio (plataforma)** | Fundador/equipo DONEFIXER: adopción, retención, unit economics | Esquema `platform` (ADR-012) | Diaria |
| **Sistema (SRE)** | Salud técnica | Telemetría (Doc 54) | Tiempo real |

Todo KPI se calcula desde eventos de dominio y datos transaccionales (EV-7) — nunca de tablas paralelas manuales. (DC)

## 2. KPIs de producto (dentro del tenant)

| KPI | Definición | Por qué importa | Fuente |
|---|---|---|---|
| MTTR | Tiempo medio de resolución (creación→completada) | KPI universal de mantenimiento | wo.* |
| % OT preventivas vs. correctivas | Razón PM/total | Madurez del programa de mantenimiento | pm.generated, wo.* |
| Cumplimiento de PM | PM ejecutados a tiempo / planificados | Salud de la planificación (P-D1) | pm.* |
| Tiempo de ciclo de solicitud | Solicitud→aprobada→asignada | Fricción administrativa (problema #2, Doc 01) | sr.* |
| Backlog por criticidad | OT abiertas ponderadas por riesgo | Riesgo operativo visible | wo.* |
| TCO por activo | Costos acumulados OT + repuestos + externo | RF-WO-005; decisión reparar/reemplazar | wo.*, stock.* |
| Downtime por activo | Horas fuera de servicio | RF-AST-004 | wo.*, meter.* |
| Tasa de adopción offline | % OT ejecutadas con al menos 1 operación offline | Prueba de la propuesta de valor #1 | sync.* |

## 3. Métricas de negocio (plataforma, solo equipo DONEFIXER)

| Métrica | Definición | Hipótesis vinculada (Doc 03) |
|---|---|---|
| Activación de tenant | Tenant con ≥5 OT reales en sus primeras 2 semanas | HV-3 (onboarding <1 semana, J-7) |
| WAU técnicos / técnicos invitados | Adopción real del usuario primario | HV-1 |
| Tasa de éxito de sync por tenant | >99.9%/día esperado | RNF-SYNC-001 |
| Costo IA por tenant vs. ingreso | Línea roja 30% | RNF-FIN-002 |
| Costo soporte / MRR | ≤8% | RNF-FIN-003 |
| Costo por tenant activo | Métrica mensual | RNF-FIN-004 |
| Conversión Gratis→Profesional | Pilotos medirán | HV-5 |
| Churn de pilotos | Señal temprana | HV-6 |

## 4. North Star Metric — propuesta de resolución de PD-2 (PD)

**Candidata recomendada (NO confirmada):** *"Órdenes de Trabajo completadas por semana por tenant activo" (WOTC).* (PD)

| Criterio de evaluación | Análisis |
|---|---|
| Refleja valor entregado | La OT completada es la unidad de valor real del CMMS: trabajo hecho, no clics |
| Medible y accionable | Evento `wo.completed` (Doc 30); segmentable por plan/industria/país |
| Predictora de retención | Un tenant cuyo WOTC crece o se estabiliza >0 es un tenant que renovará (hipótesis HV-6) |
| No gameable | A diferencia de "usuarios registrados", exige uso real del ciclo completo |
| Captura offline | Las OT completadas offline cuentan al sincronizarse — coherente con la propuesta de valor |

**Métricas guarda (evitan optimizar la North Star en detrimento de calidad):** tasa de veredictos REJECT (integridad), % OT reabiertas (calidad del cierre), éxito de sync (salud del canal). (PD)

**Alternativas descartadas:** WAU (mide actividad, no valor); OT creadas (mide entrada, no resolución); MRR (lagging, no accionable semanalmente). (PD)

> **AO-6:** PD-2 queda calendarizada — el Fundador decide en esta Ola 4 o antes del primer piloto. La instrumentación se construye para las tres candidatas, de modo que la decisión no bloquee ingeniería. (DC)

## 5. Métricas guarda de sistema (resumen; detalle en Doc 54)

Disponibilidad (99.5% interno, RNF-AVL-001), latencia API p95, éxito de sync, lag por dispositivo, crash-free móvil >99.5% (RNF-MOB-001), error budget. (DC)

## 6. Gobernanza de métricas

- Todo KPI nuevo nace con: definición, fuente de eventos, dueño, y revisión trimestral (gobernanza de arquitectura, Doc 20).
- Prohibido: KPIs calculados fuera del pipeline de eventos (sombra de datos). (DC)
- Los dashboards de tenant respetan permisos (P-U1 auditor: solo lectura; Doc 19). (DC)

## 7. Criterios de aceptación del documento

1. Tres planos de métricas definidos con fuente y latencia. ✅
2. PD-2 con candidata fundamentada, guardas y alternativas — **sigue PD**. ✅
3. Trazado a HV-1…7 y RNF. ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación (Ola 4, documento 4 de 8). Propone resolución de PD-2 (AO-6) sin confirmarla.*
