# 22 — Web Architecture

| Campo | Valor |
|---|---|
| Documento | 22_Web_Architecture |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Autoría | Equipo de documentación DONEFIXER bajo dirección del Fundador |
| Precedencia | Documento 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | ADR-011 v1.1, Docs 14, 18 (AI), 11 (RF), 12 (RNF), 21 (Solución), 27 (Sync), 29 (API) |

> **Convención de evidencia:** DC · SU · PD en toda afirmación relevante.

---

## 1. Propósito y alcance

Define la arquitectura de los canales web de DONEFIXER: la **Web App** (canal de administración, supervisión, planificación, compras, reportes y configuración de tenant) y la **PWA** (continuidad ligera, mismo codebase). Conforme a ADR-011 v1.1, Web App y PWA son **una sola base de código React** con capacidades diferenciadas por manifiesto y configuración, no dos productos. (DC)

**Fuera de alcance:** la app móvil nativa (Doc 23), el framework móvil (PD N-1), código, y endpoints definitivos. (DC)

---

## 2. Decisiones WA (Web Architecture)

### WA-1. Stack: React + TypeScript + Vite (SPA). (DC)

Single Page Application renderizada en cliente, sirviendo una API REST versionada (Doc 29). **Justificación trazada:** la Web App es una aplicación de trabajo intensiva en interacción (tableros, planificadores, formularios dinámicos), no un sitio de contenido; el SEO no es requisito funcional de los canales autenticados (Doc 18); un único equipo (N-10 PD) se beneficia de un stack maduro, con el mayor mercado de talento y ecosistema de componentes. RNF-MNT-001 (mantenibilidad), RNF-USE-004 (estado del sistema siempre visible), ADR-011 (Web App + PWA un codebase). (DC)

### WA-2. Un solo codebase para Web App y PWA. (DC)

Diferenciación por *build targets* y manifiesto PWA: la PWA habilita service worker, instalación y caché de shell; la Web App de escritorio no instala. La PWA ofrece **continuidad ligera** (consulta, aprobaciones, avisos) y **no reemplaza** a la app nativa para trabajo de campo offline intensivo (ADR-011 v1.1 §Matriz de prioridad de canales). (DC)

### WA-3. Capacidad offline web: consulta y captura limitada, no ejecución completa. (DC)

La PWA cachea el shell y datos de consulta frecuente (IndexedDB); la captura offline web se limita a formularios de alta prioridad (aviso de falla, J-1) con cola local de envío. La ejecución completa de órdenes de trabajo offline (7 días, 200 operaciones, RNF-SYNC-003) es responsabilidad de la app nativa con SQLite + SQLCipher (Doc 27). Esta división respeta ADR-011 (paridad funcional controlada, no réplica) y evita duplicar el motor de sincronización en IndexedDB. (DC)

> **SU (marcado):** si los pilotos demuestran demanda real de ejecución completa de OT desde navegador (técnicos con tablet compartida sin app), se evaluará elevar la capacidad offline de la PWA mediante ADR, reutilizando la abstracción de sync del Doc 27.

### WA-4. Arquitectura interna: modular por contextos de dominio. (DC)

Estructura por *feature modules* alineados a los bounded contexts del Doc 14 (trabajo, activos, planificación, inventario, compras, gobierno), con tres capas internas: **UI (componentes) → estado y casos de uso (hooks/stores) → cliente de API (generado desde OpenAPI, Doc 29 AP-3)**. Ningún componente de UI llama a la API directamente sin pasar por la capa de casos de uso; esto mantiene la separación dominio/aplicación/infraestructura también en el cliente (regla de la Ola 3). (DC)

### WA-5. Estado: servidor como fuente de verdad; caché de servidor con TanStack Query; estado local mínimo. (DC)

- **Datos de servidor:** TanStack Query (caché, revalidación, invalidación por mutación). Los veredictos de sincronización (ACCEPT/ADJUST/REJECT, Doc 27 SY-9) se reflejan en la UI mediante invalidación explícita.
- **Estado de UI local:** estado de React/Zustand solo para UI efímera (modales, filtros, borradores de formulario).
- **Prohibido:** duplicar reglas de negocio en stores; los clientes ejecutan solo validaciones provisionales conforme a la regla literal del Fundador (ADR-011 v1.1), y toda decisión que modifique estado oficial se re-valida en servidor. (DC)

### WA-6. Sistema de diseño propio sobre librería headless. (DC)

Componentes accesibles headless (Radix UI o equivalente) + sistema de diseño DONEFIXER (tokens, tipografía, densidad) + Tailwind CSS para utilidades. **Justificación:** branding por tenant (ADR-012: branding administrable) exige tokens tematizables; una librería de componentes cerrada (MUI/AntD) dificulta white-label; construir todo desde cero es inviable para el equipo. WCAG 2.2 AA interno desde Fase 1 (N-8 PD para certificación formal VPAT). (DC) Trazabilidad: RNF-ACC-001 (accesibilidad web/PWA), Doc 03 (plan Enterprise white-label). (DC)

### WA-7. Internacionalización como capacidad estructural. (DC)

i18n desde el primer componente (catálogo de mensajes, nunca cadenas embebidas), etiquetado anclado al Glosario Canónico (Doc 13), formatos de fecha/moneda por locale, UTC interno (Doc 29 AP-11). Idiomas de lanzamiento: **PD-4 permanece abierto** (recomendación ES+EN registrada en N-6, no confirmada). La arquitectura no asume el conjunto final. (DC/PD)

### WA-8. Seguridad del cliente web. (DC)

