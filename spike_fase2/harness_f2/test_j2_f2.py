# SPIKE FASE 2 — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01 / DC-03). No es código de producción.
"""Batería F2 (N-2): misma lógica J-2 que Fase 1 (mismo contrato de ops del
write-path validado), ejecutada sobre el canal parametrizable
(A=Cloud, B=Self-Hosted, CONTROL=línea base write-path).

Casos ejecutables en sandbox (modo CONTROL): F2-IT-01, F2-OT-01, F2-CT-01,
F2-CT-04, idempotencia, RLS, F2-LT-01.
Casos Carril B (entorno PowerSync real): F2-CH-*, F2-RT-01, F2-FT-01,
F2-LR-01, F2-LT-02..04 — se marcan SKIP con motivo registrado.

Salida: resultados_f2.csv (caso_id, entorno, metrica, valor, unidad, clasificacion, evidencia_ref).
Uso:  F2_ENV_LABEL=CONTROL python3 test_j2_f2.py
"""
import csv, json, os, sys, time, uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../spike/harness"))
sys.path.insert(0, os.path.dirname(__file__))

from sync_engine import (DSN, DSN_ADMIN, migrate, process_operations, tenant_tx,  # noqa: E402
                         TENANT_A, TENANT_B, USER_A, Hlc)
from sync_channel import make_channel, ENV_LABEL, PS_MODE  # noqa: E402
import psycopg  # noqa: E402

RESULTS = os.path.join(os.path.dirname(__file__), "resultados_f2.csv")
metrics, skips, fails = [], [], []

def metric(case, name, value, unit="", clasif="DC", evid=""):
    metrics.append({"caso_id": case, "entorno": ENV_LABEL, "metrica": name, "valor": value,
                    "unidad": unit, "clasificacion": clasif, "evidencia_ref": evid})

def check(case, cond, detalle):
    estado = "PASS" if cond else "FAIL"
    if not cond: fails.append(case)
    print(f"  {case}: {estado} — {detalle}")

def skip(case, motivo):
    skips.append({"caso_id": case, "entorno": ENV_LABEL, "motivo": motivo})
    print(f"  SKIP {case}: {motivo}")

def now_ms(): return int(time.time() * 1000)

class OpGen:
    """Generador de operaciones J-2 con el contrato exacto del write-path (Fase 1)."""
    def __init__(self): self.hlc = Hlc().tick(now_ms())
    def _op(self, kind, entity, entity_id, payload, actor=USER_A):
        self.hlc = self.hlc.tick(now_ms())
        return {"operation_id": str(uuid.uuid4()), "actor_id": actor, "entity": entity,
                "entity_id": entity_id, "kind": kind, "payload": payload,
                "hlc_phys": self.hlc.phys, "hlc_logical": self.hlc.logical}
    def toggle(self, item_id, done=True): return self._op("wo.item.toggle", "wo_item", item_id, {"done": done})
    def evidence(self, wo): return self._op("evidence.add", "work_order", wo,
        {"evidenceId": str(uuid.uuid4()), "kind": "photo", "sha256": uuid.uuid4().hex, "note": "rodamiento montado"})
    def transition(self, wo, to, base): return self._op("wo.transition", "work_order", wo, {"to": to, "baseVersion": base})
    def stock(self, wo, part, delta): return self._op("stock.consume", "work_order", wo, {"partId": part, "delta": delta})
    def note(self, wo, text): return self._op("wo.note.edit", "work_order", wo, {"note": text})
    def delete_wo(self, wo): return self._op("wo.delete", "work_order", wo, {})

def seed_wo(conn, tenant=TENANT_A, title="OT F2 — J-2"):
    wo = str(uuid.uuid4()); tenant_tx(conn, tenant)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO work_orders (id, tenant_id, title) VALUES (%s,%s,%s)", (wo, tenant, title))
        items = []
        for label in ["Desmontar guarda", "Extraer rodamiento", "Montar rodamiento nuevo", "Torque final"]:
            iid = str(uuid.uuid4()); items.append(iid)
            cur.execute("INSERT INTO wo_items (id, tenant_id, work_order_id, label) VALUES (%s,%s,%s,%s)",
                        (iid, tenant, wo, label))
    conn.commit(); return wo, items

