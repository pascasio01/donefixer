# DONEFIXER — 04 · Market and Competitor Research

> **Nombre oficial:** DONEFIXER · **Categoría:** Enterprise Maintenance & Operations Platform
> **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · **Fecha de consulta de fuentes:** julio 2026 · **Estado:** ✅ APROBADO (aprobación oficial Ola 1, 2026-07-29)
> **Etiquetas de evidencia:** DC = decisión/dato confirmado con fuente fechada · SU = supuesto/estimación · PD = pendiente de decisión · INF = inferencia del equipo (no es hecho)
> **Advertencia de método:** las cifras de consultoras de mercado son estimaciones comerciales de metodología no auditable; se reportan con fuente y fecha y se usan solo como orientación de orden de magnitud, nunca como hechos.

---

## 1. Objetivo
Establecer la base de evidencia de mercado y competencia que gobierna la visión (doc 01), el charter (doc 02) y el modelo de negocio (doc 03) de DONEFIXER. Todo dato aquí citado es la única fuente canónica de cifras de mercado para el resto de la suite.

## 2. Alcance
CMMS, EAM, Facility Management (IWMS) y Field Service Management (FSM); regiones: global, Latinoamérica y Estados Unidos; competidores directos e indirectos; precios públicos; barreras, oportunidades y riesgos.

## 3. Exclusiones
No incluye análisis de verticales industriales específicos (minería, farma) más allá de su relevancia para el roadmap; no incluye valoraciones de inversión ni asesoría financiera; no replica identidad visual, textos ni activos de competidores.

---

## 4. Tamaño y evolución del mercado

### 4.1 Cifras citadas (con nivel de confianza)

| Métrica | Valor | Fuente (fecha) | Confianza |
|---|---|---|---|
| Mercado CMMS global 2024 | ~USD 1.29B | Reporte comercial de consultora (2024–2025) [^14^] | Media (SU) |
| CMMS proyectado 2030 | ~USD 2.41B, CAGR ~11.1% | Misma serie [^14^] | Media (SU) |
| Mercado EAM global 2025 | ~USD 4.4B | Consultora comercial (2025) [^8^] | Media-baja (SU) |
| EAM proyectado 2033 | ~USD 8.77B, CAGR ~9% | Misma serie [^8^] | Media-baja (SU) |
| Norteamérica, cuota CMMS | >31% (2024) | Misma serie [^14^] | Media (SU) |

**Interpretación (INF):** aunque las cifras absolutas varían entre consultoras, tres señales convergen y sí son robustas: (a) el mercado crece a ritmo de un dígito alto a doble dígito; (b) el crecimiento se concentra en SaaS cloud sobre legacy on-premise; (c) los motores citados de forma consistente son IA, IoT, movilidad frontline y presión por extender la vida de activos. DONEFIXER no dimensiona su plan sobre los dólares absolutos sino sobre estas tres señales (DC metodológica).

### 4.2 Segmentos

| Segmento | Qué resuelve | Ticket típico (SU) | Dinámica |
|---|---|---|---|
| **CMMS** | Órdenes de trabajo, PM, activos, inventario | $20–75/usuario/mes | Segmento de entrada; competencia intensa; gana la adopción frontline |
| **EAM** | Ciclo de vida completo, TCO, CapEx, APM | Contratos enterprise 5–7 cifras/año | Dominado por Tier-1; implementaciones largas |
| **Facility Mgmt / IWMS** | Portafolio inmobiliario, espacios, arrendamientos, proveedores | Por sitio/portafolio | Convergencia con CMMS; multi-sitio como núcleo |
| **FSM** | Despacho de técnicos a clientes externos, facturación de servicio | Por técnico | Adyacente; relevante para proveedores/contratistas |

**INF:** la frontera entre los cuatro segmentos se está difuminando (los CMMS suben a EAM; los IWMS bajan a operación diaria). DONEFIXER se diseña con un solo modelo de dominio que cubre los cuatro por capas de madurez (trazable a doc 01 y al roadmap doc 69), lo que evita la reescritura que sufren los CMMS al subir de segmento.

---

