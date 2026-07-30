# AUDITORÍA INTEGRAL DE ARQUITECTURA — DONEFIXER (2026-07)

| Campo | Valor |
|---|---|
| Documento | AUDITORIA_INTEGRAL_ARQUITECTURA_2026-07 |
| Versión | 1.0 |
| Estado | ⏳ Entregada — pendiente de aprobación expresa del Fundador (condición previa a Ola 4) |
| Mandato | Aprobación oficial Ola 3 (2026-07-29): auditoría obligatoria antes de Ola 4, con entregas A–E |
| Alcance | Los 34 documentos oficiales: Ola 1 (01–04), ADR-011/012, N-1…N-10, Ola 2 (09–19), Ola 3 (20–33), más AUD-00 e Índice Maestro |
| Método | Verificación cruzada automatizada de identificadores (RF/RNF/SY/MT/eventos/ADRs) + revisión manual de coherencia semántica, valores numéricos y dependencias |

> **Veredicto global:** la arquitectura es **sólida en sus decisiones sustantivas** — no se encontraron contradicciones de diseño ni decisiones sin trazabilidad ascendente. Los hallazgos son de **trazabilidad mecánica** (identificadores citados con familia o número incorrecto en 3 documentos), **dos inconsistencias menores de contenido** y **vacíos de formalización** heredados. Ningún hallazgo invalida una decisión arquitectónica aprobada; todos son corregibles con erratas editoriales o documentos complementarios. Detalle en secciones A–E.

---

## Revisión por los 14 objetivos del mandato

### 1. Consistencia entre las 34 decisiones arquitectónicas

Se verificaron las familias de decisiones: MT-1…12, SY-1…15, EV-1…7, AP-1…12, IN-1…7, SE-1…6, EA-1…8, WA-1…10, MA-1…10, AIA-1…9, GA-1…7. **Sin contradicciones sustantivas entre ellas.** Verificaciones puntuales superadas:

- La regla de autoridad del backend (texto literal del Fundador, ADR-011 v1.1) se respeta en WA-5, MA-1/principio 4, SY-8 y en el flujo 3.2 del Doc 21: validación local provisional → re-validación en servidor → veredicto visible. Ningún documento otorga autoridad de estado al cliente.
- La separación de planos (ADR-012 v1.1, principio permanente) se mantiene en EA-6, topología del Doc 21 y tabla de límites de responsabilidad (§4): la Admin API nunca se mezcla con la API de tenant.
- La máquina de estados de OT (Doc 14) es la única referida por Docs 16, 19, 24, 27 y 32; ningún documento introduce transiciones alternativas.
- Los diferidos (ClickHouse, Kafka, K8s, Python ML, vector DB) tienen criterios medibles consistentes entre su documento de capa y el Doc 21 §2.3.

**Hallazgo H-01 (menor, editorial):** el Doc 23 (MA-8) fija "búsqueda local ≤300 ms p95" mientras RNF-PERF-002 fija "latencia local móvil (lecturas SQLite) <100 ms p95". Son métricas de alcance distinto (búsqueda FTS vs. lectura simple) pero el Doc 23 no lo aclara. → Acción AO-3.

### 2. Coherencia entre bounded contexts

Los contextos del Doc 14 (identity, work, assets, planning, inventory, procurement, governance, platform) se mapean sin huérfanos a: esquemas lógicos del Doc 25, módulos del monolito (Doc 24), módulos web (Doc 22 §3), catálogo de eventos (Doc 30) y objetos de IA (Doc 18). **Sin contexto sin hogar arquitectónico ni componente sin contexto.** El contexto `platform` queda correctamente aislado en el plano de plataforma en todos los documentos.

### 3. Revisión de dependencias

