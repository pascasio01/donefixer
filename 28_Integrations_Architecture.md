# DONEFIXER — 28 · Integration Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)

---

## 1. Objetivo
Definir cómo DONEFIXER se conecta con el mundo: canales de entrada (WhatsApp, email, QR), webhooks salientes, ERPs, pagos y futuros conectores — con una capa anti-corrupción que protege el dominio canónico (doc 14) de los modelos ajenos.

## 2. Alcance
Integraciones de Fases 1–4 con priorización; patrón de conectores; webhooks; gestión de secretos de integración; monitoreo.

## 3. Exclusiones
Implementación de conectores específicos (specs doc 43); pagos definitivo (PD N-4); IoT (Fase 4, doc 32 futuro).

## 4. Decisiones confirmadas (DC)

| # | Decisión | Trazabilidad |
|---|---|---|
| IN-1 | **Capa anti-corrupción por integración:** cada conector traduce el modelo externo al dominio canónico en su adaptador; los conceptos ajenos nunca cruzan la frontera | doc 24 BK-2, doc 14 canónico |
| IN-2 | **Webhooks salientes** desde eventos de dominio (doc 30): suscripción por tenant, firma HMAC-SHA256, secreto rotativo, reintentos con backoff, payload versionado | AUD-00 §10, doc 30 EV |
| IN-3 | Integraciones con credenciales del cliente: secretos en gestor central (Vault/KMS), rotación, acceso auditado | RNF-SEC, AUD-00 §10 |
| IN-4 | Toda integración entrante normaliza a comandos de la capa de aplicación (misma autoridad que la UI — ADR-011 v1.1) | doc 24 §7 |
| IN-5 | Priorización por demanda verificada de pilotos (FEP), no por catálogo de moda | doc 02 §10 bis |
| IN-6 | WhatsApp como canal de intake sujeto a FinOps (costo por conversación Meta) con fallback portal/QR/SMS | AUD-00 H-25, doc 16 J-1 |
| IN-7 | Monitoreo por integración: éxito, latencia, reintentos, último contacto — visible en consola | RNF-OBS |

## 5. Decisiones pendientes (PD)
N-4 (procesador de pagos) · qué ERPs regionales primero (PD-3 dependiente; candidatos LatAm SU: Softland, Defontana, Alegra + SAP/Oracle enterprise Fase 4) · WhatsApp Business API proveedor (BSP oficial — SU).

## 6. Supuestos (SU)
Los clientes S1 valoran más WhatsApp y exportación contable simple que integración ERP profunda (validar HV en pilotos).

## 7. Catálogo de integraciones por fase

| Fase | Integración | Dirección | Notas |
|---|---|---|---|
| 1 | Email (entrada/salida) | Ambas | Solicitudes por email → triage (SU) |
| 1 | WhatsApp Business API | Entrada | Intake + notificaciones al solicitante (SU-FinOps) |
| 1 | SMS (fallback) | Salida | Notificaciones y fallback de intake (SU) |
| 2 | Procesador de pagos SaaS | Saliente | Billing de suscripciones (PD N-4) |
| 2 | Exportación contable CSV/Excel | Saliente | Facturas AP/costos hacia el ERP del cliente |
| 3 | OCR/visión (proveedor externo o modelo) | Interna | Facturas, activos (doc 33) |
| 4 | ERP conectores (SAP/Oracle/regionales) | Ambas | Capa anti-corrupción; mapeo por conector |
| 4 | IoT/MQTT brokers | Entrada | Doc 25 §7.5 (aplazado E-4) |
| 4 | Identity providers enterprise (SAML/OIDC, SCIM) | Entrada | SSO/SCIM — gate Enterprise (doc 03) |

## 8. Patrón de conector (nivel arquitectónico)

```
Sistema externo ⇄ Adaptador (anti-corrupción: traducción de modelo + validación + idempotencia)
   → Cola de ingreso (reintentos, dead-letter con alerta)
   → Comandos a la capa de aplicación (autoridad intacta)
   → Registro: todo mensaje externo con payload original + resultado (auditoría)
```
**Reglas:** (1) todo conector declara su esquema de mapeo versionado; (2) fallos del sistema externo = reintento, nunca pérdida silenciosa; (3) los secretos del cliente se cifran y su uso se audita; (4) los conectores se activan por tenant (configuración, ADR-012).

## 9. Webhooks salientes (detalle)
- Eventos ofrecidos: subconjunto del catálogo doc 30 §7 elegido por el tenant.
- Entrega: HTTPS POST con firma `X-DONEFIXER-Signature` (HMAC-SHA256 del payload + timestamp), tolerancia a replay por timestamp, reintentos (1m, 5m, 30m, 2h, 12h — SU), desactivación tras N fallos consecutivos con aviso (SU N=50), consola de entregas con reenvío manual.
- Seguridad: secreto por suscripción, rotación sin downtime (dos secretos activos en ventana).

## 10. Alternativas evaluadas
| Alternativa | Veredicto |
|---|---|
| **Conectores propios con capa anti-corrupción (elegido)** | Control total del dominio; costo: cada conector es trabajo propio |
| iPaaS (Zapier/Make) como integración principal | Complemento futuro para clientes (Fase 4); nunca como columna vertebral (dependencia y latencia) |
| ESB/bus empresarial | Sobrearquitectura para Etapa A–B (condición 5) — descartado |
| API suelta sin webhooks | Insuficiente para integradores (polling costoso) — descartado |

## 11. Estrategia de evolución
Fase 1 canales de intake → Fase 2 pagos/exportación → Fase 4 conectores ERP formales + marketplace evaluable (E-8, Etapa C). Cada integración nueva: FEP + análisis de costo recurrente (FinOps) + spec (doc 43).

## 12. Riesgos
| Riesgo | Mitigación |
|---|---|
| Dependencia de Meta (precio/políticas WhatsApp) | Fallback multi-canal (IN-6); FinOps vigila costo |
| Conector ERP diverge del dominio | IN-1 + tests de contrato del mapeo |
| Webhook abusado/spoofed | IN-2 firma + rotación + tolerancia replay |
| Secretos de clientes filtrados | IN-3 + escaneo de secretos en CI |

## 13. Métricas
Éxito de entrega de webhooks · latencia de intake por canal · costo por conversación WhatsApp (FinOps) · tiempo medio de incorporación de un nuevo conector (salud de la capa anti-corrupción).

## 14. Criterios de aceptación
1. Capa anti-corrupción normada. ✅ 2. Webhooks con seguridad y operación completas. ✅ 3. Priorización por FEP, no por moda. ✅ 4. PD explícitas (N-4, ERPs, BSP). ✅

## 15. Referencias cruzadas
Depende de: 24, 29, 30, 14, ADR-012. Alimenta: 43 (specs de conectores), 33 (IA en intake), 60 (FinOps), 65 (soporte de integraciones).

## 16. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). Patrón de conector anti-corrupción, webhooks firmados con operación completa, catálogo por fases, WhatsApp sujeto a FinOps |
