# DONEFIXER — 13 · Domain Glossary (Glosario Canónico de Dominio)

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Evidencia:** DC para las reglas de uso del glosario y términos fijados por ADRs aprobados; SU para definiciones que los pilotos podrían refinar; PD donde falta decisión del Fundador.

---

## 1. Objetivo
Garantizar que una palabra signifique una sola cosa en todo DONEFIXER — documentación, UI, API, base de datos, IA y soporte. La ambigüedad terminológica es la fuente más barata de prevenir y más cara de corregir en un producto multi-idioma y multi-segmento (CMMS/EAM/FM/FSM).

## 2. Alcance
Terminología de: estructura organizacional (tenant→unidad), mantenimiento (OT, PM, fallas), activos e inventario, procurement, personas y permisos, IA, sincronización, facturación. Incluye equivalentes EN (código/API) y ES (UI inicial); PT/FR/HT pendientes de PD-4.

## 3. Exclusiones
No define el modelo de datos (doc 14) ni traducciones de contenido legal (doc 37). Los idiomas PT/FR/HT se añaden cuando PD-4 se resuelva.

## 4. Reglas canónicas (DC — heredadas de ADR-010 y gobernanza aprobada)
1. **El código, la API y la base de datos usan el término inglés canónico.** La UI usa el idioma del usuario (ES primero). Nunca mezclar.
2. **Una palabra, un significado.** Si dos conceptos comparten palabra en el habla común ("orden", "solicitud", "cliente"), el glosario los separa con términos distintos.
3. **Los términos de IA y sync usan la definición técnica de este glosario**, no la de marketing.
4. Todo documento nuevo que introduzca un término debe registrarlo aquí antes de aprobarse (FEP/DoR).
5. El glosario tiene dueño: el Fundador. Cambios vía control de cambios.

## 5. Decisiones pendientes (PD)
PD-4 (idiomas): columnas PT/FR/HT · PD-3 (países): variantes regionales del español (p. ej., "repuesto" vs. "refacción" vs. "pieza") — **regla: la UI ofrece variantes regionales configurables por tenant; el glosario fija el término neutro**.

## 6. Dependencias
ADR-010, doc 01/04 (aprobados), AUD-00 §6 (glosario ampliado de auditoría). Alimenta: 14 (modelo de dominio), 09, 11, 43, 44 (traducción), toda la suite.

## 7. Riesgos
| Riesgo | Mitigación |
|---|---|
| Deriva terminológica al crecer la suite | DoR exige registrar términos nuevos; revisión trimestral (doc 02 §11) |
| Colisión CMMS vs FM vs FSM (misma palabra, distinto concepto) | §8 separa explícitamente los pares conflictivos |

---

## 8. Glosario canónico (núcleo)

### 8.1 Estructura organizacional y multi-tenancy

