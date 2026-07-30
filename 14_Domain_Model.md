# DONEFIXER — 14 · Domain Model (Modelo de Dominio)

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Evidencia:** DC para decisiones de ADRs aprobados y el núcleo de dominio validado por la investigación; SU para extensiones cuya forma final se validará en pilotos; PD donde falta decisión.
> **Alcance explícito:** modelo de dominio **conceptual** (entidades, relaciones, invariantes, máquinas de estado). **NO es DDL ni esquema físico** — la estructura física pertenece al doc 25 (Data Architecture) y solo se escribe tras los gates.

---

## 1. Objetivo
Definir el modelo de dominio canónico que gobernará la base de datos, la API, la sincronización offline y la IA durante 10 años, evitando la migración más costosa del sector (rehacer el dominio al subir de CMMS a EAM/FM — doc 04).

## 2. Alcance
Todos los módulos de las tres capas de madurez (CMMS → EAM → FM), aunque su implementación sea por fases: el dominio se define completo **ahora** y se implementa **por fases** — esta es la decisión que protege la evolución a 10 años (DC de diseño, doc 01).

## 3. Exclusiones
No incluye DDL, índices, tipos de columna físicos (doc 25); no incluye entidades de facturación SaaS internas de DONEFIXER más allá de su frontera con el tenant (spec billing, doc 43).

## 4. Decisiones confirmadas (DC) que gobiernan el modelo
1. **Campos de plataforma en toda entidad de negocio:** `id` (UUIDv7), `tenant_id`, `version` (control optimista + If-Match en sync), `created_at/by`, `updated_at/by`, `deleted_at` (tombstone; "los borrados ganan"), `sync_metadata`. (ADR-001, ADR-002-reabierto, AUD-00 §4.)
2. **Autoridad backend con lógica local provisional** (ADR-011 v1.1): el dominio define invariantes que el servidor re-valida siempre.
3. **Jerarquía de activos recursiva** con camino materializado (ltree en la implementación física).
4. **Códigos de falla problema/causa/acción** como catálogo por tenant con valores semilla de plataforma.
5. **Medidores de primera clase**; sensores IoT como extensión de fase 4.
6. **Evidencias aditivas e inmutables tras cierre** (hash de contenido); nunca se sobrescriben.
7. **Inventario por deltas** (prohibido `set` sobre saldos).
8. **Máquina de estados explícita** para OT (§7.2); los estados no son texto libre.
9. **Tres conceptos de factura separados** (AP / AR / SaaS Billing — doc 13).
10. **Una cuenta → N membresías → perfiles contextuales** (AUD-00 §7, §9.1).

## 5. Decisiones pendientes (PD)
PD-3 (variantes regionales de catálogos); PD-RETENCIÓN (afecta `deleted_at` y purga); PD-AC-1 (entidades de consola); SU-FLAGS (entidad feature flag propia o externa).

## 6. Supuestos (SU)
La granularidad de Project, Warranty y Service Billing (AR) se validará en pilotos de Fase 2–3; las entidades IoT son provisionales hasta Fase 4.

## 7. Modelo

### 7.1 Mapa de contextos delimitados (bounded contexts)

```
IDENTIDAD Y TENANCY          TRABAJO                      ACTIVOS
Account, User,               ServiceRequest,             AssetCategory,
Membership, Profile,   ──►   WorkOrder, Task,      ──►   Asset (jerarquía),
Role, Permission             Evidence, Approval,         Meter, MeterReading,
                             WorkPermit, Incident        FailureCode, Sensor(F4),
                                                         Warranty
PLANIFICACIÓN                INVENTARIO                   PROCUREMENT
PMPlan, Trigger,             InventoryItem,              Contract, Vendor,
Schedule, Assignment,        Warehouse, StockLevel,      PurchaseRequisition,
Round, Inspection,           StockMovement (delta),      PurchaseOrder, Receipt,
Finding                      ReorderPoint                Return, Invoice(AP),
                                                        ServiceBilling(AR)(F3)
GOBIERNO                     PLATAFORMA (plano DONEFIXER)
AuditEvent (inmutable),      Plan, Entitlement,
Notification, SLA,           FeatureFlag(SU), Consumption,
Escalation                   PlatformAudit (ADR-012)
```

**Regla de frontera (DC):** los contextos se referencian por ID y eventos de dominio, nunca por joins trans-contexto en la implementación de servicios futuros — esto preserva la extracción a servicios (ADR-005).

### 7.2 Work Order — la entidad central

**Máquina de estados (DC):**

```
solicitada → aprobada → planificada → asignada → en_progreso
                                            ↘ en_espera_repuesto ↗
                                            ↘ en_espera_aprobacion ↗
en_progreso → completada → verificada → cerrada
(cualquier estado previo a completada) → cancelada (con motivo)
```

| Estado | Quién transiciona (matriz por rol — detalle en doc 19) | Invariante del servidor (DC ADR-011 v1.1) |
|---|---|---|
| →aprobada | supervisor, gerente, planificador | La SR origen existe y no está duplicada |
| →asignada | supervisor, planificador (sugerencia IA = riesgo medio, humano confirma) | Asignado tiene membresía activa y habilidad requerida si el procedimiento la exige |
| →en_progreso | técnico asignado | OT asignada al ejecutor o a su equipo |
| →en_espera_* | técnico, supervisor | Motivo obligatorio; SLA se pausa según política del tenant |
| →completada | técnico | Evidencias requeridas por el procedimiento presentes (validación local provisional + re-validación servidor) |
| →verificada | supervisor (si el tenant lo exige por tipo de OT) | Verificador ≠ ejecutor (segregación) |
| →cerrada | sistema o supervisor | Acumulación final de costos; alimenta KPIs |
| →cancelada | supervisor+ | Motivo; evidencias conservadas |

