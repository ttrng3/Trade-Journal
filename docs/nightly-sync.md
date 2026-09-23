# Trade-Journal — nightly sync runbook

Canonical. Where the routine prompt and this file disagree, this file wins.

## The chain

    Webull CSV (Google Drive) → cloud routine → GitHub → Pages

**This repo is the source of truth.** `data/fills/<YYYY-MM>.json` holds the
fills and `data/index.json` is the manifest; the page is the same engine
running against them.

Until 2026-09-23 the chain ran the other way — `Webull CSV (Mac) → artifact DB
→ shards → GitHub → Pages` — with a claude.ai artifact database as the source
and this repo as a read-only mirror. Ty ruled that day that the repo URL is
what gets used internally and that the same information must not sit in two
places. The artifact was deleted, the flow was inverted, and the Mac dropped
out of it entirely.

## Why the snapshot is sharded

`data/journal.json` was a single **6.66 MB** file. That is what pinned the
nightly push to the laptop: the GitHub contents API caps a single file at
**1 MB**, so no cloud session could write it, and the routine had to shell out
on the Mac through `device_bash` with a personal access token read from
`09 Trading/Trade Journal/_secrets/github_token_trade-journal.txt`.

The snapshot is now split by month:

    data/index.json          manifest: shards[], notes, meta, generatedUtc
    data/fills/<YYYY-MM>.json   one file per month, 49 of them

Largest shard is **710 KB**, comfortably under the limit, so the cloud can
write them with the GitHub MCP tools and no token. Better still, a nightly sync
touches only the **current month's** shard — a few KB — instead of re-uploading
6.66 MB every night.

Verified at both levels when the split was made: the rendered page was
byte-identical (1,913 chars, hash `69866e19`), and the reassembled data was
deep-equal to the original — 23,257 fills, `meta` and `notes` identical.

`data/journal.json` has been removed so there is one source of truth. The
loader still falls back to a whole-file `journal.json` if no manifest is
present, which keeps other copies of the page working; the mirror does not use
that path.

## Why it is no longer Mac-bound

The old runbook said, of the CSV folder: *"Nothing in the cloud can reach that
folder, so a run that must ingest a new export needs the Mac. That is a real
constraint, not a false assumption."* **It was a false assumption.**
`09 Trading/Trade Journal/Raw Records/` is on **Google Drive**, and the routine
has the Drive connector. The laptop was never required to read the source; it
was required only because the pipeline had grown around it.

Two other things were dragging the Mac in, and both are fixed:

- **The parser** was scraped out of `260917_TRD_System_Webull-Trade-Journal_v1.html`
  on Drive, lines 158–242, on every single run. It now lives here as
  `tools/parse-webull.js`, lifted verbatim.
- **The push** used a fine-grained PAT from `_secrets/` on Drive, via
  token-in-URL. The routine now writes with the GitHub MCP file tools, which
  need no token in this tree.

Check the claim before accepting the next "this has to run on the Mac".

## The tools

    node tools/sync.js --csv-dir <dir> [--data-dir data] [--check]

`--check` parses, merges and reports what *would* change without writing.
**With no new fills it must report `"changedFiles": []`.** That is the
regression test for the serialization, and it is not cosmetic: month files are
minified with keys sorted ascending and fill fields in alphabetical order
(`k,p,price,qty,side,sym,t,tif`), and the manifest is pretty-printed with a
**one-space** indent. Change either and all 49 months rewrite, burying the real
change in noise.

`sync.js` refuses to run if `index.json`'s `totalFills` disagrees with what the
month files actually hold, rather than papering over a corrupt tree.

## Dedup on content, never on filename

Fills are keyed and **existing keys win**, so re-importing a CSV is always
safe. This is not a nicety. Webull re-exports to the same generic filename
`Webull_Orders_Records_Options.csv`, and on 2026-09-23 that file came back
holding 100 genuinely new fills under a name already in the import ledger. A
filename-only dedup would have silently dropped them.

## The heartbeat

`data/.last-check` is written on **every** run including nights with no new
fills. It separates "ran, nothing new" from "stopped running". The repo's own
history shows why that matters: several commits read `0 new fills`, which is
indistinguishable from a broken sync unless the run leaves its own mark.

Thresholds are tighter here than the weekly dashboards — the sync runs
Tue–Sat, so `MAX_RUN_AGE_DAYS=4` and `MAX_DATA_AGE_DAYS=14`.

The old watchdog measured `index.html`'s commit age. The routine is explicitly
told never to touch `index.html`, so that clock never moved and the check would
have false-alarmed within 10 days of being installed.

## Timestamps

`meta.snapshotAt` comes from JS `toISOString()` and carries milliseconds. The
page displays it, so it is stored verbatim. `generatedUtc` is the same instant
rounded to seconds and is what the watchdog parses; the watchdog also tolerates
a fractional-second stamp so a future producer cannot break it.

## Verifying a run — never fetch the live site

Confirm `main` moved by the sha each write returned and read the file back. Do
not `curl` or `WebFetch` https://ttrng3.github.io/ from a routine: cloud egress
rejects it with `CONNECT 403`, and WebFetch then raises a permission prompt
nobody is there to answer, parking the run with its work already committed.

The old step 6 did exactly this — "fetch … allow up to 3 minutes for Pages to
redeploy". Pages propagation is not observable from the sandbox.

## Case

The repo is `ttrng3/Trade-Journal` and the site is
https://ttrng3.github.io/Trade-Journal/ — capital T and J. Lowercase 404s.

## Credentials

**None.** The sync publishes from the cloud with the GitHub MCP file tools. The
PAT at `09 Trading/Trade Journal/_secrets/github_token_trade-journal.txt` is no
longer read by anything; it was revoked on GitHub on 2026-09-23. Do not
reintroduce a token-in-URL push.
