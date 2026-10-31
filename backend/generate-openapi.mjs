import { writeFile } from 'node:fs/promises';
import { openapi } from './lib/openapi.js';

await writeFile(new URL('./openapi.json', import.meta.url), `${JSON.stringify(openapi, null, 2)}\n`);
