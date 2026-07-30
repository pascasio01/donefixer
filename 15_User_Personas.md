# DONEFIXER — 15 · User Personas

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Regla de evidencia (Ola 2, regla 7 del Fundador):** cada persona está clasificada. Todas las personas de esta versión son **SU (supuestos de diseño)** derivadas de la investigación de mercado aprobada (doc 04) — ninguna se basa aún en entrevistas directas con usuarios reales; la validación con pilotos es obligatoria y está registrada como actividad de salida de Fase 0/1 (doc 69). Los rasgos marcados **DC** provienen de decisiones aprobadas (docs 01–04, ADRs); los **PD** indican decisiones del Fundador que afectan a la persona.

---

## 1. Objetivo
Definir las personas que gobiernan todo diseño de producto, UX, requisitos y priorización de DONEFIXER. Cada funcionalidad futura debe declarar a qué persona(s) sirve (FEP-2, doc 02 §10 bis).

## 2. Alcance
Personas de usuarios (quienes usan el producto) y personas compradoras (quienes deciden la compra) para los segmentos S1–S3 del Business Model aprobado (doc 03). Se excluyen las personas del equipo interno DONEFIXER (cubiertas por ADR-012 y doc 19).

## 3. Exclusiones
No incluye personas de verticales reguladas (farma, salud hospitalaria) hasta Fase 5; no incluye perfiles de mercado EE. UU. hasta que la expansión se active (doc 01 §13).

## 4. Decisiones confirmadas (DC) que gobiernan este documento
- **Usuario primario: el técnico de campo** (doc 01 §5: "cuando dos usuarios compiten por una decisión, gana el técnico").
- **Los solicitantes nunca pagan asiento** (doc 03 §7).
- Contextos de diseño obligatorios: sótanos, techos, guantes, poca luz, una mano, redes deficientes, niveles digitales bajos (AUD-00 §12, aprobado en gobernanza).
- Idiomas de lanzamiento: **PD-4** (abierto); la redacción de personas asume ES primero sin cerrar PD-4.
- Países de pilotaje: **PD-3** (abierto); las personas usan perfiles LatAm genéricos sin país fijado.

## 5. Decisiones pendientes (PD) que afectan a personas
| PD | Efecto sobre personas |
|---|---|
| PD-3 países | Ajustes culturales/idiomáticos de todas las personas |
| PD-4 idiomas | P-T1, P-R1, P-V1 requieren variantes PT/FR/HT si se amplía |
| N-10 equipo | Define si la persona P-S1 recibe soporte de 1 o más personas |

## 6. Supuestos (SU) globales
Las personas son arquetipos compuestos de patrones documentados en la investigación de mercado (doc 04) y en la literatura pública del sector, no individuos reales. Se validarán con ≥3 entrevistas por persona crítica (P-T1, P-S1, P-M1, P-R1) antes de cerrar la Fase 1 (criterio de salida, doc 69).

## 7. Dependencias
Doc 04 (aprobado), doc 01 (aprobado), doc 03 (aprobado). Alimenta: 16 (journeys), 17 (blueprints), 19 (roles), 09 (PRD), 11 (RF), 40/41 (UX/accesibilidad), specs de módulos (43).

## 8. Riesgos
| Riesgo | Mitigación |
|---|---|
| Personas idealizadas que no corresponden a la realidad | Validación obligatoria con pilotos; revisión tras las primeras 10 entrevistas |
| Sobre-diseñar para el buyer y descuidar al técnico | Regla DC del usuario primario; FEP-2 la exige |
| Personas monolingües si PD-4 se amplía | Diseño i18n nativo ya confirmado; las personas se versionan por idioma |

---

## 9. Personas de usuarios

### P-T1 · "El técnico de campo" — USUARIO PRIMARIO (SU, validación obligatoria)

| Atributo | Descripción |
|---|---|
| Perfil | 25–55 años, técnico electromecánico/HVAC/mantenimiento general; empleado de planta o de empresa FM; smartphone Android de gama media como herramienta diaria |
| Contexto físico | Sótanos, cuartos mecánicos, techos, exteriores; guantes; ruido; poca luz; **señal celular intermitente o nula en su zona de trabajo** |
| Nivel digital | Variable: desde nativo de WhatsApp hasta quien evita "sistemas"; **cero tolerancia a capacitación formal** |
| Objetivos | Saber qué le toca hoy, llegar al activo, resolver, evidenciar y seguir; que no le hagan escribir de más; que su trabajo quede visible |
| Frustraciones | Papel que se pierde; reportar dos veces lo mismo; apps que "no agarran sin señal"; campos obligatorios absurdos; que le pidan fotos pero la app no funcione en el sótano |
| Qué necesita de DONEFIXER (DC de diseño) | Ciclo completo de OT offline; ≤3 toques por tarea frecuente; escaneo QR del activo; foto/voz como entrada; sincronización automática e **invisible** (con estado visible cuando importa) |
| Métrica de su éxito | Cierra sus OTs del día en la app, no en papel; su MTTR personal mejora |
| Canal | App móvil nativa (ADR-011) |

