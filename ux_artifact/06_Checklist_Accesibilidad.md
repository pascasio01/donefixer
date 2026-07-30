# 06 · Checklist de accesibilidad (WCAG 2.2 AA)

> Design Artifact PRE-GO — No reutilizable como código de producción sin autorización posterior.
> Entregable WP-UX-ART · subordinado a DC-13 (Fase 1) y DC-14 (EGM) · fuente normativa: Doc 40 (Design System), Docs 11/12 (RF/RNF).

- [x] Contraste ≥4.5:1 en texto y ≥3:1 en componentes (paleta interina verificada).
- [x] Foco visible con token `--focus-ring` en `:focus-visible`.
- [x] Targets táctiles ≥44pt (btn, chip, bottom-nav, otp).
- [x] Indicadores críticos con icono + texto, nunca solo color (conectividad, sync).
- [x] `prefers-reduced-motion` desactiva animaciones.
- [x] `prefers-color-scheme` con tema oscuro + override manual.
- [x] `lang="es"` y roles ARIA en alertas/estados (`role="alert"`, `role="status"`).
