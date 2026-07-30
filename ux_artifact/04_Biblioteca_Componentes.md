# 04 · Biblioteca de componentes (Doc 40 → CSS)

> Design Artifact PRE-GO — No reutilizable como código de producción sin autorización posterior.
> Entregable WP-UX-ART · subordinado a DC-13 (Fase 1) y DC-14 (EGM) · fuente normativa: Doc 40 (Design System), Docs 11/12 (RF/RNF).

Cada componente del prototipo es la traducción visual de un componente DS. Ninguno contiene lógica.

| Componente DS | Clase CSS | Pantallas |
|---|---|---|
| App shell / Topbar | `.app-shell`, `.topbar` | todas |
| Indicador de conectividad (DS-8.1) | `.connectivity.{offline,pending}` | P-05…P-09, P-11, P-12 |
| Card / KPI | `.card`, `.kpi`, `.kpi-row` | P-05, P-12 |
| Botón ≥44pt (DS-3) | `.btn.{secondary,danger,block}` | todas |
| Badge / SyncBadge (DS-8.2) | `.badge`, `.sync-badge.{confirmed,provisional,conflict}` | P-05…P-11 |
| Fila de lista | `.list-row` | P-05, P-06, P-08…P-12 |
| Campo de formulario | `.field` | P-02…P-04, P-11 |
| Chips de filtro | `.chips`, `.chip` | P-06 |
| Checklist + checkbox | `.checklist-item`, `.checkbox.done` | P-07, P-14 |
| Tabs | `.tabs`, `.tab` | P-07 |
| Toast de estado sync | `.toast` | P-07 |
| Empty state (DS-7) | `.empty-state` | P-06, P-15 |
| Skeleton >300ms (DS-7) | `.skeleton` | P-15 |
| Área de firma | `.signature-pad` | P-07 |
| Grid de evidencias con sync badge | `.evidence-grid` | P-07 |
| Tarjeta IA siempre identificada | `.ai-card`, `.ai-label`, `.cite` | P-05, P-13 |
| Navegación inferior S <640px (DS-3) | `.bottom-nav` (5 destinos: Hoy/Órdenes/Escanear/Avisos/Más) | P-05…P-09, P-11…P-14 |
| Banner del artefacto (obligatorio) | `.artifact-banner` | todas |
| Comparación de conflicto (DS-8.4) | `.conflict-compare` | P-10 |
| OTP | `.otp` | P-03 |