| Término EN (código/API) | Término ES (UI) | Definición única | NO confundir con |
|---|---|---|---|
| **Tenant** | Organización | Cliente de DONEFIXER; límite de aislamiento de datos, facturación y claves | Company, Site |
| **Company** | Empresa | Subdivisión legal opcional dentro de un tenant (grupo corporativo) | Tenant |
| **Program** | Programa | Contrato marco de servicios con un cliente final del tenant (contexto FM) | Project |
| **Property** | Propiedad / Inmueble | Activo inmobiliario gestionado (contexto FM) | Site |
| **Facility** | Instalación | Conjunto físico operado (edificio, planta, campus); en FM equivale a Property | Asset |
| **Site** | Sitio | Subdivisión operativa de una propiedad/empresa: planta, sucursal, edificio | Property (contenedor) |
| **Building** | Edificio | Estructura dentro de un sitio | Site |
| **Zone** | Zona | División interior: piso, ala, área | Location |
| **Unit / Space** | Unidad / Espacio | Espacio arrendable o asignable (contexto FM) | Asset |
| **Location** | Ubicación | Punto genérico georreferenciable donde existe o se ejecuta trabajo (también posición de almacén según contexto declarado) | Zone (división física) |
| **User** | Usuario | Persona con credenciales en la plataforma (cualquier tenant) | Account |
| **Account** | Cuenta | Identidad global de autenticación: **una cuenta → N membresías** (DC, AUD-00 §7) | User |
| **Membership** | Membresía | Vínculo usuario↔tenant con su rol base | Profile |
| **Profile** | Perfil | Contexto de una membresía: sitio, equipo, función — permisos contextuales | Role |
| **Role** | Rol | Conjunto nombrado de permisos (RBAC) | Permission |
| **Permission** | Permiso | Autorización atómica sobre un recurso/acción (puede ser ABAC: por sitio, programa, proveedor) | Role |
| **Service Account** | Cuenta de servicio | Identidad API no humana (integraciones, agentes IA) con RBAC propio | User |
| **Vendor / Contractor** | Proveedor / Contratista | Ejecutor externo de trabajo con contrato y SLA | Supplier (sinónimo aceptado; se usa **Vendor** en código) |
| **Requester** | Solicitante | Persona que reporta una necesidad; **no es asiento de pago** (DC doc 03) | Customer |
| **Occupant** | Ocupante / Inquilino | Requester en contexto FM (habita o usa el espacio) | — |
| **Customer (of tenant)** | Cliente (del tenant) | Cliente final del tenant en contexto FM/FSM | Tenant (cliente de DONEFIXER) |

### 8.2 Trabajo de mantenimiento

| Término EN | Término ES | Definición única | NO confundir con |
|---|---|---|---|
| **Service Request (SR)** | Solicitud de servicio | Demanda registrada, **aún no autorizada** | Work Order |
| **Work Order (WO)** | Orden de trabajo (OT) | Trabajo **autorizado** y ejecutable, con estados, costos y evidencias | Request, Project |
| **Emergency WO** | OT de emergencia | OT con SLA de minutos/horas y despacho inmediato | Priority alta (atributo) |
| **Project** | Proyecto | Conjunto planificado de OTs con presupuesto y fechas | PM (recurrente), Program |
| **Task** | Tarea | Paso dentro de una OT | Procedure (plantilla) |
| **Procedure** | Procedimiento | Plantilla reutilizable de pasos/checklist con evidencias requeridas | Task (instancia) |
| **Checklist** | Lista de verificación | Conjunto de ítems verificables (en procedimiento o inspección) | Inspection |
| **Inspection** | Inspección | Evaluación puntual de condición/cumplimiento; genera hallazgos | Round |
| **Round** | Ronda | Recorrido programado de inspecciones/lecturas en ruta | Inspection (puntual) |
| **Finding** | Hallazgo | Desviación detectada en inspección/ronda; puede generar OT | Incident |
| **Incident** | Incidente | Evento de seguridad/EHS vinculado a trabajo o activo | Failure (del activo) |
| **Preventive Maintenance (PM) Plan** | Plan de mantenimiento preventivo | Definición recurrente con triggers: tiempo / medidor / evento / condición / predicción | Route, Schedule |
| **Trigger** | Disparador | Condición que genera OTs desde un PM | Schedule (calendario fijo) |
| **Meter** | Medidor | Contador de uso del activo (horas, km, ciclos, unidades producidas) | Sensor (tiempo real) |
| **Meter Reading** | Lectura de medidor | Valor registrado de un medidor; alimenta triggers | Sensor reading (IoT) |
| **Sensor** | Sensor | Fuente de datos de condición en tiempo casi real (IoT, Fase 4) | Meter (manual/periódico) |
| **Failure Code (Problem/Cause/Action)** | Código de falla (problema/causa/acción) | Taxonomía por tenant para RCA: qué se observó, por qué ocurrió, qué se hizo | Incident |
| **Downtime** | Tiempo de inactividad | Período en que el activo no está disponible; planificado o no | Idle (sin programar) |
| **Backlog** | Trabajo pendiente | Horas de trabajo abierto / capacidad semanal | Queue (técnica) |
| **SLA** | Acuerdo de nivel de servicio | Compromiso de tiempos por prioridad/estado (respuesta, resolución) | OLA (interno) |
| **Approval** | Aprobación | Decisión registrada que habilita una transición (OT, compra, factura) | Review (sin efecto) |
| **Work Permit** | Permiso de trabajo | Autorización de seguridad previa (trabajo en caliente, alturas, LOTO) | Approval (genérica) |
| **LOTO (Lockout-Tagout)** | Bloqueo y etiquetado | Procedimiento de aislamiento de energías | Work Permit (lo contiene) |
| **Evidence** | Evidencia | Foto, video, audio, firma, lectura o documento que prueba el trabajo; **aditiva, con hash e inmutable tras cierre** (DC) | Attachment (genérico) |
| **Signature (capture)** | Firma (capturada) | Firma manuscrita digital ligada a sesión autenticada + hash de evidencia | Firma electrónica avanzada (Fase 5, 21 CFR Part 11) |

