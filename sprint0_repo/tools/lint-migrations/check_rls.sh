#!/usr/bin/env bash
# Linter de migraciones (POL-EGM-07, lección empírica Spike): toda tabla con tenant_id debe
# nacer con ENABLE + FORCE ROW LEVEL SECURITY y al menos una policy, en la MISMA migración.
# Gate permanente indesactivable. Uso: check_rls.sh <dir_migraciones>
set -euo pipefail
DIR="${1:?uso: check_rls.sh <dir_migraciones>}"
fails=0
for f in "$DIR"/V*.sql; do
  [ -e "$f" ] || continue
  # tablas nuevas con tenant_id en esta migración
  mapfile -t tablas < <(grep -oiE 'CREATE TABLE (IF NOT EXISTS )?[a-z_]+' "$f" | awk '{print $NF}' | sort -u)
  for t in $tablas; do
    if grep -qEi "CREATE TABLE.*$t" "$f" && grep -A50 -iE "CREATE TABLE.*$t" "$f" | grep -qi "tenant_id"; then
      grep -qi "ALTER TABLE $t ENABLE ROW LEVEL SECURITY" "$f" || { echo "FAIL $f: $t con tenant_id sin ENABLE RLS"; fails=1; }
      grep -qi "ALTER TABLE $t FORCE ROW LEVEL SECURITY"  "$f" || { echo "FAIL $f: $t con tenant_id sin FORCE RLS"; fails=1; }
      grep -qi "CREATE POLICY .* ON $t "                    "$f" || { echo "FAIL $f: $t sin policy en la misma migración"; fails=1; }
    fi
  done
  # prohibited: crear tabla tenant sin tenant_id queda para revisión; aquí solo bloqueamos lo crítico
done
[ "$fails" -eq 0 ] && echo "lint-migrations RLS/FORCE: PASS" || exit 1
