# DONEFIXER — Auditoría Fundacional Independiente (v1.0)

> **Nombre oficial:** DONEFIXER · **Categoría:** Enterprise Maintenance & Operations Platform
> **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Documento:** AUD-00 — Auditoría Fundacional y Expansión Documental · **Versión:** 1.0 · 2026-07-29
> **Objeto de auditoría:** los 6 documentos fundacionales previos (suite `donefixter/` 01–05 + índice maestro 00 de `donefixer/`).
> **Posición del auditor:** independiente y adversarial. Ninguna decisión previa se defiende por inercia; cada una se re-justifica con evidencia o se reabre. **No se genera código, DDL, migraciones ni infraestructura en este documento.**
> **Regla de evidencia:** DC = decisión/dato confirmado con fuente · SU = supuesto o estimación · PD = pendiente de decisión · HE = hallazgo de esta auditoría.

---

## A. Resumen ejecutivo de la auditoría

La suite fundacional de DONEFIXER es **sólida en estrategia y dominio, pero sobre-arquitecturada para la Fase 1 y con afirmaciones que no resisten verificación**. La auditoría produjo **41 hallazgos** (7 críticos, 12 altos, 14 medios, 8 bajos).

Las cinco conclusiones que cambian el plan:

1. **El motor de sincronización propio (ADR-002) no está justificado y se reabre.** La re-verificación de julio 2026 muestra que PowerSync —descartado en la investigación previa por costo— ofrece un **tier gratuito funcional, un plan Pro de $49/mes, edición self-hosted gratuita (Open Edition, licencia FSL), SDKs open-source Apache 2.0 para Flutter, React Native, Web y .NET (beta), y cumplimiento SOC 2 + HIPAA logrado en enero 2026** [^50^][^53^]. Construir un motor propio es el riesgo técnico nº 1 del proyecto (ya identificado como R1 en el índice maestro) y consumiría 6–12 meses de ingeniería especializada que un equipo fundador pequeño no tiene. **La decisión correcta se invierte: adoptar PowerSync (self-hosted Open Edition o Cloud) y reservar motor propio solo como estrategia de salida documentada.**

2. **El stack de Fase 1 tiene sobrearquitectura demostrable.** Kafka, ClickHouse, Kubernetes, TimescaleDB, dos lenguajes backend y despliegue soberano están justificados a escala enterprise (Fase 3+) pero **no tienen ningún requisito confirmado de Fase 1 que los exija**. La auditoría recomienda la arquitectura por etapas A→B→C (sección I), que reduce el costo operativo inicial estimado de ~$1.500–3.000/mes a ~$150–500/mes (SU) y elimina 3 especializaciones humanas que el equipo inicial no posee.

3. **Varias afirmaciones de la investigación previa se degradan de DC a SU.** El mapa de posicionamiento competitivo usaba coordenadas inventadas; el "TCO 18% menor de Flutter" y los plazos "24–28 sem vs 14" carecían de fuente verificable; las cifras de consultoras (CAGR 11.1%, $8.77B EAM 2033) provienen de reportes comerciales de metodología no auditable y deben presentarse como rangos orientativos, no hechos. La matriz de trazabilidad completa está en la sección 1.

4. **Omisiones estructurales confirmadas:** el modelo de identidad "una cuenta → un usuario → múltiples membresías → permisos contextuales" no estaba diseñado (los portales 38–42 se insinuaban como apps separadas, lo que se corrige); faltaban threat model formal, gobierno de IA con clasificación de riesgo y lista de prohibiciones, programa legal (DPA, subprocesadores, ToS), i18n más allá de ES/EN (se añade FR, PT, criollo haitiano), FinOps con escenarios, y 70 documentos del índice expandido (sección J) que sustituyen al índice previo.

5. **Lo que sí resiste la auditoría:** la tesis de mercado (vacío entre Tier-1 enterprise y CMMS mobile-first), el dominio canónico (activos jerárquicos, máquina de estados de OT, códigos de falla), multi-tenancy pool+RLS con tier híbrido (con endurecimientos, sección 5), PostgreSQL como sistema de registro, monolito modular, la regla "IA como capa gobernada, no autoridad", offline-first como principio (aunque cambie su implementación), y la gobernanza documental (DC/SU/PD).

**Veredicto:** el proyecto NO está listo para programar. Está listo para ejecutar la Ola de documentación corregida (sección K) con las decisiones reabiertas (sección D) resueltas por el Fundador (sección N).

---

## B. Tabla de hallazgos clasificados

