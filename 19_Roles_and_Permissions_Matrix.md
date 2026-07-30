# DONEFIXER — 19 · Roles and Permissions Matrix

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** ✅ APROBADO (aprobación oficial Ola 2, 2026-07-29)
> **Evidencia:** DC para el modelo de identidad (AUD-00 §7, ADR-012 aprobado) y las prohibiciones de IA; SU para la composición exacta de permisos por rol (se valida en pilotos); PD donde falta decisión.

---

## 1. Objetivo
Definir quién puede hacer qué, dónde y bajo qué condiciones — la matriz que gobierna RBAC/ABAC, la experiencia dinámica por permisos (una sola app, H-06/ADR-011) y las transiciones de estado del dominio (doc 14 §7.2).

## 2. Alcance
Roles del plano tenant (cliente), roles del plano plataforma (equipo DONEFIXER), service accounts (API e IA), y la matriz de transiciones de la OT por rol.

## 3. Exclusiones
No implementa IAM técnico (doc 26: OIDC, step-up, SCIM); no define permisos de la consola de plataforma más allá de sus roles (ADR-012 §5 tiene la matriz de acciones críticas).

## 4. Decisiones confirmadas (DC)
1. **Modelo de identidad:** Cuenta (global) → Membresía (usuario×tenant) → Perfil (contexto: sitio/equipo/función) → permisos efectivos = Rol (RBAC) + condiciones contextuales (ABAC: sitio, programa, proveedor asignado). *(AUD-00 §7, gobierno aprobado.)*
2. **Una sola app configurable por permisos** con experiencia dinámica (ADR-011); portales de solicitante/proveedor son experiencias web ligeras con roles restringidos.
3. **Separación de planos permanente:** los roles de plataforma no existen en el plano tenant y viceversa (ADR-012 v1.1).
4. **Mínimo privilegio y segregación de funciones** (ADR-012): quien ejecuta no verifica; quien configura no opera datos de clientes sin consentimiento.
5. **Los agentes IA son Service Accounts con RBAC propio**; prohibiciones de la lista doc 33 son restricciones arquitectónicas de esta matriz (el agente literalmente no posee el permiso).

## 5. Decisiones pendientes (PD)
PD-3 (nombres localizados de roles por región); SSO/SCIM como gate del plan Enterprise (doc 03 — confirmado en pricing, pendiente diseño técnico doc 26).

## 6. Supuestos (SU)
Los nombres de roles son puntos de partida; cada tenant podrá renombrar y componer roles personalizados (Fase 2) sin cambiar los permisos atómicos.

## 7. Dependencias
Doc 13 (glosario), 14 (máquina de estados), 15 (personas), ADR-012. Alimenta: 26 (IAM), 09/11 (RF), 43 (specs), 40 (UX por permisos), 33 (permisos de agentes).

## 8. Riesgos
| Riesgo | Mitigación |
|---|---|
| Explosión de roles personalizados ingobernables | Roles semilla cerrados en Fase 1; personalización Fase 2 con auditoría |
| ABAC mal configurado → acceso excesivo | Simulador de permisos efectivos en Tenant Admin ("ver como") + tests de aislamiento en CI |

---

## 9. Roles del plano TENANT

### 9.1 Catálogo de roles semilla (Fase 1)

| Rol | Persona | Alcance típico (ABAC) |
|---|---|---|
| **Tenant Admin** | P-C1 | Todo el tenant |
| **Director/Portfolio** | P-X1 | Todos los sitios, solo lectura + aprobaciones de alto nivel |
| **Maintenance Manager** | P-M1 | Sitios asignados |
| **Planner/Dispatcher** | P-D1 | Sitios/equipos asignados |
| **Supervisor** | P-S1 | Su equipo/sitio |
| **Technician** | P-T1 | Sus OTs, su sitio, sus rondas |
| **Requester** | P-R1 | Portal/WhatsApp: solo sus solicitudes |
| **Vendor (external)** | P-V1 | Solo OTs asignadas a su empresa + sus facturas |
| **Inventory Clerk** | P-F1 (inventario) | Almacenes de su sitio |
| **Purchasing** | P-F1 (compras) | Requisiciones, OC, facturas de su alcance |
| **Finance** | P-F1 | Facturas, conciliación, reportes de costos |
| **Auditor (read-only)** | P-U1 | Solo lectura + exportación, todo el tenant |

