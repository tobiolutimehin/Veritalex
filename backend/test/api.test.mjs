import assert from 'node:assert/strict';
import { once } from 'node:events';
import { after, before, beforeEach, test } from 'node:test';
import { initializeApp as initializeAdmin, deleteApp as deleteAdmin } from 'firebase-admin/app';
import { getAuth as getAdminAuth } from 'firebase-admin/auth';
import { getFirestore, Timestamp } from 'firebase-admin/firestore';
import { initializeApp, deleteApp } from 'firebase/app';
import { connectAuthEmulator, getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import { createApp } from '../lib/app.js';

assert.ok(process.env.FIRESTORE_EMULATOR_HOST, 'Firestore emulator required');
assert.ok(process.env.FIREBASE_AUTH_EMULATOR_HOST, 'Auth emulator required');
const projectId = 'demo-veritalex';
const ownerEmail = 'olutimehintobi@gmail.com';
const admin = initializeAdmin({ projectId }, 'api-tests');
const auth = getAdminAuth(admin);
const db = getFirestore(admin);
const clients = [];
const tokens = {};
const payload = { title: 'Pride and Prejudice', author: 'Jane Austen' };
const books = '/v1/me/saved-books';
let server;
let baseUrl;

async function signIn(uid) {
  const email = uid === 'alice' ? ownerEmail : `${uid}@example.test`;
  await auth.createUser({ uid, email, emailVerified: true, password: 'Emulator-only-123!' });
  const client = initializeApp({ projectId, apiKey: 'emulator-only-key' }, uid);
  clients.push(client);
  const clientAuth = getAuth(client);
  connectAuthEmulator(clientAuth, `http://${process.env.FIREBASE_AUTH_EMULATOR_HOST}`, { disableWarnings: true });
  const credential = await signInWithEmailAndPassword(clientAuth, email, 'Emulator-only-123!');
  return credential.user.getIdToken();
}

async function request(path, options = {}) {
  const { method = 'GET', token = tokens.alice, body, headers = {}, rawBody } = options;
  const response = await fetch(`${baseUrl}${path}`, {
    method,
    signal: AbortSignal.timeout(15000),
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(body !== undefined || rawBody !== undefined ? { 'Content-Type': 'application/json' } : {}),
      ...headers,
    },
    ...(rawBody !== undefined ? { body: rawBody } : body !== undefined ? { body: JSON.stringify(body) } : {}),
  });
  const text = await response.text();
  return {
    status: response.status,
    headers: response.headers,
    json: response.headers.get('content-type')?.includes('application/json') && text ? JSON.parse(text) : null,
    text,
  };
}
const save = (id = '1342', options = {}) => request(`${books}/${id}`, { method: 'PUT', body: payload, ...options });

before(async () => {
  tokens.alice = await signIn('alice');
  tokens.bob = await signIn('bob');
  if (process.env.API_BASE_URL) {
    baseUrl = process.env.API_BASE_URL;
  } else {
    server = createApp({ auth, db, limits: { perMinute: 10000, perDay: 100000 }, log: () => {} }).listen(0, '127.0.0.1');
    await once(server, 'listening');
    baseUrl = `http://127.0.0.1:${server.address().port}`;
  }
});
beforeEach(async () => {
  const result = await fetch(`http://${process.env.FIRESTORE_EMULATOR_HOST}/emulator/v1/projects/${projectId}/databases/(default)/documents`, { method: 'DELETE' });
  assert.equal(result.status, 200);
});
after(async () => {
  if (server) {
    server.closeAllConnections();
    await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  }
  await Promise.all(clients.map(deleteApp));
  await db.terminate();
  await deleteAdmin(admin);
});

