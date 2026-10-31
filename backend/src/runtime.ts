import { getApps, initializeApp } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore } from 'firebase-admin/firestore';
import { createApp } from './app.js';
import { defaultOwnerEmail } from './access.js';

export function createRuntime() {
  const config = JSON.parse(process.env.FIREBASE_CONFIG ?? '{}') as { projectId?: string };
  const projectId = process.env.GCLOUD_PROJECT ?? process.env.GOOGLE_CLOUD_PROJECT ?? config.projectId;
  if (!projectId) throw new Error('Set GCLOUD_PROJECT to the Firebase project ID.');
  const firestoreEmulator = process.env.FIRESTORE_EMULATOR_HOST;
  const authEmulator = process.env.FIREBASE_AUTH_EMULATOR_HOST;
  const usingEmulators = !!(firestoreEmulator || authEmulator);
  if (usingEmulators && (!projectId.startsWith('demo-') || !firestoreEmulator || !authEmulator)) {
    throw new Error('Local API tests require a demo project and both Firebase emulators.');
  }
  if (projectId.startsWith('demo-') && !usingEmulators) {
    throw new Error('Demo projects must use the local Firebase emulators.');
  }
  const admin = getApps()[0] ?? initializeApp({ projectId });
  const db = getFirestore(admin);
  return { app: createApp({
    auth: getAuth(admin), db,
    ownerEmail: process.env.VERITALEX_OWNER_EMAIL ?? defaultOwnerEmail,
    limits: {
      perMinute: Number(process.env.API_REQUESTS_PER_MINUTE ?? 30),
      perDay: Number(process.env.API_REQUESTS_PER_DAY ?? 200),
    },
  }), db, admin };
}
