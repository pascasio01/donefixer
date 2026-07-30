# 32 — AI Architecture

| Campo | Valor |
|---|---|
| Documento | 32_AI_Architecture |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Autoría | Equipo de documentación DONEFIXER bajo dirección del Fundador |
| Precedencia | Documento 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 01 (AI-First como principio), 14 (Dominio), 19 (Roles — cuentas de servicio IA), 25 (pgvector), 27 (Sync), 29 (API), 31 (Search SE-5/SE-6), 03 (§11 bis costos de IA) |

> **Convención de evidencia:** DC · SU · PD en toda afirmación relevante.
> Documento hermano normativo: **33_AI_Governance** (políticas, prohibiciones, FinOps). Este documento define el *cómo técnico*; el 33 define el *qué está permitido*. Ninguna capacidad aquí descrita está habilitada si el Doc 33 la prohíbe. (DC)

---

## 1. Propósito y alcance

Define la arquitectura de inteligencia artificial de DONEFIXER bajo el principio **AI-First**: la IA no es un módulo añadido sino una capacidad transversal del dominio — pero implementada con **alimentación gradual** (Etapa A con APIs gestionadas, Etapa B con servicio propio solo si los criterios medibles lo justifican), sin sobre-arquitectura prematura (condición permanente del Fundador). (DC)

**Fuera de alcance:** políticas de gobierno (Doc 33), selección de proveedor/modelo específico de LLM (**PD-IA-1**, nueva PD registrada en §9), código y prompts definitivos. (DC)

---

## 2. Casos de uso de IA por fase (trazados al dominio)

| ID | Caso de uso | Fase | Riesgo (Doc 33) | Trazabilidad |
|---|---|---|---|---|
| IA-1 | **Copiloto de consulta en lenguaje natural** ("¿qué OT vencen esta semana en Planta 2?") con respuesta citada o abstención | F1 | Bajo (solo lectura) | Doc 31 SE-6; RF-RPT |
| IA-2 | **Estructuración de avisos** (foto + voz → solicitud clasificada: activo probable, prioridad sugerida, tipo de falla) | F1 | Medio (sugiere, humano confirma) | J-1; RF-REQ |
| IA-3 | **Búsqueda semántica** sobre historial de OT, activos y manuales | F3 | Bajo | Doc 31 SE-5; pgvector (Doc 25) |
| IA-4 | **Sugerencia de diagnóstico** basada en códigos de falla (problema/causa/acción) e historial del activo similar | F3 | Medio | Doc 14 §Códigos de falla |
| IA-5 | **Resumen automático de OT al cierre** para el técnico y para reportes gerenciales | F3 | Bajo | RF-WO; J-8 |
| IA-6 | **Predicción de demanda de repuestos** (sugerencia de reabastecimiento) | F4 | Medio | Doc 14 §Inventario; RF-INV |
| IA-7 | **Priorización asistida de backlog** (riesgo × criticidad × vencimiento) | F4 | Medio | Doc 14 §PM; P-D1 |
| IA-8 | **Detección de anomalías en medidores** | F4 (medidores nativos; sensores IoT en Fase 4) | Medio | Doc 14 §Medidores |
| IA-9 | **Mantenimiento predictivo (PdM)** | F5 | Alto | Doc 01 (visión 10 años) |
| IA-10 | **Agentes de automatización** (ej.: conciliación de facturas, seguimiento de SLA) | F5 | Alto — con aprobación humana obligatoria | Doc 30 (eventos ai.*); Doc 33 |

> **Regla:** cada caso de uso entra al producto solo vía **FEP** (Doc 02 §10 bis) con evidencia de demanda, y opera bajo el régimen de riesgo del Doc 33. (DC)

---

## 3. Decisiones AIA (AI Architecture)

### AIA-1. Etapa A: APIs gestionadas de LLM detrás de una capa de abstracción propia. (DC)

Toda llamada a modelos pasa por un **AI Gateway interno** (módulo del monolito, Doc 24) que provee: selección de modelo por caso de uso, plantillas de prompt versionadas, redacción/enmascaramiento de datos (ver AIA-4), límites por tenant, registro de costos, y cacheo de respuestas idempotentes. Ningún componente del dominio habla directo con un proveedor de IA. (DC)

