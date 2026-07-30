// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// Infraestructura: PostgreSQL 16 + RLS + set_config transaccional (Doc 26 MT-4), outbox (EV-1).
using Npgsql;

namespace SpikeBackend.Infrastructure;

public static class Database
{
    public static string ConnectionString { get; set; } =
        Environment.GetEnvironmentVariable("SPIKE_DB")
        ?? "Host=127.0.0.1;Port=5432;Database=spike;Username=postgres;Password=postgres";

    public static async Task MigrateAsync()
    {
        await using var con = new NpgsqlConnection(ConnectionString);
        await con.OpenAsync();
        var sql = """
        CREATE TABLE IF NOT EXISTS tenants (id uuid PRIMARY KEY, name text NOT NULL);
        CREATE TABLE IF NOT EXISTS users (
            id uuid PRIMARY KEY, tenant_id uuid NOT NULL REFERENCES tenants(id),
            email text NOT NULL, full_name text NOT NULL);
        CREATE TABLE IF NOT EXISTS work_orders (
            id uuid PRIMARY KEY, tenant_id uuid NOT NULL REFERENCES tenants(id),
            title text NOT NULL, state text NOT NULL DEFAULT 'Asignada',
            version int NOT NULL DEFAULT 1,
            deleted_at timestamptz NULL,
            updated_at timestamptz NOT NULL DEFAULT now());
        CREATE TABLE IF NOT EXISTS wo_items (
            id uuid PRIMARY KEY, tenant_id uuid NOT NULL, work_order_id uuid NOT NULL REFERENCES work_orders(id),
            label text NOT NULL, done boolean NOT NULL DEFAULT false, version int NOT NULL DEFAULT 1);
        CREATE TABLE IF NOT EXISTS evidences (
            id uuid PRIMARY KEY, tenant_id uuid NOT NULL, work_order_id uuid NOT NULL REFERENCES work_orders(id),
            kind text NOT NULL, sha256 text NOT NULL, note text NULL,
            hlc_phys bigint NOT NULL, hlc_logical bigint NOT NULL,
            created_by uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now());
        CREATE TABLE IF NOT EXISTS stock_movements (
            id uuid PRIMARY KEY, tenant_id uuid NOT NULL, work_order_id uuid NOT NULL,
            part_id uuid NOT NULL, delta int NOT NULL,
            operation_id uuid UNIQUE NOT NULL, created_at timestamptz NOT NULL DEFAULT now());
        CREATE TABLE IF NOT EXISTS sync_operations (
            operation_id uuid PRIMARY KEY, tenant_id uuid NOT NULL, actor_id uuid NOT NULL,
            entity text NOT NULL, entity_id uuid NOT NULL, kind text NOT NULL,
            payload jsonb NOT NULL, hlc_phys bigint NOT NULL, hlc_logical bigint NOT NULL,
            verdict text NOT NULL, verdict_reason text NULL,
            server_version int NULL, processed_at timestamptz NOT NULL DEFAULT now());
        CREATE TABLE IF NOT EXISTS outbox_events (
            id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            tenant_id uuid NOT NULL, event_type text NOT NULL, payload jsonb NOT NULL,
            created_at timestamptz NOT NULL DEFAULT now(), published_at timestamptz NULL);

        -- RLS (Doc 26): aislamiento por tenant con defensa en profundidad
        ALTER TABLE work_orders ENABLE ROW LEVEL SECURITY;
        ALTER TABLE wo_items ENABLE ROW LEVEL SECURITY;
        ALTER TABLE evidences ENABLE ROW LEVEL SECURITY;
        ALTER TABLE stock_movements ENABLE ROW LEVEL SECURITY;
        ALTER TABLE sync_operations ENABLE ROW LEVEL SECURITY;
        DO $$ BEGIN
          CREATE POLICY tenant_iso ON work_orders USING (tenant_id = current_setting('app.current_tenant')::uuid);
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        DO $$ BEGIN
          CREATE POLICY tenant_iso ON wo_items USING (tenant_id = current_setting('app.current_tenant')::uuid);
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        DO $$ BEGIN
          CREATE POLICY tenant_iso ON evidences USING (tenant_id = current_setting('app.current_tenant')::uuid);
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        DO $$ BEGIN
          CREATE POLICY tenant_iso ON stock_movements USING (tenant_id = current_setting('app.current_tenant')::uuid);
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        DO $$ BEGIN
          CREATE POLICY tenant_iso ON sync_operations USING (tenant_id = current_setting('app.current_tenant')::uuid);
        EXCEPTION WHEN duplicate_object THEN NULL; END $$;

        -- Seed: 2 tenants para pruebas de aislamiento
        INSERT INTO tenants (id, name) VALUES
          ('11111111-1111-1111-1111-111111111111','Tenant A'),
          ('22222222-2222-2222-2222-222222222222','Tenant B')
        ON CONFLICT DO NOTHING;
        INSERT INTO users (id, tenant_id, email, full_name) VALUES
          ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa','11111111-1111-1111-1111-111111111111','tec@a.dev','Técnico A'),
          ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb','22222222-2222-2222-2222-222222222222','tec@b.dev','Técnico B')
        ON CONFLICT DO NOTHING;
        """;
        await using var cmd = new NpgsqlCommand(sql, con);
        await cmd.ExecuteNonQueryAsync();
    }

    /// <summary>Abre conexión + transacción y fija app.current_tenant con set_config local a la transacción (PgBouncer-safe, MT-4).</summary>
    public static async Task<(NpgsqlConnection, NpgsqlTransaction)> BeginTenantTxAsync(Guid tenantId)
    {
        var con = new NpgsqlConnection(ConnectionString);
        await con.OpenAsync();
        var tx = await con.BeginTransactionAsync();
        await using var cmd = new NpgsqlCommand(
            "SELECT set_config('app.current_tenant', @t, true)", con, tx);
        cmd.Parameters.AddWithValue("t", tenantId.ToString());
        await cmd.ExecuteNonQueryAsync();
        return (con, tx);
    }
}
