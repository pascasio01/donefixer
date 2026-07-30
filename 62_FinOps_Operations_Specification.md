# 62 — FinOps Operations Specification

| Campo | Valor |
|---|---|
| Documento | 62_FinOps_Operations_Specification |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Precedencia | Doc 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 03 §11 bis (sensibilidad), 12 (RNF-FIN-001…004), 21 §5 (dashboard), 32 (AIA-9), 33 §6, 51 (métricas negocio); AO-6 (SU-FLAGS, PD-RETENCIÓN) |

---

## 1. Modelo de costo y Cost Allocation

| Dimensión de asignación | Método | Granularidad |
|---|---|---|
| Por tenant | Costo directo (IA, almacenamiento de evidencias, emails/WhatsApp) + proporcional (cómputo, BD) por uso medido | Mensual, visible en Consola (RNF-FIN-004) |
| Por caso de uso de IA | Tokens/costo registrado en AI Gateway (AIA-9) | Por request |
| Por ambiente | Etiquetado obligatorio de recursos (env/tenant/servicio) | Diario |
| Por canal de notificación | Email (costo unitario), push (≈0), WhatsApp (por conversación, H-25 SU) | Mensual |

**Regla:** ningún recurso cloud sin etiquetas de asignación; recurso sin etiqueta aparece como "huérfano" en revisión semanal. (DC)

## 2. Presupuestos y Budget Alerts

| Presupuesto | Valor Etapa A | Alertas |
|---|---|---|
| Infraestructura total | $150–500/mes (RNF-FIN-001, SU) | 50% / 80% / 100% / proyección >110% |
| IA total | Derivado de línea roja por tenant | Por tenant al 70% y 90% de su línea |
| Soporte | ≤8% MRR (RNF-FIN-003, SU) | Mensual |
| WhatsApp | Tope por tenant por plan | 80%/100% con corte o overage según elección del tenant |

Alertas al dashboard FinOps + P2/P3 según Doc 54 §5. (DC)

## 3. Líneas rojas (heredadas, vinculantes)

1. **Costo IA >30% del ingreso del tenant** → revisión obligatoria: routing a modelo más barato, ajuste de cuota o de precio (RNF-FIN-002, Doc 33 §6). (DC)
2. **Costo por tenant activo > ingreso por tenant** durante 2 meses consecutivos → revisión de plan/precio del segmento (Doc 03 §11 bis). (DC)
3. **Infraestructura > presupuesto 110%** sin crecimiento de tenants que lo explique → revisión arquitectónica (gobernanza trimestral, Doc 20). (DC)

## 4. Capacity Forecasting

- Proyección mensual de: tenants, usuarios, OTs, almacenamiento de evidencias, tokens IA — contra dimensión de diseño Etapa A (50 tenants / 5K usuarios / 500K OTs, RNF-SCL-001 SU). (DC)
- Punto de revisión al 60% de cualquier dimensión: decide si escalar dentro de Etapa A o activar criterio de Etapa B (ClickHouse/Kafka/K8s según sus criterios medibles — nunca por adelantado). (DC)
- Forecast a 6 meses actualizado en cada revisión trimestral de arquitectura. (DC)

## 5. Reserved Capacity Strategy

Etapa A: **todo bajo demanda** (volumen incierto, pilotos). Compromisos de capacidad (reserved/savings plans) solo cuando: (a) uso estable demostrado ≥3 meses, (b) descuento ≥25% vs. bajo demanda, (c) el compromiso no exceda el 70% del uso base medido. Primera evaluación: tras 3 meses de pilotos. (DC)

## 6. AI Cost Monitoring (detalle operativo)

| Control | Implementación |
|---|---|
| Medición | Tokens in/out, modelo, caso de uso, tenant — por request en AI Gateway (RNF-AI-004) |
| Cuotas | Por plan (Doc 03 §11 bis); overage de pago o degradación, elección del tenant |
| Routing | Modelo más barato que supere umbral de calidad del golden-set (Doc 03 §11 bis) |
| Cacheo | Respuestas idempotentes cacheadas; consultas repetidas no pagan doble |
| Opt-out | Tenant puede desactivar IA externa (Doc 33 §7.4) — su costo IA → 0 |
| Reporte | Mensual por tenant en Consola; línea roja visible |

## 7. Storage Lifecycle Policies

| Clase de dato | Política de ciclo de vida | Trazabilidad |
|---|---|---|
| Evidencias (S3) | Caliente 90 días → frío (infrequent access) → archivo a los 12 meses; borrado solo con eliminación de tenant (certificado, RNF-PRV-003) o política del tenant | DC |
| Backups | Retención 35 días con PITR; mensuales 12 meses; cifrados (RNF-SEC-002); ensayo trimestral (RNF-AVL-004) | DC |
| Logs/telemetría | Caliente 30 días; agregados 13 meses | SU (ajustar a costo real) |
| Auditoría de tenant | Vida del tenant + exportación al cierre (RNF-PRV-002) | DC |
| **Auditoría de plataforma** | **PD-RETENCIÓN (AO-6):** propuesta del equipo — mínimo 24 meses online + archivo indefinido (es evidencia legal). **Sigue PD** hasta decisión del Fundador | PD |
| Datos locales móviles | Poda por bucket (RNF-MOB-004); borrado al revocar (RNF-SEC-005) | DC |

## 8. Resolución planificada de SU-FLAGS (AO-6)

**Análisis para decisión del Fundador (sigue SU):** los feature flags de plataforma (ADR-012, categoría 6) tienen costo operativo propio: combinaciones de estado a probar (2^n por flag activo en un flujo), deuda de flags huérfanos, y observabilidad adicional. **Recomendación (NO confirmada):** adoptar flags con política estricta — máximo 10 flags activos simultáneos, cada uno con dueño, fecha de expiración obligatoria y eliminación al estabilizar (≤2 releases); sin flags en rutas críticas de sync. Costo estimado: bajo con disciplina, alto sin ella. Decisión del Fundador en Ola 4 o antes de pilotos. (SU)

## 9. FinOps como disciplina

Revisión semanal de dashboard (fundador), revisión mensual de unit economics contra HV-1…7 (Doc 03), y toda nueva capacidad con costo variable (IA, WhatsApp, almacenamiento) exige estimación de costo por tenant en su FEP (Doc 02 §10 bis) antes de aprobarse. (DC)

## 10. Criterios de aceptación del documento

1. Incluye los 6 elementos de la ampliación obligatoria. ✅
2. Líneas rojas coherentes con RNF-FIN y Doc 33. ✅
3. AO-6 atendida: PD-RETENCIÓN y SU-FLAGS con propuesta — **siguen PD/SU**. ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación (Ola 4, documento 7 de 8) con las ampliaciones obligatorias del Fundador y AO-6 integrada sin resolver PD.*
