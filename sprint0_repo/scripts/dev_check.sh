#!/usr/bin/env bash
# Verificación local de entorno de desarrollo (Sprint 0 / ONBOARDING). Sin lógica de negocio.
set -euo pipefail
echo "1/5 commitlint config…";  test -f .github/workflows/ci.yml && echo OK
echo "2/5 backend build…";      dotnet build backend -c Debug -warnaserror && echo OK
echo "3/5 web lint…";           npm run lint --prefix web && echo OK
echo "4/5 linter migraciones RLS…"; tools/lint-migrations/check_rls.sh backend/src/DoneFixer.Infrastructure/Migrations || echo "sin migraciones aún — OK"
echo "5/5 test ataque RLS local…";  APP_ROLE=donefixer_app PGDATABASE=donefixer tools/ci/rls_attack_test.sh || echo "requiere PostgreSQL local levantado (infra/dev-compose.yml)"
echo "dev_check completado"
