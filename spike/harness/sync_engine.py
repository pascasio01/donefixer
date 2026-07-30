# SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
# Harness del write-path de sincronización (SY-5 idempotencia, SY-8 re-validación,
# SY-9 veredictos) — espejo funcional del backend .NET (Application/SyncWritePath.cs)
# para medición en este entorno (PostgreSQL 16 via socket Unix).
import json, time, uuid, psycopg

# Conexión con rol de APLICACIÓN (no superuser) para que RLS aplique de verdad (Doc 26 MT-3)
DSN = "postgresql://app_spike:spike@/spike?host=/tmp/pgtest"
DSN_ADMIN = "postgresql://postgres@/spike?host=/tmp/pgtest"  # solo migración/seed

TENANT_A = "11111111-1111-1111-1111-111111111111"
TENANT_B = "22222222-2222-2222-2222-222222222222"
USER_A   = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

# ---------- Dominio puro: máquina de estados OT (Doc 14, subset J-2) ----------
ALLOWED = {
    "Asignada":   ["EnProgreso", "Cancelada"],
    "EnProgreso": ["Completada", "Cancelada"],
    "Completada": ["Verificada"],
    "Verificada": ["Cerrada"],
    "Cerrada":    [],
    "Cancelada":  [],
}

def revalidate_transition(server_state, attempted):
    """ADR-011 v1.1: autoridad en el servidor. Devuelve (verdict, reason)."""
    if server_state == attempted:
        return "accept", "duplicate-transition"
    if attempted in ALLOWED.get(server_state, []):
        return "accept", None
    return "reject", f"server-state-{server_state}-authoritative"

# ---------- HLC (SY-6) ----------
class Hlc:
    def __init__(self, phys=0, logical=0):
        self.phys, self.logical = phys, logical
    def tick(self, now_ms):
        if now_ms > self.phys: return Hlc(now_ms, 0)
        return Hlc(self.phys, self.logical + 1)
    def merge(self, other, now_ms):
        mp = max(self.phys, other.phys, now_ms)
        if mp == self.phys and mp == other.phys: lg = max(self.logical, other.logical) + 1
        elif mp == self.phys: lg = self.logical + 1
        elif mp == other.phys: lg = other.logical + 1
        else: lg = 0
        return Hlc(mp, lg)
    def key(self): return (self.phys, self.logical)

# ---------- Migración (misma DDL que el backend .NET) ----------
DDL = open("/mnt/agents/output/donefixer/spike/harness/schema.sql").read()

def migrate(conn):
    with conn.cursor() as cur:
        cur.execute(DDL)
    conn.commit()

def tenant_tx(conn, tenant_id):
    """MT-4: set_config transaccional (PgBouncer-safe)."""
    with conn.cursor() as cur:
        cur.execute("SELECT set_config('app.current_tenant', %s, true)", (tenant_id,))

# ---------- Write-path ----------
def process_operations(conn, tenant_id, ops):
    tenant_tx(conn, tenant_id)
    results = []
    for op in sorted(ops, key=lambda o: (o["hlc_phys"], o["hlc_logical"])):
        results.append(process_one(conn, tenant_id, op))
    conn.commit()
    return results

