> Expediente de cierre de PDs bloqueantes (G-0 del Doc 70). Material preparado; la decisión y la evidencia externa corresponden al Fundador. Subordinado a DC-01…DC-15. Nada de esto autoriza código de producción.

# 03 · Ficha de decisión — PD-4 (idiomas de lanzamiento)

**Qué decide:** idiomas soportados en el lanzamiento (vinculada a N-6).
**Impacto:** Doc 11 (RF-I18N), glosario Doc 13 (terminología canónica por idioma), UX artifact (longitudes de texto), plan de testing (casos i18n).

## Criterios del corpus que aplican
- RF-I18N (familia existente en Doc 11): la plataforma ya exige arquitectura i18n; PD-4 fija solo el *alcance de lanzamiento*.
- Doc 01/03: mercados objetivo y países piloto (PD-3 relacionada, no bloqueante de G-0).
- Doc 13: el glosario es la fuente de verdad terminológica — cada idioma añadido requiere su mapeo canónico.

## Opciones
| Opción | Encaje | Riesgo principal |
|---|---|---|
| A — Solo español en lanzamiento | Mínimo alcance; pilotos hispanohablantes | Re-traducción temprana si el piloto exige EN/PT |
| B — Español + inglés | Cobertura LatAm + mercado global | Esfuerzo de QA i18n desde el inicio |
| C — Español + inglés + portugués | Cobertura LatAm completa | Máximo esfuerzo previo al lanzamiento |

## Formato de cierre
Actualizar Doc 11 (alcance de RF-I18N), Doc 13 (glosario por idioma), Registry; reflejar en `fase1_plan` (casos de test i18n). Decisión del Fundador → registrar como **DC** nueva o como resolución de N-6 según el alcance final.
