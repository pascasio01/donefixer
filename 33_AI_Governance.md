# 33 — AI Governance

| Campo | Valor |
|---|---|
| Documento | 33_AI_Governance |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Autoría | Equipo de documentación DONEFIXER bajo dirección del Fundador |
| Precedencia | Documento 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Doc 32 (AI Architecture), Doc 19 (Roles), Doc 02 §10 bis (FEP), Doc 03 §11 bis (costos), ADR-012 (auditoría de plataforma) |

> **Convención de evidencia:** DC · SU · PD en toda afirmación relevante.
> Este documento es **normativo y vinculante**: define qué puede y qué no puede hacer la IA en DONEFIXER. En caso de conflicto con cualquier otro documento sobre capacidades de IA, **prevalece este**. (DC — propuesto; sujeto a aprobación del Fundador)

---

## 1. Propósito

DONEFIXER es AI-First (Doc 01), pero opera sobre infraestructura física real: máquinas, personas, inventarios y dinero. Un error de IA en este dominio no es un texto incorrecto — es una máquina detenida, un repuesto comprado de más, o una decisión laboral injusta. Este documento establece el marco de gobierno que hace que la IA de DONEFIXER sea **confiable, auditable, reversible y financieramente sostenible** durante 10 años. (DC)

---

## 2. Principios de gobierno de IA (GA-1…GA-7)

| ID | Principio | Consecuencia operativa |
|---|---|---|
| GA-1 | **El humano decide lo que importa.** Ninguna acción de riesgo medio/alto se ejecuta sin aprobación humana explícita. | Flujo de sugerencias con aceptar/editar/rechazar (Doc 32 AIA-3) |
| GA-2 | **Las prohibiciones son técnicas, no promesas.** Se implementan como ausencia de permisos en las Service Accounts (Doc 19). | Un agente no puede aprobar una factura porque no posee el permiso, no porque "se le indicó no hacerlo" |
| GA-3 | **Citar o abstenerse.** La IA que informa sobre datos del tenant cita registros reales o se abstiene. | Doc 32 AIA-6; métrica de fidelidad auditada |
| GA-4 | **Toda acción de IA es auditable.** Quién/qué modelo/con qué datos/con qué resultado/quién aprobó. | Eventos `ai.*` (Doc 30) + 10 campos de auditoría cuando aplique (ADR-012) |
| GA-5 | **Toda acción de IA aprobada es reversible o registrada como irreversible.** | Rechazo posterior visible; motivos obligatorios |
| GA-6 | **El tenant es dueño de sus datos.** Sus datos no entrenan modelos sin consentimiento explícito, revocable y granular. | Configuración de tenant; anonimización verificable |
| GA-7 | **La IA es financieramente sostenible.** Costo medido por tenant; línea roja definida. | §6 FinOps |

---

## 3. Clasificación de riesgo de acciones de IA

| Nivel | Definición | Ejemplos (Doc 32) | Régimen |
|---|---|---|---|
| **Bajo** | Solo lectura o generación de contenido sin cambio de estado | IA-1 copiloto, IA-3 semántica, IA-5 resúmenes | Respuesta citada; registro estándar |
| **Medio** | Sugerencias que, de aceptarse, modifican datos operativos | IA-2 avisos, IA-4 diagnóstico, IA-6/7/8 sugerencias | Aprobación humana obligatoria; sugerencia explicable (por qué se sugiere); tasa de aceptación medida |
| **Alto** | Acciones con impacto financiero, de seguridad o sobre personas | IA-9 PdM que dispara OT, IA-10 agentes (conciliación de facturas) | Aprobación humana + doble verificación de datos + registro completo + revisión periódica de desempeño del agente |

---

## 4. Prohibiciones absolutas (vigentes en todas las fases)

Las siguientes acciones están **prohibidas para la IA en cualquier fase del producto**, implementadas como ausencia de permisos (GA-2). **Esta es la única lista canónica de prohibiciones de IA del proyecto** (identificadores P-33-1…P-33-7); el Doc 19 §11 deriva de ella los permisos denegados de las Service Accounts y no mantiene lista propia (AO-2, 2026-07-29). Cambiar esta lista requiere ADR + aprobación expresa del Fundador. (DC)

1. **P-33-1. Aprobar o rechazar facturas** de proveedores (decisión financiera del tenant).
2. **P-33-2. Cerrar órdenes de trabajo críticas** (cierre y verificación son humanas, Doc 14 máquina de estados).
3. **P-33-3. Modificar inventario** (crear/ajustar movimientos de stock) — la IA puede *sugerir* reabastecimiento (IA-6), nunca ejecutarlo.
4. **P-33-4. Sancionar, evaluar desempeño o tomar acciones sobre personas** (técnicos, solicitantes, proveedores) — la IA no produce "scores" de trabajadores.
5. **P-33-5. Comunicarse externamente en nombre del tenant** (correos a clientes/proveedores) sin que un humano revise y envíe.
6. **P-33-6. Acceder a datos de otro tenant** bajo cualquier circunstancia (misma RLS y aislamiento que cualquier actor, Doc 26).
7. **P-33-7. Entrenar con datos de un tenant sin su consentimiento explícito** (GA-6), ni usar datos identificables de personas para entrenamiento.

