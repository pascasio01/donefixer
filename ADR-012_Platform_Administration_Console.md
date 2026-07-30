# DONEFIXER — ADR-012 · Platform Administration Console

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **ADR-012 · Versión 1.1 · 2026-07-29 · Estado: APROBADO CON AJUSTES por el Fundador (DC)**
> **Ajustes aprobados:** (1) la separación de planos se eleva a principio arquitectónico permanente (§3.1); (2) Admin API con autenticación, autorización, auditoría, versionado y límites independientes (§3.2); (3) retención de auditorías → PD hasta política legal oficial (§6); (4) régimen de acciones críticas Fase 0–1 definido (§3.9); (5) aprobación dual condicionada a segundo administrador autorizado (§3.9); (6) Feature Flags propios → SU hasta análisis FinOps/observabilidad/costos (§6).
> **Tipo:** Decisión arquitectónica de plataforma — gobierno interno de DONEFIXER. Impacta docs 19, 22, 23, 26, 34, 35, 46, 51, 52, 61 y la spec de módulo "Administración de plataforma" (doc 43).

---

## 1. Decisión confirmada (texto normativo)

DONEFIXER incorporará una **Platform Administration Console** protegida y auditada, que permitirá administrar de forma segura:

organizaciones · usuarios · roles · permisos · módulos · planes · entitlements · feature flags · configuraciones · flujos · formularios · automatizaciones · integraciones · idiomas · branding · políticas · versiones · mantenimiento · IA · observabilidad · soporte · facturación · consumo · seguridad.

### Clasificación obligatoria de cambios
Todo cambio operado desde la consola se clasifica en exactamente una categoría:

| # | Categoría | Definición operativa | Ejemplos | Riesgo base |
|---|---|---|---|---|
| 1 | **Configuración dinámica** | Cambio de valor en caliente, sin despliegue, reversible al instante | Umbrales, textos, límites, políticas de SLA | Bajo |
| 2 | **Feature flag** | Activación/desactivación de capacidad por tenant/segmento/% | Nuevo módulo, IA por plan | Bajo-medio |
| 3 | **Actualización remota compatible** | Contenido/lógica actualizable sin release (donde la plataforma lo permita) | Formularios dinámicos, flujos, traducciones, catálogos | Medio |
| 4 | **Despliegue web** | Release de Web App/PWA | Nueva pantalla de admin | Medio |
| 5 | **Actualización móvil mediante tienda** | Release iOS/Android (sujeta a revisión de stores) | Cambio de sync, cámara | Medio-alto (latencia de store) |
| 6 | **Migración de datos** | Cambio de esquema/datos (expand/contract) | Nueva entidad, backfill | Alto |
| 7 | **Cambio de infraestructura** | IaC, red, bases, regiones | Nueva región, upgrade PostgreSQL | Alto |

### Registro obligatorio por modificación (auditoría inmutable)
Cada modificación registra: **actor · fecha · motivo · estado anterior · estado nuevo · alcance · impacto · aprobación · resultado · rollback**. Diez campos, ninguno opcional. Registro append-only, hash-encadenado (coherente con doc 46 Audit Model y ADR de auditoría inmutable previa).

### Controles de acceso
- Acciones críticas: **reautenticación + privilegios elevados** y, cuando corresponda, **aprobación dual** (dos aprobadores; la matriz de qué acciones la exigen se define en doc 26/34; criterio inicial: todo lo de categorías 6–7, todo cambio de entitlements/facturación, y todo acceso a datos de tenant).
- **Prohibido por arquitectura:** la consola **no** ofrece acceso directo e irrestricto a base de datos, código fuente, secretos ni infraestructura. Opera exclusivamente a través de una Admin API interna con comandos autorizados y auditados (no SQL libre, no shells, no llaves).
- Controles: **RBAC + ABAC + mínimo privilegio + segregación de funciones + auditoría inmutable + entornos separados** (la consola de producción no toca staging y viceversa; credenciales y sesiones distintas por entorno).

### Cambios sin efecto simultáneo global (DC)
DONEFIXER podrá activar, desactivar, agregar, retirar o modificar capacidades **sin afectar a todos los clientes simultáneamente**, mediante: feature flags (por tenant, segmento o porcentaje), **configuración versionada** (cada tenant resuelve una versión de configuración; los cambios se publican como nueva versión, no como sobrescritura) y **despliegues progresivos** (canary por cohorte de tenants).

---

## 2. Contexto y fundamento

