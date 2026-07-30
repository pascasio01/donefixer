# DONEFIXER — Registro de Decisiones Estratégicas Pendientes N-1…N-10

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado de las 10 decisiones: PD (Pendiente de Decisión)** — ninguna recomendación aquí contenida es una decisión confirmada. Se convierten en DC únicamente cuando el Fundador las apruebe expresamente, y entonces se actualizará la Constitución (doc 00) y los documentos afectados.
> **Formato por decisión:** qué se decide · por qué importa · alternativas (2–5) · comparativa (ventajas/desventajas/riesgos/costos/complejidad/evolución) · recomendación con fundamento · reversibilidad · efecto de posponer · dependencias.

---

## N-1 · Framework de la aplicación móvil nativa — **PD**

**1. Qué se decide:** el framework con el que se construirá la app nativa iOS/Android (canal prioritario para campo, ADR-011).

**2. Por qué importa:** es la superficie donde vive la promesa central del producto (offline, evidencia, ≤3 toques). Condiciona contratación, velocidad de desarrollo, calidad en dispositivos Android de gama media (el dispositivo dominante del técnico LatAm) y mantenimiento a 10 años.

**3. Alternativas viables:**
- **A. Flutter (Dart)** — un codebase, renderizado propio.
- **B. React Native + Expo (TypeScript)** — un codebase, comparte lenguaje con la web.
- **C. Nativo Swift + Kotlin** — dos codebases.
- **D. Kotlin Multiplatform (KMP)** — lógica compartida, UI nativa por plataforma.

**4. Comparativa:**

| Criterio | A. Flutter | B. RN+Expo | C. Nativo | D. KMP |
|---|---|---|---|---|
| Ventajas | UI determinista y consistente en Android modesto; un codebase; SDK PowerSync oficial | Pool de talento grande; comparte TS con web; OTA updates (EAS); SDK PowerSync oficial | Máximo rendimiento y acceso a APIs del OS | UI 100% nativa + lógica compartida |
| Desventajas | Pool Dart menor en LatAm; lenguaje adicional | Rendimiento algo menor en pantallas muy densas; OTA limitado por políticas de stores | 2× costo y tiempo; dos especialidades | Ecosistema iOS aún madurando; pool pequeño |
| Riesgos | Contratación lenta | Dependencia del ecosistema Expo/Meta | Inviable con equipo de 1–3 | Inmadurez relativa |
| Costo | 1 codebase | 1 codebase | ~2× | ~1.3× |
| Complejidad | Media | Media | Alta | Media-alta |
| Evolución | Buena (Google lo mantiene) | Buena (Meta + comunidad) | Máxima | Incierta a 10 años |

**5. Recomendación (NO confirmada):** **A. Flutter**, por consistencia visual en Android de gama media y determinismo de UI; con cláusula de conmutación documentada: si dos procesos de contratación fallan, conmutar a B sin costo arquitectónico (los contratos API y PowerSync son idénticos — AUD-00 §3). *Fundamento:* el canal móvil es el diferenciador; la elección se hace donde el riesgo de ejecución es menor para el equipo real disponible.

**6. Clasificación:** **Difícil de cambiar** (reescritura de meses si se cambia en producción; mitigada parcialmente por API-First).

**7. Si se pospone:** se bloquea el doc 23 (Mobile Architecture), el prototipo de sync (gate M2) y cualquier estimación de Fase 1. La Ola 2 puede avanzar (personas/journeys/requisitos son agnósticos), pero la Ola 3 se detiene en el doc 23.

**8. Dependencias:** docs 23, 39, 41, 43 (todas las specs móviles), 47, 62; gate M2; ADR-011.

---

## N-2 · PowerSync: Cloud gestionado vs. self-hosted Open Edition — **PD**

**1. Qué se decide:** modalidad de operación del motor de sincronización adoptado (ADR-002 revertido en AUD-00, pendiente de tu ratificación como DC).

