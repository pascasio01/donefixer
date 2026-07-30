# DONEFIXER — 18 · Information Architecture (Arquitectura de Información)

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Evidencia:** SU (estructura propuesta a validar con usuarios en pilotos — card sorting/tree testing, doc 47) salvo reglas DC de decisiones aprobadas.

---

## 1. Objetivo
Definir cómo se organiza, nombra, navega y encuentra la información en los tres canales (ADR-011), para que un técnico encuentre su trabajo en ≤2 niveles y un gerente sus KPIs sin buscar.

## 2. Alcance
Taxonomía, navegación por rol (experiencia dinámica, doc 19 §12), búsqueda, etiquetado y modelo de navegación por canal. Fases 1–2; Fase 3+ se extiende en specs.

## 3. Exclusiones
Diseño visual y componentes (docs 39/40); estructura de datos (doc 14/25); contenido de ayuda (doc 69-User Documentation).

## 4. Decisiones confirmadas (DC)
- Experiencia dinámica por permisos: **la navegación se compone según el rol**, no existe una navegación única (doc 19 §12, ADR-011).
- Consistencia semántica entre canales, sin réplica visual (ADR-011).
- Glosario canónico como fuente de todo etiquetado (doc 13, regla DC).
- Usuario primario manda: el móvil se organiza alrededor del **trabajo del día**, no de módulos administrativos (doc 01).

## 5. Decisiones pendientes (PD)
PD-4 (etiquetas por idioma de lanzamiento) · PD-3 (variantes regionales de etiquetas) · búsqueda global con IA (Fase 3, RF-SRCH).

## 6. Supuestos (SU)
La profundidad máxima de 3 niveles es una hipótesis de usabilidad a validar con tree testing en pilotos.

## 7. Dependencias
Docs 13, 14, 15, 16, 19, ADR-011. Alimenta: 39/40 (diseño), 43 (specs de portales), 31 (search), 47 (tests de navegación).

## 8. Riesgos
| Riesgo | Mitigación |
|---|---|
| Navegación por módulos técnicos en vez de por tareas del usuario | Organización por trabajo/objetos, no por features; validación con usuarios |
| Crecimiento desordenado al añadir módulos | Reglas de ubicación (§10): toda nueva capacidad tiene un lugar definido o se justifica vía FEP |

---

## 9. Taxonomía principal (organización por objetos de trabajo, no por módulos)

**Objetos de primer nivel (universo del usuario):**
1. **Trabajo** — mis OTs, solicitudes, calendario, rondas (el hogar del técnico y del supervisor)
2. **Activos** — jerarquía, medidores, historial
3. **Planificación** — planes PM, calendario maestro, despacho (roles de planificación)
4. **Inventario** — ítems, almacenes, movimientos (Fase 2)
5. **Compras y proveedores** — requisiciones, OC, facturas, contratos (Fase 2)
6. **Personas** — usuarios, equipos, habilidades
7. **Reportes** — KPIs, dashboards, programados
8. **Configuración** — del tenant (solo Tenant Admin; plano tenant, ADR-012)

**Regla DC:** el primer nivel nunca supera 8 objetos (carga cognitiva); los módulos nuevos se cuelgan de estos objetos o de un noveno solo con FEP aprobado.

## 10. Navegación por canal

### 10.1 App móvil nativa (P-T1 primero) — SU a validar
```
Barra inferior (máx. 4 + "Más"):
[ Hoy ] [ Órdenes ] [ Escanear ] [ Avisos ] [ Más ]
   │         │          │           │
   │         │          │           └─ Notificaciones + estado de solicitudes
   │         │          └─ Cámara/QR inmediato (acción central siempre visible)
   │         └─ Lista con filtros (asignadas/en espera/completadas)
   └─ Mi día: OTs de hoy + rondas + próximos PM (tarjetas grandes, una mano)
"Más": Activos · Inventario (si rol) · Reportes (si rol) · Mi perfil · Contexto (selector de membresía/sitio)
Estado de sync: indicador persistente en barra superior (DC RNF-USE-004)
```
**Regla:** la acción primaria del técnico (escanear/ejecutar) nunca está a más de 1 toque.

### 10.2 Web App (roles de oficina) — SU
```
Sidebar por objetos (Trabajo · Activos · Planificación · Inventario · Compras · Personas · Reportes · Configuración)
Topbar: búsqueda global · selector de sitio/contexto · notificaciones · usuario
Home por rol: Manager→KPIs y alertas · Planner→calendario/carga · Supervisor→su equipo hoy
```
### 10.3 PWA / portales ligeros (P-R1, P-V1) — SU
```
Solicitante: [ Reportar ] [ Mis solicitudes ] — nada más (DC: sin cuenta compleja)
Proveedor: [ Mis OTs ] [ Facturas ] [ Mi contrato ]
```

## 11. Búsqueda y encontrabilidad

| Mecanismo | Fase | Regla |
|---|---|---|
| Búsqueda global (OTs, activos, personas, repuestos) por texto/QR/ID | 1 | Resultados agrupados por objeto; acción directa desde resultado |
| Filtros guardados por rol | 2 | "Mis OTs en espera", "PMs del mes" como vistas guardadas |
| Búsqueda en lenguaje natural (copiloto con fuentes) | 3 | DC doc 33: responde con fuente o se abstiene |
| Deep links | 1 | Toda OT/activo/solicitud tiene URL compartible respetando permisos (DC ADR-011) |

## 12. Etiquetado (naming en UI)

- Todo label proviene del glosario (doc 13): "Órdenes de trabajo", nunca "Tickets" ni "Tasks" en español de UI (DC).
- Variantes regionales configurables por tenant (PD-3): p. ej., "Repuesto" ↔ "Refacción".
- Verbos de acción en botones ("Completar orden"), sustantivos en navegación ("Órdenes").
- Prohibido jerga técnica interna en UI de usuario (nada de "sync bucket" — se muestra "sincronización", DC RNF-ACC-004).

## 13. Modelo de estados vacíos, errores y ayuda (DC de UX)
Todo objeto declara: empty state con acción sugerida, estado de error con recuperación, estado offline (qué puedo hacer sin red), estado de carga (skeleton). La ayuda es contextual (por pantalla), nunca un manual separado como primera línea.

## 14. Métricas
Tasa de éxito en tree testing por objeto (objetivo ≥80% SU) · toques para llegar a una OT desde home (≤2) · uso de búsqueda vs. navegación · abandono en portal de solicitante (≤10% SU).

## 15. Criterios de aceptación del documento
1. Taxonomía ≤8 objetos de primer nivel con regla de crecimiento. ✅ 2. Navegación por canal y por rol. ✅ 3. Etiquetado anclado al glosario. ✅ 4. Estados (vacío/error/offline/carga) normados. ✅

## 16. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador; validación con card sorting/tree testing en pilotos (v1.1).

## 17. Referencias cruzadas
Depende de: 13, 14, 15, 16, 19, ADR-011. Alimenta: 39, 40, 41, 43, 31, 47.

## 18. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). Taxonomía por objetos de trabajo, navegación móvil "Hoy/Escanear" centrada en técnico, portales ligeros, etiquetado anclado al glosario, métricas de encontrabilidad |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
