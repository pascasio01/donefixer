# GATE 70 — Registro de Riesgos Residuales (expediente, DC-12)

| ID | Riesgo | Origen / evidencia | Prob. | Impacto | Mitigación registrada | Estado |
|---|---|---|---|---|---|---|
| RR-01 | Elección de framework móvil sin evidencia de dispositivo (N-1) | Doc 23; Fase 1 no pudo medir dispositivo | Media | Alto | Instrumentación N-1 lista; medición en dispositivo tras N-2 (DC-10); ADR-013 con evidencia | Abierto — PD |
| RR-02 | Canal de réplica sync sin comparativa objetiva (N-2) | Fase 1 validó write-path, no el canal | Media | Alto | Fase 2B con variable controlada única; regla de decisión objetiva; si no diferencia → N-2 sigue PD | Abierto — PD |
| RR-03 | RLS bypass por rol privilegiado en producción | Hallazgo empírico Spike Fase 1 (superuser ignora RLS) | Baja | Crítico | app role no privilegiado + FORCE RLS + test de ataque en CI (RNF-SEC-006); lección incorporada a Doc 26 | Mitigado — verificar en auditoría final |
| RR-04 | Escalabilidad 10.000 usuarios solo simulable | Limitación de entorno declarada (SU) | Media | Medio | Clasificación SU explícita; load tests reales en Carril B; capacity planning Doc 62 | Abierto — SU |
| RR-05 | Dependencia de proveedor PowerSync (tarifa/continuidad) | TCO Fase 2 pendiente | Media | Medio | TCO comparativo + criterio MDN2-7 (riesgo 5%) + reversibilidad evaluada en matriz N-2 | Abierto — se evalúa en Carril B |
| RR-06 | Cumplimiento legal sin revisión profesional externa | Docs 03/12 son borradores documentales | Alta | Alto | Revisión legal antes de pilotos (PD-3); Doc 60 cumplimiento | Abierto — acción externa |
| RR-07 | Coste de IA supera línea roja (30% revenue tenant) | Doc 62/33 | Baja | Alto | Monitoreo FinOps con alertas + kill-switch por tenant (GA) | Mitigado por diseño — validar en operación |
| RR-08 | Deriva documental al crecer el corpus | Auditoría integral detectó 25 IDs rotos (corregidos AO-1) | Media | Medio | Verificación de integridad obligatoria antes de cada aprobación de ola (instrucción del Fundador) + Registry | Mitigado — control permanente |
| RR-09 | ADR-014 fase 1 (write-path propio) quedara invalidado por resultado de Fase 2 | DC-05: fase 1 es DC-C, no definitiva | Baja | Medio | Fase 2 con mismos casos; si evidencia contradice, ADR nuevo y plan de transición | Abierto — por diseño |
| RR-10 | Revisión legal / marca / residencia bloquean pilotos aunque el gate técnico pase | G-6 del checklist | Media | Medio | Gate incluye área Cumplimiento; NO GO si 🔲 sin resolver | Abierto |

*Registro vivo: se actualiza en cada fase y obligatoriamente en la auditoría final (paso 3 del Protocolo).*
