# SPIKE S-1 — Especificación Completa de la Architecture Spike N-1/N-2

| Campo | Valor |
|---|---|
| Documento | SPIKE_S1_Especificacion |
| Versión | 1.0 |
| Estado | Activo — bajo EXENCIÓN-SPIKE-01 (DC, 2026-07-29) |
| Autoridad | MASTER_PROMPT_Architecture_Spike_v1.0 + condiciones del Fundador (8 reglas) |
| Ubicación del código | `/mnt/agents/output/donefixer/spike/` — **código de investigación técnica, separado y no reutilizable en producción salvo ADR** |
| Trazabilidad | Docs 16 (J-2), 27 (SY-1…15), 23 (MA-1…10, matriz §4), 14 (máquina de estados OT), 12 (RNF-SYNC/PERF/MOB/SEC), ADI §6 |

---

## 1. Objetivo único

Obtener **evidencia medible** para cerrar **N-1** (framework móvil) y **N-2** (PowerSync Cloud vs. self-hosted) mediante ADR-013 y ADR-014. Si la evidencia es insuficiente, ambas quedan **PD** (condición del Fundador). (DC)

## 2. Alcance exacto — flujo J-2 canónico (Doc 16)

```
1. Técnico abre OT asignada (con red) → datos en réplica local
2. MODO AVIÓN activado
3. Ejecuta: checklist → edición de notas → adjunta 3 fotos → firma →
   consume 2 repuestos (delta) → cierre provisional de la OT
4. En paralelo, un segundo actor (supervisor) edita la misma OT en servidor
   (genera conflicto normativo: estado OT = servidor autoritativo;
   evidencias = aditivas; repuestos = deltas — Doc 14 §matriz)
5. MODO AVIÓN desactivado → sincronización
6. Servidor re-valida → veredictos ACCEPT/ADJUST/REJECT por operación
7. Confirmación visible al usuario: qué se aceptó, qué se ajustó y por qué
```

**Prohibido:** cualquier funcionalidad fuera de estos 7 pasos (login social, dashboard, más módulos, IA, branding). (DC)

## 3. Candidatos

| Eje | Candidatos | Referencia comparativa documentada (no implementada) |
|---|---|---|
| N-1 | **Flutter** · **React Native + Expo** | Kotlin Multiplatform, nativo dual (Doc 23 §4) |
| N-2 | **PowerSync self-hosted (Open Edition)** · **PowerSync Cloud** | Zero (fallback, Doc 27 §Alternativas) |

## 4. Arquitectura de la Spike (fiel a los documentos aprobados)

```
App candidata (Flutter / RN-Expo)
  └─ SQLite local + outbox local (operation_id UUIDv7, HLC, payload)
  └─ Adaptador de sync (MA-1) → PowerSync SDK
Backend mínimo (.NET 8 minimal API, estructura de capas Doc 24)
  ├─ POST /sync/operations  → write-path: idempotencia → re-validación
  │   de dominio (máquina de estados OT Doc 14) → veredicto por operación
  ├─ POST /auth/login       → JWT mínimo con tenant claim (Doc 26 MT-4)
  └─ PostgreSQL 16 + RLS (set_config transaccional) + esquema mínimo:
     tenants, users, work_orders, wo_items, evidences, stock_movements,
     sync_operations (registro de veredictos), outbox_events (EV-1)
```

Decisiones aprobadas que la Spike **sí implementa** (porque son el objeto de medición): outbox local en misma transacción (SY-4), idempotencia (SY-5), HLC (SY-6), tombstones (SY-10), matriz de conflictos (Doc 14), veredictos visibles (SY-9), re-validación de autoridad (ADR-011 v1.1).

## 5. Harness de medición (reproducible)

