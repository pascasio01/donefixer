# DONEFIXER — 02 · Product Charter

> **Nombre oficial:** DONEFIXER · **Categoría:** Enterprise Maintenance & Operations Platform
> **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 1, 2026-07-29)
> Este documento es el acta constitutiva del proyecto: define quién decide, qué es innegociable y cómo se gobierna el cambio.

---

## 1. Objetivo
Establecer la autoridad, el alcance, las restricciones, los principios no negociables y el gobierno de decisiones de DONEFIXER como esfuerzo profesional de producto — no como proyecto improvisado.

## 2. Alcance
Todo el ciclo de vida del producto: investigación, documentación, diseño, construcción, lanzamiento, operación y evolución a 10 años.

## 3. Exclusiones
No es un contrato legal de sociedad ni un documento corporativo de constitución de empresa (doc 37 Legal Framework cubre los instrumentos jurídicos; PD: revisión por abogados licenciados). No define requisitos ni arquitectura.

---

## 4. Propósito
Construir una plataforma original, nativa, profesional, segura, accesible, escalable y preparada para producción, capaz de evolucionar 10 años sin arquitectura innecesariamente compleja en su primera etapa (objetivo oficial declarado por el Fundador — DC). **Explícitamente prohibido:** entregar demos disfrazadas de producto, MVPs improvisados llamados de otra forma, plantillas compradas, clones de competidores, o código sin trazabilidad documental.

## 5. Stakeholders y autoridad

| Rol | Persona/Entidad | Autoridad |
|---|---|---|
| **Fundador, Creador y Desarrollador** | **Pascasio Emmanuel Reynoso Reyes** | Autoridad final sobre TODAS las decisiones del proyecto: producto, arquitectura, negocio, marca y publicación |
| Usuarios de pilotos (futuros) | Clientes Fase 1 | Voz consultiva vía métricas y entrevistas; no deciden roadmap |
| Asistentes de IA / herramientas | Varios | Ejecutan bajo dirección; **no poseen autoría** sobre el producto ni sobre decisiones |
| Asesores legales (futuros, por jurisdicción) | Abogados licenciados | Revisión obligatoria de docs legales antes de lanzamiento (PD: contratación) |

**Regla de autoría (DC, permanente):** la autoría del proyecto DONEFIXER pertenece exclusivamente a Pascasio Emmanuel Reynoso Reyes. Ningún documento, código, artefacto o registro atribuirá la creación a otra persona, equipo o herramienta. La asistencia de IA se documenta como herramienta, nunca como autor.

## 6. Restricciones declaradas

| Restricción | Tipo | Consecuencia |
|---|---|---|
| Equipo inicial de 1–3 personas (SU — PD N-10 del Fundador) | Capacidad | Etapa A de arquitectura; prohibido K8s/microservicios/ML propio en Fase 1 (AUD-00 §I) |
| Presupuesto limitado no cuantificado (PD) | Financiero | FinOps con escenarios (doc 60); todo costo recurrente requiere aprobación |
| Sin clientes aún | Comercial | Ningún SLO contractual hasta Etapa B; pilotos con alcance escrito |
| Certificaciones: ninguna obtenida | Cumplimiento | Prohibido afirmar SOC 2/ISO/GDPR-compliance; estado honesto: "diseño alineado, aspiracional" (DC de integridad) |
| Nombre y marca sin registro marcario aún | Legal | PD: registrar DONEFIXER antes del lanzamiento público |
| Regla de evidencia DC/SU/PD | Metodológica | Ningún documento presenta supuestos como hechos |

## 7. Principios no negociables

1. **Nombre e identidad:** el producto se llama únicamente **DONEFIXER**. Cualquier otra grafía es un defecto de consistencia y se corrige de inmediato (DC-00, registrada 2026-07-29 tras corrección global).
2. **Autoría:** Pascasio Emmanuel Reynoso Reyes, siempre (§5).
3. **Originalidad:** prohibido copiar identidad visual, textos, código, interfaces o activos de competidores. Se estudian, no se imitan.
4. **Integridad de evidencia:** DC/SU/PD en todo; cifras con fuente y fecha; prohibido declarar "sin errores" — se diseña para prevenir, detectar, contener, recuperar y aprender.
5. **Offline-first y técnico-primero** como propiedades del producto, no del discurso.
6. **IA gobernada:** la IA nunca es autoridad autónoma; lista de prohibiciones implementable (doc 33).
7. **Privacidad y seguridad por diseño** desde el primer documento, no como parche.
8. **El dato del cliente es del cliente:** exportación completa garantizada ("salida digna").
9. **Sin promesas vacías:** ni de marketing ni de ingeniería; todo compromiso tiene métrica, dueño y fecha.
10. **Documentación antes que código:** ningún módulo se programa sin su spec aprobada (M-gates, AUD-00 §M).

## 8. Criterios de éxito (proyecto, no solo producto)

