# ADI — Architecture Decision Index (Índice de Decisiones Arquitectónicas)

| Campo | Valor |
|---|---|
| Documento | ADI_Architecture_Decision_Index |
| Versión | 1.0 |
| Estado | ✅ Creado por instrucción adicional 1 de la aprobación de la Auditoría Integral (2026-07-29) |
| Responsable del índice | Fundador (Pascasio Emmanuel Reynoso Reyes) — toda alta/cambio de estado requiere su aprobación expresa o ADR |
| Regla | Toda decisión arquitectónica del proyecto existe exactamente una vez en este índice. Las familias de decisiones detalladas (MT, SY, EV, AP, IN, SE, EA, WA, MA, AIA, GA, DA) viven en sus documentos canónicos y se indexan aquí por familia con rango de IDs. |

---

## 1. Decisiones con documento ADR propio

| ID | Decisión | Estado | Documentos donde aplica | Dependencias | Fecha aprobación | Responsable | Reversibilidad | Impacto |
|---|---|---|---|---|---|---|---|---|
| ADR-011 | Estrategia Multicanal: Web App + PWA (un codebase React) + app nativa; paridad controlada; **autoridad del backend con lógica local provisional y re-validación en sync** (texto literal del Fundador); framework móvil PD | ✅ DC (v1.1) | 16, 18, 21, 22, 23, 27, 19 | N-1 (PD), Doc 27 | 2026-07-29 | Fundador | Reversible por canal (PWA↔Web); la regla de autoridad solo por ADR nuevo | Alto — define los tres canales y la ley de autoridad cliente/servidor |
| ADR-012 | Platform Administration Console: separación de planos como **principio permanente**; Admin API independiente (auth/authz/auditoría/versionado/límites); 10 campos de auditoría; régimen Fase 0-1 de acciones críticas | ✅ DC (v1.1) | 19, 21, 26, 29, 33 | Retención PD; SU-FLAGS | 2026-07-29 | Fundador | Solo por ADR + aprobación expresa; si una funcionalidad exige fusionar planos, se rediseña la funcionalidad | Alto — gobierna toda operación de plataforma |

## 2. Decisiones tempranas (ADR-001…010) — detalle en `ADR-001-010_Registro.md`

| ID | Decisión | Estado | Aplica en | Dependencias | Fecha | Responsable | Reversibilidad | Impacto |
|---|---|---|---|---|---|---|---|---|
| ADR-001 | Tenancy híbrida pool+RLS con camino a tenants dedicados | DC | 10, 12, 14, 25, 26 | — | AUD-00 (2026-07) | Fundador | Hacia más aislamiento, nunca menos | Crítico |
| ADR-002 | Sync: PowerSync adoptado (revertido desde motor propio); escrituras vía backend | DC; modalidad **PD (N-2)** | 14, 23, 24, 27 | N-2, PoC Fase 0 | AUD-00 D-1 (2026-07) | Fundador | Exit strategy documentada; adaptador MA-1 | Crítico |
| ADR-003 | PostgreSQL como base única inicial | DC | 12, 21, 25 | — | AUD-00 | Fundador | Por criterio (ClickHouse Etapa B) | Alto |
| ADR-004 | Backend .NET 8 | DC | 21, 24 | — | AUD-00 | Fundador | Costosa; solo con ADR + evidencia | Alto |
| ADR-005 | Monolito modular; extracción a servicios solo por métricas | DC | 10, 14, 20, 21, 24 | — | AUD-00 | Fundador | Por módulo, por diseño | Alto |
| ADR-006 | Analítica separada: vistas materializadas F1; ClickHouse Etapa B por criterio | DC | 16, 17, 25, 26, 30 | Criterio >50M filas / p95 >2 s | AUD-00 E-3 | Fundador | Activación por criterio | Medio |
| ADR-007 | AI Gateway multi-modelo con routing por costo | DC; proveedor **PD (PD-IA-1)** | 03, 10, 21, 32, 33 | PD-IA-1 | AUD-00 | Fundador | Sustitución sin tocar dominio | Alto |
| ADR-008 | PostgreSQL 16+ (RLS, ltree, pgvector, pgcrypto) | DC | 12, 21, 25 | — | AUD-00 | Fundador | Migración mayor expand/contract | Alto |
| ADR-009 | API REST versionada, deprecación 12 meses, eventos con esquema versionado | DC | 10, 14, 16, 29, 30 | — | AUD-00 | Fundador | Solo hacia políticas más estrictas | Alto |
| ADR-010 | i18n nativa, cero strings hardcodeados, glosario canónico | DC; idiomas **PD (PD-4)** | 10, 11, 13, 22 | PD-4 | AUD-00 | Fundador | Más idiomas sin redeploy | Medio |