## 5. Regiones prioritarias

### 5.1 Latinoamérica (mercado inicial — DC estratégica del Fundador)

**Hechos verificables:** existen competidores con tracción demostrada en la región — Tractian (Brasil, industrial, monitoreo de condición) y Fracttal (Chile, mid-market hispanohablante) — lo que confirma demanda y disposición de pago (DC con fuentes de la investigación previa, 2025–2026 [^28^][^41^]). Ningún líder global nace en español con soporte, precios y cumplimiento regionales (INF a partir de la revisión de sitios y documentación pública de los competidores).

**Inferencias (INF):** WhatsApp es el canal operativo por defecto en PYMEs y facility management latinoamericano; ningún líder global lo resuelve como canal nativo de intake (verificado en la matriz de capacidades, §7). La conectividad deficiente en plantas, sótanos y zonas rurales hace del offline-first una ventaja estructural, no cosmética. Los equipos multilingües (ES/PT/FR/criollo haitiano en el Caribe) están desatendidos por herramientas monolingües.

**Riesgos:** menor disposición de pago por asiento que EE. UU.; informalidad operativa (Excel/papel como competidor real); complejidad fiscal multi-país para facturación SaaS (PD: país de incorporación, ver doc 03).

### 5.2 Estados Unidos (expansión — DC estratégica del Fundador)

**Hechos:** es el mercado más grande (cuota >31% según §4.1, SU) y el más exigente en cumplimiento: SOC 2 Type II es requisito de facto en ventas enterprise (DC de la investigación de compliance previa [^35^]). Los precios de referencia públicos ($20–75/usuario/mes, §7) fijan el techo del mid-market.

**Inferencias (INF):** entrar en EE. UU. sin SOC 2 ni SSO/SCIM es inviable en enterprise pero viable en SMB; el mercado hispanohablante de técnicos en EE. UU. (millones de trabajadores de mantenimiento y facilities) es un puente de expansión natural para un producto bilingüe nativo — esta hipótesis requiere validación (registrada en doc 03, H-VAL).

### 5.3 Priorización recomendada (recomendación)
1. **Fase 1:** país de origen del Fundador + 1–2 países LatAm de validación (criterio: facilidad fiscal, presencia de clientes piloto).
2. **Fase 3:** Ampliación LatAm (México, Brasil con PT, Caribe con FR/HT).
3. **Fase 5:** EE. UU. con SOC 2 obtenido.
*Fundamento:* el costo de cumplimiento enterprise estadounidense es inasumible antes de tener ingresos recurrentes. *Riesgo:* un competidor global acelera su localización en LatAm. *Decisión del Fundador requerida:* países exactos de pilotaje (PD).

---

## 6. Competidores directos e indirectos

**Directos (mismo presupuesto del cliente):** MaintainX, Fiix, UpKeep, Limble, eMaint, Fracttal, Tractian, Fabrico, OxMaint.
**Directos enterprise:** IBM Maximo, SAP EAM, Oracle EAM, Hexagon, IFS, Infor EAM.
**Directos FM:** Facilio, Planon, Eptura/Archibus, MRI, Infraspeak, IBM TRIRIGA.
**Indirectos (el competidor real de la Fase 1):** Excel + WhatsApp + papel (INF: la mayoría de los clientes objetivo migran desde ahí, no desde otro CMMS — corroborado cualitativamente por el posicionamiento de "migración desde hojas de cálculo" de Limble [^30^]).
**Sustitutos:** ERP con módulo de mantenimiento (SAP PM, Oracle), hojas de cálculo, servicios tercerizados de mantenimiento con sus propias herramientas.

---

## 7. Matriz de capacidades (verificada con fuentes públicas, julio 2026)

Leyenda: ✅ nativo y maduro · 🟡 parcial / plan alto / limitado · ❌ ausente o vacío estructural documentado · ? no verificable públicamente.

