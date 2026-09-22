# Trade-Journal — nightly sync runbook

Canonical. Where the routine prompt and this file disagree, this file wins.

## The chain

    Webull CSV (Mac) → artifact DB → shards → GitHub → Pages

This repo is a **read-only mirror** of a private Webull options journal. The
authoring surface is the Claude artifact, which holds the database; the page
here is the same engine running against a static snapshot.

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

## Two writers during the changeover

The nightly routine is **device-bound**: editing its content requires a device
attestation from the Mac it is bound to, which a cloud session cannot produce.
So until Ty updates it from the laptop, the old sync still runs and still
writes a whole `data/journal.json`, while this repo now carries shards.

Preferring either one blindly would serve a stale page with fresh data sitting
beside it — the exact failure this whole rebuild exists to remove. So the
loader takes **whichever was published more recently**, comparing
`Last-Modified` with a HEAD request on each so it never downloads 6.7 MB just
to read a date.

Verified both directions: with the whole file newer it is used and zero shards
are fetched; with the shards newer all 49 are fetched and the only
`journal.json` request is the HEAD. The page renders identically either way
(1,913 chars, hash `69866e19`).

Once the routine is updated to publish shards, delete `data/journal.json` and
this paragraph.

## What remains Mac-bound, and why

**Collection only.** The source is `.csv` exports Ty drops into
`09 Trading/Trade Journal/Raw Records/` on the laptop. Nothing in the cloud can
reach that folder, so a run that must ingest a *new* export needs the Mac. That
is a real constraint, not a false assumption — unlike the push, which was only
ever blocked by the 1 MB limit.

A run with no new CSV is fully cloud-capable: rebuild the shards from the
artifact DB and publish. So the page keeps updating whether or not the laptop
is awake; only new fills wait for it.

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

No PAT in this tree. Once the sync publishes from the cloud, the token file on
the Mac is no longer read by anything and should be revoked on GitHub.
