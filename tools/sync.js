#!/usr/bin/env node
/* Trade Journal sync — the whole pipeline, in the repo.
 *
 * Until 2026-09-23 this logic lived in two places outside the repo: the parser
 * was scraped line-by-line out of an HTML file on Google Drive, and the merge
 * ran against a claude.ai artifact database that was the source of truth. Both
 * are gone. The repo is now the source: `data/fills/<YYYY-MM>.json` holds the
 * fills, `data/index.json` is the manifest, and GitHub Pages reads them.
 *
 * Usage:
 *   node tools/sync.js --csv-dir <dir> [--data-dir data] [--check]
 *
 *   --check   parse and merge, report what WOULD change, write nothing.
 *             With no new fills it must report zero changed files — that is
 *             the regression test for the serialization below.
 *
 * Merge rule: fills are keyed, and EXISTING KEYS WIN. Re-importing a CSV is
 * therefore always safe. That matters more than it sounds: Webull re-exports
 * to the same generic filename `Webull_Orders_Records_Options.csv`, so a
 * filename-only dedup silently skips real trades. On 2026-09-23 that nearly
 * dropped 100 fills. Dedup on content, never on filename.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { parseWebull, compact } = require('./parse-webull.js');

const args = process.argv.slice(2);
const arg = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const CSV_DIR = arg('--csv-dir');
const DATA_DIR = arg('--data-dir', 'data');
const CHECK = args.includes('--check');
if (!CSV_DIR) { console.error('usage: sync.js --csv-dir <dir> [--data-dir data] [--check]'); process.exit(2); }

const monthOf = (t) => t.slice(0, 7);

/* Serialization is load-bearing: it decides the git diff. Month files are
 * minified with keys sorted ascending and each fill's fields in alphabetical
 * order; the manifest is pretty-printed with a ONE-space indent. Change either
 * and every month rewrites, burying the real change in noise. */
const FIELD_ORDER = ['k', 'p', 'price', 'qty', 'side', 'sym', 't', 'tif'];
function serializeMonth(fills) {
  const out = {};
  for (const k of Object.keys(fills).sort()) {
    const f = fills[k], o = {};
    for (const key of FIELD_ORDER) o[key] = f[key];
    out[k] = o;
  }
  return JSON.stringify(out);
}
const serializeIndex = (idx) => JSON.stringify(idx, null, 1);

function loadExisting() {
  const idxPath = path.join(DATA_DIR, 'index.json');
  const idx = JSON.parse(fs.readFileSync(idxPath, 'utf8'));
  const months = {};
  for (const id of idx.shards) {
    months[id] = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'fills', id + '.json'), 'utf8'));
  }
  return { idx, months };
}

function main() {
  const { idx, months } = loadExisting();
  const before = Object.values(months).reduce((n, m) => n + Object.keys(m).length, 0);
  if (before !== idx.totalFills) {
    console.error(`REFUSING: manifest says ${idx.totalFills} fills, month files hold ${before}.`);
    console.error('The repo is internally inconsistent — fix that before syncing.');
    process.exit(1);
  }

  const csvs = fs.readdirSync(CSV_DIR).filter(f => f.toLowerCase().endsWith('.csv')).sort();
  const imports = [];
  for (const name of csvs) {
    // latin1: Webull exports are not UTF-8 and a wrong decode corrupts symbols.
    const text = fs.readFileSync(path.join(CSV_DIR, name), 'latin1');
    let fills;
    try { fills = parseWebull(text); }
    catch (e) { console.error(`SKIP ${name}: ${e.message}`); continue; }
    let seen = 0, fresh = 0, dup = 0, first = null, last = null;
    for (const f of fills) {
      seen++;
      if (!first || f.t < first) first = f.t;
      if (!last || f.t > last) last = f.t;
      const m = monthOf(f.t);
      months[m] = months[m] || {};
      if (months[m][f.k]) { dup++; continue; }   // existing key wins
      months[m][f.k] = compact(f);
      fresh++;
    }
    imports.push({ at: new Date().toISOString(), dup, first, fresh, last, name, seen });
  }

  const shards = Object.keys(months).filter(m => Object.keys(months[m]).length).sort();
  const shardInfo = [], files = {};
  let total = 0;
  for (const id of shards) {
    const body = serializeMonth(months[id]);
    files[path.join(DATA_DIR, 'fills', id + '.json')] = body;
    const n = Object.keys(months[id]).length;
    total += n;
    shardInfo.push({ id, fills: n, bytes: Buffer.byteLength(body) });
  }
  if (total !== shardInfo.reduce((n, s) => n + s.fills, 0)) {
    console.error('REFUSING: shardInfo does not sum to the fill total.'); process.exit(1);
  }

  const now = new Date();
  const snapshotAt = now.toISOString();
  const generatedUtc = snapshotAt.slice(0, 19) + 'Z';
  const meta = { ...idx.meta };
  if (imports.some(i => i.fresh > 0)) {
    meta.imports = [...imports.filter(i => i.fresh > 0), ...(idx.meta.imports || [])].slice(0, 50);
  }
  meta.snapshotAt = snapshotAt;

  const next = { ...idx, generatedUtc, snapshotAt, shards, shardInfo, totalFills: total, meta };
  files[path.join(DATA_DIR, 'index.json')] = serializeIndex(next);

  const changed = Object.keys(files).filter(p => {
    let cur = null; try { cur = fs.readFileSync(p, 'utf8'); } catch (e) { /* new file */ }
    if (cur === null) return true;
    // The manifest always differs on its timestamps; compare it without them.
    if (p.endsWith('index.json')) {
      const strip = (s) => s.replace(/"(generatedUtc|snapshotAt)": "[^"]*"/g, '"$1": ""');
      return strip(cur) !== strip(files[p]);
    }
    return cur !== files[p];
  });

  const summary = {
    csvs: csvs.length,
    freshFills: total - before,
    totalFills: total,
    months: shards.length,
    changedFiles: changed.map(p => path.relative('.', p)),
    imports: imports.map(i => ({ name: i.name, seen: i.seen, fresh: i.fresh, dup: i.dup })),
  };

  if (CHECK) { console.log(JSON.stringify({ mode: 'check', ...summary }, null, 2)); return; }
  if (!changed.length) { console.log(JSON.stringify({ mode: 'write', wrote: [], ...summary }, null, 2)); return; }
  for (const p of changed) fs.writeFileSync(p, files[p]);
  fs.writeFileSync(path.join(DATA_DIR, '.last-check'),
    `${generatedUtc} newest-source=${summary.freshFills ? imports.filter(i => i.fresh).map(i => i.name).join(',') + ` (${summary.freshFills} new fills, last ${imports.filter(i => i.fresh).map(i => i.last).sort().pop()})` : 'no new fills'}\n`);
  console.log(JSON.stringify({ mode: 'write', wrote: changed.map(p => path.relative('.', p)), ...summary }, null, 2));
}

main();
