# Trade-Journal — monthly backup and restore

## What runs

On the 1st of every month at 06:17 UTC (13:17 Vietnam), after that day's 04:00 UTC sync when the 1st is a sync day (Tue–Sat; the routine's cron is `0 4 * * 2-6`),
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
deleted, its releases would go with it. So each month's file is also copied to
Drive, by a job on Ty's Mac (added 2026-10-03, `work/261003-monthly-drive-backup/`).

## The Drive copy (Mac job)

`tools/monthly-drive-backup.sh` runs every day at 14:00 Hanoi from a launchd job,
or at the next wake if the Mac was asleep. It acts once a month: when this
month's `trade-journal-backup-YYYY-MM-01.json.gz` isn't in Drive
`09 Trading/Trade Journal/Backups/` yet. In that run it

1. downloads the master from the release, checks it with `restore.js --check`
   against a fresh clone of `main`, copies it into `Backups/` and confirms the
   SHA-256;
2. moves every CSV in `Raw Records/` whose fills are already in the journal
   (`sync.js --check` prints `"changedFiles": []` for it alone) into
   `Backups/CSVs to <date>/`: copy, check size and SHA-256, then remove. A CSV
   that hasn't synced yet stays for next month.

It never deletes a copy, never writes to the repo, and on any failure removes
nothing, adds a line to `Backups/backup-log.md` and shows a Mac notification.
Ty authorized these monthly moves on 2026-10-03 (the spec's Conflicts table).

The job is `~/Library/LaunchAgents/com.tytr3.trade-journal-backup.plist`, local
only. It sets `TJ_DRIVE_DIR` to the Trade Journal folder on Drive, which is a
personal path and so is never written into this repo. Its output goes to
`~/Library/Logs/trade-journal-backup.log`. Turn it off with
`launchctl bootout gui/$UID ~/Library/LaunchAgents/com.tytr3.trade-journal-backup.plist`.
Missing a month is harmless: each master is a full snapshot, not an increment,
and the job catches up the next time the Mac is awake.

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
the Webull CSVs on Drive, and the next sync adds them back (existing
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
