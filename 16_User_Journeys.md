# DONEFIXER — 16 · User Journeys

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Evidencia:** todos los journeys son **SU** (hipótesis de diseño derivadas de doc 04 y doc 15) hasta su validación con pilotos; los pasos marcados DC derivan de decisiones aprobadas (ADR-011, ADR-012, docs 01–04). Cada journey declara su persona, canal, riesgos y criterios de aceptación medibles.

---

## 1. Objetivo
Describir los flujos de extremo a extremo que el producto debe servir, con los puntos de fricción que la investigación identificó y las métricas que dirán si el journey funciona. Los RF de los docs 09/11 nacerán de estos journeys (trazabilidad RF↔journey al 100%, gate G2).

## 2. Alcance
9 journeys críticos de Fases 1–2 (operación CMMS núcleo + primera capa EAM/procurement). Los journeys de Fase 3+ (FM multi-portafolio, IoT) se documentan en sus specs de módulo (doc 43).

## 3. Exclusiones
No incluye journeys de soporte interno DONEFIXER (ADR-012), ni journeys de verticales reguladas, ni flujos de EE. UU. (expansión, doc 01 §13).

## 4. Decisiones confirmadas (DC) que gobiernan los journeys
Offline-first ciclo completo (doc 01); autoridad del backend con lógica local provisional (ADR-011 v1.1); solicitantes gratuitos (doc 03); IA gobernada con aprobación humana en riesgo medio/alto (AUD-00 §11); usuario primario = técnico (doc 15).

## 5. Decisiones pendientes (PD) que afectan journeys
PD-3 (países): el canal WhatsApp puede variar por país (costo Meta, H-25). PD-4 (idiomas): J-1 y J-4 multilingües. N-2: afecta la experiencia de sync en J-2/J-3 (modalidad PowerSync). N-9: afecta J-9 (soporte).

## 6. Supuestos (SU) globales
Los tiempos objetivo son hipótesis a validar (HV en doc 03 §16); las fricciones citadas provienen de reviews públicos de competidores (doc 04 §8, DC a su fecha).

## 7. Dependencias
Doc 15 (personas), doc 04 (evidencia de fricciones), ADR-011 (canales). Alimenta: 17 (blueprints), 09 (PRD), 11 (RF), 43 (specs), 40 (UX).

## 8. Riesgos
| Riesgo | Mitigación |
|---|---|
| Journeys diseñados desde la oficina, no desde el piso | Validación en pilotos con observación directa; métricas por paso |
| Métricas de tiempo que premian velocidad sobre calidad del dato | Cada journey mide también calidad (evidencia completa, rechazos de sync) |

---

## 9. Los journeys

### J-1 · "Reportar una falla" — P-R1 (solicitante) · SU

**Canal:** WhatsApp / portal PWA / QR en el activo o sitio. **Objetivo de diseño: ≤60 segundos desde que ve la falla hasta confirmación.**

| Paso | Acción | Sistema | Fricción evitada (evidencia doc 04) |
|---|---|---|---|
| 1 | Escanea QR o abre WhatsApp del número de mantenimiento | Identifica sitio/activo automáticamente | Formularios largos de portales tradicionales |
| 2 | Describe con texto, **voz o foto** (elige el más rápido) | Voz→texto; adjunta evidencia | "No sabía qué categoría elegir" |
| 3 | Recibe confirmación inmediata con folio | Triage IA: prioridad sugerida, activo detectado, duplicados detectados (riesgo medio: humano confirma en J-4) | "Reporté y nadie confirmó" |
| 4 | Consulta estado en cualquier momento por el mismo canal | Notificaciones de cambio de estado | "Nunca supe qué pasó" (queja nº 1 documentada) |

**Métricas:** tiempo mediano de reporte (<60 s); % solicitudes con estado consultado sin llamada (≥90%, hipótesis HV-5); % triage IA aceptado sin cambio por el humano.
**Criterios de aceptación:** funciona sin crear cuenta (DC: solicitantes no pagan); el original del mensaje se conserva aunque se traduzca (ADR-010/i18n); duplicados detectados se enlazan, no se crean dos OTs.