### 8.3 Activos e inventario

| Término EN | Término ES | Definición única | NO confundir con |
|---|---|---|---|
| **Asset** | Activo | Equipo, sistema o estructura mantenible; jerarquía recursiva (planta→línea→equipo→componente, ltree) | Property, Item |
| **Asset Category** | Categoría de activo | Clasificación con especificaciones y checklists heredables | Failure code |
| **Spare Part** | Repuesto | Ítem de inventario consumible en mantenimiento (variante regional configurable: refacción/pieza — PD-3) | Inventory Item (más amplio) |
| **Inventory Item** | Ítem de inventario | Cualquier bien almacenable (repuesto, consumible, herramienta) | Asset (se mantiene, no se consume) |
| **Warehouse / Stock Location** | Almacén / Ubicación de stock | Lugar físico de existencias por sitio | Site |
| **Stock Movement** | Movimiento de inventario | Entrada/salida/transferencia/ajuste con costo; **operaciones delta, nunca `set`** (DC AUD-00 §4) | Adjustment (subtipo) |
| **Reorder Point** | Punto de reorden | Nivel de stock que dispara necesidad de compra | Safety stock (colchón) |
| **TCO (Total Cost of Ownership)** | Costo total de propiedad | Suma de costos del activo en su ciclo de vida (adquisición, operación, mantenimiento, disposición) | Costo de OT (parcial) |

### 8.4 Procurement y finanzas del tenant

| Término EN | Término ES | Definición única | NO confundir con |
|---|---|---|---|
| **Purchase Requisition (PR)** | Requisición de compra | Necesidad interna de comprar, pendiente de aprobación | Purchase Order |
| **Purchase Order (PO)** | Orden de compra (OC) | Compromiso formal de compra a un proveedor | Work Order |
| **Receipt** | Recepción | Registro de bienes recibidos contra una OC | Invoice |
| **Return** | Devolución | Retorno de bienes al proveedor con motivo | Adjustment |
| **Invoice (AP)** | Factura (por pagar) | Cobro del proveedor → validación/conciliación (tres vías: OC/recepción/factura) | Invoice (AR) |
| **Invoice (AR)** | Factura (por cobrar) | El tenant cobra a su cliente por servicios (FSM, Fase 3+) | Billing (SaaS) |
| **SaaS Billing** | Facturación SaaS | DONEFIXER cobra la suscripción al tenant (doc 03) | Invoice (AP/AR) |
| **Contract** | Contrato | Acuerdo con proveedor (alcance, SLA, tarifas, vigencia) | Warranty |
| **Warranty** | Garantía | Cobertura del fabricante/instalador sobre un activo, con vigencia y condiciones | Contract |
| **Labor Cost** | Costo de mano de obra | Horas × tarifa por rol/perfil en una OT | Rate (la tarifa) |

