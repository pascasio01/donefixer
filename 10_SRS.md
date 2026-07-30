# DONEFIXER — 10 · Software Requirements Specification (SRS)

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Propósito:** especificación formal que consolida requisitos (docs 11/12), dominio (doc 14), interfaces y restricciones en un único contrato de referencia para diseño, construcción y pruebas. Estructura inspirada en IEEE 830/ISO 29148 adaptada a producto SaaS.
> **Evidencia:** DC / SU / PD por sección; nada aquí contradice los documentos aprobados — si lo hiciera, este documento está mal y se corrige (regla de precedencia: docs aprobados > SRS > specs).

---

## 1. Introducción

### 1.1 Objetivo
Formalizar QUÉ debe hacer el software DONEFIXER (no cómo se construye — eso son los docs 20–33) para que cualquier ingeniero, diseñador o auditor pueda verificar el sistema contra una referencia única.

### 1.2 Alcance del producto
Plataforma SaaS multicanal (Web App, PWA, app nativa — ADR-011) de mantenimiento, órdenes de trabajo, activos, operaciones e instalaciones, multi-tenant, offline-first, AI-gobernada. Fases cubiertas por esta versión: 0–2 en detalle, 3–5 por referencia al PRD (doc 09 §9.4).

### 1.3 Definiciones
Todas las del doc 13 (Domain Glossary) — este SRS no redefine términos.

### 1.4 Referencias
Docs 01–04 (aprobados), 09, 11, 12, 13, 14, 15, 16, 17, 19, ADR-001/005/009/010/011/012, AUD-00.

### 1.5 Precedencia documental (DC)
En conflicto: Constitución/Charter (00/02) > ADRs aprobados > Ola 1 aprobada (01–04) > este SRS > specs de módulo (43). Ningún documento de menor rango puede contradecir a uno de mayor rango; el de menor rango se corrige.

---

## 2. Descripción general

### 2.1 Perspectiva del producto
DONEFIXER es un sistema nuevo e independiente que se integra con: proveedores LLM (IA), WhatsApp Business API (SU H-25), email/SMS, procesador de pagos (PD N-4), ERPs de clientes (Fase 4) y fuentes IoT (Fase 4). No es componente de otro sistema.

### 2.2 Funciones principales (resumen)
Las capacidades del PRD §9 (doc 09) con prioridades MoSCoM por fase. Este SRS no duplica el catálogo: lo referencia (doc 11) y define las reglas transversales que lo gobiernan.

### 2.3 Características de usuarios
Las 11 personas del doc 15 con prioridad P-T1 (técnico) > P-S1 > P-R1 > resto (DC). Niveles digitales heterogéneos: desde cero capacitación (P-T1/P-R1) hasta administradores técnicos (P-C1).

### 2.4 Restricciones generales (DC consolidada)

| # | Restricción | Origen |
|---|---|---|
| C-1 | Offline-first: el ciclo OT funciona sin red | doc 01, ADR-011 |
| C-2 | Autoridad backend; lógica local provisional re-validada en sync | ADR-011 v1.1 (texto del Fundador) |
| C-3 | Multi-tenant con aislamiento probado en CI | ADR-001, AUD-00 §5 |
| C-4 | Separación de planos administrativos permanente | ADR-012 v1.1 |
| C-5 | IA como capa gobernada; prohibiciones arquitectónicas | doc 33 / AUD-00 §11 |
| C-6 | Exclusiones de producto (12 ítems) | doc 01 §12 bis |
| C-7 | Evidencias aditivas e inmutables tras cierre | doc 14 |
| C-8 | Inventario por deltas; prohibido `set` sobre saldos | AUD-00 §4 |
| C-9 | i18n nativa; cero strings hardcodeados | ADR-010 |
| C-10 | Equipo 1–3 personas: arquitectura Etapa A | AUD-00 §I, N-10 (PD) |
| C-11 | Ninguna certificación afirmada sin evidencia | Charter §7.4 |
| C-12 | Stack condicionado: backend .NET (DC razonada de auditoría), PostgreSQL+RLS (DC), sync PowerSync (pendiente ratificación N-2), framework móvil **PD N-1** | AUD-00 §2, N-1/N-2 |

### 2.5 Supuestos (SU)
Equipo unipersonal en Fase 0–1 (N-10 PD) · pilotos con datos reales tras revisión legal (N-3 PD) · idiomas de lanzamiento ES+EN (PD-4 abierto) · países de pilotaje por definir (PD-3 abierto).

