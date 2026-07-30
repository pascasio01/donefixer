# Protección de ramas (configuración a aplicar en el hosting Git — POL-EGM-04/05)

## main
- Require PR: sí · Aprobaciones: **2** (CODEOWNERS) · Dismiss stale reviews: sí
- Required checks: todos los jobs de `ci.yml` (incl. performance-accessibility en release)
- Require linear history: sí · Force pushes: prohibidos · Deletions: prohibidos
- Solo mergeable desde `release/*` o `hotfix/*`

## develop
- Require PR: sí · Aprobaciones: **1** (CODEOWNER del área) · Dismiss stale: sí
- Required checks: commitlint, secrets-scan, build-*, unit-backend, docs-integrity, contract, integration (incl. rls_attack_test), security, e2e (suite J-2)
- Force pushes: prohibidos

## feature/*, release/*, hotfix/*
- Nomenclatura obligatoria (verificada por commitlint + regla de rama en CI).
- `release/*`: solo commits de fix con PR y gates completos.
- `hotfix/*`: solo con issue de hotfix enlazado a incidente SEV abierto.

## Reglas globales
- Autor ≠ aprobador (técnico).
- Required conversations resolved antes de merge.
- Escaneo de secretos también como protección de push (push protection) si la plataforma lo ofrece.