### P-S1 · "El supervisor de mantenimiento" (SU)

| Atributo | Descripción |
|---|---|
| Perfil | 30–50 años, ascendido de técnico; lidera 5–20 técnicos; vive entre el piso y la oficina |
| Objetivos | Asignar trabajo equilibrado, desbloquear a su equipo, responder "¿en qué va eso?" sin llamar a nadie, cumplir los PMs del mes |
| Frustraciones | Cuadrar horarios en papel/Excel; enterarse de fallas por el cliente antes que por su equipo; reportes que le toman el viernes completo |
| Necesita | Calendario de carga por técnico; estados en tiempo real; aprobaciones rápidas desde el móvil; KPIs automáticos |
| Canal | Web (planificación) + móvil (aprobaciones, piso) |

### P-M1 · "El gerente de mantenimiento/operaciones" — BUYER de S1–S2 (SU)

| Atributo | Descripción |
|---|---|
| Perfil | 35–55 años, responde por disponibilidad y costo de mantenimiento; reporta a dirección |
| Objetivos | Bajar MTTR/downtime, demostrar el valor de su departamento con datos, justificar presupuesto |
| Frustraciones | KPIs armados a mano con datos de dudosa calidad; no poder comparar sitios; software anterior "que nadie usó" |
| Necesita | Dashboards confiables (MTTR/MTBF/PM compliance/costos), evidencia de adopción de su equipo, ROI demostrable |
| Objeción de compra | "Ya probamos un software y fracasó" → se responde con piloto medible (doc 03 §5) |
| Canal | Web |

### P-D1 · "El planificador/despachador" (SU, aparece en S2+)

| Atributo | Descripción |
|---|---|
| Perfil | Rol dedicado en equipos medianos; coordina OTs, turnos y proveedores |
| Objetivos | Maximizar horas productivas, minimizar traslados y tiempos muertos |
| Necesita | Vista de capacidad/habilidades/disponibilidad; sugerencias de asignación (IA asistiva con confirmación humana, doc 33); reagendado masivo |
| Canal | Web |

### P-R1 · "El solicitante" (SU)

| Atributo | Descripción |
|---|---|
| Perfil | Cualquier empleado/ocupante que reporta una falla: recepcionista de hotel, operario, inquilino, docente |
| Nivel digital | El más heterogéneo del sistema; **no instala apps, no tiene cuenta compleja, no paga (DC)** |
| Objetivos | Reportar en 30 segundos por el canal que ya usa (WhatsApp/portal/QR) y saber qué pasó con su reporte |
| Frustraciones | "Reporté y nunca supe nada" (la queja nº 1 documentada en reviews de CMMS, doc 04 §8) |
| Necesita | Intake omnicanal; confirmación inmediata; estado visible sin persecución |
| Canal | PWA/portal ligero + WhatsApp (ADR-011 matriz de paridad) |

### P-V1 · "El proveedor/contratista externo" (SU)

| Atributo | Descripción |
|---|---|
| Perfil | Empresa o técnico independiente que ejecuta OTs para el cliente; relación contractual con SLA |
| Objetivos | Recibir OTs claras, evidenciar su trabajo, facturar sin persecución, cobrar a tiempo |
| Frustraciones | OTs por email/WhatsApp sin detalle; facturas "perdidas"; pagos sin trazabilidad |
| Necesita | Portal de proveedor: OTs asignadas, cierre con evidencia, estado de factura; **validación IA de factura = menos rechazos arbitrarios** |
| Canal | Web ligera (portal) + móvil ocasional |

### P-A1 · "El administrador de activos" (SU, aparece en S2–S3/EAM)

| Atributo | Descripción |
|---|---|
| Perfil | Ingeniero/analista responsable del ciclo de vida y del TCO |
| Objetivos | Decidir reparar vs. reemplazar con datos; planificar CapEx a 5 años |
| Necesita | Historial completo por activo (costos, fallas, downtime), TCO, códigos de falla para RCA |
| Canal | Web |

### P-X1 · "El director de portafolio / multi-sitio" (SU, S2–S3)

