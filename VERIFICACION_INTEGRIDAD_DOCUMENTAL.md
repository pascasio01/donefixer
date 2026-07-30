# Verificación de Integridad Documental — Proceso Obligatorio Pre-Aprobación de Olas

| Campo | Valor |
|---|---|
| Documento | VERIFICACION_INTEGRIDAD_DOCUMENTAL |
| Versión | 1.0 |
| Estado | ✅ Creado por instrucción adicional 3 de la aprobación de la Auditoría Integral (2026-07-29) |
| Norma | **Ninguna ola futura podrá aprobarse con errores de integridad documental.** Esta verificación se ejecuta antes de solicitar la aprobación de cualquier ola y su reporte se adjunta a la entrega consolidada. |

---

## 1. Alcance de la verificación (7 comprobaciones)

| # | Comprobación | Qué detecta | Método |
|---|---|---|---|
| V-1 | **Referencias cruzadas** | Cita a un documento inexistente o sección inexistente | Extracción de patrones `Doc N`, `doc NN`, `ADR-0XX`, nombres de archivo `.md` y comparación contra el inventario real de la carpeta |
| V-2 | **Identificadores inexistentes** | Cita de RF/RNF/ADR/MT/SY/EV/AP/IN/SE/EA/WA/MA/AIA/GA/P-33/C/J/SB/N que no existe en el **Canonical Identifier Registry** | Extracción automática de todos los tokens con formato de ID y comparación contra el Registry (origen del hallazgo H-04) |
| V-3 | **Duplicados** | El mismo ID definido dos veces en el mismo documento o en dos documentos distintos | Cruce de definiciones (tablas de catálogo) entre documentos |
| V-4 | **Enlaces rotos** | Referencia a archivo `.md` inexistente en `/mnt/agents/output/donefixer/` | Listado de archivos vs. nombres citados |
| V-5 | **Inconsistencias DC/SU/PD** | (a) Afirmación normativa sin marca de evidencia; (b) un mismo hecho marcado DC en un documento y SU/PD en otro; (c) una PD tratada como DC | (a) y (c) por revisión de patrón; (b) por tabla de hechos clave (valores numéricos y líneas rojas) comparada entre documentos — método usado en la auditoría 2026-07 para verificar la línea roja FinOps en 3 fuentes |
| V-6 | **Documentos huérfanos** | Documento oficial no citado por ningún otro ni registrado en el Índice Maestro | Grafo de citas sobre el inventario de archivos |
| V-7 | **Trazabilidad incompleta** | Decisión tecnológica sin trazado a RF/RNF/SRS/PRD/Domain Model/ADR (condición permanente 1 de la Ola 3), o RF/RNF del catálogo sin ningún documento de arquitectura que lo atienda | Tabla de trazabilidad por documento + cobertura inversa de catálogos RF/RNF |

## 2. Procedimiento

1. **Extracción automática** de identificadores citados y definidos (expresiones regulares sobre todos los `.md` de la carpeta oficial) — mismo método que detectó H-04 en la auditoría 2026-07.
2. **Comparación contra el Registry** (`REGISTRY_Canonical_Identifiers.md`): todo ID citado debe existir; todo ID definido debe estar registrado.
3. **Grafo de documentos:** inventario real (`ls`) vs. citas; huérfanos y enlaces rotos.
4. **Tabla de hechos clave:** valores normativos críticos (línea roja FinOps, SLOs, presupuestos, umbrales) comparados entre todos los documentos que los citan — deben ser idénticos.
5. **Revisión de marcado DC/SU/PD** en afirmaciones nuevas.
6. **Reporte:** lista de errores (bloqueantes) y advertencias (no bloqueantes), en la entrega consolidada de la ola.

## 3. Criterio de aprobación

- **Errores bloqueantes (cero permitidos):** ID inexistente (V-2), enlace roto (V-4), duplicado (V-3), hecho clave con valores distintos en dos documentos (V-5b), decisión sin trazabilidad (V-7).
- **Advertencias (deben declararse; la ola puede aprobarse con ellas si el Fundador las acepta explícitamente):** huérfanos (V-6), afirmaciones sin marca en texto narrativo no normativo (V-5a).

## 4. Ejecución inicial (retroactiva a la Ola 3, post AO-1…AO-4)

Ejecutada el 2026-07-29 tras aplicar AO-1–AO-4:

| Verificación | Resultado |
|---|---|
| V-2 (IDs) | ✅ 0 identificadores rotos restantes en Docs 21/22/23 (verificado: 0 coincidencias de familias inválidas tras AO-1) |
| V-5b (hechos clave) | ✅ Línea roja 30% idéntica en Doc 12 / Doc 03 / Doc 33; SLOs sin divergencias detectadas |
| V-4 (archivos) | ✅ ADR-001-010_Registro.md, ADI y Registry creados; citas ADR-00X ahora resuelven |
| V-3 (duplicados) | ✅ Lista de prohibiciones IA unificada (AO-2): Doc 33 §4 canónica, Doc 19 deriva |
| Resto | Declarado en la entrega consolidada de la Ola 4 |

---

*Registro de cambios — v1.0 (2026-07-29): creación por instrucción adicional 3. Obligatorio antes de aprobar cualquier ola futura.*
