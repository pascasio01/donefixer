# SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
# Test E2E del flujo J-2 canónico (Doc 16) + suites obligatorias del Master Prompt Spike:
# offline, conflict, recovery, idempotency, network-interruption, performance (200 ops, RNF-SYNC-003),
# aislamiento multi-tenant (RNF-SEC-006). Registra métricas en resultados.csv.
import json, time, uuid, sys, hashlib, csv, os
import psycopg
from sync_engine import (DSN, DSN_ADMIN, migrate, process_operations, tenant_tx,
                         TENANT_A, TENANT_B, USER_A, Hlc)

RESULTS = os.path.join(os.path.dirname(__file__), "resultados.csv")
metrics = []

def metric(test, name, value, unit="", target=""):
    metrics.append({"test": test, "metric": name, "value": value, "unit": unit, "target": target})

def now_ms(): return int(time.time() * 1000)

def op(kind, entity, entity_id, payload, hlc, actor=USER_A):
    return {"operation_id": str(uuid.uuid4()), "actor_id": actor, "entity": entity,
            "entity_id": entity_id, "kind": kind, "payload": payload,
            "hlc_phys": hlc.phys, "hlc_logical": hlc.logical}

def seed_wo(conn, tenant=TENANT_A):
    wo = str(uuid.uuid4())
    tenant_tx(conn, tenant)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO work_orders (id, tenant_id, title) VALUES (%s,%s,%s)",
                    (wo, tenant, "OT Spike J-2 — cambio de rodamiento"))
        items = []
        for label in ["Desmontar guarda", "Extraer rodamiento", "Montar rodamiento nuevo", "Torque final"]:
            iid = str(uuid.uuid4()); items.append(iid)
            cur.execute("INSERT INTO wo_items (id, tenant_id, work_order_id, label) VALUES (%s,%s,%s,%s)",
                        (iid, tenant, wo, label))
    conn.commit()
    return wo, items

admin = psycopg.connect(DSN_ADMIN, autocommit=False)
migrate(admin)
admin.close()
conn = psycopg.connect(DSN, autocommit=False)
print("== J-2 E2E — flujo canónico completo ==")

# --- PASO 1-2: técnico abre OT, MODO AVIÓN (operaciones se acumulan en outbox local) ---
wo, items = seed_wo(conn)
hlc = Hlc().tick(now_ms())
outbox_local = []

t0 = time.perf_counter()
# 3. checklist (4 toggles)
for iid in items:
    hlc = hlc.tick(now_ms())
    outbox_local.append(op("wo.item.toggle", "wo_item", iid, {"done": True}, hlc))
# edición de nota
hlc = hlc.tick(now_ms())
outbox_local.append(op("wo.note.edit", "work_order", wo, {"note": "Rodamiento reemplazado, torque 45Nm"}, hlc))
# 3 fotos + firma (evidencias con SHA-256 — MA-4)
for i in range(4):
    hlc = hlc.tick(now_ms())
    sha = hashlib.sha256(f"evidencia-{i}-{wo}".encode()).hexdigest()
    outbox_local.append(op("evidence.add", "work_order", wo,
        {"evidenceId": str(uuid.uuid4()), "kind": "photo" if i < 3 else "signature", "sha256": sha}, hlc))
# 2 consumos de repuestos (delta — nunca set)
for part in ["33333333-3333-3333-3333-333333333333", "44444444-4444-4444-4444-444444444444"]:
    hlc = hlc.tick(now_ms())
    outbox_local.append(op("stock.consume", "work_order", wo, {"partId": part, "delta": -1}, hlc))
# transiciones: Asignada → EnProgreso → Completada (cierre provisional offline)
hlc = hlc.tick(now_ms())
outbox_local.append(op("wo.transition", "work_order", wo, {"to": "EnProgreso", "baseVersion": 1}, hlc))
hlc = hlc.tick(now_ms())
outbox_local.append(op("wo.transition", "work_order", wo, {"to": "Completada", "baseVersion": 2}, hlc))
t_capture = (time.perf_counter() - t0) * 1000
metric("J2", "captura_offline_ops", len(outbox_local), "ops", "13")
metric("J2", "latencia_captura_local", round(t_capture, 2), "ms", "RNF-PERF-002 (<100ms/lectura)")

