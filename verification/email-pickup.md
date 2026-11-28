# Verification: the morning email pickup

## Promise

Each run of the Trade Journal routine saves the options CSV from every Webull export email still in the inbox into `Raw Records/` as the next `… copy N.csv`, byte-identical to the attachment and stored as a plain CSV, then moves that email, and only that email, to Gmail trash. With no export email it saves nothing, trashes nothing and reports "No webull email found". Spec: `work/261128-webull-email-pickup/spec.md`.

## Clean state

- The routine's live config (`RemoteTrigger get`) has the Gmail connector with exactly four permitted tools: `search_threads`, `get_message`, `download_gmail_attachment`, `trash_message`; and its Drive connector permits `create_file`, `download_file_content` and `update_file` (an empty permitted list means all).
- `main` holds this runbook's "Email pickup (step 0)" section.
- Write down the names in `Raw Records/` and the Gmail search `from:noreply@webull.com subject:Webull_Orders_Records in:inbox` result before each step.

## Steps

1. **One email.** Ty emails one export from Webull and leaves it unopened. Confirm the search above returns exactly that one message. Fire the routine once (`RemoteTrigger run`) and wait for it to finish (`list_runs`).
   **Expected:**
   - `Raw Records/` has exactly one new file, named the next free `Webull_Orders_Records_Options[ copy[ N]].csv`;
   - its Drive `mimeType` is `text/csv` (not a Google Sheet);
   - its sha256 equals the sha256 of the email's `Webull_Orders_Records_Options.csv` attachment, downloaded separately in this session;
   - the same search now returns nothing, and the message is in Gmail trash; no other message changed label;
   - `data/.last-check` on `main` ends with `email=saved`;
   - the run report's line 1 names the file and the trashed email;
   - on a fresh clone of `main`, `node tools/sync.js --csv-dir <dir holding every Raw Records CSV> --check` prints `"changedFiles": []`.
2. **No email.** With the search returning nothing, fire the routine again.
   **Expected:** no new file in `Raw Records/`; nothing moved in Gmail; `data/.last-check` ends with `email=none`; the report's line 1 says "No webull email found".
3. **Already saved.** Ty emails one more export of a session whose CSV is already in `Raw Records/` (byte-identical), and leaves it. Fire the routine.
   **Expected:** no new file in `Raw Records/`; that email is in Gmail trash; `data/.last-check` ends with `email=saved`; the report says the CSV was already saved.
4. **Forced failure.** Ty emails one export and leaves it. Remove the Gmail connector's `trash_message` from the routine's permitted tools, fire the routine, then restore it.
   **Expected:** the CSV is saved (or found already saved) as a `.csv`; the email is still in the inbox; `data/.last-check` ends with `email=FAILED`; the report names the trash failure. The next run (after the restore) saves no new file and trashes the email (`email=saved`).
5. **Schedule.** `RemoteTrigger get`. **Expected:** `cron_expression` is `0 23 * * 1-5`; `next_run_at` is a 23:00 UTC time on a Monday–Friday (06:00 Hanoi Tuesday–Saturday).
6. **First real morning** (the first scheduled fire after step 5). **Expected:** `last_fired_at` is that morning's 23:00 UTC; step 1's checks hold for the export Ty emailed the night before; the new fills are in `data/fills/` on `main`.
7. `python3 tools/scan_public.py --all` and `git grep -n -E 'msg-f[:]|thread-f[:]|\b[0-9a-f]{16}\b' -- work docs verification README.md CLAUDE.md`. **Expected:** `scan: 0 hit(s)` and no grep output: no personal address and no Gmail message or thread id (the connector returns 16 hex characters, checked 2026-11-28) in the repo. The grep patterns are written so this line can't match itself.

## Results

(none yet)
