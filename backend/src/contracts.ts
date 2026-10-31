import { z } from 'zod';
import { ApiError } from './errors.js';

export const bookIdSchema = z.string().regex(/^[1-9][0-9]{0,8}$/);
export const saveBookSchema = z.strictObject({
  title: z.string().min(1).max(500).regex(/\S/, 'Title must contain text'),
  author: z.string().max(300),
});
export const savedBookSchema = saveBookSchema.extend({
  gutenbergId: bookIdSchema,
  savedAt: z.iso.datetime(),
  updatedAt: z.iso.datetime(),
  revision: z.string().regex(/^[A-Za-z0-9_-]{1,128}$/),
});
export const pageQuerySchema = z.strictObject({
  limit: z.string().regex(/^(?:[1-9][0-9]?|100)$/).optional(),
  cursor: z.string().min(1).max(1024).optional(),
});
export const pageSchema = z.strictObject({
  data: z.array(savedBookSchema).max(100),
  nextCursor: z.string().nullable(),
});
export const errorSchema = z.strictObject({
  error: z.strictObject({
    code: z.string(), message: z.string(), requestId: z.string().uuid(),
    details: z.array(z.strictObject({ field: z.string(), message: z.string() })).max(20).optional(),
  }),
});
const cursorSchema = z.strictObject({
  v: z.literal(1), uid: z.string().min(1).max(128), id: bookIdSchema,
  seconds: z.number().int().min(0).max(253402300799),
  nanoseconds: z.number().int().min(0).max(999999999),
});

export type SaveBook = z.infer<typeof saveBookSchema>;
export type SavedBook = z.infer<typeof savedBookSchema>;
export type Cursor = z.infer<typeof cursorSchema>;
export type Conditions = { match?: string; createOnly?: boolean };

export function validate<T>(schema: z.ZodType<T>, value: unknown): T {
  const parsed = schema.safeParse(value);
  if (!parsed.success) {
    throw new ApiError(400, 'INVALID_ARGUMENT', 'The request contains invalid fields.',
      parsed.error.issues.slice(0, 20).map(issue => ({
        field: issue.path.join('.').slice(0, 100), message: issue.message.slice(0, 200),
      })));
  }
  return parsed.data;
}

export function readConditions(match?: string, noneMatch?: string): Conditions {
  if ((match && noneMatch) || (noneMatch && noneMatch !== '*')) {
    throw new ApiError(400, 'INVALID_ARGUMENT', 'Use one strong If-Match value or If-None-Match: *.');
  }
  if (match) {
    const parsed = /^"([A-Za-z0-9_-]{1,128})"$/.exec(match);
    if (!parsed?.[1]) throw new ApiError(400, 'INVALID_ARGUMENT', 'If-Match must contain one quoted strong revision.');
    return { match: parsed[1] };
  }
  return noneMatch ? { createOnly: true } : {};
}

export function encodeCursor(cursor: Cursor): string {
  return Buffer.from(JSON.stringify(cursor)).toString('base64url');
}

export function decodeCursor(value: string, uid: string): Cursor {
  try {
    if (!/^[A-Za-z0-9_-]+$/.test(value)) throw new Error();
    const buffer = Buffer.from(value, 'base64url');
    if (buffer.toString('base64url') !== value) throw new Error();
    const parsed = cursorSchema.parse(JSON.parse(buffer.toString('utf8')));
    if (parsed.uid !== uid) throw new Error();
    return parsed;
  } catch {
    throw new ApiError(400, 'INVALID_ARGUMENT', 'The page cursor is invalid for this account.');
  }
}
