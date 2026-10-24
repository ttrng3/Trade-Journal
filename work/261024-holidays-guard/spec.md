# Holiday calendar for the whole journal, a staleness warning, and a current preview build (24 Oct 2026)

Status: built and verified on `work/261024-holidays-guard`; ships on Ty's phrase after he sees the recount. Source: Ty's
follow-ups to PR #22 (by paste, 24 Oct).

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
`holidayStale(trades)`: true when any trade's entry date or expiry falls in a year after the last year in the list
(`HOL_LAST_YEAR`, 2027 today). Then the Rules card shows, in the page's critical red: "Holiday calendar ends <year>,
update it: the overnight 0–1 DTE check may miscount." The protocol checks it (rules-check.md invariants).

## 3. build/artifact.html
The repo keeps the preview fragment committed and rebuilds it whenever index.html changes (CLAUDE.md; earlier specs
do it in the ship turn). It had fallen behind index.html (PR #22 and earlier). Regenerated from this index.html, and the
protocol now fails if the committed fragment differs from `tools/build-fragment.py`'s output.

## Check (24 Oct, local server, this branch)
Protocol recount (as committed) = page Rules card on all nine rows for all history (2020-12-01 → 2026-12-31) and for
2026-10-19 → 23. Page: `holidayStale` false, no warning shown, `HOL_LAST_YEAR` 2027, 70 dates, fixture for 2028 true,
trading days 2021-11-24→26 = 1 and 2026-09-04→08 = 1. `cmp` fragment vs build/artifact.html: equal. `sync.js --check`:
`"changedFiles": []`.