- Cadena crítica verificada: clientes → API → pipeline multi-tenant (JWT→membresía→`set_config`) → dominio → outbox → workers. Sin dependencias circulares entre capas; dominio puro no importa infraestructura en ningún documento.
- **Dependencia externa más crítica: PowerSync** (N-2 abierta). Mitigaciones presentes en tres documentos independientes (27 §Alternativas, 21 §8, 23 MA-1 adaptador). Coherente.
- **Hallazgo H-02 (vacío de formalización):** ADR-002, ADR-004 y ADR-005 se citan en 10 documentos (00, 02, 11, 14, 20, 21, 24, 25, AUD-00, N1-N10) pero **no existen como documentos ADR individuales** — son decisiones absorbidas de la investigación previa registradas dentro de AUD-00. La trazabilidad "ADR-004" no resuelve a un artefacto concreto. → Acción AO-4 (registro índice de ADR-001…010).

### 4. Revisión de escalabilidad

Criterios de escalado verificados como medibles y coherentes: RNF-SCL (Doc 12), índices tenant-first (Doc 26), cursor pagination (AP-5), cuotas anti-noisy-neighbor (Doc 26), extracción de módulos por métricas (Doc 24), criterios ClickHouse/Kafka/K8s (Docs 25/30/24). Sin tecnología sin criterio de activación. **Conforme.**

### 5. Revisión de resiliencia

RTO ≤4h / RPO ≤15min (Doc 12) compatibles con backup + réplica de Etapa A (Doc 21 §7, alternativa E pospuesta con justificación). Outbox garantiza cero pérdida de eventos (EV-1); idempotencia de punta a punta (SY-5, AP-8); RNF-SYNC-004 (pérdida de datos = 0) coherente con tombstones y veredictos. **Conforme.** Observación: la prueba de restauración de backup no tiene frecuencia asignada → recomendación R-3 (no bloqueante).

### 6. Revisión de seguridad

Cadena verificada: RNF-SEC-001…009 ↔ Docs 26 (aislamiento + matriz de ataques bloqueando CI = RNF-SEC-006), 25 (clasificación 4 niveles), 22 (WA-8), 23 (MA-7), 33 (§7). MFA para admins coherente entre RNF-SEC-004 y régimen Fase 0-1 de ADR-012. **Conforme.**

### 7. Revisión FinOps

Línea roja de IA (≤30% del ingreso del tenant) **idéntica en los tres documentos que la definen o citan**: RNF-FIN-002, Doc 03 §11 bis, Doc 33 §6. Cuotas por plan coherentes entre Doc 03 y AIA-9. Infra Etapa A $150–500/mes (RNF-FIN-001, SU). **Conforme.**

### 8. Revisión de observabilidad

RNF-OBS-001…005 ↔ Doc 21 §5 (logs con trace_id/tenant_id/actor_id/operation_id, OTel, métricas de negocio, alertas por ausencia de señal) ↔ Doc 33 §5 (evaluación IA). `tenant_id` en el 100% de trazas (RNF-OBS-001) compatible con RLS. **Conforme.**

### 9. Revisión de mantenibilidad

Monolito modular + capas estrictas + OpenAPI generado desde código (AP-3) + cliente de API generado (WA-4) + expand/contract (Doc 25) + presupuestos en CI (WA-9). Coherente con equipo mínimo (N-10 PD). **Conforme.**

### 10. Revisión de experiencia offline

Pilar verificado de punta a punta: RNF-SYNC-003 (≥7 días / 200 ops) ↔ SY-4/SY-5/SY-6/SY-12/SY-13 ↔ MA-2/MA-3/MA-4 ↔ J-2 (prueba literal de modo avión, criterio de salida Fase 1) ↔ WA-3 (división deliberada: web no duplica motor de sync). La división offline nativo vs. captura limitada PWA está justificada y marcada con SU de posible elevación vía ADR. **Conforme — es la parte más sólida de la arquitectura.**

### 11. Revisión de IA y gobierno