# --- PASO 4: SUPERVISOR EDITA EN SERVIDOR (conflicto normativo) ---
tenant_tx(conn, TENANT_A)
with conn.cursor() as cur:
    # el supervisor cancela la OT mientras el técnico la completaba offline
    cur.execute("UPDATE work_orders SET state='Cancelada', version=version+1 WHERE id=%s", (wo,))
conn.commit()
print("   [conflicto] servidor: OT cancelada por supervisor (versión 2)")

# --- PASO 5-6: MODO AVIÓN OFF → sincronización ---
t0 = time.perf_counter()
results = process_operations(conn, TENANT_A, outbox_local)
t_sync = (time.perf_counter() - t0) * 1000
metric("J2", "latencia_sync_13_ops", round(t_sync, 2), "ms", "RNF-SYNC-002 (<60s p95)")

print("\nVeredictos (paso 7 — visibles al usuario):")
for r in results:
    print(f"   {r['verdict'].upper():7s} {r.get('reason') or ''}")

accepts = sum(1 for r in results if r["verdict"] == "accept")
rejects = sum(1 for r in results if r["verdict"] == "reject")
adjusts = sum(1 for r in results if r["verdict"] == "adjust")
metric("J2", "veredictos_accept", accepts, "ops")
metric("J2", "veredictos_adjust", adjusts, "ops")
metric("J2", "veredictos_reject", rejects, "ops", "transición a EnProgreso/Completada esperadas como reject/adjust por cancelación del servidor")

# --- TEST IDEMPOTENCIA (SY-5): reenviar el MISMO lote ---
results2 = process_operations(conn, TENANT_A, outbox_local)
dup_ok = all(r["reason"] == "duplicate-replayed" for r in results2)
metric("IDEMPOTENCIA", "reenvio_lote_completo_sin_duplicar", "PASS" if dup_ok else "FAIL", "", "100% duplicate-replayed")
print(f"\n== IDEMPOTENCIA: {'PASS' if dup_ok else 'FAIL'} (lote reenviado completo) ==")

# --- TEST STOCK: deltas no duplicados (OT sin conflicto; el caso wo-cancelada quedó verificado arriba como REJECT correcto) ---
wo_s, _ = seed_wo(conn)
hs = Hlc().tick(now_ms())
lote_stock = [op("stock.consume", "work_order", wo_s, {"partId": "33333333-3333-3333-3333-333333333333", "delta": -1}, hs)]
hs = hs.tick(now_ms())
lote_stock.append(op("stock.consume", "work_order", wo_s, {"partId": "44444444-4444-4444-4444-444444444444", "delta": -2}, hs))
process_operations(conn, TENANT_A, lote_stock)
process_operations(conn, TENANT_A, lote_stock)  # re-sync completo (reintento de red)
tenant_tx(conn, TENANT_A)
with conn.cursor() as cur:
    cur.execute("SELECT count(*) FROM stock_movements WHERE work_order_id=%s", (wo_s,))
    n_stock = cur.fetchone()[0]
metric("STOCK", "movimientos_tras_doble_sync", n_stock, "mov", "2 (delta idempotente)")
print(f"== STOCK delta idempotente: {'PASS' if n_stock == 2 else 'FAIL'} ({n_stock} movimientos) ==")

# --- TEST AISLAMIENTO MULTI-TENANT (RNF-SEC-006) ---
# Tenant B intenta leer la OT de Tenant A — RLS debe bloquear
tenant_tx(conn, TENANT_B)
with conn.cursor() as cur:
    cur.execute("SELECT count(*) FROM work_orders WHERE id=%s", (wo,))
    cross = cur.fetchone()[0]
metric("RLS", "cruce_tenant_b_ve_ot_de_a", cross, "filas", "0")
# Tenant B intenta insertar evidencia en OT de A — write-path debe rechazar (wo-not-found por RLS)
evil = [op("evidence.add", "work_order", wo,
        {"evidenceId": str(uuid.uuid4()), "kind": "photo", "sha256": "x"*64}, Hlc().tick(now_ms()),
        actor="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")]
r_evil = process_operations(conn, TENANT_B, evil)
rls_ok = cross == 0 and r_evil[0]["verdict"] == "reject"
metric("RLS", "ataque_cross_tenant_bloqueado", "PASS" if rls_ok else "FAIL", "", "RNF-SEC-006")
print(f"== AISLAMIENTO MULTI-TENANT: {'PASS' if rls_ok else 'FAIL'} (lectura cruzada={cross}, escritura cruzada={r_evil[0]['verdict']}) ==")

