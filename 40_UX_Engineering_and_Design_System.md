# 40 — UX Engineering & Design System Specification

| Campo | Valor |
|---|---|
| Documento | 40_UX_Engineering_and_Design_System |
| Versión | 1.0 (borrador para aprobación) |
| Estado | Pendiente de aprobación del Fundador |
| Precedencia | Doc 10 (SRS) §Precedencia documental |
| Trazabilidad ascendente | Docs 18 (IA), 15 (Personas), 16 (Journeys), 22 (WA-6/WA-9), 23 (MA-6/MA-8), 12 (RNF-ACC, RNF-USE), ADR-011 v1.1, ADR-012 (branding por tenant) |

> **Convención de evidencia:** DC · SU · PD. Este documento define *contratos de experiencia*; no incluye valores visuales finales de marca (paleta, logotipo), que dependen de identidad de marca — registrada como SU con proceso de definición (N-5 marca).

---

## 1. Propósito y alcance

Especifica el sistema de diseño y las reglas de ingeniería de experiencia de DONEFIXER para los tres canales (Web App, PWA, app nativa), garantizando: consistencia multi-canal (ADR-011 paridad controlada), usabilidad frontline (RNF-USE-001…005), accesibilidad (RNF-ACC-001…004), theming por tenant (ADR-012), y UX de estados offline/provisionales (Doc 27, Doc 16 flujos OFF). (DC)

---

## 2. Design Tokens canónicos (DS-1)

Los tokens son la **única fuente de valores visuales** (color, espaciado, tipografía, radios, elevación, duraciones). Un solo paquete versionado de tokens alimenta web (CSS custom properties / Tailwind theme) y móvil (constantes del framework elegido, N-1 PD). (DC — WA-6, MA §riesgo deriva visual)

| Capa | Contenido | Regla |
|---|---|---|
| Tokens primitivos | Escala de color neutra + rampas semánticas, escala tipográfica modular, escala de espaciado base-4, radios, sombras | Inmutables salvo release de sistema |
| Tokens semánticos | `color.surface.default`, `color.text.primary`, `color.action.primary`, `color.status.{success,warning,danger,info}`, `color.sync.{confirmed,provisional,conflict}` | Los componentes solo consumen tokens semánticos |
| Tokens de tenant | Subconjunto sobreescribible (primario, logo, densidad) vía Consola/Configuración | ADR-012 branding; nunca rompe contraste AA (validación automática, §7) |

**Token semántico exclusivo de DONEFIXER:** `color.sync.*` — el estado de sincronización (confirmado / provisional / en conflicto) es una categoría visual de primera clase, no un adorno (RNF-USE-004: estado del sistema siempre visible). (DC)

## 3. Component Library (DS-2)

Biblioteca única web (sobre headless accesible, WA-6) + catálogo de equivalencias para el framework móvil (N-1 PD: la especificación es agnóstica). Jerarquía: **primitivos** (Button, Input, Select, Checkbox, Dialog, Toast, Tooltip, Tabs) → **compuestos** (DataTable virtualizada, FormField con validación, SearchBar, FilterChip, EmptyState, SyncBadge, EvidenceCapture, AssetTree, SignaturePad) → **patrones de página** (List+Detail, Kanban planificador, Form wizard). (DC)

Cada componente se especifica con: anatomía, estados (§6–§9), props, tokens consumidos, comportamiento de teclado/lector de pantalla, y pruebas obligatorias (WA-10). Componentes de campo (EvidenceCapture, SignaturePad, AssetTree) deben funcionar sobre réplica local sin red (MA-4/MA-5). (DC)

## 4. Responsive Design Rules (DS-3)

| Breakpoint | Rango | Uso principal | Reglas |
|---|---|---|---|
| S (móvil) | <640px | App nativa/PWA técnico | Una columna; barra inferior [Hoy][Órdenes][Escanear][Avisos][Más] (Doc 18); targets ≥44pt (RNF-ACC-002); gestos con guantes (RNF-USE-003) |
| M (tablet) | 640–1024px | Supervisor de planta | Dos columnas colapsables; navegación lateral mini |
| L (desktop) | >1024px | Web App administración | Layout con sidebar; DataTable con densidad configurable; atajos de teclado |

Contenido y funcionalidad nunca desaparecen por breakpoint — se reordenan (paridad controlada ADR-011). (DC)

## 5. Motion Guidelines (DS-4)

- Duraciones: micro 100–150 ms, transiciones de vista 200–300 ms, jamás bloqueantes. (SU, calibrar en pilotos)
- Propósito únicamente funcional: confirmar acción, indicar origen/destino de navegación, mostrar cambio de estado de sync.
- `prefers-reduced-motion` respetado en 100% de animaciones (RNF-ACC). (DC)
- Prohibido: animaciones decorativas en flujos del técnico; parallax; autoplay. (DC)

## 6. Accessibility Rules (DS-5) — WCAG 2.2 AA interno (RNF-ACC-001)

