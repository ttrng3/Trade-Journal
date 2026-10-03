# Spec: monthly-drive-backup

**Approved:** 2026-10-03 · Requirement 1 narrowed to monthly CSV moves after approval, awaiting Ty's confirmation

**Intent:** accepted 2026-10-03 · **Status:** approved

## Requirements

1. **Daily, idempotent run.** A launchd job on Ty's Mac runs once a day at 14:00 Hanoi, which is after the backup Action's 06:17 UTC run on the 1st. If the Mac was asleep, launchd runs it at the next wake. It does work only when this month's master isn't in `Backups/` yet; the CSV moves happen in that same run, so CSVs move once a month, not daily. Otherwise it exits without writing anything (intent, Outcome 1–3). *(Narrowed after approval to match Ty's "on the first of each month"; awaiting Ty's confirmation.)*
2. **Master file.** The job downloads `trade-journal-backup-<YYYY-MM>-01.json.gz` from the public release URL with `curl`, which needs no credential. It runs `restore.js --check` on the file from a fresh clone of `main`, copies the file to `Backups/`, and confirms the copy's SHA-256 matches. If the release isn't published yet, it exits quietly and tries again the next day (Outcome 1).
3. **CSV moves.** For each `*.csv` in `Raw Records/`, the job puts that one file alone in a temporary folder and runs `sync.js --check` against the fresh clone's `data/`. It moves the file only when the check prints `"changedFiles": []`:
   - it copies the file to `Backups/CSVs to <YYYY-MM-DD>/`;
   - it confirms the copy has the same size (above zero) and the same SHA-256;
   - only then does it remove the original.

   Any other result leaves the file in place (Outcome 2–3).
4. **Failure.** Any failed check stops that file and removes nothing. The job appends one dated line per run that did work, or failed, to `Backups/backup-log.md`. On failure it also shows a macOS notification (Outcome 4).
5. **Scope.** The job never writes to the repo, `data/` or Ty's working tree. It reads the public repo only through a shallow clone in a temporary folder, which it deletes afterwards.

## Design

- **`tools/monthly-drive-backup.sh`** (new, about 60 lines of bash; `node` and `curl` only).
  - The Drive folder comes from the environment variable `TJ_DRIVE_DIR`. The script contains no personal path.
  - `set -euo pipefail`, with a trap that sends the notification on any error.
  - It stops at the first I/O error. That covers "Resource deadlock avoided" and a zero-byte copy, which the root rule treats as STOP.
- **`~/Library/LaunchAgents/com.tytr3.trade-journal-backup.plist`** (local only, never in the repo).
  - Runs the script from the repo checkout.
  - Sets `TJ_DRIVE_DIR`, a `PATH` containing `/usr/local/bin`, and `StartCalendarInterval` Hour 14 Minute 0.
  - Logs to `~/Library/Logs/trade-journal-backup.log`.
- **`docs/backup.md`:** replace "download each month's file and keep it off GitHub" with a section on the job: what it does, how to install or remove it, and where its log is.
- **Pipeline Wiring:** a section-5 entry naming this as a Mac dependency, in its own PR at ship time, per the trade-journal-pipeline rule.
- **No change** to `index.html`, `data/`, `tools/sync.js`, the nightly routine or the backup Action.

## Conflicts

Policy loaded this session:
- kernel "Standing Instructions" and root `CLAUDE.md`;
- the repo `CLAUDE.md`;
- memory "artifact-mirror-contract" and "trade-journal-pipeline";
- secure-pages, run on this repo today and again below.

The apple-design skill doesn't apply: there is no UI.

| Rule (by name) | What in the design touches it | Resolution |
|---|---|---|
| "File operation safety — copy, verify size, then delete", item 9: "Never autonomously delete, rename, move or archive" (root `CLAUDE.md`) | The job moves CSVs out of `Raw Records/` every month with nobody present. | **Ty, 2026-10-03 (approve):** this instruction ("move the CSVs into the backups") is the standing authorization for this job only. The job only moves `*.csv` files out of `Raw Records/` and only after their fills are in the journal, and it never deletes a copy.  |
| Same rule, items 2–5 (copy, then check size, then delete; stop on I/O errors) | The moves happen on the Drive mount. | Requirements 3 and 4: copy, size and hash check, then remove, file by file. It stops on any error and never uses `mv`. |
| "Strategic objective" (root `CLAUDE.md`: flag every Mac dependency as debt) | This is a new Mac dependency. | Ty chose it on 2026-10-03 over a Google credential in GitHub. It's named on the Pipeline Wiring page, section 5. |
| "Never write … personal data by value into this public repo" (repo `CLAUDE.md`) | The Drive path contains the account's email. | The path lives only in the local plist, as `TJ_DRIVE_DIR`. Promise 4 greps the repo for it. |
| "Changes reach `main` through a PR and Ty's ship" (repo `CLAUDE.md`) | — | Branch `work/monthly-drive-backup`, PR, reviewer, then Ty ships. The plist is installed after the merge. |
| Nightly runbook: "Nothing is lost, provided those CSVs are still in `Raw Records/`" | Moving a CSV that hasn't synced would break that promise. | Requirement 3 moves only CSVs whose fills `sync.js --check` finds already in `main`'s `data/`. |
| Entity separation | — | None: personal journal. |

## Security (secure-pages, 2026-10-03)

The check from earlier today stands:
```
1 Secrets ........ PASS (rerun on the branch before the PR)
2 Visibility ..... PUBLIC — PASS (no new served file)
3 Pages .......... PASS — .pages-allow unchanged; tools/ and work/ not served
4 Supabase ....... N/A
Verdict: safe to ship
```

## Promise

1. **Drill on a scratch copy.** Run the script with `TJ_DRIVE_DIR` set to a scratch folder holding:
   - a `Raw Records/` with one already-synced CSV and one CSV carrying a fill that isn't in the journal;
   - no `Backups/` folder.

   **Pass:**
   - October's master is in `Backups/` with a matching SHA-256;
   - the synced CSV is in `Backups/CSVs to <today>/` with a matching hash and gone from `Raw Records/`;
   - the unsynced CSV is still in `Raw Records/`;
   - `backup-log.md` has one line.
2. **Idempotent.** Run the script a second time on the same scratch folder.
   **Pass:** no file changes and no new log line.
3. **Failure path.** Make the copy target read-only and run again.
   **Pass:** the script exits non-zero, a notification fires, and `Raw Records/` is unchanged.
4. **Nothing personal in the repo.** `git grep` for the account email and `CloudStorage`.
   **Pass:** 0 hits.
5. **Live install.** After the merge, run `launchctl print gui/$UID/com.tytr3.trade-journal-backup` and kick it once.
   **Pass:** the job shows as loaded; the run is a no-op, because October is already done and Raw Records holds only CSVs that haven't synced; and the log says so.
6. **First real run, 2026-11-01.** **Pass:** November's master and October's synced CSVs are in `Backups/`. I'll check this at the first session on or after that date.

## Out of scope

- No deletion of anything, ever.
- No change to how the master file is made.
- No cloud runner and no Google credential.
- No cleanup of `Backups/`; it grows by about 1.5 MB a month.
- The old Drive files beside `Raw Records/` (the v1–v3 docs, `site/`, the zip) are left as they are.