**2. Por qué importa:** afecta costo, carga operativa, data residency y la promesa offline. Es la pieza más crítica del sistema.

**3. Alternativas viables:**
- **A. PowerSync Cloud** (gestionado; tier gratuito para desarrollo, Pro desde $49/mes a fecha de consulta jul-2026 — verificación trimestral obligatoria).
- **B. PowerSync Open Edition self-hosted** (gratuita, licencia FSL; tú operas el servicio).
- **C. Híbrido por etapa:** Cloud en Fases 0–2, self-hosted evaluado en Etapa B por residency/enterprise.

**4. Comparativa:**

| Criterio | A. Cloud | B. Self-hosted | C. Híbrido |
|---|---|---|---|
| Ventajas | Cero operación; soporte del vendor; SOC2/HIPAA del servicio (vendor, ene-2026) | Control total; datos no salen de tu infra; sin costo de licencia | Lo mejor de cada etapa |
| Desventajas | Costo crece con uso; datos de sync en tercero | Tú operas, monitorizas y actualizas el servicio de sync | Requiere migración futura documentada |
| Riesgos | Cambio de precio/términos del vendor | Error operativo propio en la pieza más crítica | Complejidad de planificar la transición |
| Costo | $0–49+/mes inicial (SU, según uso) | Costo de infra + horas de operación | Variable |
| Complejidad | Baja | Media-alta | Media |
| Evolución | Buena | Buena (mismo producto) | Máxima flexibilidad |

**5. Recomendación (NO confirmada):** **C. Híbrido empezando por A (Cloud).** *Fundamento:* en Fases 0–1 el equipo no tiene capacidad de operar el servicio de sync sin distraerse del producto; la migración Cloud→self-hosted es un camino documentado por el propio vendor, así que empezar en Cloud no cierra la puerta a residency enterprise posterior.

**6. Clasificación:** **Fácil de cambiar** (migración documentada entre modalidades del mismo producto; no cambia el SDK ni el protocolo del cliente).

**7. Si se pospone:** bloquea el prototipo de sync (gate M2) y el doc 27 (Offline Sync Architecture). Es la PD más bloqueante del gate M2 junto con N-1.

**8. Dependencias:** docs 25 (datos), 26 (tenancy), 27 (sync), 36/37 (residency), 60 (FinOps), 52 (IaC si self-hosted), gate M2.

---

## N-3 · Presupuesto legal (ToS, DPA, privacidad por jurisdicción) — **PD**

**1. Qué se decide:** si se asigna presupuesto para revisión por abogados licenciados de los documentos legales antes del lanzamiento, y en qué momento.

**2. Por qué importa:** los ToS/DPA/privacidad redactados sin revisión legal son un riesgo de responsabilidad personal y de validez contractual; además, el tratamiento de fotos, ubicación, voz, firmas y datos laborales de terceros (empleados de los clientes) exige bases legales correctas en cada jurisdicción. Nada de lo generado por la suite es asesoría jurídica (regla del Charter).

**3. Alternativas viables:**
- **A. Revisión legal antes del primer piloto pagado** (alcance mínimo: ToS piloto + privacidad + DPA).
- **B. Revisión legal antes del lanzamiento público comercial** (pilotos gratuitos con términos de prueba limitados).
- **C. Plantillas especializadas SaaS + revisión puntual** (menor costo, menor cobertura).
- **D. Aplazar toda revisión hasta ingresos** (no recomendable).

**4. Comparativa:**

| Criterio | A | B | C | D |
|---|---|---|---|---|
| Ventajas | Riesgo cubierto cuando empieza el dinero y los datos reales | Ahorra costo en la fase más incierta | Costo inicial bajo | Costo cero ahora |
| Desventajas | Costo antes de ingresos | Pilotos con términos débiles | Plantillas genéricas no cubren datos laborales/IA | Responsabilidad personal sin red |
| Riesgos | Bajo | Medio | Medio | **Alto** |
| Costo (SU) | $1.5K–5K por jurisdicción inicial | Igual, diferido | $500–1.5K + revisión | $0 ahora, potencialmente muy alto después |
| Complejidad | Baja | Baja | Baja | — |
| Evolución | Base reutilizable | Base reutilizable | Requiere rehacer | — |

