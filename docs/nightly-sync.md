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

Largest shard is **710 KB**. The laptop and the token went away with the
split; since 2026-09-24 the cloud session pushes through its own git proxy
(see *Pushing*), and the 1 MB cap binds only the file-tools fallback. A nightly sync touches only the **current month's** shard instead of
re-uploading 6.66 MB every night — but by late in a busy month that one shard
is hundreds of KB (2026-09 was 351 KB at commit `2663407`, 2026-09-30), so it is pushed with
shell git, not the file tools (see *Pushing* below).

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
  token-in-URL. The routine now pushes through the cloud session's own git
  credential proxy, which needs no token in this tree (see *Pushing*).

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

## Pushing

**Shell `git push` is the path for any run that changes a month shard.** Commit
the changed files together and push to `main`. The cloud session already has a proxied git credential, so no token
is read or written. Every fill run since 2026-09-24 went this way: those commits
are authored by the Claude bot account and change the month shard,
`index.json` and `.last-check` in one commit (e.g. `2663407`, 2026-09-30).

Why not the file tools for the shard: `create_or_update_file` takes the whole
file inline, one call per file, so a 351 KB shard would pass through the model
character by character, with a real chance of silent corruption and three
commits instead of one.

**The GitHub MCP file tools are for small files only.** A run with no new fills
writes `.last-check` (a few bytes) with them; those commits carry the author
`ttrng3`.

**If the push is refused as non-fast-forward** (something reached `main` after
the clone), run `git pull --rebase origin main` once and push again. If the
rebase stops on a conflict (another data commit got there first), run
`git rebase --abort` and treat it as a second refusal.

**If the push is refused again, or for any other reason** (auth, proxy), do
not re-send the shard through the file tools.
Still write the heartbeat, alone, with the file tools, and make its source
field say so: `<UTC stamp> newest-source=BLOCKED: push refused`. The preview
step runs as on every run (it will find nothing new). Report the run as
**BLOCKED** with the refusal. The watchdog reads only the stamp, so a
push that keeps being refused raises no automatic alarm until
`MAX_DATA_AGE_DAYS` (14) — the BLOCKED report and the `newest-source=BLOCKED` heartbeat
line are the signal. Nothing is lost: the next run re-reads every CSV
in `Raw Records/`, dedups by fill key, and pushes the same fills.

## Verifying a run — never fetch the live site

Confirm `main` moved — after a shell push, `git fetch origin` then
`git merge-base --is-ancestor HEAD origin/main` (it prints nothing: exit
status 0 means `main` has the commit, 1 means it does not); after a file-tools write, the
sha it returned — and read the file back. Do
not `curl` or `WebFetch` https://ttrng3.github.io/ from a routine: cloud egress
rejects it with `CONNECT 403`, and WebFetch then raises a permission prompt
nobody is there to answer, parking the run with its work already committed.

The old step 6 did exactly this — "fetch … allow up to 3 minutes for Pages to
redeploy". Pages propagation is not observable from the sandbox.

## Case

The repo is `ttrng3/Trade-Journal` and the site is
https://ttrng3.github.io/Trade-Journal/ — capital T and J. Lowercase 404s.

## Credentials

**No live credential in this repo or on Drive.** The sync pushes through the cloud session's
git credential proxy (small files: the GitHub MCP file tools). The
PAT at `09 Trading/Trade Journal/_secrets/github_token_trade-journal.txt` is no
longer read by anything; it was revoked on GitHub on 2026-09-23. Do not
reintroduce a token-in-URL push.