| ID | Severidad | Hallazgo | Documento afectado | Acción |
|---|---|---|---|---|
| H-01 | 🔴 Crítico | ADR-002 (sync propio) decidido con información desactualizada: PowerSync tiene tier gratis, $49/mes Pro, Open Edition self-hosted gratuita y SOC2+HIPAA (ene-2026) [^50^][^53^] | 19/27 | Reabrir ADR-002 → adoptar PowerSync |
| H-02 | 🔴 Crítico | Kafka + ClickHouse + K8s + TimescaleDB en Fase 1 sin requisito confirmado que los exija; sobrecosto y sobrecomplejidad | 12, 16, 17, 21 | Aplazar a Etapa B/C (sección I) |
| H-03 | 🔴 Crítico | Mapa de posicionamiento con coordenadas inventadas presentadas visualmente como análisis | 04 | Regenerar con criterios medibles o eliminar ejes numéricos |
| H-04 | 🔴 Crítico | Sin threat model formal; la seguridad era una lista de controles, no un modelo de amenazas por riesgo real | 34, 35 | Crear docs 34/35 (sección J) |
| H-05 | 🔴 Crítico | Gobierno de IA sin clasificación de riesgo ni lista de prohibiciones explícitas | 32, 33 | Crear doc 33 con matriz bajo/medio/alto/prohibido |
| H-06 | 🔴 Crítico | Modelo de identidad "1 cuenta → N membresías → permisos contextuales" ausente; portales insinuados como apps separadas | 19, 43 | Rediseñar: una app configurable por permisos |
| H-07 | 🔴 Crítico | Programa legal inexistente: ToS, DPA, subprocesadores, privacidad, propiedad intelectual, tratamiento de fotos/voz/firmas/datos laborales | 37 | Crear doc 37 + revisión legal por jurisdicción (no es asesoría jurídica) |
| H-08 | 🟠 Alto | ElectricSQL —citado como "referencia de diseño y fallback"— tiene CVE-2026-40906 (inyección SQL crítica, corregida en 1.5.0) y reportes de arquitectura frágil (long polling); se retira como fallback [^57^][^52^] | 27 | Sustituir fallback por Zero (Rocicorp) o WatermelonDB+backend propio |
| H-09 | 🟠 Alto | Flutter elegido sin comparación objetiva contra RN/Expo con PowerSync, que hoy ofrece SDK oficial y background sync documentado [^50^][^51^] | 23 | Reevaluación en sección 3 — resultado: se mantiene Flutter con condiciones |
| H-10 | 🟠 Alto | Dos lenguajes backend (.NET + Python) desde el día 1 duplican CI, DevOps y contratación | 24 | Python se aplaza a Etapa B; IA inicial vía APIs externas desde .NET |
| H-11 | 🟠 Alto | Cifras de consultoras (CAGR 11.1%, EAM $8.77B 2033) presentadas como hechos; son estimaciones comerciales | 03, 04 | Re-etiquetar SU con rangos y fuente/fecha |
| H-12 | 🟠 Alto | Sin FinOps: no hay escenarios de costo por etapa ni costo unitario de IA | 60 | Crear doc 60 con escenarios A/B/C |
| H-13 | 🟠 Alto | i18n limitada a ES/EN; el mercado inicial (Caribe incluido) requiere FR, PT y criollo haitiano; falta traducción de chat conservando original | 13, 43 | Ampliar docs 13 y módulo de traducción |
| H-14 | 🟠 Alto | Resolución de conflictos: la tabla por entidad era correcta, pero faltaban idempotencia, ordenamiento causal, recuperación parcial, deduplicación, dispositivos compartidos, revocación y resolución humana | 27 | Incorporar los 17 puntos de la sección 4 |
| H-15 | 🟠 Alto | Multi-tenant: RLS declarado sin pruebas automatizadas de aislamiento, sin claves por tenant, sin data residency ni restauración por tenant documentadas | 26 | Sección 5: endurecimiento obligatorio |
| H-16 | 🟠 Alto | Glosario canónico insuficiente: faltan tenant/organización/programa/propiedad/instalación/sitio/unidad/membresía/perfil — riesgo de colisión semántica CMMS/EAM/FM/FSM | 13, 14 | Glosario ampliado (sección 6) |
| H-17 | 🟠 Alto | Sin clasificación de datos ni política de retención/legal hold | 44, 45 | Crear docs 44/45 |
| H-18 | 🟠 Alto | SLO "99.9% → 99.95%" y latencias fijados sin justificar costo | 54, 55 | Re-derivar SLOs desde requisitos de cliente, no aspiración |
| H-19 | 🟡 Medio | "TCO 18% menor Flutter", "24–28 sem vs 14 sem" sin fuente | 23 | Etiquetar SU o eliminar |
| H-20 | 🟡 Medio | Benchmarks MTTR/MTBF/OEE de una única fuente comercial; rangos plausibles pero no normativos | 03, 51 | Presentar como referenciales (SU) |
| H-21 | 🟡 Medio | Roles incompletos: faltaban propietario de plataforma, admin global DONEFIXER, despachador, compras, finanzas, auditor, seguridad, cumplimiento, soporte, API service account | 19 | Matriz ampliada (sección 7) |
| H-22 | 🟡 Medio | Módulos de procurement incompletos: recepción/devoluciones, conciliación de facturas, garantías no estaban como módulos | 43 | Incorporados al índice de módulos (sección 8) |
| H-23 | 🟡 Medio | "Salida en vivo <7 días" era benchmark de mercado, no capacidad propia; se presentaba como compromiso | 64 | Re-etiquetar como objetivo SU con proceso de onboarding (doc 64) |
| H-24 | 🟡 Medio | Despliegue soberano on-premise prometido sin analizar su costo de soporte (multiplica QA y release) | 61, 66 | Posponer a Etapa C + contrato enterprise específico |
| H-25 | 🟡 Medio | WhatsApp como canal: sin análisis de costos por conversación (Meta cobra por plantilla/conversación) ni de cumplimiento | 60, módulo | Costear en FinOps; diseño de fallback SMS/email |
| H-26 | 🟡 Medio | Sin estrategia de pagos/facturación SaaS (Stripe vs. procesador regional LatAm, impuestos, monedas) | 43, 60 | Doc de billing + PD para el Fundador |
| H-27 | 🟡 Medio | Observabilidad móvil (crashes, ANRs, batería, almacenamiento) no definida | 54 | Incorporar a doc 54 |
| H-28 | 🟡 Medio | Contradicción: "IA incluida desde plan profesional" vs. costo de LLMs sin modelo FinOps que lo sustente | 03, 60 | Resolver con límites de uso por plan (doc 60) |
| H-29 | 🟡 Medio | Contradicción: roadmap previo pedía "monolito modular" y a la vez listaba 8 servicios/estores separados en la figura de arquitectura | 12 | La figura se reinterpreta como vista lógica, no de despliegue |
| H-30 | 🟡 Medio | Estado "verificada" de OT y "en espera por repuesto": correctos, pero sin quién puede transicionar (máquina de estados sin matriz de transición por rol) | 43 (módulo OT) | Matriz de transición en spec de módulo |
| H-31 | 🟡 Medio | Sin estrategia de importación desde competidores (MaintainX/Fiix/UpKeep exportan CSV; Excel es el competidor real) | 63 | Doc 63 con mapeo de entidades |
| H-32 | 🟡 Medio | Criollo haitiano y FR/PT ausentes también de contenido legal por jurisdicción | 13, 37 | Incorporar a i18n y legal |
| H-33 | 🟡 Medio | Sin plan de gestión de menores aunque sea "no aplica" documentado | 37 | Declaración explícita en doc 37 |
| H-34 | 🟢 Bajo | Nombre de carpeta de entregables `donefixter` vs oficial `donefixer` | — | Corregido en esta entrega |
| H-35 | 🟢 Bajo | Glosario ES/EN sin francés/portugués | 13 | Ampliar |
| H-36 | 🟢 Bajo | Sin status page ni modelo de soporte | 55, 65 | Docs 55/65 |
| H-37 | 🟢 Bajo | Postmortems citados sin plantilla ni proceso | 59 | Doc 59 |
| H-38 | 🟢 Bajo | "Bus-factor" identificado como riesgo sin acción concreta de contratación/comunidad | 69 | PD para el Fundador |
| H-39 | 🟢 Bajo | Figura de sync sin manejo de archivos binarios grandes en redes lentas (se mencionaba, sin protocolo) | 27 | Sección 4.6 |
| H-40 | 🟢 Bajo | Sin política de uso aceptable ni suspensión/terminación | 37 | Doc 37 |
| H-41 | 🟢 Bajo | Control de versiones documental presente pero sin cadencia de revisión | 00 | Revisión trimestral obligatoria |

---

## C. Decisiones que deben mantenerse (confirmadas por la auditoría)

| # | Decisión | Por qué resiste la auditoría |
|---|---|---|
| C-1 | **Tesis de mercado:** vacío entre EAM enterprise pesado y CMMS mobile-first superficial | Corroborada por múltiples fuentes independientes de la investigación previa |
| C-2 | **Offline-first como principio de producto** (no su implementación propia) | Requisito real del dominio (sótanos, plantas, LatAm); diferenciador confirmado |
| C-3 | **PostgreSQL como sistema de registro** con RLS (endurecido, §5) | Estándar de facto; PowerSync lo requiere (`wal_level=logical`) [^50^]; pgvector evita una DB vectorial prematura |
| C-4 | **Multi-tenancy pool + tenant_id con vía híbrida a DB dedicada** | Correcto para B2B SaaS nuevo; el endurecimiento corrige sus vacíos, no su dirección |
| C-5 | **Monolito modular antes que microservicios** | Reafirmado por el principio de esta auditoría: "comenzar modular, observable y extraíble" |
| C-6 | **Modelo de dominio canónico:** activos jerárquicos (ltree), máquina de estados de OT, códigos de falla problema/causa/acción, medidores de primera clase, evidencias aditivas | Coherente con SMRP/ISO 55000 y con la taxonomía de la industria; sin contradicciones detectadas |
| C-7 | **IA como capa de asistencia gobernada, jamás autoridad autónoma** | Alineada con la dirección del mercado (agentes con auditoría) y con la sección 11 de gobierno |
| C-8 | **API-First, eventos de dominio, exportación completa por tenant ("salida digna")** | Reduce lock-in percibido y acelera ventas enterprise |
| C-9 | **Gobernanza documental DC/SU/PD y trazabilidad** | Validada como necesaria por esta propia auditoría |
| C-10 | **Español primero, dominio en inglés canónico** | Se mantiene y se amplía a FR/PT/HT (sección 13) |
| C-11 | **No competir en precio; diferenciar en offline, IA gobernada y LatAm** | La guerra de precios contra planes gratuitos es inasumible para un entrante |
| C-12 | **Disciplina de fases con criterios de salida medibles** | Reforzada por la auditoría de roadmap (sección 16) |

