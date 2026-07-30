# Plantilla — Matriz de decisión oficial N-2 (Entregable 6, DC-02)

Escala 1–5. **Puntuación sin evidencia = inválida.** Cada celda exige: evidencia + métrica + justificación + referencia a prueba.

| Criterio | Peso | A (Cloud) | Justificación + evidencia A | B (Self-Hosted) | Justificación + evidencia B |
|---|---|---|---|---|---|
| MDN2-1 Confiabilidad y consistencia de sync | 30% | | F2-CT-*, F2-CH-*, F2-LR-01 | | ídem |
| MDN2-2 Operación y mantenibilidad | 20% | | Benchmark §3 | | ídem |
| MDN2-3 Rendimiento | 15% | | Benchmark §1 | | ídem |
| MDN2-4 Seguridad | 15% | | Benchmark §4 | | ídem |
| MDN2-5 TCO | 10% | | TCO §4 | | ídem |
| MDN2-6 Escalabilidad | 5% | | F2-LT-* | | ídem |
| MDN2-7 Riesgo tecnológico | 5% | | Riesgos (Entregable 7) | | ídem |
| **TOTAL ponderado** | 100% | **=Σ(peso×nota)** | | **=Σ(peso×nota)** | |

## Regla de decisión

- Diferencia de totales **≥ 0,5 puntos** → recomendación objetiva de la alternativa superior.
- Diferencia **< 0,5** o criterio MDN2-1 con nota < 3 en cualquiera → la evidencia **no diferencia objetivamente**: N-2 permanece PD y se documenta por qué (criterio de aceptación del Master Prompt v1.1).
- Cualquier métrica sin Anexo de Reproducibilidad queda excluida del cálculo (REGLA ADICIONAL del Fundador).

**Resultado:** A = ___ · B = ___ · Decisión propuesta: ___ · Firma técnica: ___
**Aprobación del Fundador (cierra N-2 vía ADR-014 definitivo):** ☐ Aprobada ☐ Rechazada — fecha ___
