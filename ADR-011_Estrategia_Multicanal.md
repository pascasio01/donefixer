# DONEFIXER — ADR-011 · Estrategia Multicanal con Paridad Funcional Controlada

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **ADR-011 · Versión 1.1 · 2026-07-29 · Estado: APROBADO CON MODIFICACIONES por el Fundador (DC)**
> **Modificaciones aprobadas:** (1) sustitución de la regla de autoridad del backend (§3.1); (2) el framework móvil permanece PD — Flutter NO es decisión definitiva (§3.4).
> **Tipo:** Decisión arquitectónica estratégica — reversible parcialmente, con consecuencias de largo alcance en docs 14, 22, 23 y en las specs de módulo.

---

## 1. Decisión confirmada (texto normativo)

DONEFIXER adoptará una estrategia multicanal con paridad funcional controlada:

1. **Web App** responsive y empresarial.
2. **Progressive Web App (PWA)** instalable.
3. **Aplicación móvil nativa** para iOS y Android.

Todos los canales compartirán: APIs, modelo de dominio, autenticación, permisos, reglas de negocio, datos, auditoría, automatización e inteligencia artificial.

La experiencia **no será una réplica visual idéntica** entre plataformas. Cada interfaz se adaptará al contexto y capacidades del dispositivo, manteniendo **consistencia funcional, semántica y de marca**.

### Prioridades por canal

| Canal | Prioridad funcional (DC) |
|---|---|
| **App móvil nativa** | Flujos de campo, trabajo offline, captura de evidencia, cámara, GPS, QR, voz, firma, biometría, notificaciones push, sincronización en segundo plano |
| **Web App** | Administración, configuración, planificación, analítica, reportes, operaciones masivas, gobierno de la plataforma |
| **PWA** | Instalación ligera y continuidad básica; **no sustituye automáticamente a la app nativa** cuando existan requisitos técnicos que los navegadores no puedan garantizar |

---

## 2. Contexto y fundamento

- La investigación de mercado (doc 04) confirmó que la adopción del técnico de campo decide la calidad del dato — de ahí la primacía móvil — y que la administración enterprise ocurre en escritorio (planificación, reportes, gobierno).
- La auditoría (AUD-00 §3) documentó que las limitaciones de background sync, cámara avanzada, biometría y almacenamiento local son **restricciones de los navegadores**, no del framework: la PWA complementa pero no sustituye (coherente con la decisión).
- Una sola fuente de verdad funcional (API + dominio + reglas en el backend) evita la divergencia de lógica entre clientes, el error más costoso de los productos multicanal.

## 3. Consecuencias confirmadas (derivadas de la decisión)

1. **Regla de autoridad del backend (DC, texto aprobado por el Fundador, sustituye a la formulación anterior):**
   > **"Las reglas críticas del negocio tienen su autoridad en el backend. Los clientes podrán ejecutar validaciones y lógica local necesarias para una experiencia Offline-First, pero toda decisión que modifique el estado oficial del sistema deberá validarse nuevamente en el servidor durante la sincronización."**

   Interpretación normativa (DC): (a) el cliente **puede y debe** ejecutar validaciones locales (formularios, máquina de estados local, permisos cacheados, reglas de captura) para que el trabajo offline sea posible y fluido; (b) esas decisiones locales son **provisionales**: al sincronizar, el servidor re-valida cada mutación contra la autoridad del dominio (estado, permisos, inventario, SLA) y puede aceptar, ajustar o rechazar con resolución documentada (doc 27 — matriz de conflictos); (c) el cliente muestra al usuario el resultado de esa re-validación (confirmado/ajustado/rechazado) — nunca simula éxito definitivo de una operación aún no sincronizada; (d) la lógica local se deriva del mismo contrato de dominio (especificación compartida), no se reinventa por canal — la duplicación de reglas entre cliente y servidor se minimiza y, cuando exista, se genera o se testea contra el mismo contrato (docs 24, 27, 47). Los tres canales consumen la misma API versionada (ADR-009).
2. **Paridad funcional controlada — matriz normativa:** cada capacidad declara su cobertura por canal en su spec de módulo (doc 43) con uno de tres valores: **Total** (todos los canales), **Prioritario** (canal líder + versión reducida en otros), **Exclusivo** (solo un canal, con justificación). Ejemplos normativos:

| Capacidad | Móvil nativo | Web App | PWA |
|---|---|---|---|
| Ejecutar OT offline con evidencia (foto/voz/firma/GPS) | **Total (prioritario)** | No aplica campo | Reducida (sin garantía de background/biometría) |
| Planificación, calendario, despacho | Consulta | **Total (prioritario)** | Reducida |
| Analítica, reportes, operaciones masivas | Consulta | **Total (prioritario)** | No |
| Configuración de tenant, roles, gobierno | No | **Exclusivo** | No |
| Portal de solicitante / proveedor | Web ligera responsive | **Total** | Instalable como PWA ligera |
| Notificaciones push | **Total** | Web push donde aplique | Donde el navegador lo garantice |

3. **PWA y Web App comparten codebase** (React + TypeScript): la PWA es la Web App con manifiesto, service worker y estrategia de caché — no es un tercer producto. Costo incremental bajo; se documenta en doc 22 (Web Architecture).
4. **Framework móvil: permanece PD (modificación aprobada por el Fundador).** ADR-011 es agnóstica al framework: la paridad se garantiza en la autoridad del backend y la API, no en el cliente. **Flutter NO es decisión definitiva.** La evaluación técnica y de contratación (N-1) continúa abierta con candidatos Flutter / RN+Expo / nativo / KMP según el registro de decisiones N-1; se cerrará únicamente con la aprobación expresa del Fundador al finalizar dicha evaluación.
5. **Consistencia sin réplica (DC):** un solo Design System (doc 39) con tokens de marca compartidos y patrones adaptados por plataforma (Material/Cupertino en móvil, patrones de productividad de datos en web). La identidad es semántica y de marca, no de píxeles idénticos.
6. **Offline:** la garantía offline-first completa (ciclo OT, evidencias, sync en segundo plano) es responsabilidad del canal nativo; la PWA ofrece continuidad básica (consulta en caché, colas de envío best-effort) y **nunca se anuncia como offline-equivalente** (regla de integridad del Charter §7.5).
7. **Pruebas (doc 47):** la matriz de paridad se convierte en requisito de pruebas: cada spec de módulo declara cobertura por canal y la DoD exige verificarla en los canales marcados como Total.
8. **Accesibilidad (doc 41):** WCAG 2.2 AA aplica a Web App y PWA; equivalencias nativas (VoiceOver/TalkBack, Dynamic Type) en móvil.

## 4. Alternativas evaluadas y descartadas

| Alternativa | Por qué se descarta |
|---|---|
| Una sola PWA para todo | Los navegadores no garantizan background sync, biometría, almacenamiento duradero ni cámara avanzada (AUD-00 §3, fuentes fechadas) — incumpliría la promesa offline del técnico |
| Réplica visual idéntica en los 3 canales | Desaprovecha el contexto de cada dispositivo y contradice la guía explícita del Fundador; aumenta costo sin ganar usabilidad |
| Apps separadas por rol (portal técnico, portal supervisor…) | Rechazada ya en AUD-00 H-06: una app configurable por permisos con experiencia dinámica; se reafirma |
| Lógica duplicada por cliente para "velocidad" | Divergencia de reglas = incidentes de datos; prohibido por consecuencia 1 |

## 5. Decisiones pendientes abiertas por este ADR (PD)

- PD-MC-1: ¿Service worker de la PWA con qué estrategia de caché por sección? → doc 22.
- PD-MC-2: ¿Web push en Web App o solo email/WhatsApp en Fase 1? → doc 22/48 (costo y soporte de navegadores).
- PD-MC-3: Portal de proveedor: ¿PWA propia o secciones de la Web App con rol proveedor? → spec módulo portal proveedor (doc 43).

## 6. Referencias cruzadas
Mantiene/coherente con: ADR-009 (API-First), AUD-00 §3 (mobile) y H-06 (app única por permisos), doc 01 (principios técnico-primero/offline-first), doc 02 (Charter). Actualiza/obliga a: 22 (Web Architecture: Web+PWA un codebase), 23 (Mobile Architecture), 39 (Design System multi-plataforma), 41 (Accesibilidad), 43 (specs con matriz de paridad), 47 (Testing). Registra como resuelta parcialmente la pregunta N-1 (canal móvil confirmado; framework sigue condicionado a contratación).

## 7. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Decisión confirmada por el Fundador (estrategia multicanal con paridad funcional controlada); matriz de paridad normativa; PWA=Web App un codebase; reafirmada app única configurable por permisos |
| 1.1 | 2026-07-29 | **APROBADO CON MODIFICACIONES por el Fundador:** (1) §3.1 sustituida por la regla de autoridad del backend con lógica local offline provisional y re-validación en servidor durante la sincronización (texto normativo del Fundador + interpretación normativa); (2) §3.4: framework móvil permanece **PD** — Flutter no es definitivo, la evaluación N-1 continúa |
