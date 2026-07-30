# DONEFIXER — 11 · Functional Requirements (Catálogo Global RF)

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Convención:** `RF-<MODULO>-###` · Prioridad MoSCoM · Fase · Trazabilidad a journey (doc 16) y dominio (doc 14) · Criterio de aceptación verificable. DC = derivado de decisión aprobada · SU = hipótesis a validar.
> **Nota de alcance:** este es el catálogo **global núcleo** (Fases 0–2). Las specs de módulo (doc 43) lo extienden con RF específicos por módulo; ningún RF entra sin FEP (doc 02 §10 bis).

---

## 1. Objetivo
Catálogo único y trazable de requisitos funcionales núcleo. Todo RF tiene ID estable, criterio de aceptación y trazabilidad; los IDs **nunca se reutilizan** (un RF retirado queda marcado "retirado + motivo").

## 2. Alcance
Requisitos de Fase 0–2 (núcleo + inventario/compras) con semillas de Fase 3 marcadas. Fases 4–5 se detallan al acercarse.

## 3. Exclusiones
RNF (doc 12); detalle de implementación (specs doc 43); requisitos de consola interna más allá de los esenciales (ADR-012 los define).

## 4. Decisiones confirmadas (DC) que gobiernan estos RF
ADR-011 v1.1 (autoridad backend, lógica local provisional) · ADR-012 (consola, auditoría 10 campos) · doc 14 (máquina de estados, invariantes) · doc 19 (permisos/transiciones) · doc 33 (prohibiciones IA) · doc 03 (solicitantes gratis) · doc 01 §12 bis (exclusiones).

## 5. Decisiones pendientes (PD)
PD-3 (variantes regionales, canales) · PD-4 (idiomas lanzamiento) · N-2 (modalidad sync) · N-4 (billing) · N-8 (nivel accesibilidad contractual).

## 6. Supuestos (SU)
Los umbrales numéricos son hipótesis HV; WhatsApp como canal sujeto a FinOps (H-25).

## 7. Dependencias
Docs 09, 13, 14, 15, 16, 17, 19. Alimenta: 10 (SRS), 43 (specs), 47 (pruebas), 12 (RNF emparejados).

## 8. Riesgos
| Riesgo | Mitigación |
|---|---|
| Inflación de RF sin prioridad | MoSCoM obligatorio + FEP |
| Criterios de aceptación no verificables | Todo criterio es binario y medible; QA lo revisa (doc 47) |

---

## 9. Catálogo RF núcleo

### Módulo: Autenticación y Onboarding (RF-ONB)

| ID | Requisito | Prioridad | Fase | Traz. | Criterio de aceptación | Evidencia |
|---|---|---|---|---|---|---|
| RF-ONB-001 | El sistema permite crear una organización (tenant) con su primer administrador | M | 1 | J-7 | Tenant operativo en <10 min sin soporte | DC |
| RF-ONB-002 | Importación de activos/usuarios/sitios desde Excel/CSV con mapeo asistido y reporte de errores por fila descargable | M | 1 | J-7 | Importación de 500 filas con errores claros; nunca importación parcial silenciosa (DC SB-3) | DC |
| RF-ONB-003 | Plantillas por industria (catálogos, códigos de falla, checklists) aplicables en onboarding | M | 1 | J-7 | Una plantilla aplicada crea catálogo funcional sin configuración extra | SU |
| RF-ONB-004 | Onboarding de técnico en app en ≤3 pantallas | M | 1 | J-7 | Técnico invitado llega a su primera OT asignada en <10 min | SU |
| RF-ONB-005 | Autenticación con MFA opcional (obligatorio para Tenant Admin y plataforma) | M | 1 | — | MFA exigible por política del tenant | DC (ADR-012 §3.9) |

### Módulo: Organizaciones y Tenancy (RF-TEN)

| ID | Requisito | Prioridad | Fase | Traz. | Criterio | Evidencia |
|---|---|---|---|---|---|---|
| RF-TEN-001 | Estructura Tenant→(Empresa)→Sitio→Edificio/Zona→Unidad según glosario (doc 13) | M | 1 | — | Jerarquía configurable sin código | DC |
| RF-TEN-002 | Aislamiento: ningún usuario accede a datos de otro tenant | M | 1 | — | Tests automatizados de aislamiento en CI fallan ante intento cruzado (DC AUD-00 §5) | DC |
| RF-TEN-003 | Catálogos con doble ámbito: semilla de plataforma + sobre-escritura por tenant | S | 1 | — | Un código de falla del tenant convive con los de plataforma | DC |

### Módulo: Usuarios y Permisos (RF-USR)