---

## D. Decisiones que deben reabrirse

| # | Decisión previa | Motivo de reapertura | Nueva recomendación |
|---|---|---|---|
| D-1 | **ADR-002: motor de sync propio** | Decidido con datos desactualizados de PowerSync [^50^][^53^] | **Adoptar PowerSync** (Open Edition self-hosted o Cloud Pro $49/mes); escrituras vía backend propio (control total de lógica de conflicto, que es donde vive el valor); motor propio solo como exit strategy si PowerSync depreca o su licencia FSL cambia |
| D-2 | **Kafka en Fase 1** | Sin requisito confirmado; outbox + cola simple (cola de PostgreSQL/Redis) cubre webhooks y notificaciones hasta Etapa B | Aplazar; diseñar eventos de dominio con esquema desde ya (eso sí se mantiene) para no bloquear Kafka futuro |
| D-3 | **ClickHouse en Fase 1** | Dashboards iniciales caben en PostgreSQL con rollups y réplica de lectura; ClickHouse cuando el volumen lo demuestre (métrica: >50M filas de eventos o p95 de dashboards >2s) | Aplazar a Etapa B con criterio de activación medible |
| D-4 | **Kubernetes en Fase 1** | Un equipo pequeño opera mejor con PaaS (Render/Fly.io/Railway o VM única + Docker Compose) | Etapa A: PaaS/VM; K8s en Etapa B/C cuando haya SRE |
| D-5 | **Python/FastAPI separado en Fase 1** | Duplica pipeline y contratación; la IA inicial (triage, resúmenes, RAG básico) se consume vía APIs de LLM desde el backend .NET | Aplazar servicio Python a Etapa B (ML predictivo propio) |
| D-6 | **Flutter (ver sección 3)** | Reevaluado objetivamente: se mantiene **condicionado** (ver §3) | Flutter confirmado, con RN/Expo como alternativa documentada si la contratación Dart falla en 2 búsquedas |
| D-7 | **"IA incluida desde plan profesional"** | Insostenible sin límites | IA con cuotas por plan + overage; documentar en billing |

---

## E. Decisiones que deben aplazarse (con criterio de activación)

| # | Decisión | Aplazar hasta | Criterio de activación medible |
|---|---|---|---|
| E-1 | Kubernetes / multi-AZ activo-activo | Etapa B | Equipo ≥3 ingenieros de plataforma o cliente enterprise que lo exija contractualmente |
| E-2 | Kafka | Etapa B | >5 consumidores de eventos o necesidad de replay/CDC a OLAP |
| E-3 | ClickHouse | Etapa B | >50M filas de eventos/lecturas o p95 dashboards >2 s |
| E-4 | TimescaleDB / IoT MQTT | Etapa B (Fase 4 del roadmap) | Primer cliente con sensores contratados |
| E-5 | Servicio Python + MLflow | Etapa B | Primer modelo ML propio (anomalías/forecast) con datos reales suficientes |
| E-6 | Despliegue soberano on-premise | Etapa C | Contrato enterprise que lo pague (el soporte on-prem multiplica QA) |
| E-7 | CRDT para texto colaborativo (Yjs) | Etapa B | Edición colaborativa simultánea como requisito confirmado de clientes |
| E-8 | Marketplace de integraciones / plataforma de extensiones | Etapa C | ≥10 integraciones nativas estables |
| E-9 | 21 CFR Part 11 / verticales reguladas | Etapa C | Primer cliente farma/salud en pipeline |
| E-10 | Gemelos digitales / AR | Años 5+ | Fuera del horizonte de planificación seria actual |

---

## F. Contradicciones encontradas

1. **"Monolito modular" vs. figura de arquitectura con 8 componentes distribuidos** (Kafka, ClickHouse, Timescale, vector DB, Redis, gateway, servicio IA): la figura se re-interpreta como vista lógica de capacidades, no de despliegue; el despliegue de Etapa A es un único backend + PostgreSQL + PowerSync + Redis.
2. **"IA incluida desde el plan profesional" vs. "routing por costo para proteger margen"**: sin cuotas, ambas no pueden ser ciertas. Se resuelve con límites por plan (D-7).
3. **"El sync es el producto, no se terceriza" vs. evidencia de que tercerizar el transporte (PowerSync) y conservar la lógica de conflictos es la arquitectura estándar de producción**: el valor diferencial vive en las reglas de negocio de resolución, no en el pipe de replicación WAL→SQLite [^50^][^56^].
4. **"Salida en vivo <7 días" como compromiso** vs. ausencia total de proceso de onboarding/migración que lo haga posible: se convierte en objetivo (SU) con documento 64/63 que lo sustente.
5. **"Multi-modelo con modelos locales edge para LatAm" vs. offline-first**: los modelos LLM locales en dispositivos de gama media latinoamericana no son viables hoy (SU); el modo offline degrada a reglas + IA diferida (sección 11).
6. **Portal de solicitantes "gratuito e ilimitado" vs. modelo por usuario**: se aclara — los solicitantes no son asientos de pago, son contactos con acceso limitado por portal (matriz de roles, §7).

---

## G. Omisiones (consolidadas, además de las del índice maestro previo)

1. Threat model formal con los 25 vectores (§10 de este encargo) — **doc 35**.
2. Gobierno de IA con clasificación bajo/medio/alto/prohibido y prohibiciones explícitas — **doc 33**.
3. Programa legal completo (ToS, DPA, subprocesadores, AUP, propiedad intelectual, tratamiento de fotos/ubicación/voz/firmas/datos laborales, reclamaciones, requerimientos legales) — **doc 37**. *Nota: ningún texto de esta suite constituye asesoría jurídica; los documentos legales requieren revisión de abogados licenciados en cada jurisdicción de operación antes del lanzamiento.*
4. Clasificación de datos y retención/legal hold — **docs 44, 45**.
5. Modelo de identidad con membresías múltiples y permisos contextuales — **doc 19**.
6. Matriz de transiciones de estado de OT por rol — **spec de módulo (43)**.
7. Estrategia de importación/migración (CSV, Excel, competidores) — **doc 63**.
8. FinOps con escenarios A/B/C y costo unitario de IA — **doc 60**.
9. Billing SaaS: procesador de pagos, impuestos, monedas LatAm — **doc de módulo billing + 60**.
10. Observabilidad móvil (crashes, ANR, batería, storage) — **doc 54**.
11. Service blueprints (no solo journeys) — **doc 17**.
12. North Star Metrics — **doc 08**.
13. Data residency y transferencias internacionales — **docs 26, 36, 37**.
14. Gestión de dispositivos compartidos y revocación con borrado local — **doc 27** (§4.6 de esta auditoría).
15. Política de entrenamiento IA con datos de cliente y opt-out — **doc 33**.
16. Status page y comunicación de incidentes a clientes — **docs 55, 59, 65**.
17. Cadencia de revisión documental (trimestral) — **doc 00**.

