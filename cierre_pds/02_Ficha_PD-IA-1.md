> Expediente de cierre de PDs bloqueantes (G-0 del Doc 70). Material preparado; la decisión y la evidencia externa corresponden al Fundador. Subordinado a DC-01…DC-15. Nada de esto autoriza código de producción.

# 02 · Ficha de decisión — PD-IA-1 (proveedor LLM del gateway)

**Qué decide:** proveedor(es) iniciales detrás del gateway multi-modelo de IA.
**Lo que NO decide:** ADR-007 ya fija el gateway con routing por costo y dominio desacoplado del proveedor — la decisión es reversible por diseño.

## Criterios del corpus que aplican
- ADR-007: sustitución de proveedor sin tocar dominio → mínimo 1 proveedor compatible con el contrato del gateway.
- Doc 33 (P-33-1…7): prohibiciones IA (sin acciones de negocio, cita de fuentes o abstención — RNF-AI-001/003).
- RNF-AI-004: coste por tenant/mes visible con límite → el proveedor debe permitir medición y topes.
- Doc 03 (Business Model): coste de IA dentro del margen del plan.
- UX artifact (P-13): IA siempre identificada, degradación offline no bloqueante — requisito de diseño, no del proveedor.

## Opciones (parametrizadas)
| Opción | Encaje | Riesgo principal |
|---|---|---|
| A — Proveedor frontera único (p. ej. OpenAI/Anthropic/Google) | Calidad máxima, setup mínimo | Dependencia inicial; coste por token |
| B — Gateway con 2 proveedores (primario + fallback) | Cumple routing por costo desde el día 1; resiliencia | Doble contrato/facturación |
| C — Modelo abierto auto-alojado | Control total de datos | Coste operativo y de GPUs; madurez de funciones |

## Datos que debe adjuntar la decisión
Precio por 1M tokens (entrada/salida), límites de tasa, residencia de datos (RGPD), política de entrenamiento con datos del cliente, estimación de coste por tenant/mes frente al límite RNF-AI-004.

## Formato de cierre
Entrada en ADI (o ADR complementario a ADR-007) + Índice Maestro; actualizar `sprint0_repo/infra/env/.env.template` con claves del proveedor elegido. Decisión del Fundador → registrar como **DC** nueva.
