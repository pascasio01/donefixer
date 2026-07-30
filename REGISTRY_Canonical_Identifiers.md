# Canonical Identifier Registry — DONEFIXER

| Campo | Valor |
|---|---|
| Documento | REGISTRY_Canonical_Identifiers |
| Versión | 1.0 |
| Estado | ✅ Creado por instrucción adicional 2 de la aprobación de la Auditoría Integral (2026-07-29) |
| Norma | **Este registro es la única fuente oficial de identificadores del proyecto.** Citar un identificador que no existe aquí es un error de integridad documental (verificable por el proceso de la instrucción adicional 3). Ninguna ola futura podrá aprobarse con referencias rotas. |
| Regla de altas | Un identificador nuevo nace en su documento canónico y se registra aquí en el mismo commit documental. Los IDs son inmutables: nunca se reutilizan ni renumeran; un retirado queda `DEPRECADO`, nunca eliminado. |

---

## 1. Convención de nombres de familia (tabla normativa anti-erratas)

Las familias RNF del catálogo oficial (Doc 12) son **exactamente estas** — no existe `SEG`, `USA`, `PER`, `OFF`, `SYN` ni `EVD`:

| Familia válida | Significado | Familia inválida frecuente (prohibida) → corrección |
|---|---|---|
| RNF-PERF | Rendimiento | `RNF-PER-*` → RNF-PERF-* |
| RNF-AVL | Disponibilidad y continuidad | — |
| RNF-SYNC | Sincronización y offline | `RNF-OFF-*` / `RNF-SYN-*` → RNF-SYNC-* |
| RNF-SEC | Seguridad | `RNF-SEG-*` → RNF-SEC-* |
| RNF-PRV | Privacidad | — |
| RNF-ACC | Accesibilidad | `RNF-USA-*` (accesibilidad) → RNF-ACC-* |
| RNF-USE | Usabilidad frontline | `RNF-USA-*` (usabilidad) → RNF-USE-* |
| RNF-SCL | Escalabilidad | — |
| RNF-MOB | Móvil | — |
| RNF-AI | IA | — |
| RNF-FIN | FinOps | — |
| RNF-OBS | Observabilidad | — |
| RNF-MNT | Mantenibilidad | — |

Familias RF válidas (Doc 11): `RF-ONB, RF-TEN, RF-USR, RF-REQ, RF-WO, RF-SYNC, RF-AST, RF-PM, RF-DISP, RF-INV, RF-PROC, RF-RPT, RF-NTF, RF-AUD, RF-PLT, RF-I18N`. **No existen** `RF-WEB` ni `RF-EVD` (evidencias = RF-WO-003/007; QR = RF-WO-006, RF-REQ-001).

---

## 2. RF — Requisitos Funcionales (canónico: Doc 11)

| ID | Nombre corto | Estado |
|---|---|---|
| RF-ONB-001…005 | Onboarding de tenant (importación, plantillas, asistencia) | DC/SU según Doc 11 |
| RF-TEN-001…003 | Gestión de tenant (configuración, catálogos, membresías) | DC |
| RF-USR-001…003 | Usuarios y accesos (invitación, membresías múltiples, desactivación) | DC |
| RF-REQ-001 | Intake por portal PWA y QR, gratuito e ilimitado, ≤60 s | DC |
| RF-REQ-002…005 | Ciclo de solicitud (triage, duplicados, conversión a OT, notificación al solicitante) | DC/SU |
| RF-WO-001 | Ciclo de vida OT según máquina de estados (Doc 14) | DC |
| RF-WO-002 | Ejecución offline completa (prueba literal J-2 modo avión) | DC |
| RF-WO-003 | Evidencias aditivas con hash, inmutables tras cierre | DC |
| RF-WO-004 | Códigos de falla (problema/causa/acción) al cerrar correctivas | DC |
| RF-WO-005 | Costos acumulados por OT (labor/repuestos/externo) | DC |
| RF-WO-006 | Escaneo QR del activo vincula/confirma la OT | SU |
| RF-WO-007 | Firma ligada a sesión autenticada + hash de evidencia | DC |
| RF-WO-008 | Voz→texto en notas de OT | SU |
| RF-SYNC-001…010 | Sincronización (idempotencia, outbox local, HLC, tombstones, veredictos, buckets, reanudación) — **no negociables** | DC |
| RF-AST-001 | Jerarquía recursiva sin ciclos con camino materializado | DC |
| RF-AST-002 | Desactivación (no borrado) con historial | DC |
| RF-AST-003 | Medidores con lecturas y triggers PM | DC |
| RF-AST-004 | Historial completo por activo | DC |
| RF-PM-001…003 | Planes PM (calendario/medidor, generación de OT, reprogramación) | DC |
| RF-DISP-001…003 | Disponibilidad y asignación (turnos, capacidad, asignación) | DC/SU |
| RF-INV-001…003 | Inventario (repuestos, stock por ubicación, movimientos delta) | DC |
| RF-PROC-001…004 | Compras (requisición, OC, recepción; portal de proveedor RF-PROC-004) | DC |
| RF-RPT-001…004 | Reportes (tableros, KPIs, exportación, programados) | DC |
| RF-NTF-001…003 | Notificaciones (preferencias, push/in-app/email, digest) | DC |
| RF-AUD-001…003 | Auditoría de tenant (eventos, consulta, exportación) | DC |
| RF-PLT-001…004 | Consola de plataforma (organizaciones, planes/entitlements, soporte, consumo) | DC |
| RF-I18N-001 | i18n nativa; cero strings hardcodeados; idiomas PD-4 | DC |