**5. Recomendación (NO confirmada):** **A, con alcance mínimo** (ToS piloto + política de privacidad + DPA + declaración de tratamiento de datos laborales/IA). *Fundamento:* el primer piloto ya procesa datos personales de técnicos (ubicación, fotos, horas); el riesgo legal nace con el primer dato real, no con el primer cobro. La opción B es aceptable solo si los pilotos son gratuitos y con datos mínimos.

**6. Clasificación:** **Fácil de cambiar** (contratación de servicio, no compromiso estructural).

**7. Si se pospone:** bloquea pilotos con datos reales y el doc 37 (Legal Framework) queda sin validación; riesgo personal del Fundador creciente con cada usuario real. No bloquea la Ola 2 documental.

**8. Dependencias:** docs 36, 37, 45; términos de piloto; N-7 (jurisdicción define qué abogados); ADR-012 (retención de auditoría PD-AC-3).

---

## N-4 · Procesador de pagos SaaS — **PD**

**1. Qué se decide:** plataforma de cobro de suscripciones (planes del doc 03).

**2. Por qué importa:** determina monedas cobrables, métodos de pago LatAm (tarjetas locales, transferencias, billeteras), impuestos/facturación local, y la fricción de cobro — un punto de fallo mortal en suscripciones.

**3. Alternativas viables:**
- **A. Stripe** (si opera en el país de incorporación).
- **B. Procesador regional LatAm** (p. ej., Mercado Pago, Conekta, dLocal, PayU — según países objetivo, PD-3).
- **C. Plataforma de suscripciones con merchant of record** (Paddle, Lemon Squeezy — gestionan impuestos globales).
- **D. A (o C) + B combinados por mercado.**

**4. Comparativa:**

| Criterio | A. Stripe | B. Regional | C. Merchant of Record | D. Combinado |
|---|---|---|---|---|
| Ventajas | Mejor API, suscripciones maduras, dunning | Métodos locales, moneda local, confianza local | Se encargan de IVA/impuestos en decenas de países | Cobertura total |
| Desventajas | No opera desde todos los países LatAm; impuestos por tu cuenta | APIs menos maduras; dunning débil | Comisión mayor (~5%+); menos control | Complejidad doble |
| Riesgos | Cobros fallidos en tarjetas locales | Fragmentación multi-país | Dependencia del MoR para tu facturación | — |
| Costo (SU) | ~2.9% + $0.30 | Variable local (3–5%) | ~5%+ | — |
| Complejidad | Baja | Media | Baja | Alta |
| Evolución | Excelente | Media | Buena | Buena |

**5. Recomendación (NO confirmada):** **Decidir después de N-7** (país de incorporación) y PD-3 (países de pilotaje); recomendación condicional: si el país lo permite, **A. Stripe** por madurez de suscripciones; si los pilotos exigen métodos locales, **D** empezando por el procesador del país de pilotaje. **C** es la mejor opción si se prioriza simplicidad fiscal global sobre margen.

**6. Clasificación:** **Difícil de cambiar** (migrar suscripciones activas entre procesadores es posible pero doloroso; mitigable abstrayendo billing en el módulo 54).

**7. Si se pospone:** no bloquea Ola 2 ni pilotos gratuitos; bloquea el primer cobro y el diseño del módulo billing/entitlements (docs 43-spec, 54). Debe resolverse antes de Fase 1 comercial.

**8. Dependencias:** docs 03 (planes), 37 (fiscalidad), 43 spec billing, 54 entitlements, 60 FinOps; N-7, PD-3.