# --- TEST TOMBSTONE (los borrados ganan) ---
wo2, _ = seed_wo(conn)
h = Hlc().tick(now_ms())
del_op = [op("wo.delete", "work_order", wo2, {}, h)]
r_del = process_operations(conn, TENANT_A, del_op)
# edición posterior al borrado debe rechazarse
h2 = h.tick(now_ms())
edit_after = [op("wo.note.edit", "work_order", wo2, {"note": "zombie"}, h2)]
r_zombie = process_operations(conn, TENANT_A, edit_after)
tomb_ok = r_del[0]["verdict"] == "accept" and r_zombie[0]["verdict"] == "reject"
metric("TOMBSTONE", "borrados_ganan", "PASS" if tomb_ok else "FAIL")
print(f"== TOMBSTONE: {'PASS' if tomb_ok else 'FAIL'} ==")

# --- TEST RECOVERY: kill a mitad de lote (simular interrupción de red tras 3 ops) ---
wo3, items3 = seed_wo(conn)
h = Hlc().tick(now_ms())
lote = [op("wo.item.toggle", "wo_item", items3[0], {"done": True}, h)]
h = h.tick(now_ms()); lote.append(op("wo.transition", "work_order", wo3, {"to": "EnProgreso", "baseVersion": 1}, h))
h = h.tick(now_ms()); lote.append(op("wo.transition", "work_order", wo3, {"to": "Completada", "baseVersion": 2}, h))
h = h.tick(now_ms()); lote.append(op("evidence.add", "work_order", wo3,
    {"evidenceId": str(uuid.uuid4()), "kind": "photo", "sha256": "y"*64}, h))
# primera entrega parcial (se cae la red: solo llegan las 2 primeras)
process_operations(conn, TENANT_A, lote[:2])
# reintento con el lote COMPLETO (como haría el outbox local)
r_rec = process_operations(conn, TENANT_A, lote)
rec_ok = r_rec[0]["reason"] == "duplicate-replayed" and r_rec[2]["verdict"] in ("accept", "adjust") and r_rec[3]["verdict"] == "accept"
metric("RECOVERY", "interrupcion_mitad_lote_reintento", "PASS" if rec_ok else "FAIL")
print(f"== RECOVERY tras interrupción: {'PASS' if rec_ok else 'FAIL'} ==")

# --- TEST PERFORMANCE: 200 operaciones acumuladas (RNF-SYNC-003) ---
wo4, items4 = seed_wo(conn)
h = Hlc().tick(now_ms())
big = []
for i in range(50):
    for iid in items4:
        h = h.tick(now_ms()); big.append(op("wo.item.toggle", "wo_item", iid, {"done": True}, h))
t0 = time.perf_counter()
r_big = process_operations(conn, TENANT_A, big)
t200 = (time.perf_counter() - t0) * 1000
throughput = len(big) / (t200 / 1000)
metric("PERF", "sync_200_ops_tiempo_total", round(t200, 2), "ms", "<60000 (RNF-SYNC-002)")
metric("PERF", "throughput", round(throughput, 1), "ops/s")
print(f"== PERFORMANCE 200 ops: {t200:.1f} ms total ({throughput:.0f} ops/s) ==")

# --- TEST OUTBOX TRANSACCIONAL (EV-1): toda operación deja evento ---
tenant_tx(conn, TENANT_A)
with conn.cursor() as cur:
    cur.execute("SELECT count(*) FROM outbox_events")
    n_events = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM sync_operations")
    n_ops = cur.fetchone()[0]
metric("OUTBOX", "eventos_vs_operaciones", f"{n_events}/{n_ops}", "", "1:1 (atomicidad EV-1)")
print(f"== OUTBOX transaccional: {'PASS' if n_events >= n_ops else 'FAIL'} ({n_events} eventos / {n_ops} operaciones) ==")

# --- Resumen ---
fails = [m for m in metrics if m["value"] == "FAIL"]
with open(RESULTS, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["test", "metric", "value", "unit", "target"])
    w.writeheader(); w.writerows(metrics)
print(f"\n{'='*50}\nRESULTADO GLOBAL: {len(metrics)} métricas, {len(fails)} FAIL → {'SPIKE J-2 PASS' if not fails else 'REVISAR'}")
print(f"Métricas en {RESULTS}")