- El modelo multi-tenant (ADR-001) exige operación por tenant: sin consola, cada cambio comercial (plan, flag, idioma) sería un despliegue o un SQL manual — inaceptable en seguridad y velocidad.
- La matriz de identidad "cuenta → membresías → perfiles → permisos contextuales" (AUD-00 §7) requiere un plano de administración separado del plano de datos de los tenants.
- Los 10 campos de registro convierten cada cambio en evidencia de auditoría (SOC 2 CC7, ISO A.8.15/A.8.16 — aspiracional, doc 38): la consola **es** una fuente de evidencia de cumplimiento, no solo una herramienta.
- Coherente con ADR-009 (API-First): la consola es un cliente más de APIs internas, con privilegios especiales pero sin vías laterales.

## 3. Consecuencias derivadas (obligatorias para la suite)

1. **Separación de planos como PRINCIPIO ARQUITECTÓNICO PERMANENTE (DC, ajuste del Fundador — deja de ser una excepción):**
   > **Principio de Separación de Planos Administrativos:** existen dos planos administrativos arquitectónicamente separados y permanentes: el **Plano Plataforma** (Platform Administration Console, operado por el equipo DONEFIXER: tenants, planes, flags, soporte, consumo, facturación SaaS, gobierno de IA) y el **Plano Tenant** (Tenant Administration, operado por el administrador de cada organización cliente: SUS usuarios, roles, sitios, catálogos — mismo patrón de auditoría, sin visibilidad cross-tenant). Esta separación es un principio permanente de la arquitectura — no una excepción ni una concesión — y se aplica a autenticación, autorización, despliegue, dominio, credenciales, auditoría y entornos. Ninguna evolución del producto podrá fusionar ambos planos; si alguna funcionalidad parece requerirlo, la funcionalidad se rediseña, no el principio. (Referencia: la regla H-06 de "una app configurable por permisos" aplica exclusivamente a aplicaciones orientadas a clientes; el Plano Plataforma no es una aplicación de cliente y queda fuera de su ámbito por definición, no por excepción.)
2. **Admin API interna con independencia total (DC, ampliado por el Fundador):** toda operación de la consola pasa por una Admin API interna que tiene **autenticación, autorización, auditoría, versionado y límites (rate limiting/cuotas) INDEPENDIENTES de la API pública de tenants** — sus propios scopes (`platform:tenants:write`, `platform:flags:write`, etc.), su propio esquema de versionado, sus propios límites y su propio registro de auditoría. Compartir con la API pública únicamente: modelo de dominio y estándares de calidad. Nunca compartir: credenciales, sesiones, límites, tokens ni superficie de exposición. La Admin API no es pública, no se documenta externamente y no está accesible desde aplicaciones de cliente.
3. **Soporte asistido con consentimiento (DC):** el acceso del equipo DONEFIXER a datos de un tenant (soporte) ocurre vía la consola con: motivo registrado, alcance limitado, tiempo limitado, notificación al tenant y registro en la auditoría del propio tenant (visible para el cliente). Sin "modo dios" silencioso.
4. **Configuración versionada (DC):** toda configuración dinámica y formularios/flujos llevan `config_version`; los clientes resuelven por versión fijada; rollback = apuntar a versión anterior (el campo "rollback" del registro referencia el mecanismo concreto usado).
5. **Categorías 4–7 no se ejecutan "desde" la consola:** la consola **dispara y observa** pipelines (CI/CD, migraciones expand/contract, Terraform), no ejecuta despliegues ni migraciones ella misma (segregación de funciones; docs 51/52/61).
6. **Feature flags con ciclo de vida (DC):** cada flag registra dueño, fecha de creación, criterio de retiro; flag sin dueño >6 meses entra en revisión de retiro (evita deuda de flags).
7. **Consumo y FinOps (doc 60):** la consola expone consumo por tenant (almacenamiento, sync, tokens IA, mensajes) — es la fuente operativa del costo unitario y de los límites de plan.
8. **Módulo de gobierno de IA (doc 33):** la consola administra proveedores LLM activos, límites por tenant, opt-out de IA, y revisión de decisiones de agentes — el punto de operación del gobierno de IA.

## 4. Alternativas evaluadas y descartadas

| Alternativa | Por qué se descarta |
|---|---|
| Operación por SQL/scripts manuales | Sin auditoría confiable, alto riesgo humano, incompatible con SOC 2 (aspiracional) |
| Consola = sección de la Web App de tenant | Mezcla planos; el equipo DONEFIXER no debe autenticarse como usuario de tenant; superficie de ataque compartida |
| Herramienta de terceros (admin genérico/retool) | Dependencia crítica con acceso a todo el sistema; el plano de administración es demasiado sensible para tercerizar (misma lógica que AUD-00 aplicó al sync, pero aquí construir SÍ está justificado: es un CRUD interno bien acotado) |
| Flags con herramienta SaaS externa en Fase 1 | Aplazable: Fase 1 usa flags en base de datos propia; SaaS de flags solo si el volumen de experimentación lo justifica (PD-AC-2) |

