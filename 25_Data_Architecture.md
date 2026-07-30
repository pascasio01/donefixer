# DONEFIXER — 25 · Data Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)
> **Evidencia:** DC para decisiones derivadas de documentos aprobados (14, 12, ADR-001/008, AUD-00); SU para estimaciones de volumen y umbrales de evolución; PD donde falta decisión del Fundador.
> **Regla Ola 3:** toda decisión tecnológica trazada a RF/RNF/decisiones aprobadas; ninguna tecnología por tendencia; alternativas evaluadas con costo operativo y estrategia de reemplazo. **Este documento no contiene DDL ni esquema físico definitivo** (regla del Fundador: el físico se deriva tras la Ola 3; aquí se define la arquitectura de datos).

---

## 1. Objetivo
Definir cómo DONEFIXER almacena, organiza, protege, escala y retira sus datos durante 10 años, derivándose del dominio canónico aprobado (doc 14) — nunca al revés (condición permanente 5 de la Ola 2).

## 2. Alcance
Sistema de registro (OLTP), lectura/analítica, archivos/objetos, embeddings, series temporales (fase), clasificación de datos, residencia, ciclo de vida y estrategia de evolución.

## 3. Exclusiones
DDL y esquema físico definitivo (posteriores a gates); multi-tenancy detallado (doc 26); protocolo de sync (doc 27); topología de infra (doc 52).

## 4. Decisiones confirmadas (DC)

| # | Decisión | Trazabilidad |
|---|---|---|
| DA-1 | **PostgreSQL 16+ como sistema de registro único** (OLTP) | ADR-008 (auditoría C-3), RNF-SEC, doc 14 |
| DA-2 | Campos de plataforma en toda entidad: `id` UUIDv7, `tenant_id`, `version`, timestamps, `deleted_at`, `sync_metadata` | doc 14 §4.1 (aprobado) |
| DA-3 | Jerarquía de activos con camino materializado (ltree) | doc 14 §7.3 |
| DA-4 | Inventario como log de movimientos (saldo derivado, prohibido `set`) | doc 14 §7.5, AUD-00 §4 |
| DA-5 | Analítica separada del OLTP: Fase 1 con vistas materializadas + réplica; **ClickHouse aplazado a Etapa B con criterio de activación medible** | ADR-006, AUD-00 E-3 (evitar sobrearquitectura — condición permanente 5) |
| DA-6 | pgvector para embeddings en Fase 1–3; vector DB dedicada solo si escala lo demuestra | AUD-00 §2, doc 32 |
| DA-7 | Objetos en S3-compatible con URLs firmadas, hash SHA-256, ciclo de vida a frío | doc 11 RF-SYNC-007, RNF-SEC-002 |
| DA-8 | Series temporales IoT: aplazadas a Fase 4 (tablas particionadas PG si hace falta antes) | AUD-00 E-4 |
| DA-9 | Soft-delete con tombstones; purga según retención (PD-RETENCIÓN) | doc 14 §4.1, ADR-012 §6 |
| DA-10 | Clasificación de datos en 4 niveles (§7) y minimización | RNF-PRV-001, AUD-00 H-17 |

## 5. Decisiones pendientes (PD)
- **PD-RETENCIÓN:** política de retención (afecta purgas de tombstones, auditoría, adjuntos) → doc 37/45, vinculada a N-3/N-7.
- **N-7:** región/residencia inicial de datos.
- **SU-FLAGS:** entidad de feature flags propia vs. servicio (afecta esquema `platform`).

## 6. Supuestos (SU)
Volúmenes de diseño Etapa A: 50 tenants, 5K usuarios, 500K OTs, 2M evidencias, 5M movimientos/año (coherente con RNF-SCL-001; se recalibran con datos reales).

## 7. Arquitectura de datos por subsistemas

### 7.1 OLTP — PostgreSQL (núcleo)
- **Esquemas lógicos:** `identity` · `assets` · `work` · `planning` · `inventory` · `procurement` · `governance` (auditoría, SLA, notificaciones) · `platform` (tenants, planes, flags, consumo — plano DONEFIXER). La frontera entre esquemas respeta los contextos delimitados del doc 14 §7.1 (regla: referencias por ID y eventos, no joins trans-contexto, DC ADR-005).
- **Extensiones justificadas:** ltree (jerarquía — RF-AST-001), pgvector (RAG — doc 32), pgcrypto (hash/cifrado de columna para PII sensible — RNF-SEC), y `wal_level=logical` (requisito de sync, doc 27).
- **Reglas de diseño físico (para la etapa DDL):** índices compuestos tenant-first (AUD-00 §5); FKs dentro del esquema; ninguna FK hacia `platform` desde tablas de negocio más allá de `tenant_id`; particionamiento por `tenant_id`/fecha solo cuando una tabla supere umbrales medidos (SU: >50M filas o degradación medida).
- **Alternativas evaluadas:** MySQL (sin RLS equivalente maduro — descartada, doc 26), MongoDB (rompe invariantes relacionales del dominio — descartada), CockroachDB (costo/complejidad sin requisito — descartada en Etapa A, reevaluable Etapa C). *Costo operativo de la elegida: bajo (estándar, gestionable en PaaS/VM). Estrategia de reemplazo: SQL estándar + exportación completa por tenant (RNF-PRV-002); el ORM se abstrae tras repositorios por contexto.*

