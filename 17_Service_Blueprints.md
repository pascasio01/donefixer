# DONEFIXER — 17 · Service Blueprints

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Evidencia:** SU (blueprints de diseño, no observados aún en campo) salvo elementos DC citados.

---

## 1. Objetivo
Extender los journeys (doc 16) a la vista completa del servicio: qué ve el usuario (frontstage), qué hace el sistema (backstage), qué procesos de soporte y gobierno lo sostienen, y dónde están los puntos de fallo críticos. Los blueprints son la fuente de requisitos no funcionales (doc 12) y de pruebas E2E (doc 47).

## 2. Alcance
Los 3 servicios más críticos de Fase 1: **SB-1** Servicio de solicitud→resolución (J-1+J-4+J-2), **SB-2** Sincronización offline como servicio (J-2 backstage), **SB-3** Onboarding de cliente (J-7). El resto se blueprintea en specs de módulo (doc 43).

## 3. Exclusiones
No incluye blueprints de soporte interno de plataforma (ADR-012 tiene su propio flujo documentado), ni de Fase 3+.

## 4. Decisiones confirmadas (DC)
Autoridad backend con re-validación en sync (ADR-011 v1.1); IA con aprobación humana por nivel de riesgo (doc 33/AUD-00 §11); notificaciones multicanal con estado visible (doc 48); soporte asistido con consentimiento y notificación al tenant (ADR-012 §3.3).

## 5. Decisiones pendientes (PD)
N-2 (modalidad PowerSync) afecta el backstage de SB-2; N-9 afecta la línea de soporte de SB-3.

## 6. Supuestos (SU)
Tiempos objetivo por etapa son hipótesis; la existencia de canales (WhatsApp Business API) tiene costo por conversación (H-25, a FinOps doc 60).

## 7. Dependencias
Docs 15, 16, ADR-011/012. Alimenta: 12 (RNF), 21/30 (arquitectura de eventos), 47 (pruebas), 48 (notificaciones), 55 (SRE).

## 8. Riesgos
| Riesgo | Mitigación |
|---|---|
| Diseñar el backstage ideal sin validar con restricciones reales (redes, dispositivos) | Pruebas de chaos y de campo en pilotos (doc 47) |
| Puntos de fallo invisibles para el usuario | Cada blueprint declara su "modo degradado" explícito |

---

## 9. SB-1 · Servicio Solicitud → Resolución (SU)

### Líneas del blueprint

| Etapa | 1. Reporte | 2. Triage | 3. Planificación | 4. Ejecución | 5. Cierre y aprendizaje |
|---|---|---|---|---|---|
| **Evidencia física** | WhatsApp/portal/QR + folio | Bandeja triada | Calendario | App técnico | Notificación al solicitante; KPI actualizado |
| **Acciones del usuario (frontstage)** | Describe con voz/foto/texto | Supervisor confirma/corrige | Asigna (o acepta sugerencia) | Ejecuta, evidencia, cierra provisional | Solicitante consulta estado |
| **Contacto (sistema visible)** | Confirmación inmediata + folio | Estados visibles | Push al técnico | Estado "pendiente de sync" | "Resuelto" con resumen |
| **Backstage (sistema)** | Normalización del canal; conservación del original (DC i18n) | Triage IA (prioridad/activo/duplicados, riesgo medio→humano confirma, DC) | Sugerencia por habilidad/proximidad/carga | Lógica local provisional; outbox durable | Re-validación servidor; evento `wo.closed` |
| **Procesos de soporte** | Costo Meta por conversación (SU) | Golden-set del triage (doc 33) | Reglas de balanceo | Sync engine; resolución humana de conflictos | Cálculo KPI (rollups, ADR-006); aprendizaje de códigos de falla |
| **Gobierno** | Prohibido IA sin fuente (DC) | Registro de correcciones al triage | Auditoría de asignaciones automáticas | Registro inmutable de evidencias (hash) | Auditoría por decisión IA (DC) |

### Puntos de fallo y modo degradado (DC metodológica: prevenir/detectar/contener/recuperar/aprender)