**Justificación trazada:** equipo mínimo (N-10 PD) no puede operar infraestructura de ML en Etapa A; la línea roja FinOps (Doc 33) exige medición por tenant desde el día uno; el cambio de proveedor/modelo no puede tocar el dominio (PD-IA-1 queda abierta sin riesgo de lock-in arquitectónico). (DC)

### AIA-2. Los agentes de IA son cuentas de servicio, no usuarios especiales. (DC)

Los agentes operan mediante **Service Accounts** con RBAC propio (Doc 19: 5 cuentas de servicio IA definidas), sujetos a la misma API, los mismos límites y la misma auditoría que cualquier actor. Las prohibiciones se implementan como **ausencia de permisos** (Doc 33): el agente no "promete no aprobar facturas" — simplemente no tiene el permiso. (DC)

### AIA-3. La IA nunca modifica estado oficial directamente. (DC)

Todo output de IA que aspire a cambiar datos entra por una de dos vías: (a) **sugerencia** visible que un humano acepta/edita/rechaza (riesgo medio/alto), o (b) **borrador** que requiere confirmación. La máquina de estados de OT (Doc 14) y el write-path de sync (Doc 27) no distinguen ni permiten bypass por origen IA. (DC)

### AIA-4. Privacidad y minimización de datos en prompts. (DC)

- Clasificación de datos de 4 niveles (Doc 25): datos nivel Restringido **nunca** salen hacia proveedores externos de IA.
- Enmascaramiento de PII en el AI Gateway antes de llamadas externas; configuración por tenant (clientes Enterprise pueden exigir no-envío, degradando a funciones locales).
- Retención cero exigida contractualmente al proveedor (criterio de PD-IA-1). (DC)

### AIA-5. Búsqueda semántica con pgvector dentro de PostgreSQL. (DC)

Embeddings almacenados en PostgreSQL (pgvector, Doc 25), generados de forma asíncrona vía eventos (Doc 30) con reindexación versionada por modelo. Base vectorial dedicada: **diferida** — criterio de activación: >10M de vectores o p95 de búsqueda semántica >500 ms. (DC)

### AIA-6. Regla cite-or-abstain como contrato técnico. (DC)

El copiloto (IA-1) solo responde con **citas a registros reales del tenant** (IDs de OT, activos, reportes) o se **abstiene** ("no tengo datos suficientes"). Implementación: recuperación acotada por permisos del usuario (Doc 31 SE-6), composición de respuesta con referencias verificables, y evaluación automática de fidelidad en muestra (Doc 33 §Calidad). Prohibido responder de memoria paramétrica del modelo. (DC)

### AIA-7. Evaluación continua como componente arquitectónico. (DC)

Cada caso de uso de IA tiene: dataset de evaluación propio (curado de pilotos, anonimizado), métrica de calidad definida (precisión de clasificación, tasa de abstención correcta, tasa de aceptación de sugerencias por humanos), y **umbral de apagado**: si la calidad cae bajo el umbral en producción, el caso de uso se degrada a modo manual automáticamente. (DC)

### AIA-8. IA y Offline-First: degradación explícita. (DC)

Sin conectividad no hay IA externa; la app lo comunica sin fricción ("las sugerencias IA se generarán al sincronizar"). Capacidades ligeras on-device (clasificación básica de fotos de avisos) se evalúan en Etapa B — **SU**, no compromiso. La ausencia temporal de IA nunca bloquea el flujo de trabajo del técnico (Doc 16 J-2). (DC)

### AIA-9. Cuotas y medición de costo por tenant desde Etapa A. (DC)

Cuotas por plan (Doc 03 §11 bis), medición de tokens/costo por tenant y por caso de uso en el AI Gateway, dashboard FinOps (Doc 21 §5), y línea roja: costo de IA >30% del ingreso del tenant dispara revisión (Doc 33). (DC)

---

## 4. Vista de componentes (Etapa A)