def wo_version(conn, wo):
    with conn.cursor() as cur:
        tenant_tx(conn, TENANT_A)
        cur.execute("SELECT version, state FROM work_orders WHERE id=%s", (wo,))
        v, s = cur.fetchone()
    conn.rollback(); return v, s

admin = psycopg.connect(DSN_ADMIN); migrate(admin); admin.close()
conn = psycopg.connect(DSN)
channel = make_channel(DSN)
print(f"== SPIKE F2 — batería J-2 | entorno={ENV_LABEL} modo={PS_MODE} ==")

# ---------- F2-IT-01 / F2-OT-01: J-2 offline completo, 13 operaciones ----------
g = OpGen()
wo, items = seed_wo(conn)
outbox = [g.toggle(i) for i in items]                                   # 4 toggles (offline)
outbox.append(g.evidence(wo))                                           # 1 evidencia
outbox.append(g.transition(wo, "EnProgreso", base=1))                   # 1 transición
outbox += [g.stock(wo, "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", -1) for _ in range(6)]               # 6 consumos
outbox.append(g.transition(wo, "Completada", base=2))                   # 1 transición
assert len(outbox) == 13

t0 = time.perf_counter()
res = process_operations(conn, TENANT_A, outbox)
sync_ms = (time.perf_counter() - t0) * 1000
accepted = sum(1 for r in res if r["verdict"] in ("accept", "adjust"))
metric("F2-IT-01", "sync_13_ops_ms", round(sync_ms, 2), "ms", "DC", "write-path Fase 1 portado")
metric("F2-IT-01", "ops_aceptadas", accepted, "ops", "DC")
check("F2-IT-01", accepted == 13, f"13 ops en {sync_ms:.2f} ms, aceptadas={accepted}/13")

# ---------- Idempotencia: reenvío idéntico ----------
t0 = time.perf_counter()
res2 = process_operations(conn, TENANT_A, outbox)
idem_ms = (time.perf_counter() - t0) * 1000
dups = sum(1 for r in res2 if r["reason"] == "duplicate-replayed")
metric("F2-IT-01", "idempotencia_reenvio_ms", round(idem_ms, 2), "ms", "DC")
metric("F2-IT-01", "duplicados_detectados", dups, "ops", "DC")
check("F2-IT-01", dups == 13, f"idempotencia {dups}/13 duplicate-replayed")

# ---------- F2-CT-01: conflicto simultáneo (transición tardía, server-authoritative) ----------
v_now, s_now = wo_version(conn, wo)
res_c = process_operations(conn, TENANT_A, [g.transition(wo, "Cancelada", base=1)])
verd, reason = res_c[0]["verdict"], res_c[0]["reason"]
metric("F2-CT-01", "veredicto", verd, "", "DC"); metric("F2-CT-01", "motivo", reason, "", "DC")
check("F2-CT-01", verd == "reject" and "authoritative" in (reason or ""),
      f"Cancelada tardía sobre {s_now} -> {verd} ({reason})")

# ---------- RLS cross-tenant ----------
with conn.cursor() as cur:
    tenant_tx(conn, TENANT_B)
    cur.execute("SELECT COUNT(*) FROM work_orders WHERE id=%s", (wo,))
    visible = cur.fetchone()[0]
conn.rollback()
metric("F2-IT-01", "rls_filas_cruzadas", visible, "filas", "DC")
check("F2-IT-01", visible == 0, f"RLS cross-tenant: {visible} filas visibles")