- Prohibiciones implementadas como ausencia de permisos: verificado en Doc 19 §11 (service accounts + permisos denegados), RNF-AI-003, GA-2 y AIA-2. Coherente.
- Cite-or-abstain: RNF-AI-001 ↔ AIA-6 ↔ GA-3. Coherente.
- **Hallazgo H-03 (inconsistencia menor de contenido):** la lista de prohibiciones de IA del Doc 19 §11 (7 ítems, redacción propia: incluye "diagnósticos de seguridad concluyentes", "decisiones legales", "enviar datos a terceros no autorizados") **no es textualmente idéntica** a la lista canónica de 7 prohibiciones del Doc 33 §4 (que incluye "no entrenar con datos sin consentimiento" y "no acceder a datos de otro tenant", ausentes como ítem explícito en Doc 19). Se solapan ~80%. El Doc 33 declara precedencia, pero coexistir dos listas es deuda documental. → Acción AO-2 (lista única canónica en Doc 33; Doc 19 la referencia).
- PD-IA-1 correctamente abierta; AI Gateway protege al dominio del lock-in.

### 12. Identificación de riesgos técnicos

Consolidados de todos los documentos (sin nuevos riesgos descubiertos por la auditoría): dependencia PowerSync (mitigada ×3), complejidad write-path (mitigada con 8 casos normativos + J-2), operación unipersonal (mitigada con observabilidad + régimen Fase 0-1), alucinación del copiloto (mitigada con cite-or-abstain + umbral de apagado), fragmentación Android (pendiente de PD-3). Registro completo en sección B.

### 13. Identificación de deuda técnica potencial

- **DT-1:** doble lista de prohibiciones IA (H-03).
- **DT-2:** ADRs tempranos sin artefacto propio (H-02).
- **DT-3:** identificadores RNF/RF citados con familia inexistente en Docs 21/22/23 (H-04, sección C).
- **DT-4:** sin frecuencia asignada a pruebas de restauración de backup (R-3).
- **DT-5:** SU-FLAGS y PD-RETENCIÓN arrastradas desde ADR-012 sin fecha de revisión (ya registradas como PD; se recomienda ventana de resolución).

### 14. Verificación de trazabilidad completa (Product Vision → AI Governance)

Se extrajeron y cruzaron **todos** los identificadores RF-*/RNF-* citados en los 14 documentos de la Ola 3 contra los catálogos de los Docs 11 y 12. Resultado:

- **Docs 24, 25, 26, 27, 28, 29, 30, 31, 20, 32, 33: citas íntegras y resolubles.** ✅
- **Docs 21, 22, 23: 25 citas con identificador roto** (H-04). La trazabilidad *conceptual* es correcta (el requisito existe y la decisión le responde), pero el *identificador mecánico* apunta a familias que el Doc 12 no define.

---

## A. Hallazgos

| ID | Severidad | Hallazgo | Documentos afectados |
|---|---|---|---|
| H-01 | Menor | Posible tensión "búsqueda local ≤300 ms" (MA-8) vs. "lectura local <100 ms" (RNF-PERF-002) sin aclaración de alcance | 23 vs. 12 |
| H-02 | Media | ADR-001…010 citados pero sin documento propio (viven dentro de AUD-00); la referencia no resuelve a artefacto | 00, 02, 11, 14, 20, 21, 24, 25 + AUD-00 |
| H-03 | Media | Dos listas de prohibiciones de IA no idénticas (~80% solape) en Docs 19 y 33 | 19, 33 |
| H-04 | Alta (documental) | 25 citas RNF/RF con familia o número inexistente (detalle en C) | 21, 22, 23 |
| H-05 | Menor | Prueba de restauración de backup sin frecuencia asignada | 12, 21 |
| H-06 | Informativo | PD arrastradas sin ventana de revisión (SU-FLAGS, PD-RETENCIÓN, PD-2, PD-IA-1) | ADR-012, 02, 32 |

## B. Riesgos (consolidado del proyecto, verificados)

