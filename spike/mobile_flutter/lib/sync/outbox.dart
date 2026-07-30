// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// Outbox local en la MISMA transacción SQLite que el cambio (SY-4) — pieza central Offline-First.
import 'package:sqflite_sqlcipher/sqflite.dart';
import 'package:uuid/uuid.dart';
import 'hlc.dart';

class LocalOp {
  final String operationId; // UUIDv7 — idempotencia de punta a punta (SY-5)
  final String entity;
  final String entityId;
  final String kind;
  final String payloadJson;
  final int hlcPhys;
  final int hlcLogical;

  LocalOp(this.operationId, this.entity, this.entityId, this.kind,
      this.payloadJson, this.hlcPhys, this.hlcLogical);
}

/// Regla de oro del Doc 27: la operación y el cambio local se escriben en UNA transacción.
/// Si la app muere entre ambos, no existe ese "entre".
Future<void> executeLocalWithOutbox(
  Database db,
  Future<void> Function(Transaction txn) localChange,
  LocalOp Function() buildOp,
) async {
  await db.transaction((txn) async {
    await localChange(txn);
    final op = buildOp();
    await txn.insert('outbox', {
      'operation_id': op.operationId,
      'entity': op.entity,
      'entity_id': op.entityId,
      'kind': op.kind,
      'payload': op.payloadJson,
      'hlc_phys': op.hlcPhys,
      'hlc_logical': op.hlcLogical,
      'created_at': DateTime.now().millisecondsSinceEpoch,
      'status': 'pending', // pending | sent | verdict_accept | verdict_adjust | verdict_reject
    });
  });
}

LocalOp newOp(HlcClock hlc, String entity, String entityId, String kind, String payloadJson) {
  final t = hlc.tick(DateTime.now().millisecondsSinceEpoch);
  return LocalOp(const Uuid().v7(), entity, entityId, kind, payloadJson, t.phys, t.logical);
}