### J-2 · "Ejecutar una OT en campo, sin internet" — P-T1 (técnico) · SU con pasos DC

**Canal:** app nativa. **Este journey es la prueba de fuego del producto (DC: offline-first).**

| Paso | Acción | Sistema | Punto crítico |
|---|---|---|---|
| 1 | Recibe OT asignada (push o al abrir la app) | OT + procedimiento + repuestos + historial del activo **ya descargados en su bucket de sync** (DC: reglas de sync declarativas) | El trabajo llega al técnico, no al revés |
| 2 | Llega al sitio **sin señal**; escanea QR del activo | Confirma activo correcto; abre OT | QR evita errores de activo |
| 3 | Ejecuta con checklist; adjunta foto/voz/firma; registra repuestos y tiempo | **Todo local, decisiones provisionales** (DC: ADR-011 v1.1); estado visible "pendiente de sincronizar" | Nada bloquea el trabajo |
| 4 | Cierra la OT con evidencia completa | Validaciones locales (campos requeridos, foto obligatoria si el procedimiento la exige) | Sin evidencia no hay cierre provisional |
| 5 | Sale de la zona sin señal (minutos u horas después) | **Sync automático en segundo plano**: push de operaciones; servidor **re-valida** (autoridad backend, DC); resultado visible: confirmado / ajustado / rechazado con motivo | Si hay rechazo (p. ej., repuesto ya consumido por otro), entra a cola de resolución humana — **nunca LWW silencioso** (DC, AUD-00 §4) |

**Métricas:** éxito de sync >99.9%/día (SLO interno); % OTs cerradas con evidencia completa (≥80%, HV); toques medios para cerrar OT estándar (≤15, SU a calibrar); crash-free sessions >99.5%.
**Criterios de aceptación:** el técnico puede completar pasos 1–4 con el teléfono en modo avión (prueba de aceptación literal, doc 47); ninguna pérdida de datos tras 24 h offline (test de chaos, doc 47/60); el estado de sincronización es siempre visible (AUD-00 §12).

### J-3 · "Semana de mantenimiento preventivo" — P-S1 (supervisor) + P-T1 · SU

| Paso | Acción | Sistema |
|---|---|---|
| 1 | El lunes, revisa el plan semanal | OTs de PM generadas automáticamente por triggers (tiempo/medidor); balanceo de carga sugerido por IA, **humano confirma** (DC: riesgo medio) |
| 2 | Ajusta asignaciones arrastrando en calendario | Conflictos de disponibilidad/habilidad marcados |
| 3 | Los técnicos ejecutan (J-2) | Progreso visible en tiempo real cuando hay red |
| 4 | El viernes, revisa cumplimiento | PM compliance calculado automático; PMs vencidos escalados (doc 50) |

**Métricas:** PM compliance ≥85% sostenido en clientes (HV); tiempo de planificación semanal del supervisor (−50% vs. su proceso actual, SU).
**Criterios de aceptación:** ningún PM se genera duplicado; los triggers por medidor usan lecturas reales; el ajuste manual del supervisor prevalece sobre la sugerencia IA (y se registra).

### J-4 · "De la solicitud a la OT asignada" — P-S1/P-D1 · SU

| Paso | Acción | Sistema |
|---|---|---|
| 1 | Bandeja de solicitudes triadas por IA (prioridad/activo/duplicados sugeridos) | El humano revisa y confirma o corrige (DC: riesgo medio) |
| 2 | Aprueba → se crea OT con contexto completo | Estados iniciales: aprobada → planificada → asignada (DC: máquina de estados) |
| 3 | Asigna por habilidad/proximidad (sugerencia IA) o manual | El técnico recibe J-2 |

**Métricas:** tiempo solicitud→asignación (<2 h laborables para prioridad alta, SU); % correcciones al triage IA (métrica de calidad del modelo, doc 33).

### J-5 · "Repuesto que falta" — P-T1 + P-S1 + inventario · SU (Fase 2)

