# DONEFIXER — 12 · Non-Functional Requirements (Catálogo Global RNF)

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Convención:** `RNF-<AREA>-###` · cada valor lleva su **fuente** (DC de decisión aprobada / SU hipótesis / referencia de industria) — prohibido SLOs arbitrarios (AUD-00 §14). Los RNF son **objetivos internos de diseño**; ninguno es compromiso contractual hasta Etapa B (DC AUD-00).

---

## 1. Objetivo
Definir cuánto es "suficientemente bueno" en cada dimensión de calidad, con valores verificables y su justificación, para que arquitectura, pruebas y SRE midan contra lo mismo.

## 2. Alcance
Rendimiento, disponibilidad, sync/offline, seguridad, privacidad, accesibilidad, usabilidad, escalabilidad, observabilidad, móvil, IA, costos (FinOps), compatibilidad, mantenibilidad.

## 3. Exclusiones
SLAs contractuales (doc 37/Etapa B); RNF específicos de módulo (heredan estos y solo declaran endurecimientos, doc 43).

## 4. Decisiones confirmadas (DC)
SLOs derivados de capacidad real del equipo, no aspiracionales (AUD-00 §14) · sin promesas de infalibilidad (Charter §7.4) · WCAG 2.2 AA como objetivo interno (SU hasta N-8) · régimen de acciones críticas de plataforma (ADR-012 §3.9) · "prevenir, detectar, contener, recuperar, aprender".

## 5. Decisiones pendientes (PD)
N-8 (accesibilidad contractual) · N-2 (afecta RNF de sync operativo) · PD-3/PD-4 (afectan RNF de i18n y compatibilidad regional) · N-9 (afecta RNF de soporte).

## 6. Supuestos (SU)
Los valores numéricos sin fuente externa son objetivos de diseño del equipo, calibrables tras el primer trimestre de producción con datos reales.

## 7. Dependencias
Docs 09, 11, 14, 16, 17, ADR-011/012, AUD-00. Alimenta: 10 (SRS), 20–33 (arquitectura), 47 (pruebas), 49 (performance), 54/55 (observabilidad/SRE), 61 (release).

## 8. Riesgos
| Riesgo | Mitigación |
|---|---|
| Valores aspiracionales no medibles | Cada RNF tiene método de medición declarado |
| RNF ignorados por módulos | Herencia obligatoria (doc 43 solo declara excepciones) |

---

## 9. Catálogo RNF

### 9.1 Rendimiento (RNF-PERF)

| ID | Requisito | Valor objetivo | Fuente | Medición |
|---|---|---|---|---|
| RNF-PERF-001 | Latencia API p95 (lecturas tenant-scoped) | <500 ms | SU (calibrado desde AUD-00 §14; el valor original 300 ms se relajó por realismo de Etapa A) | APM por endpoint |
| RNF-PERF-002 | Latencia local móvil (lecturas SQLite) | <100 ms p95 | Referencia local-first (DC AUD-00 §4) | Telemetría móvil |
| RNF-PERF-003 | Tiempo de carga inicial web (P95, red 4G) | <3 s | SU (estándar UX B2B) | RUM |
| RNF-PERF-004 | Apertura de OT en app (datos locales) | <1 s | SU | Telemetría móvil |
| RNF-PERF-005 | Consultas N+1 | 0 toleradas | DC calidad | Tests de integración |

### 9.2 Disponibilidad y continuidad (RNF-AVL)

| ID | Requisito | Valor | Fuente | Medición |
|---|---|---|---|---|
| RNF-AVL-001 | Disponibilidad servicio (objetivo **interno**, no contractual) | 99.5% mensual | DC AUD-00 §14 (equipo pequeño; 99.9% original era aspiracional) | Uptime monitor |
| RNF-AVL-002 | RPO | ≤15 min | SU (WAL archiving) | Ensayo trimestral |
| RNF-AVL-003 | RTO | ≤4 h | SU | Ensayo de DR |
| RNF-AVL-004 | Backups cifrados con restauración ensayada | Trimestral | DC (Charter: un backup no probado no existe) | Acta de ensayo |

### 9.3 Sincronización y offline (RNF-SYNC) — DC por offline-first