| # | Riesgo | Mitigación vigente | Estado |
|---|---|---|---|
| R-1 | Dependencia de PowerSync (N-2 abierta) | Adaptador de sync (MA-1), fallback Zero (Doc 27), PoC previa a decisión | Mitigado |
| R-2 | Complejidad del write-path de sync | 8 casos normativos + J-2 como gate de Fase 1 | Mitigado |
| R-3 | Operación unipersonal | Observabilidad Etapa A + régimen Fase 0-1 + simplicidad deliberada | Mitigado |
| R-4 | Alucinación del copiloto | Cite-or-abstain + umbral de apagado (RNF-AI-001, AIA-6/7) | Mitigado |
| R-5 | Costo de IA desbordado | Cuotas + línea roja 30% + dashboard (RNF-FIN-002) | Mitigado |
| R-6 | Fuga de datos a proveedor LLM | AIA-4 + retención cero contractual (PD-IA-1) + opt-out Enterprise | Mitigado, pendiente de PD-IA-1 |
| R-7 | Fragmentación Android en pilotos | Dispositivo objetivo por definir con PD-3 | Abierto (depende de PD-3) |
| R-8 | Backup nunca probado en restauración | — (H-05) | **Sin mitigar → AO-5** |

## C. Inconsistencias (detalle técnico de H-04)

Citas en Docs 21/22/23 que usan familias **inexistentes** en el catálogo del Doc 12, con su mapeo correcto verificado:

| Cita rota (Ola 3) | Familia usada | Identificador correcto (Doc 12) | Dónde |
|---|---|---|---|
| RNF-OFF-001 / OFF-002 (7 días, 200 ops, convergencia) | `OFF` (no existe) | **RNF-SYNC-003** (≥7 días / 200 operaciones) y RNF-SYNC-002 (convergencia <60 s) | 21 §3.2, 23 MA/principios |
| RNF-OFF-004 / OFF-005 (batería, datos móviles) | `OFF` | **RNF-MOB-003** (batería) y RNF-MOB-004 (almacenamiento/buckets) | 23 MA-8 |
| RNF-PER-001…005 | `PER` (no existe) | **RNF-PERF-001…005** (misma numeración: 001 carga web, 002 INP/interacción, 003 Redis/caché → verificar fila exacta al aplicar, 004 arranque, 005 búsqueda local) | 21 §2.2, 22 WA-9, 23 MA-8 |
| RNF-SEG-001 (auth) | `SEG` (no existe) | **RNF-SEC-001/RNF-SEC-005** (TLS/sesiones) según contexto | 21 §2.2, 23 MA-7 |
| RNF-SEG-005 (SQLCipher) | `SEG` | **RNF-SEC-003** (cifrado local móvil) | 23 MA-2 |
| RNF-SEG-006 (borrado remoto/revocación) | `SEG` | **RNF-SEC-005** (revocación por dispositivo) | 23 MA-2/MA-7 |
| RNF-USA-001/002/004 | `USA` (no existe) | **RNF-ACC-*** (accesibilidad) y **RNF-USE-*** (usabilidad frontline: ≤3 toques = RNF-USE-001; estado visible = RNF-USE-004) | 22 WA-1/WA-6, 23 MA-6 |
| RNF-SYN-001 (>99.9%/día) | `SYN` | **RNF-SYNC-001** | 21 §5 |
| RF-AST-008 (escaneo QR) | número inexistente (AST llega a 004) | **RF-WO-006** (escaneo QR vincula OT) y RF-REQ-001 (intake por QR) | 23 MA-5 |
| RF-EVD (evidencias) | familia inexistente | **RF-WO-003** (evidencias aditivas con hash) y RF-WO-007 (firma) | 21 §2.2, 22 WA-8 |
| RF-WEB | familia inexistente | Requisitos web viven en RF-REQ-001 (PWA), RF-RPT-*, RF-PLT-*; citar por capacidad concreta | 22 WA-1 |

**Naturaleza:** erratas de identificador, no errores de diseño — en cada caso el requisito correcto existe y la decisión le responde fielmente. Corrección editorial de bajo riesgo, sin tocar ninguna decisión.

## D. Recomendaciones