| Capacidad | MaintainX | Fiix | UpKeep | Limble | Fracttal | Tractian | Facilio | Maximo |
|---|---|---|---|---|---|---|---|---|
| OTs móviles frontline | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 |
| Offline ciclo completo | 🟡 [^9^] | 🟡 [^9^] | 🟡 | 🟡 | ? | ? | ? | 🟡 |
| Jerarquía de activos multinivel | 🟡 | ✅ [^27^] | ✅ | 🟡 | ✅ | ✅ | ✅ | ✅ |
| Códigos de falla / RCA | ❌ | ✅ [^27^] | 🟡 | 🟡 | 🟡 | ✅ | 🟡 | ✅ |
| Gestión de proveedores/contratos | ❌ [^27^] | ❌ [^27^] | 🟡 | ❌ | 🟡 | ❌ | ✅ [^27^] | ✅ |
| Portal de solicitantes/inquilinos | ❌ [^27^] | 🟡 [^32^] | 🟡 | 🟡 | 🟡 | ❌ | ✅ [^27^] | 🟡 |
| Validación de facturas pre-aprobación | ❌ [^27^] | ❌ [^27^] | ❌ | ❌ | ? | ❌ | ✅ [^27^] | 🟡 |
| IA asistiva (copiloto) | 🟡 solo Enterprise [^27^] | 🟡 desde plan $75 [^31^] | 🟡 | 🟡 [^33^] | ✅ planes altos [^28^] | ✅ | ✅ | ✅ |
| IA agentiva con auditoría | ❌ [^27^] | ❌ [^27^] | ❌ | ❌ | 🟡 | 🟡 | ✅ [^27^] | 🟡 |
| IoT / monitoreo de condición | 🟡 | 🟡 | ✅ sensores propios [^7^] | 🟡 | 🟡 | ✅ sensor-agnóstico [^28^] | ✅ | ✅ |
| Multi-sitio / portafolio | 🟡 [^27^] | 🟡 | 🟡 | 🟡 | ✅ | 🟡 | ✅ núcleo [^27^] | ✅ |
| WhatsApp como intake | ❌ [^27^] | ❌ | ❌ | ❌ | ? | ? | ? | ❌ |
| Español nativo + soporte LatAm | 🟡 | 🟡 | 🟡 | 🟡 | ✅ | ✅ | 🟡 | 🟡 |
| API pública | 🟡 plan alto | ✅ [^27^] | ✅ | ✅ | ✅ | ? | ✅ | ✅ |
| Plan gratuito | ✅ [^27^] | ✅ [^29^] | ❌ | ✅ [^30^] | ? | ❌ | ❌ | ❌ |

*Nota de integridad: esta matriz se construyó con fuentes públicas citadas y la investigación previa (julio 2026); los competidores cierran brechas constantemente — la matriz se re-verifica trimestralmente (regla de suite, doc 00).*

### Precios públicos verificados (a julio 2026, con riesgo de cambio — re-verificar trimestralmente)

| Producto | Precios públicos | Fuente (fecha) |
|---|---|---|
| MaintainX | Gratis; Essential ~$20/usuario/mes; Premium ~$65 | Sitio de precios / análisis (2025–2026) [^27^] |
| Fiix | Gratis; Basic $45; Professional $75/usuario/mes | Sitio oficial (2025–2026) [^29^] |
| Limble | Gratis; Standard $28; Premium+ ~$69 | Sitio oficial (2025–2026) [^30^] |
| UpKeep | Lite ~$20–45; hasta ~$120 con add-ons/sensores | Sitio oficial (2025–2026) [^32^] |
| Facilio / Maximo / SAP EAM | Custom, no públicos | Sitios oficiales [^27^][^11^] |

**Rango de mercado mid-market (INF):** $20–75 por usuario/mes; implementación enterprise $5K–100K+ adicionales (SU, fuente comercial [^30^]).

---

## 8. Debilidades reales documentadas (DC con fuentes, julio 2026)