| Punto de fallo | Detección | Modo degradado | Recuperación |
|---|---|---|---|
| WhatsApp API caída | Monitor de webhook | Portal/PWA y QR siguen abiertos; mensaje al solicitante | Cola de reintentos; reconciliación al volver |
| Triage IA no disponible | Health check del servicio IA | Solicitudes entran sin triage con etiqueta "sin clasificar"; prioridad por defecto conservadora | Re-triage diferido cuando vuelve (marca "retroactivo") |
| Sin señal en campo | (estado normal, no fallo) | Todo local (J-2 paso 3) | Sync al recuperar red |
| Conflicto de sync en cierre | Re-validación servidor | OT queda "en revisión", no se pierde | Cola de resolución humana con ambos estados |
| Notificación no entregada | Log de entregas | Estado consultable on-demand | Reenvío por canal alterno |

### Métricas del servicio (SLIs semilla para doc 54/55)
Tiempo reporte→folio (<10 s p95); tiempo solicitud→asignación; MTTR end-to-end; % conflictos de sync por 1,000 OTs; % notificaciones entregadas; costo por solicitud (WhatsApp+IA, FinOps).

## 10. SB-2 · La sincronización como servicio (SU — el blueprint más importante del producto)

| Etapa | Escritura local | Outbox | Push | Re-validación servidor | Pull y convergencia |
|---|---|---|---|---|---|
| **Usuario ve** | Respuesta instantánea | "Pendiente de sync" (visible, AUD-00 §12) | Indicador de progreso | Confirmado/ajustado/rechazado | Datos actualizados |
| **Cliente hace** | SQLite + outbox en **una transacción** (DC) | Cola durable con `operation_id` | Lotes idempotentes con backoff+jitter | — | Aplica deltas; resuelve tombstones ("borrados ganan", DC) |
| **Servidor hace** | — | — | Autentica dispositivo; deduplica por operation_id | **Re-valida: estado, permisos, stock, SLA, versión (If-Match)** (DC ADR-011 v1.1) | Sirve deltas por cursor; expira tombstones según retención (PD-RETENCIÓN) |
| **Soporte/gobierno** | Cifrado local SQLCipher | Métricas: tamaño de outbox, edad del más viejo | Rate limit por dispositivo | Registro inmutable de rechazos | Métrica: lag de sync por dispositivo |
| **Fallo y degradado** | Disco lleno → aviso y protección de outbox | App muerta → reanuda al abrir | Red hostil → comprime, prioriza metadatos>fotos>video | Rechazo → cola humana, nunca descarte silencioso | Buckets: fallo de uno no bloquea otros |

**Casos de borde obligatorios (a pruebas, doc 47):** dispositivo compartido con cambio de usuario (wipe entre usuarios, DC AUD-00 §4); revocación de sesión con outbox lleno (se descarta outbox del usuario revocado + wipe); reloj del dispositivo mal configurado (HLC + timestamp servidor); subida de foto interrumpida al 90% (reanudación por offset, deduplicación por hash); 7 días offline con 200 operaciones (convergencia completa, sin pérdidas).

## 11. SB-3 · Onboarding de cliente (SU)

| Etapa | Registro e importación | Configuración | Invitación | Primer valor |
|---|---|---|---|---|
| **Usuario hace** | Sube Excel/CSV; revisa mapeo | Elige plantilla por industria | Invita técnicos (SMS/WhatsApp/email) | Crea/aprobar primera OT real |
| **Sistema hace** | Validación por fila con errores descargables | Aplica plantilla: catálogos, códigos de falla, checklists | App con onboarding de 3 pantallas | Guía contextual solo si el usuario no avanza |
| **Soporte** | Plantillas por industria mantenidas por DONEFIXER | Catálogos base por idioma | FAQ | Métrica "tiempo al primer valor" por cohorte |
| **Fallo y degradado** | Excel corrupto → reporte de errores, nunca importación parcial silenciosa | Plantilla no aplica → mínimo viable editable | Invitación perdida → reenvío | Sin OT en 7 días → alerta a éxito de cliente (N-9) |

## 12. Criterios de aceptación de este documento
1. Cada blueprint con 5+ líneas (evidencia, frontstage, backstage, soporte, gobierno) y puntos de fallo con modo degradado. ✅
2. Casos de borde de sync explícitos y asignados a pruebas. ✅
3. Todo clasificado DC/SU/PD. ✅

## 13. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador.

## 14. Referencias cruzadas
Depende de: 15, 16, ADR-011/012, AUD-00. Alimenta: 12, 21, 30, 47, 48, 54, 55.

## 15. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). SB-1 solicitud→resolución, SB-2 sync como servicio con casos de borde, SB-3 onboarding; puntos de fallo con modo degradado |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
