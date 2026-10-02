# Verification: the trade journal

## Promise

Every file https://ttrng3.github.io/Trade-Journal/ serves (the page, `index.json`, every month file) is byte-identical to `main`. The manifest's shards are well-formed `YYYY-MM` months in order, each with its file; each month file matches its `shardInfo` count and byte size, keeps the fixed serialization (minified, sorted keys) and the fixed fill fields, holds only its own month's fills, and no fill appears twice; `totalFills` is their sum. The sync's own dry run with no new CSV changes nothing. `data/journal.json` stays removed. In a browser with no overlay, the page shows the snapshot `main` holds, with its charts and no error. The run and the data are fresh. No private file, personal link, email address, account handle, Drive id or Cowork preview tag sits in any served or tracked file, and no work entity is named anywhere in this repo. The Cowork preview carries `main`'s data or the last run's.

## Clean state

```bash
cd ~/Projects/Trade-Journal && git checkout main && git pull --ff-only
```
Run on the Mac, never from the routine (a live-site fetch from a routine parks the run: CLAUDE.md, 23/09). Needs `node` for the sync's dry run. Run after a sync (the routine's cron, `0 4 * * 2-6` UTC = 11:00 Hanoi Tuesday to Saturday, per the status page's collector on 01/10) or after any merge, once the merge's Pages run is green (`gh run list -w "Pages (allowlist)" -L1`).

## Steps

