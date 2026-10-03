# Spec: rules-check

**Approved:** 2026-10-03

**Intent:** accepted 2026-10-03 · **Status:** approved

Ty's answers, 2026-10-03, in chat:
- R is entered on the page and stored only where the page keeps its settings, never in the repo.
- An add-down is a BUY fill at least 3% below the first fill.
- The 10-minute hold rule covers 0DTE trades only.
- SPXW counts as a broken rule.
- One filter: "rule breaks only".

## Requirements

1. Every closed option trade (net known, so not OPEN or UNKNOWN) is checked against five trade rules (intent, Outcome 1–5):
   - **add-down:** a BUY fill after the first, at a price ≤ 97% of the first BUY's price;
   - **early 0DTE:** expiry date equals entry date, and the entry time is before 10:00 ET;
   - **late 0DTE:** expiry date equals entry date, and the entry time is from 14:00 to before 15:00 ET;
   - **long hold:** 0DTE, and held more than 600 seconds;
   - **SPXW:** the underlying is `SPXW`.
2. Every day is checked against the cap: its closed-trade net is below −3 × R (intent, Outcome 6). A day is the page's own day, `t.date` (the exit date). With no R set, the cap is not checked and the page says so.
3. In the trade log, each rule a trade breaks shows as a badge in the Result cell. Every trade on an over-cap day also shows an "over cap" badge (intent, Outcome).
4. The trade log gets one toggle, "Rule breaks only", which keeps trades breaking at least one rule, the cap included (Ty's answer 5).
5. Reports gets one card, "Rules", for the current date range. It shows:
   - one row per rule: trades that broke it, their net, win rate and profit factor, using the page's existing `stats()`;
   - a "No rule broken" row;
   - an "Over-cap days" row: number of days and their net, or "Set R in Settings" (intent, Outcome).
6. Settings, Calculation card: one field, "R: dollars risked per trade". It's saved with the existing Save button into `S.meta.R` through `store.saveMeta`, the same path as the fee fields (Ty's answer 1).

## Design

**One file changes: `index.html`.**
- One new function, `ruleFlags(t)`, returns the trade rules broken.
- One new function, `overCapDays(trades)`, returns the set of over-cap dates for the trades given.
- `rebuild()` sets `t.rules` on each trade after `buildTrades`.
- `rowHtml` adds badges, using the existing `badge` classes: `r` for the five rules and the cap.
- `renderTrades` adds the toggle next to the existing filters. Its state is `S.filters.rules`, which, like the other filters, isn't saved.
- `renderReports` adds the Rules card through the existing `statTable`.
- `renderSettings` adds the R field.
- No new colour, font, file under `data/`, or change to `tools/`.

**Where R lives:**
- On Pages: `store.saveMeta` writes to this browser's `localStorage`. That's the overlay; the nightly sync never reads or writes it.
- In the Cowork preview: the same call writes the preview's private artifact database, which is never the repo.
- Neither place is the repo, so R is never published.

**New file `verification/rules-check.md`** (Stage 4): the protocol below. It isn't served, because `.pages-allow` lists only `index.html` and `data/`.

**Mock:** none. The change reuses the page's existing badge, button, card and table components, so the screenshot in the Promise is the design check.

## Conflicts

Policy loaded:
- kernel "Standing Instructions" and root `CLAUDE.md`, read this session;
- memory "artifact-mirror-contract" and "trade-journal-pipeline";
- the apple-design skill;
- the repo `CLAUDE.md`;
- the secure-pages skill, run this session.

| Rule (by name) | What in the design touches it | Resolution |
|---|---|---|
| "Visual standard for artifacts and HTML deliverables — Apple design, one theme per page" (standing-instructions) | `index.html` was deliberately left on its own styling (memory, trade-journal-pipeline). | Keep its theme and components and add no new colour, as the rule says for edits. Every flag is a word badge, never colour alone. |
| "Public on purpose … do not widen what is served" and "Never write … personal data by value" (repo CLAUDE.md) | R is a personal figure. | R is stored only in `localStorage` (Pages) or the preview's private database. It's never in `data/`, a commit, the spec or the protocol. Promise check 4 greps for it. |
| "Serialization is fixed" and "`--check` … must print `"changedFiles": []`" (repo CLAUDE.md) | None: the change only reads fills. | Promise check 3 runs it. |
| "Changes reach `main` through a PR and Ty's ship" (repo CLAUDE.md) | — | Branch `work/rules-check`, PR, reviewer, then Ty ships. |
| artifact-mirror-contract: "any merge that touches a renderer → rebuild + publish the preview in the ship turn" | `index.html` changes. | In the ship turn: run `tools/build-fragment.py`, publish `build/artifact.html` to the preview (the page alone, then read it back: one `<html>`). Its URL is never shown. |
| trade-journal-pipeline: "the wiring page is part of the change" (page behaviour) | Page behaviour changes. | Ty, 2026-10-03: add the entry. A dated section-7 entry in `ttrng3/pipeline-wiring`, in its own PR, at ship time, and its mirror republished. |
| Entity separation | — | None: the rules and data are personal. |
| "Simplicity first" (`~/.claude/CLAUDE.md`) | — | One page file and one protocol. No settings beyond R, and no filters beyond the one toggle. |

**Two differences from the 03/10 analysis (by design, not conflicts):**
- The page counts only closed trades. The analysis also counted 3 trades held to expiry as worthless, and the page keeps those as OPEN.
- The page groups days by exit date; the analysis used entry date.

So the page's counts won't equal the analysis figures exactly. The Promise compares the page against an independent recount that uses the same definitions, not against 323.

## Security (secure-pages, 2026-10-03)
```
1 Secrets ........ PASS | history: 0 hits
2 Visibility ..... PUBLIC — PASS (fills are public on purpose, per repo CLAUDE.md; no notes in the snapshot)
3 Pages .......... PASS — Actions deploy from main, allowlist: index.html, data/index.json, data/fills/*.json
4 Supabase ....... N/A — not used (the only mention is REVIEW.md text)
Verdict: safe to ship
```
This change adds nothing served except `index.html` itself.

## Promise

Run on the Mac on the branch (served locally), then again on Pages after the merge:

1. **Counts match.** A Playwright script opens the page in a fresh browser profile and sets R = 100 through the Settings field. It sets a custom range of 2024-12-10 to 2026-10-02 and reads the Rules card. Separately, a Node recount loads `data/` with `tools/parse-webull.js` `buildTrades`, applies the definitions in Requirements 1–2 and prints the same numbers.
   **Pass:** for every rule row, "No rule broken" and "Over-cap days", the count and net are equal.
2. **Badges and filter.** With "Rule breaks only" on, the trade log count equals the trades breaking at least one rule in the recount. One add-down trade from 2026-09-09 shows the add-down badge.
   **Pass:** both true.
3. **Data untouched.** `node tools/sync.js --csv-dir <empty> --check`.
   **Pass:** `"changedFiles": []`.
4. **R never published.** `git grep -n "\"R\"\s*:"` and a search of `data/` for the R key.
   **Pass:** 0 hits. The live page after the merge shows "Set R in Settings" in a fresh profile.
5. **Existing protocol.** `verification/journal.md` step 1.
   **Pass:** `"pass": true`.
6. **Evidence:** the JSON from steps 1–2, one screenshot of the Rules card and one of the filtered trade log.

**Measured:** on the branch before the PR, and on Pages the same day as the merge.

## Out of scope

- No new rule beyond the six.
- No alerts or notifications.
- No change to how trades are built, to fees or to the nightly sync.
- No per-browser rule settings beyond R.
- No changes to the dashboard or journal views.
- No backtest of the rules.
