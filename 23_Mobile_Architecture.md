# 23 — Mobile Architecture

| Campo | Valor |
|---|---|
| Documento | 23_Mobile_Architecture |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Autoría | Equipo de documentación DONEFIXER bajo dirección del Fundador |
| Precedencia | Documento 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | ADR-011 v1.1 (incl. regla de autoridad del backend, texto literal del Fundador), Doc 27 (Offline/Sync), Doc 14 (Dominio), Doc 18 (IA), Doc 15 (Personas), Doc 16 (Journeys), Docs 11/12 (RF/RNF) |

> **Convención de evidencia:** DC · SU · PD en toda afirmación relevante.
> **Advertencia permanente:** la decisión **N-1 (framework móvil) permanece PD**. Este documento es deliberadamente **agnóstico de framework**: define la arquitectura que cualquier framework elegido deberá satisfacer, y la matriz de evaluación con la que N-1 se resolverá. Ninguna sección asume Flutter como definitivo. (DC — corrección expresa del Fundador, ADR-011 v1.1 §3.4)

---

## 1. Propósito y alcance

Define la arquitectura del canal móvil nativo de DONEFIXER — el **canal primario del usuario primario** (técnico de campo, P-T1) — incluyendo: estructura interna de la app, almacenamiento local, integración con el motor de sincronización, experiencia offline, seguridad del dispositivo, rendimiento, testing, y el proceso formal para resolver N-1. (DC)

**Fuera de alcance:** elección del framework (N-1 PD), código, diseños visuales finales. (DC)

---

## 2. Principios del canal móvil

1. **Offline es el modo normal, no el modo degradado.** La app se diseña y prueba primero sin conectividad (Doc 16 J-2 como prueba literal de "modo avión"). (DC)
2. **La verdad local es SQLite cifrado; la verdad oficial es el servidor.** Toda decisión local es provisional hasta re-validación en sincronización (ADR-011 v1.1, texto literal del Fundador; Doc 27 SY-8). (DC)
3. **El estado provisional es visible.** El técnico siempre distingue dato confirmado de dato pendiente de sincronización (Doc 16, flujos OFF). (DC)
4. **Cero reglas críticas con autoridad en el cliente.** Validaciones locales sí; autoridad final, nunca (Doc 24, Doc 27). (DC)
5. **Un técnico con guantes, sol directo y una mano ocupada es el caso de diseño base**, no la excepción (Doc 15 P-T1, escenarios offline). (DC)

---

## 3. Decisiones MA (Mobile Architecture)

### MA-1. Arquitectura interna por capas, independiente del framework. (DC)

```
┌─────────────────────────────────────────────────────┐
│ UI (pantallas, componentes, navegación)             │
├─────────────────────────────────────────────────────┤
│ Casos de uso (view models / controladores)          │
│ — orquestan, nunca contienen reglas críticas        │
├─────────────────────────────────────────────────────┤
│ Capa de dominio local (validaciones provisionales,  │
│ máquina de estados *informativa*, sin autoridad)    │
├─────────────────────────────────────────────────────┤
│ Capa de datos                                       │
│  ├─ Repositorios (lectura desde SQLite local)       │
│  ├─ Outbox local (operaciones pendientes,           │
│  │   operation_id + HLC + payload, misma            │
│  │   transacción que el cambio — Doc 27 SY-4)       │
│  └─ Adaptador de sincronización (único punto de     │
│      contacto con el motor de sync)                 │
├─────────────────────────────────────────────────────┤
│ Infraestructura de dispositivo                      │
│ (SQLite/SQLCipher, cámara, GPS, biometría, archivos)│
└─────────────────────────────────────────────────────┘
```

El **adaptador de sincronización** es una interfaz única y acotada: el framework y el motor de sync (PowerSync según N-2, o su fallback) pueden cambiar sin tocar casos de uso ni UI. Esta es la protección arquitectónica explícita contra dos decisiones abiertas (N-1, N-2). (DC)

### MA-2. Almacenamiento local: SQLite cifrado (SQLCipher) como réplica de trabajo. (DC)

Esquema local alineado al modelo de dominio (Doc 14) limitado a los **buckets de sincronización del perfil del usuario** (Doc 27 SY-12: el técnico replica sus OT, activos de su zona, catálogos; no el tenant completo). Cifrado en reposo obligatorio (RNF-SEC-003). Borrado remoto al cerrar sesión o revocar acceso (RNF-SEC-005). (DC)