## 3. RNF — Requisitos No Funcionales (canónico: Doc 12)

| ID | Requisito | Valor | Estado |
|---|---|---|---|
| RNF-PERF-001 | Latencia API p95 (lecturas tenant-scoped) | <500 ms | SU calibrado |
| RNF-PERF-002 | Latencia local móvil (lecturas SQLite) | <100 ms p95 | DC |
| RNF-PERF-003 | Carga inicial web p95 (4G) | <3 s | SU |
| RNF-PERF-004 | Apertura de OT en app (datos locales) | <1 s | SU |
| RNF-PERF-005 | Consultas N+1 | 0 toleradas | DC |
| RNF-AVL-001 | Disponibilidad (objetivo interno, no contractual) | 99.5% mensual | DC |
| RNF-AVL-002 | RPO | ≤15 min | SU |
| RNF-AVL-003 | RTO | ≤4 h | SU |
| RNF-AVL-004 | Backups cifrados con restauración ensayada | Trimestral | DC |
| RNF-SYNC-001 | Éxito de sync diario por dispositivo | >99.9% | DC |
| RNF-SYNC-002 | Convergencia con red estable | <60 s p95 | DC |
| RNF-SYNC-003 | Trabajo offline continuo sin pérdida | ≥7 días / 200 operaciones | DC |
| RNF-SYNC-004 | Pérdida de datos de usuario | 0 (postmortem obligatorio) | DC |
| RNF-SYNC-005 | Conflictos críticos resueltos por humano | 100% (prohibido LWW silencioso) | DC |
| RNF-SYNC-006 | Lag de sync por dispositivo visible | 100% dispositivos | DC |
| RNF-SEC-001 | Cifrado en tránsito | TLS 1.3 | DC |
| RNF-SEC-002 | Cifrado en reposo | AES-256 | DC |
| RNF-SEC-003 | Cifrado local móvil | SQLCipher + keystore/keychain | DC |
| RNF-SEC-004 | MFA | Obligatorio admins tenant + plataforma | DC |
| RNF-SEC-005 | Sesiones | Tokens corta vida + revocación por dispositivo | DC |
| RNF-SEC-006 | Tests de aislamiento multi-tenant en CI | 100%, bloquean merge | DC |
| RNF-SEC-007 | SAST/SCA/secretos/DAST en pipeline | Bloqueo en críticas | DC |
| RNF-SEC-008 | Pentest externo | Pre-lanzamiento + anual | SU |
| RNF-SEC-009 | Auditoría inmutable (hash-encadenada) | 100% eventos | DC |
| RNF-PRV-001…005 | Minimización; exportación completa <30 días; eliminación verificable; datos nunca entrenan modelos base; registro de subprocesadores | ver Doc 12 | DC |
| RNF-ACC-001 | WCAG 2.2 AA interno web/PWA | objetivo interno (N-8 PD) | SU |
| RNF-ACC-002…004 | Móvil (TalkBack/VoiceOver, ≥44pt); QA accesibilidad en DoD; errores comprensibles | ver Doc 12 | DC |
| RNF-USE-001 | Tarea frecuente del técnico | ≤3 toques | DC |
| RNF-USE-002 | Capacitación requerida para técnico | 0 | DC |
| RNF-USE-003 | Uso con guantes / una mano | compatible | DC |
| RNF-USE-004 | Estado del sistema siempre visible | 100% flujos | DC |
| RNF-USE-005 | Autosave | captura >30 s | DC |
| RNF-SCL-001 | Dimensión Etapa A | 50 tenants / 5K usuarios / 500K OTs | SU |
| RNF-SCL-002 | Camino de escala | réplicas→particiones→dedicados→shard | DC |
| RNF-SCL-003 | Noisy neighbor | rate limit + cuotas por tenant desde F1 | DC |
| RNF-MOB-001…005 | Crash-free >99.5% (SU); ANR <0.5% (SU); batería dentro de presupuesto OS; almacenamiento local con aviso al 80%; compatibilidad 2 OS atrás (SU) | ver Doc 12 | DC/SU |
| RNF-AI-001 | Respuestas IA citan fuente o se abstienen | 100% | DC |
| RNF-AI-002 | Riesgo medio/alto con aprobación humana | 100% (arquitectónico) | DC |
| RNF-AI-003 | Prohibiciones IA como ausencia de permiso | test verificado | DC |
| RNF-AI-004 | Costo IA por tenant/mes visible con límite | consola | DC |
| RNF-AI-005 | Núcleo CMMS 100% funcional sin IA | test de caída | DC |
| RNF-AI-006 | Latencia copiloto p95 | <5 s | SU |
| RNF-AI-007 | Golden-set por caso de uso | antes de activar | DC |
| RNF-FIN-001 | Infra Etapa A | $150–500/mes | SU |
| RNF-FIN-002 | Costo IA ≤30% del ingreso por tenant | línea roja | DC |
| RNF-FIN-003 | Costo soporte | ≤8% MRR | SU |
| RNF-FIN-004 | Costo por tenant activo | métrica mensual | DC |
| RNF-OBS-001 | Trazas con `tenant_id` | 100% requests | DC |
| RNF-OBS-002 | Métricas RED por endpoint y tenant | todas | DC |
| RNF-OBS-003 | Logs estructurados con correlación | 100% | DC |
| RNF-OBS-004 | Alertado por síntoma con runbook | SLOs AVL/SYNC | DC |
| RNF-OBS-005 | Status page | pre-lanzamiento | SU |
| RNF-MNT-001 | Cobertura núcleo ≥80% (SU) | calidad > % | SU |
| RNF-MNT-002 | Migraciones expand/contract | 100% | DC |
| RNF-MNT-003 | Deprecación API | aviso 12 meses | DC |
| RNF-MNT-004 | Deuda técnica | 20% capacidad/trimestre | SU |
| RNF-MNT-005 | ADR para toda decisión irreversible | 100% | DC |