---

## 5. Calidad y evaluación

| Control | Descripción | Frecuencia |
|---|---|---|
| Dataset de evaluación por caso de uso | Curado de pilotos, anonimizado, versionado | Actualización por release |
| Métricas de calidad | Precisión/exactitud según caso; tasa de abstención correcta (copiloto); tasa de aceptación humana de sugerencias | Continuo en producción |
| Umbral de apagado | Caída bajo umbral → degradación automática a modo manual (Doc 32 AIA-7) | Automático |
| Revisión de sesgos | Muestra de sugerencias revisada por humanos buscando patrones sistemáticos erróneos | Trimestral (Etapa A) |
| Evaluación pre-release | Cambio de modelo/prompt pasa evaluación de regresión antes de producción | Por cambio |

---

## 6. FinOps de IA (línea roja y cuotas)

- **Medición:** costo por tenant, por caso de uso y por modelo, registrado en el AI Gateway (Doc 32 AIA-9). (DC)
- **Cuotas por plan** (Gratis/Profesional/Business/Enterprise) con overage cobrado o degradación elegida por el tenant — anclado al modelo de negocio (Doc 03 §11 bis: costos de IA como línea explícita de margen). (DC)
- **Línea roja:** si el costo de IA de un tenant supera el **30% del ingreso** que ese tenant genera, se dispara revisión obligatoria (ajuste de modelo, cuota o precio). (DC)
- **Transparencia al tenant:** su consumo de IA es visible en su panel de configuración (P-C1). (DC)

---

## 7. Privacidad y protección de datos en IA

1. Clasificación de 4 niveles (Doc 25): nivel Restringido jamás sale a proveedores externos. (DC)
2. Enmascaramiento de PII antes de cualquier llamada externa (Doc 32 AIA-4). (DC)
3. Retención cero exigida contractualmente al proveedor (criterio de PD-IA-1). (DC)
4. Derecho del tenant a **optar por no usar IA externa** (degradación a funciones locales/manuales) — diferenciador Enterprise. (DC)
5. Cumplimiento de regulación aplicable según países piloto (**PD-3** abierta): la evaluación legal de IA se integra a N-3 (presupuesto legal) y se revisará al decidir países. (PD)

---

## 8. Transparencia hacia los usuarios

- Toda sugerencia de IA se **etiqueta visiblemente como generada por IA** en la UI. (DC)
- Toda sugerencia de riesgo medio/alto incluye **explicación de sus fundamentos** (datos usados). (DC)
- El usuario puede **rechazar sin fricción** y su rechazo alimenta la evaluación de calidad. (DC)
- La documentación de ayuda explica en lenguaje claro qué hace y qué no hace la IA (Doc 13, registro de términos). (DC)

---

## 9. Gobernanza de cambios de IA

| Evento | Proceso requerido |
|---|---|
| Nuevo caso de uso de IA | FEP completo (Doc 02 §10 bis) + clasificación de riesgo (§3) + ADR si toca arquitectura |
| Cambio de proveedor/modelo (PD-IA-1) | Evaluación de regresión + análisis FinOps + registro ADR |
| Cambio de prompt en riesgo medio/alto | Evaluación de regresión sobre dataset del caso de uso |
| Modificar lista de prohibiciones (§4) | ADR + aprobación expresa del Fundador |
| Incidente de IA (alucinación con impacto, fuga, costo desbordado) | Postmortem documentado + medida correctiva con responsable y fecha |

---

## 10. Riesgos de gobierno y mitigaciones

| Riesgo | Mitigación |
|---|---|
| "Automation bias": humanos aceptan sugerencias sin revisar | Medición de tasa de aceptación ciega; explicación obligatoria; fricción deliberada en riesgo alto |
| Presión comercial por relajar prohibiciones | §4 solo cambia con ADR + Fundador; las prohibiciones son parte del posicionamiento de confianza (Doc 01 §12 bis) |
| Regulación futura de IA (p. ej., marcos de IA de alto riesgo) | Clasificación de riesgo propia ya alineada con esquemas regulatorios comunes; revisión legal integrada a N-3/PD-3 |
| Costos regulatorios de cumplimiento en pilotos | PD-3 abierta; países piloto se evaluarán también por carga regulatoria de IA |

---

## 11. Criterios de aceptación de este documento

1. Prohibiciones implementables como ausencia de permisos (coherencia con Doc 19). ✅
2. Todo caso de uso del Doc 32 tiene nivel de riesgo y régimen asignado. ✅
3. FinOps con línea roja y cuotas coherente con el modelo de negocio. ✅
4. Gobernanza de cambios definida con autoridad del Fundador preservada. ✅
5. PD abiertas registradas (PD-IA-1 heredada; PD-3 vinculada). ✅

---

*Registro de cambios — v1.0: creación (Ola 3, documento 14 de 14).*

*v1.1 (2026-07-29) — AO-2 (autorizada por el Fundador): §4 declarada única lista canónica de prohibiciones de IA del proyecto con identificadores P-33-1…P-33-7; el Doc 19 deriva de ella sus permisos denegados.*