# ---------- F2-CT-04: tombstone (deletes win) ----------
wo2, _ = seed_wo(conn, title="OT F2 — tombstone")
res_d = process_operations(conn, TENANT_A, [g.delete_wo(wo2), g.note(wo2, "edición concurrente tardía")])
v1, v2 = res_d[0]["verdict"], res_d[1]["verdict"]
metric("F2-CT-04", "veredicto_delete", v1, "", "DC"); metric("F2-CT-04", "veredicto_edicion_tardia", v2, "", "DC")
check("F2-CT-04", v1 == "accept" and v2 == "reject", f"delete={v1}, edición tardía={v2} (deletes win)")

# ---------- F2-LT-01: 10 usuarios simulados ----------
wo3, items3 = seed_wo(conn, title="OT F2 — carga")
t0 = time.perf_counter(); total = 0
for _ in range(10):
    gu = OpGen()
    ops = [gu.toggle(items3[i % 4], done=False) for i in range(20)]
    for o in ops: o["actor_id"] = str(uuid.uuid4())
    process_operations(conn, TENANT_A, ops); total += len(ops)
lt_ms = (time.perf_counter() - t0) * 1000
metric("F2-LT-01", "usuarios", 10, "u", "DC"); metric("F2-LT-01", "ops_totales", total, "ops", "DC")
metric("F2-LT-01", "duracion_ms", round(lt_ms, 2), "ms", "DC")
metric("F2-LT-01", "throughput", round(total / (lt_ms / 1000), 1), "ops/s", "DC")
check("F2-LT-01", total == 200, f"10u × 20ops = {total} ops en {lt_ms:.1f} ms ({total/(lt_ms/1000):.0f} ops/s)")

# ---------- Canal de réplica (línea base CONTROL / real en Carril B) ----------
h = channel.health()
clasif_canal = "DC" if PS_MODE == "powersync" else "SU"
metric("F2-IT-01", "canal_health_ok", h.get("ok"), "", clasif_canal,
       "PowerSync /probe" if PS_MODE == "powersync" else "control: línea base write-path, no mide PowerSync")
cp = channel.checkpoint()
t0 = time.perf_counter(); channel.fetch_changes(None)
dl_ms = (time.perf_counter() - t0) * 1000
metric("F2-IT-01", "canal_descarga_ms", round(dl_ms, 2), "ms", clasif_canal)
print(f"  Canal [{channel.label}]: health={h.get('ok')} checkpoint={cp} descarga={dl_ms:.1f} ms")

# ---------- Casos Carril B ----------
if PS_MODE != "powersync":
    for case, motivo in [
        ("F2-CH-01", "corte de red real a mitad de sync — requiere entorno PowerSync"),
        ("F2-CH-02", "reinicio del servidor PowerSync — requiere Docker/cuenta Cloud"),
        ("F2-CH-03", "flapping de red (10 ciclos) — requiere entorno real"),
        ("F2-CT-02", "conflictos múltiples ≥5 clientes — se ejecuta en Carril B con clientes reales"),
        ("F2-CT-03", "conflictos cruzados estado+evidencia+stock — Carril B"),
        ("F2-CT-05", "conflicto de edición mismo campo — Carril B"),
        ("F2-RT-01", "restauración desde backup — requiere entorno real"),
        ("F2-FT-01", "failover del canal — requiere entorno real"),
        ("F2-LR-01", "long running 2 h — requiere entorno real"),
        ("F2-LT-02", "100 usuarios — Carril B sobre ambos entornos"),
        ("F2-LT-03", "1.000 usuarios simulados — Carril B"),
        ("F2-LT-04", "10.000 usuarios simulados — Carril B, clasificación SU"),
    ]:
        skip(case, motivo)

# ---------- Salida ----------
exists = os.path.exists(RESULTS)
with open(RESULTS, "a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["caso_id", "entorno", "metrica", "valor", "unidad",
                                      "clasificacion", "evidencia_ref"])
    if not exists: w.writeheader()
    w.writerows(metrics)
print(f"\nResultado: {len(metrics)} métricas | FAIL={len(fails)} {fails} | SKIP(Carril B)={len(skips)}")
sys.exit(1 if fails else 0)
