# DONEFIXER — 26 · Multi-Tenant Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)
> **Evidencia:** DC para el patrón y endurecimientos (ADR-001, AUD-00 §5, doc 14/25 aprobados o en oleada); SU para umbrales y costos; PD marcadas.

---

## 1. Objetivo
Definir el aislamiento entre clientes como propiedad verificable del sistema — no como convención de código — con su estrategia de escalado a 10 años.

## 2. Alcance
Modelo de aislamiento (pool + RLS + tier híbrido), identidad de tenant en el pipeline de request, noisy neighbors, operación por tenant (backup/restore/exportación), pruebas de aislamiento, evolución.

## 3. Exclusiones
Data architecture general (doc 25); IAM (doc 26-futuro→34/35 Ola 4); billing (spec doc 43).

## 4. Decisiones confirmadas (DC)

| # | Decisión | Trazabilidad |
|---|---|---|
| MT-1 | **Patrón pool + `tenant_id` + Row-Level Security en PostgreSQL**, con vía híbrida a base dedicada para enterprise regulado | ADR-001 (aprobado en gobierno), AUD-00 C-4 |
| MT-2 | Identidad de tenant resuelta en el borde: JWT/OIDC con `tenant_id` validado; la app nunca confía en parámetros del cliente | AUD-00 §3.1 |
| MT-3 | Contexto de tenant **por transacción**: `set_config('app.current_tenant', ..., true)` con scope transaccional (seguro con PgBouncer en modo transacción) | AUD-00 §3.3 |
| MT-4 | RLS como **última línea de defensa**: la aplicación filtra siempre por tenant y la BD lo impone además; "RLS no es la solución, es una capa probada y monitoreada" | AUD-00 §5 |
| MT-5 | Índices compuestos tenant-first en toda tabla multi-tenant | AUD-00 §5, doc 25 §7.1 |
| MT-6 | **Suite automatizada de pruebas de aislamiento en CI que bloquea el merge** | AUD-00 §5, RNF-SEC-006 |
| MT-7 | Noisy neighbors: rate limiting y cuotas por tenant en gateway y colas | RNF-SCL-003 |
| MT-8 | Operación por tenant: exportación, eliminación verificable, restauración | RNF-PRV-002/003, AUD-00 §5 |
| MT-9 | Claves: KMS con llave por tenant en tier enterprise (Etapa C); llave compartida gestionada en Etapa A | AUD-00 §5 |
| MT-10 | Analítica preserva `tenant_id`; el equipo de plataforma consulta flota completa sin tocar OLTP | ADR-006 |
| MT-11 | Acceso de soporte cross-tenant: solo vía consola, con consentimiento, motivo, tiempo límite y registro visible al tenant | ADR-012 §3.3 (aprobado) |
| MT-12 | Residencia de datos como atributo del tenant | doc 25 §9 |

## 5. Decisiones pendientes (PD)
N-7 (región/residencia inicial) · criterio exacto de migración a base dedicada (se define con el primer candidato enterprise; SU: requisito contractual o >5% de carga sostenida de la flota).

## 6. Supuestos (SU)
50 tenants en Etapa A caben en una PostgreSQL bien dimensionada con réplica; el overhead de RLS es <5% con índices tenant-first (referencia de la práctica del patrón; se medirá).

## 7. Arquitectura del pipeline de request

```
1. Request → API Gateway: autentica JWT → extrae tenant_id + roles (claims firmados)
2. Validación: membresía activa del usuario en ese tenant (doc 19) — 401/403 si no
3. Middleware: abre transacción → set_config('app.current_tenant', tenant_id, true)
4. Consultas: WHERE tenant_id = ... (aplicación) + POLICY RLS (base de datos)
5. Eventos/outbox: todo evento porta tenant_id (doc 30)
6. Respuesta: nunca incluir datos fuera del contexto; caché particionada por tenant
```
**Regla DC:** ningún endpoint "admin global" en la API pública; el plano plataforma tiene su propia Admin API (ADR-012 §3.2, aprobado).

