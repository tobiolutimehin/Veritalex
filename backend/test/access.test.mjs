import assert from 'node:assert/strict';
import { once } from 'node:events';
import { test } from 'node:test';
import { createApp } from '../lib/app.js';

test('minute and daily request limits stop bursts and reset at their boundaries', async () => {
  let clock = 0;
  const app = createApp({
    auth: { verifyIdToken: async () => ({ uid: 'owner', email: 'olutimehintobi@gmail.com', email_verified: true }) },
    db: { collection: () => { throw new Error('This request must not access the database'); } },
    limits: { perMinute: 2, perDay: 3 }, now: () => clock, log: () => {},
  });
  const server = app.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const call = () => fetch(`http://127.0.0.1:${server.address().port}/health`, {
    headers: { Authorization: 'Bearer test-token', 'X-Forwarded-For': String(clock) },
    signal: AbortSignal.timeout(5000),
  });
  try {
    assert.equal((await call()).status, 200);
    assert.equal((await call()).status, 200);
    const burst = await call();
    assert.equal(burst.status, 429);
    assert.equal(burst.headers.get('retry-after'), '60');
    assert.equal((await burst.json()).error.code, 'RATE_LIMITED');
    clock = 60_000;
    assert.equal((await call()).status, 200);
    const daily = await call();
    assert.equal(daily.status, 429);
    assert.equal(daily.headers.get('retry-after'), '86340');
    clock = 86_400_000;
    assert.equal((await call()).status, 200);
  } finally {
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
});
