import { onRequest } from 'firebase-functions/v2/https';
import { createRuntime } from './runtime.js';

const { app } = createRuntime();

export const api = onRequest({
  region: 'us-east1', memory: '256MiB', timeoutSeconds: 30,
  minInstances: 0, maxInstances: 1, concurrency: 40,
  invoker: 'private', cors: false,
  serviceAccount: 'veritalex-api@veritalex-bdf40.iam.gserviceaccount.com',
}, app);