## 4. ADR (canónicos: ADI + ADR-001-010_Registro)

| ID | Estado | Documento |
|---|---|---|
| ADR-001…010 | DC (ADR-002 revertido; detalle en registro) | `ADR-001-010_Registro.md` |
| ADR-011 | ✅ DC v1.1 | `ADR-011_Estrategia_Multicanal.md` |
| ADR-012 | ✅ DC v1.1 | `ADR-012_Platform_Administration_Console.md` |

## 5. Familias de la Ola 3 (rangos canónicos)

| Familia | IDs válidos | Canónico |
|---|---|---|
| MT | MT-1…MT-12 | Doc 26 |
| SY | SY-1…SY-15 | Doc 27 |
| EV | EV-1…EV-7 | Doc 30 |
| AP | AP-1…AP-12 | Doc 29 |
| IN | IN-1…IN-7 | Doc 28 |
| SE | SE-1…SE-6 | Doc 31 |
| EA | EA-1…EA-8 | Doc 20 |
| WA | WA-1…WA-10 | Doc 22 |
| MA | MA-1…MA-10 | Doc 23 |
| AIA | AIA-1…AIA-9 | Doc 32 |
| GA | GA-1…GA-7 | Doc 33 |
| P-33 (prohibiciones IA) | P-33-1…P-33-7 | Doc 33 §4 (única lista canónica) |

## 6. Otros identificadores oficiales

| Familia | IDs | Canónico |
|---|---|---|
| C (restricciones SRS) | C-1…C-12 | Doc 10 |
| P (personas) | P-T1, P-S1, P-M1, P-D1, P-R1, P-V1, P-A1, P-X1, P-C1, P-F1, P-U1 | Doc 15 |
| J (journeys) | J-1…J-9 | Doc 16 |
| SB (blueprints) | SB-1…SB-3 | Doc 17 |
| IA-* (casos de uso IA) | IA-1…IA-10 | Doc 32 |
| N (decisiones del Fundador) | N-1…N-10 | DECISIONES_N1-N10 |
| PD / SU | PD-2, PD-3, PD-4, PD-RETENCIÓN, SU-FLAGS, PD-IA-1, PD-CLOUD | ADI §5 |
| DC-00 | Nombre oficial DONEFIXER | Doc 00 |
| AO (acciones de auditoría) | AO-1…AO-6 | AUDITORIA_INTEGRAL_ARQUITECTURA_2026-07 |

---

*Registro de cambios — v1.0 (2026-07-29): creación por instrucción adicional 2 de la aprobación de la Auditoría Integral de Arquitectura. Fuente única oficial de identificadores.*