---

## N-5 · Registro de marca DONEFIXER — **PD**

**1. Qué se decide:** si se registra la marca DONEFIXER y en qué jurisdicciones/clases.

**2. Por qué importa:** sin registro, un tercero puede registrarla primero y forzar un cambio de nombre con producto en el mercado — el daño más caro imaginable para una marca que este proyecto blinda por regla (DC-00). Costo bajo, protección alta.

**3. Alternativas viables:**
- **A. Registrar ya** en país de origen (clases 9 y 42 como mínimo).
- **B. Registrar antes del lanzamiento público** (tras validar pilotos).
- **C. Registrar en origen + Madrid Protocol** para expansión posterior.
- **D. No registrar por ahora.**

**4. Comparativa:**

| Criterio | A | B | C | D |
|---|---|---|---|---|
| Ventajas | Protección desde ya; disuade copias | Gasta solo si el proyecto avanza | Cobertura internacional escalable | Costo cero |
| Desventajas | Costo antes de validar | Ventana de exposición | Mayor costo inicial | Riesgo de perder el nombre |
| Riesgos | Bajo | Medio (que otro registre primero) | Bajo | **Alto** |
| Costo (SU) | $200–1K por jurisdicción | Igual, diferido | $1K–3K+ | $0 ahora |
| Complejidad | Baja (gestor local) | Baja | Media | — |
| Evolución | Ampliable vía Madrid | Ampliable | Ya internacional | — |

**5. Recomendación (NO confirmada):** **A o B según tu apetito de riesgo**, en clases 9 y 42; ampliar con C al entrar a EE. UU./Brasil. *Fundamento:* el costo es el de una cena de empresa; el riesgo de no hacerlo es perder la identidad completa del proyecto.

**6. Clasificación:** **Fácil de cambiar** en alcance (se amplía), **difícil de revertir** el daño si se pospone y otro registra primero.

**7. Si se pospone:** ventana de riesgo de usurpación de marca; no bloquea documentación ni pilotos privados, pero sí el lanzamiento público y cualquier inversión en marketing.

**8. Dependencias:** doc 37 (legal), 42 (branding), N-7 (jurisdicción), lanzamiento público y stores (doc 62).

---

## N-6 · Idiomas de lanzamiento — **PD**

**1. Qué se decide:** idiomas de la UI disponibles en Fase 1 (la i18n nativa ya es DC — ADR-010; esto decide el *alcance inicial*).

**2. Por qué importa:** define carga de traducción, QA por idioma, contenido legal traducido, y qué mercados son accesibles desde el día 1. El mercado caribeño (FR/criollo haitiano) y Brasil (PT) dependen de esta decisión.

**3. Alternativas viables:**
- **A. ES + EN** en Fase 1; PT/FR/HT en Fase 3.
- **B. ES + EN + PT** (si Brasil entra en pilotaje, PD-3).
- **C. Los 5 idiomas desde el inicio** (ES/EN/PT/FR/HT).
- **D. Solo ES** (máxima velocidad, mercado inicial más pequeño).

**4. Comparativa:**

| Criterio | A | B | C | D |
|---|---|---|---|---|
| Ventajas | Foco; QA manejable; cubre puente EE. UU. | Abre Brasil (mayor mercado LatAm) | Cobertura caribeña total | Velocidad máxima |
| Desventajas | Brasil/Caribe esperan | +1 idioma de QA y legal | QA y contenido legal ×5 | Sin EN pierde puente EE. UU. y credibilidad enterprise |
| Riesgos | Bajo | Medio-bajo | Medio (calidad de traducción) | Medio |
| Costo (SU) | Base | +10–15% esfuerzo de contenido | +30–40% | −15% |
| Complejidad | Baja | Media | Alta | Mínima |
| Evolución | Los demás idiomas se añaden sin cambio arquitectónico (i18n nativa DC) | Igual | Ya completo | Requiere añadir EN después |

