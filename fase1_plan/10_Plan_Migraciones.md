# FASE 1 PRE-GO — 10: Plan de Migraciones

**Norma:** DC-13 · Fuente: Doc 28 (PostgreSQL), Doc 26 (RLS), lecciones de la Spike.

## 1. Estrategia

- **Versionado:** migraciones numeradas e inmutables (`V0001__nombre.sql` o equivalente del tool elegido en WP-B1); aplicadas por el pipeline, nunca a mano.
- **Expand/contract obligatorio:** (1) expand: añadir lo nuevo sin tocar lo viejo → desplegar código que usa ambos → (2) contract: retirar lo viejo en un release posterior. Un rollback de aplicación **nunca** exige rollback destructivo de base de datos.
- **Orden de migración (build order DB):** tenants/usuarios/roles (B1) → RLS policies + FORCE RLS (B2) → tablas de dominio OT/activos/inventario/solicitudes (D-*) → sync_operations/outbox_events (C1) → índices de rendimiento tras carga inicial (F1).
- Cada migración: up **y** down verificados en CI contra una copia del esquema de staging.

## 2. Reglas RLS en migraciones (lección empírica de la Spike)

- Toda tabla con `tenant_id` se crea **con policy + FORCE ROW LEVEL SECURITY en la misma migración** — no se permite mergear una tabla de tenant sin RLS (gate de CI: linter de migraciones).
- Las migraciones corren con rol owner, pero **la aplicación nunca** (rol no privilegiado). Test de CI: conectar como rol de app y verificar 0 filas cross-tenant tras cada migración que toque tablas de tenant.
- `set_config('app.current_tenant', …, true)` transaccional (MT-4) — verificado en tests de integración bajo pooler.

## 3. Sync y WAL

- `wal_level=logical` desde la primera migración (requisito del canal `{{ADR-014}}`).
- Las tablas publicadas al canal se registran en la configuración del Anexo de Reproducibilidad Fase 2; añadir/retirar tablas de la publicación es una migración con su runbook (RB-07).

## 4. Seeds y datos de referencia

- Seeds de desarrollo/staging versionados (misma estructura que el seed J-2 de la Spike); producción: solo datos de referencia (catálogos), nunca datos de prueba.

## 5. Rollback de datos

- Backups antes de cada migración contract (ensayo WP-F4); punto de restauración documentado en el release.
- Ver Plan de Rollback (entregable 11) para criterios de disparo.
