// SPIKE N-1 — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01 / DC-10). No es código de producción.
// MetricsLogger — contrato único de métricas para la app Flutter (espejo: MetricsLogger.ts).
// Salida CSV canónica: timestamp_ms,evento,detalle,valor,unidad
import 'dart:io';
import 'dart:convert';

class MetricRow {
  final int timestampMs;
  final String evento;   // cold_start_start | first_interactive | wo_open | j2_offline_start |
                         // j2_step | airplane_off | sync_first_op_sent | sync_last_verdict |
                         // sync_verdict | mem_rss_mb | export_done
  final String detalle;  // p.ej. nombre del paso J-2 o operation_id
  final num valor;
  final String unidad;
  const MetricRow(this.timestampMs, this.evento, this.detalle, this.valor, this.unidad);

  String toCsv() => '$timestampMs,$evento,${detalle.replaceAll(',', ';')},$valor,$unidad';
}

class MetricsLogger {
  static final MetricsLogger instance = MetricsLogger._();
  MetricsLogger._();
  final List<MetricRow> _rows = [];
  final _sw = Stopwatch()..start();

  /// Marca un evento con el reloj monotónico de la app (ms desde arranque del logger).
  void mark(String evento, {String detalle = '', num valor = 0, String unidad = ''}) {
    _rows.add(MetricRow(_sw.elapsedMilliseconds, evento, detalle, valor, unidad));
  }

  /// Arranque en frío: llamar en main() lo antes posible.
  void coldStart() => mark('cold_start_start');

  /// Primera pantalla interactiva (login usable).
  void firstInteractive() => mark('first_interactive');

  /// Veredicto de una operación sincronizada (SY-9).
  void syncVerdict(String operationId, String verdict, String reason) =>
      mark('sync_verdict', detalle: '$operationId|$verdict|$reason');

  /// Exporta el CSV canónico a un archivo compartible. Devuelve la ruta.
  Future<String> exportCsv(Directory dir) async {
    mark('export_done');
    final f = File('${dir.path}/metricas_n1_flutter_${DateTime.now().toIso8601String()}.csv');
    final sb = StringBuffer('timestamp_ms,evento,detalle,valor,unidad\n');
    for (final r in _rows) { sb.writeln(r.toCsv()); }
    await f.writeAsString(sb.toString(), encoding: utf8);
    return f.path;
  }
}