1. **MaintainX/Fiix:** ausencia estructural de gestión de proveedores, portal de solicitantes e IA autónoma; multi-sitio débil; IA encerrada en planes altos [^27^][^31^].
2. **UpKeep:** acoplamiento a sensores propietarios; costo que escala con módulos; reportes de bugs por usuarios [^32^][^7^].
3. **Maximo/SAP:** implementaciones de 6–24+ meses, costos de 6–7 cifras, curva de aprendizaje pronunciada, resistencia del usuario [^2^][^11^].
4. **Limble:** analítica e IA menos maduras [^28^].
5. **General del segmento:** offline parcial en todos los CMMS móviles verificados [^9^]; WhatsApp ignorado como canal [^27^]; precio por asiento que castiga el crecimiento del cliente [^27^].

## 8 bis. Análisis profundo por competidor: fortalezas reales, errores históricos, ventajas sostenibles y capacidades difíciles de replicar

> Ampliación exigida por la aprobación condicional de la Ola 1 (2026-07-29). Regla: toda fortaleza o error se cita con fuente y fecha; los "errores históricos" se limitan a hechos públicos verificables, no a opiniones; las capacidades "difíciles de replicar" se evalúan contra la capacidad real de un entrante pequeño (DONEFIXER), no en abstracto.

### MaintainX (el líder frontline a batir)

- **Fortalezas reales (DC):** UX móvil de adopción sin capacitación, validada por el mercado: **11,000+ empresas, 11M+ activos gestionados, 500K+ profesionales frontline** (cifras de la compañía, jul-2025) [^68^]; Serie D de **$150M a valoración $2.5B** (jul-2025, Crunchbase News) [^65^]; total captado ~$254M [^68^]; ~500–759 empleados [^64^][^69^]; biblioteca precargada de **10,000+ planes de mantenimiento aprobados por OEM** (Verdantix Green Quadrant 2025, top-3 en 8 de 12 categorías) [^71^]; ARR estimado ~$115.5M (GetLatka, sep-2025 — fuente de confianza media, SU) [^69^].
- **Errores históricos / decisiones cuestionables:** ninguno documentado públicamente de forma verificable (no se encontraron fuentes de fallos, layoffs o crisis — honestidad de evidencia). **Debilidad estratégica observable (INF):** la ausencia de gestión de proveedores, portal de solicitantes e IA autónoma en un producto con $254M de capital sugiere decisión deliberada de foco (ejecución de trabajo) más que descuido — lo que significa que cerrarán esos gaps solo si su estrategia cambia, y la nueva financiación anunciada va dirigida a IA y EAM [^68^], es decir, **hacia arriba, no hacia los gaps que DONEFIXER explota**.
- **Ventajas sostenibles:** marca frontline consolidada; escala de datos operativos (11M activos) que alimenta su IA; capital para 5+ años de carrera; canal G2/review sites dominado.
- **Difícil de replicar por DONEFIXER:** la escala de datos y la biblioteca OEM de 10K planes (requiere años y acuerdos con fabricantes). **Replicable/superable:** la experiencia móvil en sí (un equipo pequeño puede igualarla), y el vacío de proveedores/portal/WhatsApp (estructural de su modelo por asientos).

### Fiix / Rockwell Automation

- **Fortalezas reales (DC):** pionero en IA para CMMS (adquirió Alchemy IoT en 2019) [^77^]; al momento de su adquisición (dic-2020) gestionaba **2M+ activos y 6M+ OTs/año**, con crecimiento de ingresos del 70% en 2019 y >85% de ingresos recurrentes [^79^]; respaldo de Rockwell (~23,000 empleados, 100+ países) con integración al ecosistema de automatización industrial [^75^]; códigos de falla y Foresight para optimización de PMs [^27^].
- **Errores históricos / riesgos observables (DC + INF):** la venta a Rockwell (consideración total ~**$287M** según el 10-Q de Rockwell, fuente primaria SEC, 2021) [^82^] es un éxito de salida pero un riesgo estructural para sus clientes: el producto quedó subordinado a la estrategia de un gigante de automatización (priorización de roadmap ajena, foco en su ecosistema); usuarios reportan reportes básicos e IA solo desde el plan $75 [^31^]. **Lección para DONEFIXER (INF):** la dependencia de un socio industrial mayor puede limitar la neutralidad del producto — DONEFIXER permanece sensor-agnóstico y ERP-agnóstico.
- **Ventajas sostenibles:** canal de ventas de Rockwell; credibilidad industrial de 17 años (fundada 2008); integración nativa con automatización de planta.
- **Difícil de replicar:** la integración profunda con hardware de automatización (no es el objetivo de DONEFIXER en Fases 1–3). **Replicable:** la gestión de OTs/PM y los códigos de falla (el dominio canónico de DONEFIXER ya los contempla).

