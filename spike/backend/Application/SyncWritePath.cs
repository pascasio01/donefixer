// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// Aplicación: write-path de sincronización (SY-5 idempotencia, SY-8 re-validación, SY-9 veredictos).
using Npgsql;
using SpikeBackend.Domain;
using System.Text.Json;

namespace SpikeBackend.Application;

public record SyncOperation(
    Guid OperationId, Guid ActorId, string Entity, Guid EntityId, string Kind,
    JsonElement Payload, long HlcPhys, long HlcLogical);

public record OperationResult(
    Guid OperationId, string Verdict, string? Reason, int? ServerVersion);

public static class SyncWritePath
{
    private static readonly JsonSerializerOptions J = new(JsonSerializerDefaults.Web);

    public static async Task<List<OperationResult>> ProcessAsync(Guid tenantId, List<SyncOperation> ops)
    {
        var results = new List<OperationResult>();
        var (con, tx) = await Infrastructure.Database.BeginTenantTxAsync(tenantId);
        try
        {
            foreach (var op in ops.OrderBy(o => o.HlcPhys).ThenBy(o => o.HlcLogical))
                results.Add(await ProcessOneAsync(con, tx, tenantId, op));
            await tx.CommitAsync();
        }
        catch { await tx.RollbackAsync(); throw; }
        finally { await con.DisposeAsync(); }
        return results;
    }

    private static async Task<OperationResult> ProcessOneAsync(
        NpgsqlConnection con, NpgsqlTransaction tx, Guid tenantId, SyncOperation op)
    {
        // SY-5: idempotencia — ¿ya procesada esta operación?
        var existing = await ScalarAsync(con, tx,
            "SELECT verdict FROM sync_operations WHERE operation_id=@id",
            ("@id", op.OperationId));
        if (existing is string v)
            return new OperationResult(op.OperationId, v, "duplicate-replayed", null);

        var (verdict, reason, version) = op.Kind switch
        {
            "wo.transition" => await HandleTransition(con, tx, op),
            "wo.item.toggle" => await HandleItemToggle(con, tx, op),
            "evidence.add" => await HandleEvidence(con, tx, tenantId, op),   // aditiva
            "stock.consume" => await HandleStock(con, tx, tenantId, op),     // delta
            "wo.note.edit" => await HandleNote(con, tx, op),
            "wo.delete" => await HandleDelete(con, tx, op),                  // tombstone
            _ => ("reject", "unknown-kind", (int?)null)
        };

        // Registro del veredicto (auditoría de sync, SY-9)
        await ExecAsync(con, tx, """
            INSERT INTO sync_operations
              (operation_id, tenant_id, actor_id, entity, entity_id, kind, payload,
               hlc_phys, hlc_logical, verdict, verdict_reason, server_version)
            VALUES (@id, @t, @a, @e, @eid, @k, @p, @hp, @hl, @v, @r, @sv)
            """,
            ("@id", op.OperationId), ("@t", tenantId), ("@a", op.ActorId),
            ("@e", op.Entity), ("@eid", op.EntityId), ("@k", op.Kind),
            ("@p", op.Payload.GetRawText()), ("@hp", op.HlcPhys), ("@hl", op.HlcLogical),
            ("@v", verdict), ("@r", reason ?? (object)DBNull.Value),
            ("@sv", version ?? (object)DBNull.Value));

        // EV-1: evento en outbox en la MISMA transacción
        await ExecAsync(con, tx,
            "INSERT INTO outbox_events (tenant_id, event_type, payload) VALUES (@t, @et, @p)",
            ("@t", tenantId), ("@et", $"{op.Entity}.{op.Kind}.{verdict}"),
            ("@p", JsonSerializer.Serialize(new { op.OperationId, op.EntityId, verdict }, J)));

        return new OperationResult(op.OperationId, verdict, reason, version);
    }

    // Conflicto: estado OT = SERVIDOR AUTORITATIVO (Doc 14) — nunca LWW silencioso
    private static async Task<(string, string?, int?)> HandleTransition(
        NpgsqlConnection con, NpgsqlTransaction tx, SyncOperation op)
    {
        var row = await RowAsync(con, tx,
            "SELECT state, version FROM work_orders WHERE id=@id FOR UPDATE",
            ("@id", op.EntityId));
        if (row == null) return ("reject", "wo-not-found", null);

        var serverState = Enum.Parse<WoState>((string)row[0]);
        var attempted = Enum.Parse<WoState>(op.Payload.GetProperty("to").GetString()!);
        var clientBaseVersion = op.Payload.GetProperty("baseVersion").GetInt32();

        var verdict = WorkOrderStateMachine.RevalidateTransition(serverState, attempted);
        if (verdict is Verdict.Reject)
            return ("reject", $"server-state-{serverState}-authoritative", (int)row[1]);
        if (verdict is Verdict.AcceptDuplicate)
            return ("accept", "duplicate-transition", (int)row[1]);

        var newVersion = (int)row[1] + 1;
        var adjusted = clientBaseVersion != (int)row[1];
        await ExecAsync(con, tx,
            "UPDATE work_orders SET state=@s, version=@v, updated_at=now() WHERE id=@id",
            ("@s", attempted.ToString()), ("@v", newVersion), ("@id", op.EntityId));
        return (adjusted ? "adjust" : "accept",
                adjusted ? "applied-on-newer-server-version" : null, newVersion);
    }