**5. Recomendación (NO confirmada):** **A (ES + EN)** salvo que PD-3 incluya Brasil, en cuyo caso **B**. *Fundamento:* la arquitectura i18n ya soporta los 5; añadir idiomas es trabajo de contenido y QA, no de ingeniería — no hay ventaja en pagar ese costo antes de tener clientes en esos idiomas.

**6. Clasificación:** **Fácil de cambiar** (añadir idiomas es incremental; la decisión irreversible — i18n nativa — ya está tomada).

**7. Si se pospone:** bloquea parcialmente doc 13 (glosario por idioma) y specs de traducción (doc 43-módulo 22), y la preparación de contenido de pilotos. Ola 2 puede avanzar en ES+EN como idiomas de redacción sin decidir el alcance comercial.

**8. Dependencias:** docs 13, 43 (módulo traducción), 36/37 (contenido legal por idioma), 64 (onboarding localizado), PD-3.

---

## N-7 · País de incorporación legal y residencia de datos inicial — **PD**

**1. Qué se decide:** dónde se constituye legalmente la entidad (o si se opera inicialmente como persona física) y en qué región cloud residen los datos de producción al lanzar.

**2. Por qué importa:** es la decisión más enredada del proyecto: determina jurisdicción de los ToS/DPA (N-3), opciones de procesador de pagos (N-4), registro de marca (N-5), obligaciones fiscales, qué leyes de protección de datos aplican, y la promesa de residency a clientes. Afecta a casi todos los documentos legales y de datos.

**3. Alternativas viables:**
- **A. Persona física / entidad en país de origen del Fundador** + datos en región cloud más cercana.
- **B. Entidad en EE. UU. (Delaware LLC/C-Corp)** + datos en región US.
- **C. Entidad en país de origen + entidad EE. UU. posterior** (estructura por etapas).
- **D. Jurisdicción regional de servicios** (p. ej., Estonia e-Residency u otras) — menos común para SaaS LatAm.

**4. Comparativa:**

| Criterio | A | B | C | D |
|---|---|---|---|---|
| Ventajas | Simple, barato, rápido; coherente con mercado inicial LatAm | Credibilidad enterprise/inversores; Stripe completo; mercado US | No cierra puertas; costo diferido | Operación digital remota |
| Desventajas | Menor acceso a pagos/inversión global | Costo y obligaciones fiscales US; complejidad si no hay ingresos US | Doble estructura eventual | Poca familiaridad de clientes LatAm |
| Riesgos | Techo de cristal para enterprise US | Cumplimiento fiscal US sin ingresos US | Complejidad futura gestionable | Medio |
| Costo (SU) | Bajo ($100–1K) | $500–3K/año + compliance | Escalable | $300–1K/año |
| Complejidad | Baja | Media-alta | Media | Media |
| Evolución | Migrable a C | Es el destino típico si hay expansión US | Máxima flexibilidad | Limitada |

**5. Recomendación (NO confirmada):** **A o C según tu país de origen y ambición de inversión.** Si el país de origen permite operar y cobrar razonablemente: **A** ahora con camino documentado a **C** cuando entre EE. UU. (Fase 5). Residency de datos: región cloud más cercana a los pilotos (p. ej., São Paulo o US-East para LatAm — decidir con PD-3). *Fundamento:* la experiencia de SaaS B2B indica que la estructura se sofistica cuando los ingresos la justifican; pero debe diseñarse la migración desde ya (datos exportables, DPA preparado para subprocesadores — docs 36/37).

**6. Clasificación:** **Difícil de cambiar** (migrar entidad y residency es posible pero costoso; mitigable con plan documentado).

