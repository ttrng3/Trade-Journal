# Intent: the morning sync picks up the Webull export from email, so Ty no longer downloads, drags or deletes it

**Status:** accepted 2026-11-28
**Source:** chat, 2026-11-28

**Problem.** Each trading night (Mon–Fri) Ty asks Webull to email the day's order
records, then by hand downloads the email's options CSV, drags it into
`Raw Records/` on Drive, and deletes the email. The sync routine only sees what he
has dragged in, so a late or forgotten drag means a missed run (25/09, 26/09: CSV
landed after the run fired). Evidence the email route works: on 2026-11-28 the
Gmail connector found the fresh export email in the inbox and its
`Webull_Orders_Records_Options.csv` attachment was byte-identical (sha256) to the
`copy 6.csv` Ty had dragged in that morning. Trashed exports are invisible to the
connector, so the email must still be in the inbox when the routine runs.

**Outcome.** Each run of the Trade Journal routine, before the sync:
1. Finds every Webull order-records email in the inbox that arrived since the last
   run (sender and subject named in the runbook).
2. From each, saves only the `Webull_Orders_Records_Options.csv` attachment into
   `Raw Records/` as the next free `Webull_Orders_Records_Options copy N.csv`.
3. Reads the saved file back from Drive; only if it is there and the same size as
   the attachment, moves that email to Gmail trash. If the save fails, the email
   stays in the inbox and the run reports it.
4. Then runs the sync and publishes exactly as today.

The routine fires at **06:00 Hanoi, Tue–Sat** (was 11:00), so the 07:00 iMessage
brief can report on it. Ty's only step left is sending the export to email.
Checked by: first automatic morning after the switch, the CSV is in `Raw Records/`,
the email is in trash, the new fills are in `data/` and on Pages; a morning with no
email saves nothing and trashes nothing; its data commit carries only `data/.last-check`.

**Who and what is affected.** The Trade Journal routine (prompt,
schedule, Gmail connector added); `docs/nightly-sync.md` (runbook); Pipeline Wiring
page (Trade Journal row + section 7 entry); Ty's Gmail inbox (export emails trashed
after pickup).

**Constraints.**
- Sync, dedup and parsing unchanged: `tools/sync.js` untouched; content dedup means
  a re-saved duplicate is harmless.
- Monthly Mac backup job unchanged; it still moves the month's CSVs on the 1st.
- Trash only, never permanent delete; only emails from the Webull export sender with
  the export subject; never touch any other email.
- Ty can still drag a CSV in by hand; nothing breaks if he does.
- Public repo: no email address, message id or account id written in the repo.
- The morning brief's journal line is a separate change in another repo (its own intent and
  ship steps), not part of this one.

**Open questions.** none open. Answered by Ty 2026-11-28:
- Latest send of the export is around 04:00 Hanoi, so 06:00 leaves two hours.
- On a trading day with no export email, the run's report (and later the brief line)
  says "No webull email found".
