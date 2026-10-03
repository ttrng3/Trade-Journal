# Verification: the monthly Drive backup

## Promise

`tools/monthly-drive-backup.sh` saves the month's master file to `Backups/`, byte-identical to the release. It moves only CSVs whose fills are already in the journal, verified file by file. A second run changes nothing. On any failure it removes nothing and says so.

## Clean state

Run on the Mac from the repo root, against a scratch folder, never the real Drive folder:
```bash
D=$(mktemp -d); mkdir -p "$D/Raw Records"
```
Put one CSV that is already synced in `$D/Raw Records/` (any file from `Backups/CSVs to …/`). Add one CSV holding a fill the journal doesn't have: copy a synced CSV and change the price on its first data row.

## Steps

1. `TJ_DRIVE_DIR=$D tools/monthly-drive-backup.sh`
   **Expected:**
   - exit 0;
   - `Backups/` holds this month's master, and its SHA-256 equals the release asset's;
   - the synced CSV is in `Backups/CSVs to <today>/` and gone from `Raw Records/`;
   - the unsynced CSV is still in `Raw Records/`;
   - `backup-log.md` has one line.
2. Run step 1's command again. **Expected:** exit 0; the hash list of every file under `$D` is identical before and after; the log has no new line.
3. Remove the master from `Backups/`, put the synced CSV back, and create `Backups/CSVs to <today>/` with mode 555. Run again. **Expected:** exit 1, a "FAILED … Nothing was removed." log line, and both CSVs still in `Raw Records/`.
4. Make `Backups/` mode 555 and run again. **Expected:** exit 1, and `Raw Records/` unchanged.
5. `git grep -n -i -E 'gmail\.com|GoogleDrive-[a-z]'`. **Expected:** no output. The pattern is written so this line can't match itself.
6. Live check: `launchctl print gui/$UID/com.tytr3.trade-journal-backup | grep -E 'state|last exit'`, then `launchctl kickstart gui/$UID/com.tytr3.trade-journal-backup`. **Expected:**
   - the job is loaded;
   - the kicked run exits 0;
   - in the month its master is already saved, the run writes nothing.

Measured 2026-10-03 on branch `work/monthly-drive-backup`: steps 1–5 passed.

## Adversary

- **A CSV that hasn't synced gets moved, and its fills exist nowhere else.** Each CSV is checked alone against a fresh clone of `main` before it moves. Step 1 proves an unsynced one stays.
- **A half-written copy on a cold Drive placeholder, then the original deleted.** Size and SHA-256 must match before `rm`, and the master is written as `.part` and renamed only after its hash matches. Steps 3–4 prove a failure removes nothing.
- **The Drive path, which holds the account email, leaks into the public repo.** It lives only in the local plist. Step 5.

## Not covered

- Whether launchd actually fires on 2026-11-01. That is checked by looking at `Backups/` in the first session on or after that date.
