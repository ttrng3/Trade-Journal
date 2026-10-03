# Intent: the journal page flags trades and days that break the 0DTE rules

**Status:** accepted 2026-10-03
**Source:** chat, 2026-10-03

**Problem.** The page shows what happened but not whether a trade broke the rules Ty set on 2026-10-03. An analysis in chat on 2026-10-03 (not filed; the figures below are Likely, and the Rules card this change adds recomputes them from `data/`) of the 532 closed long option trades from 2024-12-10 to 2026-10-02 found the losses come from a few repeatable habits. Today nothing on the page points at them:
- adding contracts below the first entry price: 61% of trades; those trades netted −$6,519;
- entries from 14:00 to 15:00 ET: profit factor 0.36, −$3,084;
- SPXW: profit factor 0.41, −$3,885;
- holds over 10 minutes: every bucket above 10 minutes lost money;
- days with no loss cap: the worst day was −$1,055 and the deepest drawdown −$5,122.

**Outcome.** Every closed trade on the page carries a flag for each rule it broke, and every day carries a flag if its net loss went past the daily cap. The rules:
1. **Add-down:** a BUY fill below the trade's first entry price.
2. **Late 0DTE:** a 0DTE entry from 14:00 to 15:00 ET.
3. **Early 0DTE:** a 0DTE entry before 10:00 ET.
4. **Long hold:** held more than 10 minutes.
5. **SPXW:** the underlying is SPXW.
6. **Over cap:** a day's net below −3R.

The page also shows, for any date range, how many trades broke each rule and what those trades netted, next to the trades that broke none. A check: on the 532-trade window the counts match the 03/10 analysis (for example, 323 add-down trades).

**Who and what is affected.**
- Repo `ttrng3/Trade-Journal`: `index.html` (the journal engine), possibly the settings section.
- The Pages site and the Cowork preview.
- The nightly sync routine and `tools/sync.js` should be untouched, because the check reads fills and doesn't write `data/`.

**Constraints.**
- `data/` serialization is unchanged. `sync.js --check` with no new fills still prints `"changedFiles": []` (CLAUDE.md, Rules).
- No new file kinds under `data/` without their own PR (CLAUDE.md, `.pages-allow`).
- Light theme only; any new colour is a token (README, "Look").
- Public repo: no account size, R value or other personal figure is written into the repo by value. If R is stored, it lives in the per-browser overlay (`meta`), not in the snapshot.
- Personal entity only; nothing from any work entity.
- Changes reach `main` through a PR and Ty's ship.

**Open questions.**
- What is R in dollars, or should the page ask for it (stored only in this browser)?
- Should the add-down rule fire on any lower add, or only 3% or more below the first fill (the threshold the analysis used)?
- Should "Long hold" apply to all trades, or only 0DTE?
- Should rule 5 flag SPXW as a broken rule or only as a warning until the SPY/QQQ gate is met?
- Should flags be view-only, or also filterable (for example, "show only rule-breaking trades")?