## 8. Patrón RLS (nivel arquitectónico, sin DDL)
- **Policy de aislamiento:** `tenant_id = current_setting('app.current_tenant')::uuid` en toda tabla de negocio; RLS forzada también para el rol de la aplicación (sin BYPASS).
- **Excepciones controladas:** esquema `platform` (sin RLS de tenant; acceso solo desde Admin API); catálogos semilla globales (lectura cross-tenant, escritura solo plano plataforma).
- **Pruebas de aislamiento (MT-6):** matriz de ataques: (a) usuario A intenta leer/escribir/borrar recursos de B por ID directo, por listado, por búsqueda, por exportación, por webhook; (b) token manipulado con tenant_id ajeno; (c) sesión de soporte fuera de ventana de consentimiento. Todo debe fallar. *Estos tests son tan importantes como los de lógica de negocio (DC).*

## 9. Alternativas evaluadas (regla Ola 3)

| Alternativa | Ventajas | Desventajas / costo operativo | Estrategia de reemplazo | Veredicto |
|---|---|---|---|---|
| **Pool + RLS (elegida)** | Menor costo; una migración DDL; escala a miles de tenants (referencia: patrón usado por SaaS B2B grandes) | Exige disciplina de pruebas; PITR por tenant más complejo | Migración de tenant a base dedicada vía exportación/importación lógica (documentada) | **Etapa A–B** |
| Schema-per-tenant | Aislamiento visual claro | Migraciones sobre N esquemas; deriva de esquema; "trampa" documentada (AUD-00) | — | Descartada |
| DB-per-tenant (default) | Aislamiento máximo; PITR trivial | Costo e idle-waste; operación de N bases | — | Solo tier híbrido enterprise (Etapa C) |
| Disco-dependiente: RLS sin pruebas | — | Falsa seguridad | — | Prohibido (MT-6) |

## 10. Noisy neighbors y cuotas (MT-7)
Límites por tenant: requests/min (gateway), jobs concurrentes, tokens IA/mes (FinOps), storage GB, dispositivos de sync. Respuesta ante abuso: 429 con cabeceras de retry + alerta en consola (nunca afectar a otros tenants). Escalación: cuotas endurecidas por plan comercial (doc 03).

## 11. Operación por tenant (MT-8)
| Operación | Mecanismo | Etapa |
|---|---|---|
| Exportación completa | Job asíncrono → paquete firmado (datos + adjuntos + manifiesto) | A |
| Eliminación | Anonimización de PII + borrado verificable + certificado | A |
| Restauración selectiva | PITR a instancia temporal + extracción por tenant | A (proceso), C (automatizado) |
| Migración a base dedicada | Exportación lógica + corte con ventana de mantenimiento del tenant | C |

## 12. Estrategia de evolución
Réplica de lectura → particionamiento de tablas calientes → bases dedicadas para enterprise → shard por tenant (último recurso). Cada salto: métrica que lo exige + ADR (condición permanente 5).

## 13. Riesgos
| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Fuga cross-tenant por error de código | Media | **Crítico** | RLS + tests CI (MT-6) + revisión de seguridad por módulo + pentest |
| Noisy neighbor degrada la flota | Media | Alto | Cuotas MT-7 + métricas por tenant (RNF-OBS-002) |
| Costo de PITR por tenant | Media | Medio | Proceso documentado; automatización en Etapa C |
| Drift de RLS en nuevas tablas | Media | Crítico | Test CI: toda tabla nueva de negocio sin policy = build rojo |

## 14. Métricas
Incidentes de aislamiento (objetivo 0) · % tablas con policy (100%) · latencia añadida por RLS (<5%) · distribución de carga por tenant (top-1% de tenants vs. flota).

## 15. Criterios de aceptación
1. Pipeline de request con tenant en cada paso. ✅ 2. RLS + tests de aislamiento como requisito de CI. ✅ 3. Alternativas con costo y reemplazo. ✅ 4. Evolución por etapas medibles. ✅

## 16. Referencias cruzadas
Depende de: 25, 14, 19, 12, ADR-001/012, AUD-00 §5. Alimenta: 27 (sync por tenant), 24, 29 (API), 34/35 (seguridad/threat), 54 (SRE), 60 (FinOps).

## 17. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). Pool+RLS endurecido con 12 decisiones DC, pipeline de request, matriz de ataques de aislamiento, cuotas por tenant, operación por tenant |