---

## H. Riesgos de sobrearquitectura

| Riesgo | Síntoma en la suite previa | Corrección |
|---|---|---|
| **Currículum-driven design** | K8s + Kafka + ClickHouse + Timescale + 2 lenguajes + vector DB en Fase 1 | Etapa A mínima viable operable (§I) |
| **Inventar infraestructura diferenciadora** | Motor de sync propio | PowerSync + lógica de conflictos propia (D-1) |
| **Premature distribution** | Microservicios insinuados | Monolito modular (C-5) con eventos esquematizados |
| **SLOs aspiracionales sin cliente** | 99.95% | SLOs derivados de contratos reales (H-18) |
| **Multi-cloud/portabilidad como objetivo gratuito** | "K8s para portabilidad" | Portabilidad vía contenedores estándar; multi-cloud nunca fue requisito confirmado |
| **Diseñar para millones antes del primer piloto** | "10K tenants, 100M OTs" como dimensionador inicial | Etapa A dimensionada para 50 tenants / 5K usuarios; la arquitectura documenta el camino, no lo pre-construye |

---

## I. Arquitectura recomendada por etapas

### Etapa A — Inicial modular de bajo costo (Fases 0–1, 0–50 tenants)

```
App Flutter (iOS/Android)          Web React (PWA)
        │                                │
        └──── PowerSync SDK ◄────────────┘
                    │ (WAL logical replication)
        ┌───────────┴────────────┐
        │  PowerSync (Open Edition │
        │   self-hosted o Cloud)   │
        └───────────┬────────────┘
   ┌────────────────┼─────────────────┐
   │  Backend .NET monolito modular   │  ← escrituras, reglas de conflicto,
   │  (API REST + lógica + jobs)      │    RBAC/RLS, IA vía API externa
   └────────────────┼─────────────────┘
        PostgreSQL 16 (RLS, ltree, pgvector, outbox)
        Redis (caché/colas cortas) · S3 (adjuntos)
        PaaS o 1–2 VMs + Docker · CI/CD GitHub Actions
```
- **Costo objetivo:** $150–500/mes (SU). **Equipo:** 1–3 personas.
- IA: llamadas a API LLM desde .NET con gateway ligero propio (abstracción de proveedor), cuotas por tenant.
- Analítica: vistas materializadas + réplica de lectura si hace falta.
- Eventos: tabla outbox + worker; webhooks con firma HMAC.

### Etapa B — Crecimiento intermedio (50–500 tenants)
Activa por criterio (§E): réplicas gestionadas, ClickHouse para analítica, Kafka/Redpanda si >5 consumidores, servicio Python de ML, Kubernetes gestionado (EKS/GKE/AKS), TimescaleDB si entra IoT, observabilidad OTel completa, SLOs contractuales, SOC 2 Type I→II. Costo: $2K–8K/mes (SU).

### Etapa C — Enterprise alta escala (500+ tenants)
Tier híbrido con DB dedicada para cuentas reguladas, multi-región, data residency, despliegue soberano opcional, marketplace, verticales (21 CFR Part 11), SSO/SCIM, ISO 27001, DR activo-pasivo cross-region, equipos por dominio y extracción selectiva de servicios **solo donde las métricas lo demuestren**.

**Regla permanente:** ningún componente de Etapa B/C se introduce en A sin el criterio de activación cumplido y un ADR que lo registre.

---

## 1. Auditoría de evidencia (matriz de trazabilidad)

| Afirmación previa | Fuente | Fecha fuente | Estado | Corrección |
|---|---|---|---|---|
| CMMS $1.29–1.42B, CAGR 11.1% a $2.41B (2030) | Reportes comerciales (Grand View/Mordor-type) [^14^] | 2024–2025 | **SU** — metodología no auditable | Usar como rango orientativo con fuente y fecha |
| EAM $4.4B (2025) → $8.77B (2033), CAGR 9% | Data Insights Reports [^8^] | 2025 | **SU** — consultora menor | Idem; nunca como hecho |
| Precios Fiix $45/$75, MaintainX ~$20/$65, Limble $28/$69 | Sitios oficiales de precios [^29^][^27^][^30^] | 2025–2026 | **DC** a esa fecha; **riesgo de desactualización** | Re-verificar trimestralmente; citar fecha |
| "MaintainX valoración $2.5B, #1 G2 Winter 2026" | Prensa/G2 [^33^] | 2026 | **DC** con fecha | Mantener con fecha |
| Vacíos de MaintainX/Fiix (proveedores, portal, IA autónoma) | Análisis comparativo de review sites [^27^] | 2026 | **DC razonable**, pero dinámico | Re-verificar cada 6 meses; los competidores cierran gaps |
| Mapa de posicionamiento (coordenadas X/Y) | **Inventado** | — | **Inválido (H-03)** | Regenerar con criterios medibles o sin ejes numéricos |
| "Flutter TCO 18% menor", "24–28 sem vs 14" | Sin fuente verificable | — | **SU/eliminar** | Eliminar cifras; mantener argumento cualitativo |
| Benchmarks MTTR/MTBF/OEE/PMP world-class | Fuente comercial única [^37^][^38^] | 2025 | **SU** plausible | Presentar como referenciales, no normativos |
| Realm Device Sync deprecado sept-2024 | Anuncio oficial MongoDB | 2024 | **DC** | Mantener (lección de dependencia) |
| PowerSync: gratis/$49, Open Edition FSL, SOC2+HIPAA ene-2026, SDKs Flutter/RN/Web/.NET | Documentación y prensa PowerSync [^50^][^53^] | feb–jul 2026 | **DC** (nuevo, revierte ADR-002) | Incorporar a ADR-002 reabierto |
| ElectricSQL como "fallback" | CVE-2026-40906 + reportes de fragilidad [^57^][^52^] | 2026 | **Retirado** | Fallback = Zero o DIY sobre PowerSync pattern |
| Costo brecha de datos $4.44M | IBM Cost of a Data Breach | 2025 | **DC** con fuente anual | Mantener con año |
| "70% de controles comunes SOC2/ISO/HIPAA" | Literatura de compliance [^46^] | 2025 | **SU** razonable | Mantener como estimación |

**Regla resultante:** ninguna cifra entra a la suite sin (fuente, fecha, etiqueta DC/SU). Las cifras de consultoras se presentan como "estimaciones comerciales orientativas", jamás como hechos.

---

## 2. Auditoría del stack (10 preguntas por tecnología)