| ID | Requisito | Prioridad | Fase | Traz. | Criterio | Evidencia |
|---|---|---|---|---|---|---|
| RF-USR-001 | Cuenta global → membresías → perfiles contextuales (doc 19 §4.1) | M | 1 | — | Un usuario opera en 2 tenants con contextos separados y auditoría por contexto | DC |
| RF-USR-002 | Experiencia dinámica por permisos efectivos (una app) | M | 1 | — | Dos roles distintos ven navegación/acciones distintas sin apps separadas | DC (ADR-011) |
| RF-USR-003 | "Ver como" (simulador de permisos) para Tenant Admin | S | 2 | — | El admin previsualiza la experiencia de cualquier rol | SU |

### Módulo: Solicitudes (RF-REQ)

| ID | Requisito | Prioridad | Fase | Traz. | Criterio | Evidencia |
|---|---|---|---|---|---|---|
| RF-REQ-001 | Intake por portal PWA y QR sin cuenta compleja, gratuito e ilimitado | M | 1 | J-1 | Solicitud creada en ≤60 s (mediana) | DC (doc 03) |
| RF-REQ-002 | Intake por WhatsApp con conservación del mensaje original | S | 1 | J-1 | Original visible junto a traducción/normalización (DC i18n) | SU (H-25 FinOps) |
| RF-REQ-003 | Entrada por voz y foto con voz→texto | M | 1 | J-1 | Solicitud creada sin teclado | SU |
| RF-REQ-004 | Triage IA (prioridad, activo sugerido, duplicados) con confirmación humana | S | 1 | J-1/J-4 | Ninguna SR se convierte en OT sin confirmación humana (DC doc 33) | DC |
| RF-REQ-005 | Notificación de estado al solicitante en cada cambio | M | 1 | J-1 | Solicitante informado sin llamar (≥90% de SRs, HV) | DC |

### Módulo: Órdenes de Trabajo (RF-WO)

| ID | Requisito | Prioridad | Fase | Traz. | Criterio | Evidencia |
|---|---|---|---|---|---|---|
| RF-WO-001 | Máquina de estados completa del doc 14 §7.2 con matriz de transiciones por rol (doc 19 §9.3) | M | 1 | J-2/J-4 | Transición inválida rechazada por servidor aunque el cliente la permita (DC ADR-011 v1.1) | DC |
| RF-WO-002 | Ejecución offline completa: consulta, checklist, evidencias, repuestos, tiempos, cierre provisional | M | 1 | J-2 | **Prueba literal: pasos 1–4 de J-2 en modo avión** | DC |
| RF-WO-003 | Evidencias aditivas con hash, inmutables tras cierre | M | 1 | J-2 | Ninguna evidencia puede editarse/borrarse tras cierre de OT | DC |
| RF-WO-004 | Códigos de falla (problema/causa/acción) obligatorios al cerrar correctivas | M | 1 | J-2 | OT correctiva no cierra sin los tres códigos (si el tenant lo exige) | DC |
| RF-WO-005 | Costos acumulados por OT (labor/repuestos/externo) | M | 2 | J-5/J-8 | TCO por activo calculable desde OTs | DC |
| RF-WO-006 | Escaneo QR del activo vincula/confirma la OT | M | 1 | J-2 | QR incorrecto bloquea apertura con mensaje claro | SU |
| RF-WO-007 | Firma capturada ligada a sesión autenticada + hash de evidencia | M | 1 | J-2 | Firma verificable contra evidencia y sesión | DC (AUD-00 §10) |
| RF-WO-008 | Voz→texto en notas de OT | S | 1 | J-2 | Nota dictada sin teclado en campo | SU |

### Módulo: Sincronización (RF-SYNC) — DC en su totalidad por offline-first

| ID | Requisito | Prioridad | Fase | Traz. | Criterio | Evidencia |
|---|---|---|---|---|---|---|
| RF-SYNC-001 | Outbox local durable en la misma transacción que el dato | M | 1 | J-2/SB-2 | Sin pérdida ante cierre abrupto de la app (test de chaos) | DC |
| RF-SYNC-002 | Operaciones idempotentes con `operation_id`; deduplicación servidor | M | 1 | SB-2 | Reintentos de red nunca duplican efectos | DC |
| RF-SYNC-003 | Re-validación servidor de toda mutación (estado, permisos, stock, versión If-Match) | M | 1 | SB-2 | Mutación obsoleta detectada y resuelta según matriz de conflictos | DC (ADR-011 v1.1) |
| RF-SYNC-004 | Resolución de conflictos por matriz (doc 14 §8); cola humana para críticos; **prohibido LWW silencioso en campos críticos** | M | 1 | SB-2 | Conflicto en estado OT llega a cola de supervisor con ambos valores | DC |
| RF-SYNC-005 | Estado de sincronización siempre visible (pendiente/confirmado/ajustado/rechazado) | M | 1 | J-2 | El técnico distingue cierre provisional de confirmado | DC (AUD-00 §12) |
| RF-SYNC-006 | Sync por buckets (perfil del dispositivo), delta, reintentos con backoff | M | 1 | SB-2 | Técnico no descarga el tenant completo; fallo de un bucket no bloquea otros | DC |
| RF-SYNC-007 | Archivos por canal separado: subida reanudable, hash, prioridad metadatos>fotos>video | M | 1 | SB-2 | Subida interrumpida al 90% reanuda sin duplicar | DC |
| RF-SYNC-008 | Dispositivo compartido: cambio de usuario con wipe local; revocación con borrado remoto | M | 1 | SB-2 | Datos del usuario A inaccesibles para usuario B en el mismo dispositivo | DC |
| RF-SYNC-009 | Cifrado local (SQLCipher) con desbloqueo biométrico opcional | M | 1 | SB-2 | SQLite ilegible sin credenciales | DC |
| RF-SYNC-010 | Convergencia tras 7 días offline con 200 operaciones sin pérdida | M | 1 | SB-2 | Test de escenario en CI (doc 47) | DC |