| Paso | Acción | Sistema |
|---|---|---|
| 1 | En campo, el técnico marca "repuesto no disponible" | OT pasa a estado "en espera por repuesto" (DC: máquina de estados), visible para todos |
| 2 | Se genera necesidad de compra/stock | Requisición automática o alerta de reorden (punto de reorden) |
| 3 | Llega el repuesto, se recibe | Notificación al técnico; la OT se reactiva con prioridad |
| 4 | Se cierra la OT | Consumo descontado de stock con **operación delta** (DC: nunca `set` — AUD-00 §4) |

**Métricas:** % OTs en espera >5 días; exactitud de inventario (físico vs. sistema, ≥95% SU).
**Criterios de aceptación:** el consumo concurrente de dos técnicos offline se resuelve por deltas sin lost-updates; discrepancia financiera va a resolución humana.

### J-6 · "Factura de proveedor sin sorpresas" — P-V1 + P-F1 · SU (Fase 2)

| Paso | Acción | Sistema |
|---|---|---|
| 1 | El proveedor cierra su OT y sube factura por el portal | OCR extrae datos; agente IA **valida** contra contrato/tarifas/OT (DC: riesgo ALTO → aprobación humana obligatoria, límites monetarios, doc 33) |
| 2 | Finanzas recibe factura pre-validada con discrepancias marcadas | Aprueba o rechaza con motivo; el proveedor ve el estado |
| 3 | Pago y archivo | Trazabilidad completa OT→factura→pago |

**Métricas:** días factura→aprobación; % facturas con discrepancia detectada antes de pago; tiempo de conciliación mensual.
**Criterios de aceptación:** el agente nunca aprueba solo (prohibición arquitectónica, doc 33); toda decisión registrada con auditoría por decisión (DC, ADR-012 §3).

### J-7 · "Nuevo cliente operativo en una semana" — P-C1 + P-M1 · SU

| Paso | Acción | Sistema |
|---|---|---|
| 1 | Crea su organización; importa activos y usuarios desde **Excel/CSV** (doc 63) | Mapeo asistido de columnas; errores claros por fila |
| 2 | Configura sitios, catálogos (plantillas por industria) y primer PM | Plantillas precargadas; nada obligatorio que bloquee el primer valor |
| 3 | Invita técnicos; ellos instalan y usan en <10 min | Onboarding en app de 3 pantallas |
| 4 | Primera OT real ejecutada y cerrada | "Tiempo al primer valor" medido |

**Métricas:** tiempo al primer valor (<1 día SU; objetivo <7 días para operación completa — meta, no promesa, AUD-00 H-23); % importaciones sin intervención de soporte.
**Criterios de aceptación:** un cliente S1 puede llegar a la primera OT cerrada sin contactar soporte (HV-6).

### J-8 · "Reporte mensual que se escribe solo" — P-M1/P-X1 · SU (Fase 3)

| Paso | Acción | Sistema |
|---|---|---|
| 1 | Fin de mes: el reporte ya está generado | KPIs automáticos (OLAP/rollups, ADR-006); agente IA redacta resumen ejecutivo con **fuentes citadas** (DC: el copiloto cita o se abstiene, doc 33) |
| 2 | El gerente revisa, ajusta y comparte | Exportación PDF/Excel; programación de envío |

**Métricas:** tiempo de elaboración del reporte mensual (de días a <30 min, HV); % cifras del resumen IA verificadas correctas (golden-set, doc 33).

### J-9 · "Algo salió mal: soporte sin fricción" — cualquier persona · SU

| Paso | Acción | Sistema |
|---|---|---|
| 1 | Reporta problema desde la app/web (contexto técnico adjunto automáticamente) | Ticket con dispositivo, versión, tenant, último sync |
| 2 | FAQ asistido responde lo conocido (IA con fuentes; nunca compromisos — N-9/doc 33) | Lo no resuelto pasa a humano con prioridad |
| 3 | Seguimiento hasta cierre | Estado visible; postmortem interno si fue incidente (doc 59) |

**Métricas:** tiempo de primera respuesta dentro del horario declarado (N-9); % resuelto por FAQ sin humano (objetivo 40–60%, SU).

---

## 9 bis. Flujos alternativos, excepciones y estados offline por journey (ampliación exigida por aprobación Ola 2, instrucción 8)