| Atributo | Descripción |
|---|---|
| Perfil | Dirige operaciones de varios sitios/edificios; compara desempeño |
| Necesita | Rollup de KPIs por sitio, SLAs por contrato, benchmarking interno |
| Canal | Web |

### P-C1 · "El administrador del tenant" (SU)

| Atributo | Descripción |
|---|---|
| Perfil | TI o operaciones del cliente; configura usuarios, roles, catálogos, integraciones |
| Objetivos | Configurar sin depender de DONEFIXER para todo; auditoría de quién hizo qué |
| Necesita | Tenant Administration (principio de separación de planos, ADR-012); importación de usuarios; SSO (Enterprise) |
| Canal | Web (exclusivo, ADR-011) |

### P-F1 · "Finanzas/compras del cliente" (SU, Fase 2+)

| Atributo | Descripción |
|---|---|
| Perfil | Aprueba compras, recibe facturas de proveedores |
| Necesita | Requisiciones→OC→recepción→factura conciliada; alerta de discrepancias (agente IA con aprobación humana) |
| Canal | Web |

### P-U1 · "El auditor/compliance del cliente" (SU, S3)

| Atributo | Descripción |
|---|---|
| Perfil | Solo lectura; verifica cumplimiento, evidencias, trazabilidad |
| Necesita | Acceso de solo lectura con exportación; log de auditoría inmutable |
| Canal | Web |

---

## 9 bis. Fichas completas por persona (ampliación exigida por aprobación Ola 2, instrucción 7)

> Cada ficha añade: responsabilidades, permisos (trazados a doc 19), escenarios offline y métricas de éxito. Clasificación: SU salvo lo marcado DC.

### P-T1 · Técnico de campo (USUARIO PRIMARIO)
- **Responsabilidades:** ejecutar OTs y rondas, evidenciar trabajo, registrar tiempos/repuestos reales, reportar condiciones inseguras.
- **Permisos (doc 19):** ejecutar OTs asignadas (X), consumir repuestos en OT, consultar activos/PMs de su sitio, crear solicitudes. No puede: aprobar, verificar cierres, configurar.
- **Escenarios offline (críticos):** (a) jornada completa en sótano sin señal → trabaja con su bucket descargado, decisiones provisionales (DC ADR-011 v1.1); (b) señal intermitente → sync oportunista automático, él no gestiona nada; (c) dispositivo compartido por turnos → cambio de usuario con wipe local (DC RF-SYNC-008); (d) 2–3 días en planta remota → convergencia al volver sin pérdida (RNF-SYNC-003).
- **Métricas de éxito:** % OTs cerradas en app (no papel), adopción semanal >80% (HV), toques por tarea ≤3 (DC), cero reportes de pérdida de trabajo.

### P-S1 · Supervisor
- **Responsabilidades:** asignar y desbloquear, verificar cierres (≠ejecutor, DC), cumplir PMs, escalar riesgos.
- **Permisos:** triar solicitudes de su equipo, asignar/verificar/cancelar OTs de su equipo, aprobar en su contexto.
- **Escenarios offline:** aprueba desde el móvil con mala señal → aprobación queda en outbox y se confirma al sincronizar (visible como "pendiente"); consulta estado de su equipo con datos del último sync, con marca de tiempo visible.
- **Métricas:** tiempo de asignación, PM compliance de su equipo ≥85% (HV), % cierres verificados en <48 h.

### P-M1 · Gerente (buyer S1–S2)
- **Responsabilidades:** disponibilidad, costo, KPIs hacia dirección, decisión de compra.
- **Permisos:** CRU en su contexto, aprobaciones, reportes completos de sus sitios.
- **Escenarios offline:** consulta dashboards en avión/poca conexión → web/PWA muestra último cálculo con fecha/hora visible ("datos al 08:15"), nunca simula frescura (DC integridad).
- **Métricas:** tiempo de generación de reporte mensual (<30 min, HV), MTTR de su operación, adopción de su equipo.

### P-R1 · Solicitante
- **Responsabilidades:** reportar fallas con información suficiente; consultar estado.
- **Permisos:** crear solicitudes (portal/WhatsApp/QR, sin cuenta compleja, DC); ver solo las suyas.
- **Escenarios offline:** sin datos móviles → QR + SMS fallback (SU canal); si el portal no carga, el número de WhatsApp sigue abierto (SB-1 modo degradado).
- **Métricas:** tiempo de reporte <60 s (mediana), % con estado consultado sin llamada ≥90% (HV).

### P-D1 · Planificador/despachador
- **Responsabilidades:** calendario, balanceo de carga, coordinación con proveedores.
- **Permisos:** planificar y asignar en su contexto; no verifica cierres.
- **Escenarios offline:** rol de oficina — dependencia de red asumida; degradado: exportación local de la programación del día.
- **Métricas:** horas productivas/capacidad, reagendados por semana.