| Tecnología | Requisito confirmado que resuelve | ¿Fase 1? | Alternativa más simple | Costo ops | Especialización | Salida | Veredicto |
|---|---|---|---|---|---|---|---|
| **Flutter** | App móvil nativa offline, 1 codebase iOS/Android (DC) | Sí | RN/Expo (equivale; ver §3) | Bajo | Dart | Reescritura parcial; contratos API lo acotan | **Mantener con condición (D-6)** |
| **React+TS web** | Admin web, ecosistema, talento (DC) | Sí | — | Bajo | Común | Framework agnóstico vía API | **Mantener** |
| **.NET 8 backend** | Núcleo transaccional de larga vida, tipado, tooling enterprise (DC razonada) | Sí | Node/NestJS (equivale) | Bajo-medio | C# | API-First lo hace reemplazable por módulo | **Mantener** |
| **Python (servicio IA)** | ML propio | **No (E-5)** | Llamadas LLM API desde .NET | Medio | ML/Python | Frontera API/eventos | **Aplazar a Etapa B** |
| **PostgreSQL+RLS** | Sistema de registro multi-tenant (DC) | Sí | — | Bajo | Común | Estándar SQL | **Mantener endurecido (§5)** |
| **Kafka** | Ninguno confirmado en Fase 1 | **No (E-2)** | Outbox+worker, cola Redis | Alto | Streaming | Eventos esquematizados desde ya | **Aplazar** |
| **ClickHouse** | Ninguno en Fase 1 | **No (E-3)** | Vistas materializadas PG + réplica | Medio-alto | OLAP | CDC lo alimenta después | **Aplazar** |
| **TimescaleDB/IoT** | Ninguno hasta Fase 4 | **No (E-4)** | Tablas PG particionadas | Medio | TSDB | Extensión PG, migración natural | **Aplazar** |
| **MQTT** | IoT Fase 4 | No | — | Medio | IoT | Estándar | **Aplazar** |
| **Motor sync propio** | Offline-first (DC) — **pero PowerSync lo resuelve** | **No (D-1)** | **PowerSync** [^50^][^53^] | Bajo (self-host) | — | SDKs Apache 2.0; patrón documentado permite DIY futuro | **Revertir: adoptar PowerSync** |
| **Kubernetes** | Ninguno hasta Etapa B | **No (E-1)** | PaaS/VM+Docker | Alto | K8s/SRE | Contenedores estándar | **Aplazar** |
| **Redis** | Caché, colas cortas, presencia | Sí | Colas PG (pgmq) | Bajo | Común | Trivial | **Mantener (opcional en A)** |
| **pgvector** | RAG sobre manuales/historial | Sí (ligero) | Vector DB externa | Bajo | Común | Export embeddings | **Mantener; Qdrant solo a escala** |

---

## 3. Auditoría mobile (objetiva)

| Criterio | Flutter | RN + Expo | Nativo Swift/Kotlin | PWA |
|---|---|---|---|---|
| Experiencia nativa | Alta (render propio, consistente) | Alta (componentes nativos) | Máxima | Media (complemento, no sustituto) |
| Cámara/GPS/firma/biometría | Maduro | Maduro | Máximo | Limitado |
| Almacenamiento local | SQLite (PowerSync SDK Flutter oficial) [^53^] | SQLite (PowerSync SDK RN oficial) [^53^] | SQLite/Room/CoreData | IndexedDB (límites iOS) |
| Background sync | Mismas restricciones OS (iOS ~30s, fetch 15min+, Android FGS/WorkManager) [^49^][^55^] | Idénticas (expo-background-task + PowerSync documentado) [^51^] | Idénticas restricciones, más control | Muy limitado |
| Rendimiento | Excelente determinista | Muy bueno (nueva arquitectura) | Máximo | Medio |
| Contratación LatAm | **Menor pool Dart** | **Mayor pool JS/TS** | 2 equipos | Pool web |
| Costo 10 años | 1 codebase | 1 codebase + comparte TS con web | 2 codebases | Incluido en web |
| Publicación stores | Normal | Normal (+OTA EAS) | Normal | No aplica igual |

**Conclusión (D-6):** funcionalmente Flutter y RN/Expo **empatan** para DONEFIXER — ambos tienen SDK PowerSync oficial y las mismas limitaciones de background del OS. El factor decisivo ya no es técnico sino de **equipo y ecosistema**: RN/Expo comparte lenguaje con la web y tiene mayor mercado de contratación; Flutter ofrece UI más determinista y consistente en Android de gama media (dispositivo dominante del técnico LatAm). **Decisión: se mantiene Flutter** por la consistencia de UI en dispositivos modestos y su modelo de renderizado, **condicionado a**: si en dos procesos de contratación no se consigue talento Dart/Flutter, se conmuta a RN/Expo sin costo arquitectónico (los contratos API y PowerSync son idénticos). **PD final del Fundador** (sección N). La PWA existe como complemento para portales ligeros (solicitante/proveedor), nunca como sustituto de la app del técnico.

---

## 4. Auditoría offline-first (17 puntos obligatorios)

**Decisión reabierta y resuelta (D-1):** comparativa de alternativas maduras:

| Alternativa | Estado 2026 | Veredicto |
|---|---|---|
| **PowerSync** | Tier gratis, Pro $49/mes, Open Edition self-hosted (FSL), SDKs Apache 2.0 (Flutter/RN/Web/Kotlin/Swift/.NET beta), SOC2+HIPAA (ene-2026) [^50^][^53^] | **Adoptar** |
| ElectricSQL | CVE-2026-40906 (SQLi crítica, fix 1.5.0); reportes de long-polling frágil y escrituras DIY [^57^][^52^] | Descartar |
| Zero (Rocicorp) | Maduro, buena reputación de producción [^52^] | Fallback documentado |
| WatermelonDB | Mantenido (Nozbe lo usa en producción) pero sync DIY [^61^] | Fallback si RN |
| RxDB | Premium comercial para features enterprise [^61^] | Descartar (licencia) |
| Realm/MongoDB Device Sync | Deprecado 2024 | Descartado (DC) |
| Motor propio | 6–12 meses de ingeniería especializada | Solo como exit strategy |

**Los 17 puntos que el documento 27 (Offline Sync Architecture) debe especificar** — independientemente del motor, porque la mayoría viven en *nuestro* backend de escrituras:

1. **Conflictos por entidad y por campo** (matriz: estados OT=servidor autoritativo+máquina de estados; evidencias=aditivas; contadores=deltas; texto largo=CRDT aplazado E-7; borrados=tombstones).
2. **Idempotencia:** `operation_id` UUID por mutación; el backend deduplica.
3. **Versionado:** `version` por fila + If-Match.
4. **Tombstones** con retención y purga programada.
5. **Reintentos** con backoff exponencial y jitter; cola durable en cliente.
6. **Ordenamiento causal:** reloj híbrido (HLC) para operaciones del mismo dispositivo; el servidor ordena por dependencia, no por llegada.
7. **Recuperación parcial:** sync por buckets; fallo de un bucket no bloquea otros.
8. **Sincronización de archivos:** canal separado, subida reanudable (tus/S3 multipart), hash SHA-256, metadatos primero.
9. **Cargas interrumpidas:** reanudación desde offset; deduplicación por hash.
10. **Deduplicación:** por `operation_id` y por hash de contenido.
11. **Cifrado local:** SQLCipher; llave en keystore/keychain con biometría.
12. **Borrado remoto:** al revocar sesión o desvincular dispositivo, wipe del SQLite local (patrón documentado: JWT corta vida + wipe al expirar [^56^]).
13. **Dispositivos compartidos:** modo kiosco con cambio de usuario sin mezclar datos; wipe entre usuarios.
14. **Revocación de sesión:** tokens cortos; sync tokens invalidables por dispositivo.
15. **Redes lentas:** delta sync, compresión, priorización (metadatos>fotos>video), presupuesto de datos configurable.
16. **Resolución humana:** conflictos críticos (estado de OT, stock financiero) entran a cola de revisión del supervisor — **nunca LWW silencioso** en esos campos.
17. **LWW prohibido por defecto:** LWW solo donde se demuestre inocuo (campos descriptivos de un mismo autor).

---

## 5. Auditoría multi-tenant

**Comparativa** (resumen de la decisión C-4 mantenida): pool+RLS (menor costo, una migración) / schema-per-tenant (migraciones N-esquemas — descartado) / DB-per-tenant (tier enterprise regulado) / **híbrido por nivel — adoptado**.