| Horizonte | Criterio medible |
|---|---|
| Fin Fase 0 | Olas 1–4 documentales aprobadas; prototipo de sync validado; gates M1–M8 |
| Fin Fase 1 | 3–5 pilotos activos; adopción frontline >80%; sync >99.9%; primeros clientes de pago |
| Año 3 | Ingresos recurrentes que cubran costos operativos (punto de equilibrio operativo — SU hasta doc 03 validado) |
| Año 5 | Referencia CMMS en español; SOC 2 Type II **obtenido**; expansión regional |
| Año 10 | Plataforma EAM/FM global sin reescritura arquitectónica |

## 9. Criterios de fracaso (condiciones de parada o pivote)

1. Pilotos con adopción frontline <40% tras dos ciclos de corrección → re-diseño UX radical o parada.
2. Sync offline con pérdida de datos en campo no resoluble → reevaluación arquitectónica total.
3. Costo de IA por tenant >30% del ingreso por tenant sostenidamente → modelo de precios/IA inviable, re-diseñar.
4. Imposibilidad de financiar el cumplimiento mínimo para vender → replantear mercado objetivo.
5. Dependencia de un solo proveedor crítico (LLM, sync, cloud) sin salida viable → ejecutar estrategia de salida documentada.
*Regla: los criterios de fracaso se evalúan con datos, en revisión trimestral, nunca por intuición ni por cansancio.*

## 10. Gobierno de decisiones

| Tipo de decisión | Quién decide | Registro |
|---|---|---|
| Estratégica (mercado, precios, marca, pivote) | Fundador | ADR + actualización docs |
| Arquitectónica irreversible (tenancy, sync, datos, identidad) | Fundador, con análisis documentado obligatorio (alternativas + consecuencias) | ADR formal (doc 13/21) |
| Reversible de implementación | Criterio de ingeniería documentado en spec del módulo | Nota en spec |
| Cumplimiento/legal | Fundador + abogado licenciado | Doc 37 + acta de revisión |
| Gasto recurrente nuevo | Fundador | Registro FinOps (doc 60) |

**Regla de irreversibilidad:** ninguna decisión irreversible se cierra sin documento de alternativas. **Regla de reapertura:** toda decisión puede reabrirse con evidencia nueva (precedente: ADR-002 revertido por AUD-00 al aparecer datos nuevos de PowerSync — ejemplo de gobierno sano, no de debilidad).

## 10 bis. Proceso formal de evaluación de nuevas funcionalidades (Feature Evaluation Process — FEP)

> Añadido por exigencia de la aprobación condicional de la Ola 1. **Ninguna funcionalidad entra al producto sin pasar este proceso.** Aplica a peticiones de clientes, ideas internas, respuestas a competidores y propuestas de terceros. La velocidad nunca se usa como excusa para saltarlo: el proceso tiene carriles según tamaño.

### FEP-1 · Registro (obligatorio para toda idea)
Toda propuesta se registra con: origen (cliente/mercado/interno/competidor), problema que resuelve (no la solución deseada), frecuencia de la demanda (cuántos clientes la pidieron, con fechas), y evidencia (tickets, entrevistas, datos de uso). Sin registro no existe evaluación. Las ideas no se borran: se archivan con motivo.

### FEP-2 · Filtro de admisión (4 preguntas, una respuesta "no" lo frena)
1. **¿Sirve al usuario primario o a un buyer real?** (técnico/supervisor/gerente — doc 15). Si solo suena bien en una demo → **rechazar**.
2. **¿Respeta las exclusiones?** (doc 01 §12 bis y §13). Si contradice una exclusión → rechazar o escalar a reversión de exclusión (proceso propio, más exigente).
3. **¿Encaja en una fase del roadmap actual o siguiente?** (doc 69). Si no → **parking lot** con fecha de revisión, no compromiso.
4. **¿Puede medirse su éxito?** Si no existe métrica concebible → reformular o rechazar.

### FEP-3 · Evaluación (puntuación documentada, no intuición)

| Dimensión | Pregunta | Peso |
|---|---|---|
| Valor para el usuario primario | ¿Reduce tiempo, errores o trabajo del técnico/supervisor? | 30% |
| Alineación con diferenciadores | ¿Refuerza offline / IA gobernada / LatAm / migración? | 25% |
| Evidencia de demanda | ¿Cuántos clientes reales, con qué intensidad? | 20% |
| Costo de construcción y operación | ¿Esfuerzo, deuda, costo recurrente (IA, terceros)? | 15% |
| Riesgo | ¿Seguridad, privacidad, complejidad de sync, soporte que genera? | 10% |

Umbrales (SU iniciales, a calibrar tras 2 trimestres de uso): ≥75% → priorizar en roadmap; 50–74% → parking lot con fecha; <50% → rechazar con motivo registrado. **La puntuación nunca sustituye el juicio del Fundador: lo obliga a justificar desviaciones por escrito** (si se aprueba algo <75%, se documenta por qué).