| Instrumento | Qué mide |
|---|---|
| `spike/harness/timing.ts|dart` | Timestamps por operación: creación→confirmación local, envío→veredicto, convergencia total |
| `spike/harness/netem.sh` | Perfiles de red: offline, 3G lento, pérdida 10%, corte a mitad de sync |
| `spike/harness/metricas_dispositivo.md` | Guía para medir en dispositivo real: arranque en frío (3×), memoria, CPU, batería (Battery Historian / Xcode Energy), tamaño del binario |
| `spike/harness/resultados.csv` | Plantilla única de registro — toda métrica del informe sale de aquí |
| Backend | Logs estructurados por operación (operation_id, latencia de re-validación, veredicto) |

## 6. Matriz de decisión y ponderación (aprobada en Doc 23 §4)

| Criterio | Peso | Métrica de la Spike que lo alimenta |
|---|---|---|
| Integración con motor de sync y SQLite | 25% | Errores de integración, líneas de código del adaptador, tests de conflicto pasados |
| Rendimiento en gama media | 20% | Arranque ≤2 s (RNF-PERF-004 ref.), scroll/jank, memoria, tamaño binario |
| Capacidades nativas (cámara, firma, background) | 15% | Implementación de foto+firma sin código nativo ad hoc |
| Productividad equipo mínimo | 15% | Tiempo de implementación del mismo J-2, LOC, complejidad ciclomática |
| Compartición con web (tokens, lógica no crítica) | 10% | % de lógica no crítica reutilizable |
| Talento/longevidad | 10% | Datos de mercado al momento (se documentan, no se miden en código) |
| Riesgo de plataforma | 5% | Licencias, gobernanza del framework |

**N-2** se decide por: facilidad de despliegue/operación (equipo de 1 persona), latencia y throughput medidos en ambos modos, observabilidad disponible, costo a 50 tenants (Doc 62), y riesgo de dependencia (licencia FSL vs. servicio gestionado).

## 7. Tests obligatorios (de las condiciones del Fundador)

| Suite | Contenido |
|---|---|
| Unit | HLC, outbox local, máquina de estados (dominio puro backend) |
| Integration | Write-path: idempotencia, veredictos, RLS multi-tenant (2 tenants, intento de cruce) |
| Offline | Los 7 pasos J-2 en modo avión real/simulado |
| Conflict | Los 8 casos normativos del Doc 27 (subset aplicable a J-2) |
| Recovery | Kill de app a mitad de captura y a mitad de sync; wipe + relogin |
| Performance | Convergencia con 200 operaciones acumuladas (RNF-SYNC-003) |
| Battery/Network | Medición en dispositivo (guía del harness) |

## 8. Limitaciones del entorno (declaradas, afectan plan de medición)

| Recurso | Estado en este entorno | Consecuencia |
|---|---|---|
| .NET 8 + PostgreSQL 16 | ✅ Disponible y verificado | S-2 completo aquí |
| PowerSync self-hosted (Docker) | ❌ Sin Docker ni red a registries (verificado) | Se implementa el **canal de sync equivalente sobre el write-path propio + cliente de replicación**, y N-2 se evalúa: (a) self-hosted vía evidencia arquitectónica + (b) Cloud con cuenta del Fundador. **Si esta evidencia se considera insuficiente, N-2 queda PD** (regla del Fundador) |
| Emulador/dispositivo Android/iOS | ❌ No disponible | S-4 entrega código instrumentado + guía; las métricas de dispositivo se completan en hardware real por el Fundador o su equipo |
| PowerSync Cloud | ⚠️ Requiere cuenta gratuita | El Fundador crea la cuenta cuando llegue S-3 |

## 9. Criterios de aceptación de S-1

1. Alcance = J-2 exacto, sin ampliaciones. ✅
2. Ponderación de decisión = la aprobada en Doc 23 §4. ✅
3. Limitaciones de entorno declaradas con su efecto en N-1/N-2. ✅
4. Todo el código bajo `spike/`, separado y marcado como investigación. ✅

---

*Registro de cambios — v1.0 (2026-07-29): creación bajo EXENCIÓN-SPIKE-01.*
