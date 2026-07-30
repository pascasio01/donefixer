# 10 · Manual UX/UI (resumen operativo)

> Design Artifact PRE-GO — No reutilizable como código de producción sin autorización posterior.
> Entregable WP-UX-ART · subordinado a DC-13 (Fase 1) y DC-14 (EGM) · fuente normativa: Doc 40 (Design System), Docs 11/12 (RF/RNF).

## Principios
1. **La sincronización es identidad de producto**: nada parece definitivo hasta el veredicto del servidor. Provisional ≠ error; es un estado normal visible.
2. **Offline no es un modo, es el escenario base**: el técnico nunca pierde trabajo ni se bloquea (J-2).
3. **La IA siempre se identifica**: etiqueta ✦, fuentes citadas, recomendación de verificación; nunca ejecuta acciones de negocio por sí sola; offline se degrada sin bloquear.
4. **Sin callejones sin salida**: todo estado de error, permiso o conflicto ofrece la siguiente acción.
5. **Motion comunica estado**: única animación en loop permitida = skeleton de carga (>300ms). `prefers-reduced-motion` respeta al usuario.
6. **Tokens semánticos o nada**: prohibido valor crudo de color/espaciado en componentes; facilita el rebrand cuando se cierre la paleta (SU).

## Handoff PRE-GO
Este material es **referencia visual y de comportamiento**, no código de producción. Tras el GO (Doc 70) y las decisiones ADR-013/ADR-014, los flujos y estados aquí validados se implementan en el stack definitivo; los hex actuales se sustituyen por la paleta de marca sin tocar componentes (solo tokens).