### FEP-4 · Decisión y clasificación
Toda funcionalidad aprobada se clasifica (heredado de ADR-012): configuración dinámica / feature flag / actualización remota compatible / despliegue web / actualización móvil por tienda / migración de datos / cambio de infraestructura. Las que afectan sync offline, seguridad, datos del cliente o modelo de dominio requieren además: spec de módulo actualizada (doc 43), matriz de conflicto de sync (doc 27) y revisión de seguridad (doc 34).

### FEP-5 · Post-lanzamiento (aprender, no solo entregar)
Cada funcionalidad lanzada declara su métrica de éxito antes de construirse y se evalúa a los 60/90 días: **adoptada** (se mantiene), **subadoptada** (se mejora o se retira — con fecha), **fallida** (se retira y se documenta la lección en retrospectiva sin culpables, doc 59). Una funcionalidad sin dueño ni métrica a los 6 meses entra en candidatura de retiro. **El producto se poda, no solo crece.**

### FEP-6 · Carriles
| Carril | Alcance | Proceso |
|---|---|---|
| Menor | Texto, umbral, campo opcional, traducción | FEP-1 + FEP-2 (mismo día) |
| Estándar | Feature de módulo existente | FEP completo |
| Mayor | Nuevo módulo, nueva integración, capacidad de IA | FEP completo + ADR + spec + revisión de seguridad |
| Reversión de exclusión | Contradice doc 01 §12 bis | FEP completo + evidencia ≥5 clientes + aprobación expresa del Fundador + ADR |

## 11. Control de cambios del proyecto

- Suite documental versionada por documento (tabla de control en cada uno); revisión global **trimestral** obligatoria (resuelve hallazgo H-41 de auditoría).
- Matriz de precios y capacidades de competidores: re-verificación trimestral (doc 04 §7).
- Todo cambio en decisiones confirmadas requiere actualizar: ADR, documentos afectados (referencias cruzadas) y este charter si aplica.

## 12. Ownership y propiedad intelectual

- **Código, documentación, diseños, marca y datos de plataforma:** propiedad de Pascasio Emmanuel Reynoso Reyes (hasta constitución de entidad legal — PD N-7: país de incorporación).
- **Datos de clientes:** propiedad del cliente (principio no negociable §7.8).
- **Contenido generado con asistencia de IA:** derechos reclamados por el Fundador según los términos de las herramientas; revisar licencias de toda dependencia antes de uso comercial (doc 37).
- **Registro de marca DONEFIXER:** PD antes del lanzamiento público.

## 13. Identidad oficial

Nombre: **DONEFIXER** (única grafía válida). Categoría: **Enterprise Maintenance & Operations Platform**. Fundador, Creador y Desarrollador: **Pascasio Emmanuel Reynoso Reyes**. Visión geográfica: global, foco inicial Latinoamérica, expansión posterior a Estados Unidos y otros mercados. Estas tres líneas se replican textualmente en la portada de todo documento de la suite.

## 14. Responsabilidades (RACI resumido de gobierno)

| Función | Responsable |
|---|---|
| Aprobar documentos y gates | Fundador |
| Mantener trazabilidad DC/SU/PD | Todo artefacto generado lo declara; Fundador audita |
| Revisión legal por jurisdicción | Abogados licenciados (PD contratación) |
| Seguridad de la información | Fundador (hasta contratar responsable — PD) |
| Verificación de fuentes de mercado | Revisión trimestral registrada en doc 04 |

## 15. Definition of Ready (documental)

Un documento está listo para revisión cuando: (1) tiene las 18 secciones estándar o declara cuáles no aplican y por qué; (2) toda evidencia externa lleva fuente y fecha; (3) DC/SU/PD aplicado; (4) referencias cruzadas actualizadas; (5) nombre DONEFIXER verificado; (6) sin lenguaje promocional vacío ni promesas de infalibilidad.

## 16. Definition of Done (documental)

Un documento está terminado cuando: DoR cumplido + revisado contra su lista de contenido mínimo + aprobado **expresamente** por el Fundador (aprobación registrada en la tabla de control de cambios) + sus dependencias (docs bloqueantes) están aprobadas + ninguna PD crítica sin dueño y fecha.

## 17. Referencias cruzadas
Gobierna a: toda la suite. Depende de: 00 (índice y reglas), AUD-00 (hallazgos), 01 (visión), 04 (evidencia). Alimenta: 05–08, 37 (legal), 69 (roadmap), 70 (PRR).

## 18. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 1). Registra DC-00 de corrección nominal DONEFIXER, gobierno de decisiones con precedente ADR-002, criterios de fracaso y DoR/DoD documental |
| 1.1 | 2026-07-29 | **Ampliación por aprobación condicional Ola 1:** nuevo §10 bis — Proceso Formal de Evaluación de Funcionalidades (FEP) en 6 etapas con scoring ponderado, 4 carriles y post-lanzamiento con poda del producto |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 1** por el Fundador. Base estratégica oficial; no congelado: futuras modificaciones por gobierno documental (evidencia, trazabilidad, ADR, versionado, motivo) |