## 3. Decisiones fundacionales (no-ADR)

| ID | Decisión | Estado | Fecha | Responsable | Reversibilidad | Impacto |
|---|---|---|---|---|---|---|
| DC-00 | Nombre oficial: **DONEFIXER** (única grafía válida) | ✅ DC | 2026-07-29 | Fundador | Solo por decisión formal del Fundador | Global (branding, N-5 marca) |

## 4. Familias de decisiones por documento canónico (Ola 3)

Los rangos completos de cada familia están en el **Canonical Identifier Registry**. Estado de todas: **DC propuestas → aprobadas con la Ola 3 (2026-07-29)**, salvo excepciones PD/SU marcadas en su documento.

| Familia | Documento canónico | Rango | Dependencias clave | Reversibilidad |
|---|---|---|---|---|
| MT (Multi-Tenant) | 26 | MT-1…12 | ADR-001 | Hacia más aislamiento |
| SY (Offline/Sync) | 27 | SY-1…15 | ADR-002, N-2 | Vía adaptador; N-2 abierta |
| EV (Eventos) | 30 | EV-1…7 | ADR-006/009 | Kafka por criterio E-2 |
| AP (API) | 29 | AP-1…12 | ADR-009 | Solo más estricto |
| IN (Integraciones) | 28 | IN-1…7 | ADR-009; WhatsApp SU (FinOps) | Por conector (ACL) |
| SE (Búsqueda) | 31 | SE-1…6 | ADR-008 (pgvector) | Typesense por criterio |
| EA (Empresarial) | 20 | EA-1…8 | Todos | Solo por ADR |
| WA (Web) | 22 | WA-1…10 | ADR-011 | Stack: solo con ADR |
| MA (Móvil) | 23 | MA-1…10 | ADR-011, **N-1/N-2 PD** | Agnóstica por diseño |
| AIA (Arquitectura IA) | 32 | AIA-1…9 | ADR-007, PD-IA-1 | Gateway protege dominio |
| GA (Gobierno IA) | 33 | GA-1…7 + P-33-1…7 | ADR-012 | Prohibiciones: solo ADR + Fundador |
| DA (Datos) | 25 | DA-1… | ADR-003/006/008 | Expand/contract |

## 5. Decisiones PD abiertas (registro de control)

| PD | Tema | Documento de referencia | Ventana de revisión |
|---|---|---|---|
| N-1 | Framework móvil | DECISIONES_N1-N10; Doc 23 §4 | Tras PoC comparativa (J-2) |
| N-2 | PowerSync Cloud vs. self-hosted | DECISIONES_N1-N10; Doc 27 | Tras PoC Fase 0 |
| N-3 | Presupuesto legal | DECISIONES_N1-N10 | Ola 4 (AO-6) |
| N-4 | Pagos/facturación | DECISIONES_N1-N10 | Después de N-7 |
| N-5 | Marca registrada (clases 9, 42) | DECISIONES_N1-N10 | Antes de lanzamiento público |
| N-6 | Idiomas de lanzamiento | DECISIONES_N1-N10; PD-4 | Ola 4 (AO-6) |
| N-7 | Incorporación/residencia fiscal | DECISIONES_N1-N10 | Bloquea N-4 y proveedor cloud |
| N-8 | Accesibilidad (VPAT formal) | DECISIONES_N1-N10 | Enterprise (Etapa B/C) |
| N-9 | Modelo de soporte | DECISIONES_N1-N10 | Antes de pilotos |
| N-10 | Equipo (solo + freelancers) | DECISIONES_N1-N10 | Por hito |
| PD-2 | North Star metric | Doc 02 | Ola 4 (AO-6) |
| PD-3 | Países piloto | Docs 01/03 | Antes de pilotos |
| PD-4 | Idiomas de lanzamiento | Docs 01/11 | Ola 4 (AO-6) |
| PD-RETENCIÓN | Retención de auditoría de plataforma | ADR-012 | Ola 4 (AO-6) |
| SU-FLAGS | Feature flags (FinOps/observabilidad) | ADR-012 | Ola 4 (AO-6) |
| PD-IA-1 | Proveedor/modelo LLM Etapa A | Doc 32 §9 | Antes de Fase 1 (configuración) |
| PD-CLOUD | Proveedor cloud específico | Doc 21 §6 | Depende de N-7 |

## 6. Exenciones activas

