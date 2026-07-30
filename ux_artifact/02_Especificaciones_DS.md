# 02 · Especificaciones del Design System aplicadas

> Design Artifact PRE-GO — No reutilizable como código de producción sin autorización posterior.
> Entregable WP-UX-ART · subordinado a DC-13 (Fase 1) y DC-14 (EGM) · fuente normativa: Doc 40 (Design System), Docs 11/12 (RF/RNF).

Las pantallas del prototipo usan **únicamente tokens semánticos del Doc 40**, traducidos a CSS custom properties en `app/assets/tokens.css` y `components.css`. No se ha inventado ningún token.

## 1. Color (semántico, nunca valores crudos en componentes)
| Token | Uso |
|---|---|
| `color.surface.{base,raised,sunken}` | fondos, tarjetas, zonas hundidas |
| `color.text.{primary,secondary,inverse}` | tipografía |
| `color.action.{primary,primary-hover,danger}` | botones y acciones |
| `color.status.{success,warning,error,info}` | badges y alertas |
| **`color.sync.{confirmed,provisional,conflict}`** | **token exclusivo DONEFIXER (DS-8)**: estado de sincronización |

Paleta concreta: **SU — pendiente de identidad de marca (Doc 40 §7)**. Los valores hex actuales son placeholders interinos que cumplen contraste WCAG 2.2 AA (4.5:1 texto, 3:1 UI).

## 2. Espaciado
Escala 4pt: `space-1…space-10` (4–40px). Todo margen/padding del prototipo es múltiplo de 4px.

## 3. Tipografía
Familia system-ui (placeholder hasta identidad de marca). Escala: 12/14/16/20/28px (`text-xs…text-xl`). Cuerpo base 16px, line-height 1.45.

## 4. Iconografía
Placeholder tipográfico (⌂ ▤ ◉ ♪ ⋯ ✦). El set definitivo es SU pendiente de identidad de marca; la regla DS se respeta: icono siempre acompañado de texto en indicadores críticos (conectividad, sync).

## 5. Motion (comunicar estado, nunca decorar)
| Token | Valor | Uso |
|---|---|---|
| `motion-fast` | 120ms | hover/press |
| `motion-base` | 200ms | transiciones de estado |
| easing | cubic-bezier(.2,.8,.2,1) | estándar |
| skeleton | 1.2s shimmer | único loop permitido, solo si carga >300ms |

`prefers-reduced-motion: reduce` desactiva toda animación (verificado en tokens.css).

## 6. Accesibilidad (WCAG 2.2 AA)
- Foco visible: `--focus-ring` (halo 3px) en `:focus-visible`, nunca `outline:none` sin sustituto.
- Targets táctiles ≥44pt en botones, chips y bottom-nav (DS-3).
- Tema oscuro vía `prefers-color-scheme` + override manual `[data-theme]`.