### Módulo: Activos (RF-AST)

| ID | Requisito | Prioridad | Fase | Criterio | Evidencia |
|---|---|---|---|---|---|
| RF-AST-001 | Jerarquía recursiva sin ciclos con camino materializado | M | 1 | Intento de ciclo rechazado por servidor | DC |
| RF-AST-002 | Desactivación (no borrado) de activos con historial | M | 1 | KPIs históricos intactos tras desactivar | DC |
| RF-AST-003 | Medidores por activo con lecturas y triggers PM | M | 1 | PM por medidor genera OT al cruzar umbral | DC |
| RF-AST-004 | Historial completo por activo (OTs, costos, downtime, fallas) | M | 1 | Vista de activo muestra TCO parcial desde Fase 2 | DC |

### Módulo: Mantenimiento Preventivo (RF-PM)

| ID | Requisito | Prioridad | Fase | Criterio | Evidencia |
|---|---|---|---|---|---|
| RF-PM-001 | Triggers por tiempo y medidor (condición/predicción = Fase 4) | M | 1 | OT generada automáticamente en ventana correcta | DC |
| RF-PM-002 | Deduplicación: sin OT duplicada del mismo plan/activo/ventana | M | 1 | 0 duplicados en test de generación masiva | DC |
| RF-PM-003 | PM compliance calculado (±10% del intervalo) | M | 1 | KPI disponible sin exportar a Excel | DC |

### Módulo: Planificación y Despacho (RF-DISP)

| ID | Requisito | Prioridad | Fase | Criterio | Evidencia |
|---|---|---|---|---|---|
| RF-DISP-001 | Calendario con carga por técnico y conflictos de disponibilidad/habilidad | M | 1 | Sobreasignación visible antes de confirmar | SU |
| RF-DISP-002 | Sugerencia IA de asignación (habilidad/proximidad/carga) con confirmación humana | S | 1 | El ajuste manual prevalece y se registra | DC (doc 33) |
| RF-DISP-003 | Reagendado masivo por filtros | S | 2 | 50 OTs reagendadas en una operación auditada | SU |

### Módulo: Inventario (RF-INV) — Fase 2

| ID | Requisito | Prioridad | Criterio | Evidencia |
|---|---|---|---|---|
| RF-INV-001 | Movimientos delta con costo y referencia (OT/PO/recepción); saldo derivado, prohibido `set` | M | Consumo concurrente offline de 2 técnicos converge sin lost-update | DC |
| RF-INV-002 | Punto de reorden con alerta/generación de necesidad | M | Cruce de umbral genera alerta/requisición | DC |
| RF-INV-003 | Exactitud físico vs. sistema ≥95% medible | M | Reporte de discrepancias por almacén | SU |

### Módulo: Compras y Facturas (RF-PROC) — Fase 2

| ID | Requisito | Prioridad | Criterio | Evidencia |
|---|---|---|---|---|
| RF-PROC-001 | Flujo Requisición→aprobación→OC→recepción→devolución con auditoría | M | Cada paso con actor y estado | DC |
| RF-PROC-002 | OCR de facturas + agente validador contra contrato/OC/recepción con **aprobación humana obligatoria y límites monetarios** | M | El agente marca, nunca aprueba (DC doc 33) | DC |
| RF-PROC-003 | Conciliación tres vías con tolerancias y cola de discrepancias | M | Discrepancia fuera de tolerancia va a humano | DC |
| RF-PROC-004 | Portal de proveedor: OTs asignadas, evidencia, facturas, estado de pago | M | Proveedor opera sin cuenta de empleado | DC |

### Módulo: Reportes y KPIs (RF-RPT)

