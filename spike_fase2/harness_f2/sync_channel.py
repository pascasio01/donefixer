# SPIKE FASE 2 — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01 / DC-03). No es código de producción.
"""Canal de réplica parametrizable para Fase 2 (N-2).

La ÚNICA variable controlada entre Entorno A y Entorno B es el servicio PowerSync.
Todo lo demás (PostgreSQL, write-path, dominio, dataset, RLS, casos) es idéntico.

Configuración por variables de entorno (ver config/entorno_*.env):
  F2_ENV_LABEL      "A" (Cloud) | "B" (Self-Hosted) | "CONTROL" (sin PowerSync)
  PS_ENDPOINT       URL del servicio PowerSync (Cloud: https://<inst>.powersync.journeyapps.com)
  PS_TOKEN          token JWT de desarrollo del servicio
  PS_MODE           "powersync" | "control"

Modo CONTROL: valida que la batería F2 es ejecutable end-to-end sin PowerSync
(el write-path de Fase 1 ya validado actúa de canal directo). Sirve para:
  - verificar la batería antes de gastar tiempo de entorno real;
  - tener línea base de rendimiento del write-path puro para aislar
    el coste/latencia que añade cada alternativa PowerSync.
"""
import os, time, json, urllib.request, urllib.error

ENV_LABEL = os.environ.get("F2_ENV_LABEL", "CONTROL")
PS_ENDPOINT = os.environ.get("PS_ENDPOINT", "").rstrip("/")
PS_TOKEN = os.environ.get("PS_TOKEN", "")
PS_MODE = os.environ.get("PS_MODE", "control")


class ChannelError(Exception):
    """Fallo del canal de réplica (red, servidor caído, token inválido)."""


class BaseChannel:
    """Contrato del canal de réplica (lado descarga: servidor → cliente)."""
    label = "base"

    def checkpoint(self) -> dict:
        """Estado actual del stream (checkpoint PowerSync o equivalente)."""
        raise NotImplementedError

    def fetch_changes(self, since: str | None) -> dict:
        """Descarga cambios desde un checkpoint. Devuelve {ops, next_checkpoint}."""
        raise NotImplementedError

    def health(self) -> dict:
        raise NotImplementedError


class ControlChannel(BaseChannel):
    """Canal directo: lee el outbox de PostgreSQL (sin PowerSync). Línea base."""
    label = "CONTROL"

    def __init__(self, dsn):
        import psycopg
        self._dsn = dsn
        self._conn_factory = psycopg.connect

    def checkpoint(self):
        with self._conn_factory(self._dsn) as c, c.cursor() as cur:
            cur.execute("SELECT COALESCE(MAX(id),0) FROM outbox_events")
            return {"checkpoint": str(cur.fetchone()[0])}

    def fetch_changes(self, since):
        with self._conn_factory(self._dsn) as c, c.cursor() as cur:
            cur.execute(
                "SELECT id, event_type, payload FROM outbox_events WHERE id > %s ORDER BY id",
                (int(since or 0),))
            rows = cur.fetchall()
        return {"ops": [{"id": r[0], "type": r[1], "payload": r[2]} for r in rows],
                "next_checkpoint": str(rows[-1][0]) if rows else (since or "0")}

    def health(self):
        try:
            cp = self.checkpoint()
            return {"ok": True, "checkpoint": cp["checkpoint"]}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "error": str(e)}


class PowerSyncChannel(BaseChannel):
    """Canal PowerSync real (A=Cloud o B=Self-Hosted según PS_ENDPOINT).

    Usa la API HTTP de PowerSync (/sync/stream sería SSE; aquí se usa polling
    de checkpoint para medición reproducible sin SDK nativo en el sandbox).
    """
    label = ENV_LABEL

    def _req(self, path, timeout=30):
        url = f"{PS_ENDPOINT}{path}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {PS_TOKEN}"})
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = json.loads(r.read().decode() or "{}")
            return body, (time.perf_counter() - t0) * 1000
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            raise ChannelError(str(e)) from e

    def checkpoint(self):
        body, _ = self._req("/write-checkpoint2")
        return body

    def fetch_changes(self, since):
        # Endpoint de diagnóstico; en Carril B se medirá también vía SDK oficial.
        body, ms = self._req("/sync/stream" if since else "/write-checkpoint2")
        body["_latency_ms"] = ms
        return body

    def health(self):
        try:
            body, ms = self._req("/probe/liveness", timeout=10)
            return {"ok": True, "latency_ms": round(ms, 2), "body": body}
        except ChannelError as e:
            return {"ok": False, "error": str(e)}


def make_channel(dsn) -> BaseChannel:
    if PS_MODE == "powersync":
        if not PS_ENDPOINT or not PS_TOKEN:
            raise SystemExit("F2: PS_MODE=powersync requiere PS_ENDPOINT y PS_TOKEN")
        return PowerSyncChannel()
    return ControlChannel(dsn)