**Jerarquía de identidad y estructura canónica (resuelve H-16):**

```
Plataforma DONEFIXER
 └── Tenant (Organización cliente)         ← límite de aislamiento, facturación, claves
      └── Empresa(s)                       ← opcional: grupo corporativo multi-empresa
           └── Programa(s)                 ← opcional: contrato/programa de servicios
                └── Propiedad / Instalación (Property/Facility)
                     └── Sitio (Site) → Edificio → Zona/Piso → Unidad/Espacio
                          └── Activos (jerarquía ltree)
Usuario (1 cuenta global) → Membresía(s) (usuario×tenant) → Perfil(es) (membresía×contexto:
sitio/equipo/función) → Rol(es) → Permisos (RBAC + ABAC por sitio/programa/proveedor)
```

**Endurecimientos obligatorios del documento 26:** (1) suite de **pruebas automatizadas de aislamiento** en CI (intentos cruzados de tenant deben fallar); (2) contexto de tenant por transacción (`set_config(..., true)`); (3) índices tenant-first; (4) cuotas y rate limiting por tenant (noisy neighbor); (5) claves de cifrado: KMS con llave por tenant en tier enterprise; (6) **data residency** como atributo del tenant (región de datos); (7) exportación/eliminación/restauración por tenant documentadas y ensayadas; (8) PITR; (9) migraciones expand/contract compatibles con sync; (10) auditoría de todo acceso cross-tenant (solo soporte, con justificación y log); (11) estrategia de evolución documentada (réplicas→particiones→tenants dedicados→shard). **RLS no se declara solución final: es una capa más, probada y monitoreada.**

---

## 6. Auditoría de dominio y glosario canónico (ampliado)

El modelo previo cubre CMMS bien, EAM parcialmente, FM insuficientemente. **Nuevas incorporaciones sin colisión:** contratos y garantías (garantía de activo vs. contrato de proveedor — hoy ausentes), facturación al cliente (service billing — distinta de billing SaaS), costos laborales con tarifas por rol, proyectos (trabajos multi-OT), incidentes (seguridad/EHS, distintos de OT), aprobaciones (flujo genérico reutilizable), emergencias (OT con SLA de minutos y despacho inmediato).

| Término canónico | Definición única | NO confundir con |
|---|---|---|
| Tenant | Organización cliente, límite de aislamiento | Empresa, Sitio |
| Programa | Contrato marco de servicios con un cliente del tenant | Proyecto |
| Propiedad/Instalación | Inmueble gestionado | Sitio (subdivisión operativa) |
| Solicitud (Request) | Demanda no aprobada | OT (trabajo autorizado) |
| Incidente | Evento EHS/seguridad | Falla de activo |
| Proyecto | Conjunto planificado de OTs con presupuesto | PM recurrente |
| Contrato | Acuerdo con proveedor (SLA, tarifas) | Garantía (del fabricante/instalador sobre un activo) |
| Factura (AP) | Cobra un proveedor → conciliación | Factura (AR): el tenant cobra a su cliente · Billing SaaS: DONEFIXER cobra al tenant |
| Ronda (Round) | Recorrido de inspección programado | Inspección puntual |
| Membresía | Vínculo usuario↔tenant | Perfil (contexto dentro de la membresía) |
| Service Account | Identidad API no humana | Usuario de soporte |

---

## 7. Roles y portales

**Decisión (resuelve H-06): UNA aplicación móvil + UNA aplicación web, configurables por permisos.** Los "portales" del índice previo (38–42) se convierten en **experiencias dinámicas** de la misma app según rol — salvo el portal de solicitante/inquilino y el de proveedor, que son web ligeras de acceso controlado (público-invitado), porque sus usuarios no instalan apps. Roles mínimos: propietario de plataforma (DONEFIXER), admin global DONEFIXER (soporte, acceso auditado), admin de tenant, director, gerente, supervisor, despachador, técnico, solicitante, contacto cliente (del tenant), proveedor/contratista, compras, inventario, finanzas, auditor (solo lectura), oficial de seguridad, oficial de cumplimiento, agente de soporte, service account API. Modelo: cuenta → membresías → perfiles contextuales → experiencia dinámica.

## 8. Módulos obligatorios — matriz de cobertura (45 módulos)

De los 45 módulos exigidos: la suite previa cubría suficientemente **14** (OTs, activos, solicitudes parcial, PM, inventario parcial, reportes parcial, auditoría parcial, API parcial, webhooks parcial, documentos parcial, evidencias parcial, notificaciones parcial, SLA parcial, integraciones parcial). **31 requieren spec nueva o ampliación mayor**, destacando como **fase temprana**: autenticación/onboarding, tenants, usuarios/permisos, ubicaciones, despacho, importación, billing SaaS, privacidad/derechos de datos. La priorización completa por fase queda en el índice de módulos del doc 43, con la regla: ningún módulo inicia sin RF/RNF propios + matriz de conflicto de sync + criterios de aceptación.

## 9. Privacidad, seguridad y protección legal

Incorporados íntegramente al índice (docs 36, 37, 44, 45). **Aclaración expresa exigida:** Fundador, Creador y Desarrollador: **Pascasio Emmanuel Reynoso Reyes**. Nombre oficial: **DONEFIXER**. **Nada de lo generado en esta suite constituye asesoría jurídica definitiva**; ToS, DPA, política de privacidad, acuerdos empresariales, contenido legal por jurisdicción y tratamiento de fotografías, ubicación, voz, firmas y datos laborales **deben ser revisados por abogados licenciados en cada jurisdicción antes del lanzamiento** (PD-Fundador: presupuesto legal). Se documentará además: consentimiento y notificación de IA, divulgación de decisiones automatizadas, gestión de menores (declaración de no-aplicación con revisión anual), propiedad del contenido (el tenant es dueño de sus datos; DONEFIXER obtiene licencia limitada para operar el servicio), y protección de marca DONEFIXER (registro marcario — PD).

## 10. Seguridad técnica — threat model inicial

El documento 35 contendrá el threat model completo con metodología STRIDE-por-activo. Vectores priorizados por riesgo real del dominio: **acceso cruzado entre tenants** (mitigación: RLS + tests CI + auditoría) · **sincronización manipulada** (firma de operaciones, validación servidor, HLC) · **fraude de horas/ubicación** (geocerca opcional, evidencia con hash y timestamp servidor) · **falsificación de firmas** (firma ligada a sesión autenticada + hash de evidencia) · **prompt injection** (sanitización RAG, herramientas allowlist, sin SQL directo) · **dispositivo robado** (SQLCipher, biometría, wipe remoto) · **webhooks falsificados** (HMAC + rotación) · **insider threat** (mínimo privilegio, acceso soporte justificado y logueado) · **supply chain** (SBOM, SCA, firma de artefactos, pinning de dependencias). **Diferenciación terminológica obligatoria en toda la suite:** DONEFIXER se encuentra en estado **"cumplimiento aspiracional / diseño alineado"** con SOC 2, ISO 27001 y GDPR; **no posee readiness auditada, auditoría externa ni certificación alguna** a la fecha. Ningún documento afirmará lo contrario sin evidencia formal.

## 11. Gobierno de IA

**Principio rector (se mantiene y se endurece): la IA es capa de asistencia gobernada, no autoridad autónoma.** Clasificación obligatoria por caso de uso:

| Riesgo | Ejemplos | Control |
|---|---|---|
| **Bajo** | Resúmenes, traducción, sugerencia de texto, búsqueda semántica | Registro + fuente visible |
| **Medio** | Triage de solicitudes, sugerencia de prioridad/asignación, generación de procedimientos | Humano confirma; reversible; confianza mostrada |
| **Alto** | Validación de facturas, conciliación de inventario, generación de reportes regulatorios | Aprobación humana obligatoria + doble registro + límites monetarios |
| **Prohibido** | Cerrar OTs críticas sin autorización, aprobar compras, modificar inventario financiero, sancionar trabajadores, decisiones legales, diagnósticos de seguridad concluyentes, enviar datos sensibles a terceros no autorizados | Bloqueado por arquitectura (el agente no tiene la herramienta) |

Requisitos: human-in-the-loop por nivel, explicabilidad con fuentes, trazabilidad por decisión, evaluación continua con golden sets, detección de alucinaciones (el copiloto cita el registro origen o se abstiene), anti prompt-injection, permisos de agente por RBAC propio, reversibilidad de toda acción, retención de prompts configurable por tenant, **entrenamiento con datos de cliente solo con opt-in explícito y aislado**, opt-out completo de IA por tenant, sustitución de proveedores LLM por configuración, fallback a reglas cuando no hay IA (incluido offline), límites presupuestarios por tenant, observabilidad de tokens/latencia/costo.

## 12. UX, accesibilidad y diseño nativo

Incorporado íntegramente a los docs 39–42 (Design System, UX Bible, Accessibility, Brand). Objetivo **WCAG 2.2 AA** (SU: confirmar nivel legal por jurisdicción — PD). Contextos de diseño obligatorios documentados: sótanos, techos, ascensores, cuartos mecánicos, exteriores, lluvia, guantes, poca luz, ruido, redes deficientes, una mano, niveles digitales bajos, dispositivos antiguos razonables. Requisitos: VoiceOver/TalkBack, Dynamic Type, contraste AA, targets ≥44pt, foco visible, reducción de movimiento, errores comprensibles, autosave, estado de sincronización siempre visible, skeletons, empty states, permisos just-in-time, haptics útiles, cámara nativa, firma, push, deep links. **Patrones familiares antes que innovación sin propósito.**

## 13. Internacionalización

Idiomas de lanzamiento: **español, inglés, portugués, francés y criollo haitiano** (HT es requisito real del mercado caribeño de facility management). Reglas: traducción de chat conservando siempre el original visible; traducción de notas bajo demanda; transcripción por idioma detectado; zonas horarias por sitio (no por usuario); multi-moneda con impuestos por jurisdicción; unidades métricas/imperiales por activo; pluralización CLDR; preparación para RTL futuro; contenido legal por jurisdicción versionado.

## 14. Observabilidad, SRE y operación

SLOs se **re-derivan** (resuelve H-18): Etapa A se compromete solo a lo sostenible por un equipo pequeño — disponibilidad 99.5% objetivo interno (no contractual), RPO ≤15 min, RTO ≤4 h, con SLIs de latencia API p95 <500 ms, éxito de sync >99.9% por día, crashes-free sessions >99.5% (móvil), ANR <0.5%, presupuesto de batería/almacenamiento documentado, costo de IA por tenant como métrica de primera clase. Error budgets, runbooks, on-call, status page y postmortems sin culpables quedan en docs 54/55/59. **Ningún SLO se publica contractualmente hasta Etapa B.**

## 15. FinOps y viabilidad (escenarios SU, a validar)

| Escenario | Infra/mes | Herramientas/mes | Notas |
|---|---|---|---|
| Desarrollo local | $0–50 | $0–100 | Docker local, tiers gratuitos |
| Staging + pruebas | $50–150 | $50 | Entorno efímero |
| **Producción inicial (Etapa A)** | **$150–500** | $200–600 (LLM API, email, monitoreo, stores $99+$25/año) | Escala con cuotas de IA |
| Crecimiento (Etapa B) | $2K–8K | $1K–3K (SOC2 pentest, LLM, ClickHouse) | Auditoría SOC2 ~$20–50K/año (SU) |
| Enterprise (Etapa C) | $10K+ | Según contratos | On-prem se cotiza aparte |

Costos variables vigilados como métricas: almacenamiento de imágenes/video (ciclo de vida a frío), ancho de banda de sync, tokens LLM (routing por costo), SMS/WhatsApp por conversación, mapas, OCR, traducción. **Regla: no optimizar para millones de usuarios si eso hace inviable lanzar.**

## 16. Roadmap corregido (etapas controladas, sin "MVP improvisado")

| Fase | Alcance | Exclusiones | Criterios de salida (DoD de fase) |
|---|---|---|---|
| **0: Fundamentos** | Esta auditoría + documentación Ola 1–4 + prototipo de sync con PowerSync | Código de producción | Gates G1–G8 (sección M) |
| **1: Núcleo operacional production-grade** | Auth/onboarding, tenants, usuarios/permisos, ubicaciones, activos, solicitudes, OTs, PM por tiempo/medidor, checklists, evidencias, notificaciones, despacho básico, reportes KPI, app offline con PowerSync, portal solicitante, importación CSV | Inventario financiero, compras, IoT, agentes | 3–5 pilotos; >80% adopción semanal técnico; sync >99.9% éxito; cero fugas cross-tenant en pentest |
| **2: Inventario, compras y proveedores** | Inventario/almacenes, requisiciones, OC, recepción/devoluciones, facturas+conciliación, contratos/garantías, portal proveedor | Predictivo | Flujo repuesto→OT→factura auditado E2E en 2 clientes |
| **3: Colaboración, traducción e IA asistiva** | Chat contextual con traducción (original conservado), voz/transcripción, OCR, copiloto con cuotas, i18n ES/EN/PT/FR/HT | Visión por computadora avanzada | Copiloto con evaluación golden-set aprobada; costo IA/tenant dentro de presupuesto |
| **4: Analítica, automatización e integraciones** | OLAP, dashboards ejecutivos, motor de automatización, ERP conectores, API pública completa, anomalías ML (Etapa B activada) | Marketplace | Criterios E-2/E-3/E-5 medidos y ADRs aprobados |
| **5: Enterprise e internacional** | SSO/SCIM, multi-región, residency, verticales, soberano opcional, SOC2/ISO formal | — | Certificaciones obtenidas (no aspiracionales) |

Cada fase declara además: dependencias, riesgos, métricas, pruebas, costos aproximados y capacidad operativa — formalizado en el documento 69.

---

## J. Índice maestro documental definitivo (70 documentos)

> Sustituye al índice previo. Estructura estándar por documento: objetivo, alcance, exclusiones, decisiones confirmadas, decisiones pendientes, supuestos, dependencias, riesgos, RF, RNF, seguridad, privacidad, accesibilidad, pruebas, métricas, criterios de aceptación, DoD, referencias cruzadas, control de cambios. Regla de evidencia DC/SU/PD en todos.

