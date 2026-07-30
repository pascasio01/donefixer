# 09 · Fichas de validación por pantalla

> Design Artifact PRE-GO — No reutilizable como código de producción sin autorización posterior.
> Entregable WP-UX-ART · subordinado a DC-13 (Fase 1) y DC-14 (EGM) · fuente normativa: Doc 40 (Design System), Docs 11/12 (RF/RNF).

Una ficha por pantalla del prototipo (15). Campos obligatorios según Master Prompt UX-ART.

### P-01 · Splash / Entrada — `index.html`
| Campo | Contenido |
|---|---|
| Objetivo | Puerta de entrada al prototipo |
| Usuario | Todos |
| Flujo | — |
| RF | RF-PLT-001 |
| RNF | RNF-USR (claridad) |
| Componentes DS | btn, splash |
| Estados UX | — |
| Riesgos UX | Confundir con app real → banner permanente |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Identidad provisional (paleta SU) |

### P-02 · Inicio de sesión — `login.html`
| Campo | Contenido |
|---|---|
| Objetivo | Acceso con organización + credenciales |
| Usuario | Todos |
| Flujo | UF-0 |
| RF | RF-PLT-002, RF-USR-001 |
| RNF | RNF-SEC |
| Componentes DS | field, btn, card, error L2 |
| Estados UX | Error L2 |
| Riesgos UX | Enumeración de usuarios → mensajes genéricos |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Sin autenticación funcional |

### P-03 · MFA — `mfa.html`
| Campo | Contenido |
|---|---|
| Objetivo | Segundo factor OTP 6 dígitos |
| Usuario | Todos |
| Flujo | UF-0 |
| RF | RF-PLT-002 |
| RNF | RNF-SEC |
| Componentes DS | otp, btn |
| Estados UX | — |
| Riesgos UX | Reenvío sin límite visual |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Targets ≥44pt |

### P-04 · Recuperar acceso — `recuperar.html`
| Campo | Contenido |
|---|---|
| Objetivo | Reset de contraseña |
| Usuario | Todos |
| Flujo | UF-0 |
| RF | RF-PLT-002 |
| RNF | RNF-SEC anti-enumeración |
| Componentes DS | field, card |
| Estados UX | Mensaje neutral |
| Riesgos UX | Enumeración → mensaje idéntico siempre |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Cumple anti-enumeración |

### P-05 · Dashboard técnico (Hoy) — `dashboard.html`
| Campo | Contenido |
|---|---|
| Objetivo | Qué tengo hoy y su estado de sync |
| Usuario | Técnico |
| Flujo | UF-1 |
| RF | RF-WO-001 |
| RNF | RNF-PERF (J-2) |
| Componentes DS | kpi, list-row, sync-badge, connectivity, ai-card |
| Estados UX | Loading skeleton, Empty |
| Riesgos UX | IA sin identificar → .ai-label + .cite obligatorios |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Corazón del flujo J-2 |

### P-06 · Lista de OT — `ordenes.html`
| Campo | Contenido |
|---|---|
| Objetivo | Filtrar y priorizar órdenes |
| Usuario | Técnico |
| Flujo | UF-1/UF-2 |
| RF | RF-WO-001/002 |
| RNF | RNF-PERF |
| Componentes DS | chips, list-row, sync-badge, empty-state |
| Estados UX | Empty explicado |
| Riesgos UX | Filtros sin resultado → empty con salida |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Estado conflict visible |

### P-07 · Detalle de OT — `orden.html`
| Campo | Contenido |
|---|---|
| Objetivo | Ejecutar la OT: checklist, materiales, evidencias, firma, cierre |
| Usuario | Técnico |
| Flujo | UF-1 (J-2 núcleo) |
| RF | RF-WO-003/004/005 |
| RNF | RNF-PERF, RNF-SEC (firma) |
| Componentes DS | tabs, checklist, evidence-grid, signature-pad, toast |
| Estados UX | Provisional en cierre |
| Riesgos UX | Cierre parece definitivo → botón dice «provisional hasta veredicto» |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Autosave >30s (DS-8.5) representado con toast |