### Tractian

- **Fortalezas reales (DC):** Serie C de **$120M** (dic-2024, led by Sapphire Ventures; total $183.5M) [^81^][^66^]; única empresa de manufactura en la lista Forbes AI 50 [^81^]; modelo hardware+software integrado (sensores propios + plataforma), "Industrial Copilot"; fuerte presencia Brasil/LatAm y EE. UU. (HQ Atlanta).
- **Errores históricos / riesgos observables (INF):** el acoplamiento hardware+software es su fortaleza y su jaula: instalar sensores propios limita la velocidad de despliegue y excluye clientes con sensores existentes de otras marcas (misma lección documentada de UpKeep, §8); su foco es industrial-manufacturero, dejando FM/edificios/multi-sitio descubierto.
- **Ventajas sostenibles:** datos de condición de máquina propietarios (la barrera más dura del sector); marca en manufactura; capital reciente.
- **Difícil de replicar:** su base de datos de vibración/fallas de máquinas y el negocio de hardware. **Estrategia de DONEFIXER:** no competir en hardware; ser la capa de operación sensor-agnóstica que puede incluso *consumir* datos de sensores Tractian vía integración (coopetencia, Fase 4).

### Fracttal

- **Fortalezas reales (DC razonable):** presencia consolidada hispanohablante (Chile, expansión Iberia), agentes IA y analítica en planes altos [^28^]; foco mid-market LatAm — el segmento exacto de DONEFIXER, lo que lo convierte en **el competidor directo más peligroso en el mercado inicial** (INF).
- **Errores históricos / riesgos observables:** sin financiación pública comparable a MaintainX/Tractian verificada en esta consulta (no se hallaron rondas recientes — honestidad de evidencia); IA encerrada en planes altos [^28^]; WhatsApp como intake no verificado en su oferta (doc 04 §7).
- **Ventajas sostenibles:** marca y soporte en español ya establecidos; conocimiento del comprador LatAm.
- **Difícil de replicar:** su base instalada actual. **Replicable:** funcionalidad — aquí DONEFIXER debe ganar por ejecución (offline completo, WhatsApp nativo, IA con cuotas desde planes medios).

### UpKeep

- **Fortalezas reales (DC):** sensores Edge propios + inventario + TCO por ciclo de vida; adopción en equipos con activos distribuidos [^7^].
- **Errores históricos / riesgos observables (DC):** reportes públicos de usuarios sobre bugs y costo creciente con módulos/sensores (~$120/usuario con add-ons) [^32^]; acoplamiento a hardware propietario como barrera para clientes con infraestructura existente [^7^]. **Lección canónica ya incorporada a DONEFIXER:** sensor-agnóstico (doc 01 §12).
- **Difícil de replicar:** nada que un software bien diseñado no cubra; su hardware es reemplazable por integraciones.

### Limble

- **Fortalezas reales (DC):** posicionamiento "migración desde Excel" con despliegue rápido y soporte <60 s [^30^][^31^]; plan gratuito; inversión reciente en IA (Resource Planning, Asset Snap, MCP) [^33^].
- **Errores/debilidades (DC):** analítica e IA menos maduras que los líderes [^28^].
- **Lección adoptada:** la migración sin fricción es un arma de ventas — DONEFIXER la convierte en módulo (doc 63) y en mensaje central para S1.

### Facilio (el referente de IA agentiva)

- **Fortalezas reales (DC):** multi-sitio como arquitectura núcleo; agentes IA **autónomos con auditoría por decisión** (Atom); gestión de proveedores y portal de inquilinos nativos [^27^] — exactamente las capacidades que los mid-market no tienen.
- **Riesgos observables (INF):** precio por portafolio lo aleja del mid-market LatAm; menor presencia/marca en la región.
- **Lección adoptada:** la dirección de IA agentiva gobernada de DONEFIXER está validada por un jugador enterprise; la oportunidad es traerla al mid-market en español antes de que Facilio baje de segmento.

