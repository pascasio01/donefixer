# 43 — Module Specifications

| Campo | Valor |
|---|---|
| Documento | 43_Module_Specifications |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Precedencia | Doc 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 14 (Dominio), 11 (RF), 12 (RNF), 19 (Roles), 24–33 (arquitecturas de capa), 40 (Design System), MASTER_PROMPT_Implementacion_Enterprise_v1.0 |

> **Convención de evidencia:** DC · SU · PD. Este documento define la **plantilla única obligatoria** de especificación de módulos y las especificaciones de los módulos de la Etapa A. No contiene código ni DDL.

---

## 1. Plantilla única obligatoria (MS-0)

Toda especificación de módulo de DONEFIXER usa **exactamente** estos 17 campos, en este orden (ampliación obligatoria del Fundador, 2026-07-29). Ningún campo puede quedar vacío; si no aplica, se declara "No aplica — razón". (DC)

| # | Campo | Contenido requerido |
|---|---|---|
| 1 | Objetivo | Qué hace el módulo y para quién (persona del Doc 15) |
| 2 | Alcance | Capacidades incluidas, por fase |
| 3 | Exclusiones | Qué NO hace (Won't explícito, Doc 09) |
| 4 | RF relacionados | IDs del Registry |
| 5 | RNF relacionados | IDs del Registry |
| 6 | Entidades del dominio | Agregados/entidades del Doc 14 que toca |
| 7 | Eventos | Eventos de dominio emitidos/consumidos (Doc 30) |
| 8 | APIs | Operaciones de dominio expuestas (verbos explícitos, Doc 29 — sin endpoints definitivos) |
| 9 | Seguridad | Permisos requeridos (Doc 19), datos clasificados (Doc 25), controles RNF-SEC |
| 10 | Offline | Comportamiento offline/sync: buckets, conflictos aplicables (Doc 27), veredictos |
| 11 | IA | Casos de uso IA-* del Doc 32 y régimen de riesgo (Doc 33) |
| 12 | Observabilidad | Métricas de negocio/técnicas, logs, trazas (Doc 54) |
| 13 | Rendimiento | Presupuestos aplicables (RNF-PERF; Doc 47) |
| 14 | Dependencias | Módulos/servicios externos requeridos |
| 15 | Riesgos | Riesgos del módulo con mitigación |
| 16 | Criterios de aceptación | Binarios, medibles, heredados de RF + propios |
| 17 | Estrategia de pruebas | Capas de prueba obligatorias (Doc 47) |

---

## 2. Inventario de módulos — Etapa A

| Módulo | Contexto (Doc 14) | Personas primarias | Fases |
|---|---|---|---|
| MOD-IDENTITY | Identity & Access | P-C1 | 0–1 |
| MOD-REQUESTS | Trabajo (solicitudes) | P-R1, P-S1 | 1 |
| MOD-WORKORDERS | Trabajo (OT) | P-T1, P-S1 | 1 |
| MOD-SYNC | Infraestructura de sincronización | P-T1 (todos) | 1 |
| MOD-ASSETS | Activos | P-A1, P-T1 | 1 |
| MOD-PM | Planificación (PM) | P-D1 | 2 |
| MOD-INVENTORY | Inventario | P-S1, P-A1 | 2 |
| MOD-PROCUREMENT | Compras | P-M1, P-F1, P-V1 | 3 |
| MOD-REPORTS | Inteligencia | P-X1, P-M1 | 2 |
| MOD-NOTIFY | Notificaciones | Todos | 1 |
| MOD-TENANT-ADMIN | Configuración de tenant | P-C1 | 1 |
| MOD-PLATFORM | Plano plataforma (ADR-012) | Equipo DONEFIXER | 0–1 |
| MOD-AI-GATEWAY | IA transversal | Todos | 1 (IA-1, IA-2) |

---

## 3. Especificaciones (Etapa A, núcleo crítico)

> Por economía documental se especifican completos los 4 módulos definitorios (MOD-WORKORDERS, MOD-SYNC, MOD-IDENTITY, MOD-AI-GATEWAY) y en forma compacta los restantes. Las fichas compactas se expandirán a la plantilla completa antes de su construcción — la plantilla MS-0 es gate del Doc 70. (DC)

### 3.1 MOD-WORKORDERS

1. **Objetivo:** ciclo de vida completo de la OT según máquina de estados canónica, ejecutable 100% offline por el técnico (P-T1). (DC)
2. **Alcance:** F1 — creación, asignación, ejecución con checklist/evidencias/repuestos/tiempos, cierre provisional, códigos de falla; F2 — costos acumulados, verificación. (DC)
3. **Exclusiones:** no planificación de capacidad (MOD-PM); no facturación (MOD-PROCUREMENT); no OT predictivas automáticas (F5, IA-9). (DC)
4. **RF:** RF-WO-001…008; RF-SYNC-001…010. (DC)
5. **RNF:** RNF-SYNC-001…006; RNF-PERF-002/004; RNF-USE-001…005; RNF-ACC-002/004; RNF-SEC-003/005. (DC)
6. **Entidades:** WorkOrder (agregado raíz), ChecklistItem, Evidence, TimeEntry, MaterialUsage, FailureCode, WorkOrderTransition. (DC — Doc 14)
7. **Eventos:** `wo.approved · wo.assigned · wo.status_changed · wo.completed · wo.closed · evidence.attached`. (DC — Doc 30)
8. **APIs:** operaciones `:approve :assign :start :pause :resume :complete :verify :close :cancel` sobre work-orders; `:attach` evidencias; `:consume` repuestos. (DC — Doc 29 §verbos)
9. **Seguridad:** transiciones por rol según matriz Doc 19; evidencias con SHA-256 e inmutables tras cierre (RF-WO-003); firma ligada a sesión (RF-WO-007); datos nivel Confidencial (Doc 25). (DC)
10. **Offline:** bucket "mis OT + OT de mi zona" (SY-12); conflictos: estado OT = servidor autoritativo, evidencias = aditivas, repuestos = deltas; cierre offline = provisional hasta re-validación (SY-8/9); veredictos visibles (Doc 40 §9). (DC)
11. **IA:** IA-2 (estructuración de avisos, riesgo medio — humano confirma), IA-4 (sugerencia de diagnóstico, medio), IA-5 (resumen al cierre, bajo). Prohibiciones P-33-2 (cierre crítico). (DC)
12. **Observabilidad:** métricas: OT por estado, tiempo ciclo, tasa de veredictos ADJUST/REJECT por causa; trazas con `operation_id`. (DC — Doc 54)
13. **Rendimiento:** apertura OT local <1 s (RNF-PERF-004); completar OT en ≤5 toques efectivos (RNF-USE-001 ≤3 para tareas frecuentes). (DC)
14. **Dependencias:** MOD-IDENTITY, MOD-SYNC, MOD-ASSETS (árbol), MOD-INVENTORY (consumos), almacenamiento S3 (evidencias). (DC)
15. **Riesgos:** (a) complejidad de estados provisionales → UX de veredictos (Doc 40 §9), pruebas de campo; (b) QR incorrecto bloquea (RF-WO-006, SU) → calibrar con pilotos. (DC)
16. **Criterios de aceptación:** prueba literal J-2 modo avión pasa; máquina de estados sin transición ilegal posible (tests exhaustivos); evidencia tras cierre no editable (test); veredicto REJECT nunca pierde dato del técnico. (DC)
17. **Pruebas:** unit (dominio puro, matriz de transiciones), integración sync (8 casos normativos Doc 27), E2E J-2, chaos (RNF-SYNC-003), accesibilidad, performance (MA-8). (DC — Doc 47)

### 3.2 MOD-SYNC

1. **Objetivo:** transportar operaciones cliente↔servidor con cero pérdida, orden causal, idempotencia y re-validación de autoridad en servidor. (DC)
2. **Alcance:** F1 — outbox local, ingestión con veredictos, replicación por buckets, tombstones, HLC, reanudación de binarios. (DC)
3. **Exclusiones:** no decide reglas de negocio (invoca dominio); no resuelve conflictos fuera de la matriz normativa (los críticos van a humano). (DC)
4. **RF:** RF-SYNC-001…010 (no negociables). (DC)
5. **RNF:** RNF-SYNC-001…006; RNF-MOB-003/004; RNF-OBS-001; RNF-SEC-005. (DC)
6. **Entidades:** SyncOperation (operation_id, HLC, payload, veredicto), SyncBucket, Tombstone, DeviceReplica. (DC — Docs 14/27)
7. **Eventos:** `sync.conflict_queued · sync.operation_verdict`. (DC)
8. **APIs:** canal de sync (PowerSync según N-2 PD) + operación `:submit-operations` del write-path. (DC — sin endpoints definitivos)
9. **Seguridad:** transporte TLS 1.3; SQLCipher local (RNF-SEC-003); aislamiento RLS también en write-path (Doc 26); revocación de dispositivo → borrado remoto (RNF-SEC-005). (DC)
10. **Offline:** es el módulo offline por definición: ≥7 días / 200 operaciones (RNF-SYNC-003); 8 casos límite normativos asignados a tests. (DC)
11. **IA:** ninguna (No aplica — la IA consume eventos, no el canal de sync). (DC)
12. **Observabilidad:** éxito diario por dispositivo (>99.9%), lag por dispositivo (RNF-SYNC-006), cola de conflictos, outbox depth. (DC)
13. **Rendimiento:** convergencia <60 s p95 con red estable (RNF-SYNC-002); búsqueda FTS local ≤300 ms (Doc 23 MA-8). (DC)
14. **Dependencias:** PowerSync (N-2 PD), SQLite/SQLCipher, PostgreSQL, MOD-IDENTITY. (DC)
15. **Riesgos:** dependencia PowerSync → adaptador + fallback Zero + PoC previa a N-2 (R-1 auditoría). (DC)
16. **Criterios de aceptación:** pérdida de datos = 0 en chaos tests; 8/8 casos normativos pasan; veredictos 100% auditados; sync exitoso tras wipe+relogin sin duplicados (idempotencia). (DC)
17. **Pruebas:** integración sync, conflictos (matriz completa), chaos (red intermitente, kill de proceso a mitad de operación), DR (restauración de réplica), performance bajo 200 ops acumuladas. (DC — Doc 47)

### 3.3 MOD-IDENTITY

1. **Objetivo:** autenticación OIDC, membresías multi-tenant, RBAC+ABAC efectivo y contexto de tenant en cada petición. (DC)
2. **Alcance:** F0-1 — login, MFA (admins), invitaciones, membresías, revocación por dispositivo, pipeline tenant. (DC)
3. **Exclusiones:** no administra plano plataforma (MOD-PLATFORM/Admin API); no HR/nómina (Doc 01 §12 bis). (DC)
4. **RF:** RF-USR-001…003; RF-TEN-001…003. (DC)
5. **RNF:** RNF-SEC-001/004/005/006; RNF-PRV-001. (DC)
6. **Entidades:** User, Membership, Role, Permission, Device. (DC)
7. **Eventos:** `user.invited · membership.activated · membership.deactivated · device.revoked`. (DC)
8. **APIs:** operaciones de membresía/dispositivos; emisión de contexto tenant (claim → set_config). (DC)
9. **Seguridad:** Zero Trust, least privilege; tokens corta vida; MFA obligatorio admins (RNF-SEC-004); tests de aislamiento en CI (RNF-SEC-006). (DC)
10. **Offline:** sesión con desbloqueo local por política de tenant (MA-7, SU); revocación efectiva al próximo contacto de red. (DC)
11. **IA:** ninguna directa (las Service Accounts IA se autentican por este módulo — Doc 19 §11). (DC)
12. **Observabilidad:** logins fallidos, revocaciones, latencia de pipeline tenant. (DC)
13. **Rendimiento:** validación JWT + pipeline <50 ms p95 (contribuye a RNF-PERF-001). (SU)
14. **Dependencias:** proveedor OIDC (SU), PostgreSQL RLS. (DC)
15. **Riesgos:** misconfiguración de RLS → defensa en profundidad (MT-3) + tests de aislamiento bloqueantes. (DC)
16. **Criterios de aceptación:** 100% de requests con `app.current_tenant` correcto; imposibilidad demostrada de cruzar tenant (batería de ataques, Doc 26); revocación <5 min efectiva. (DC)
17. **Pruebas:** seguridad (matriz de ataques MT), integración OIDC, E2E multi-membresía, performance de pipeline. (DC)

### 3.4 MOD-AI-GATEWAY

1. **Objetivo:** punto único de acceso a capacidades IA: plantillas versionadas, enmascaramiento, cuotas, FinOps, cacheo, registro. (DC — AIA-1)
2. **Alcance:** F1 — IA-1 copiloto (cite-or-abstain), IA-2 estructuración de avisos; F3+ — resto IA-*. (DC)
3. **Exclusiones:** no entrena modelos (P-33-7); no ejecuta acciones de riesgo medio/alto sin aprobación humana (GA-1). (DC)
4. **RF:** RF-RPT-001 (copiloto consulta), RF-REQ-002 (triage asistido). (DC)
5. **RNF:** RNF-AI-001…007; RNF-FIN-002; RNF-PRV-001/004. (DC)
6. **Entidades:** AIRequest (tenant, caso de uso, modelo, tokens, costo), PromptTemplate (versionada), AIEvaluation. (DC)
7. **Eventos:** `ai.decision_recorded`. (DC — Doc 30)
8. **APIs:** operación interna `:complete :embed :classify` (no pública directa). (DC)
9. **Seguridad:** datos nivel Restringido nunca salen (AIA-4); enmascaramiento PII; Service Accounts con RBAC propio. (DC)
10. **Offline:** degradación explícita; núcleo funcional sin IA (RNF-AI-005). (DC)
11. **IA:** es el módulo de IA; régimen Doc 33 completo (GA-1…7, P-33-1…7). (DC)
12. **Observabilidad:** costo por tenant/caso de uso, latencia copiloto <5 s (RNF-AI-006), tasa de abstención, tasa de aceptación. (DC)
13. **Rendimiento:** cacheo de respuestas idempotentes; latencia copiloto p95 <5 s. (DC)
14. **Dependencias:** proveedor LLM (**PD-IA-1 — bloquea configuración, no arquitectura**), pgvector. (DC/PD)
15. **Riesgos:** alucinación → cite-or-abstain + umbral de apagado (AIA-6/7); costo → línea roja 30% (RNF-FIN-002). (DC)
16. **Criterios de aceptación:** 100% respuestas con cita o abstención (test sobre golden-set); 0 datos Restringidos en payloads de salida (test); umbral de apagado demostrado. (DC)
17. **Pruebas:** golden-set por caso de uso, evaluación de regresión pre-release, test de caída del proveedor, FinOps (simulación de cuota). (DC)

### 3.5 Fichas compactas (expandir a MS-0 antes de construcción)

| Módulo | RF clave | Offline | IA | Riesgo dominante |
|---|---|---|---|---|
| MOD-REQUESTS | RF-REQ-001…005 | Captura PWA con cola (WA-3); QR sin cuenta | IA-2 | Intake anónimo abusable → rate limit (RNF-SCL-003) |
| MOD-ASSETS | RF-AST-001…004 | Árbol en réplica; escaneo QR offline | IA-4 (historial similar) | Jerarquías profundas → ltree (DA) |
| MOD-PM | RF-PM-001…003 | Generación en servidor; consulta offline | IA-7 | Triggers duplicados → idempotencia |
| MOD-INVENTORY | RF-INV-001…003 | Deltas offline; nunca `set` | IA-6 (sugerencia, no ejecución — P-33-3) | Stock negativo fantasma → re-validación |
| MOD-PROCUREMENT | RF-PROC-001…004 | No (canal web) | IA-10 (F5) | P-33-1: IA nunca aprueba facturas |
| MOD-REPORTS | RF-RPT-001…004 | No (web) | IA-1, IA-5 | Dashboards lentos → criterio ClickHouse |
| MOD-NOTIFY | RF-NTF-001…003 | Push como señal, no transporte (MA-9) | — | Costo WhatsApp (H-25, FinOps) |
| MOD-TENANT-ADMIN | RF-TEN-001…003, RF-PLT-* | No | — | Misconfiguración → auditoría 10 campos |
| MOD-PLATFORM | RF-PLT-001…004 | No | — | Separación de planos (ADR-012) |

---

## 4. Criterios de aceptación del documento

1. Plantilla única de 17 campos definida y obligatoria. ✅
2. Módulos definitorios especificados completos; resto con ficha compacta y gate de expansión. ✅
3. Sin código, sin DDL, sin endpoints definitivos; PD intactas (PD-IA-1, N-2). ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación (Ola 4, documento 2 de 8) con la plantilla de 17 campos de la ampliación obligatoria del Fundador.*
