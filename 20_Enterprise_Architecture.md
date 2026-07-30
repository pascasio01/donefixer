# DONEFIXER — 20 · Enterprise Architecture

> **Nombre oficial:** DONEFIXER · **Fundador, Creador y Desarrollador:** Pascasio Emmanuel Reynoso Reyes
> **Versión:** 1.0 · 2026-07-29 · **Estado:** En revisión (Ola 3)

---

## 1. Objetivo
Vista integradora: cómo las capacidades de negocio, las aplicaciones, los datos y la tecnología de DONEFIXER se alinean con la estrategia aprobada (docs 01–04) y gobiernan su evolución a 10 años.

## 2. Alcance
Mapa de capacidades de negocio, mapa de aplicaciones, mapa de datos, principios de gobierno arquitectónico y su ciclo. Es el documento de referencia ejecutiva de la arquitectura.

## 3. Exclusiones
Detalle de solución (doc 21) y de cada subsistema (docs 22–33).

## 4. Decisiones confirmadas (DC) — principios arquitectónicos consolidados

| # | Principio | Origen |
|---|---|---|
| EA-1 | **El dominio aprobado es la ley:** ninguna decisión técnica puede contradecirlo (condición permanente 5 de la Ola 2) | doc 14 canónico |
| EA-2 | Evolución por etapas con criterios medibles; prohibida la sobrearquitectura prematura | Condición permanente 5 (Ola 1) |
| EA-3 | Separación dominio / aplicación / infraestructura | Regla Ola 3 |
| EA-4 | Offline-first, mobile-first, AI-gobernada, multi-tenant nativo como propiedades del sistema | docs 01, ADR-011, AUD-00 |
| EA-5 | API-First, eventos primero, salida digna del cliente | ADR-009 |
| EA-6 | Separación permanente de planos administrativos | ADR-012 v1.1 |
| EA-7 | Seguridad y privacidad por diseño; integridad > seguridad > offline > usabilidad > rendimiento > costo | doc 10 §3.5 |
| EA-8 | Documentación como fuente de verdad; el código la implementa | Condición permanente 6 |

## 5. Mapa de capacidades de negocio (nivel 1 → nivel 2)

```
GESTIÓN DEL TRABAJO          GESTIÓN DE ACTIVOS          OPERACIÓN DE INSTALACIONES (F3+)
├─ Intake omnicanal          ├─ Jerarquía y registro      ├─ Multi-sitio / portafolio
├─ Órdenes de trabajo        ├─ Medidores y condición     ├─ Portales (inquilino/proveedor)
├─ Ejecución móvil offline   ├─ Códigos de falla / RCA    ├─ Contratos y SLAs
├─ Preventivo y programación ├─ TCO y ciclo de vida (F2+) ├─ Rondas y cumplimiento
└─ Despacho y habilidades    └─ Garantías (F2)            └─ Permisos de trabajo (F3)

CADENA DE SUMINISTRO (F2)    INTELIGENCIA Y GOBIERNO      PLATAFORMA SaaS
├─ Inventario y almacenes    ├─ KPIs y analítica          ├─ Tenancy y planes
├─ Compras y recepciones     ├─ IA copiloto y agentes     ├─ Entitlements y flags
├─ Facturas y conciliación   ├─ Auditoría inmutable       ├─ Consola de administración
└─ Proveedores y contratos   └─ Cumplimiento y evidencia  └─ Facturación SaaS y consumo
```
*Regla: cada capacidad de nivel 2 tiene (o tendrá) una spec en doc 43 y RF trazados en doc 11.*

## 6. Mapa de aplicaciones (estado objetivo por etapas)

| Etapa | Aplicaciones | Notas |
|---|---|---|
| **A (F0–F2)** | Web App/PWA (React) · App nativa (framework PD-N1) · Backend monolito modular (.NET) + workers · Consola de plataforma · PostgreSQL+RLS · PowerSync (PD-N2) · Redis · S3 | Un artefacto backend; un codebase web; un codebase móvil |
| **B (F3–F4)** | + Servicio IA Python (ML propio) · + ClickHouse (criterio E-3) · + Kafka/Redpanda (criterio E-2) · + Timescale si entra IoT (E-4) · K8s gestionado (E-1) | Solo por criterios medidos + ADR |
| **C (F5+)** | + Bases dedicadas enterprise · multi-región · marketplace · despliegues soberanos opcionales | Por contrato enterprise |

## 7. Mapa de datos (vista ejecutiva — detalle doc 25)
Sistema de registro: PostgreSQL (verdad operativa) · Local: SQLite en dispositivos (verdad de trabajo de campo, convergente) · Objetos: S3 (evidencias/documentos) · Analítica: vistas materializadas → ClickHouse (Etapa B) · Conocimiento: pgvector → dedicada si escala · **Flujo:** campo → sync (autoridad backend) → OLTP → eventos → analítica/IA. La verdad fluye en una sola dirección y se puede auditar en cada salto.

## 8. Gobierno arquitectónico
1. **ADRs** para toda decisión irreversible (registro doc 21-futuro/13-ADR consolidado); reapertura solo con evidencia nueva (precedente ADR-002).
2. **Revisión arquitectónica trimestral:** deriva vs. dominio, deuda, criterios de etapa medidos, licencias de dependencias críticas (PowerSync, LLM, cloud — lección Realm).
3. **FEP** para capacidades; **regla de tendencia prohibida** (toda tecnología: problema que resuelve + costo operativo + estrategia de reemplazo).
4. **Gates:** M1–M8 antes de código (AUD-00 §M); PRR (doc 70) antes de producción.

## 9. Riesgos
| Riesgo | Mitigación |
|---|---|
| Deriva entre capacidades construidas y mapa | Revisión trimestral EA-8; mapa actualizado por FEP |
| Salto de etapa por entusiasmo | Criterios medibles + ADR obligatorio |
| Concentración de conocimiento (bus-factor) | Esta suite + ADRs + handbook (doc 67) |

## 10. Métricas de la arquitectura
% capacidades con spec y RF (objetivo 100%) · criterios de etapa medidos vs. activados · deuda registrada vs. quemada (20%/trimestre, RNF-MNT-004) · ADRs abiertos sin resolver (visibilidad).

## 11. Criterios de aceptación
1. Tres mapas (capacidades/aplicaciones/datos) coherentes con docs aprobados. ✅ 2. Principios con origen. ✅ 3. Gobierno con ciclo y precedentes. ✅

## 12. Referencias cruzadas
Depende de: 01–04, 09–14, 24–31, ADRs. Alimenta: 21 (solution), 43 (specs), 69 (roadmap), 70 (PRR).

## 13. Control de cambios
| v | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-07-29 | Creación (Ola 3). 8 principios EA, mapa de capacidades en 6 dominios, mapa de aplicaciones por etapas, gobierno con revisión trimestral |