| ID | Requisito | Valor | Medición |
|---|---|---|---|
| RNF-SYNC-001 | Éxito de sincronización diaria por dispositivo | >99.9% | Métrica de sync (consola) |
| RNF-SYNC-002 | Convergencia con red estable | <60 s p95 | Telemetría |
| RNF-SYNC-003 | Trabajo offline continuo sin pérdida | ≥7 días / 200 operaciones | Test CI de chaos |
| RNF-SYNC-004 | Pérdida de datos de usuario | 0 (nunca aceptable; se diseña para prevenir y, si ocurre, postmortem obligatorio) | Incidentes |
| RNF-SYNC-005 | Conflictos críticos resueltos por humano | 100% (prohibido LWW silencioso) | Cola de conflictos |
| RNF-SYNC-006 | Lag de sync por dispositivo visible en consola | 100% de dispositivos | Observabilidad |

### 9.4 Seguridad (RNF-SEC)

| ID | Requisito | Valor | Fuente |
|---|---|---|---|
| RNF-SEC-001 | Cifrado en tránsito | TLS 1.3 | DC |
| RNF-SEC-002 | Cifrado en reposo | AES-256 (BD, backups, objetos) | DC |
| RNF-SEC-003 | Cifrado local móvil | SQLCipher + keystore/keychain | DC |
| RNF-SEC-004 | MFA | Obligatorio: admins tenant + plataforma; opcional resto | DC (ADR-012) |
| RNF-SEC-005 | Sesiones | Tokens corta vida + revocación por dispositivo | DC |
| RNF-SEC-006 | Tests de aislamiento multi-tenant en CI | 100% suites pasando; bloquean merge | DC (AUD-00 §5) |
| RNF-SEC-007 | SAST/SCA/secretos/DAST en pipeline | Bloqueo en críticas | DC |
| RNF-SEC-008 | Pentest externo | Antes de lanzamiento público y anual después | SU (costo en doc 60) |
| RNF-SEC-009 | Auditoría inmutable (hash-encadenada) | 100% eventos de seguridad y negocio | DC |

### 9.5 Privacidad (RNF-PRV)

| ID | Requisito | Valor | Fuente |
|---|---|---|---|
| RNF-PRV-001 | Minimización de datos | Solo lo necesario por función; revisión por módulo | DC (privacy by design) |
| RNF-PRV-002 | Exportación completa por tenant (datos + adjuntos) | Formatos abiertos, <30 días | DC ("salida digna") |
| RNF-PRV-003 | Eliminación por tenant verificable | Con certificado de borrado | DC |
| RNF-PRV-004 | Datos de tenant nunca entrenan modelos base | Opt-in aislado solo si se ofrece fine-tuning | DC (doc 33) |
| RNF-PRV-005 | Registro de subprocesadores | Público y actualizado | DC (doc 36/37) |

### 9.6 Accesibilidad (RNF-ACC)

| ID | Requisito | Valor | Fuente |
|---|---|---|---|
| RNF-ACC-001 | Estándar interno web/PWA | WCAG 2.2 **AA** (objetivo interno SU hasta N-8; no contractual) | AUD-00 §12 |
| RNF-ACC-002 | Móvil | VoiceOver/TalkBack, Dynamic Type, targets ≥44pt, contraste AA | DC diseño |
| RNF-ACC-003 | QA de accesibilidad en DoD | Checklist por feature + pruebas con lector de pantalla en flujos críticos | DC |
| RNF-ACC-004 | Errores y estados comprensibles | Sin códigos crípticos; acción sugerida | DC |

### 9.7 Usabilidad frontline (RNF-USE) — DC por usuario primario

| ID | Requisito | Valor | Fuente |
|---|---|---|---|
| RNF-USE-001 | Tarea frecuente del técnico | ≤3 toques | DC (doc 01) |
| RNF-USE-002 | Capacitación requerida para técnico | 0 (autoexplicativo) | DC |
| RNF-USE-003 | Uso con guantes / una mano | Targets y gestos compatibles | AUD-00 §12 |
| RNF-USE-004 | Estado del sistema siempre visible (sync, guardado, errores) | 100% de flujos | DC |
| RNF-USE-005 | Autosave | Toda captura >30 s de trabajo | DC |

### 9.8 Escalabilidad (RNF-SCL)

| ID | Requisito | Valor Etapa A | Fuente |
|---|---|---|---|
| RNF-SCL-001 | Dimensión de diseño Etapa A | 50 tenants / 5K usuarios / 500K OTs (SU) | DC AUD-00 §H (no pre-construir para millones) |
| RNF-SCL-002 | Camino de escala documentado | Réplicas→particiones→tenants dedicados→shard | DC (ADR-001) |
| RNF-SCL-003 | Noisy neighbor | Rate limit y cuotas por tenant desde Fase 1 | DC |

### 9.9 Móvil (RNF-MOB)