### MA-3. Cola de operaciones (outbox local) con garantías normativas. (DC)

- `operation_id` UUID generado en cliente; idempotencia de punta a punta (Doc 27 SY-5; Doc 29 AP-8).
- HLC por dispositivo para ordenamiento causal (SY-6).
- Reintentos con backoff; operaciones fallidas tras veredicto REJECT pasan a bandeja visible del usuario con explicación (nunca desaparecen en silencio). (DC)

### MA-4. Captura de evidencias offline. (DC)

Fotos/firmas/notas de voz se almacenan en el sistema de archivos cifrado del dispositivo con hash SHA-256 calculado en captura; los binarios se suben en la sincronización por canal separado y reanudable (los metadatos viajan con la operación; el binario no bloquea la cola de operaciones — Doc 27 SY-13). Compresión adaptativa según red. (DC)

### MA-5. Escaneo QR/código como entrada primaria de identificación de activos. (DC)

El centro de la barra inferior ([Escanear], Doc 18) abre cámara directa: identificar activo → acciones contextuales (ver historial, crear aviso, iniciar OT). Funciona 100% offline contra la réplica local. Trazabilidad: RF-WO-006 (escaneo QR), RF-REQ-001 (intake por QR); J-1/J-2. (DC)

### MA-6. Navegación móvil anclada a la IA canónica. (DC)

Barra inferior: **[Hoy] [Órdenes] [Escanear] [Avisos] [Más]** (Doc 18, DC). Profundidad máxima de 3 niveles para tareas de técnico; cualquier flujo crítico (reportar falla, completar OT) en ≤ 5 toques (RNF-USE-001, J-1 ≤60 s). (DC)

### MA-7. Seguridad del dispositivo. (DC)

| Control | Decisión | Trazabilidad |
|---|---|---|
| Autenticación | OIDC con PKCE; refresh rotation | RNF-SEC-005 |
| Desbloqueo rápido | Biometría/PIN local opcional por política del tenant (no sustituye re-autenticación periódica) | RNF-SEC-004; Doc 19 |
| Datos en reposo | SQLCipher + keystores del SO | RNF-SEC-003 |
| Sesión | Cierre remoto, borrado local, lista de dispositivos visible para el usuario y admin | RNF-SEC-005 |
| Root/jailbreak | Detección con política por tenant (avisar/bloquear) — SU, calibrar en pilotos | SU |

### MA-8. Rendimiento y presupuestos móviles. (DC)

| Presupuesto | Objetivo | Trazabilidad |
|---|---|---|
| Arranque en frío a pantalla útil | ≤ 2 s en gama media Android | RNF-PERF-004 (apertura de OT como operación de referencia) |
| Búsqueda local FTS sobre réplica | ≤ 300 ms p95 — **aclaración AO-3:** métrica de búsqueda de texto completo, distinta de la lectura simple de RNF-PERF-002 (<100 ms); no hay conflicto entre ambas | RNF-PERF-002 (lecturas simples); métrica FTS propia (SU); Doc 31 SE-3 |
| Consumo de batería | Sin wakelocks persistentes; sync por lotes, no continuo | RNF-MOB-003 |
| Datos móviles | Sync incremental; evidencias diferibles a Wi-Fi por configuración | RNF-MOB-004 |
| Dispositivo objetivo mínimo | Android gama media de los países piloto (PD-3) — definir en pilotos | SU |

### MA-9. Notificaciones push y sincronización en segundo plano. (DC)

Push (FCM/APNs) como señal de "hay novedades", nunca como transporte de datos; el dato real llega por el canal de sync (Doc 27). Sincronización en segundo plano sujeta a las restricciones del SO con degradación elegante documentada (Doc 16, flujos OFF). (DC)

### MA-10. Testing móvil normativo. (DC)

| Capa | Contenido obligatorio |
|---|---|
| Unitaria | Casos de uso, validaciones provisionales, HLC, outbox |
| Integración sync | Los **8 casos límite normativos** del Doc 27 (doble completado, stock concurrente offline, tombstone vs. edición, etc.) |
| E2E dispositivo | **J-2 completo en modo avión literal** + convergencia 7 días/200 operaciones (RNF-SYNC-003) |
| Campo | Pruebas con técnicos reales en pilotos (Doc 15 P-T1 escenarios) |

---

## 4. Resolución de N-1: matriz de evaluación formal (framework sigue PD)

