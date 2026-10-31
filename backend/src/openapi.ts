import { z } from 'zod';
import { errorSchema, pageSchema, savedBookSchema, saveBookSchema } from './contracts.js';

const ref = (name: string) => ({ $ref: `#/components/schemas/${name}` });
const json = (schema: object) => ({ 'application/json': { schema } });
const error = (description: string) => ({ description, content: json(ref('Error')) });
const etag = { description: 'Strong revision for conditional mutations.', schema: { type: 'string' } };
const commonErrors = {
  400: error('Invalid input or cursor.'), 401: error('Missing, invalid, expired or revoked Firebase ID token.'),
  403: error('Only the configured owner account with a verified email may use this API.'),
  429: { ...error('Request limit reached; retry after the indicated delay.'), headers: { 'Retry-After': { schema: { type: 'integer', minimum: 1 }, description: 'Seconds until the local request budget resets.' } } },
  500: error('Unexpected server error.'), 503: error('Authentication or database temporarily unavailable; retry with backoff.'),
};
const record = (description: string) => ({
  description, headers: { ETag: etag },
  content: json({ type: 'object', additionalProperties: false, required: ['data'], properties: { data: ref('SavedBook') } }),
});
const bookId = { name: 'gutenbergId', in: 'path', required: true, schema: { type: 'string', pattern: '^[1-9][0-9]{0,8}$' } };
const match = { name: 'If-Match', in: 'header', schema: { type: 'string', pattern: '^"[A-Za-z0-9_-]{1,128}"$' } };
const parameters = [bookId];

export const openapi = {
  openapi: '3.1.0',
  info: {
    title: 'Veritalex Saved Books API', version: '1.0.0',
    description: 'Account identity is derived exclusively from a verified Firebase ID token. Account-scoped endpoints never accept a user ID. Lists are cursor-paginated live views, not synchronization snapshots. Saved timestamps and revisions are owned by the server.',
  },
  security: [{ firebaseBearer: [] }],
  paths: {
    '/health': { get: { operationId: 'health', responses: { ...commonErrors, 200: { description: 'Process is running.' } } } },
    '/openapi.json': { get: { operationId: 'getOpenApi', responses: { ...commonErrors, 200: { description: 'This OpenAPI document.' } } } },
    '/v1/me': { get: { operationId: 'getAccount', responses: { ...commonErrors, 200: { description: 'Verified account.', content: json({ type: 'object', required: ['data'], properties: { data: { type: 'object', required: ['uid'], properties: { uid: { type: 'string' } } } } }) } } } },
    '/v1/me/saved-books': {
      get: {
        operationId: 'listSavedBooks',
        description: 'Ordered by savedAt descending, then Gutenberg document ID descending (lexical). Pass nextCursor unchanged. A cursor belongs to one account.',
        parameters: [
          { name: 'limit', in: 'query', schema: { type: 'integer', minimum: 1, maximum: 100, default: 20 } },
          { name: 'cursor', in: 'query', schema: { type: 'string', maxLength: 1024 } },
        ],
        responses: { ...commonErrors, 200: { description: 'A bounded page.', content: json(ref('SavedBooksPage')) } },
      },
    },
    '/v1/me/saved-books/{gutenbergId}': {
      get: { operationId: 'getSavedBook', parameters, responses: { ...commonErrors, 200: record('Saved book.'), 404: error('Book is not in this account library.') } },
      put: {
        operationId: 'saveBook',
        description: 'Creates a deterministic resource. Identical unconditional retries return the unchanged record. Changing existing metadata requires If-Match. If-None-Match: * supports create-only saves. Conditional retries can return 412 after success; reconcile with GET. The body limit is 16 KiB.',
        parameters: [...parameters, match, { name: 'If-None-Match', in: 'header', schema: { type: 'string', const: '*' } }],
        requestBody: { required: true, content: json(ref('SaveBook')) },
        responses: {
          ...commonErrors, 200: record('Existing or updated book.'), 201: record('New saved book.'),
          412: error('Revision changed or create-only condition failed.'), 413: error('Body exceeds 16 KiB.'),
          415: error('Body must use application/json.'), 428: error('Current revision is required to change metadata.'),
        },
      },
      delete: {
        operationId: 'removeSavedBook', description: 'Requires the current ETag, protecting a re-saved book from old offline deletes. If the record is already absent the condition fails with 412; reconcile with GET.',
        parameters: [...parameters, { ...match, required: true }],
        responses: { ...commonErrors, 204: { description: 'Removed.' }, 412: error('Revision changed or the book is absent.'), 428: error('If-Match is required.') },
      },
    },
  },
  components: {
    securitySchemes: { firebaseBearer: { type: 'http', scheme: 'bearer', bearerFormat: 'Firebase ID token' } },
    schemas: {
      SaveBook: z.toJSONSchema(saveBookSchema), SavedBook: z.toJSONSchema(savedBookSchema),
      SavedBooksPage: z.toJSONSchema(pageSchema), Error: z.toJSONSchema(errorSchema),
    },
  },
};
