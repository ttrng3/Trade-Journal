# Intent: a cost-stress column in the Saturday report

**Status:** accepted 2026-10-09 (Ty: "Cost-stress plan: accept, with one change. No bot change and no Mac collector.")
**Source:** chat, 2026-10-09 (Cowork's Task 4)

**Problem.** Bot #1 died on spread: +2.2% a trade in its study, −1.8% after spread on the hold-out. The weekly report shows the bots' fills as they came, so the same failure would show late.

**Outcome.** The Saturday weekly report gets one column for the bots' trades of the week: realised result recomputed (a) at 2× the spread actually paid at entry and exit, and (b) with entry and exit filled one 1-minute bar late. Shown in R and in %. The report states beside it: "read-only, no setting changes may cite this column."

**Who and what is affected.** A step in the cloud routine (no bot change, no Mac collector change) that joins each bot fill's timestamp to the next 1-minute bar and writes the stressed figures into the weekly report; the weekly template in `docs/wiki.md`; `wiki-check.py --weekly`. Bot trades only, not Ty's manual trades.

**Constraints.** Read-only: no setting, gate or tune may use it (6 Oct rule). Not a backtest: only the week's real fills are re-priced. Public repo: no ids, no $ beside Ty. The routine runs in the cloud with no IBKR.

**Where it is used (Ty, 2026-10-09).** Reported weekly in the Coach row as cost-stressed expectancy with its interval. A Coach FLAG (not a stop) fires if the sample mean sits below −2 standard errors, checked twice only: at trade 15 and at trade 20. It never gates 3c; 3c passes on behaviour against the frozen prediction.md, and the only hard stop is paper P&L at or below −$1,500.

**Check done 2026-10-09: the bars log holds the underlying only.** The bot's `bar` rows carry the stock bar, levels and votes; option prices exist only at the moment of an order (`entry_start` / `exit_start` bid and ask, and the fill price). `raw/<day>.json` likewise carries stock candles after each trade. So "one bar late" needs option prices from outside the bot's logs.

**Interim (9 Oct):** until a source for the late-bar option price exists, the column = the week at 2× the logged entry spread; the one-bar-late part reads "pending".

**Price source (Ty, 2026-10-09, his later message stands; supersedes "no bot change"):** after 3d passes, the bot logs, log only, the option bid/ask one bar after each fill and at exit (orb-options intent `work/261009-post3d-logging`). The routine reads those fields from the bundle. No Alpaca. Mac-bound while the bot runs on the Mac.

**Open questions.** none known