**Atributos de dominio:** tipo (correctiva, preventiva, emergencia, inspección-derivada, proyecto), prioridad, activo, ubicación, SR origen, PM origen (si aplica), asignados, procedimiento, tareas, repuestos planificados/consumidos (deltas), tiempos (estimado/real por persona), costos (labor, repuestos, externo), códigos de falla (problema/causa/acción al cerrar correctivas), downtime asociado, SLA vinculado, evidencias, firma(s).

**Invariante de integridad (DC):** una OT cerrada alimenta exactamente una vez los KPIs y el historial del activo (idempotencia por `operation_id` — el sync nunca duplica efectos).

### 7.3 Asset (jerarquía)

`Asset`: padre recursivo (planta→línea→equipo→componente), categoría, ubicación, estado operativo, medidores asociados, documentos, garantías, fecha puesta en servicio, costo de adquisición, vida útil estimada. **Reglas:** la jerarquía es un árbol (sin ciclos — invariante servidor); mover un activo actualiza su camino materializado; desactivar ≠ borrar (los activos con historial se desactivan, nunca se eliminan — preserva KPIs históricos).

### 7.4 PM Plan y triggers

`PMPlan`: activo(s) o categoría, procedimiento, triggers (`time`: cada N días/semanas/meses · `meter`: cada N unidades · `event`: ante evento de dominio · `condition`: F4 · `prediction`: F4), ventana de cumplimiento (PM compliance = completado dentro del ±10% del intervalo — SU benchmark doc 04 §5), próxima generación calculada. **Invariante:** un trigger no genera OT duplicada si ya existe una abierta del mismo plan para el mismo activo (deduplicación por ventana).

### 7.5 Inventario y procurement

`StockLevel` es **derivado** de `StockMovement` (deltas con costo y referencia a OT/PO/recepción). `Invoice(AP)`: conciliación tres vías (PO ↔ Receipt ↔ Invoice); discrepancias fuera de tolerancia → cola de resolución humana (el agente IA valida, el humano aprueba — riesgo ALTO, DC doc 33). `Contract`: tarifas y SLA del proveedor; `Warranty`: vigencia por activo (una OT en garantía marca el costo como reclamable).

### 7.6 Identidad (resumen — detalle en doc 19/26)

`Account` (global) → `Membership` (tenant) → `Profile` (contexto: sitio/equipo/función) → permisos efectivos = rol + ABAC contextual. **Invariante:** ningún permiso se concede fuera de una membresía; los Service Accounts (incluidos agentes IA) tienen su propio RBAC y nunca impersonan usuarios sin registro.

### 7.7 Eventos de dominio (semilla — detalle en doc 30)

`sr.created · sr.triaged · wo.approved · wo.assigned · wo.status_changed · wo.completed · wo.closed · pm.generated · meter.reading_recorded · stock.moved · reorder.triggered · invoice.flagged · finding.created · evidence.attached · sla.breached`. Todo evento: esquema versionado, `tenant_id`, `operation_id`, timestamp servidor (DC ADR-009).

## 8. Matriz de conflicto de sync por entidad (resumen — autoridad en doc 27)

| Entidad/campo | Estrategia (DC de AUD-00 §4) |
|---|---|
| WO.status, asignación | Servidor autoritativo + máquina de estados; conflicto → cola humana |
| Evidencias, notas, fotos | Aditivas (conjunto CRDT-like); nunca sobrescribir |
| Stock, lecturas de medidor | Deltas (`increment_by`) |
| Catálogos del tenant | LWW por campo con versión + aviso |
| Borrados | Tombstones, retención PD |
| Costos financieros cerrados | Inmutables; correcciones vía contra-asiento |

## 9. Métricas del modelo
% OTs cerradas con códigos de falla completos (objetivo ≥70% en clientes maduros, SU); % movimientos de stock trazables a OT/PO (100% requerido); profundidad media de jerarquía de activos por tenant (salud del modelo); % entidades con campos de plataforma completos (100% requerido, test CI).

## 10. Criterios de aceptación de este documento
1. Contextos delimitados con regla de frontera. ✅ 2. Máquina de estados de OT con matriz por rol e invariantes. ✅ 3. Todas las decisiones DC trazables a ADRs aprobados. ✅ 4. Sin DDL ni diseño físico. ✅

## 11. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador; refinamiento de contextos EAM/FM tras pilotos (v1.1).

## 12. Referencias cruzadas
Depende de: 13 (glosario), ADR-001/002/005/009/011, AUD-00 §4–6. Alimenta: 25 (data architecture), 26 (multi-tenant), 27 (sync), 09/11 (requisitos), 43 (specs).

## 13. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). Contextos delimitados, máquina de estados de OT con invariantes, jerarquía de activos, PM/triggers, inventario por deltas, eventos semilla, matriz de conflicto |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
