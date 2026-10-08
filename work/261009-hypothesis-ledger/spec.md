# Spec: hypothesis-ledger

**Approved:** 2026-10-09 (Ty, same message as the intent; docs-only change)
**Intent:** accepted 2026-10-09 · **Status:** approved

## Requirements
1. `wiki/hypothesis-ledger.md` with the intent's eleven columns plus `bundle name` (the bot's `setup` value in the bundle, so the compiler can tell a known setup from a new one), in three tables: bots and setups, agents, Friday tunes (empty, header only).
2. Seed rows H01–H15 (Phase A ORB, 5-min ORB retest, VWAP/EMA, sweep V0–V6, Bot #1, Bot #2, Chandelier, Trend+Timing, gap, QQQ→TSLA lead, Bot #1 on other symbols, sweep reclaim, volume rule, the TradingView setup study, Bot #3 on Champ's rules) and A01 structure, A02 Flow agent. Every number is copied from the orb-options study records as of 2026-10-08; nothing is recomputed.
3. `wiki/index.md` links it; `docs/wiki.md` step 3 says when the compiler adds a row.

## Promise
`python3 tools/wiki-check.py` prints `WIKI OK … dangling=0 uncited=0`, and a privacy scan of the new page finds no `Ty` beside `$`, no order or account ids, no work-entity names.

## Out of scope
The cost-stress column (its own PR), any change to the compile beyond the one runbook line, Friday tune rows (added by each tune).