La elección se hará con esta matriz ponderada cuando el Fundador lo decida. **Ninguna columna está cerrada; Flutter es candidato con cláusula de cambio, no decisión** (ADR-011 v1.1 §3.4). (DC/PD)

| Criterio | Peso | Qué se medirá |
|---|---|---|
| Calidad de integración con motor de sync y SQLite local | 25% | Madurez del SDK del motor elegido (N-2) en cada framework; prueba de concepto con outbox local |
| Rendimiento en Android gama media (arranque, listas densas, cámara) | 20% | Benchmark de PoC contra presupuestos MA-8 |
| Acceso a capacidades nativas (cámara, GPS, biometría, background) | 15% | Cobertura sin código nativo ad hoc |
| Productividad de un equipo mínimo + freelancers (N-10 PD) | 15% | Tiempo de implementación del mismo flujo J-2 en PoC |
| Compartición con web (tokens de diseño, lógica no crítica) | 10% | Reutilización real medida en PoC |
| Mercado de talento y longevidad del framework | 10% | Datos de hiring y salud del ecosistema al momento de decidir |
| Riesgo de plataforma (licencias, dependencia de vendor) | 5% | Revisión de licencias y gobernanza |

**Candidatos registrados (todos vivos hasta N-1):** Flutter, React Native/Expo, Kotlin Multiplatform + Compose/SwiftUI, nativo dual puro. La PoC comparativa sobre el flujo J-2 es el entregable que habilita la decisión (Doc 27 §Alternativas exige la misma PoC para el motor de sync; se ejecutan juntas). (DC)

---

## 5. Alternativas evaluadas (nivel arquitectura, no framework)

| Alternativa | Razón de descarte | Evidencia |
|---|---|---|
| **App nativa con réplica local SQLite (elegida)** | — | DC |
| PWA como único canal móvil | Insuficiente para offline profundo (almacenamiento, background, cámara robusta); rechazada en ADR-011 | DC |
| App híbrida WebView (Cordova/Capacitor) | Rendimiento y UX por debajo de RNF-USE/RNF-PERF para uso de campo intensivo | DC descartada |
| Réplica local en almacenamiento clave-valor (no SQLite) | Consultas relacionales del dominio (árbol de activos, historiales) requieren SQL local; además el motor de sync se apoya en SQLite | DC descartada |

---

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| N-1 se resuelve hacia un framework con SDK de sync débil | Alto | Criterio de mayor peso (25%) en la matriz; PoC antes de decidir; adaptador de sync acotado (MA-1) |
| Complejidad de la UI de estados provisionales/veredictos | Alto | Patrones de UX de sync definidos en Doc 16 flujos OFF; pruebas de campo en pilotos |
| Fragmentación Android en países piloto (PD-3) | Medio | Dispositivo objetivo mínimo definido con pilotos; pruebas en gama media real |
| Límite de almacenamiento local por réplica grande | Medio | Buckets por perfil (SY-12) + poda de datos históricos locales |

---

## 7. Evolución

- **Etapa B:** escaneo de códigos de barras industriales adicionales, modo tablet para supervisores de planta, widgets de "Hoy".
- **Etapa C:** wearables (SU), realidad aumentada para identificación de activos (SU, solo si pilotos Enterprise lo demandan vía FEP, Doc 02 §10 bis).
- En todas: el adaptador de sincronización y la capa de dominio local permanecen estables aunque cambie el framework o el motor de sync. (DC)

---

## 8. Criterios de aceptación de este documento

1. Agnosticismo de framework verificable: ninguna decisión MA depende de un framework específico. ✅
2. N-1 y N-2 abiertas, con matriz formal y PoC definida para resolverlas. ✅
3. Coherencia total con Doc 27 (outbox local, HLC, buckets, veredictos) y ADR-011 v1.1 (regla del Fundador literal). ✅
4. Alternativas, riesgos, impacto operativo, evolución y criterios incluidos. ✅

---

*Registro de cambios — v1.0: creación (Ola 3, documento 12 de 14).*

*v1.1 (2026-07-29) — Erratas editoriales AO-1 y AO-3 (autorizadas por el Fundador, sin cambio de decisiones): identificadores corregidos al catálogo oficial (RNF-SEC-003/004/005, RNF-MOB-003/004, RNF-SYNC-003, RNF-PERF-002/004, RNF-USE-001, RF-WO-006, RF-REQ-001); aclaración AO-3 de alcance de la métrica de búsqueda local FTS (≤300 ms) vs. lectura simple RNF-PERF-002 (<100 ms).*
