# DONEFIXER — 09 · Product Requirements Document (PRD)

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Evidencia:** DC para requisitos derivados de decisiones aprobadas (Ola 1, ADR-011/012, AUD-00); SU para prioridades y metas a validar en pilotos; PD donde falta decisión del Fundador.

---

## 1. Objetivo
Traducir la estrategia aprobada (docs 01–04) en el conjunto de capacidades de producto que DONEFIXER entregará, por fase, con prioridades, métricas y criterios de aceptación. Es el puente obligatorio entre la visión y los requisitos formales (docs 11/12/10).

## 2. Alcance
Fases 0–2 en detalle (núcleo operacional + inventario/compras/proveedores); Fases 3–5 en resumen (el detalle se genera al acercarse cada fase, regla anti-predicción-prematura).

## 3. Exclusiones
No detalla diseño técnico (docs 20–33), ni specs completas de módulo (doc 43), ni diseño visual (docs 39–41).

## 4. Decisiones confirmadas (DC) que gobiernan este PRD
Usuario primario = técnico (doc 01/15) · offline-first ciclo completo · multicanal con paridad controlada y autoridad backend (ADR-011 v1.1) · separación de planos (ADR-012) · IA gobernada con prohibiciones arquitectónicas (doc 33) · exclusiones de producto (doc 01 §12 bis) · FEP para toda incorporación futura (doc 02 §10 bis) · solicitantes gratuitos e ilimitados (doc 03).

## 5. Decisiones pendientes (PD) que condicionan requisitos
| PD | Requisitos condicionados |
|---|---|
| PD-3 países | RF de regionalización (variantes, WhatsApp vs. SMS por costo) |
| PD-4 idiomas | RF de i18n por lanzamiento (ES+EN base SU) |
| N-1 framework móvil | Ninguno funcional (ADR-011 es agnóstica); afecta solo ejecución |
| N-2 PowerSync modalidad | RF de sync: afecta operación, no el contrato |
| N-4 pagos | RF de billing SaaS |
| N-8 accesibilidad | RNF de accesibilidad (objetivo AA interno SU) |

## 6. Supuestos (SU)
Las metas numéricas (adopción, tiempos) son hipótesis HV (doc 03 §16); el alcance de Fase 2 depende de los criterios de salida de Fase 1 (doc 69).

## 7. Dependencias
Docs 01–04 (aprobados), 15/16/17 (personas, journeys, blueprints), 13/14/19 (glosario, dominio, roles), ADR-011/012. Alimenta: 11 (RF), 12 (RNF), 10 (SRS), 43 (specs), 69 (roadmap).

## 8. Riesgos del PRD
| Riesgo | Mitigación |
|---|---|
| PRD leído como compromiso de fechas | Sin fechas en requisitos; las fechas viven solo en el roadmap (doc 69) |
| Alcance inflado por peticiones de pilotos | FEP obligatorio (doc 02 §10 bis) |
| Requisitos sin trazabilidad | Todo RF enlaza a journey y a este PRD (gate G2) |

---

## 9. Capacidades por fase (prioridad MoSCoW: **M**ust / **S**hould / **C**ould / **W**on't-esta-fase)

### 9.1 Fase 0 — Fundamentos (sin código de producción)

| Capacidad | Prioridad | Journey | Notas |
|---|---|---|---|
| Documentación Ola 2–4 completa | M | — | Gates M1–M8 |
| Prototipo de sync (PowerSync, no producción) | M | J-2 | Prueba: conflicto OT, evidencia offline, wipe, dispositivo compartido (gate M2) |
| Validación de personas/journeys con 5–10 técnicos reales | M | Todos | SU→DC |

### 9.2 Fase 1 — Núcleo operacional production-grade

