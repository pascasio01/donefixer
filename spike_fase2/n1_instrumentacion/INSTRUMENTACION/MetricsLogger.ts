// SPIKE N-1 — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01 / DC-10). No es código de producción.
// MetricsLogger — contrato único de métricas para la app RN + Expo (espejo: MetricsLogger.dart).
// Salida CSV canónica: timestamp_ms,evento,detalle,valor,unidad

export type MetricEvento =
  | 'cold_start_start' | 'first_interactive' | 'wo_open' | 'j2_offline_start'
  | 'j2_step' | 'airplane_off' | 'sync_first_op_sent' | 'sync_last_verdict'
  | 'sync_verdict' | 'mem_rss_mb' | 'export_done';

interface MetricRow {
  timestampMs: number;
  evento: MetricEvento;
  detalle: string;
  valor: number;
  unidad: string;
}

class MetricsLogger {
  static readonly instance = new MetricsLogger();
  private readonly rows: MetricRow[] = [];
  private readonly t0 = Date.now();

  private mark(evento: MetricEvento, detalle = '', valor = 0, unidad = ''): void {
    this.rows.push({ timestampMs: Date.now() - this.t0, evento, detalle, valor, unidad });
  }

  /** Arranque en frío: llamar en el entry point lo antes posible. */
  coldStart(): void { this.mark('cold_start_start'); }

  /** Primera pantalla interactiva (login usable). */
  firstInteractive(): void { this.mark('first_interactive'); }

  /** Paso del guion J-2 (nombre exacto del paso, idéntico al de Flutter). */
  j2Step(nombre: string): void { this.mark('j2_step', nombre.replace(/,/g, ';')); }

  /** Veredicto de una operación sincronizada (SY-9). */
  syncVerdict(operationId: string, verdict: string, reason: string): void {
    this.mark('sync_verdict', `${operationId}|${verdict}|${reason}`);
  }

  /** CSV canónico, idéntico formato al de Flutter. */
  toCsv(): string {
    const lines = this.rows.map(
      (r) => `${r.timestampMs},${r.evento},${r.detalle.replace(/,/g, ';')},${r.valor},${r.unidad}`,
    );
    return ['timestamp_ms,evento,detalle,valor,unidad', ...lines].join('\n');
  }
}

export default MetricsLogger;