**7. Si se pospone:** bloquea N-3 (qué abogados), N-4 (qué procesadores), N-5 (dónde registrar), doc 37 (jurisdicción de contratos), doc 36 (ley aplicable) y la respuesta a clientes "¿dónde están mis datos?". **Es la PD con más dependencias cruzadas.** No bloquea la Ola 2 documental (puede redactarse con placeholder de jurisdicción), pero bloquea pilotos pagados y el lanzamiento.

**8. Dependencias:** docs 36, 37, 45, 26 (residency), 52 (regiones IaC), 60 (impuestos), 03 (facturación), N-3/N-4/N-5.

---

## N-8 · Nivel de accesibilidad contractual — **PD**

**1. Qué se decide:** si WCAG 2.2 AA se adopta como estándar interno vinculante (diseño+QA) y si se ofrece contractualmente a clientes (VPAT/ACR en ventas enterprise).

**2. Por qué importa:** la accesibilidad es requisito legal en varios mercados (EE. UU.: ADA/Section 508 en sector público; UE: EAA desde jun-2025 para productos digitales — DC con fecha) y diferenciador comercial; pero comprometerla contractualmente sin verificación formal es un riesgo (regla: no afirmar cumplimiento sin evidencia).

**3. Alternativas viables:**
- **A. WCAG 2.2 AA como estándar interno**; sin compromiso contractual hasta auditoría de accesibilidad.
- **B. AA interno + VPAT/ACR** tras evaluación profesional (Etapa B, ventas enterprise/sector público).
- **C. Solo WCAG 2.2 A** (mínimo).
- **D. Decidir por mercado** (AA donde la ley lo exija).

**4. Comparativa:**

| Criterio | A | B | C | D |
|---|---|---|---|---|
| Ventajas | Calidad real sin riesgo contractual | Habilita sector público/enterprise US y UE | Menor costo | Ajusta costo a obligación |
| Desventajas | Pierde ventas que exigen VPAT | Costo de evaluación y remediación | Insuficiente legalmente en varios mercados | Complejidad de gobernar por mercado |
| Riesgos | Bajo | Bajo (una vez evaluado) | Medio-alto | Medio |
| Costo (SU) | +5–10% esfuerzo de diseño/dev | $5–15K evaluación + remediación | Menor | Variable |
| Complejidad | Media | Media | Baja | Media-alta |
| Evolución | Camino natural a B | Ya completo | Requiere upgrade | — |

**5. Recomendación (NO confirmada):** **A ahora → B en Etapa B** (antes de ventas enterprise/sector público EE. UU./UE). *Fundamento:* adoptar AA internamente desde el diseño es mucho más barato que remediar después, y el compromiso contractual solo cuando exista evidencia (regla de integridad del Charter).

**6. Clasificación:** **Fácil de cambiar hacia arriba** (A→B es evolución natural); **difícil revertir** si se promete contractualmente sin sustento.

**7. Si se pospone:** el doc 41 (Accessibility Standard) no tiene nivel normativo y la Ola 5 queda bloqueada en esa decisión; si se diseña sin nivel, la remediación posterior multiplica costo.

**8. Dependencias:** docs 41, 39, 40, 47 (QA accesibilidad), 62 (stores: etiquetas de accesibilidad), 37 (obligaciones por jurisdicción), ventas enterprise (Fase 5).

---

## N-9 · Modelo de soporte en Fase 1 — **PD**

**1. Qué se decide:** qué se promete de soporte con equipo unipersonal: canales, horario, tiempos de respuesta y qué se declara en los términos de piloto.

**2. Por qué importa:** prometer soporte 24/7 con una persona destruye la credibilidad al primer incidente nocturno (regla §9 Charter: sin promesas vacías); pero el soporte es parte del producto en B2B — la honestidad del SLA de piloto define la confianza inicial.

**3. Alternativas viables:**
- **A. Soporte fundador directo, horario declarado** (p. ej., L–V 9–18 h local), mejor esfuerzo fuera de horario, canal WhatsApp/email + base de conocimiento.
- **B. A + herramienta de soporte** (chat con base de conocimiento y respuestas asistidas por IA gobernada).
- **C. Soporte por niveles desde ya** (declarado como roadmap, no como servicio actual).
- **D. Tercerizar soporte nivel 1** (prematuro en Fase 1).

