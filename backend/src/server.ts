import { deleteApp } from 'firebase-admin/app';
import { createRuntime } from './runtime.js';

const port = Number(process.env.PORT ?? 8080);
if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('PORT must be an integer from 0 through 65535.');
const { app, db, admin } = createRuntime();
const server = app.listen(port, '127.0.0.1', () => {
  const address = server.address();
  console.info(JSON.stringify({ event: 'listening', port: typeof address === 'object' ? address?.port : port }));
});
server.headersTimeout = 10_000;
server.requestTimeout = 30_000;

let stopping = false;
function shutdown() {
  if (stopping) return;
  stopping = true;
  const deadline = setTimeout(() => { server.closeAllConnections(); process.exit(1); }, 8000).unref();
  server.close(async () => {
    try {
      await db.terminate();
      await deleteApp(admin);
      clearTimeout(deadline);
      process.exit(0);
    } catch {
      process.exit(1);
    }
  });
}
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
