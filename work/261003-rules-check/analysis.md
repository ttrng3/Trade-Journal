# Analysis behind the intent (2026-10-03)

The figures in `intent.md` come from this script, run in chat on 2026-10-03 over `data/` as of snapshot 2026-10-02 17:56 UTC.

**Method:**
- Trades are built with `tools/parse-webull.js` `buildTrades`, with fees at $0 and long-only on.
- It covers closed long option trades. A trade still open after its expiry counts as worthless; 3 trades in the window did.
- Unknown-cost lots are skipped.
- Days are grouped by entry date.
- An add-down is a BUY more than 3% below the first fill (strict `<`).

The page's rules differ from this method on purpose (spec, "Two differences"), so its numbers won't match this file exactly.

Run from the repo root: `node work/261003-rules-check/analysis.js`

Output, 2024-12-10 to 2026-10-02:
- 532 trades, net −$3,296, win rate 61.5%, payoff 0.55, profit factor 0.88.
- Add-down trades: 323, net −$6,519, profit factor 0.74. Other trades: 209, net +$3,223, profit factor 2.19.
- Entries 14:00–15:00 ET: 55 trades, profit factor 0.36, net −$3,084.
- SPXW: 90 trades, profit factor 0.41, net −$3,885.
- Holds under 2 minutes: profit factor 8.13. Holds of 2–10 minutes: profit factor 1.54. Every longer bucket was below 1.
- Days: worst −$1,055, deepest drawdown −$5,122.