1. **Repo and live site.** `python3 tools/verify_live.py --forbid <words>` → exit 0 and `"pass": true`. The words are the work entities' and their dashboards' names, from the runner's own notes; this personal repo never spells them (Ty, 30/09). Without `--forbid` the entity verdict fails on purpose. Here it reads every tracked file, not only the served ones.
2. **Live page in Chrome.** Open https://ttrng3.github.io/Trade-Journal/ in a browser profile that has never imported a CSV here (a fresh profile or a guest window), and run the script under Invariants. Never clear `localStorage` in Ty's own browser: it holds his page-only notes, settings and dropped CSVs. Expected: the "snapshot … UTC" stamp equals `snapshotAt` to the minute; the dashboard draws its charts; no load error.
3. **Console.** After that reload, read errors for `TypeError|ReferenceError|Uncaught|SyntaxError`. Expected: none.
4. **Preview.** Get the preview link from the routine's prompt (`RemoteTrigger get`). Never write it here. Find the last sync: `c=$(git log --first-parent --format='%h %s' -- data/index.json | grep -v ' (#[0-9]*)$' | grep -v '^[0-9a-f]* Merge ' | head -1 | cut -d' ' -f1)`. `Artifact list` the preview's files and `Artifact read` `data/index.json` and the newest month file. Expected: the page fragment plus the data files `main` or `$c` holds, nothing else; each file read has the sha256 of `main`'s copy (`shasum -a 256 <path>`) or `$c`'s (`git show $c:<path> | shasum -a 256`). The routine refreshes the preview's data as the last step of every run.

## Invariants

Step 1 prints these verdicts, all of which must be true: `shards_well_formed`, `shard_files_match`, `journal_json_absent`, `shards_sound` (each month file: `shardInfo` count and bytes, serialization, fields `k,p,price,qty,side,sym,t,tif`, own month only), `total_fills_match`, `no_duplicate_fills`, `sync_check_clean` (`node tools/sync.js --csv-dir <empty> --check` → `"changedFiles": []`), `served_equals_main`, `private_not_served` (and `data/journal.json` answers 404), `heartbeat_fresh` (≤ 4 days, the watchdog for this Tue–Sat pipeline and `freshness.py`'s `MAX_RUN_AGE_DAYS`), `data_fresh` (≤ 14 days, `freshness.py`'s `MAX_DATA_AGE_DAYS` default), `all_tracked_read`, `no_personal_traces`, `no_drive_ids_tracked`, `no_preview_tags_tracked`, `no_forbidden_words`.

Step 2, in the page (no query strings in the fetches: the browser tool blocks them; if `no_overlay` is false, stop and reopen in a fresh profile rather than clearing anything):
```js
await new Promise(r=>setTimeout(r,4000));
const idx=await fetch('data/index.json').then(r=>r.json());
const shown=(document.body.innerText.match(/snapshot ([0-9-]+ [0-9:]+) UTC/)||[])[1]||'';
JSON.stringify({snapshot_matches:shown===idx.snapshotAt.slice(0,16).replace('T',' '),
  charts_render:document.querySelectorAll('svg,canvas').length>0,
  no_overlay:Object.keys(localStorage).filter(k=>k.startsWith('tj:')&&k!=='tj:range2').length===0,
  no_load_error:!/failed|error|không nạp/i.test(document.querySelector('main, body').innerText.slice(0,600))})
```
All of them must be true.

## Adversary

- **A stranger on the public journal** (public on purpose, Ty 29/09). `private_not_served`: the README, CLAUDE.md, REVIEW.md, both runbooks, the heartbeat, the seven `tools/` scripts, this protocol, one `work/` file found at run time, `freshness.py` and `.pages-allow` all exist on `main` and answer 404 live, and so does the removed `data/journal.json`. `no_personal_traces`, `no_drive_ids_tracked` and `no_preview_tags_tracked` read every served file live and on `main` and every other tracked text file, by count and file, never by value.
- **A work entity named in a personal repo** (30/09, again 01/10: #10). `no_forbidden_words` reads every tracked file with the names supplied at run time.
- **A sync that loses, doubles or misfiles fills.** `total_fills_match`, `no_duplicate_fills` (dedup on content, never on file name), `shards_sound` (own month only).
- **A serialization change that rewrites every month and buries the real diff** (23/09). `shards_sound` (serialization) and `sync_check_clean`.
- **A drifted manifest.** `shard_files_match`, `shards_sound` (`shardInfo`), `total_fills_match`; `sync.js` itself refuses to run on a `totalFills` mismatch.
- **A routine that stopped running.** `heartbeat_fresh`. **Weeks with no new fills:** `data_fresh`.
- **"The page is not updating"** when the overlay hides the snapshot. Step 2 runs where no overlay exists, and `no_overlay` proves it.

## Sanctioned substitutes

- The forbidden word list is passed on the command line, so this repo never spells the names. It cannot catch a name nobody listed.
- The preview cannot be fetched by a script, so step 4 is done by the runner with `Artifact list` and `Artifact read`.
- `shards_sound` re-serializes with Python and compares text with what `sync.js` wrote; the two differ only for numbers below 1e-4 or at 1e16 and above (exponent form), which option prices and quantities never reach. `sync_check_clean` is the sync's own test of the same thing.
- The sync's dry run uses an empty CSV folder, so it proves stable serialization, not that the parser reads a new Webull export: that is the runbook's job each night.

## Evidence

- The JSON from step 1 and the JSON from step 2.
- One screenshot (`save_to_disk: true`) of the dashboard in the overlay-free profile.
- For step 4: the preview's file list and the hashes read.

## Not covered

- Whether the fills equal Webull's own records: the CSV export on Drive is the source; the sync's content dedup is trusted.
- The monthly backup release (`monthly-backup.yml`): checked by `node tools/restore.js <file> --check` (`docs/backup.md`), not here.
- Figures shown for a custom date range: the page computes them in the browser from the same fills.

## Traps

- The script adds a cache-busting query to every request, so a `served_equals_main` failure straight after a merge means the Pages run has not finished: wait for it to go green, then re-run. Each request retries once on a network error or a 5xx.
- The page keeps a per-browser overlay: a CSV dropped on it, notes and settings live in `localStorage`. Step 2 must run where there is none, or the page shows that browser's data, not the snapshot. The page's keys all start `tj:` (`tj:range2` is only the selected date range). Do not clear them to get there: on 01/10 the first run of this step cleared `localStorage` in Ty's own Chrome and erased at least his saved date range.
- The CSV's time on Drive is shown in Hanoi time (UTC+7); the run's time is logged in UTC. Compare the two before calling a sync late (CLAUDE.md, 26/09).
- The browser tool refuses fetches with a query string, so step 2 fetches plain paths (01/10).
- The repo is `Trade-Journal`, capital T and J; lowercase 404s.