**4. Comparativa:**

| Criterio | A | B | C | D |
|---|---|---|---|---|
| Ventajas | Honesto, gratis, cercano al cliente (aprendizaje directo) | Escala sin contratar; IA responde FAQs | Aspiración clara para ventas | Cobertura horaria real |
| Desventajas | Cobertura limitada; depende de una persona | Costo de herramienta; riesgo de IA mal gobernada | Promete lo que no existe aún | Costo; conocimiento de producto externo |
| Riesgos | Agotamiento del fundador | Bajo si IA con alcance limitado | Incumplimiento percibido | Medio |
| Costo (SU) | $0 | $20–100/mes | $0 ahora | $500+/mes |
| Complejidad | Baja | Baja-media | Baja | Media |
| Evolución | Natural hacia B/C al contratar | Base del futuro nivel 1 | — | — |

**5. Recomendación (NO confirmada):** **A + B ligero.** Horario y tiempos declarados en términos de piloto (mejor esfuerzo fuera de horario); WhatsApp como canal (coherente con el producto); base de conocimiento bilingüe desde el piloto 3; asistencia IA solo para FAQs con fuentes, nunca para compromisos con el cliente (doc 33). *Fundamento:* en Fase 1 el soporte es I+D disfrazado — cada ticket es un requisito; pero se promete solo lo cumplible.

**6. Clasificación:** **Fácil de cambiar** (evoluciona con el equipo; lo difícil es revertir una promesa ya hecha — de ahí la cautela).

**7. Si se pospone:** los términos de piloto no tienen sección de soporte (bloquea contratos de piloto junto con N-3); riesgo de promesas verbales inconsistentes. No bloquea Ola 2 documental (doc 65 se redacta con esta PD abierta).

**8. Dependencias:** docs 65 (Support Model), 37 (términos), 64 (onboarding), 33 (IA en soporte), N-10 (capacidad).

---

## N-10 · Equipo en Fase 1: solo fundador o con contrataciones — **PD**

**1. Qué se decide:** si DONEFIXER Fase 1 se construye y opera solo por el Fundador o con 1–2 contrataciones (y en qué roles).

**2. Por qué importa:** define qué arquitectura es operable (la Etapa A de la auditoría asume 1–3 personas), la velocidad real del roadmap, la aprobación dual humana (PD-AC-4), el bus-factor (riesgo R6), y la viabilidad financiera (salarios vs. runway).

**3. Alternativas viables:**
- **A. Solo fundador** en Fase 1, con IA como multiplicador y esta suite como memoria.
- **B. Fundador + 1 contratación técnica** (desarrollo; prioriza velocidad).
- **C. Fundador + 1 contratación comercial/operativa** (ventas, pilotos, soporte; prioriza validación de mercado).
- **D. Fundador + freelancers por hito** (diseño UX, legal, pentest puntual).

**4. Comparativa:**

| Criterio | A | B | C | D |
|---|---|---|---|---|
| Ventajas | Costo mínimo; control total; velocidad de decisión | 2× velocidad de construcción; dual humana posible | Validación de mercado más rápida; libera al fundador para construir | Capacidad puntual sin costo fijo |
| Desventajas | Bus-factor 1; techo de velocidad; agotamiento | Costo fijo alto; contratación técnica difícil sin producto | La construcción sigue siendo cuello de botella | Coordinación; calidad variable |
| Riesgos | **Alto** (R6) | Medio (contratación errónea) | Medio | Bajo-medio |
| Costo (SU) | $0 | $2–6K/mes LatAm según senioridad | $1.5–4K/mes | $500–3K por hito |
| Complejidad | Baja organizativa | Media | Media | Baja-media |
| Evolución | Puede contratar después | Equipo núcleo | Equipo núcleo | Complementa cualquiera |