### 9.2 Matriz de permisos por capacidad (extracto normativo)

Leyenda: **C** crear · **R** leer · **U** actualizar · **A** aprobar · **X** ejecutar · **—** sin acceso · **(ctx)** limitado a su contexto ABAC.

| Capacidad | Admin | Manager | Planner | Supervisor | Technician | Requester | Vendor | Inventory | Purchasing | Finance | Auditor |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Solicitudes (crear) | C | C | C | C | C | C(propias) | — | C | C | C | R |
| Solicitudes (triar/aprobar→OT) | A | A(ctx) | A(ctx) | A(su equipo) | — | — | — | — | — | — | R |
| OT ejecutar/evidenciar | X | X | — | X | X(asignadas) | — | X(asignadas) | — | — | — | R |
| OT verificar cierre | A | A(ctx) | — | A(≠ejecutor, DC segregación) | — | — | — | — | — | — | R |
| OT cancelar | A | A(ctx) | U | A(su equipo) | — | — | — | — | — | — | R |
| Activos CRU | CRU | CRU(ctx) | R | R | R | — | R(sus OTs) | R | R | R | R |
| PM planes | CRUA | CRUA(ctx) | CRU | R | R | — | — | — | — | — | R |
| Inventario movimientos | X | R | R | R | X(consumo en OT) | — | — | X | R | R | R |
| Requisiciones | C | C | C | C | C(necesidad) | — | — | C | CRU | R | R |
| Órdenes de compra | A | A(ctx) | — | — | — | — | R(suyas) | — | CRU | R | R |
| Facturas AP | R | R | — | — | — | — | C(propias) | R | R | A(conciliar) | R |
| Contratos/garantías | CRU | CRU(ctx) | R | R | R | — | R(suyos) | — | CRU | R | R |
| Usuarios/roles del tenant | CRUA | R | — | R(equipo) | — | — | — | — | — | — | R |
| Reportes/KPIs | R | R(ctx) | R | R(equipo) | R(propio) | — | R(propio) | R | R | R | R |
| Configuración tenant | CRUA | — | — | — | — | — | — | — | — | — | R |
| Auditoría (ver log) | R | — | — | — | — | — | — | — | — | — | R |

### 9.3 Matriz de transiciones de OT por rol (resuelve AUD-00 H-30)

| Transición | Technician | Supervisor | Planner | Manager | Sistema |
|---|---|---|---|---|---|
| →aprobada | — | ✔(equipo) | ✔ | ✔ | ✔(PM/IoT automática, registrada) |
| →planificada | — | ✔ | ✔ | ✔ | — |
| →asignada | — | ✔ | ✔(sugerencia IA, humano confirma) | ✔ | ✔(reglas automáticas con auditoría) |
| →en_progreso | ✔(asignado) | ✔ | — | ✔ | — |
| →en_espera_* | ✔(motivo) | ✔ | — | ✔ | ✔(reglas, p. ej. repuesto agotado) |
| →completada | ✔ | ✔ | — | ✔ | — |
| →verificada | — | ✔(≠ejecutor) | — | ✔ | — |
| →cerrada | — | ✔ | — | ✔ | ✔(si el tenant no exige verificación) |
| →cancelada | — | ✔ | ✔ | ✔ | — |

## 10. Roles del plano PLATAFORMA (equipo DONEFIXER)

| Rol | Alcance | Controles (DC ADR-012) |
|---|---|---|
| **Platform Owner** (Fundador) | Todo el plano plataforma | MFA + régimen de acciones críticas §3.9 |
| **Platform Admin** | Tenants, planes, flags, soporte | Mismo régimen; dual cuando exista 2º admin |
| **Support Agent** | Lectura asistida de tenant **con consentimiento y notificación** (ADR-012 §3.3) | Acceso temporal, motivo, registro visible al tenant |
| **Platform Auditor** | Solo lectura de auditorías de plataforma | — |
| **Ningún rol tiene:** acceso directo a BD, secretos, código ni infraestructura (prohibido por arquitectura, DC ADR-012) |

