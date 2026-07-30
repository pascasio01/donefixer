> Registro de incidente — WP-UX-ART. Documento de evidencia, no de gobernanza.

# 13 · Registro de incidente — Preview Platform Rendering Failure — External to WP-UX-ART

## Clasificación
**Preview Platform Rendering Failure — External to WP-UX-ART.** El defecto se localiza en el servicio de visualización de la plataforma, no en el artefacto. El Work Package permanece cerrado; no se modificará el prototipo salvo nueva evidencia técnica que demuestre un defecto en los archivos.

## Evidencia conservada

> Nota de atribución (precisión del Fundador): todos los resultados técnicos listados son **salidas de las verificaciones automáticas del proyecto**, no inspección directa del Fundador. La evidencia describe lo reportado por los verificadores; la inspección humana independiente queda pendiente de la revisión del Gate.
| Ítem | Valor |
|---|---|
| Versión de referencia | **eb63bf6** (instantánea guardada tras la reparación de navegabilidad) |
| Fecha/hora de la prueba | 2026-07-29 23:27 UTC |
| Motor de renderizado usado | Chromium headless (mismo navegador del entorno), `file://` directo sobre los archivos de la instantánea |
| Capturas del renderizado (generadas por el agente, no inspeccionadas por el Fundador) | `evidencia_preview/render_real_index.png` (splash P-01) · `evidencia_preview/render_real_dashboard.png` (dashboard P-05) — render correcto con tokens, componentes, bottom-nav y banner |
| CSS (resultado de la verificación automática del proyecto) | llaves balanceadas 82/82; 0 rutas absolutas |
| Enlaces (resultado de la verificación automática del proyecto) | 13/13 destinos existen; 15/15 pantallas alcanzables desde `index.html` (BFS) |
| Verificaciones automáticas | `verificacion_preview.py` TODO PASS · `verificacion_ux.py` 7/7 PASS |
| Síntoma en plataforma | Pantalla en blanco en Preview pese a instantánea correcta |

## Protocolo de verificación acordado (para el Fundador)
1. Abrir exclusivamente la versión **eb63bf6**.
2. Recarga completa del Preview.
3. Esperar unos minutos si la plataforma tarda en procesar la instantánea.
4. No generar nuevas versiones (añade ruido sobre qué snapshot se está probando).

## Criterio de reapertura
Solo si aparece evidencia técnica nueva que demuestre un defecto en los archivos (p. ej. captura del renderizado fallido *de los propios archivos*, o consola con error atribuible al HTML/CSS). En ausencia de ella, el incidente queda archivado como externo.