test('health and API documentation require the owner account', async () => {
  assert.equal((await request('/health', { token: null })).status, 401);
  assert.equal((await request('/openapi.json', { token: null })).status, 401);
  assert.equal((await request('/health', { token: tokens.bob })).status, 403);
  const contract = await request('/openapi.json');
  assert.equal(contract.status, 200);
  assert.equal(contract.json.openapi, '3.1.0');
  assert.ok(contract.json.paths['/v1/me/saved-books/{gutenbergId}'].put);
  assert.equal(contract.json.components.schemas.SaveBook.additionalProperties, false);
  assert.ok(contract.json.paths['/v1/me/saved-books/{gutenbergId}'].put.responses['412']);
});

for (const token of [null, 'alice', 'not-a-jwt']) {
  test(`rejects ${token ?? 'missing'} authentication with a structured 401`, async () => {
    const result = await request('/v1/me', { token });
    assert.equal(result.status, 401);
    assert.equal(result.json.error.code, 'UNAUTHENTICATED');
    assert.equal(result.json.error.requestId, result.headers.get('x-request-id'));
    assert.match(result.headers.get('www-authenticate'), /^Bearer/);
  });
}

test('derives the account from a verified token and ignores claimed user headers', async () => {
  const result = await request('/v1/me', { headers: { 'X-User-ID': 'bob' } });
  assert.equal(result.status, 200);
  assert.equal(result.json.data.uid, 'alice');
  assert.equal(result.headers.get('cache-control'), 'private, no-store');
});

test('does not accept tokens issued for a different Firebase project', async () => {
  const [header, encoded, signature] = tokens.alice.split('.');
  const claims = JSON.parse(Buffer.from(encoded, 'base64url').toString());
  claims.aud = 'demo-other-project';
  const token = `${header}.${Buffer.from(JSON.stringify(claims)).toString('base64url')}.${signature}`;
  assert.equal((await request('/v1/me', { token })).status, 401);
});

test('rejects expired and disabled-user sessions', async () => {
  const [header, encoded, signature] = tokens.alice.split('.');
  const claims = JSON.parse(Buffer.from(encoded, 'base64url').toString());
  claims.exp = 1;
  assert.equal((await request('/v1/me', { token: `${header}.${Buffer.from(JSON.stringify(claims)).toString('base64url')}.${signature}` })).status, 401);
  const token = await signIn('disabled-user');
  await auth.updateUser('disabled-user', { disabled: true });
  assert.equal((await request('/v1/me', { token })).status, 401);
});

test('saving a book is deterministic and identical retries preserve its revision', async () => {
  const first = await save();
  assert.equal(first.status, 201);
  assert.equal(first.json.data.gutenbergId, '1342');
  assert.equal(first.json.data.title, payload.title);
  assert.ok(first.json.data.savedAt.endsWith('Z'));
  assert.equal(first.headers.get('etag'), `"${first.json.data.revision}"`);
  const retry = await save();
  assert.equal(retry.status, 200);
  assert.deepEqual(retry.json, first.json);
  assert.equal(retry.headers.get('etag'), first.headers.get('etag'));
  const list = await request(books);
  assert.equal(list.json.data.length, 1);
});

test('other signed-in accounts cannot use any reading endpoints', async () => {
  await save();
  assert.equal((await request(`${books}/1342`, { token: tokens.bob })).status, 403);
  assert.equal((await request(books, { token: tokens.bob })).status, 403);
  const own = await save('1342', { token: tokens.bob, body: { ...payload, title: 'Bob metadata' } });
  assert.equal(own.status, 403);
  assert.equal((await request(`${books}/1342`, { method: 'DELETE', token: tokens.bob, headers: { 'If-Match': '"a"' } })).status, 403);
  assert.equal((await request('/v1/me', { token: tokens.bob })).status, 403);
  assert.equal((await request(`${books}/1342`)).json.data.title, payload.title);
  assert.equal((await request('/v1/users/alice/saved-books', { token: tokens.bob })).status, 403);
});