### 3.9 Régimen de acciones críticas por etapa (DC, ajuste del Fundador)

**Fase 0–1 (equipo unipersonal):** toda acción crítica requiere obligatoriamente:
1. **MFA** activo en la cuenta de plataforma;
2. **Reautenticación** (step-up) en el momento de la acción;
3. **Motivo obligatorio** registrado (sin motivo, no hay acción);
4. **Registro inmutable** (los 10 campos de §1);
5. **Confirmación explícita** (pantalla de confirmación con resumen del alcance e impacto; confirmación diferida para las de mayor riesgo);
6. **Rollback cuando sea posible** (toda acción crítica declara su mecanismo de rollback antes de ejecutarse; si no existe rollback, la acción requiere confirmación adicional y backup previo verificado).

**Activación de aprobación dual (DC):** cuando exista un **segundo administrador autorizado**, se activa la aprobación dual humana para operaciones críticas (matriz §5). Hasta entonces, la dual se sustituye por el régimen Fase 0–1 anterior. La transición se registra en la auditoría de la consola.

## 5. Matriz inicial de acciones críticas (a refinar en docs 26/34)

| Acción | Categoría | Reauth | Aprobación dual |
|---|---|---|---|
| Cambiar plan/entitlements de un tenant | 1–2 | Sí | Sí (facturación) |
| Activar feature flag a 1 tenant | 2 | Sí | No |
| Rollout progresivo a cohorte | 2–4 | Sí | Sí si >10% de tenants |
| Publicar nueva versión de configuración | 3 | Sí | No |
| Acceder a datos de un tenant (soporte) | — | Sí | Sí + notificación al tenant |
| Ejecutar/observar migración de datos | 6 | Sí | Sí |
| Cambio de infraestructura | 7 | Sí | Sí |
| Rotar secretos | 7 | Sí | Sí (vía pipeline, nunca valor visible) |
| Suspender tenant | 1 | Sí | Sí |

## 6. Decisiones pendientes (PD) y supuestos (SU) — actualizado con ajustes del Fundador

- PD-AC-1: ¿Consola como app separada desde Fase 1 o sección aislada con dominio propio? (Recomendación auditoría: separada desde el inicio — coherente con el principio de separación de planos; pendiente de confirmación).
- ~~PD-AC-2~~ → **SU-FLAGS (ajuste del Fundador):** la implementación de Feature Flags propios permanece como **SU (supuesto)** hasta finalizar el análisis de FinOps, observabilidad y costos operativos (docs 60, 54, 61). No es decisión: el análisis puede recomendar flags propios, servicio externo o híbrido.
- ~~PD-AC-3~~ → **PD-RETENCIÓN (ajuste del Fundador):** la retención de auditorías (consola y plataforma) permanece **PD** hasta definir la política legal oficial (doc 37, vinculada a N-3/N-7). Toda cifra de años mencionada hasta entonces es SU, no compromiso.
- ~~PD-AC-4~~ → **RESUELTA (DC por el Fundador, §3.9):** Fase 0–1 con régimen MFA+reauth+motivo+registro+confirmación+rollback; dual humana al existir segundo administrador autorizado.

## 7. Referencias cruzadas
Coherente con: ADR-001 (multi-tenant), ADR-009 (API-First), ADR-011 (multicanal; excepción documentada a H-06), AUD-00 (threat model: insider threat, escalación de privilegios). Obliga a: 19 (roles — roles de plataforma), 22 (consola web), 26 (IAM: step-up, dual), 34/35 (seguridad/threat), 46 (audit model), 51/52 (CI/CD, IaC: la consola observa, no ejecuta), 60 (FinOps), 61 (release progresivo), doc 43 spec "Administración de plataforma".

## 8. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Decisión confirmada por el Fundador: consola de plataforma protegida y auditada; 7 categorías de cambio; 10 campos de registro; controles críticos; cambios sin efecto global simultáneo |
| 1.1 | 2026-07-29 | **APROBADO CON AJUSTES por el Fundador:** separación de planos elevada a principio arquitectónico permanente (§3.1); Admin API con autenticación/autorización/auditoría/versionado/límites independientes (§3.2); régimen de acciones críticas Fase 0–1 (§3.9); aprobación dual condicionada a segundo administrador; retención de auditorías → PD; feature flags propios → SU |