def process_one(conn, tenant_id, op):
    with conn.cursor() as cur:
        # SY-5: idempotencia
        cur.execute("SELECT verdict FROM sync_operations WHERE operation_id=%s", (op["operation_id"],))
        row = cur.fetchone()
        if row:
            return {"operation_id": op["operation_id"], "verdict": row[0], "reason": "duplicate-replayed"}

        kind = op["kind"]
        if kind == "wo.transition":   verdict, reason, ver = h_transition(cur, op)
        elif kind == "wo.item.toggle":verdict, reason, ver = h_toggle(cur, op)
        elif kind == "evidence.add":  verdict, reason, ver = h_evidence(cur, tenant_id, op)
        elif kind == "stock.consume": verdict, reason, ver = h_stock(cur, tenant_id, op)
        elif kind == "wo.note.edit":  verdict, reason, ver = h_note(cur, op)
        elif kind == "wo.delete":     verdict, reason, ver = h_delete(cur, op)
        else: verdict, reason, ver = "reject", "unknown-kind", None

        cur.execute("""
            INSERT INTO sync_operations
              (operation_id, tenant_id, actor_id, entity, entity_id, kind, payload,
               hlc_phys, hlc_logical, verdict, verdict_reason, server_version)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (op["operation_id"], tenant_id, op["actor_id"], op["entity"], op["entity_id"],
             kind, json.dumps(op["payload"]), op["hlc_phys"], op["hlc_logical"],
             verdict, reason, ver))
        # EV-1: outbox en la MISMA transacción
        cur.execute("INSERT INTO outbox_events (tenant_id, event_type, payload) VALUES (%s,%s,%s)",
                    (tenant_id, f'{op["entity"]}.{kind}.{verdict}',
                     json.dumps({"operation_id": op["operation_id"], "entity_id": op["entity_id"], "verdict": verdict})))
        return {"operation_id": op["operation_id"], "verdict": verdict, "reason": reason, "server_version": ver}

def h_transition(cur, op):
    cur.execute("SELECT state, version FROM work_orders WHERE id=%s FOR UPDATE", (op["entity_id"],))
    row = cur.fetchone()
    if not row: return "reject", "wo-not-found", None
    state, version = row
    attempted = op["payload"]["to"]
    base_version = op["payload"]["baseVersion"]
    verdict, reason = revalidate_transition(state, attempted)
    if verdict == "reject":
        return "reject", reason, version
    if reason == "duplicate-transition":
        return "accept", reason, version
    new_version = version + 1
    adjusted = base_version != version
    cur.execute("UPDATE work_orders SET state=%s, version=%s, updated_at=now() WHERE id=%s",
                (attempted, new_version, op["entity_id"]))
    return ("adjust" if adjusted else "accept",
            "applied-on-newer-server-version" if adjusted else None, new_version)

def h_toggle(cur, op):
    cur.execute("UPDATE wo_items SET done=%s, version=version+1 WHERE id=%s",
                (op["payload"]["done"], op["entity_id"]))
    return ("accept", None, None) if cur.rowcount == 1 else ("reject", "item-not-found", None)

def h_evidence(cur, tenant_id, op):
    cur.execute("SELECT state FROM work_orders WHERE id=%s", (op["entity_id"],))
    row = cur.fetchone()
    if not row: return "reject", "wo-not-found", None
    if row[0] in ("Cerrada", "Cancelada"):
        return "reject", f'wo-{row[0]}-immutable-evidence', None  # RF-WO-003
    cur.execute("""
        INSERT INTO evidences (id, tenant_id, work_order_id, kind, sha256, note, hlc_phys, hlc_logical, created_by)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (op["payload"]["evidenceId"], tenant_id, op["entity_id"], op["payload"]["kind"],
         op["payload"]["sha256"], op["payload"].get("note"), op["hlc_phys"], op["hlc_logical"], op["actor_id"]))
    return "accept", None, None

def h_stock(cur, tenant_id, op):
    cur.execute("SELECT state FROM work_orders WHERE id=%s", (op["entity_id"],))
    row = cur.fetchone()
    if not row: return "reject", "wo-not-found", None
    if row[0] in ("Cerrada", "Cancelada"):
        return "reject", f'wo-{row[0]}-no-consumption', None
    cur.execute("""
        INSERT INTO stock_movements (id, tenant_id, work_order_id, part_id, delta, operation_id)
        VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (operation_id) DO NOTHING""",
        (str(uuid.uuid4()), tenant_id, op["entity_id"], op["payload"]["partId"],
         op["payload"]["delta"], op["operation_id"]))
    return "accept", None, None

def h_note(cur, op):
    cur.execute("UPDATE work_orders SET title=%s, version=version+1, updated_at=now() WHERE id=%s AND deleted_at IS NULL",
                (op["payload"]["note"], op["entity_id"]))
    return ("accept", None, None) if cur.rowcount == 1 else ("reject", "wo-not-found-or-deleted", None)

def h_delete(cur, op):
    cur.execute("UPDATE work_orders SET deleted_at=now(), version=version+1 WHERE id=%s", (op["entity_id"],))
    return ("accept", "tombstone-applied", None) if cur.rowcount == 1 else ("reject", "wo-not-found", None)
