# Personal rules on the rules check (24 Oct 2026)

Status: built on branch `work/261024-personal-rules`, verified, **not merged**. Source: Ty's rulings on the 5A review of
19–23 Oct, relayed by paste (orb-options ledger R132). Merge waits for his own words.

## What changes (index.html, `RULES` and `ruleFlags` only)
| Flag | Rule (Ty) | How the page checks it |
|---|---|---|
| `earlyadd` "add-down before 10:00" | replaces "early 0DTE": flag adding to a losing position, or entering with no stop, before 10:00 | the add-down rule (a later buy ≥ 3% below the first) on a trade entered before 10:00 ET. The "no stop" half is **not built**: see Not built |
| `spxpm` "SPX after 12:00" | no SPX entries after 12:00 (two-week trial, then a P&L-by-time review) | underlying SPXW, entry at or after 12:00 ET. The older all-day "SPXW" flag (3 Oct) stays; Chose keep because the new rule narrows nothing Ty asked to remove |
| `overnight` "overnight 0–1 DTE" | no overnight holds on 0–1 DTE | exit on a later date than entry, and expiry at most 1 business day after the entry date |
| `giveback` "after 30% giveback" | once up $300 on the day, stop after giving back 30% of the peak | per exit day, realized net in exit order; the first exit where the peak is ≥ $300 and net ≤ 70% of peak sets the stop time; every option trade entered that day after it is flagged |

Unchanged: add-down, late 0DTE, long hold, SPXW, the −3R cap. `data/` is not touched.

## Not built (needs data the journal does not keep)
- **Hard stop at the day's low on an opening dip-buy**, and the **"entering with no stop"** half of the narrowed early flag.
  The journal stores filled orders only. Stop orders that never trigger are dropped at import. In the Webull export they
  appear as sell orders whose Price has no "@" (51 cancelled, 1 failed, 1 working since 5 Oct; none filled). Assumption,
  to be confirmed by Ty: a bare price means a stop order. Checking "at the day's low" also needs the underlying's prices,
  which the page does not have. Next step if wanted: keep unfilled stop orders at import (a data-format change, own spec).

## Check
Independent recount (`verification/rules-check.md`, recount extended) vs the page's Rules card, custom range
2026-10-19 → 2026-10-23, run 24 Oct on the branch: add-down 44 / +304, add-down before 10:00 10 / +1,101,
SPX after 12:00 10 / −1,115, overnight 0–1 DTE 1 / −566, after 30% giveback 31 / −898: page equal to recount on every
row. `sync.js --check` with no CSVs: `"changedFiles": []`.