### IBM Maximo / SAP EAM (Tier-1)

- **Fortalezas reales (DC):** ecosistema, integración ERP, credibilidad enterprise de décadas [^2^][^13^].
- **Errores estructurales (DC):** implementaciones de 6–24+ meses, costos de 6–7 cifras, curvas de aprendizaje pronunciadas y resistencia de usuarios [^2^][^11^] — el origen del vacío del medio que DONEFIXER ocupa.
- **Difícil de replicar:** su credibilidad enterprise (DONEFIXER la construye con SOC 2/ISO en Etapa B, no intentando parecer enterprise antes de serlo).

### Síntesis de la sección (INF)

| Competidor | Su barrera más dura | Su flanco abierto que DONEFIXER ataca |
|---|---|---|
| MaintainX | Escala de datos + marca frontline + capital | Proveedores, portal, IA autónoma, WhatsApp, precio por asiento |
| Fiix/Rockwell | Ecosistema Rockwell + credibilidad | Subordinado a estrategia ajena; IA en plan caro |
| Tractian | Datos de condición propietarios + hardware | FM/edificios fuera de foco; acoplamiento a su hardware |
| Fracttal | Base instalada hispanohablante | IA en planes altos; sin WhatsApp verificado |
| UpKeep | Instalado con sensores propios | Acoplamiento hardware; costo por módulos |
| Limble | Migración fácil + soporte rápido | IA/analítica inmaduras |
| Facilio | IA agentiva + multi-sitio enterprise | Precio enterprise; poca presencia LatAm |
| Maximo/SAP | Credibilidad y ecosistema enterprise | 6–24 meses de implementación; UX hostil |

**Advertencia de integridad:** las cifras de clientes, activos y resultados que los vendors publican sobre sí mismos (p. ej., "34% menos downtime" de MaintainX [^72^]) son **claims de marketing no auditados** — se citan como tales, nunca como hechos independientes. Financiaciones verificadas con fuentes primarias/prensa: MaintainX $150M/$2.5B (jul-2025) [^65^][^68^], Tractian $120M (dic-2024) [^81^], Fiix ~$287M consideración (SEC, 2021) [^82^].

---

## 9. Barreras de entrada (propias y del mercado)

**Que DONEFIXER enfrenta:** confianza y marca (mitigación: pilotos con resultados medibles); cumplimiento (SOC 2 en roadmap, doc 38); costo de cambio del cliente (mitigación: herramienta de migración, doc 63); planes gratuitos de competidores (no competir en precio — DC de estrategia).
**Que DONEFIXER construye contra copias:** datos de mantenimiento estructurados por vertical (mejoran IA); motor offline validado en campo; red de proveedores por región; integraciones ERP regionales; marca bilingüe LatAm. *(INF — ninguna barrera es real hasta construirla.)*

## 10. Oportunidades

1. **El vacío del medio (INF, soportada por §7–8):** profundidad enterprise con UX frontline y precio mid-market; hoy nadie lo ocupa.
2. **IA agentiva gobernada** (triage, facturas, conciliación, reportes) disponible desde planes medios — los líderes la encierran en Enterprise o no la tienen [^27^][^31^].
3. **Offline-first de ciclo completo** como estándar, no excepción [^9^].
4. **LatAm bilingüe/multilingüe** con WhatsApp nativo, precios regionales y soporte en español/portugués [^28^][^41^].
5. **Migración desde Excel:** herramienta de importación como arma de ventas (el segmento lo valida Limble [^30^]).
6. **Solicitantes ilimitados gratuitos** como motor viral interno (patrón probado por MaintainX [^27^]).