test('metadata changes require a current ETag and preserve the original saved timestamp', async () => {
  const first = await save();
  const body = { ...payload, author: '' };
  assert.equal((await save('1342', { body })).status, 428);
  const changed = await save('1342', { body, headers: { 'If-Match': first.headers.get('etag') } });
  assert.equal(changed.status, 200);
  assert.equal(changed.json.data.savedAt, first.json.data.savedAt);
  assert.notEqual(changed.headers.get('etag'), first.headers.get('etag'));
  assert.equal((await save('1342', { headers: { 'If-Match': first.headers.get('etag') } })).status, 412);
});

test('create-only and missing-resource preconditions are enforced', async () => {
  assert.equal((await save('1342', { headers: { 'If-None-Match': '*' } })).status, 201);
  assert.equal((await save('1342', { headers: { 'If-None-Match': '*' } })).status, 412);
  assert.equal((await save('84', { headers: { 'If-Match': '"missing-revision"' } })).status, 412);
  assert.equal((await save('84', { headers: { 'If-Match': '"a"', 'If-None-Match': '*' } })).status, 400);
});

test('conditional writes serialize concurrent changes instead of losing updates', async () => {
  const first = await save();
  const headers = { 'If-Match': first.headers.get('etag') };
  const results = await Promise.all([
    save('1342', { body: { ...payload, title: 'Change A' }, headers }),
    save('1342', { body: { ...payload, title: 'Change B' }, headers }),
  ]);
  assert.deepEqual(results.map(x => x.status).sort(), [200, 412]);
});

test('old offline deletes cannot remove a book saved again after deletion', async () => {
  const first = await save();
  assert.equal((await request(`${books}/1342`, { method: 'DELETE' })).status, 428);
  assert.equal((await request(`${books}/1342`, { method: 'DELETE', headers: { 'If-Match': first.headers.get('etag') } })).status, 204);
  assert.equal((await request(`${books}/1342`)).status, 404);
  const again = await save();
  assert.equal(again.status, 201);
  assert.equal((await request(`${books}/1342`, { method: 'DELETE', headers: { 'If-Match': first.headers.get('etag') } })).status, 412);
  assert.equal((await request(`${books}/1342`)).status, 200);
});

test('pagination is bounded, stable for tied timestamps and account-scoped', async () => {
  const sameTime = Timestamp.fromMillis(1700000000000);
  for (const id of ['1', '2', '3']) {
    await db.doc(`users/alice/savedBooks/${id}`).set({ ...payload, savedAt: sameTime, updatedAt: sameTime, revision: `revision-${id}` });
  }
  const first = await request(`${books}?limit=2`);
  assert.equal(first.status, 200);
  assert.deepEqual(first.json.data.map(x => x.gutenbergId), ['3', '2']);
  const cursor = first.json.nextCursor;
  assert.ok(cursor);
  const next = await request(`${books}?limit=2&cursor=${encodeURIComponent(cursor)}`);
  assert.deepEqual(next.json.data.map(x => x.gutenbergId), ['1']);
  assert.equal(next.json.nextCursor, null);
  assert.equal((await request(`${books}?cursor=${encodeURIComponent(cursor)}`, { token: tokens.bob })).status, 403);
});

test('a matching email without verified ownership is denied', async () => {
  const [header, encoded, signature] = tokens.alice.split('.');
  const claims = JSON.parse(Buffer.from(encoded, 'base64url').toString());
  claims.email_verified = false;
  const token = `${header}.${Buffer.from(JSON.stringify(claims)).toString('base64url')}.${signature}`;
  assert.equal((await request('/v1/me', { token })).status, 403);
});

for (const query of ['limit=0', 'limit=101', 'limit=oops', 'limit=1&limit=2', 'cursor=garbage', 'extra=value']) {
  test(`rejects invalid pagination ${query}`, async () => {
    assert.equal((await request(`${books}?${query}`)).status, 400);
  });
}

