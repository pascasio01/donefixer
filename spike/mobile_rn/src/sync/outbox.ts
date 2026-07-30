// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// Outbox local en la MISMA transacción SQLite que el cambio (SY-4).
import * as Crypto from 'expo-crypto';
import type { HlcClock } from './hlc';

export interface LocalOp {
  operationId: string; // UUIDv7 — idempotencia punta a punta (SY-5)
  entity: string;
  entityId: string;
  kind: string;
  payloadJson: string;
  hlcPhys: number;
  hlcLogical: number;
}

function uuidv7(): string {
  // timestamp-ordered UUID (compatible con el ordenamiento causal del lote)
  const now = Date.now().toString(16).padStart(12, '0');
  const rand = () => Math.floor(Math.random() * 0xffff).toString(16).padStart(4, '0');
  return `${now.slice(0, 8)}-${now.slice(8)}-7${rand().slice(1)}-${rand()}-${rand()}${rand()}${rand()}`;
}

export function newOp(hlc: HlcClock, entity: string, entityId: string, kind: string, payloadJson: string): LocalOp {
  const t = hlc.tick(Date.now());
  return { operationId: uuidv7(), entity, entityId, kind, payloadJson, hlcPhys: t.phys, hlcLogical: t.logical };
}

// Regla de oro (Doc 27): cambio local + operación en UNA transacción SQLite.
export async function executeLocalWithOutbox(
  db: any, // SQLiteDatabase de expo-sqlite
  localChange: () => Promise<void>,
  buildOp: () => LocalOp,
): Promise<void> {
  await db.withTransactionAsync(async () => {
    await localChange();
    const op = buildOp();
    await db.runAsync(
      `INSERT INTO outbox (operation_id, entity, entity_id, kind, payload, hlc_phys, hlc_logical, created_at, status)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')`,
      [op.operationId, op.entity, op.entityId, op.kind, op.payloadJson, op.hlcPhys, op.hlcLogical, Date.now()],
    );
  });
}

export async function sha256Of(data: string): Promise<string> {
  return Crypto.digestStringAsync(Crypto.CryptoDigestAlgorithm.SHA256, data);
}