> Estructura por journey: flujo principal (ya descrito en §9) · **FA** flujos alternativos · **EX** excepciones · **OFF** comportamiento offline/sync · **R** riesgos · **CA** criterios de aceptación (los de §9 más los nuevos aquí).

### J-1 · Reportar una falla
- **FA-1:** reporte por voz sin texto (el sistema transcribe y pide confirmación con resumen en una frase).
- **FA-2:** reporte de emergencia (el solicitante marca "urgente") → prioridad máxima sugerida y notificación inmediata a supervisor (DC máquina de prioridades, doc 50 futuro).
- **FA-3:** reporte duplicado → el sistema enlaza a la solicitud existente y notifica al nuevo solicitante el folio original.
- **EX-1:** foto ilegible o sin contexto suficiente → solicitud entra con etiqueta "requiere aclaración"; el triage humano la completa.
- **EX-2:** WhatsApp API caída → portal/QR/SMS operativos; mensaje al usuario por canal alterno (SB-1).
- **OFF:** el solicitante sin datos usa SMS fallback (SU canal, H-25); el QR precarga el sitio aunque la foto se suba después (metadatos primero, DC RF-SYNC-007).
- **R:** triage IA equivocado con consecuencia de seguridad → mitigación: prioridad conservadora por defecto y confirmación humana (DC doc 33).
- **CA adicional:** en EX-1 la solicitud nunca se rechaza silenciosamente; en FA-3 nunca se crean dos OTs del mismo fallo.

### J-2 · Ejecutar OT offline (prueba de fuego)
- **FA-1:** OT requiere segundo técnico no asignado → el técnico solicita apoyo desde la app (decisión del supervisor).
- **FA-2:** procedimiento no aplica a la condición encontrada → desviación documentada con foto y motivo; el supervisor la revisa en verificación.
- **EX-1:** conflicto de sync en el cierre (otro técnico modificó la OT) → la OT va a cola de resolución humana con ambos valores; **nunca se descarta trabajo** (DC RF-SYNC-004).
- **EX-2:** repuesto consumido no existía en stock según servidor → delta se registra, discrepancia a cola de inventario (nunca bloquea el cierre provisional).
- **EX-3:** app muere a mitad de captura → el outbox y la evidencia local sobreviven (transacción única, DC RF-SYNC-001); al reabrir, continúa donde quedó.
- **OFF:** es el estado normal del journey (pasos 1–4 en modo avión, prueba literal doc 47); estados visibles: pendiente → confirmado/ajustado/rechazado con motivo.
- **R:** evidencia falsa (foto de archivo) → hash + timestamp servidor + metadatos EXIF revisables; geocerca opcional por tenant (SU).
- **CA adicional:** EX-1 y EX-3 verificados por tests de chaos en CI (RNF-SYNC-003); tras 7 días offline, convergencia completa sin intervención de soporte.

### J-3 · Semana de PM
- **FA-1:** técnico de baja → reasignación masiva con conflicto de habilidades marcado.
- **EX-1:** lectura de medidor anómala (10× el promedio) → validación: se acepta pero se marca para confirmación (regla de cordura, SU umbrales por categoría).
- **OFF:** las OT de PM ya generadas están en el bucket del técnico; la generación de nuevas OT es servidor-side (no requiere red del técnico).
- **R:** tormenta de OTs generadas en fecha de cierre → balanceo por ventana de cumplimiento (±10%, DC RF-PM-003).

### J-4 · Solicitud → OT asignada
- **FA-1:** supervisor corrige el activo sugerido por IA → corrección registrada como dato de evaluación del modelo (DC doc 33).
- **EX-1:** solicitud sin activo identificable → OT "por investigar" asignada a técnico para diagnóstico (tipo de OT específico, doc 14).
- **OFF:** la aprobación puede quedar en outbox del supervisor (P-S1 offline); el técnico recibe la OT al sincronizar.
- **CA adicional:** ninguna asignación automática se ejecuta sin la regla del tenant que la habilite + auditoría (DC doc 19 §9.3).