### 7.2 Lectura y analítica
- **Fase 1–2:** vistas materializadas de KPIs (MTTR/MTBF/PM compliance — RF-RPT-001) refrescadas por jobs; réplica de lectura cuando el p95 de dashboards supere 2 s (criterio medible, no fecha).
- **Etapa B (criterio de activación, DC AUD-00 E-3):** >50M filas de eventos/lecturas o p95 dashboards >2 s sostenido → ClickHouse alimentado por CDC (Debezium o gestionado). *Estrategia de reemplazo: los KPIs se definen en capa semántica (doc 51) independiente del motor.*

### 7.3 Objetos (evidencias, documentos)
S3-compatible; estructura `tenant_id/entidad/id_hash`; URLs firmadas de corta duración (RNF-SEC); antivirus/malware scan en subida (SU, doc 34); ciclo de vida: caliente 90 días → frío (SU costo, doc 60); hash de contenido para deduplicación y verificación de evidencia (RF-WO-003).

### 7.4 Embeddings y búsqueda semántica
pgvector en la misma PostgreSQL (evita un sistema más en Etapa A — condición 5); corpus: manuales, procedimientos, historial de OTs, catálogos (doc 32/31); aislamiento por `tenant_id` en el filtrado (obligatorio, DC RNF-PRV). *Criterio de migración a Qdrant/Weaviate: latencia p95 de búsqueda >800 ms o >5M vectores por tenant grande (SU).*

### 7.5 Series temporales (Fase 4)
Lecturas de sensores: tablas particionadas por mes en PostgreSQL como primer paso; TimescaleDB/ClickHouse solo con el primer cliente IoT contratado (AUD-00 E-4). *Sin tecnología IoT pre-comprada.*

## 8. Clasificación de datos (DA-10 — alimenta doc 44)

| Nivel | Ejemplos | Controles (DC) |
|---|---|---|
| **Público** | Catálogos semilla de plataforma, contenido de ayuda | Ninguno especial |
| **Interno** | OTs, activos, inventario, KPIs | RLS + RBAC/ABAC + auditoría de acceso |
| **Confidencial** | Contratos, facturas, costos laborales, datos de proveedores | + cifrado de columna selectivo + acceso registrado con motivo (soporte, ADR-012 §3.3) |
| **Restringido (PII/sensible)** | Datos personales de usuarios/solicitantes (nombre, contacto, ubicación, voz, foto, firma), credenciales | + cifrado de columna + minimización + retención específica (PD) + base legal por jurisdicción (doc 36/37) |

## 9. Ciclo de vida, residencia y soberanía
- **Residencia:** atributo del tenant (región de datos) decidida con N-7 (PD); tier enterprise podrá fijar región distinta (Etapa C).
- **Retención:** PD-RETENCIÓN — hasta su política: sin purga automática de datos de negocio; tombstones y logs se conservan; toda purga futura será configurable por tenant.
- **Eliminación de tenant:** exportación ofrecida → borrado verificable con certificado (RNF-PRV-003) tras ventana de gracia (SU 30 días).
- **Backups:** cifrados, PITR RPO ≤15 min (RNF-AVL-002), ensayo trimestral de restauración (DC).

## 10. Estrategia de evolución (10 años)
`Etapa A:` PostgreSQL único + réplica + S3 + pgvector → `Etapa B (criterios medidos):` réplicas gestionadas, ClickHouse, particionamiento agresivo, vector DB dedicada si aplica → `Etapa C:` tenants enterprise a bases dedicadas (tier híbrido, doc 26), multi-región, shard por tenant solo como último recurso (DC ADR-001). **Regla: ningún salto de etapa sin métrica que lo exija + ADR** (condición permanente 5).

## 11. Riesgos
| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Crecimiento de tablas calientes degrada OLTP | Media | Alto | Criterios de particionamiento medidos; OLAP offload |
| pgvector insuficiente a escala | Media | Medio | Criterio de migración declarado; embeddings exportables |
| Retención indefinida infla costos y riesgo legal | Media | Medio | PD-RETENCIÓN priorizada en Ola 4 |
| Deriva esquema físico vs. dominio | Baja | Alto | El dominio (doc 14) es canónico; el DDL se genera derivado y se revisa contra él |

## 12. Métricas
p95 de consultas por endpoint · tamaño/crecimiento por tabla · lag de réplica · costo por GB y por tenant · % tablas con índices tenant-first (objetivo 100%).

## 13. Criterios de aceptación
1. Toda decisión trazada a RF/RNF/ADR. ✅ 2. Alternativas evaluadas con costo y reemplazo. ✅ 3. Sin DDL ni físico definitivo. ✅ 4. Criterios de evolución medibles. ✅

## 14. Referencias cruzadas
Depende de: 14 (dominio canónico), 12 (RNF), 11 (RF), ADR-001/005/006/008, AUD-00. Alimenta: 26 (multi-tenant), 27 (sync), 24 (backend), 44/45 (clasificación/retención), 51 (reporting), 60 (FinOps).

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). Subsistemas de datos por etapas con criterios medibles; clasificación de 4 niveles; alternativas evaluadas; sin DDL |