| ID | Requisito | Valor | Medición |
|---|---|---|---|
| RNF-MOB-001 | Crash-free sessions | >99.5% (SU) | Crash reporting |
| RNF-MOB-002 | ANR (Android) | <0.5% (SU) | Telemetría |
| RNF-MOB-003 | Consumo de batería | Sin drenaje anómalo: sync en segundo plano dentro del presupuesto del OS (DC: restricciones iOS/Android documentadas, AUD-00 §3) | Profiling por release |
| RNF-MOB-004 | Almacenamiento local | Bucket sincronizado con límite configurable; aviso al 80% | Telemetría |
| RNF-MOB-005 | Compatibilidad | 2 versiones mayores de OS hacia atrás (SU; ajustar a pilotos PD-3) | Matriz de dispositivos |

### 9.10 IA (RNF-AI) — DC por gobierno

| ID | Requisito | Valor |
|---|---|---|
| RNF-AI-001 | Toda respuesta IA de datos muestra fuente o se abstiene | 100% |
| RNF-AI-002 | Acciones de riesgo medio/alto con aprobación humana | 100% (arquitectónico) |
| RNF-AI-003 | Prohibiciones doc 33 implementadas como ausencia de permiso | Verificado por test |
| RNF-AI-004 | Costo de IA por tenant/mes visible y con límite | Consola (FinOps) |
| RNF-AI-005 | Degradación sin IA: núcleo CMMS 100% funcional | Test de caída del servicio IA |
| RNF-AI-006 | Latencia copiloto p95 | <5 s (SU) |
| RNF-AI-007 | Golden-set de evaluación por caso de uso | Antes de activar cada agente |

### 9.11 FinOps (RNF-FIN)

| ID | Requisito | Valor | Fuente |
|---|---|---|---|
| RNF-FIN-001 | Infra Etapa A | $150–500/mes (SU) | AUD-00 §15 |
| RNF-FIN-002 | Costo de IA | ≤30% del ingreso por tenant (línea roja) | DC (Charter criterio de fracaso) |
| RNF-FIN-003 | Costo de soporte | ≤8% del MRR | SU (doc 03 §11 bis) |
| RNF-FIN-004 | Costo por tenant activo | Métrica mensual en consola | DC (ADR-012 §3.7) |

### 9.12 Observabilidad (RNF-OBS)

| ID | Requisito | Valor |
|---|---|---|
| RNF-OBS-001 | Trazas con `tenant_id` como atributo | 100% de requests |
| RNF-OBS-002 | Métricas RED por endpoint y por tenant | Todas |
| RNF-OBS-003 | Logs estructurados con correlación | 100% |
| RNF-OBS-004 | Alertado por síntoma con runbook | SLOs de RNF-AVL/SYNC |
| RNF-OBS-005 | Status page | Antes del lanzamiento público (SU) |

### 9.13 Mantenibilidad y calidad de ingeniería (RNF-MNT)

| ID | Requisito | Valor |
|---|---|---|
| RNF-MNT-001 | Cobertura de pruebas del núcleo | ≥80% (SU; calidad > porcentaje) |
| RNF-MNT-002 | Migraciones expand/contract | 100%; prohibido destructivas en un paso |
| RNF-MNT-003 | Deprecación de API | Aviso 12 meses (DC ADR-009) |
| RNF-MNT-004 | Deuda técnica | 20% de capacidad por trimestre (SU) |
| RNF-MNT-005 | ADR para toda decisión irreversible | 100% |

## 10. Herencia por módulos (DC)
Las specs (doc 43) heredan TODOS estos RNF; solo pueden: (a) endurecer un valor declarándolo explícitamente, (b) declarar una excepción con justificación y aprobación del Fundador vía FEP/ADR. Ningún módulo puede relajar RNF-SEC, RNF-SYNC, RNF-PRV ni RNF-AI.

## 11. Métricas del catálogo
% RNF con método de medición implementado en observabilidad (objetivo 100% antes del lanzamiento) · RNF incumplidos con plan de corrección (100% de los detectados).

## 12. Criterios de aceptación del documento
1. Todo RNF con valor, fuente y medición. ✅ 2. Sin valores aspiracionales sin justificar. ✅ 3. Herencia y excepciones normadas. ✅

## 13. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador; calibración con primer trimestre de datos reales (v1.1).

## 14. Referencias cruzadas
Depende de: 09, 11, 14, 16, 17, ADR-011/012, AUD-00. Alimenta: 10, 20–33, 47, 49, 54, 55, 60, 61.

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). 60+ RNF en 13 áreas con valor/fuente/medición; SLOs relajados a realismo de Etapa A (AUD-00 §14); herencia normada |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
