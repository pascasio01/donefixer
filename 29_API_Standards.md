# DONEFIXER — 29 · API Standards

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)
> **Regla del Fundador (Ola 2): "no diseñar APIs definitivas todavía"** — este documento define **estándares** (convenciones vinculantes), no la API definitiva ni sus endpoints específicos (estos se derivan de las specs de módulo en la etapa de construcción).

---

## 1. Objetivo
Fijar las convenciones que harán de la API de DONEFIXER un producto consistente, versionado y evolutivo durante 10 años — la superficie que comparten los tres canales (ADR-011) y futuras integraciones (doc 28).

## 2. Alcance
Estilo, versionado, errores, paginación, filtros, autenticación/autorización, límites, idempotencia, documentación, deprecación y gobierno de cambios de la API pública y de la Admin API (superficie, según ADR-012).

## 3. Exclusiones
Endpoints definitivos por módulo (etapa de construcción); Admin API detallada (ADR-012 §3.2); webhooks payload (doc 28/30).

## 4. Decisiones confirmadas (DC)

| # | Estándar | Trazabilidad |
|---|---|---|
| AP-1 | **REST sobre HTTPS, JSON**, recursos en inglés canónico del glosario (doc 13) | ADR-009, doc 13 |
| AP-2 | **Versionado por URL** `/v1/…`; cambios incompatibles → `/v2` conviviendo; **deprecación con aviso de 12 meses** | ADR-009, RNF-MNT-003 |
| AP-3 | **OpenAPI generado desde código** (fuente de verdad = el código); contrato publicado por versión | ADR-009, doc 24 |
| AP-4 | Errores: formato único (código de máquina, mensaje humano localizable, `trace_id`, detalles por campo) — nunca stack traces | RNF-ACC-004, RNF-OBS-003 |
| AP-5 | Paginación por cursor (`?cursor=&limit=`); filtros explícitos; orden estable con desempate por `id` | RNF-PERF, doc 14 (cursor sync usa el mismo patrón) |
| AP-6 | Auth: **OIDC/OAuth 2.1**, tokens de corta vida; autorización RBAC+ABAC en servidor en cada request (la UI no es seguridad) | doc 19, ADR-011 v1.1 |
| AP-7 | `tenant_id` exclusivamente del claim del token validado — nunca de path/query/body del cliente | doc 26 MT-2 |
| AP-8 | **Idempotencia en mutaciones:** cabecera `Idempotency-Key` (además del `operation_id` del sync); reintentos seguros | RF-SYNC-002, AUD-00 §4 |
| AP-9 | Rate limiting por tenant y por usuario con cabeceras estándar (`X-RateLimit-*`, `Retry-After`, 429) | RNF-SCL-003, doc 26 MT-7 |
| AP-10 | Toda respuesta de lista filtrable por tenant automáticamente (RLS + filtro aplicación); **prohibidos endpoints cross-tenant en API pública** | doc 26 §7 |
| AP-11 | Timestamps UTC ISO-8601 con zona del sitio como dato aparte donde aplique; dinero como entero en moneda menor + código ISO 4217 | RF-I18N-002, doc 14 |
| AP-12 | Toda operación mutante registra auditoría (actor, antes/después) — regla de 10 campos donde aplique | RF-AUD-001, ADR-012 |

## 5. Decisiones pendientes (PD)
GraphQL para casos de reporting (SU: evaluar en Fase 4 con OLAP; REST es el estándar) · API de webhooks: formato de firma exacto (HMAC-SHA256, secreto rotativo — SU detalle en doc 28).

## 6. Supuestos (SU)
Versionado por URL preferido sobre cabeceras por claridad para integradores LatAm; cursor sobre offset por rendimiento en tablas grandes.

## 7. Convenciones de diseño (extracto normativo)

**Recursos:** sustantivos plurales del glosario (`/v1/work-orders`, `/v1/assets`, `/v1/service-requests`) · sub-recursos solo para relaciones de composición (`/v1/work-orders/{id}/evidences`) · acciones de dominio como verbos de operación cuando no encajan en CRUD (`POST /v1/work-orders/{id}:complete` — transición de estado con cuerpo de evidencias).

**Estados y transiciones:** la máquina de estados de la OT (doc 14 §7.2) se expone como operaciones explícitas, nunca como `PATCH status` libre — el servidor valida la transición por rol (doc 19 §9.3) y responde 409 con el estado actual si es inválida.

**Optimistic concurrency:** `ETag`/`If-Match` por `version` en mutaciones de registros editables (coherente con sync, doc 27).

**Respuestas:** envoltura mínima; metadatos de paginación en cabeceras o sobre `meta`; errores 4xx con `application/problem+json`-like (AP-4).

**Consistencia cliente-servidor (ADR-011 v1.1):** la API expone también **contratos de validación** (esquemas por formulario) para que los clientes deriven su lógica local del mismo contrato — minimizando duplicación y divergencia (interpretación normativa §3.1.d de ADR-011).

## 8. Gobierno de cambios de la API
1. Todo endpoint nuevo nace en spec de módulo (doc 43) con RF trazado (regla Ola 3).
2. Revisión de contrato (API review) antes de publicar: naming contra glosario, errores, paginación, permisos.
3. Cambio compatible (añadir campos opcionales): libre dentro de la versión. Cambio incompatible: `/v{n+1}` + deprecación 12 meses con `Sunset` header.
4. Tests de contrato en CI (doc 47): el OpenAPI generado se compara con el publicado; divergencia = build rojo.

## 9. Alternativas evaluadas

| Alternativa | Desventaja principal | Veredicto |
|---|---|---|
| **REST+OpenAPI (elegido)** | — | **Estándar** |
| GraphQL como API principal | Caché compleja, límites por query costosos, curva para integradores | Solo evaluable para reporting Fase 4 (PD) |
| gRPC externo | No apto para clientes web/móviles públicos ni integradores generales | Interno futuro si hiciera falta (no ahora) |
| Versionado por cabecera | Menos visible para integradores | Descartado |

## 10. Estrategia de evolución
v1 con los módulos de Fases 1–2 · sandbox de integradores con datos sintéticos (Fase 4) · catálogo de webhooks creciente (doc 28) · SDK generados desde OpenAPI cuando haya demanda (SU Fase 4).

## 11. Riesgos
| Riesgo | Mitigación |
|---|---|
| Divergencia entre API y dominio | AP-3 + tests de contrato + revisión contra doc 14 |
| Filtrado accidental cross-tenant | AP-7/AP-10 + tests de aislamiento (doc 26 MT-6) |
| Deuda de versiones | Regla de convivencia máxima: 2 versiones activas (SU) |

## 12. Métricas
Adopción por versión · errores 4xx/5xx por endpoint · latencia p95 (RNF-PERF-001) · % endpoints con test de contrato (objetivo 100%).

## 13. Criterios de aceptación
1. 12 estándares DC trazados. ✅ 2. Sin endpoints definitivos (regla del Fundador). ✅ 3. Gobierno de cambios y deprecación. ✅ 4. Coherencia con sync y autoridad backend. ✅

## 14. Referencias cruzadas
Depende de: 13, 14, 19, 26, 27, ADR-009/011. Alimenta: 28 (integraciones/webhooks), 43 (specs), 47 (tests de contrato), 68 (documentación de API para desarrolladores).

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). 12 estándares DC de API, operaciones de dominio vs. CRUD, ETag/If-Match, contratos de validación compartidos con clientes, gobierno de cambios |
