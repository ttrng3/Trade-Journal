# Spec: ledger-session-trials

**Approved:** 2026-10-11 (Ty released PR 20 at 00:15 Hanoi, merged as b1c849b, and at 00:30 Hanoi asked for this status to read approved)
**Intent:** accepted 2026-10-10 · **Status:** approved

## Requirements
1. Rows S001–S012 at the end of the bots and setups table of `wiki/hypothesis-ledger.md`, in the page's 12 columns, status `failed`. Source: orb-options `research/session_bt/ledger_rows_S001-S012.csv`, branch `pkg/session-v1` @ba529e3. The backtest was rerun on 2026-10-11 from the committed scripts and gave the same trade counts, means and t values for all 12.
2. H15 and H06 each get a dated line in `result` and "+2 (S0nn, S0nn, 2026-10-10)" in `variations`. No other existing row changes.
3. One sentence in the page header defines `S` rows. The S source line names the branch and commit. The closing source line is scoped to the H and A rows.
4. S012's lesson says the QQQ-only result is "proposed as trial S013 (shadow only), not yet ruled", because no ruling has registered S013. This is the only place the copied text is changed.

## Promise
`python3 tools/wiki-check.py` prints `WIKI OK pages=14 dangling=0 uncited=0`; the diff touches `wiki/hypothesis-ledger.md` and this folder only; the live file at `ttrng3.github.io/Trade-Journal/wiki/hypothesis-ledger.md` holds 12 rows whose id starts `S0` after the merge.

## Out of scope
Rewriting the per-row lessons; an S013 row (added when it is ruled); the minus-sign and range formatting of the copied cells; any change to the compile runbook.
