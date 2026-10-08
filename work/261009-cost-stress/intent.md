# Intent: a cost-stress column in the Saturday report

**Status:** draft (Ty agreed 2026-10-09 that this is a build with its own PR; waiting for "accept")
**Source:** chat, 2026-10-09 (Cowork's Task 4)

**Problem.** Bot #1 died on spread: +2.2% a trade in its study, −1.8% after spread on the hold-out. The weekly report shows the bots' fills as they came, so the same failure would show late.

**Outcome.** The Saturday weekly report gets one column for the bots' trades of the week: realised result recomputed (a) at 2× the spread actually paid at entry and exit, and (b) with entry and exit filled one 1-minute bar late. Shown in R and in %. The report states beside it: "read-only, no setting changes may cite this column."

**Who and what is affected.** `tools/postexit.py` or a new small tool that writes the stressed figures into `raw/<day>.json`; the weekly template in `docs/wiki.md`; `wiki-check.py --weekly`. Bot trades only, not Ty's manual trades.

**Constraints.** Read-only: no setting, gate or tune may use it (6 Oct rule). Not a backtest: only the week's real fills are re-priced. Public repo: no ids, no $ beside Ty. The routine runs in the cloud with no IBKR.

**Open questions.**
1. "One bar late" needs each option's 1-minute bar after the fill. v8 logs the spread at entry and exit, so (a) needs no new data. For (b): read Alpaca option bars from the cloud (free key, history starts 2024-01-18), or have the Mac collector add the next bar to the bundle at 10:30 from IBKR? Recommendation: the Mac collector, since it already reads the bots' data and the routine stays free of a new key.
2. Whether this column feeds a 3c end rule is Ty's open decision (the profit-floor question); this intent only builds the column.
