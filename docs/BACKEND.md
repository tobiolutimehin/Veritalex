# Veritalex API and Firebase

## Current state

The saved-book API is implemented locally in TypeScript/Express. It is restricted
to the owner's verified account and binds to 127.0.0.1. Cloud deployment is
paused at the user's request: keep Spark and billing disabled. The Firebase
HTTPS Functions entry point is retained with private invocation as a guard,
not as an active hosted service.

| Resource | Configuration |
| --- | --- |
| Project | [Veritalex](https://console.firebase.google.com/project/veritalex-bdf40/overview), `veritalex-bdf40` |
| Android application | `com.veritalex` |
| Firebase Android ID | `1:884339258397:android:5a6e5e2387dd29ec31c2f4` |
| Authentication | Google sign-in configured; development SHA-1/SHA-256 registered |
| Firestore | `(default)`, Standard, Native mode, `us-east1`, free-tier eligible |
| API | Local-only, owner-restricted; do not deploy |
| Production rules | Last verified: earlier account-owned client rules; cloud lockdown was not completed |
| Repository rules | Deny direct client access; deployment is paused |

The plugin refreshed `app/google-services.json` with Google OAuth clients.
The real file stays out of Git. CI copies the tracked demo-only
`config/google-services.example.json` to that location so build checks need no
real Firebase credentials. A fresh checkout can use the same copy for local
build checks; real Google sign-in requires the plugin-provided project config.
The Android build retains Firebase Authentication and no longer includes the
Firestore SDK. The UI still displays sample data: its sign-in and HTTP repository
integration are separate app work. Release/Play signing fingerprints must be
registered before distributing Google sign-in builds.

## Request flow

```text
Android → Firebase Auth sign-in → Firebase ID token
Android → Authorization: Bearer <token> → /v1/me/... API → Firestore
```

The API verifies the token's signature, project, expiry and revocation/disabled
account state through Firebase Admin. Every route, including health and API
documentation, requires the verified email to match the configured owner:
`olutimehintobi@gmail.com`. Other signed-in accounts receive 403. The allowed
email comes from server configuration and is checked against the verified token,
never a client-supplied email header. The verified UID scopes every database
query. It accepts no account ID in the URL, query or request body. Firebase Admin
uses server credentials and bypasses Firestore client rules, so authorization
and validation are enforced in the API.

Only local demo projects may use emulator credentials. Production uses
Application Default Credentials and a dedicated runtime service account;
no service-account key file is stored or shipped to Android.

## Local request limits

The default budget is 30 authenticated owner requests per minute and 200 per UTC
day, across all routes. Excess requests return 429 with Retry-After. Trusted
server environment variables API_REQUESTS_PER_MINUTE and API_REQUESTS_PER_DAY
can override these defaults; tests raise them only for the bulk integration
suite and separately verify the limiter with a controlled clock.

These are in-memory per-process limits. Restarting the server resets them, so
they are not a durable billing cap. The zero-spending protection for now is
keeping billing disabled, the API local and all test data in demo emulators.

## Saved-book contract

The machine-readable contract is [backend/openapi.json](../backend/openapi.json).
It is generated from the same Zod schemas used for runtime validation and is
also served at `GET /openapi.json`.

| Route | Behavior |
| --- | --- |
| `GET /health` | Process health, no database query |
| `GET /v1/me` | Verified account UID |
| `GET /v1/me/saved-books` | Cursor-paginated account library |
| `GET /v1/me/saved-books/{gutenbergId}` | Record plus ETag |
| `PUT /v1/me/saved-books/{gutenbergId}` | Idempotent save; conditional metadata update |
| `DELETE /v1/me/saved-books/{gutenbergId}` | Conditional removal using If-Match |

A PUT body contains exactly `title` (1–500 characters, nonblank) and `author`
(0–300 characters). The ID is a canonical positive Gutenberg number of at most
nine digits. The server owns `savedAt`, `updatedAt` and an opaque `revision`.
Responses return ISO-8601 timestamps and include a quoted revision as ETag.

Identical unconditional saves return the same record without another write.
Changing metadata requires the current ETag in `If-Match`; `If-None-Match: *`
supports create-only saves. DELETE also requires the current ETag. Stale
conditions return 412, including a repeated conditional delete after success.
The client fetches current state before deciding whether to retry. New saves
after deletion receive a fresh revision, so old queued deletes cannot remove
the re-saved book.

Pages default to 20 records and allow 1–100. Ordering is savedAt descending,
then document ID descending (lexical). Opaque cursors are validated and scoped
to the verified account. They are live-list pagination, not a synchronization
snapshot or change feed. Shelves, notes, reading progress, guest import and
account deletion are outside this saved-book API.

Application errors use `{ error: { code, message, requestId, details? } }`.
Responses include X-Request-ID and private/no-store caching. Bodies are limited
to 16 KiB. Logs include route templates, status and timing, excluding tokens,
bodies and user details. Clients must still handle platform/network failures
whose bodies may not match the application error schema.

## Local verification

Use Node 22 for the Firebase deployment runtime and Java 21+ for Firestore.

```sh
rtk proxy npm --prefix backend ci --no-audit --no-fund
rtk proxy npm --prefix backend run build
rtk proxy npm --prefix backend run contract
rtk proxy npx -y firebase-tools@latest emulators:exec --project demo-veritalex --only auth,firestore 'rtk proxy npm --prefix backend test'
```

To test the actual HTTPS function adapter, include the Functions emulator and
point the same HTTP suite at it:

```sh
rtk proxy env API_REQUESTS_PER_MINUTE=10000 API_REQUESTS_PER_DAY=100000 npx -y firebase-tools@latest emulators:exec --project demo-veritalex --only auth,firestore,functions 'rtk proxy env API_BASE_URL=http://127.0.0.1:5001/demo-veritalex/us-east1/api npm --prefix backend test'
```

Tests refuse to run without the local Auth and Firestore emulators and always
use `demo-veritalex`. They cover real emulator-issued Firebase credentials,
owner-only access, verified-email checks, rate limits, validation, pagination, revisions, concurrent writes,
legacy records, safe errors and blocked direct-client access. The real Google
provider UI is not exercised by these tests.

The standalone entry point is `npm --prefix backend start`, with
`GCLOUD_PROJECT=demo-veritalex`, both emulator host variables and optional PORT.
It serves the same Express application used by the HTTPS function, bound only
to 127.0.0.1. VERITALEX_OWNER_EMAIL can explicitly select another verified owner
account. The default is the connected owner's address above.

The gRPC override pins a patched release because the Firebase client test SDK
otherwise resolves a vulnerable older release. Recheck the override when
updating Firebase dependencies.

## Deployment and cost

Firebase HTTPS Functions requires Blaze and a linked billing account, even when
usage fits the no-cost allowances. Local emulator development requires no
billing account. Build/image storage, network traffic, database operations and
compute have separate pricing: a $0 total is not guaranteed.

The function is configured for us-east1, 256 MiB, a 30-second timeout, zero warm
instances, at most one instance and concurrency 40. This scales to zero when
idle and limits capacity; maxInstances is not a monetary spending limit.

Before deployment, the runtime service account
`veritalex-api@veritalex-bdf40.iam.gserviceaccount.com` must be created and given
`roles/datastore.user` and `roles/firebaseauth.viewer`. The deployment account
also needs permission to act as that service account. It has not been created
or granted roles by this change.

No deployment or billing changes are currently authorized. The database-rule
lockdown was not completed: automatic approval review rejected the deployment,
reporting that the rules still allowed signed-in access. The repository file
denies all direct client access; do not describe that local file as deployed.

If hosting is explicitly reconsidered later, first establish durable quotas and
a reviewed cost limit, provision the runtime identity, and verify the deployed
access controls before connecting Android. The current function has a private
IAM invoker: a Firebase ID token alone cannot satisfy that platform gate.
Private hosting needs a separate reviewed IAM access path; do not silently
change invocation to public.

Firebase spend caps are currently Preview and enforcement can lag; they do not
guarantee an absolute spending ceiling.

Official references: [Functions setup](https://firebase.google.com/docs/functions/get-started),
[Functions pricing](https://firebase.google.com/docs/functions/faq-and-troubleshooting#functions_pricing),
[Cloud Run request-based pricing](https://cloud.google.com/run/pricing),
[Spend caps](https://firebase.google.com/docs/projects/billing/spend-caps).
