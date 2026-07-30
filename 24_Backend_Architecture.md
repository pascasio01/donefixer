# DONEFIXER — 24 · Backend Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)
> **Evidencia:** DC para decisiones derivadas de aprobados (ADR-004/005, docs 10–14, 25–27); SU para detalles de implementación; PD marcadas.

---

## 1. Objetivo
Definir la arquitectura del servidor de aplicaciones que ejerce la **autoridad del dominio** (ADR-011 v1.1): estructura modular, capas, write path de sync, jobs, y su evolución controlada de monolito modular a servicios cuando la evidencia lo exija.

## 2. Alcance
Backend de negocio (API pública + lógica de dominio + workers), Admin API de plataforma (superficie, según ADR-012), integración con sync (doc 27), eventos (doc 30). No cubre infraestructura (doc 52) ni IA interna (docs 32/33).

## 3. Exclusiones
Código, framework de IA (32), frontend (22/23), IaC (52).

## 4. Decisiones confirmadas (DC)

| # | Decisión | Trazabilidad |
|---|---|---|
| BK-1 | **.NET 8+ (C#) ASP.NET Core como backend núcleo**, monolito modular | ADR-004/005 (aprobados en gobierno); alternativas §9 |
| BK-2 | **Separación estricta dominio / aplicación / infraestructura** (regla del Fundador para Ola 3): el dominio no conoce HTTP, BD ni frameworks | Regla Ola 3; doc 14 canónico |
| BK-3 | Módulos = contextos delimitados del dominio (identity, assets, work, planning, inventory, procurement, governance); frontera por ID + eventos, no joins trans-módulo | doc 14 §7.1, ADR-005 |
| BK-4 | **Write path de sync en el backend** (re-validación, conflictos) — doc 27 §7 | ADR-011 v1.1 |
| BK-5 | Outbox transaccional para eventos (mismo commit que el dato); workers para procesamiento asíncrono | AUD-00 §4, doc 30 |
| BK-6 | Admin API separada (auth/authz/auditoría/versionado/límites independientes) | ADR-012 v1.1 (aprobado) |
| BK-7 | Jobs con cola ligera en Fase 1 (cola PostgreSQL o Redis); Kafka aplazado a Etapa B por criterio (E-2) | AUD-00 (condición 5: sin sobrearquitectura) |
| BK-8 | Autorización: RBAC+ABAC evaluados en servidor en cada operación (la UI nunca es seguridad) | doc 19 §12, ADR-011 v1.1 |
| BK-9 | IA invocada vía gateway desde el backend (sin servicio Python en Fase 1 — aplazado E-5) | AUD-00 D-5 |
| BK-10 | Extracción a servicios solo por métrica + ADR (escala o equipo que lo demuestre) | ADR-005, condición permanente 5 |

## 5. Decisiones pendientes (PD)
N-2 (afecta la topología del servicio de sync, no el write path) · motor de colas definitivo en Etapa B (SU: Hangfire/Cola PG → evaluar) · SU-FLAGS (librería propia de flags).

## 6. Supuestos (SU)
Un proceso único de aplicación + workers en el mismo artefacto cubre Etapa A (50 tenants) con escalado horizontal trivial (stateless).

## 7. Arquitectura por capas (regla del Fundador: dominio / aplicación / infraestructura)

```
┌─ INTERFACES (adaptadores de entrada)
│   REST API v1 (pública) · Write API de sync · Webhooks entrantes · Admin API (plataforma)
├─ APLICACIÓN (casos de uso por módulo)
│   Comandos/consultas · políticas de autorización (RBAC+ABAC) · orquestación de transacciones
├─ DOMINIO (canónico, doc 14)
│   Entidades, invariantes, máquina de estados OT, reglas de conflicto, servicios de dominio
│   → PURO: sin dependencias de frameworks, HTTP ni BD
├─ INFRAESTRUCTURA (adaptadores de salida)
│   Repositorios (EF Core) · RLS/contexto tenant · outbox · storage S3 · LLM gateway · colas
└─ WORKERS (mismo artefacto, procesos aparte en Etapa A)
    Generación PM · KPIs/rollups · notificaciones · conciliación · purgas programadas
```

**Reglas vinculantes:** (1) las dependencias apuntan hacia el dominio, nunca al revés; (2) toda mutación pasa por la capa de aplicación con autorización + validación de dominio — no existen "atajos" de escritura (incluidos agentes IA y consola, que usan APIs); (3) cada módulo es potencialmente extraíble porque sus líneas son ID+eventos (BK-3/BK-10).

## 8. Write path de sync (detalle del backend — complementa doc 27)

1. Recibe lote → autentica dispositivo → deduplica por `operation_id` (tabla de operaciones procesadas).
2. Ordena por causalidad (HLC + grafo de dependencias por entidad).
3. Por operación, en una transacción: carga agregado con `FOR UPDATE` lógico (versión) → evalúa autorización (doc 19) → evalúa invariantes de dominio (máquina de estados, stock, SLA) → **ACEPTA** (aplica + evento outbox) / **AJUSTA** (aplica valor final + registra) / **RECHAZA** (registra motivo; conflicto crítico → cola humana).
4. Responde el resultado por operación (confirmado/ajustado/rechazado) — el cliente lo hace visible (RF-SYNC-005).
5. **Idempotencia total:** reejecutar el lote produce el mismo estado y los mismos resultados (RF-SYNC-002).

## 9. Alternativas evaluadas (regla Ola 3)

| Alternativa | Ventajas | Desventajas/costo | Reemplazo | Veredicto |
|---|---|---|---|---|
| **.NET 8 monolito modular (elegido)** | Tipado fuerte end-to-end; rendimiento top; tooling enterprise; una sola especialidad para Etapa A; mejor historia de mantenimiento a 10 años | Pool de talento menor que JS en algunas regiones | Extracción a servicios por módulo (BK-3/BK-10); API-First lo hace reemplazable | **Etapa A–B** |
| Node/NestJS | Comparte TS con web | Tipado más débil en dominio complejo; mismo nivel de madurez | Equivalente | Descartada (sin ventaja decisiva) |
| Go | Rendimiento, simplicidad | Menor expresividad para dominio rico (máquinas de estado, invariantes) | — | Descartada |
| Java/Spring | Madurez enterprise | Verbosidad operativa similar a .NET sin ventaja | — | Descartada |
| Microservicios desde el inicio | Escala selectiva | Complejidad operativa inasumible para 1–3 personas; distribuye las invariantes | — | **Prohibido en Fase 1 (BK-10)** |
| Servicio Python IA separado (F1) | Ecosistema ML | Duplica pipeline y contratación | Se introduce en Etapa B con ML propio (E-5) | Aplazado |

## 10. Estrategia de evolución
Etapa A: monolito modular + workers (stateless, escala horizontal) → Etapa B (criterios medidos): réplicas gestionadas, cola dedicada, servicio Python ML, posible extracción del módulo de reporting o sync si su carga lo exige (métrica: >30% de CPU de la flota por un módulo + equipo ≥6) → Etapa C: servicios por dominio donde el equipo lo justifique. **Cada extracción: métrica + ADR.**

## 11. Impacto operativo
Un artefacto → un pipeline CI/CD, una observabilidad, un runbook (Etapa A). Workers como procesos del mismo artefacto (mismo despliegue, distinta escala). Admin API: mismo artefacto, **puerto/superficie separada con auth propia** (BK-6) — en Etapa B, despliegue separado.

## 12. Riesgos
| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Monolito se degrada en "bola de barro" | Media | Alto | Fronteras por contexto (BK-3) + revisión de arquitectura trimestral + regla de dependencias en CI |
| Contratación C# lenta | Media | Medio | Documentación de dominio canónica facilita onboarding (doc 14); N-10 PD |
| Write path de sync como cuello de botella | Media | Medio | Lotes, índices tenant-first, métrica dedicada; escalado horizontal stateless |
| Acoplamiento prematuro a EF Core en dominio | Media | Medio | Regla BK-2 verificada en revisión de código |

## 13. Métricas
p95 por endpoint (RNF-PERF-001) · throughput del write path de sync (lotes/s, ops/s) · tiempo de proceso de lote · % operaciones rechazadas por tipo · cobertura ≥80% núcleo (RNF-MNT-001).

## 14. Criterios de aceptación
1. Separación dominio/aplicación/infraestructura explícita con reglas vinculantes. ✅ 2. Write path de sync detallado con idempotencia. ✅ 3. Alternativas con costo y reemplazo. ✅ 4. Evolución por métricas, no por moda. ✅

## 15. Referencias cruzadas
Depende de: 10–14, 19, 25–27, ADR-004/005/011/012. Alimenta: 29 (API), 30 (eventos), 28 (integraciones), 32 (IA), 47 (pruebas), 50/51 (DevOps/CI-CD), 61 (release).

## 16. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). Monolito modular .NET con separación estricta de capas, write path de sync con idempotencia total, workers en mismo artefacto, extracción por métrica |