**5. Recomendación (NO confirmada):** **A + D** para Fases 0–1 (solo fundador + freelancers por hito: UX, legal N-3, pentest), evaluando **B o C** al cierre de la Fase 1 con datos de pilotos — contratar técnico si el cuello es construcción, comercial si el cuello es pipeline. *Fundamento:* la decisión de contratar es más acertada con datos de pilotos que antes; los hitos puntuales (legal, UX, seguridad) no se improvisan pero tampoco justifican nómina fija.

**6. Clasificación:** **Fácil de cambiar** (contratar es reversible; lo difícil es deshacer una contratación errónea — de ahí la espera a datos).

**7. Si se pospone:** no bloquea la documentación (la suite asume ya el escenario mínimo: Etapa A operable por 1 persona); bloquea la estimación realista del roadmap (doc 69) y la aprobación dual humana (PD-AC-4 queda en su forma degradada). Cuanto más se pospone, más larga la Fase 1.

**8. Dependencias:** docs 69 (roadmap/capacidad), 65 (soporte), 60 (FinOps), 66 (operations), PD-AC-4 (ADR-012), N-1 (qué perfil técnico contratar depende del framework).

---

## Matriz resumen

| # | Decisión | Recomendación (NO confirmada) | Reversibilidad | Bloquea principalmente |
|---|---|---|---|---|
| N-1 | Framework móvil | Flutter (con conmutación a RN si falla contratación) | Difícil de cambiar | Doc 23, prototipo sync, Fase 1 |
| N-2 | PowerSync Cloud vs self-host | Híbrido: Cloud ahora, self-host en Etapa B | Fácil | Gate M2, doc 27 |
| N-3 | Presupuesto legal | Antes del primer piloto pagado, alcance mínimo | Fácil | Pilotos con datos reales, doc 37 |
| N-4 | Procesador de pagos | Decidir tras N-7/PD-3; Stripe si aplica | Difícil de cambiar | Primer cobro, módulo billing |
| N-5 | Registro de marca | Registrar (clases 9 y 42), alcance por riesgo | Fácil ampliar; difícil revertir daño | Lanzamiento público |
| N-6 | Idiomas lanzamiento | ES+EN (B si Brasil en pilotaje) | Fácil | Contenido pilotos, doc 13 |
| N-7 | Incorporación y residency | País origen + camino a EE. UU. (C) | Difícil de cambiar | N-3/N-4/N-5, docs 36/37 — **la más enredada** |
| N-8 | Accesibilidad | AA interno ahora; VPAT en Etapa B | Fácil hacia arriba | Doc 41, Ola 5 |
| N-9 | Soporte Fase 1 | Fundador con horario declarado + FAQ IA ligera | Fácil | Términos de piloto |
| N-10 | Equipo Fase 1 | Solo + freelancers por hito; contratar tras pilotos | Fácil | Roadmap realista, dual humana |

## Orden sugerido de resolución (por dependencias, no por urgencia percibida)
**N-7 → N-3, N-4, N-5 · PD-3 (países) → N-6, N-4 · N-1 → N-10 · N-2** (puede resolverse en paralelo, desbloquea M2) · **N-8, N-9** (independientes, rápidas).

## Procedimiento de aprobación
Para cada decisión aprobada: (1) el Fundador indica la alternativa elegida (puede elegir otra no recomendada — su autoridad es final, doc 02 §10); (2) se registra como DC con fecha; (3) se actualizan la Constitución (doc 00), los documentos dependientes y la tabla DC/SU/PD; (4) solo entonces continúa el trabajo documental sobre esas áreas.

## Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación del registro N-1…N-10 con alternativas, comparativas, recomendaciones no confirmadas, reversibilidad, efectos de posponer y dependencias. Todas en estado PD |