1. **R-1:** Adoptar la regla "un identificador citable debe existir en su catálogo" como parte del DoD documental (Doc 02) — cualquier herramienta de verificación cruzada como la usada en esta auditoría puede correr en CI documental.
2. **R-2:** Mantener una **única lista canónica de prohibiciones de IA** (Doc 33 §4) y que Doc 19 §11 la referencie con permisos denegados derivados ítem por ítem.
3. **R-3:** Asignar frecuencia a la prueba de restauración (sugerencia: trimestral en Etapa A, como RNF-AVL adicional o nota en Doc 12) — la Ola 4 (calidad/operación) es el lugar natural.
4. **R-4:** Crear el registro índice de ADR-001…010 apuntando a las secciones de AUD-00 que contienen cada decisión, para que toda cita ADR resuelva.
5. **R-5:** Asignar ventana de revisión a las PD arrastradas (SU-FLAGS, PD-RETENCIÓN, PD-2, PD-IA-1) — sugerencia: antes del cierre de la Ola 4.
6. **R-6:** En Doc 23 MA-8, aclarar que "búsqueda local FTS ≤300 ms" es métrica distinta de "lectura simple <100 ms" (RNF-PERF-002), o unificar.

## E. Acciones obligatorias antes de Production Readiness

| ID | Acción | Tipo | Bloquea |
|---|---|---|---|
| **AO-1** | Aplicar las correcciones de identificadores de la tabla C en Docs 21, 22, 23 (errata editorial, con changelog; sin cambiar ninguna decisión) | Documental | Ola 4 |
| **AO-2** | Unificar la lista de prohibiciones de IA: Doc 33 §4 como canónica; Doc 19 §11 pasa a derivar permisos denegados de esa lista (changelog en ambos) | Documental | Ola 4 |
| **AO-3** | Aclarar el alcance de la métrica de búsqueda local en Doc 23 MA-8 (R-6) | Documental | Ola 4 |
| **AO-4** | Crear `ADR-001-010_Registro.md` con el mapeo de cada ADR temprano a su sección fuente en AUD-00 | Documental | Ola 4 |
| **AO-5** | Incorporar frecuencia de prueba de restauración de backup (propuesta: trimestral) al Doc 12 o al plan de la Ola 4 | Documental | Antes de Production Readiness (puede resolverse dentro de la Ola 4) |
| **AO-6** | Resolver o calendarizar PD arrastradas: SU-FLAGS, PD-RETENCIÓN, PD-2, PD-IA-1 | Decisión del Fundador | Antes de Production Readiness |

> **Nota de alcance:** AO-1 a AO-4 son ejecutables de inmediato tras su aprobación de esta auditoría (son erratas y formalizaciones, no modificaciones arquitectónicas; quedan trazadas por este documento conforme a la condición permanente 4). AO-5 y AO-6 pueden integrarse al plan de la Ola 4.

---

## Verificación contra los objetivos mínimos del mandato

| Objetivo | Resultado |
|---|---|
| Consistencia de las 34 decisiones | ✅ Sin contradicciones sustantivas |
| Coherencia entre bounded contexts | ✅ Mapeo completo sin huérfanos |
| Dependencias | ✅ 1 vacío de formalización (H-02) |
| Escalabilidad | ✅ Criterios medibles |
| Resiliencia | ✅ 1 vacío menor (H-05) |
| Seguridad | ✅ Coherente |
| FinOps | ✅ Línea roja idéntica en 3 fuentes |
| Observabilidad | ✅ Coherente |
| Mantenibilidad | ✅ Coherente con equipo mínimo |
| Experiencia offline | ✅ El pilar más sólido |
| IA y gobierno | ⚠️ 1 inconsistencia menor (H-03) |
| Riesgos técnicos | ✅ Consolidados (sección B) |
| Deuda técnica potencial | ✅ DT-1…DT-5 identificadas |
| Trazabilidad Vision → AI Governance | ⚠️ 25 citas rotas en 3 documentos (H-04), corrección editorial definida |

---

*Registro de cambios — v1.0 (2026-07-29): Auditoría Integral de Arquitectura ejecutada por mandato de la aprobación oficial de la Ola 3. Entrega en formato A–E. Pendiente de aprobación expresa del Fundador.*
