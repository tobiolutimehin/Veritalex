import { randomUUID } from 'node:crypto';
import { FieldPath, Timestamp, type DocumentSnapshot, type Firestore } from 'firebase-admin/firestore';
import { encodeCursor, savedBookSchema, type Conditions, type Cursor, type SaveBook, type SavedBook } from './contracts.js';
import { ApiError, preconditionFailed } from './errors.js';

type StoredBook = SaveBook & { savedAt: Timestamp; updatedAt: Timestamp; revision?: string };

function toResponse(id: string, data: StoredBook, legacyRevision?: string): SavedBook {
  if (!(data.savedAt instanceof Timestamp) || !(data.updatedAt instanceof Timestamp)) {
    throw new ApiError(500, 'INTERNAL', 'The saved book could not be read.');
  }
  const parsed = savedBookSchema.safeParse({
    gutenbergId: id, title: data.title, author: data.author,
    savedAt: data.savedAt.toDate().toISOString(), updatedAt: data.updatedAt.toDate().toISOString(),
    revision: data.revision ?? legacyRevision,
  });
  if (!parsed.success) throw new ApiError(500, 'INTERNAL', 'The saved book could not be read.');
  return parsed.data;
}

function readSnapshot(snapshot: DocumentSnapshot): SavedBook {
  const stamp = snapshot.updateTime;
  if (!stamp) throw new ApiError(500, 'INTERNAL', 'The saved book could not be read.');
  return toResponse(snapshot.id, snapshot.data() as StoredBook, `legacy_${stamp.seconds}_${stamp.nanoseconds}`);
}

export class SavedBooks {
  constructor(private readonly db: Firestore) {}

  private collection(uid: string) {
    return this.db.collection('users').doc(uid).collection('savedBooks');
  }

  async get(uid: string, id: string): Promise<SavedBook> {
    const snapshot = await this.collection(uid).doc(id).get();
    if (!snapshot.exists) throw new ApiError(404, 'NOT_FOUND', 'The saved book was not found.');
    return readSnapshot(snapshot);
  }

  async list(uid: string, limit: number, cursor?: Cursor) {
    let query = this.collection(uid).orderBy('savedAt', 'desc').orderBy(FieldPath.documentId(), 'desc');
    if (cursor) query = query.startAfter(new Timestamp(cursor.seconds, cursor.nanoseconds), cursor.id);
    const snapshot = await query.limit(limit + 1).get();
    const page = snapshot.docs.slice(0, limit);
    const last = page.at(-1);
    const at = last?.get('savedAt') as Timestamp | undefined;
    return {
      data: page.map(readSnapshot),
      nextCursor: snapshot.size > limit && last && at instanceof Timestamp
        ? encodeCursor({ v: 1, uid, id: last.id, seconds: at.seconds, nanoseconds: at.nanoseconds })
        : null,
    };
  }

  async put(uid: string, id: string, input: SaveBook, conditions: Conditions) {
    const ref = this.collection(uid).doc(id);
    return this.db.runTransaction(async transaction => {
      const snapshot = await transaction.get(ref);
      const current = snapshot.exists ? readSnapshot(snapshot) : undefined;
      if (conditions.createOnly && current) preconditionFailed();
      if (conditions.match && current?.revision !== conditions.match) preconditionFailed();
      if (current?.title === input.title && current.author === input.author) {
        return { created: false, data: current };
      }
      if (current && !conditions.match) {
        throw new ApiError(428, 'PRECONDITION_REQUIRED', 'Send the current ETag in If-Match to change saved-book metadata.');
      }
      const now = Timestamp.now();
      const record: StoredBook = {
        ...input, savedAt: current ? snapshot.get('savedAt') as Timestamp : now,
        updatedAt: now, revision: randomUUID(),
      };
      transaction.set(ref, record);
      return { created: !current, data: toResponse(id, record) };
    }, { maxAttempts: 3 });
  }

  async remove(uid: string, id: string, revision: string) {
    const ref = this.collection(uid).doc(id);
    await this.db.runTransaction(async transaction => {
      const snapshot = await transaction.get(ref);
      if (!snapshot.exists || readSnapshot(snapshot).revision !== revision) preconditionFailed();
      transaction.delete(ref);
    }, { maxAttempts: 3 });
  }
}
