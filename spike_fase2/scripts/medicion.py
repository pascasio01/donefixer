# SPIKE FASE 2 — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01 / DC-03). No es código de producción.
"""Scripts de medición F2 — ejecutables idénticos sobre Entorno A y Entorno B.

Uso (Carril B, desde el host de medición):
    set -a; source ../config/entorno_a_cloud.env; set +a
    python3 medicion.py latencia --iteraciones 50
    python3 medicion.py reconexion --cortes 10
    python3 medicion.py throughput --usuarios 100 --ops-por-usuario 20
    python3 medicion.py recursos --duracion-s 120        # CPU/mem/red del proceso servicio
    python3 medicion.py chaos --escenario kill_durante_sync

Toda salida se anexa a resultados_f2.csv con clasificación y referencia de evidencia.
Regla: sin Anexo de Reproducibilidad, la métrica no fundamenta el cierre de N-2.
"""
import argparse, csv, os, statistics, sys, time

RESULTS = os.path.join(os.path.dirname(__file__), "..", "harness_f2", "resultados_f2.csv")
ENV_LABEL = os.environ.get("F2_ENV_LABEL", "CONTROL")

def registrar(caso, nombre, valor, unidad, clasif, evid=""):
    fila = {"caso_id": caso, "entorno": ENV_LABEL, "metrica": nombre, "valor": valor,
            "unidad": unidad, "clasificacion": clasif, "evidencia_ref": evid}
    existe = os.path.exists(RESULTS)
    with open(RESULTS, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fila.keys()))
        if not existe: w.writeheader()
        w.writerow(fila)
    print(f"[{ENV_LABEL}] {caso} {nombre} = {valor} {unidad} ({clasif})")

def percentiles(muestras):
    s = sorted(muestras)
    def p(q): return s[min(len(s) - 1, int(q * len(s)))]
    return round(p(0.50), 2), round(p(0.95), 2), round(p(0.99), 2)

def medir_latencia(iteraciones):
    """Latencia del canal: checkpoint + descarga, p50/p95/p99 (F2-IT-01)."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "harness_f2"))
    from sync_channel import make_channel
    ch = make_channel(os.environ.get("F2_DSN", "postgresql://app_spike:spike@/spike?host=/tmp/pgtest"))
    m = []
    for _ in range(iteraciones):
        t0 = time.perf_counter(); ch.fetch_changes(None); m.append((time.perf_counter() - t0) * 1000)
        time.sleep(0.05)
    p50, p95, p99 = percentiles(m)
    registrar("F2-IT-01", "latencia_canal_p50", p50, "ms", "DC", f"medicion.py latencia n={iteraciones}")
    registrar("F2-IT-01", "latencia_canal_p95", p95, "ms", "DC", f"medicion.py latencia n={iteraciones}")
    registrar("F2-IT-01", "latencia_canal_p99", p99, "ms", "DC", f"medicion.py latencia n={iteraciones}")

def medir_reconexion(cortes):
    """Tiempo de reconexión tras corte simulado (F2-CH-01/03). Carril B."""
    print("Carril B: ejecutar con el cliente real — cortar red (iptables/airplane), medir")
    print("tiempo desde restauración hasta primer checkpoint confirmado, por ciclo.")
    registrar("F2-CH-03", "reconexion_ciclos", cortes, "ciclos", "PD", "pendiente entorno real")

def medir_throughput(usuarios, ops_por_usuario):
    """Carga N usuarios (F2-LT-*). 100/1.000 en Carril B; 10.000 simulado = SU."""
    clasif = "SU" if usuarios >= 10000 else "DC"
    print(f"Carril B: lanzar {usuarios} clientes × {ops_por_usuario} ops contra el entorno activo.")
    registrar(f"F2-LT", "carga_configurada", f"{usuarios}u x {ops_por_usuario}ops", "", clasif,
              "medicion.py throughput — ejecutar en entorno real")

def medir_recursos(duracion_s):
    """CPU/mem/red del servicio (docker stats / métricas Cloud). Carril B."""
    print("Carril B (self-hosted): docker stats powersync --no-stream cada 5 s durante", duracion_s, "s")
    print("Carril B (cloud): métricas del dashboard; declarar método en el Anexo (clasif SU).")
    registrar("F2-LR-01", "recursos_ventana_s", duracion_s, "s", "PD", "pendiente entorno real")

def chaos(escenario):
    """F2-CH-*: kill_durante_sync | reinicio_servidor | flapping. Carril B."""
    guiones = {
        "kill_durante_sync": "iniciar sync de 1.000 ops; al 50% cortar red 30 s; restaurar; verificar 0 duplicados y convergencia",
        "reinicio_servidor": "durante sync continuo: docker restart powersync (B) / nota: en Cloud no aplica — registrar como N/A con justificación",
        "flapping": "10 ciclos de 10 s corte / 10 s restauración durante sync continuo",
    }
    print(f"F2-CH {escenario}: {guiones.get(escenario, 'escenario desconocido')}")
    registrar("F2-CH", f"chaos_{escenario}", "guión emitido", "", "PD", "pendiente entorno real")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("latencia"); p.add_argument("--iteraciones", type=int, default=50)
    p = sub.add_parser("reconexion"); p.add_argument("--cortes", type=int, default=10)
    p = sub.add_parser("throughput"); p.add_argument("--usuarios", type=int, default=100); p.add_argument("--ops-por-usuario", type=int, default=20)
    p = sub.add_parser("recursos"); p.add_argument("--duracion-s", type=int, default=120)
    p = sub.add_parser("chaos"); p.add_argument("--escenario", required=True)
    a = ap.parse_args()
    {"latencia": lambda: medir_latencia(a.iteraciones),
     "reconexion": lambda: medir_reconexion(a.cortes),
     "throughput": lambda: medir_throughput(a.usuarios, a.ops_por_usuario),
     "recursos": lambda: medir_recursos(a.duracion_s),
     "chaos": lambda: chaos(a.escenario)}[a.cmd]()
