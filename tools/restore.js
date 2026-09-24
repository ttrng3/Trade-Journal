#!/usr/bin/env node
/* Trade Journal restore — feed a backup file back and data/ is as it was.
 *
 * Usage:
 *   node tools/restore.js <backup.json.gz | backup.json> [--data-dir data] [--check]
 *
 *   --check   verify the backup and report what WOULD change, write nothing.
 *
 * Every file is checked against the SHA-256 recorded at backup time, and the
 * fill count against the manifest, before anything is written. A corrupt or
 * truncated backup is refused whole — a half-restored tree is worse than none.
 *
 * Restore replaces data/ with the backup's snapshot. Fills added AFTER the
 * backup are not lost for good: they are still in the Webull CSVs on Drive,
 * and the next sync (existing keys win) puts them back on top.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');

const args = process.argv.slice(2);
const arg = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const SRC = args.find(a => !a.startsWith('--') && args[args.indexOf(a) - 1] !== '--data-dir');
const DATA_DIR = arg('--data-dir', 'data');
const CHECK = args.includes('--check');
if (!SRC) { console.error('usage: restore.js <backup.json.gz> [--data-dir data] [--check]'); process.exit(2); }

const fail = (m) => { console.error('REFUSING: ' + m); process.exit(1); };
const sha256 = (s) => crypto.createHash('sha256').update(s).digest('hex');

let raw = fs.readFileSync(SRC);
if (raw[0] === 0x1f && raw[1] === 0x8b) raw = zlib.gunzipSync(raw);
const b = JSON.parse(raw.toString('utf8'));
if (b.format !== 'trade-journal-backup/1') fail(`unknown format ${JSON.stringify(b.format)}`);

let fills = 0;
for (const [rel, text] of Object.entries(b.files)) {
  if (rel.includes('..') || path.isAbsolute(rel)) fail(`unsafe path ${rel}`);
  if (sha256(text) !== b.sha256[rel]) fail(`${rel} does not match its recorded hash`);
  if (rel.startsWith('fills/')) fills += Object.keys(JSON.parse(text)).length;
}
const idx = JSON.parse(b.files['index.json'] || fail('no index.json in backup'));
if (fills !== idx.totalFills || fills !== b.totalFills) fail(`fill counts disagree: files ${fills}, manifest ${idx.totalFills}, backup ${b.totalFills}`);
for (const id of idx.shards) if (!(`fills/${id}.json` in b.files)) fail(`manifest lists ${id} but the backup has no such month`);

const changed = Object.keys(b.files).filter(rel => {
  try { return fs.readFileSync(path.join(DATA_DIR, rel), 'utf8') !== b.files[rel]; } catch (e) { return true; }
});
// Month files on disk that the backup does not know about would make the tree
// disagree with its manifest; they are removed.
let extra = [];
try {
  extra = fs.readdirSync(path.join(DATA_DIR, 'fills'))
    .map(f => 'fills/' + f).filter(rel => !(rel in b.files));
} catch (e) { /* no fills dir yet */ }

const summary = { backup: SRC, createdUtc: b.createdUtc, totalFills: fills, months: idx.shards.length, changedFiles: changed, removedFiles: extra };
if (CHECK) { console.log(JSON.stringify({ mode: 'check', ...summary }, null, 2)); process.exit(0); }

for (const rel of changed) {
  const p = path.join(DATA_DIR, rel);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, b.files[rel]);
}
for (const rel of extra) fs.unlinkSync(path.join(DATA_DIR, rel));
console.log(JSON.stringify({ mode: 'write', ...summary }, null, 2));