```
Canales (Web/Móvil) ──► API REST ──► Módulo de aplicación
                                          │
                              ┌───────────▼────────────┐
                              │   AI Gateway interno   │
                              │ · plantillas de prompt │
                              │ · enmascaramiento PII  │
                              │ · cuotas + FinOps      │
                              │ · cacheo + registro    │
                              └───────┬─────────┬──────┘
                                      │         │
                        ┌─────────────▼──┐   ┌──▼───────────────┐
                        │ Proveedor LLM  │   │ pgvector (Post-  │
                        │ gestionado     │   │ greSQL) semántica│
                        │ (PD-IA-1)      │   └──────────────────┘
                        └────────────────┘
Eventos de dominio (Doc 30) ──► Worker de embeddings ──► pgvector
Agentes IA (Service Accounts, Doc 19) ──► misma API REST, permisos
propios, auditoría completa; aprobación humana vía flujo de sugerencias
```

---

## 5. Alternativas evaluadas

| Alternativa | Razón de descarte/posposición | Evidencia |
|---|---|---|
| **APIs gestionadas + gateway propio (elegida, Etapa A)** | — | DC |
| Servicio propio de ML (Python) desde el inicio | Sobrecarga operativa para equipo mínimo; criterio de activación definido (volumen/costo/casos que excedan APIs) — Etapa B | DC pospuesta |
| Modelos open-weight auto-hospedados (Etapa A) | Costo fijo de GPU y operación incompatible con FinOps en fase de pilotos; re-evaluar si clientes Enterprise exigen no-envío de datos | DC pospuesta |
| Framework de agentes complejo (orquestadores multi-agente) | Sin casos de uso que lo justifiquen en F1–F4; FEP lo exigiría para F5 | DC pospuesta |
| Vector DB dedicada | Criterio de activación definido (AIA-5) | DC pospuesta |

---

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Alucinación del copiloto en datos operativos | Alto | Cite-or-abstain (AIA-6) + evaluación continua (AIA-7) + umbral de apagado |
| Costo de IA desbordado por adopción | Alto | Cuotas por plan + línea roja FinOps + cacheo (Doc 33) |
| Fuga de datos a proveedor externo | Alto | AIA-4 (enmascaramiento, niveles, retención cero contractual, opción no-envío Enterprise) |
| Lock-in de proveedor | Medio | AI Gateway + PD-IA-1 abierta con criterios de cambio |
| Dependencia de IA para flujos críticos | Medio | AIA-8: la IA nunca bloquea el trabajo; degradación manual siempre disponible |

---

## 7. Evolución a 10 años

- **Etapa B (criterios medibles):** servicio Python de ML propio (pronósticos, PdM inicial), modelos open-weight para tenants con restricción de datos, clasificación on-device de evidencias.
- **Etapa C:** PdM completo (IA-9), agentes de automatización con aprobación humana (IA-10), fine-tuning por industria sobre datos anonimizados y con consentimiento del tenant (Doc 33 lo regula).
- En todas las etapas: AI Gateway, Service Accounts, cite-or-abstain y FinOps por tenant permanecen como estructura invariante. (DC)

---

## 8. Criterios de aceptación de este documento

1. Todo caso de uso trazado al dominio y a fase; todo componente presente con justificación y todo diferido con criterio. ✅
2. Coherencia con Doc 19 (Service Accounts), Doc 31 (SE-5/SE-6), Doc 25 (pgvector) y Doc 30 (eventos). ✅
3. Sin proveedor de LLM elegido (PD-IA-1 abierta). ✅
4. Separación dominio/aplicación/infraestructura respetada (IA como módulo de infraestructura tras gateway, jamás en dominio puro). ✅

---

## 9. Nuevas PD registradas en este documento

| PD | Descripción | Bloquea |
|---|---|---|
| PD-IA-1 | Proveedor/modelo de LLM para Etapa A. Criterios de evaluación: calidad ES/EN, retención cero contractual, costo por token vs. línea roja FinOps, latencia p95, estabilidad de versionado. | Configuración de Fase 1, no la arquitectura |

---

*Registro de cambios — v1.0: creación (Ola 3, documento 13 de 14).*
