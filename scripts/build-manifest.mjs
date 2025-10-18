import { readdir } from 'node:fs/promises';
import { writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const ROOT = new URL('../static/rocks', import.meta.url).pathname;
const OUT  = new URL('../static/rocks-manifest.json', import.meta.url).pathname;

function naturalSort(a, b) {
  return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
}

const IMAGE_EXT = new Set(['.jpg','.jpeg','.png','.webp','.gif']);

function ext(name) {
  const i = name.lastIndexOf('.');
  return i>=0 ? name.slice(i).toLowerCase() : '';
}

async function listDir(dir) {
  return (await readdir(dir, { withFileTypes: true })).filter(d => d.isDirectory()).map(d => d.name);
}
async function listFiles(dir) {
  const items = await readdir(dir, { withFileTypes: true });
  return items
    .filter(d => d.isFile() && IMAGE_EXT.has(ext(d.name)))
    .map(d => d.name)
    .sort(naturalSort);
}

async function main() {
  const classes = await listDir(ROOT);
  const data = {};
  for (const cls of classes.sort(naturalSort)) {
    const abs = join(ROOT, cls);
    const files = await listFiles(abs);
    // Public URLs from /static
    data[cls] = files.map(f => `/rocks/${encodeURIComponent(cls)}/${encodeURIComponent(f)}`);
  }
  await writeFile(OUT, JSON.stringify(data), 'utf-8');
  console.log(`Wrote manifest with ${classes.length} classes → ${OUT}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