| Regla | Detalle | Verificación |
|---|---|---|
| Contraste | ≥4.5:1 texto, ≥3:1 UI/gráficos — incluido tema del tenant (validación en Configuración antes de guardar) | axe CI + validador de tokens |
| Teclado | Todo operable; foco visible con token `color.focus.ring`; orden lógico | Test E2E teclado |
| Lectores de pantalla | Roles/labels ARIA correctos; VoiceOver/TalkBack en flujos críticos J-1/J-2 | RNF-ACC-003 |
| Dinámica | Dynamic Type / zoom 200% sin pérdida | RNF-ACC-002 |
| Errores | Sin códigos crípticos; mensaje + acción sugerida (RNF-ACC-004) | §8 |
| Gates | axe sin violaciones críticas en CI (Doc 47 §Accessibility Gates) | DC |

## 7. Dark / Light Theme (DS-6)

Dos temas completos definidos exclusivamente por tokens semánticos; el modo oscuro no es inversión automática sino rampa diseñada. Preferencia por usuario + detección de SO; el tema del tenant solo puede sobreescribir tokens que mantengan contraste AA en **ambos** temas (validador obligatorio). Uso de campo bajo sol directo: tema claro de alto contraste como opción explícita del técnico (P-T1). (DC; paleta final de marca: SU pendiente de identidad)

## 8. Estados de la experiencia (DS-7) — catálogo normativo

| Estado | Regla de diseño | Trazabilidad |
|---|---|---|
| **Loading** | Skeleton con forma del contenido real (no spinners aislados) para >300 ms; botones con estado de progreso inline; nunca bloquear la navegación por carga secundaria | RNF-USE-004 |
| **Empty** | Todo vacío explica: qué es esto, por qué está vacío, acción primaria para llenarlo. Prohibido "No hay datos" a secas | RNF-ACC-004; J-7 onboarding |
| **Error** | Tres niveles: (a) campo (inline, cómo corregir), (b) operación (toast/inline con reintentar), (c) sistema (pantalla con estado + soporte). Siempre qué pasó + qué hacer + si el dato está a salvo | RNF-ACC-004 |
| **Permission** | Función sin permiso: oculta en navegación (Doc 19 §12) pero con pantalla informativa si se llega por enlace directo ("tu rol no incluye…", contacto del admin). Nunca dead-end | Doc 19; RNF-USE |
| **Offline** | Ver §9 | RNF-USE-004 |

## 9. Offline UX Guidelines (DS-8) — la firma de DONEFIXER

1. **Indicador persistente de conectividad y sync** en shell (icono + texto, no solo color): `Sincronizado` / `Sin conexión — trabajando local` / `N cambios pendientes`. (DC — RNF-USE-004)
2. **Estado provisional visible:** todo dato creado/modificado offline lleva `SyncBadge` provisional (token `color.sync.provisional`) hasta veredicto del servidor. (DC — ADR-011 regla de autoridad; Doc 27 SY-9)
3. **Veredictos visibles y explicables:** ACCEPT elimina el badge; ADJUST muestra qué cambió el servidor y por qué; REJECT va a bandeja "Requiere tu atención" con explicación en lenguaje claro y acción disponible (corregir/reasignar/escalar). Nada desaparece en silencio. (DC — Doc 16 J-2 flujos OFF; RNF-SYNC-005)
4. **Conflictos a humano:** UI de resolución lado a lado (mi versión / versión del servidor) para la cola de conflictos; prohibido LWW silencioso. (DC — Doc 14 matriz)
5. **IA sin conexión:** mensaje sin fricción ("las sugerencias IA se generarán al sincronizar"); el flujo nunca se bloquea por ausencia de IA. (DC — AIA-8, RNF-AI-005)
6. **Captura protegida:** autosave en toda captura >30 s (RNF-USE-005); evidencias con indicador de subida pendiente reanudable (MA-4). (DC)

## 10. Internacionalización UX (DS-9)

Etiquetado 100% desde catálogo anclado al Glosario (Doc 13); diseño tolerante a expansión de texto (+30%); formatos por locale; idiomas PD-4 (la especificación no asume conjunto). (DC — WA-7, RF-I18N-001)

## 11. Alternativas evaluadas

| Alternativa | Razón de descarte | Evidencia |
|---|---|---|
| **Sistema propio sobre headless + tokens (elegida)** | — | DC |
| Librería cerrada (MUI/AntD) | White-label por tenant y tokens de sync propios quedan forzados | DC (WA-6) |
| Diseño por canal independiente | Deriva visual web/móvil; viola paridad controlada | DC |
| Motion rico/micro-interacciones decorativas | Contra RNF-USE/PERF y contexto de campo | DC |

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Deriva web↔móvil al resolver N-1 | Tokens como paquete único; catálogo de equivalencias (DS-2); revisión de paridad en Doc 70 |
| Theming de tenant rompe accesibilidad | Validador de contraste obligatorio antes de guardar (DS-6/DS-7) |
| Complejidad de la UX de veredictos | Probar con técnicos reales en pilotos (P-T1 escenarios) |

## 13. Criterios de aceptación del documento

1. Cubre los 11 elementos de la ampliación obligatoria del Fundador. ✅
2. Agnóstico de framework móvil (N-1 abierta). ✅
3. Trazado a RNF-ACC/USE/SYNC y ADR-011/012. ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación (Ola 4, documento 1 de 8) con las 11 ampliaciones obligatorias incorporadas.*
