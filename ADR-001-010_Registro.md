# ADR-001…010 — Registro e Índice de Decisiones Arquitectónicas Tempranas (AO-4)

| Campo | Valor |
|---|---|
| Documento | ADR-001-010_Registro |
| Versión | 1.0 |
| Estado | ✅ Aprobado como acción AO-4 de la Auditoría Integral de Arquitectura (2026-07-29) |
| Propósito | Resolver el hallazgo **H-02**: los ADR-001…010 se citan en 10 documentos pero no existían como artefactos individuales. Este registro es el **punto de resolución oficial** de toda cita `ADR-00X`: documenta qué decidió cada uno, su estado actual y su fuente normativa. |
| Origen de las decisiones | Investigación previa (documentos Doc-01…Doc-05, superseded) → validadas, revertidas o aplazadas por **AUDITORIA_FUNDACIONAL_2026-07 (AUD-00)** → absorbidas en la suite numerada. |

> **Regla de uso:** citar `ADR-00X` en cualquier documento resuelve a este registro. La fuente normativa de cada decisión es la columna "Fuente normativa vigente". Si un ADR temprano se reabre, se crea un documento ADR individual nuevo (formato ADR-011/012) y este registro se actualiza.

---

## Registro

| ADR | Decisión (resumen normativo) | Estado | Fuente normativa vigente | Documentos donde se aplica | Reversibilidad | Notas de auditoría |
|---|---|---|---|---|---|---|
| **ADR-001** | **Tenancy híbrida:** pool compartido con `tenant_id` + RLS como modelo base, con camino documentado réplicas→particiones→tenants dedicados→shard | DC | Doc 26 (MT-1…MT-12); RNF-SCL-002 | 10 (C-3), 12, 14, 25, 26 | Reversible hacia mayor aislamiento (nunca hacia menos) sin rediseño | Mantenida por AUD-00 (C-series); índice maestro §18 |
| **ADR-002** | **Motor de sincronización:** ~~propio~~ → **REVERTIDO (2026-07): adoptar PowerSync** (Open Edition self-hosted o Cloud), escrituras vía backend propio; motor propio solo como exit strategy | DC (revertido por AUD-00 D-1 con evidencia nueva); **modalidad Cloud vs. self-hosted: PD (N-2)** | Doc 27 (SY-1…SY-15); Doc 14 §campos de plataforma | 14, 23, 24, 27 | Reversible: exit strategy documentada; capa adaptador (MA-1) | Única decisión revertida por AUD-00; PowerSync: tier gratis, Pro $49/mes, Open Edition FSL, SDKs Apache 2.0, SOC2+HIPAA (ene-2026) |
| **ADR-003** | **PostgreSQL como base única inicial** (sin poliglot persistence en Etapa A) | DC (absorbida en DA-1) | Doc 25 (DA-1: PostgreSQL 16+ como sistema de registro único) | 12, 21, 25 | Reversible por criterio (ClickHouse Etapa B) | C-3 de AUD-00; citada vía índice maestro |
| **ADR-004** | **Backend en .NET 8** como plataforma de servidor | DC | Doc 24 (monolito modular .NET 8); Doc 21 §2.2 | 21, 24 | Costosa de revertir (plataforma); no se contempla sin ADR + evidencia | Citada en 00, 02, 11, 14, 20, 21, 24, 25 |
| **ADR-005** | **Monolito modular con extracción a servicios solo por métricas** (bounded contexts como módulos internos) | DC | Doc 24; Doc 14 §regla de frontera (referencias por ID y eventos, no joins trans-contexto) | 10, 14, 20, 21, 24 | Reversible hacia servicios por módulo individual (diseñado para ello) | Citada en 00, 02, 10, 11, 14, 20, 21, 24, 25 |
| **ADR-006** | **Analítica separada del OLTP:** Fase 1 con vistas materializadas + réplica de lectura; ClickHouse aplazado a Etapa B con criterio medible (>50M filas o p95 dashboards >2 s) | DC (aplazamiento con criterio, AUD-00 E-3) | Doc 25 (DA-5); Doc 30 (EV-7); Doc 26 (MT-10) | 16, 17, 25, 26, 30 | Reversible: activación por criterio, no por reescritura | Evita sobrearquitectura (condición permanente 5) |
| **ADR-007** | **Gateway multi-modelo de IA con routing por costo** (proveedores LLM sustituibles; dominio nunca habla directo con proveedor) | DC; **proveedor específico: PD (PD-IA-1)** | Doc 32 (AIA-1); Doc 03 §costos; Doc 33 | 03, 10, 21, 32, 33 | Reversible: sustitución de proveedor sin tocar dominio | Mitiga riesgo R8 (índice maestro) |
| **ADR-008** | **PostgreSQL 16+** como versión/plataforma de datos (RLS, ltree, pgvector, pgcrypto) | DC (absorbida en DA-1) | Doc 25 (DA-1) | 12, 21, 25 | Reversible por migración mayor (expand/contract, RNF-MNT-002) | C-3 de AUD-00; índice maestro §17 |
| **ADR-009** | **API REST versionada con deprecación de 12 meses y eventos con esquema versionado** | DC | Doc 29 (AP-1…AP-12); RNF-MNT-003; Doc 30 | 10, 14, 16, 29, 30 | Reversible solo hacia políticas más estrictas | Citada en 00, 10, 12, 14, 20, 29, 30 |
| **ADR-010** | **i18n nativa:** cero strings hardcodeados, catálogo de mensajes, glosario canónico como fuente de etiquetado | DC; **idiomas de lanzamiento: PD (PD-4)** | Doc 22 (WA-7); RF-I18N-001; Doc 13 §4 | 00, 10, 11, 13, 22, 44 (futuro) | Reversible hacia más idiomas sin redeploy | C-9 del SRS; G-10 del índice (traducción en tiempo real diferida al doc 44) |

---

## ADRs con documento propio (posteriores a la investigación previa)

| ADR | Título | Estado | Documento |
|---|---|---|---|
| ADR-011 | Estrategia Multicanal (Web App + PWA + nativa; autoridad del backend, texto literal del Fundador) | ✅ APROBADO v1.1 (2026-07-29) | `ADR-011_Estrategia_Multicanal.md` |
| ADR-012 | Platform Administration Console (separación de planos como principio permanente) | ✅ APROBADO v1.1 (2026-07-29) | `ADR-012_Platform_Administration_Console.md` |

---

## Regla de evolución

- Todo ADR nuevo (ADR-013+) se crea como documento individual y se registra aquí y en el **ADI** (Architecture Decision Index, AO-ADI-1).
- Reabrir un ADR exige evidencia nueva verificable (condición permanente 4) — precedente: ADR-002 revertido por AUD-00 con evidencia de mercado de feb–jul 2026.

---

*Registro de cambios — v1.0 (2026-07-29): creación como acción obligatoria AO-4 de la Auditoría Integral de Arquitectura aprobada por el Fundador.*