### 2.6 Dependencias externas
PowerSync (licencia/términos, verificación trimestral) · LLM providers (sustituibles, ADR-007) · Meta WhatsApp API (SU) · stores Apple/Google (políticas de revisión) · cloud (región según N-7 PD).

---

## 3. Requisitos específicos

### 3.1 Requisitos funcionales
Catálogo completo: **doc 11** (60+ RF en 16 familias, IDs estables, criterios binarios). Regla de este SRS: ningún RF se implementa sin su criterio de aceptación enlazado a pruebas (doc 47).

### 3.2 Requisitos no funcionales
Catálogo completo: **doc 12** (60+ RNF en 13 áreas con valor/fuente/medición). Herencia obligatoria por módulos; relajaciones prohibidas en SEC/SYNC/PRV/AI.

### 3.3 Requisitos de dominio e invariantes
Doc 14: máquina de estados de OT con matriz por rol, invariantes del servidor (re-validación), jerarquía sin ciclos, deduplicación PM, idempotencia de KPIs, fronteras de contextos delimitados.

### 3.4 Requisitos de interfaces externas

| Interfaz | Tipo | Restricciones (DC/SU) |
|---|---|---|
| API REST versionada (v1) | Saliente/entrante | OpenAPI generado desde código; deprecación 12 meses (DC ADR-009); auth OIDC; RNF-PERF-001 |
| Webhooks salientes | Eventos | Firma HMAC + rotación (DC AUD-00 §10); reintentos con backoff; payload versionado |
| PowerSync (sync engine) | Replicación WAL→clientes | Modalidad PD N-2; reglas de sync declarativas por perfil (DC) |
| LLM Gateway (interno) | IA | Multi-proveedor sustituible; cuotas por tenant; sin datos de tenant en entrenamiento base (DC) |
| WhatsApp Business API | Canal intake | SU sujeto a FinOps (H-25); fallback portal/QR/SMS |
| Email/SMS | Notificaciones | Entregabilidad monitoreada; preferencias de usuario |
| Procesador de pagos | Billing SaaS | PD N-4; abstracción en módulo billing |
| Almacenamiento S3-compatible | Evidencias/documentos | URLs firmadas; ciclo de vida a frío; malware scan (SU) |

### 3.5 Atributos de calidad
Prioridad de atributos cuando entran en conflicto (DC de diseño): **1. Integridad del dato · 2. Seguridad/aislamiento · 3. Disponibilidad del trabajo offline · 4. Usabilidad frontline · 5. Rendimiento · 6. Costo**. Ejemplo normativo: si un requisito de rendimiento amenaza integridad del dato, gana integridad.

### 3.6 Requisitos de datos
Campos de plataforma en toda entidad (DC doc 14 §4.1) · retención PD-RETENCIÓN · exportación por tenant (RNF-PRV-002) · clasificación de datos (doc 44, pendiente Ola 4) · residencia según N-7 (PD).

### 3.7 Requisitos de internacionalización
RF-I18N-* (doc 11) + contenido legal por jurisdicción (doc 37) + variantes regionales configurables por tenant (PD-3).

### 3.8 Restricciones de diseño impuestas
C-1…C-12 de §2.4 son restricciones vinculantes para cualquier diseño; violar una exige ADR nuevo aprobado por el Fundador.

---

## 4. Trazabilidad (resumen operativo)

| Origen | Destino | Mecanismo |
|---|---|---|
| Estrategia (01–04) → PRD (09) | Capacidades por fase | §9 doc 09 |
| PRD → RF (11) | Cada capacidad M/S tiene RF | Familias RF-* |
| RF → Journeys (16) | Columna Traz. en doc 11 | 100% cobertura (gate G2) |
| RF/RNF → Pruebas (47) | Criterio de aceptación = caso de prueba | Matriz de pruebas |
| RNF → Arquitectura (20–33) | Cada RNF tiene decisión que lo satisface | Revisión Ola 3 |
| Decisiones → ADR | Toda irreversible | Registro ADR |

## 5. Criterios de aceptación del documento
1. Precedencia documental declarada. ✅ 2. Restricciones consolidadas con origen. ✅ 3. Sin duplicación de catálogos (referencia, no copia). ✅ 4. Trazabilidad operativa definida. ✅

## 6. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador; actualización al aprobarse N-1/N-2/N-4/N-7 (§2.4 C-12 y §2.5–2.6).

## 7. Referencias cruzadas
Depende de: todos los docs Ola 1–2. Alimenta: 20–33 (arquitectura), 43 (specs), 47 (pruebas), 70 (PRR).

## 8. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). SRS formal con precedencia documental, 12 restricciones vinculantes, interfaces externas, prioridad de atributos de calidad, trazabilidad operativa |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
