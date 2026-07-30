# DONEFIXER — 31 · Search Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)

---

## 1. Objetivo
Definir cómo se encuentra todo en DONEFIXER: búsqueda estructurada (Fase 1), búsqueda de texto completo, búsqueda semántica/RAG (Fase 3) y búsqueda en lenguaje natural sobre datos operativos — respetando siempre permisos y tenancy.

## 2. Alcance
Búsqueda global, filtros, indexación, RAG/knowledge (frontera con doc 32/33), búsqueda móvil offline.

## 3. Exclusiones
Copiloto conversacional completo (doc 32); base de conocimiento editorial (spec doc 43); OLAP (doc 51).

## 4. Decisiones confirmadas (DC)

| # | Decisión | Trazabilidad |
|---|---|---|
| SE-1 | **Fase 1: PostgreSQL cubre la búsqueda** (índices `pg_trgm` + `tsvector` para texto; índices tenant-first para estructurada) — sin motor de búsqueda dedicado (condición 5) | doc 25 DA-1, RNF-PERF |
| SE-2 | **Todo resultado respeta permisos y tenant** (RLS + filtro de aplicación; la búsqueda nunca es una vía lateral de acceso) | doc 26 MT, ADR-011 v1.1 |
| SE-3 | Búsqueda móvil sobre el bucket local (SQLite FTS) — funciona offline sobre lo sincronizado | RF-SYNC, doc 27 SY-10 |
| SE-4 | **Búsqueda semántica/RAG con pgvector** (Fase 3), corpus filtrado por `tenant_id` obligatorio | doc 25 §7.4, RNF-PRV |
| SE-5 | Búsqueda NL→datos operativos (copiloto) siempre con **fuente citada o abstención** | doc 33 (DC), RNF-AI-001 |
| SE-6 | Criterio de adopción de motor dedicado (OpenSearch/Typesense): p95 búsqueda >800 ms o >10M documentos por tenant grande (SU medible) + ADR | condición permanente 5 |

## 5. Decisiones pendientes (PD)
Motor dedicado si se activa el criterio (SU: Typesense por costo operativo menor) · ranking semántico híbrido (Fase 3).

## 6. Supuestos (SU)
El volumen de Etapa A hace que pg_trgm/tsvector sea suficiente con buenos índices; los usuarios frontline buscan más por QR/ID que por texto libre.

## 7. Arquitectura por capas de búsqueda

| Capa | Fase | Tecnología | Corpus | Regla de acceso |
|---|---|---|---|---|
| Estructurada (filtros, listas, vistas guardadas) | 1 | PostgreSQL, índices tenant-first | Todas las entidades operativas | Permisos por consulta |
| Texto completo | 1 | `tsvector` + `pg_trgm` (ES/EN; PT/FR/HT al llegar) | OTs, activos, personas, repuestos, documentos (metadatos) | Idem |
| QR/ID directo | 1 | Lookup exacto | Activos, OTs, sitios | Idem |
| Local móvil | 1 | SQLite FTS sobre bucket | Lo sincronizado | Local (ya filtrado por bucket) |
| Semántica (RAG) | 3 | pgvector + LLM gateway | Manuales, procedimientos, historial OTs, KB | Filtro tenant obligatorio |
| NL→operativo (copiloto) | 3 | LLM + function calling sobre APIs | Datos operativos vía herramientas | Hereda RBAC de la API (doc 33) |

**Reglas de indexación (SE-1):** campos de búsqueda definidos por entidad en la spec; actualización en la misma transacción (columnas generadas) o por job eventualmente consistente con lag <60 s (SU); búsqueda fonética/aproximada para nombres propios (trigram).

## 8. Ranking y experiencia
- Estructurada: relevancia exacta + recencia; acción directa desde el resultado (doc 18 §11).
- Texto: `ts_rank` + boosts por tipo de objeto (OT abierta > cerrada; activo del sitio del usuario > otros sitios permitidos — SU).
- Semántica: híbrida (keyword + vector) con citas obligatorias (SE-5); nunca respuesta sin fuente.

## 9. Alternativas evaluadas

| Alternativa | Costo operativo | Veredicto |
|---|---|---|
| **PostgreSQL (elegida Etapa A)** | Cero adicional | **Etapa A–B inicial** |
| Typesense | Bajo-medio (un proceso más) | Candidato si se activa criterio SE-6 |
| OpenSearch/Elasticsearch | Alto (cluster, JVM, especialidad) | Solo Etapa C si el volumen lo exige |
| Algolia (SaaS) | Costo recurrente + datos fuera | Descartado (residencia/costo) |
| Vector DB dedicada desde el inicio | Sobrearquitectura (condición 5) | Aplazada (doc 25 §7.4) |

## 10. Estrategia de evolución
Estructurada+texto en PG → semántica pgvector (F3) → motor dedicado solo por criterio medido → búsqueda unificada multi-idioma (PT/FR/HT con PD-4). La capa de consulta de búsqueda se abstrae en la capa de aplicación (el motor es reemplazable tras una interfaz — estrategia de reemplazo).

## 11. Riesgos
| Riesgo | Mitigación |
|---|---|
| Búsqueda como vía de fuga cross-tenant | SE-2 + tests de aislamiento incluyen búsqueda (doc 26 §8) |
| Degradación de texto completo con volumen | Criterio SE-6 medido; índices revisados trimestralmente |
| RAG mezcla corpus entre tenants | Filtro por tenant en la consulta vectorial + test específico |
| Sobre-confianza en respuestas NL | SE-5 (fuente o abstención) + golden-set (doc 33) |

## 12. Métricas
p95 por tipo de búsqueda · CTR desde resultados · % consultas NL respondidas con fuente vs. abstención · lag de indexación.

## 13. Criterios de aceptación
1. Cobertura por capas con fases explícitas. ✅ 2. Permisos/tenant en cada capa. ✅ 3. Sin motor dedicado prematuro, con criterio de adopción medible. ✅ 4. Offline cubierto (bucket local). ✅

## 14. Referencias cruzadas
Depende de: 25, 26, 27, 18, 12, 13. Alimenta: 32 (IA), 33 (gobierno), 43 (KB spec), 47 (tests), 60 (FinOps del motor futuro).

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). Búsqueda por capas (estructurada/texto/QR/local/semántica/NL) con PostgreSQL en Etapa A y criterios medibles de evolución |