- Tokens OIDC en memoria + refresh rotation; **prohibido localStorage para tokens de acceso** (RNF-SEC-005).
- CSP estricta, `SameSite` en cookies de sesión auxiliares, sanitización de HTML enriquecido (comentarios), subida de archivos solo vía URLs firmadas (Doc 25 §Objetos).
- Ningún dato sensible en logs del navegador; clasificación de datos respetada en telemetría (Doc 25 §Clasificación). (DC)

### WA-9. Rendimiento web: presupuestos explícitos. (DC)

| Presupuesto (Etapa A) | Valor objetivo | Medición | Trazabilidad |
|---|---|---|---|
| Carga inicial (ruta principal, 4G) | ≤ 200 KB JS gzip en el primer paint útil; LCP ≤ 2.5 s | Lighthouse CI en cada PR | RNF-PERF-003 |
| Interacción en tableros densos | INP ≤ 200 ms p75 | RUM sintético | RNF-PERF-001 |
| Tablas grandes | Virtualización obligatoria >200 filas; paginación por cursor (Doc 29 AP-5) | Prueba de componente | RF-RPT, RNF-PER |
| Code splitting | Por módulo de contexto de dominio | Bundle analyzer en CI | RNF-MNT |

### WA-10. Testing web por capas. (DC)

| Capa | Herramienta tipo | Cobertura obligatoria |
|---|---|---|
| Componentes | Testing Library | Componentes de formularios críticos (OT, evidencias) |
| Casos de uso / stores | Vitest | Validaciones provisionales y cola offline de captura web |
| E2E | Playwright | Journeys J-1, J-3, J-4, J-6, J-8 (los de canal web del Doc 16) |
| Accesibilidad | axe en CI | Sin violaciones críticas (N-8 interno) |
| Visual | Snapshot selectivo | Sistema de diseño, no pantallas completas |

---

## 3. Mapa de módulos web (anclado a la IA del Doc 18)

| Módulo web | Objetos de IA que cubre | Personas principales (Doc 15) | Canal prioritario |
|---|---|---|---|
| Trabajo | Solicitudes, Órdenes de Trabajo, Avisos | P-S1 supervisor, P-D1 planificador, P-R1 solicitante | Web + móvil |
| Planificación | Planes PM, calendario, asignación | P-D1, P-S1 | **Web prioritario** |
| Activos | Árbol de activos, medidores, historial | P-A1 admin de activos, P-X1 director | Web prioritario |
| Inventario | Repuestos, stock, movimientos | P-S1, P-A1 | Web + consulta móvil |
| Compras | Requisiciones, órdenes de compra, proveedores, facturas | P-M1 gerente/compras, P-F1 finanzas, P-V1 proveedor (portal) | Web prioritario |
| Reportes | Tableros, exportaciones, reportes programados | P-X1, P-M1, P-U1 auditor | Web prioritario |
| Configuración | Usuarios, roles, catálogos, flujos, branding | P-C1 admin tenant | Web exclusivo |
| Copiloto IA | Consulta NL con cite-or-abstain | Todos (Doc 31 SE-6) | Web + móvil |

---

## 4. Alternativas evaluadas

| Alternativa | Razón de descarte/posposición | Evidencia |
|---|---|---|
| **React SPA + Vite (elegida)** | — | DC |
| Next.js (SSR/RSC) | SSR aporta SEO que los canales autenticados no necesitan; añade servidor Node que operar y complejidad de hidratación para una app de trabajo; si en el futuro existe sitio público/marketing, será un proyecto separado | DC descartada |
| Angular | Stack viable pero menor flexibilidad de ecosistema headless y mercado de talento freelance (N-10) | DC descartada |
| Blazor | Unificaría lenguaje con backend .NET, pero ecosistema de componentes/accesibilidad/i18n más pobre y hiring móvil/web fragmentado | DC descartada |
| HTMX/Alpine | Insuficiente para tableros densos, planificadores y captura offline con cola | DC descartada |
| PWA con ejecución completa de OT offline | Duplicaría el motor de sync sobre IndexedDB; diferida, no descartada — SU con vía de ADR | SU pospuesta |

---

## 5. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Duplicación de lógica de validación cliente/servidor | Medio | Esquemas de validación derivados de contratos OpenAPI; el servidor siempre re-valida (regla del Fundador) |
| Deriva visual Web vs. móvil | Medio | Tokens de diseño compartidos como paquete versionado (Doc 23 §Móvil) |
| Crecimiento del bundle | Medio | Presupuestos en CI (WA-9) con fallo de build |
| Accesibilidad degradada por componentes custom | Medio | Base headless accesible + axe en CI |

---

## 6. Evolución

- **Etapa B:** portal de proveedor como surface web separada del mismo codebase (módulo Compras), tableros embebibles, posible elevación de offline PWA (SU de WA-3).
- **Etapa C:** micro-frontends solo si múltiples equipos lo exigen (criterio: >2 equipos frontend simultáneos); theming completo white-label por tenant. (DC — criterios, no compromisos)

---

## 7. Criterios de aceptación de este documento

1. Stack y estructura trazados a RF/RNF/ADR; sin tecnología por tendencia. ✅
2. Coherencia con ADR-011 v1.1 (un codebase Web/PWA; paridad controlada; regla de autoridad del backend literal). ✅
3. Coherencia con Doc 27 (no duplicar motor de sync) y Doc 18 (IA canónica). ✅
4. Alternativas, riesgos, impacto operativo, evolución y criterios incluidos. ✅

---

*Registro de cambios — v1.0: creación (Ola 3, documento 11 de 14).*

*v1.1 (2026-07-29) — Errata editorial AO-1 (autorizada por el Fundador, sin cambio de decisiones): identificadores corregidos al catálogo oficial (RNF-SYNC-003, RNF-ACC-001, RNF-USE-004, RNF-SEC-005, RNF-PERF-003 para carga inicial, RNF-PERF-001 para interacción API).*
