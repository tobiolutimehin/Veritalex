import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { after, before, beforeEach, test } from 'node:test';
import { assertFails, initializeTestEnvironment } from '@firebase/rules-unit-testing';
import { collection, deleteDoc, doc, getDoc, getDocs, setDoc, setLogLevel, updateDoc } from 'firebase/firestore';

assert.ok(process.env.FIRESTORE_EMULATOR_HOST, 'Run through Firebase emulators:exec');
setLogLevel('silent');
let environment;
before(async () => {
  environment = await initializeTestEnvironment({
    projectId: 'demo-veritalex',
    firestore: { rules: await readFile(new URL('../firestore.rules', import.meta.url), 'utf8') },
  });
});
beforeEach(async () => {
  await environment.clearFirestore();
  await environment.withSecurityRulesDisabled(async context => {
    await setDoc(doc(context.firestore(), 'users/alice/savedBooks/1342'), { title: 'Private data' });
  });
});
after(async () => environment?.cleanup());

for (const uid of [null, 'alice', 'bob']) {
  test(`direct Firestore access is closed for ${uid ?? 'signed-out clients'}`, async () => {
    const db = uid ? environment.authenticatedContext(uid).firestore() : environment.unauthenticatedContext().firestore();
    const ref = doc(db, 'users/alice/savedBooks/1342');
    await assertFails(getDoc(ref));
    await assertFails(getDocs(collection(db, 'users/alice/savedBooks')));
    await assertFails(setDoc(doc(db, 'users/alice/savedBooks/84'), { title: 'Bypass' }));
    await assertFails(updateDoc(ref, { title: 'Bypass' }));
    await assertFails(deleteDoc(ref));
    await assertFails(setDoc(doc(db, 'other/document'), { data: true }));
  });
}
