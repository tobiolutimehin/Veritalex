# Saved Books API Implementation Plan

> **For agentic workers:** Execute this plan task by task in this checkout. Preserve existing uncommitted Android/design work. Use test-driven implementation and verification before completion.

**Goal:** Build a separate authenticated saved-book HTTP API for Veritalex.

**Architecture:** Android signs in with Firebase Auth and sends a Firebase ID token. A TypeScript Express service verifies the token and derives the UID, then uses the Firebase Admin SDK to access that account's Firestore documents. The same app runs locally and as one Firebase HTTPS function. Direct mobile Firestore access is closed in the server-only configuration.

**Tech Stack:** Node.js 22, TypeScript, Express 5, Zod 4, Firebase Admin, Firebase Functions second generation, Firebase Auth/Firestore emulators, Node test runner.

## Contract

| Endpoint | Behavior |
| --- | --- |
| `GET /health` | Process health, no database query or authentication |
| `GET /openapi.json` | Machine-readable OpenAPI 3.1 contract |
| `GET /v1/me` | Verified account UID |
| `GET /v1/me/saved-books` | Account-owned list, limit 1–100 (default 20), opaque cursor |
| `GET /v1/me/saved-books/{gutenbergId}` | One record and a strong ETag; 404 when absent |
| `PUT /v1/me/saved-books/{gutenbergId}` | Save a deterministic ID, or conditionally update metadata |
| `DELETE /v1/me/saved-books/{gutenbergId}` | Conditional removal using If-Match |

PUT accepts exactly `title` (1–500 characters) and `author` (0–300 characters).
IDs are canonical positive Gutenberg numbers of at most nine digits. The server
owns savedAt, updatedAt and revision. Records return ISO-8601 UTC timestamps.
Repeated identical unconditional PUT requests preserve the record and ETag.
Changing existing metadata requires If-Match; stale conditions return 412.
If-None-Match: * supports create-only writes. Conflicting conditional headers
are rejected. DELETE requires a strong If-Match, protecting books removed and
then saved again from old offline deletion requests. Retry status may differ
after a successful conditional mutation; clients reconcile with GET.

Lists sort by savedAt descending and document ID descending, with limit + 1
lookahead. Cursors validate their version, shape and account scope. Pages are a
live list, not a consistent sync snapshot. Full offline synchronization is
outside this first saved-book API.

All errors use `{ error: { code, message, requestId, details? } }`. Responses
include a server-generated X-Request-ID and private/no-store caching policy.
Request bodies are limited to 16 KiB. Tokens and bodies are excluded from logs.
Missing or invalid credentials return 401; authentication infrastructure
failures return 503. Unexpected errors do not expose stack traces to clients.

## Tasks

- [x] **1. Establish a failing HTTP integration suite.** Expand `backend/package.json`, add `backend/tsconfig.json`, a minimal `backend/src/app.ts`, and `backend/test/api.test.mjs`. Use actual Auth emulator credentials and Firestore, with demo-project guards. Observe expected authentication/CRUD failures before implementation.
- [x] **2. Implement the trusted API boundary.** Add `backend/src/errors.ts`, `backend/src/contracts.ts`, `backend/src/saved-books.ts`, and complete `backend/src/app.ts`. Verify authorization, account separation, schema validation, pagination, transactions, idempotent saves and conditional mutations against real emulators.
- [x] **3. Package the service and publish the contract locally.** Add `backend/src/index.ts`, `backend/src/server.ts` and `backend/src/openapi.ts`. Export a second-generation HTTPS function in us-east1 with minInstances 0, maxInstances 1, 256 MiB and a 30-second timeout. Generate `backend/openapi.json` from the runtime schemas and verify its endpoint/error definitions.
- [x] **4. Make the Android/database boundary explicit.** Remove the Android Firestore dependency, retain Firebase Auth, replace local `firestore.rules` with deny-all, update direct-client rules tests and Firebase emulator/deploy configuration. Document the HTTP repository boundary and the deployment sequence in `docs/BACKEND.md` and README.
- [ ] **5. Verify and prepare release.** Run all API/rules tests, build the function and Android app, run Android lint and inspect the diff. Verify deployment billing prerequisites without upgrading the project. Publish only after the user authorizes the required billing change; keep the existing cloud rules until API deployment is successful.

## Deployment constraint

The user targets $0/month. The existing project is Spark with billing disabled.
Firebase Functions requires Blaze even when usage fits free allowances. Build
and test the complete server first; request billing/deployment approval only
when the implementation and checks are ready. No billing account is linked by
this plan, and no exact $0 bill is promised.

Local implementation verified: 46 checks passed through the Firebase HTTPS Functions emulator on Node.js 22; Android debug/release assembly and debug lint passed. Dependency audit reports zero known vulnerabilities. Step 5 remains open only for approved cloud deployment and its live verification; billing remains disabled.

## Current owner-only constraint

The user subsequently required zero spending and owner-only use, then explicitly
paused deployment. This supersedes the earlier public health/docs routes and
release sequence: all routes require a verified owner account; defaults are
30 requests/minute and 200/UTC day with in-memory counters. Standalone serving
binds to 127.0.0.1 and the function invoker is private. The live cloud-rule
lockdown was not completed. Do not deploy or link billing as part of committing
this work. Local limits are not a durable financial cap.

Commit verification: all 48 checks passed through the Node 22 Functions emulator after the owner-only changes. Android assembly and lint passed with both the local project config and a clean temporary checkout using the demo CI config. No deployment was performed.