| ID | Requisito | Prioridad | Fase | Criterio | Evidencia |
|---|---|---|---|---|---|
| RF-RPT-001 | MTTR/MTBF/PM compliance/backlog automáticos desde OTs cerradas | M | 1 | KPI recalculado sin intervención manual | DC |
| RF-RPT-002 | Dashboards por sitio con rollup multi-sitio | S | 2 | Comparación sitio a sitio en una vista | DC |
| RF-RPT-003 | Resumen mensual generado por IA con **fuentes citadas por cifra** | S | 3 | Cifra sin fuente = no publicada (DC doc 33) | DC |
| RF-RPT-004 | Exportación PDF/Excel y envío programado | S | 2 | Reporte programado llega sin intervención | SU |

### Módulo: Notificaciones (RF-NTF)

| ID | Requisito | Prioridad | Fase | Criterio | Evidencia |
|---|---|---|---|---|---|
| RF-NTF-001 | Push, email y estado al solicitante por su canal | M | 1 | Entrega registrada con log | DC |
| RF-NTF-002 | Escalación por SLA incumplido | M | 1 | SLA roto genera escalación según política | DC |
| RF-NTF-003 | Preferencias por usuario y silencio fuera de horario | S | 2 | Usuario controla sus notificaciones | SU |

### Módulo: Auditoría (RF-AUD) — DC

| ID | Requisito | Prioridad | Criterio |
|---|---|---|---|
| RF-AUD-001 | Log inmutable (append-only, hash-encadenado) de eventos de negocio y seguridad | M | Evento no editable ni borrable vía aplicación |
| RF-AUD-002 | Registro de decisiones de IA por decisión (actor, motivo, fuentes, resultado) | M | Toda acción de agente reconstruible |
| RF-AUD-003 | Exportación de auditoría por tenant | M | Auditor cliente exporta su log completo |

### Módulo: Plataforma — Consola (RF-PLT) — DC por ADR-012

| ID | Requisito | Prioridad | Criterio |
|---|---|---|---|
| RF-PLT-001 | Gestión de tenants, planes, entitlements, flags por tenant/segmento/% | M | Cambio de plan efectivo sin despliegue |
| RF-PLT-002 | Régimen de acciones críticas Fase 0–1 (MFA+reauth+motivo+registro+confirmación+rollback) | M | Acción crítica sin motivo = imposible |
| RF-PLT-003 | Soporte asistido con consentimiento y notificación al tenant | M | Acceso de soporte visible en la auditoría del tenant |
| RF-PLT-004 | Consumo por tenant (storage, sync, tokens IA, mensajes) visible | M | Costo unitario consultable (FinOps) |

### Módulo: i18n (RF-I18N)

| ID | Requisito | Prioridad | Criterio | Evidencia |
|---|---|---|---|---|
| RF-I18N-001 | UI en ES+EN (alcance PD-4) con i18n nativa; cero strings hardcodeados | M | Cambio de idioma sin redeploy | DC (ADR-010) |
| RF-I18N-002 | Zonas horarias por sitio; fechas/monedas/unidades localizadas | M | OT muestra hora del sitio, no del servidor | DC |
| RF-I18N-003 | Traducción de chat/notas conservando original visible | S | Original siempre accesible | DC |

### Semillas Fase 3 (resumen — RF completos en specs)
Chat contextual (RF-CHAT-*) · OCR avanzado (RF-OCR-*) · Computer Vision básica (RF-CV-*) · Automatización visual (RF-AUTO-*) · Búsqueda global + RAG (RF-SRCH-*) · Billing SaaS operativo (RF-BILL-*, depende N-4).

## 10. Reglas del catálogo (DC)
1. ID inmutable; retiros marcados con motivo. 2. Todo RF nuevo pasa FEP. 3. Todo RF enlaza journey + dominio. 4. Criterio de aceptación binario y medible. 5. Los RF-SYNC son innegociables: ningún módulo de campo se aprueba sin responder "¿cómo sincroniza offline?" (ADR-002-reabierto).

## 11. Métricas del catálogo
Cobertura journey→RF = 100% (gate G2) · % RF con criterio verificable = 100% · RF retirados con motivo = 100%.

## 12. Criterios de aceptación del documento
1. IDs estables por familia con criterios binarios. ✅ 2. Trazabilidad completa. ✅ 3. RF-SYNC completos según AUD-00 §4. ✅

## 13. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador; extensión Fase 3 en specs (doc 43).

## 14. Referencias cruzadas
Depende de: 09, 13, 14, 15, 16, 17, 19, ADR-011/012, AUD-00. Alimenta: 10 (SRS), 12, 43, 47.

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). 60+ RF núcleo en 16 familias con criterios binarios; RF-SYNC innegociables; reglas del catálogo |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
