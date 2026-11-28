# Spec: webull-email-pickup

**Approved:** 2026-11-28
**Intent:** accepted 2026-11-28 · **Status:** approved

## Requirements
1. Each run, before the sync, finds every Webull order-records email still in the inbox (intent Outcome 1).
2. From each, saves only the options CSV into `Raw Records/` as the next free name in Ty's own scheme (Outcome 2).
3. The saved file is a plain CSV on Drive, byte-identical to the attachment, checked by reading it back before anything else happens (Outcome 3).
4. The email goes to Gmail trash only after check 3 passes; on any failure it stays in the inbox and the run reports it (Outcome 3, Constraints "trash only").
5. Sync, dedup, publish and preview run exactly as today (Outcome 4, Constraints).
6. The routine fires 06:00 Hanoi, Tuesday to Saturday (Outcome, Ty's 04:00 latest send).
7. On a run with no export email, the report says "No webull email found", and the run leaves a machine-readable mark the morning brief can read later (Ty's answer 2).
8. Runbook and Pipeline Wiring describe the new step and time (Who and what is affected).

## Design

**Where the steps live.** The routine prompt already says the runbook wins. So the
full procedure goes into `docs/nightly-sync.md` as a new section, *Email pickup
(step 0)*, and the prompt changes only in three places: the WHEN YOU RUN paragraph
(06:00, Ty emails the export by ~04:00), one line before STEP 1 ("do the runbook's
Email pickup first"), and the STEP 7 report's first line.

**Step 0, as the runbook will state it:**
1. Gmail `search_threads`: sender is the Webull no-reply address, subject
   `Webull_Orders_Records`, `in:inbox`. No date window: anything still in the
   inbox has not been picked up, because picked-up mail is trashed. Oldest first.
2. Per message: `get_message` → find the attachment named exactly
   `Webull_Orders_Records_Options.csv` (the email carries four: Records, IPO,
   Options, Bonds; only Options is used, as today). `download_gmail_attachment`
   saves it into the sandbox; take its sha256 and size.
3. List `Raw Records/` through the Drive connector. Name = the next free one in
   Finder's scheme: `Webull_Orders_Records_Options.csv`, then `… copy.csv`,
   `… copy 2.csv`, … (the highest existing number + 1; an empty folder after the
   monthly move starts at the bare name).
4. Drive `create_file`: `parentId` = Raw Records, that title,
   `contentMimeType` text/csv, **`disableConversionToGoogleType` true** (without it
   Drive turns the CSV into a Google Sheet and the sync can't read it), content as
   a `sha256:<hex>:<path>` file reference so the bytes never pass through the model.
5. `download_file_content` of the new file id; sha256 must equal step 2's.
6. Only then `trash_message` on that message.
7. Failure at any of 2–5 (no Options attachment, upload refused, hash differs):
   do not trash, do not delete what was created, carry on to the sync with whatever
   is in Raw Records, and mark the run.

**Heartbeat mark (for the brief, later).** `data/.last-check` today is
`<stamp> newest-source=<…>`; it gains one more status token:
` email=saved`, ` email=none`, or ` email=FAILED`. Status words only: no names, no
counts, per the runbook's public-heartbeat rule. Both readers take only the first
token (`freshness.py` `re.match(r"(\S+)")`, `verify_live.py` `.split()[0]`), so
neither changes. `email=none` is what the brief will turn into "No webull email
found".

**Routine config** (built from a same-turn `get`, per the live-config rule):
- `cron_expression` `0 4 * * 2-6` → `0 23 * * 1-5` (23:00 UTC Mon–Fri = 06:00
  Hanoi Tue–Sat).
- Add the Gmail connector to `mcp_connections`, `permitted_tools` limited to
  `search_threads`, `get_message`, `download_gmail_attachment`, `trash_message`.
  Nothing that sends, labels or permanently deletes.
- Prompt: the three edits above; everything else byte-identical.

**Files changed in this repo:** `docs/nightly-sync.md` (new section + heartbeat
format line + schedule line), `CLAUDE.md` one Known-mistakes line (a trashed
export is invisible to the connector), `verification/email-pickup.md` (new).
No code: `tools/` untouched except one docstring in `tools/bars-collect.py` (Amendment A).

**Outside this repo:** Pipeline Wiring (Trade Journal row time, section 7 dated
entry, the collector's cron table, mirror republished).

## Conflicts
Loaded: kernel standing-instructions, artifact mirror contract, repo `CLAUDE.md` +
runbook, entity separation, secure-pages. Not loaded: ty-report-standard,
apple-design (no page or report changes).

| Rule (by name) | What in the design touches it | Resolution |
|---|---|---|
| Runbook: heartbeat is "status only … no CSV names and no fill counts" | Adds an `email=` token | Status words only (`saved`/`none`/`FAILED`); runbook line updated in the same PR |
| Routine prompt: "NEVER delete anything in `Raw Records/`" | Step 0 writes into Raw Records | Only adds files; a bad upload is left in place and reported, never deleted |
| Repo `CLAUDE.md`: no personal data by value in this public repo | Runbook names the sender and subject | The sender is Webull's public no-reply address, not Ty's; Ty's address and message ids never written. `scan_public.py` must print 0 hits |
| Repo `CLAUDE.md`: "Never write a Cowork preview URL" | Prompt is edited | The preview URL stays only in the prompt, untouched; nothing added to the repo |
| Artifact mirror contract | Preview step | Unchanged; STEP 6 runs every run as today |
| Kernel "Why all of this exists" (no Mac dependency) | none added | Gmail + Drive connectors are cloud; the Mac drops out of Ty's nightly routine entirely |
| Routine Updates Use the Live Config (memory) | Prompt and cron edit | Update body built from a `get` in the same turn; no other field sent |
| Auto mode in an unattended run | `trash_message` may be judged destructive by the cloud classifier | **Likely risk (unverified).** The pre-ship test run proves it; if blocked, add a narrow `auto_mode_allow` rule for that one tool, or ask Ty |
| Monthly Drive backup job | Files appear in Raw Records at 06:00 | No change: it moves synced CSVs on the first Mac day of the month; a file saved and synced in the same run is synced |

## Security
secure-pages, 2026-11-28:

1 Secrets ........ PASS (tree 0, history 0, no JWTs)
2 Visibility ..... PUBLIC — PASS (fills are Ty's own, public on purpose per repo `CLAUDE.md`; this change adds no data)
3 Pages .......... PASS (Actions deploy of `.pages-allow` only; `data/.last-check`, docs and `work/` not served)
4 Supabase ....... N/A (not used)
Verdict: safe to ship

## Promise
`verification/email-pickup.md`, run twice:

**A. Pre-ship test (before the cron moves).** Ty emails one export and leaves it.
Fire the routine once (`run`). Pass when all hold:
- Raw Records has one new `… copy N.csv`, Drive type text/csv, sha256 equal to the attachment;
- that email is in Gmail trash, no other email touched;
- `data/.last-check` on `main` ends `email=saved`; `sync.js --check` on the pushed tree prints `"changedFiles": []`;
- the report's line 1 names the file and the trashed email.
Then fire it a second time with nothing in the inbox: no file created, nothing trashed, `email=none`, report says "No webull email found".

**B. First real morning:** Tue 1 Dec 2026, 06:00 Hanoi (Mon 30 Nov 23:00 UTC), if
shipped before then: `get` the routine shows `last_fired_at` that morning, A's
first four checks hold for Monday night's export, and the new fills are on `main`.

## Out of scope
- The 07:00 iMessage brief line: separate intent in the other repo; it reads the `email=` token defined here.
- The Webull API route (Option C): tested 28 Nov, 74 of 81 fills, not used.
- The IPO, Records and Bonds attachments.
- Any change to `tools/sync.js`, the parser, the page, or the monthly backup job.
- Unread, labelled or archived Webull mail outside the inbox.

## Amendment A (2026-11-28, after review of PR #25)
Review finding: at 06:00 the wiki step runs before the Mac writes that session's bars (10:30 Hanoi), and raw days
are written once, so every session would freeze with "bars missing". Ty chose **option B**: the wiki waits one run
for its bars. `docs/wiki.md` "Which day" defers `<day>` while its bars file is absent; the next run writes it with
`--final` (the existing path). Each session's wiki page lands one run after its fills (Friday's on Tuesday; the
Saturday weekly report names Friday as deferred, and Tuesday's run updates it, as today). The Mac job stays at 10:30.
Files added to this change: `docs/wiki.md`, `docs/backup.md`, `README.md` (schedule wording), the
`tools/bars-collect.py` docstring (one word). Requirement 5 now reads: sync, dedup, publish and preview unchanged;
the wiki step changes only in when `<day>` is written.
**Approved:** 2026-11-28 (Ty, in chat: "Go with option B").

## Amendment B (2026-11-28, after the second review) · **Status:** draft, needs Ty's approval
Adds to step 0, beyond the original design:
1. **Already saved?** Before uploading, if a file in `Raw Records/` has the attachment's exact size, compare sha256;
   on a match save nothing and go to the trash step. Stops a failed trash from creating a new `copy N` every morning.
2. **Rename, never read, a bad upload.** A file this run uploaded whose read-back hash differs is renamed with Drive
   `update_file` to `FAILED <name>.bad`, so no sync ever reads it (a truncated last row would otherwise become a
   permanent wrong fill). Nothing is deleted; the email stays in the inbox; the run marks `email=FAILED`. This
   replaces "a bad upload is left in place" in the Conflicts table and Design step 7.
3. **Routine config:** the Drive connector must permit `create_file`, `download_file_content` and `update_file`.
4. **Naming rule made exact:** the bare name counts as 0, `copy.csv` as 1, `copy N.csv` as N; the next file is
   max + 1, where 1 is written `copy.csv`.
Trade-off: if the read-back hash differed every run for a repeating reason, those fills would wait until Ty or a
session looks; the daily `email=FAILED` mark (and the brief line built on it) is the alarm.