| Capacidad | Prioridad | Journey | Persona principal |
|---|---|---|---|
| Autenticación + onboarding de tenant (importación Excel/CSV) | M | J-7 | P-C1 |
| Organizaciones, sitios, ubicaciones (tenant→sitio→zona) | M | J-7 | P-C1 |
| Usuarios, membresías, roles semilla, permisos contextuales | M | — | P-C1 |
| Solicitudes omnicanal (portal PWA + QR; WhatsApp si FinOps lo aprueba — SU H-25) | M | J-1 | P-R1 |
| Triage IA de solicitudes (riesgo medio: humano confirma) | S | J-1/J-4 | P-S1 |
| OTs completas con máquina de estados, evidencias (foto/voz/firma), códigos de falla | M | J-2 | P-T1 |
| **App móvil offline ciclo completo con sync (PowerSync)** | M | J-2 | P-T1 |
| Activos con jerarquía, QR, historial | M | J-2 | P-T1 |
| PM por tiempo y por medidor, generación automática sin duplicados | M | J-3 | P-S1 |
| Procedimientos y checklists con evidencias requeridas | M | J-2/J-3 | P-T1 |
| Calendario y despacho básico (asignación manual + sugerencia IA con confirmación) | M | J-3/J-4 | P-D1/S1 |
| Notificaciones (push, email; estado de solicitud al solicitante) | M | J-1/J-4 | P-R1/T1 |
| KPIs automáticos básicos (MTTR, MTBF, PM compliance, backlog) con rollups | M | J-8 | P-M1 |
| Auditoría inmutable de eventos de negocio | M | — | P-U1 |
| Consola de plataforma (régimen Fase 0–1, ADR-012 §3.9) | M | — | Platform |
| Portal de solicitante (consulta de estado, sin cuenta compleja) | M | J-1 | P-R1 |
| Copiloto IA v1: creación de OT por voz/foto, resúmenes, consultas NL con fuentes y cuotas | S | J-2/J-8 | P-T1/M1 |
| i18n ES+EN (SU hasta PD-4) | M | — | Todas |
| Portal de proveedor | C (F2 si no cabe) | J-6 | P-V1 |
| Importación desde competidores (más allá de CSV genérico) | C | J-7 | P-C1 |

**Won't (Fase 1):** inventario financiero completo, compras, IoT, agentes autónomos, SSO/SCIM, multi-región, verticales (coherente con doc 01 §13).

### 9.3 Fase 2 — Inventario, compras y proveedores

| Capacidad | Prioridad | Journey |
|---|---|---|
| Inventario: ítems, almacenes, movimientos delta, punto de reorden | M | J-5 |
| Requisiciones → OC → recepción/devoluciones | M | J-5 |
| Facturas AP con OCR + agente validador (aprobación humana, límites monetarios) | M | J-6 |
| Conciliación tres vías | M | J-6 |
| Contratos y garantías | M | J-5/J-6 |
| Portal de proveedor completo (OTs, evidencias, facturas, estado) | M | J-6 |
| Costos laborales con tarifas por rol | S | J-2 |
| Chat contextual por OT/activo | S | — |
| Billing SaaS y entitlements operativos (depende N-4) | M | — |

### 9.4 Fases 3–5 (resumen — detalle al acercarse)

- **F3:** chat + traducción automática (original conservado), voz/transcripción, OCR avanzado, copiloto completo ES/EN/PT/FR/HT (según PD-4), Computer Vision básica (Asset Snap-like).
- **F4:** OLAP dedicado, dashboards ejecutivos, automatización visual, conectores ERP, API pública completa, anomalías ML, IoT/MQTT.
- **F5:** SSO/SCIM, multi-región/residency, verticales, soberano, SOC 2/ISO formales, expansión EE. UU.

## 10. Métricas del PRD (por fase)

| Fase | Métrica de salida | Umbral (SU) |
|---|---|---|
| 1 | Adopción frontline semanal en pilotos | >80% |
| 1 | Éxito de sync | >99.9%/día |
| 1 | Tiempo al primer valor | <1 día |
| 2 | Flujo repuesto→OT→factura auditado E2E | 2 clientes |
| 2 | Exactitud de inventario | ≥95% |
| 3 | % OTs creadas por canales automáticos | ≥30% |

## 11. Criterios de aceptación del documento
1. Toda capacidad con prioridad MoSCoW, journey y persona. ✅
2. Won't explícito por fase. ✅
3. Métricas de salida por fase. ✅
4. Trazabilidad a decisiones aprobadas. ✅

## 12. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador.

## 13. Referencias cruzadas
Depende de: 01–04, 13, 14, 15, 16, 17, 19, ADR-011/012, AUD-00. Alimenta: 11, 12, 10, 43, 69.

## 14. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). Capacidades F0–F5 con MoSCoM, trazabilidad a journeys/personas, Won't explícitos, métricas de salida por fase |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
