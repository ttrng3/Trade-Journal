# 0DTE scalp

Manual trading buys same-day-expiry calls and puts on SPY, SPXW and TSLA and closes them within the session, often
re-entering the same strike several times. Expiry day leaves no room for a position to come back, so the result is
decided by entry timing and by how many times a losing strike is re-entered.

## Evidence
- 2026-10-21: one same-day strike, green, **+$67.00** on two contracts of SPY 769C, bought and sold inside 21
  minutes. The smallest session compiled, and the fifth green one in a row. (Verified: raw/2026-10-21.json)
- 2026-10-21: size and result moved together again, in the other direction — the smallest position of the five
  green sessions produced the smallest gain, while the same strike held to settlement was worth **+$529.00**.
  See [[what-ifs/exit-before-the-close]]. (Verified: raw/2026-10-21.json)
- 2026-10-20: two same-day strikes, **both green**, **+$462.00** — the best 0DTE session compiled. SPY 768C took 19
  contracts for +$411.00 and SPY 766C two for +$51.00. (Verified: raw/2026-10-20.json)
- 2026-10-19: one same-day strike, green, **+$188.00** on 16 contracts of SPY 767C, round-tripped in six clusters
  across the session. (Verified: raw/2026-10-19.json)
- **2026-10-19 and 2026-10-20 break the size correlation.** The most re-entered strike of each session — 16 buy
  fills, then 19 — was the session's biggest winner. With 2026-10-16 that is three consecutive counterexamples to
  the 2026-10-07 and 2026-10-08 pattern where the most re-entered strikes lost. Across all compiled days the three
  heaviest 0DTE strikes are now 19, 16 and 7 contracts, and the first two are the two largest wins.
  (Verified: computed over raw/2026-10-07…raw/2026-10-20)
- 2026-10-16: two same-day strikes, **both green**, the first clean 0DTE day compiled. QQQ 720P round-tripped
  5-for-5 at **+$127.00**; TSLA 377.5C took **$378.00** of buys and **$524.00** of sells but closed a contract
  carried in from earlier in the week, so it is **+$146.00** of net cash rather than a round trip. Net cash across
  the two strikes was **+$273.00**. (Verified: raw/2026-10-16.json)
- 2026-10-16: re-entry did not pick the loser this time. Six buy fills on TSLA and five on QQQ, and both strikes
  ended green — the opposite of 2026-10-07 and 2026-10-08, where the most re-entered strikes were the ones that
  lost. The size-is-the-tell correlation now has a counterexample.
  (Verified: computed over raw/2026-10-07…raw/2026-10-16)
- 2026-10-16: the day's realized result is not the interesting number. The QQQ put settled **$10.14** in the money
  after being sold at 1.18–1.94, so the same five contracts held to expiry were worth **$5,070.00** against the
  **$766.00** taken. See [[what-ifs/exit-before-the-close]]. (Verified: raw/2026-10-16.json)
- 2026-10-12 to 2026-10-15: no same-day-expiry trade is recorded on any of the four days. Those raw days were
  frozen before Ty's export arrived, so the fills the shard now holds for them are not in `raw/` and cannot be
  compiled. (Verified: computed over raw/2026-10-12…raw/2026-10-15; data/fills/2026-10.json)
- 2026-10-09: three same-day contracts round-tripped for **+$21.00** — SPY 776C +$94.00, TSLA 387.5C +$25.00, QQQ 750P
  -$98.00 — and trading stopped at 11:20:03, before midday. The session's real gain was a later-expiry position, not
  these. (Verified: raw/2026-10-09.json)
- 2026-10-08: four same-day contracts round-tripped for **+$118.00**, three of them winners, the first positive 0DTE
  day compiled. Size was small: 1, 1, 5 and 2 contracts against the 3-to-7 of 2026-10-07.
  (Verified: raw/2026-10-08.json)
- 2026-10-07 to 2026-10-09: across the three compiled days, 13 same-day-expiry contracts round-tripped inside the week
  for **-$615.00** with 5 winners. The one eight-day contract traded in the same period returned +$753.00, so the
  same-day book is where the week's losses sit. (Verified: computed over raw/2026-10-07…2026-10-09)
  See [[setups/later-expiry-swing]].
- 2026-10-08: re-entry stayed heavy on the losers and light on the winners. TSLA 10-09 380C took 7 buy fills and lost
  -$213.00, while the three SPY winners took 1, 1 and 5. That is the same shape as 2026-10-07.
  (Verified: raw/2026-10-08.json)
- 2026-10-07: seven contracts bought and sold in equal size the same day, all expiring that day, realized
  **-$729.00**. One of the seven made money: TSLA 375C, +$182.00 on 5 contracts. The other six lost between $44.00
  and $198.00 each. (Verified: raw/2026-10-07.json)
- 2026-10-07: the losses were not one bad position. TSLA 380C -$198.00, SPY 775P -$193.00, TSLA 377.5C -$180.00 and
  SPY 775C -$176.00 are four separate strikes losing a similar amount. (Verified: raw/2026-10-07.json)
- 2026-10-07: re-entry was heavy. TSLA 380C, SPY 775C, SPXW 7810C and TSLA 377.5C each took 7 separate buy fills to
  build 7 contracts, and all four lost. TSLA 375C, the only winner, took 5. (Verified: raw/2026-10-07.json)
- 2026-10-07: the two later-expiry contracts traded that day, TSLA 10-09 and META 10-16, were not closed flat, so they
  offer no comparison yet. (Verified: raw/2026-10-07.json)

## Count so far
Seen on 7 of 11 compiled days. Counting only same-day strikes bought and sold in equal size: **19 strikes, 108
contracts, 11 green, +$254.00**. By day those round trips returned **-$729.00, +$118.00, +$21.00, +$127.00,
+$188.00, +$462.00 and +$67.00** — the book turned positive on 2026-10-20, and every session after 2026-10-07 has
been green, five in a row. Two strikes are excluded because they closed or left a carried position rather than
round-tripping — TSLA 10-07 385C and TSLA 10-16 377.5C; counting net cash on every same-day strike instead gives
**+$776.00**. The four sessions 2026-10-12 to 2026-10-15 contribute nothing: their raw days were frozen with no
fills. (Verified: computed over raw/2026-10-07…raw/2026-10-21)

## What to do about it
Proposals only. The number to carry forward is round trips per strike against result per strike, because on this day
the four most re-entered strikes were all losers while the least re-entered was the winner. That is one day and could
easily be noise, so the useful action now is to keep the count rather than change the approach. The post-exit paths
for the same session were close to even, 16 of 28 continuing the trade's way, so this is not yet evidence that exits
were early.

Three days in, the pattern that survives is size rather than direction: the two positive 0DTE days were the two small
ones, 4 and 3 contracts, and the one heavy day, 7 contracts with 3-to-7 re-entry per strike, is the whole of the
-$615.00. That is still a correlation across three days and not a tested rule.
(Verified: computed over raw/2026-10-07…2026-10-09)