## 11. Service Accounts (API e IA)

| Cuenta | Permisos | Prohibiciones arquitectónicas (DC doc 33) |
|---|---|---|
| Integration API (del tenant) | Según scopes otorgados por Tenant Admin | No impersonar usuarios |
| **Agent: Triage** | Crear/actualizar solicitudes, sugerir prioridad | No crear OT directamente sin confirmación |
| **Agent: Scheduler** | Sugerir asignaciones | No asignar sin confirmación humana (riesgo medio) |
| **Agent: Invoice Validator** | Validar y marcar discrepancias | **No aprobar facturas ni pagos (riesgo ALTO)** |
| **Agent: Reporter** | Generar borradores de reportes con fuentes | No publicar sin revisión |
| (Todos los agentes) | — | **Prohibiciones absolutas derivadas ítem por ítem de la lista canónica del Doc 33 §4** (P-33-1 a P-33-7): aprobar/rechazar facturas (P-33-1) · cerrar OTs críticas (P-33-2) · modificar inventario (P-33-3) · acciones sobre personas/sanciones (P-33-4) · comunicación externa sin revisión humana (P-33-5) · acceso a datos de otro tenant (P-33-6) · entrenar modelos con datos de un tenant sin consentimiento explícito (P-33-7). Cada prohibición se implementa como ausencia del permiso correspondiente en esta matriz |

> **Nota AO-2 (2026-07-29):** la lista canónica y normativa de prohibiciones de IA es **únicamente la del Doc 33 §4** (identificadores P-33-1…P-33-7). Esta matriz no define prohibiciones propias: deriva los permisos denegados de aquella lista. Cualquier cambio a las prohibiciones se realiza en el Doc 33 mediante ADR + aprobación expresa del Fundador, y se propaga aquí. |

## 12. Experiencia dinámica por permisos (cómo la matriz se convierte en UI)

La app consulta los permisos efectivos de la membresía/perfil activo y compone: navegación, acciones visibles, campos editables y datos visibles. **Regla DC:** ocultar en UI nunca es seguridad — el servidor siempre re-valida (ADR-011 v1.1); la UI oculta para claridad, el backend deniega para seguridad. Un usuario con múltiples membresías/perfiles cambia de contexto explícitamente (selector visible) y la auditoría registra el contexto usado en cada acción.

## 13. Métricas
% accesos denegados correctamente (tests); incidentes de acceso excesivo (objetivo 0); uso del "ver como" para depuración (salud del soporte); tiempo medio de configuración de roles en onboarding (J-7).

## 14. Criterios de aceptación de este documento
1. Roles de ambos planos + service accounts. ✅ 2. Matriz por capacidad + matriz de transiciones OT. ✅ 3. Prohibiciones de IA como restricciones de permisos, no solo de política. ✅ 4. Segregación ejecutor/verificador explícita. ✅

## 15. Definition of Done
DoR/DoD del Charter. Pendiente: aprobación del Fundador; validación con pilotos de la composición de roles semilla.

## 16. Referencias cruzadas
Depende de: 13, 14, 15, ADR-011/012, AUD-00. Alimenta: 26 (IAM), 33 (gobierno IA), 43 (specs), 40 (UX dinámica), 47 (tests de autorización), 34 (seguridad).

## 17. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 2). 12 roles tenant + 4 plataforma + 5 service accounts; matriz por capacidad; matriz de transiciones OT por rol (H-30); prohibiciones IA como permisos denegados |
| 1.2 | 2026-07-29 | **APROBACIÓN OFICIAL OLA 2** por el Fundador. Condiciones permanentes aplican: personas/journeys/blueprints siguen SU hasta pilotos; dominio canónico; RF/RNF/SRS como contrato funcional; ninguna decisión técnica podrá contradecir el dominio aprobado |
| 1.3 | 2026-07-29 | **AO-2** (autorizada por el Fundador): lista de prohibiciones de IA unificada — este documento ya no define lista propia; deriva los permisos denegados de la lista canónica P-33-1…P-33-7 del Doc 33 §4, ítem por ítem |
