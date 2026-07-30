> Expediente de cierre de PDs bloqueantes (G-0 del Doc 70). Material preparado; la decisión y la evidencia externa corresponden al Fundador. Subordinado a DC-01…DC-15. Nada de esto autoriza código de producción.

# 00 · Expediente de cierre de PDs bloqueantes

Regla vigente (Doc 70, G-0): con una PD bloqueante abierta → NO GO automático. Este expediente reúne, por PD, (a) lo que ya existe, (b) lo que falta y de quién depende, (c) el artefacto exacto que cierra la PD.

| PD | Qué cierra | Ya existe | Falta (externo) | Artefacto de cierre |
|---|---|---|---|---|
| **N-1** (framework móvil → ADR-013) | Medición reproducible en dispositivo Android real del J-2 | `spike_fase2/n1_instrumentacion/`: SPIKE_N1_Instrumentacion.md, MetricsLogger (.dart/.ts), RESULTADOS_N1.csv (formato), ANEXO_Reproducibilidad_N1.md | Dispositivo Android físico + ejecución de la batería | ADR-013 redactado con matriz Doc 23 §4 + anexo de reproducibilidad firmado |
| **N-2** (PowerSync Cloud vs self-hosted → ADR-014) | Comparativa objetiva Carril B con regla de decisión (≥0,5 pt ponderado; Confiabilidad ≥3/5) | `spike_fase2/`: docker-compose.powersync.yml, powersync.yaml, entorno_a/b.env, GUIA_Carril_B_Entornos.md, SPIKE_F2B_Precondiciones.md, harness_f2 (6/6 PASS en CONTROL), plantillas Benchmark/TCO/Matriz | Cuenta PowerSync Cloud + host con Docker para self-hosted + ejecución F2B | ADR-014 definitivo + matriz N-2 cumplimentada + anexos de reproducibilidad de ambos entornos |
| **PD-CLOUD** (proveedor cloud) | Decisión de negocio del Fundador | Ficha 01 con opciones y criterios | Decisión del Fundador | Entrada en ADI/Registry + actualización de parametrización |
| **PD-IA-1** (proveedor LLM del gateway) | Decisión de negocio (ADR-007 fija gateway multi-modelo; queda el proveedor) | Ficha 02 | Decisión del Fundador | ADR complementario o entrada ADI + límite de coste (RNF-AI-004) |
| **PD-4** (idiomas de lanzamiento) | Decisión de producto | Ficha 03 (vinculada a N-6) | Decisión del Fundador | Actualización Doc 11 (RF-I18N) y Registry |

Tras cerrar las 5 con evidencia: ejecutar el Documento 70 (auditoría completa, expediente ya en `gate_doc70/`) y aceptar su veredicto sin reinterpretarlo.
