// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// Adaptador único de sincronización (MA-1): el framework y el motor de sync pueden cambiar
// sin tocar casos de uso ni UI. Esta es la protección arquitectónica contra N-1/N-2 abiertas.
import 'outbox.dart';

class Verdict {
  final String operationId;
  final String verdict; // accept | adjust | reject
  final String? reason;
  final int? serverVersion;
  Verdict(this.operationId, this.verdict, this.reason, this.serverVersion);
}

abstract class SyncAdapter {
  /// Sube las operaciones pendientes en orden causal (HLC) y devuelve veredictos del servidor.
  Future<List<Verdict>> push(List<LocalOp> ops);

  /// Trae réplicas confirmadas del servidor hacia SQLite local.
  Future<void> pull();
}

/// Implementación usada en la Spike: write-path directo del backend mínimo.
class DirectWritePathAdapter implements SyncAdapter {
  final String baseUrl; // p. ej. http://10.0.2.2:5080 (emulador) o IP del dispositivo
  final String token;
  DirectWritePathAdapter(this.baseUrl, this.token);

  @override
  Future<List<Verdict>> push(List<LocalOp> ops) async {
    // POST /sync/operations con lote ordenado por HLC; parsea verdicts[]
    // (implementación HTTP estándar con dio/http; instrumentada con metrics.dart)
    throw UnimplementedError('Ver SPIKE mobile_rn/README: mismo contrato');
  }

  @override
  Future<void> pull() async {
    // GET réplicas confirmadas (en la Spike: GET /work-orders/{id})
    throw UnimplementedError();
  }
}

/// Stub documentado para la fase 2 de N-2 (cuando exista cuenta Cloud o self-hosted).
/// Aquí es donde el SDK de PowerSync se conecta SIN tocar el resto de la app.
class PowerSyncAdapter implements SyncAdapter {
  @override
  Future<List<Verdict>> push(List<LocalOp> ops) =>
      throw UnimplementedError('Fase 2 N-2: SDK PowerSync (uploadQueue → write-path)');
  @override
  Future<void> pull() =>
      throw UnimplementedError('Fase 2 N-2: PowerSync buckets → SQLite (SY-12)');
}
