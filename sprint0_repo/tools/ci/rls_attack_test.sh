#!/usr/bin/env bash
# TEST DE ATAQUE RLS — gate permanente (lección empírica Spike Fase 1: superuser bypassa RLS).
# Conecta con el ROL DE APLICACIÓN (no privilegiado) fijando otro tenant y exige 0 filas cross-tenant.
set -euo pipefail
: "${PGHOST:=localhost}" "${PGPORT:=5432}" "${PGDATABASE:=donefixer_ci}"
APP_ROLE="${APP_ROLE:-donefixer_app}"
# tenant ajeno fijado en la transacción; debe devolver 0 en toda tabla de tenant
TABLAS=$(psql "postgresql://$APP_ROLE@$PGHOST:$PGPORT/$PGDATABASE" -Atc \
  "SELECT tablename FROM pg_tables WHERE schemaname='public' AND rowsecurity")
for t in $TABLAS; do
  n=$(psql "postgresql://$APP_ROLE@$PGHOST:$PGPORT/$PGDATABASE" -Atc \
    "BEGIN; SELECT set_config('app.current_tenant','00000000-0000-0000-0000-000000000000',true); SELECT COUNT(*) FROM $t; ROLLBACK;" | tail -1)
  [ "$n" = "0" ] || { echo "FAIL: $t expone $n filas cross-tenant"; exit 1; }
done
echo "rls_attack_test: PASS (0 filas cross-tenant en todas las tablas RLS)"