## 11. Riesgos de mercado

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Líderes cierran los gaps de IA/proveedores antes del lanzamiento | Media | Alto | Velocidad de ejecución; foco en offline + LatAm, más difíciles de copiar que features |
| Guerra de precios / gratis agresivo | Media | Alto | No competir en precio (DC); valor en agentes y migración |
| Adopción frontline menor a la esperada | Media | Crítico | Validación con técnicos reales en Fase 0–1 (doc 15/16); diseño ≤3 toques |
| Ciclo de venta enterprise más largo de lo previsto | Alta | Medio | Modelo de negocio arranca mid-market (doc 03) |
| Cambios regulatorios de datos (LatAm/EE. UU.) | Media | Medio | Privacy by design, residency opcional (docs 36/37) |

## 12. Posicionamiento recomendado

**Recomendación (con fundamento, alternativas, riesgos, impacto, dependencias y decisión requerida):**

> *"DONEFIXER es la plataforma de mantenimiento y operaciones que funciona donde trabajan los técnicos — sin internet, en español, por WhatsApp — con la profundidad que las operaciones enterprise exigen y una IA que ejecuta el trabajo administrativo con auditoría completa."*

- **Fundamento:** secciones 7–10; los gaps son estructurales de los líderes, no de roadmap [^27^].
- **Alternativas evaluadas:** (a) competir por precio — descartada, insostenible contra planes gratis; (b) competir solo en IA — descartada, la IA se commoditiza; (c) nicho vertical único — aplazada a Etapa C.
- **Riesgos:** que el vacío del medio se cierre; que "hacer todo" diluya la ejecución (mitigación: fases del roadmap).
- **Impacto:** define producto, pricing y marketing de los próximos 3 años.
- **Dependencias:** doc 01 (visión), doc 03 (modelo de negocio), roadmap (doc 69).
- **Decisión requerida del Fundador:** aprobar este posicionamiento (PD).

**Mapa de posicionamiento (versión corregida por auditoría H-03):** la versión anterior usaba coordenadas numéricas sin criterio medible y fue invalidada. Se reemplaza por una declaración cualitativa verificable: los líderes Tier-1 puntúan alto en profundidad y bajo en adopción frontline; los CMMS móviles, al revés; DONEFIXER se construye explícitamente contra las capacidades de la matriz §7 donde **todos** los directos mid-market tienen ❌ o 🟡 (proveedores, portal, IA agentiva, offline completo, WhatsApp). Un mapa cuantitativo solo se republicará cuando exista una metodología de scoring documentada y reproducible (PD para Ola 2).

## 13. Nivel de confianza global del documento

| Sección | Confianza | Motivo |
|---|---|---|
| 4 (tamaños) | Media | Consultoras comerciales, metodología no auditable |
| 5 (regiones) | Media-alta | Hechos + inferencias explícitas |
| 7 (matriz/precios) | Alta a la fecha de consulta | Fuentes públicas citadas; decae con el tiempo → revisión trimestral |
| 8–9 | Alta | Convergencia de fuentes |
| 10–12 | Inferencial | Tesis estratégica, validable solo con pilotos |

## 14. Referencias cruzadas
Alimenta: 01 (Product Vision), 02 (Charter), 03 (Business Model), 63 (Migration Strategy), 69 (Roadmap). Depende de: 00 (gobernanza), Auditoría AUD-00. Supersede: documento 01 de la investigación previa (contenido válido migrado y corregido).

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Versión canónica Ola 1: corrige coordenadas inventadas (H-03), re-etiqueta consultoras como SU, añade niveles de confianza, fecha de consulta y revisión trimestral. Nombre oficial DONEFIXER aplicado |
| 1.1 | 2026-07-29 | **Ampliación por aprobación condicional Ola 1:** nueva §8 bis — análisis profundo por competidor (fortalezas reales, errores históricos verificables, ventajas sostenibles, capacidades difíciles de replicar) con fuentes primarias: MaintainX Serie D $150M/$2.5B [^65^][^68^], Tractian $120M [^81^], Fiix ~$287M consideración (SEC) [^82^]. Aprobación pendiente de confirmación final del Fundador |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 1** por el Fundador. Base estratégica oficial; no congelado: futuras modificaciones por gobierno documental (evidencia, trazabilidad, ADR, versionado, motivo) |
