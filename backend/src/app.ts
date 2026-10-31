import { randomUUID } from 'node:crypto';
import express, { type ErrorRequestHandler } from 'express';
import type { Auth, DecodedIdToken } from 'firebase-admin/auth';
import type { Firestore } from 'firebase-admin/firestore';
import { bookIdSchema, decodeCursor, pageQuerySchema, readConditions, saveBookSchema, validate } from './contracts.js';
import { ApiError } from './errors.js';
import { openapi } from './openapi.js';
import { SavedBooks } from './saved-books.js';
import { createRequestBudget, defaultOwnerEmail, type RequestLimits } from './access.js';

export function createApp({ auth, db, ownerEmail = defaultOwnerEmail, limits, now,
  log = entry => console.info(JSON.stringify(entry)) }: {
  auth: Pick<Auth, 'verifyIdToken'>; db: Firestore; log?: (entry: Record<string, unknown>) => void;
  ownerEmail?: string; limits?: RequestLimits; now?: () => number;
}) {
  const allowedEmail = ownerEmail.trim().toLowerCase();
  if (!allowedEmail) throw new Error('An owner account must be configured.');
  const consumeRequest = createRequestBudget(limits, now);
  const app = express();
  const savedBooks = new SavedBooks(db);
  app.disable('x-powered-by');
  app.disable('etag');
  app.set('query parser', 'simple');
  app.use((req, res, next) => {
    const start = Date.now();
    res.locals.requestId = randomUUID();
    res.set({ 'X-Request-ID': res.locals.requestId, 'Cache-Control': 'private, no-store', 'X-Content-Type-Options': 'nosniff' });
    res.on('finish', () => log({ requestId: res.locals.requestId, method: req.method, route: req.route?.path ?? 'unmatched', status: res.statusCode, durationMs: Date.now() - start }));
    next();
  });
  app.use(async (req, res, next) => {
    const bearer = /^Bearer ([A-Za-z0-9._-]+)$/i.exec(req.get('authorization') ?? '');
    if (!bearer?.[1]) throw new ApiError(401, 'UNAUTHENTICATED', 'Sign in to access your account.');
    let identity: DecodedIdToken;
    try {
      // Admin database access bypasses Firestore rules: this verified UID owns every query below.
      identity = await auth.verifyIdToken(bearer[1], true);
    } catch (error) {
      const code = (error as { code?: string }).code;
      if (['auth/argument-error', 'auth/invalid-id-token', 'auth/id-token-expired', 'auth/id-token-revoked', 'auth/user-disabled', 'auth/user-not-found'].includes(code ?? '')) {
        throw new ApiError(401, 'UNAUTHENTICATED', 'Your session is invalid or expired. Sign in again.');
      }
      throw new ApiError(503, 'UNAVAILABLE', 'Authentication is temporarily unavailable.');
    }
    if (identity.email_verified !== true || identity.email?.toLowerCase() !== allowedEmail) {
      throw new ApiError(403, 'FORBIDDEN', 'This account is not allowed to use this API.');
    }
    consumeRequest();
    res.locals.uid = identity.uid;
    next();
  });
  app.get('/health', (_req, res) => { res.json({ status: 'ok' }); });
  app.get('/openapi.json', (_req, res) => { res.json(openapi); });
  app.get('/v1/me', (_req, res) => { res.json({ data: { uid: res.locals.uid } }); });
  const path = '/v1/me/saved-books';
  app.get(path, async (req, res) => {
    const query = validate(pageQuerySchema, req.query);
    res.json(await savedBooks.list(res.locals.uid, Number(query.limit ?? 20), query.cursor ? decodeCursor(query.cursor, res.locals.uid) : undefined));
  });
  app.get(`${path}/:bookId`, async (req, res) => {
    const data = await savedBooks.get(res.locals.uid, validate(bookIdSchema, req.params.bookId));
    res.set('ETag', `"${data.revision}"`).json({ data });
  });
  app.put(`${path}/:bookId`, (req, _res, next) => {
    if (!req.is('application/json')) throw new ApiError(415, 'UNSUPPORTED_MEDIA_TYPE', 'Send an application/json body.');
    const raw = (req as typeof req & { rawBody?: Buffer }).rawBody;
    if (raw && raw.length > 16384) throw new ApiError(413, 'PAYLOAD_TOO_LARGE', 'The request body exceeds 16 KiB.');
    next();
  }, express.json({ limit: 16384, inflate: false }), async (req, res) => {
    const result = await savedBooks.put(
      res.locals.uid, validate(bookIdSchema, req.params.bookId), validate(saveBookSchema, req.body),
      readConditions(req.get('if-match'), req.get('if-none-match')),
    );
    res.status(result.created ? 201 : 200).set('ETag', `"${result.data.revision}"`).json({ data: result.data });
  });
  app.delete(`${path}/:bookId`, async (req, res) => {
    const conditions = readConditions(req.get('if-match'), req.get('if-none-match'));
    if (!conditions.match) throw new ApiError(428, 'PRECONDITION_REQUIRED', 'Send the current ETag in If-Match to remove a saved book.');
    await savedBooks.remove(res.locals.uid, validate(bookIdSchema, req.params.bookId), conditions.match);
    res.status(204).end();
  });
  for (const [route, methods] of [[path, 'GET, HEAD'], [`${path}/:bookId`, 'GET, HEAD, PUT, DELETE']]) {
    app.all(route!, (_req, res, next) => {
      res.set('Allow', methods!);
      next(new ApiError(405, 'METHOD_NOT_ALLOWED', 'This endpoint does not support that method.'));
    });
  }
  app.use((_req, _res, next) => next(new ApiError(404, 'NOT_FOUND', 'The endpoint was not found.')));
  const errors: ErrorRequestHandler = (error: unknown, _req, res, _next) => {
    if (res.headersSent) { res.end(); return; }
    const failure = error as { type?: string; code?: number };
    let response = error instanceof ApiError ? error : new ApiError(500, 'INTERNAL', 'The request could not be completed.');
    if (failure.type === 'entity.parse.failed') response = new ApiError(400, 'INVALID_ARGUMENT', 'The request body is not valid JSON.');
    if (error instanceof URIError) response = new ApiError(400, 'INVALID_ARGUMENT', 'The request path is not valid.');
    if (failure.type === 'entity.too.large') response = new ApiError(413, 'PAYLOAD_TOO_LARGE', 'The request body exceeds 16 KiB.');
    if (failure.type === 'encoding.unsupported') response = new ApiError(415, 'UNSUPPORTED_MEDIA_TYPE', 'Compressed request bodies are not supported.');
    if (failure.type === 'charset.unsupported') response = new ApiError(415, 'UNSUPPORTED_MEDIA_TYPE', 'Send a UTF-8 JSON body.');
    if ([4, 8, 10, 14].includes(failure.code ?? -1)) response = new ApiError(503, 'UNAVAILABLE', 'The database is temporarily unavailable.');
    if (response.status === 401) res.set('WWW-Authenticate', 'Bearer');
    if (response.status === 503) res.set('Retry-After', '5');
    if (response.retryAfter) res.set('Retry-After', String(response.retryAfter));
    res.status(response.status).json({ error: {
      code: response.code, message: response.message, requestId: res.locals.requestId,
      ...(response.details ? { details: response.details } : {}),
    } });
  };
  app.use(errors);
  return app;
}