    private static async Task<(string, string?, int?)> HandleItemToggle(
        NpgsqlConnection con, NpgsqlTransaction tx, SyncOperation op)
    {
        var done = op.Payload.GetProperty("done").GetBoolean();
        var n = await ExecAsync(con, tx,
            "UPDATE wo_items SET done=@d, version=version+1 WHERE id=@id",
            ("@d", done), ("@id", op.EntityId));
        return n == 1 ? ("accept", null, null) : ("reject", "item-not-found", null);
    }

    // Evidencias: ADITIVAS (Doc 14) — siempre se aceptan si la OT existe y no está cerrada
    private static async Task<(string, string?, int?)> HandleEvidence(
        NpgsqlConnection con, NpgsqlTransaction tx, Guid tenantId, SyncOperation op)
    {
        var state = await ScalarAsync(con, tx,
            "SELECT state FROM work_orders WHERE id=@id", ("@id", op.EntityId));
        if (state is not string s) return ("reject", "wo-not-found", null);
        if (s is "Cerrada" or "Cancelada")
            return ("reject", $"wo-{s}-immutable-evidence", null); // RF-WO-003
        await ExecAsync(con, tx, """
            INSERT INTO evidences (id, tenant_id, work_order_id, kind, sha256, note, hlc_phys, hlc_logical, created_by)
            VALUES (@id, @t, @wo, @k, @h, @n, @hp, @hl, @by)
            """,
            ("@id", op.Payload.GetProperty("evidenceId").GetGuid()),
            ("@t", tenantId), ("@wo", op.EntityId),
            ("@k", op.Payload.GetProperty("kind").GetString()!),
            ("@h", op.Payload.GetProperty("sha256").GetString()!),
            ("@n", op.Payload.TryGetProperty("note", out var nt) ? nt.GetString()! : (object)DBNull.Value),
            ("@hp", op.HlcPhys), ("@hl", op.HlcLogical), ("@by", op.ActorId));
        return ("accept", null, null);
    }

    // Stock: DELTAS (Doc 14) — nunca set; idempotente por operation_id (UNIQUE)
    private static async Task<(string, string?, int?)> HandleStock(
        NpgsqlConnection con, NpgsqlTransaction tx, Guid tenantId, SyncOperation op)
    {
        var state = await ScalarAsync(con, tx,
            "SELECT state FROM work_orders WHERE id=@id", ("@id", op.EntityId));
        if (state is not string s) return ("reject", "wo-not-found", null);
        if (s is "Cerrada" or "Cancelada") return ("reject", $"wo-{s}-no-consumption", null);
        await ExecAsync(con, tx, """
            INSERT INTO stock_movements (id, tenant_id, work_order_id, part_id, delta, operation_id)
            VALUES (@id, @t, @wo, @p, @d, @op) ON CONFLICT (operation_id) DO NOTHING
            """,
            ("@id", Guid.NewGuid()), ("@t", tenantId), ("@wo", op.EntityId),
            ("@p", op.Payload.GetProperty("partId").GetGuid()),
            ("@d", op.Payload.GetProperty("delta").GetInt32()),
            ("@op", op.OperationId));
        return ("accept", null, null);
    }

    private static async Task<(string, string?, int?)> HandleNote(
        NpgsqlConnection con, NpgsqlTransaction tx, SyncOperation op)
    {
        var n = await ExecAsync(con, tx,
            "UPDATE work_orders SET title=@t, version=version+1, updated_at=now() WHERE id=@id AND deleted_at IS NULL",
            ("@t", op.Payload.GetProperty("note").GetString()!), ("@id", op.EntityId));
        return n == 1 ? ("accept", null, null) : ("reject", "wo-not-found-or-deleted", null);
    }

    // Borrado: TOMBSTONE — "los borrados ganan" (Doc 14)
    private static async Task<(string, string?, int?)> HandleDelete(
        NpgsqlConnection con, NpgsqlTransaction tx, SyncOperation op)
    {
        var n = await ExecAsync(con, tx,
            "UPDATE work_orders SET deleted_at=now(), version=version+1 WHERE id=@id",
            ("@id", op.EntityId));
        return n == 1 ? ("accept", "tombstone-applied", null) : ("reject", "wo-not-found", null);
    }

    private static async Task<object?> ScalarAsync(NpgsqlConnection con, NpgsqlTransaction tx,
        string sql, params (string, object)[] ps)
    {
        await using var cmd = new NpgsqlCommand(sql, con, tx);
        foreach (var (n, v) in ps) cmd.Parameters.AddWithValue(n, v);
        return await cmd.ExecuteScalarAsync();
    }

    private static async Task<object[]?> RowAsync(NpgsqlConnection con, NpgsqlTransaction tx,
        string sql, params (string, object)[] ps)
    {
        await using var cmd = new NpgsqlCommand(sql, con, tx);
        foreach (var (n, v) in ps) cmd.Parameters.AddWithValue(n, v);
        await using var r = await cmd.ExecuteReaderAsync();
        if (!await r.ReadAsync()) return null;
        var row = new object[r.FieldCount];
        r.GetValues(row);
        return row;
    }

    private static async Task<int> ExecAsync(NpgsqlConnection con, NpgsqlTransaction tx,
        string sql, params (string, object)[] ps)
    {
        await using var cmd = new NpgsqlCommand(sql, con, tx);
        foreach (var (n, v) in ps) cmd.Parameters.AddWithValue(n, v);
        return await cmd.ExecuteNonQueryAsync();
    }
}
