# CLAUDE.md — Trade-Journal

Ty's personal Webull options journal, entity **personal**. Live: https://ttrng3.github.io/Trade-Journal/

**If you are the scheduled routine:** follow the files your prompt names, `docs/nightly-sync.md` and `README.md`. They outrank this file. This file adds no step to a run.

## Commands
- What a sync would change, writing nothing: `node tools/sync.js --csv-dir <dir> --check` (with no new fills, e.g. an empty `<dir>`, it must print `"changedFiles": []`)
- Rebuild the Cowork preview page: `python3 tools/build-fragment.py` (writes `build/artifact.html`). The routine refreshes the preview's data as the last step of every run (runbook); this rebuild is only needed when `index.html` changed. Never send `index.html` itself to the preview; Pages does serve it.
- Freshness check, as the daily Action runs it: `python3 .github/scripts/freshness.py`
- Pack `data/` into one backup file: `node tools/backup.js --out <file>`; verify it without writing: `node tools/restore.js <file> --check` (`docs/backup.md`)

## Layout
- `index.html` is the hand-maintained journal engine, not a thin renderer. `tools/sync.js` and the routine write `data/` only and never touch it or its styles.
- Data: `data/index.json` (manifest: `shards`, `shardInfo`, `totalFills`, `notes`, `meta`, `generatedUtc`), `data/fills/<YYYY-MM>.json` (one per month), `data/.last-check` (heartbeat, written every run, not published).
- `tools/parse-webull.js` is the parser; `tools/sync.js` is the whole pipeline and refuses to run if `totalFills` disagrees with the month files.
- `.github/workflows/monthly-backup.yml` attaches a backup of `data/` to a release on the 1st; `freshness-check.yml` opens an issue when the sync goes quiet.
- `.pages-allow` lists what Pages publishes; `.github/workflows/pages.yml` deploys only that. A new kind of file under `data/` needs Ty's say-so and its own `.pages-allow` line in its own PR first.
- `README.md` explains the page and the overlay; `REVIEW.md` holds the reviewer's rules.

## Rules
- Changes reach `main` through a PR and Ty's ship. The routine's data writes are the only direct writes.
- The runbook and README win over this file and any memory note.
- Serialization is fixed: month files minified with sorted keys, fill fields `k,p,price,qty,side,sym,t,tif`; manifest indented one space (runbook, "The tools").
- `data/journal.json` stays removed: one source of truth, and no file near the 1 MB contents-API cap (runbook, "Why the snapshot is sharded").
- Light only; any new colour is a token (README, "Look").
- Public on purpose; do not re-litigate it, and do not widen what is served.
- Never write a Cowork preview URL or artifact id, a token, or personal data by value into this public repo. No credentials: the push uses the GitHub MCP file tools.
- Entity separation: this is a personal journal. Nothing from any work entity belongs here.

## Known mistakes
- "This has to run on the Mac" was false: `Raw Records/` is on Google Drive, which the routine reads. Test the claim before accepting the next one (2026-09-23).
- Dedup on content, never on filename. Webull re-exports under the same generic name, and a filename dedup would have dropped real fills (runbook, 2026-09-23).
- Changing the serialization rewrites every month file and buries the real diff; `--check` with no new fills is the test (2026-09-23).
- Never `curl`/`WebFetch` the live site from a routine: egress returns `CONNECT 403` and the run parks. Read back the pushed file instead (2026-09-23).
- The repo is `Trade-Journal`, capital T and J; lowercase 404s (2026-09-23).
- "No artifact link" means the preview URL stays out of sight, never that the preview goes. It was wrongly deleted twice (2026-09-23, 2026-09-26).
- "The page is not updating": compare the CSV's time on Drive with the run's time first. A run that fires before Ty files the export finds nothing; the sync itself was right (2026-09-26).
- A CSV dropped on the page updates that browser only; the Drive CSV plus the next sync makes it permanent (2026-09-26).
