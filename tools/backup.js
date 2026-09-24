#!/usr/bin/env node
/* Trade Journal backup — one file that holds everything under data/.
 *
 * The repo's git history already keeps every version of every fill, but it is
 * one copy in one place: if the repo goes (Signal Desk's did, 2026-09-24), the
 * history goes with it. This packs data/ into a single gzipped JSON file that
 * can live anywhere and be fed back with tools/restore.js.
 *
 * Usage:
 *   node tools/backup.js [--data-dir data] [--out <file>]
 *
 * The bundle stores each file's EXACT text, not a re-parsed copy. Restoring
 * therefore reproduces data/ byte-for-byte, and `sync.js --check` afterwards
 * reports zero changed files — the serialization rules in sync.js never come
 * into play.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');

const args = process.argv.slice(2);
const arg = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const DATA_DIR = arg('--data-dir', 'data');
const today = new Date().toISOString().slice(0, 10);
const OUT = arg('--out', `trade-journal-backup-${today}.json.gz`);

const sha256 = (s) => crypto.createHash('sha256').update(s).digest('hex');

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? walk(p) : [p];
  });
}

const idx = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'index.json'), 'utf8'));
const files = {}, hashes = {};
let fills = 0;
for (const p of walk(DATA_DIR).sort()) {
  const rel = path.relative(DATA_DIR, p).split(path.sep).join('/');
  const text = fs.readFileSync(p, 'utf8');
  files[rel] = text;
  hashes[rel] = sha256(text);
  if (rel.startsWith('fills/')) fills += Object.keys(JSON.parse(text)).length;
}

// Never write a backup of a tree that is already broken.
if (fills !== idx.totalFills) {
  console.error(`REFUSING: manifest says ${idx.totalFills} fills, month files hold ${fills}.`);
  process.exit(1);
}

const bundle = {
  format: 'trade-journal-backup/1',
  createdUtc: new Date().toISOString(),
  repo: 'ttrng3/Trade-Journal',
  commit: process.env.GITHUB_SHA || null,
  totalFills: fills,
  months: idx.shards.length,
  dataGeneratedUtc: idx.generatedUtc,
  sha256: hashes,
  files,
};
const gz = zlib.gzipSync(JSON.stringify(bundle), { level: 9 });
fs.writeFileSync(OUT, gz);
console.log(JSON.stringify({ out: OUT, bytes: gz.length, totalFills: fills, months: bundle.months, files: Object.keys(files).length }, null, 2));
