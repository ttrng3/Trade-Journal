# Intent: holiday calendar for the whole journal, a staleness warning, a current preview build

Status: **relayed by paste, 24 Oct 2026 — not yet accepted in Ty's own words.**

1. **What:** (1) every NYSE full closure over the journal's whole date range in the "overnight 0–1 DTE" count, checked against the official NYSE calendar and cited; (2) a visible warning on the Rules card when a trade or expiry falls after the list's last year; (3) no stale `build/artifact.html`.
2. **Why:** PR #22 listed holidays only from 2026-11-26, so older trades could miscount; a list that silently runs out miscounts later; nothing in a public repo should be out of date.
3. **Ty's words (paste):** "Add every NYSE full closure covering the journal's full date range ... Then rerun the 'overnight 0–1 DTE' recount on all history and tell me how many trades changed." "If any trade date or expiry falls after the last year in the holiday list, show a visible warning on the Rules card ('holiday calendar ends <year>, update it') instead of silently miscounting. Add the same check to the verification protocol." "Stale build/artifact.html: fold it into this same PR. Either regenerate it from the live page or delete it, whichever matches how the repo is meant to work." "Check the holiday list against the official NYSE calendar (nyse.com holidays page), not from memory, and cite it."
4. **Done looks like:** verification/rules-check.md run as written passes, over all history.
5. **Out:** early closes (not closures); stop orders (PR #22, Not built).