### J-5 · Repuesto que falta
- **FA-1:** repuesto disponible en otro sitio → transferencia inter-sitio con movimientos delta en ambos almacenes.
- **EX-1:** dos técnicos offline consumen el último repuesto → deltas convergen a stock negativo detectado → alerta y cola de resolución (nunca edición silenciosa del saldo, DC RF-INV-001).
- **OFF:** el consumo se registra local como delta provisional; la validación de stock es servidor-side al sincronizar.
- **CA adicional:** EX-1 reproducido en test de concurrencia (doc 47).

### J-6 · Factura sin sorpresas
- **FA-1:** factura parcial (trabajo en curso) → conciliación parcial marcada.
- **EX-1:** OCR con confianza baja → campos marcados para revisión humana (nunca se "adivina" un importe, DC doc 33).
- **EX-2:** discrepancia precio vs. contrato fuera de tolerancia → cola de resolución con el proveedor notificado del motivo.
- **OFF:** no aplica (flujo de oficina).
- **CA adicional:** el agente validador tiene prohibido aprobar — verificado por test de permisos (DC doc 19 §11).

### J-7 · Onboarding en una semana
- **FA-1:** el cliente no tiene datos digitales → plantilla en papel asistida + captura mínima (activos críticos primero, SU).
- **EX-1:** Excel con columnas irreconocibles → mapeo manual asistido; nunca importación parcial silenciosa (DC SB-3).
- **OFF:** la importación requiere red; la app del técnico funciona offline desde el primer día aunque la configuración siga en curso.
- **CA adicional:** cohorte de pilotos con tiempo al primer valor medido (HV-6).

### J-8 · Reporte mensual
- **FA-1:** el gerente ajusta el texto del resumen IA → edición humana registrada (el resumen IA nunca se presenta como verdad final sin fuentes, DC).
- **EX-1:** cifra sin fuente trazable → el copiloto se abstiene y lo declara (DC doc 33).
- **OFF:** consulta con datos al último cálculo + timestamp visible (P-M1 offline).

### J-9 · Soporte sin fricción
- **FA-1:** problema de sync → el ticket adjunta automáticamente estado del outbox y último sync (contexto técnico, doc 65).
- **EX-1:** incidente de plataforma (caída) → status page + comunicación proactiva (RNF-OBS-005); postmortem sin culpables (doc 59).
- **OFF:** el botón de soporte funciona offline: el ticket se encola y se envía al sincronizar.

## 10. Matriz de trazabilidad journey → requisitos (semilla para docs 09/11)

| Journey | Familias de RF que genera (IDs provisionales) |
|---|---|
| J-1 | RF-REQ-* (intake omnicanal, triage, notificaciones) |
| J-2 | RF-WO-* (OT offline, evidencias, sync), RF-SYNC-* |
| J-3 | RF-PM-* (planes, triggers, calendario, balanceo) |
| J-4 | RF-REQ-*, RF-DISP-* (asignación) |
| J-5 | RF-INV-* (stock, reorden, deltas) |
| J-6 | RF-PROC-* (facturas, OCR, validación, conciliación) |
| J-7 | RF-ONB-* (importación, plantillas, primer valor) |
| J-8 | RF-RPT-* (KPIs, OLAP, resumen IA) |
| J-9 | RF-SUP-* (tickets, FAQ, contexto automático) |

## 11. Criterios de aceptación de este documento
1. Cada journey: persona, canal, pasos, fricción evitada con evidencia, métricas, criterios de aceptación. ✅
2. Todos clasificados DC/SU/PD. ✅
3. Cobertura del usuario primario en el journey más detallado (J-2). ✅
4. Trazabilidad semilla hacia RF. ✅

## 12. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador + validación en pilotos (v1.1).

## 13. Referencias cruzadas
Depende de: 15, 04, ADR-011, ADR-012, AUD-00. Alimenta: 17, 09, 11, 43, 40, 47 (pruebas de aceptación J-2).

## 14. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). 9 journeys (J-1…J-9) con métricas y criterios de aceptación; J-2 como prueba de fuego offline; trazabilidad semilla hacia RF |
| 1.1 | 2026-07-29 | Ampliación por instrucción 8 de la aprobación Ola 2: flujos alternativos, excepciones, estados offline/sync, riesgos y criterios adicionales para los 9 journeys |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
