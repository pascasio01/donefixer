# EGM — 02: Diagramas de Flujo Operativos

**Norma:** DC-14 (POL-EGM-01/05/06/11/12). Los gates los ejecuta CI; no tienen override humano salvo incidente con ADR posterior.

## 1. Ciclo de vida de un Work Package

```mermaid
stateDiagram-v2
  [*] --> Backlog
  Backlog --> Ready: DoR firmada (POL-EGM-02)\ndependencias Done + parametrización resuelta
  Ready --> InProgress: rama feature/WP-<id> abierta\n(protección de ramas lo permite)
  InProgress --> InReview: PR abierto con checklist maestro
  InReview --> InProgress: cambios solicitados / pipeline rojo
  InReview --> Gates: aprobación (autor≠aprobador)
  Gates --> Done: QG-1…QG-4 verdes + docs sincronizadas (POL-EGM-03)
  Gates --> InReview: gate fallido (sin override humano)
  Done --> Released: merge a release/x.y + tag + changelog
  Released --> InProduction: deploy + test de humo + golden signals OK
  InProduction --> [*]
  Ready --> Backlog: re-priorizado
```

## 2. Flujo de Pull Request

```mermaid
flowchart LR
  A[PR abierto\ncon checklist] --> B{Checks automáticos\nPOL-EGM-05}
  B -->|pipeline rojo| R1[Rechazo automático]
  B -->|secretos / cobertura baja\nRLS test tocado / docs rotas| R1
  B -->|verde| C{Revisión humana\n1 aprobación develop\n2 main · CODEOWNER}
  C -->|cambios| A
  C -->|aprobado| D[Merge]
  R1 --> A
```

## 3. Flujo de ADR

```mermaid
flowchart LR
  E[Evento: nueva tecnología / desviación /\ncontrato / reutilización spike] --> F[Borrador ADR\nplantilla ADI]
  F --> G[Revisión arquitectura]
  G --> H{Aprobación Fundador}
  H -->|rechazado| E
  H -->|aprobado| I[Registro en ADI\n+ actualización de docs\nafectados en el mismo PR]
  I --> J[Revisión de WPs parametrizados\ndependientes del ADR]
```

## 4. Flujo de Incidente

```mermaid
flowchart TD
  D1[Detección: alerta con runbook / usuario] --> D2{Clasificación SEV\nDoc 54}
  D2 -->|SEV-1/2| D3[Guardia + responsable área\ncomunicación inmediata\ncongelar merges si aplica]
  D2 -->|SEV-3| D4[Revisión diaria]
  D3 --> D5[Ejecutar runbook RB-* /\nrollback si criterio de disparo]
  D5 --> D6[Resolución + verificación\ngolden signals]
  D6 --> D7[Postmortem sin culpa\nacciones con responsable y fecha]
  D7 --> D8[Lecciones → runbooks /\nADR si cambia norma]
```

## 5. Flujo de Deuda Técnica

```mermaid
flowchart LR
  T1[Atajo detectado\nen PR] --> T2{¿Toca seguridad, RLS,\nsync o prohibiciones IA?}
  T2 -->|sí| T3[BLOQUEO — no es deuda,\nno se mergea]
  T2 -->|no| T4[TD-<n> registrada:\ncausa, impacto, WP, fecha objetivo]
  T4 --> T5[Revisión mensual\npriorización]
  T5 --> T6[PR de eliminación\nreferencia TD-<n> + gate en verde pleno]
```