**Vol. I — Estrategia (01–08):** 01 Product Vision · 02 Product Charter · 03 Market Research · 04 Competitive Analysis · 05 Business Model · 06 Product Strategy · 07 Product Principles · 08 North Star Metrics
**Vol. II — Requisitos y dominio (09–19):** 09 PRD · 10 SRS · 11 Functional Requirements · 12 Non-Functional Requirements · 13 Domain Glossary · 14 Domain Model · 15 User Personas · 16 User Journeys · 17 Service Blueprints · 18 Information Architecture · 19 Roles & Permissions Matrix
**Vol. III — Arquitectura (20–33):** 20 Enterprise Architecture · 21 Solution Architecture · 22 Web Architecture · 23 Mobile Architecture · 24 Backend Architecture · 25 Data Architecture · 26 Multi-Tenant Architecture · 27 Offline Sync Architecture · 28 Integration Architecture · 29 API Standards · 30 Event Architecture · 31 Search Architecture · 32 AI Architecture · 33 AI Governance
**Vol. IV — Confianza (34–38):** 34 Security Architecture · 35 Threat Model · 36 Privacy Program · 37 Legal Framework · 38 Compliance Roadmap
**Vol. V — Diseño (39–42):** 39 Design System · 40 UX Bible · 41 Accessibility Standard · 42 Brand Guidelines
**Vol. VI — Módulos y datos (43–46):** 43 Module Specifications (índice + plantilla + 45 specs) · 44 Data Classification · 45 Data Retention & Legal Hold · 46 Audit Model
**Vol. VII — Calidad y plataforma (47–62):** 47 Testing Strategy · 48 Quality Plan · 49 Performance Plan · 50 DevOps Strategy · 51 CI/CD · 52 Infrastructure as Code · 53 Environments · 54 Observability · 55 SRE · 56 Backup & Restore · 57 Disaster Recovery · 58 Business Continuity · 59 Incident Response · 60 FinOps · 61 Release Management · 62 App Store Readiness
**Vol. VIII — Operación con clientes (63–69):** 63 Migration Strategy · 64 Customer Onboarding · 65 Support Model · 66 Operations Manual · 67 Developer Handbook · 68 API Documentation · 69 User Documentation
**Vol. IX — Gate (70):** 70 Production Readiness Review

## K. Orden de creación (olas corregidas)

- **Ola 0:** 00 + esta auditoría. ✅ (entregados)
- **Ola 1:** 03 → 04 → 01 → 02 → 05 → 06 → 07 → 08
- **Ola 2:** 15 → 16 → 17 → 13 → 14 → 19 → 09 → 11 → 12 → 10 → 18
- **Ola 3 (fundaciones):** 25 → 26 → 27 (con PowerSync) → 24 → 30 → 29 → 28 → 31 → 20 → 21 → 22 → 23 → 32 → 33
- **Ola 4:** 34 → 35 → 36 → 37 → 38 → 44 → 45 → 46
- **Ola 5:** 42 → 39 → 40 → 41
- **Ola 6:** 43 (specs por fase de roadmap: primero las 12 specs de Fase 1)
- **Ola 7:** 47 → 48 → 49 → 50 → 51 → 52 → 53 → 54 → 55 → 56 → 57 → 58 → 59 → 60 → 61 → 62
- **Ola 8:** 63 → 64 → 65 → 66 → 67 → 68 → 69
- **Ola 9:** 70 → **autorización para programar**

## L. Dependencias (bloqueantes)

13/14 → 25 → 26 → 27 → {22, 23, 24} → 29/30 → 32 → 33 · 19 → 26 y 43 · 35 → 34, 36, 38 · 12 → todos · 43-spec → {09, 11, 12, 14, 19, 25–27, 29, 33} · 60 → 05 y arquitectura de etapas · 63 → 25 · 64 → 54-billing, 63 · 70 → todos aprobados. **Cadena crítica:** 03 → 09 → 14 → 25 → 27 → 43(F1) → 47 → 70.

## M. Criterios obligatorios antes de escribir código (actualizados)

1. **M1** Docs 01–14 aprobados; RF trazables a journeys; RNF con valores y fuente de cada valor.
2. **M2** ADR-002 resuelto: PowerSync adoptado con prototipo de sync (prueba de concepto en Fase 0, no producción) que demuestre: conflicto en estado OT, evidencia offline, wipe remoto y dispositivo compartido.
3. **M3** Docs 25–27 aprobados sin PD abiertas; suite de tests de aislamiento multi-tenant especificada.
4. **M4** Threat model (35) y gobierno de IA (33) aprobados con lista de prohibiciones implementable.
5. **M5** Glosario (13) y modelo de identidad membresías/perfiles (19) aprobados.
6. **M6** FinOps (60) con escenario Etapa A aprobado por el Fundador, incluido presupuesto legal y de IA.
7. **M7** DoD global aprobada: tests de sync offline, aislamiento, accesibilidad WCAG 2.2 AA, seguridad, actualización documental.
8. **M8** Doc 70 firmado por el Fundador. **Sin M8, no hay código de producción.**

## N. Preguntas que requieren decisión del Fundador

| # | Decisión | Opciones | Recomendación de la auditoría |
|---|---|---|---|
| N-1 | Framework móvil final | Flutter / RN+Expo | Flutter, con conmutación si falla contratación (§3) — **confirmar** |
| N-2 | PowerSync: Cloud gestionado vs. self-hosted Open Edition | Cloud ($0–49+/mes, menos ops) / Self-hosted (control, FSL) | Cloud en Fase 0–1; self-host evaluar en Etapa B por residency |
| N-3 | Presupuesto legal (ToS/DPA/privacidad por jurisdicción) | Asignar / aplazar | Asignar antes de primer piloto pagado |
| N-4 | Procesador de pagos SaaS | Stripe / procesador regional / ambos | Stripe si cubre países objetivo; PD según país del Fundador |
| N-5 | Registro de marca DONEFIXER | Sí / después | Sí, antes del lanzamiento público |
| N-6 | Idiomas de lanzamiento | ES+EN / ES+EN+PT / los 5 con HT | ES+EN en Fase 1; PT/FR/HT en Fase 3 (i18n lista desde el inicio) |
| N-7 | País de incorporación legal y residencia de datos inicial | PD | Define residency, impuestos y DPA — bloquea doc 37 |
| N-8 | Nivel de accesibilidad contractual | WCAG 2.2 AA | Adoptar AA como estándar interno (SU hasta revisión legal) |
| N-9 | Modelo de soporte Fase 1 (fundador único) | Horario limitado declarado / herramientas de soporte | Declarar SLA de soporte honesto en ToS piloto |
| N-10 | ¿Contratación o solo fundador en Fase 1? | Solo / 1–2 contrataciones | Afecta Etapa A (K8s descartado precisamente por esto) |

---

## Registro de esta auditoría

- **Documentos auditados:** suite fundacional 01–05 + índice maestro 00 (versiones 1.0).
- **Decisiones revertidas:** 1 (ADR-002). **Reabiertas y resueltas:** 7 (D-1…D-7). **Aplazadas:** 10 (E-1…E-10). **Mantenidas:** 12 (C-1…C-12).
- **Fuentes nuevas incorporadas:** PowerSync (precios, licencias, SOC2/HIPAA) [^50^][^53^][^56^]; ElectricSQL CVE-2026-40906 [^57^]; comparativa de sync engines 2026 [^52^][^61^]; background tasks móviles [^49^][^51^][^55^][^59^].
- **Compromiso de integridad:** ninguna afirmación de esta auditoría se presenta como hecho sin fuente y fecha; las estimaciones están etiquetadas SU; nada aquí es asesoría jurídica.

**Fundador, Creador y Desarrollador: Pascasio Emmanuel Reynoso Reyes.**
**Nombre oficial: DONEFIXER.**

*Próximo paso autorizado: resolver N-1…N-10 y ejecutar la Ola 1 del índice definitivo.*
