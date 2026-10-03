# Verification: the monthly Drive backup

## Promise

`tools/monthly-drive-backup.sh` saves the month's master file to `Backups/`, byte-identical to the release. It moves only CSVs whose fills are already in the journal, verified file by file. A second run changes nothing. On any failure it removes nothing and says so.

## Clean state

Run on the Mac from the repo root, against a scratch folder, never the real Drive folder:
```bash
D=$(mktemp -d); mkdir -p "$D/Raw Records"
```
Put three CSVs in `$D/Raw Records/`:

- `synced.csv`: a file already synced. Copy any file from `Backups/CSVs to …/` read-only.
- `unsynced.csv`: a copy of `synced.csv` with one **Filled** row changed in both Price and Avg Price, for example `@1.23` to `@9.87`. The parser keys a fill on Avg Price, and a Cancelled row isn't a fill, so editing any other row changes nothing.
- `empty.csv`: only the header line of `synced.csv`.

## Steps

1. `TJ_DRIVE_DIR=$D tools/monthly-drive-backup.sh`
   **Expected:**
   - exit 0;
   - `Backups/` holds this month's master, and its SHA-256 equals the release asset's (`gh release download backup-YYYY-MM-01`);
   - `synced.csv` is in `Backups/CSVs to <today>/` and gone from `Raw Records/`;
   - `unsynced.csv` and `empty.csv` are still in `Raw Records/`;
   - `backup-log.md` has one "saved … moved 1 … left 2" line.
2. Run the same command again. **Expected:** exit 0; the sorted hash list of every file under `$D` is identical before and after; the log has no new line.
3. Remove the master from `Backups/` and move `synced.csv` back to `Raw Records/`. Create a second synced file, `synced2.csv`, in `Raw Records/` (another file from `Backups/CSVs to …/`). Pre-create `Backups/CSVs to <today>/synced2.csv` as a different file (`echo x >`) so the second move collides. Run again. **Expected:**
   - exit 1;
   - stderr has a `NOTIFY: Failed:` line;
   - the log's last line is "FAILED: synced2.csv already exists … 1 CSV(s) had already moved";
   - the master is **not** in `Backups/` (it is saved last), so the next day's run retries;
   - `synced2.csv` is still in `Raw Records/`.
4. Delete the collision file and run again. **Expected:** exit 0; `synced2.csv` moved; the master saved; one "saved" log line. This proves a failed month is picked up the next day.
5. Remove the master and the `Backups/CSVs to <today>/` folder, put one synced file in `Raw Records/`, make `Backups/` mode 555, and run. **Expected:** exit 1 (the move folder can't be created); a `NOTIFY: Failed:` line on stderr, even though the log can't be written; `Raw Records/` unchanged. Restore the mode afterwards.
6. `git grep -n -i -E 'gmail\.com|GoogleDrive-[a-z]|Cloud[S]torage/'`. **Expected:** no output. The patterns are written so this line can't match itself.
7. Live check, after the merge:
   - run `launchctl print gui/$UID/com.tytr3.trade-journal-backup | grep -E 'state|last exit'`, then `launchctl kickstart gui/$UID/com.tytr3.trade-journal-backup`;
   - **expected:** the job is loaded, the kicked run exits 0, and in a month whose master is already saved it writes nothing.

Steps 1–6 are run on the branch before the PR is shipped.

## Adversary

- **A CSV that hasn't synced gets moved, and its fills exist nowhere else.** Each CSV is checked alone against a fresh clone of `main` before it moves. Step 1 proves an unsynced one stays.
- **A half-written copy on a cold Drive placeholder, then the original deleted.** Size and SHA-256 must match before `rm`, and an unreadable file is a failure, never an empty hash that matches another empty hash (review #13). Steps 3 and 5 prove a failure removes nothing more.
- **An empty or unreadable CSV moved because it reports "no changes".** It must parse to at least one fill, all already in the journal. `empty.csv` in step 1.
- **A month left half-done and never retried.** The master is saved last, so its absence means "not finished". Steps 3–4.
- **A month whose release never appears.** After the 3rd, a missing release is a failure with a notification, not a silent skip. This is code-reviewed, not drilled: forcing it needs a fake date.
- **The Drive path, which holds the account email, leaks into the public repo.** It lives only in the local plist. Step 5.

## Not covered

- Whether launchd actually fires on 2026-11-01. That is checked by looking at `Backups/` in the first session on or after that date.