### P-08 · Offline y cola de sync — `offline.html`
| Campo | Contenido |
|---|---|
| Objetivo | Trabajar sin red y entender qué está pendiente |
| Usuario | Técnico |
| Flujo | UF-1 (modo avión) |
| RF | RF-SYNC-001/005 |
| RNF | RNF-REL |
| Componentes DS | connectivity.offline, list-row, alerta |
| Estados UX | Offline persistente |
| Riesgos UX | Usuario duda si su trabajo se perdió → mensaje explícito |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; IA degradada declarada (DS-8.6) |

### P-09 · Avisos — `avisos.html`
| Campo | Contenido |
|---|---|
| Objetivo | Atender rechazos/ajustes del servidor |
| Usuario | Técnico |
| Flujo | UF-3 |
| RF | RF-WO-006 |
| RNF | — |
| Componentes DS | list-row, sync-badge |
| Estados UX | «Requiere tu atención» |
| Riesgos UX | REJECT sin contexto → cada aviso explica motivo y lleva a acción |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; DS-8.3 verbatim |

### P-10 · Resolución de conflicto — `conflicto.html`
| Campo | Contenido |
|---|---|
| Objetivo | Comparar versiones y decidir sin perder datos |
| Usuario | Técnico |
| Flujo | UF-3 |
| RF | RF-SYNC-004 |
| RNF | — |
| Componentes DS | conflict-compare (mine/server), btn |
| Estados UX | Conflicto |
| Riesgos UX | Decisión a ciegas → lado a lado con contexto temporal |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; DS-8.4, sin dead-end |

### P-11 · Activos — `activos.html`
| Campo | Contenido |
|---|---|
| Objetivo | Consultar activo e historial |
| Usuario | Técnico/Supervisor |
| Flujo | UF-4 |
| RF | RF-AST-001/002 |
| RNF | RNF-PERF |
| Componentes DS | field búsqueda, list-row, badge |
| Estados UX | — |
| Riesgos UX | Historial sin estado sync → badges en cada OT |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Entrada por QR (Escanear) |

### P-12 · Preventivos — `preventivos.html`
| Campo | Contenido |
|---|---|
| Objetivo | Planes, próximas ejecuciones |
| Usuario | Supervisor/Planner |
| Flujo | UF-4 |
| RF | RF-PM-001/002 |
| RNF | — |
| Componentes DS | kpi, list-row |
| Estados UX | Empty |
| Riesgos UX | Vencimientos sin prioridad visual → badge «Próximo» |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Generación automática de OT mencionada |

### P-13 · Asistente IA — `ia.html`
| Campo | Contenido |
|---|---|
| Objetivo | Sugerencias con fuentes citadas |
| Usuario | Técnico/Supervisor |
| Flujo | UF-5 |
| RF | RNF-AI-001 (cita de fuentes), RNF-AI-003 |
| RNF | RNF-IA (PD-IA-1) |
| Componentes DS | ai-card, ai-label, cite, alerta offline |
| Estados UX | Offline IA |
| Riesgos UX | Confianza ciega → fuentes + «verifica antes de actuar» |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; IA nunca cierra OT ni consume stock |

### P-14 · Configuración — `configuracion.html`
| Campo | Contenido |
|---|---|
| Objetivo | Cuenta, preferencias, sync, sesión |
| Usuario | Todos |
| Flujo | UF-0 |
| RF | RF-PLT-003 |
| RNF | — |
| Componentes DS | checklist toggle, card, btn danger |
| Estados UX | — |
| Riesgos UX | Preferencias de accesibilidad ausentes → reduced-motion visible |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Enlace a cola de sync |

### P-15 · Catálogo de estados — `estados.html`
| Campo | Contenido |
|---|---|
| Objetivo | Referencia viva DS-7/DS-8 |
| Usuario | Equipo (interno) |
| Flujo | — |
| RF | — |
| RNF | RNF-ACC (WCAG 2.2 AA) |
| Componentes DS | skeleton, empty-state, errores L1-L3, permission, offline |
| Estados UX | todos |
| Riesgos UX | Inconsistencia entre pantallas → fuente única |
| Criterios de validación | Banner PRE-GO presente; tokens semánticos; contraste AA; Obligatoria en revisión de handoff |