| ID | Objeto | Estado | Condiciones | Vence |
|---|---|---|---|---|
| EXENCIÓN-SPIKE-01 | Código de investigación técnica para Architecture Spike N-1/N-2 (solo flujo J-2) | ✅ DC (2026-07-29) | 8 reglas permanentes del Fundador; código experimental separado; reutilización en producción solo por ADR; cierre de N-1/N-2 sujeto a aprobación tras resultados | Al completarse S-6 |

| ADR-014 fase 1 | Write-path propio (outbox + idempotencia + HLC + re-validación servidor) como componente definitivo | ⏳ **DC-C — Decisión Condicional (2026-07-30)** | Registrado como "validación técnica preliminar del write-path"; **no es decisión definitiva**; su aprobación definitiva depende del resultado completo de la Fase 2 de la Spike y del cierre formal de N-2 (DECISIÓN DEL FUNDADOR DC-05) |
| ADR-014 definitivo | Estrategia de sincronización: PowerSync Cloud vs Self-Hosted (N-2) | ⏸️ Pendiente | Requiere Fase 2 de la Spike (Master Prompt v1.1, DC-01) + Anexo de Reproducibilidad (REGLA ADICIONAL); N-2 permanece PD hasta entonces |

---

*Registro de cambios — v1.0 (2026-07-29): creación por instrucción adicional 1 de la aprobación de la Auditoría Integral de Arquitectura.*
*v1.1 (2026-07-30): registro de la DECISIÓN DEL FUNDADOR sobre Spike Fase 2 — DC-01 (Master Prompt v1.1 adoptado como norma de la Fase 2, ámbito exclusivo N-2), DC-02 (matriz de decisión N-2 independiente, ponderación aprobada; la matriz de Doc 23 §4 queda exclusiva de N-1), DC-03 (Carril A autorizado: documentación e infraestructura de evaluación, no código de producción), DC-04 (Carril B condicionado a cuenta Cloud + Docker self-hosted + credenciales; N-2 sigue PD), DC-05 (ADR-014 fase 1 reclasificada como DC-C, validación técnica preliminar del write-path). REGLA ADICIONAL: Anexo de Reproducibilidad obligatorio para toda métrica de Fase 2.*
*v1.2 (2026-07-30): registro de la DECISIÓN DEL FUNDADOR sobre Fase 2B — DC-06 (Master Prompt v1.2 adoptado como norma de ejecución del Carril B, condicionado al cumplimiento íntegro de precondiciones; no modifica Constitución, EXENCIÓN-SPIKE-01, Doc 70 ni DC-01…DC-05), DC-07 (detención por precondiciones no cumplidas confirmada como mecanismo de gobernanza, no retraso; prohibida cualquier comparación mientras no estén completas), DC-08 (`SPIKE_F2B_Precondiciones.md` registrado como documento de control operativo de la Fase 2B, sincronizado con ADI e Índice Maestro), DC-09 (habilitación de entornos Cloud/Self-Hosted = actividad externa al sandbox; Carril B inicia solo con ambos validados), DC-10 (mientras Carril B pendiente: solo actividades que no modifiquen arquitectura, no generen código de producción, no alteren la comparativa N-2 y aporten valor directo; prioridad recomendada: preparar instrumentación de medición N-1 en dispositivos reales para ejecutarla tras N-2).*
*v1.3 (2026-07-30): registro de la DECISIÓN DEL FUNDADOR sobre el Gate de producción — DC-11 (Master Prompt — Production Readiness Gate Enterprise v1.0 adoptado como estándar normativo oficial del Documento 70; no modifica Constitución, Doc 70, ADRs ni DC-01…DC-10), DC-12 (Carril Gate autorizado: construcción del expediente operativo — Protocolo, Checklist, Matriz de Cumplimiento, Registro de Riesgos, Veredicto, verificación automática — con trazabilidad completa; NO es ejecución del gate, NO auditoría parcial, NO veredicto oficial; estado "Preparado para ejecución"; la auditoría solo inicia con N-1, N-2, PD-CLOUD, PD-IA-1 y PD-4 cerradas con evidencia reproducible; prohibido criterio sin referencia documental).*
*v1.4 (2026-07-30): registro de DC-13 — FASE 1 IMPLEMENTACIÓN ENTERPRISE (PRE-GO): se adopta el Master Prompt — Fase 1 Implementación Enterprise Production Ready v1.0 como estándar oficial de preparación de la implementación (sin iniciar código de producción). Autorizado el paquete `fase1_plan/` con 12 entregables. Reglas: WPs con 16 campos obligatorios; WP-00 = veredicto GO del Doc 70 sin rutas que lo eviten; paquetes afectados por ADR-013 (framework móvil) y ADR-014 (sync) parametrizados, no instanciables antes de su aprobación formal; trazabilidad completa + verificación automática de integridad. Restricciones: no código de producción, no implementaciones parciales, no cambios arquitectónicos, no nuevos ADR, no cierre de PDs. **Jerarquía normativa: DC-13 queda expresamente subordinada a (1) Constitución, (2) Documento 70, (3) ADRs aprobados, (4) DC-01…DC-12; en caso de conflicto prevalecen dichos documentos.** Cadena de preparación: DC-06…DC-10 (spikes) → DC-11/DC-12 (gate) → DC-13 (PRE-GO) → Doc 70 GO (autorización formal).*
*v1.5 (2026-07-30): registro de DC-14 — EXECUTION GOVERNANCE MANUAL (EGM): adoptado el Execution Governance Manual Enterprise v1.0 como manual operativo oficial de la ejecución diaria del desarrollo (desde el primer WP autorizado hasta producción). **Naturaleza normativa: manual de ejecución — NO es fuente de requisitos ni de arquitectura; no sustituye Constitución, Product Vision, PRD, RF, RNF, SRS, ADR, Doc 70, ADI ni Registry; los operacionaliza.** Autorizado el paquete `gobernanza_ejecucion/` (12 entregables). Regla de no duplicación: política existente = referencia a documento fuente + sección + solo procedimiento operativo; prohibido modificar umbrales, requisitos, criterios técnicos o decisiones arquitectónicas. Evidencia obligatoria por política: fuente normativa, evidencia requerida, responsable, método de verificación, automatización posible, frecuencia de control. Integridad: verificación automática (RF/RNF/ADR existentes, consistencia con Registry, sin referencias inventadas, sin duplicidad normativa) — ningún documento se aprueba con errores. Restricciones: no código de producción, no implementación funcional, no cambios de arquitectura/Doc 70/Constitución, no nuevos ADR, no cierre de PDs. Jerarquía: subordinado a Constitución → Doc 70 → ADRs → DC-01…DC-13. **Estado de la gobernanza: estructura de alto nivel completa (DC-06…DC-10 spikes → DC-11/12 gate → DC-13 PRE-GO → DC-14 EGM → Doc 70 GO); a partir de aquí el trabajo principal es ejecutar el plan conforme a la gobernanza, no ampliarla.***
*v1.6 (2026-07-30): registro del WP-UX-ART — UX/UI High-Fidelity Design Artifact autorizado como **entregable PRE-GO vinculado a DC-13/DC-14** (NO como nueva DC: el Fundador determina que las ejecuciones dentro del marco aprobado no inflan el registro de decisiones; DC-15 queda reservado para una decisión que cambie el corpus). Naturaleza: artefacto de diseño — no código de producción, no implementación, no MVP, no demo funcional; no modifica arquitectura, ADRs ni Doc 70. Autorizado el paquete `ux_artifact/` (10 entregables). Restricción: el HTML se identifica expresamente como "Design Artifact PRE-GO — No reutilizable como código de producción sin autorización posterior"; sin lógica de negocio, llamadas a API, autenticación funcional, sincronización, persistencia ni servicios. Validación: trazabilidad RF/RNF/estados UX/componentes DS por pantalla + verificación automática de integridad obligatoria.*
*v1.7 (2026-07-30): registro de **DC-15 — Adopción del Master Prompt Enterprise Production Implementation v1.0 (POST-GO)**. Decisión de gobernanza de ejecución: adopta dicho Master Prompt como especificación operativa oficial que regirá la ejecución de todos los Work Packages una vez autorizado el inicio del desarrollo. **DC-15 no crea una nueva capa jerárquica: la jerarquía del corpus permanece igual; únicamente incorpora la especificación.** No modifica arquitectura, Constitución, ADRs ni Documento 70, y no autoriza desarrollo antes del GO. Sub-decisiones: DC-15a adopción como referencia oficial de ejecución POST-Gate; DC-15b **estado inerte** (inactivo hasta veredicto compatible del Doc 70: antes, prohibido código de producción, apertura de WPs de implementación o uso del prompt como autorización); DC-15c interpretación conforme al orden de precedencia vigente: Constitución → Documento 70 → ADRs aprobados → decisiones de gobernanza (DC) → Master Prompt POST-GO (en conflicto, prevalece el nivel superior); DC-15d parametrización obligatoria {{ADR-013}}/{{ADR-014}} mientras N-1 y N-2 permanezcan abiertos — ningún WP fija esas decisiones sin cierre formal; DC-15e patrones (CQRS, Repository Pattern…) solo donde el corpus los apruebe y el contexto lo justifique — su mención no es aprobación universal; DC-15f registro en ADI + Índice Maestro con verificación automática de integridad antes de considerarse vigente.*
