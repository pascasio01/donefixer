// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// API mínima: login JWT simulado (tenant claim) + sync/operations + seed de OT de prueba.
using System.Text.Json;
using SpikeBackend.Application;
using SpikeBackend.Infrastructure;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
var json = new JsonSerializerOptions(JsonSerializerDefaults.Web);

await Database.MigrateAsync();

// Login mínimo: devuelve "token" = tenantId:userId (solo para la Spike; producción usa OIDC, Doc 26)
app.MapPost("/auth/login", (LoginRequest req) =>
    Results.Ok(new { token = $"{req.TenantId}:{req.UserId}" }));

// Contexto de tenant desde el token (simulación del pipeline MT-4)
Guid TenantOf(HttpRequest r)
{
    var h = r.Headers.Authorization.ToString().Replace("Bearer ", "");
    return Guid.Parse(h.Split(':')[0]);
}
Guid ActorOf(HttpRequest r)
{
    var h = r.Headers.Authorization.ToString().Replace("Bearer ", "");
    return Guid.Parse(h.Split(':')[1]);
}

// Crear OT de prueba (para iniciar J-2)
app.MapPost("/seed/work-order", async (HttpRequest r) =>
{
    var id = Guid.NewGuid();
    var (con, tx) = await Database.BeginTenantTxAsync(TenantOf(r));
    await using (con)
    {
        await using var cmd = new Npgsql.NpgsqlCommand(
            "INSERT INTO work_orders (id, tenant_id, title) VALUES (@id, @t, @ti)", con, tx);
        cmd.Parameters.AddWithValue("id", id);
        cmd.Parameters.AddWithValue("t", TenantOf(r));
        cmd.Parameters.AddWithValue("ti", "OT Spike J-2 — cambio de rodamiento");
        await cmd.ExecuteNonQueryAsync();
        foreach (var label in new[] { "Desmontar guarda", "Extraer rodamiento", "Montar rodamiento nuevo", "Torque final" })
        {
            await using var c2 = new Npgsql.NpgsqlCommand(
                "INSERT INTO wo_items (id, tenant_id, work_order_id, label) VALUES (@i, @t, @w, @l)", con, tx);
            c2.Parameters.AddWithValue("i", Guid.NewGuid());
            c2.Parameters.AddWithValue("t", TenantOf(r));
            c2.Parameters.AddWithValue("w", id);
            c2.Parameters.AddWithValue("l", label);
            await c2.ExecuteNonQueryAsync();
        }
        await tx.CommitAsync();
    }
    return Results.Ok(new { workOrderId = id });
});

// Estado actual de la OT (para que el supervisor genere el conflicto)
app.MapGet("/work-orders/{id}", async (Guid id, HttpRequest r) =>
{
    var (con, tx) = await Database.BeginTenantTxAsync(TenantOf(r));
    await using (con)
    {
        await using var cmd = new Npgsql.NpgsqlCommand(
            "SELECT title, state, version, deleted_at FROM work_orders WHERE id=@id", con, tx);
        cmd.Parameters.AddWithValue("id", id);
        await using var rd = await cmd.ExecuteReaderAsync();
        if (!await rd.ReadAsync()) return Results.NotFound();
        return Results.Ok(new
        {
            title = rd.GetString(0), state = rd.GetString(1),
            version = rd.GetInt32(2), deleted = !rd.IsDBNull(3)
        });
    }
});

// Núcleo: write-path de sincronización (SY-5/8/9)
app.MapPost("/sync/operations", async (HttpRequest r) =>
{
    var tenant = TenantOf(r);
    var ops = await r.ReadFromJsonAsync<List<SyncOperation>>(json);
    if (ops is null || ops.Count == 0) return Results.BadRequest();
    var sw = System.Diagnostics.Stopwatch.StartNew();
    var results = await SyncWritePath.ProcessAsync(tenant, ops);
    sw.Stop();
    return Results.Ok(new
    {
        processed = results.Count,
        serverLatencyMs = sw.ElapsedMilliseconds,
        verdicts = results
    });
});

app.Run();

record LoginRequest(Guid TenantId, Guid UserId);
