# Holiday calendar for the whole journal, a staleness warning, and a current preview build (24 Oct 2026)

Status: **APPROVED** — Ty typed "approve", 24 Oct 2026, after seeing the recount (overnight 0–1 DTE: 126 → 128, 2 trades).
Source: Ty's follow-ups to PR #22 (by paste, then typed; see intent.md). Ships on his phrase.

## 1. Holiday list (`MKT_HOLIDAYS` in index.html)
Every NYSE full-day closure from the journal's first trade (2020-12-18) through 2027: 70 dates. Checked against the
official sources, not memory:
- 2020–2021: [NYSE Group 2020, 2021 and 2022 calendar](https://ir.theice.com/press/news-details/2019/NYSE-Group-Announces-2020-2021-and-2022-Holiday-and-Early-Closings-Calendar/default.aspx)
- 2022: [NYSE Group 2022, 2023 and 2024 calendar](https://ir.theice.com/press/news-details/2021/NYSE-Group-Announces-2022-2023-and-2024-Holiday-and-Early-Closings-Calendar/default.aspx) (New Year 2022 on a Saturday: no closure, NYSE Rule 7.2; Juneteenth observed Mon 20 Jun)
- 2023–2024: [NYSE Group 2023, 2024 and 2025 calendar](https://ir.theice.com/press/news-details/2022/NYSE-Group-Announces-2023-2024-and-2025-Holiday-and-Early-Closings-Calendar/default.aspx)
- 2025–2027: [nyse.com Holidays & Trading Hours](https://www.nyse.com/markets/hours-calendars), read 24 Oct 2026
- 2025-01-09, unscheduled: [NYSE to close on 9 Jan 2025, National Day of Mourning for President Carter](https://ir.theice.com/press/news-details/2024/The-New-York-Stock-Exchange-Will-Close-Markets-on-January-9-to-Honor-the-Passing-of-Former-President-Jimmy-Carter-on-National-Day-of-Mourning/default.aspx)
Early closes (1:00 pm) are not closures and are not in the list. Juneteenth first closed markets in 2022.

**Effect on "overnight 0–1 DTE", all history (3,808 closed option trades):** 126 → 128 flagged; 2 trades changed, both
now flagged: GME 2021-11-26 250C (bought Wed 24 Nov 2021, Thanksgiving closed) and SPY 2026-09-08 770C (bought Fri 4 Sep
2026, Labor Day closed).

## 2. Staleness warning
`holidayStale(trades)`: true when a trade whose expiry is within 7 calendar days of its entry has its entry date or
expiry in a year after the last year in the list (`HOL_LAST_YEAR`, 2027 today). Long-dated options and stock can't be
miscounted as 0–1 DTE, so they never raise it (Ty, typed, 24 Oct). Then the Rules card shows, in the page's critical red: "Holiday calendar ends <year>,
update it: the overnight 0–1 DTE check may miscount." The protocol checks it (rules-check.md invariants).
(Review #23, finding 3, raised the LEAP case; Ty narrowed the rule to the 7-day window.)

## 3. build/artifact.html
The repo keeps the preview fragment committed and rebuilds it whenever index.html changes (CLAUDE.md; earlier specs
do it in the ship turn). It had fallen behind index.html (PR #22 and earlier). Regenerated from this index.html, and the
protocol now fails if the committed fragment differs from `tools/build-fragment.py`'s output.

## Check (24 Oct, local server, this branch): verification/rules-check.md run as committed
Steps 1–2 over all history (2020-12-01 → 2026-10-24, R = 100): page = recount on all **ten** Rules rows (8 rules, No rule
broken 496 / +65,159, Over-cap days 1,324 / −809,281); over-cap line 243 days = recount; trade log "3312 of 4111" = recount
filtered 3,312; add-down badge sample 1; fixtures at97 true, above97 false, holidayOvernight true (page and recount);
holiday: stale false, no warning, last year 2027, 70 dates equal to the recount's own list; fixtures next-year short-dated true, LEAP false, no-expiry false (rerun after the 7-day narrowing, 24 Oct).
Step 3 `"changedFiles": []`. Step 4 `0 False`. Step 6 `BUILD_MATCH`. Also 19–23 Oct: all rows equal (earlier run).
Review fix found here: the page fixture's fills had no time, which the add-down-before-10:00 check reads; fills now carry it.
