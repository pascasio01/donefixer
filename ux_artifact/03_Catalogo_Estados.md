# 03 · Catálogo de estados UX (DS-7/DS-8)

> Design Artifact PRE-GO — No reutilizable como código de producción sin autorización posterior.
> Entregable WP-UX-ART · subordinado a DC-13 (Fase 1) y DC-14 (EGM) · fuente normativa: Doc 40 (Design System), Docs 11/12 (RF/RNF).

Implementación visual en `app/estados.html` (P-15), referencia viva obligatoria para todas las pantallas.

## Estados de carga y contenido (DS-7)
| Estado | Regla | Ejemplo en prototipo |
|---|---|---|
| Loading | Skeleton solo si la espera >300ms; nunca spinner indefinido | P-15 |
| Empty | Explica qué está vacío y qué puede hacer el usuario | P-06, P-15 |
| Error L1 | Informativo, datos locales disponibles | P-15 |
| Error L2 | Accionable (credenciales, sesión) | P-02, P-15 |
| Error L3 | Bloqueante con reintento/soporte | P-15 |
| Permission | Nunca callejón sin salida: ofrece alternativa | P-15 |

## Estados de sincronización (DS-8) — identidad DONEFIXER
| Estado | Token | Regla |
|---|---|---|
| En línea / Sin conexión / Pendientes | `connectivity.*` | Indicador persistente icono+texto en topbar (DS-8.1) |
| Confirmada | `color.sync.confirmed` | Veredicto accept del servidor |
| Provisional | `color.sync.provisional` | Persistencia local sin veredicto; el cierre de OT queda provisional (DS-8.2) |
| Conflicto | `color.sync.conflict` | REJECT → «Requiere tu atención» en Avisos (DS-8.3) → comparación lado a lado (DS-8.4) en P-10 |
| Ajustado | provisional + aviso | ADJUST siempre explica el motivo (DS-8.3) |
| IA offline | — | La IA se degrada sin bloquear el resto (DS-8.6); autosave local >30s (DS-8.5) |
