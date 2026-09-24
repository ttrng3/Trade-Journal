# Trade-Journal — monthly backup and restore

## What runs

On the 1st of every month at 02:30 UTC (09:30 Vietnam),
`.github/workflows/monthly-backup.yml` packs everything under `data/` into one
file, `trade-journal-backup-YYYY-MM-DD.json.gz` (~0.7 MB), proves it restores
byte-identical, and attaches it to a release tagged `backup-YYYY-MM-DD`:

    https://github.com/ttrng3/Trade-Journal/releases

It can also be run on demand from the Actions tab ("Monthly backup" → Run
workflow).

## Why a GitHub Action and not the Drive connector

A Claude routine can only write to Drive by passing the file's full content
through the model as a tool argument. The backup is 6.5 MB of JSON (0.7 MB
gzipped, ~0.95 MB base64), which is far past what a routine can emit. The
Action needs no model and no credential beyond its own job token.

**The catch:** a release lives inside the repo. If the repo itself were
deleted, its releases would go with it. So download each month's file and keep
it off GitHub — Drive `09 Trading/Trade Journal/Backups/` is the natural place.
Missing a month is harmless: each file is a full snapshot, not an increment.

## Restore

From the repo root:

    node tools/restore.js trade-journal-backup-YYYY-MM-DD.json.gz --check   # dry run
    node tools/restore.js trade-journal-backup-YYYY-MM-DD.json.gz           # write data/

then commit `data/` and push. Pages picks it up on the next deploy.

The restore checks every file against the SHA-256 recorded at backup time and
the fill count against the manifest **before writing anything**; a corrupt or
truncated file is refused whole. It replaces `data/` with the snapshot and
removes month files the snapshot does not know about.

Fills that arrived after the backup was taken are not lost: they are still in
the Webull CSVs on Drive, and the next nightly sync adds them back (existing
keys win, so nothing duplicates).

## The file

Gzipped JSON, format `trade-journal-backup/1`:

    { format, createdUtc, repo, commit, totalFills, months, dataGeneratedUtc,
      sha256: { "<path>": "<hex>" },
      files:  { "index.json": "<exact text>", "fills/2020-12.json": "…", … } }

Each file is stored as its exact text, not re-parsed, so a restore reproduces
`data/` byte for byte and `tools/sync.js --check` afterwards reports
`"changedFiles": []`. Verified at creation (2026-09-24): 23,422 fills, 49
months, 51 files; restore into an empty tree `diff -r` clean, sync check clean,
a one-byte edit refused on hash.