for (const id of ['0', '-1', '01342', 'a-title', '1234567890']) {
  test(`rejects invalid book ID ${id}`, async () => assert.equal((await save(id)).status, 400));
}

for (const body of [
  {}, { ...payload, ownerId: 'bob' }, { ...payload, uid: 'bob' },
  { ...payload, savedAt: '2026-01-01T00:00:00Z' }, { ...payload, revision: 'forged' },
  { ...payload, title: '' }, { ...payload, title: ' '.repeat(5) },
  { ...payload, title: 'x'.repeat(501) }, { ...payload, author: 'x'.repeat(301) },
  { ...payload, title: 42 }, { ...payload, author: [] },
]) {
  test(`rejects invalid saved-book payload ${JSON.stringify(body).slice(0,70)}`, async () => {
    assert.equal((await save('1342', { body })).status, 400);
    assert.equal((await request(`${books}/1342`)).status, 404);
  });
}

test('malformed, oversized and non-JSON bodies have predictable errors', async () => {
  assert.equal((await request(`${books}/1342`, { method: 'PUT', rawBody: '{broken' })).status, 400);
  assert.equal((await save('1342', { body: { ...payload, padding: 'x'.repeat(20000) } })).status, 413);
  assert.equal((await request(`${books}/1342`, { method: 'PUT', rawBody: '{}', headers: { 'Content-Type': 'text/plain' } })).status, 415);
});

test('unsupported methods and unknown routes return JSON errors', async () => {
  const method = await request(`${books}/1342`, { method: 'POST', body: payload });
  assert.equal(method.status, 405);
  assert.ok(method.headers.get('allow').includes('PUT'));
  const absent = await request('/unknown');
  assert.equal(absent.status, 404);
  assert.equal(absent.json.error.code, 'NOT_FOUND');
});

test('legacy saved books remain readable and can be upgraded conditionally', async () => {
  const now = Timestamp.now();
  await db.doc('users/alice/savedBooks/1342').set({ ...payload, savedAt: now, updatedAt: now });
  const current = await request(`${books}/1342`);
  assert.equal(current.status, 200);
  const updated = await save('1342', { body: { ...payload, title: 'Updated legacy book' }, headers: { 'If-Match': current.headers.get('etag') } });
  assert.equal(updated.status, 200);
});

test('malformed conditional headers and retries cannot bypass revisions', async () => {
  await save();
  for (const value of ['*', 'unquoted', 'W/"weak"', '"a", "b"']) {
    assert.equal((await save('1342', { headers: { 'If-Match': value } })).status, 400);
  }
  const current = await request(`${books}/1342`);
  const headers = { 'If-Match': current.headers.get('etag') };
  assert.equal((await request(`${books}/1342`, { method: 'DELETE', headers })).status, 204);
  assert.equal((await request(`${books}/1342`, { method: 'DELETE', headers })).status, 412);
});

test('write routes require a verified account as well', async () => {
  assert.equal((await save('1342', { token: null })).status, 401);
  assert.equal((await request(`${books}/1342`, { method: 'DELETE', token: null, headers: { 'If-Match': '"a"' } })).status, 401);
});

test('server failures never expose malformed stored data', async () => {
  const now = Timestamp.now();
  await db.doc('users/alice/savedBooks/1342').set({ title: 42, author: 'private-marker', savedAt: now, updatedAt: now });
  const result = await request(`${books}/1342`);
  assert.equal(result.status, 500);
  assert.equal(result.json.error.code, 'INTERNAL');
  assert.ok(!result.text.includes('private-marker'));
  assert.ok(!result.text.includes('stack'));
});

test('unsupported JSON charsets and malformed path encoding are client errors', async () => {
  const charset = await request(`${books}/1342`, {
    method: 'PUT', rawBody: '{}', headers: { 'Content-Type': 'application/json; charset=iso-8859-1' },
  });
  assert.equal(charset.status, 415);
  assert.equal((await request(`${books}/%E0%A4%A`)).status, 400);
});