### 8.5 Plataforma, IA y sincronización

| Término EN | Término ES | Definición única | NO confundir con |
|---|---|---|---|
| **Feature Flag** | Indicador de funcionalidad | Interruptor por tenant/segmento/% para activar capacidades (SU-FLAGS: propios vs. externos, ADR-012 §6) | Entitlement |
| **Entitlement** | Derecho de plan | Capacidad incluida en el plan comercial del tenant | Feature flag (técnico) |
| **Copilot** | Copiloto | IA asistiva que responde/sugiere con fuentes; nunca actúa sola en riesgo medio/alto (DC doc 33) | Agent |
| **Agent** | Agente | IA que ejecuta flujos con herramientas permitidas, aprobación humana según riesgo y auditoría por decisión (DC) | Copilot |
| **Decision Audit Trail** | Registro de decisión de IA | Quién/qué/cuándo/por qué de cada acción IA; inmutable | Log técnico |
| **Outbox** | Bandeja de salida | Cola durable local de operaciones pendientes de sincronizar (misma transacción que el dato, DC) | Queue |
| **Sync Bucket** | Segmento de sincronización | Subconjunto del tenant que un dispositivo sincroniza (reglas declarativas) | Shard |
| **Tombstone** | Marca de borrado | Registro de eliminación que sobrevive a ediciones concurrentes; "los borrados ganan" (DC) | Soft delete (mecanismo) |
| **HLC (Hybrid Logical Clock)** | Reloj lógico híbrido | Ordenamiento causal cliente/servidor tolerante a relojes mal configurados | Timestamp (solo) |
| **Conflict Queue** | Cola de conflictos | Resolución humana de conflictos críticos; nunca LWW silencioso en campos críticos (DC) | Error |
| **Platform Administration Console** | Consola de administración de plataforma | Plano plataforma DONEFIXER (ADR-012, principio permanente) | Tenant Administration |
| **Tenant Administration** | Administración del tenant | Plano tenant: el admin del cliente gestiona su organización | Console (plataforma) |

## 9. Pares conflictivos resueltos explícitamente (anti-ambigüedad)

1. **Orden**: "Orden de trabajo" (WO) ≠ "Orden de compra" (PO) — en UI siempre con su calificador.
2. **Cliente**: "Cliente de DONEFIXER" = Tenant · "Cliente del tenant" = Customer — prohibido usar "cliente" a secas en documentos de plataforma.
3. **Solicitud**: Request (pre-autorización) ≠ Requisition (compra) — ambas "solicitud" en español coloquial; la UI usa "solicitud de servicio" y "requisición de compra" completas.
4. **Factura**: AP (pagar) ≠ AR (cobrar) ≠ Billing SaaS (suscripción) — tres conceptos, tres términos.
5. **Medidor vs. Sensor**: medidor = lectura periódica/manual; sensor = dato continuo IoT. Los triggers PM usan medidores (Fase 1); condición usa sensores (Fase 4).
6. **Inventario financiero**: los movimientos son deltas con costo; el "ajuste" es un movimiento, no una edición del saldo (prohibido `set`, DC).

## 10. Criterios de aceptación de este documento
1. Todo término tiene EN/ES, definición única y "no confundir con". ✅
2. Pares conflictivos con resolución explícita. ✅
3. Reglas de uso DC y dueño del glosario. ✅

## 11. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador; columnas PT/FR/HT cuando PD-4 se resuelva; variantes regionales ES cuando PD-3 se resuelva.

## 12. Referencias cruzadas
Depende de: ADR-010, 01, 04, AUD-00 §6. Alimenta: 14, 09, 11, 43, 44 (traducción automática), 33 (términos IA), 27 (términos sync).

## 13. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). ~70 términos canónicos EN/ES con anti-ambigüedad; 6 pares conflictivos resueltos; reglas DC de uso; PT/FR/HT y variantes regionales pendientes de PD-4/PD-3 |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