### P-V1 · Proveedor
- **Responsabilidades:** ejecutar OTs asignadas con evidencia, facturar según contrato.
- **Permisos:** solo sus OTs/facturas/contrato (ABAC por proveedor, DC).
- **Escenarios offline:** evidencia desde obra sin señal → la app móvil con perfil proveedor (SU alcance) o portal con cola de envío best-effort (ADR-011 matriz).
- **Métricas:** días factura→pago, % facturas rechazadas por discrepancia.

### P-A1 · Administrador de activos (S2–S3)
- **Responsabilidades:** ciclo de vida, TCO, RCA, decisiones reparar/reemplazar.
- **Permisos:** lectura profunda de activos, costos, códigos de falla; sin operación.
- **Offline:** no aplica (rol web). **Métricas:** % activos críticos con TCO completo, decisiones RCA documentadas.

### P-X1 · Director de portafolio (S2–S3)
- **Responsabilidades:** comparar sitios, SLAs por contrato, inversión.
- **Permisos:** lectura global del tenant + aprobaciones de alto nivel.
- **Offline:** consulta con datos al último cálculo, con timestamp. **Métricas:** sitios bajo SLA objetivo, varianza de KPIs entre sitios.

### P-C1 · Tenant Admin
- **Responsabilidades:** usuarios, roles, catálogos, integraciones, políticas del tenant.
- **Permisos:** configuración completa del plano tenant (nunca plano plataforma — DC ADR-012).
- **Offline:** no aplica. **Métricas:** tiempo de alta de usuario, incidencias de permisos mal configurados (objetivo 0 con "ver como").

### P-F1 · Finanzas/compras (Fase 2)
- **Responsabilidades:** aprobar compras, conciliar facturas, control de costos.
- **Permisos:** CRU requisiciones/OC según alcance; aprobar facturas tras validación IA (humano decide, DC doc 33).
- **Offline:** no aplica. **Métricas:** % facturas pre-validadas sin discrepancia, tiempo de conciliación mensual.

### P-U1 · Auditor/compliance (S3)
- **Responsabilidades:** verificar evidencias, trazabilidad, cumplimiento.
- **Permisos:** solo lectura + exportación de su tenant, incluido log de auditoría.
- **Offline:** no aplica. **Métricas:** tiempo de obtención de evidencia completa para una auditoría (<1 día, SU).

## 10. Prioridad de diseño (DC heredada + SU)

`P-T1 > P-S1 > P-R1 > P-M1 > P-D1 > P-V1 > resto`. El usuario primario manda (DC); el solicitante sube al tercer lugar porque su fricción es la puerta de entrada de todo el flujo de trabajo (INF, soportada por doc 04 §8).

## 11. Métricas por persona

| Persona | Métrica de éxito de DONEFIXER para ella |
|---|---|
| P-T1 | % OTs cerradas en app vs. papel; toques por tarea frecuente; adopción semanal |
| P-S1 | Tiempo de asignación/reenvío; PM compliance de su equipo |
| P-M1 | Tiempo de generación de reporte mensual (objetivo: minutos, no días) |
| P-R1 | % solicitudes con estado consultado sin llamada |
| P-V1 | Días factura→pago; % facturas rechazadas |

## 12. Criterios de aceptación de este documento
1. Toda persona tiene: contexto, objetivos, frustraciones, canal, métrica. ✅
2. Toda persona clasificada DC/SU/PD. ✅ (todas SU salvo rasgos DC citados)
3. Usuario primario explícito y prioridad declarada. ✅
4. Plan de validación con pilotos registrado. ✅ (§6, doc 69)

## 13. Definition of Done de este documento
DoR/DoD documental del Charter (doc 02 §15–16): 18 secciones o exclusiones declaradas, evidencia etiquetada, referencias cruzadas, sin promesas vacías. Pendiente: aprobación del Fundador.

## 14. Referencias cruzadas
Depende de: 01, 03, 04 (aprobados), ADR-011. Alimenta: 16, 17, 19, 09, 11, 40, 41, 43. La validación con pilotos alimentará la v1.1.

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). 11 personas (P-T1 primaria), prioridad de diseño, métricas por persona, validación con pilotos obligatoria. Todas clasificadas SU salvo rasgos DC; PD-3/PD-4 respetadas como abiertas |
| 1.1 | 2026-07-29 | Ampliación por instrucción 7 de la aprobación Ola 2: fichas completas con responsabilidades, permisos trazados a doc 19, escenarios offline por persona y métricas de éxito |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
