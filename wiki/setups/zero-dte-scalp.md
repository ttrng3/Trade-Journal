# 0DTE scalp

Manual trading buys same-day-expiry calls and puts on SPY, SPXW and TSLA and closes them within the session, often
re-entering the same strike several times. Expiry day leaves no room for a position to come back, so the result is
decided by entry timing and by how many times a losing strike is re-entered.

## Evidence
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
Seen on 3 of 3 compiled days: 13 same-day-expiry contracts round-tripped inside the week, 5 winners, **-$615.00**.
By day, same-day-expiry round trips returned -$729.00, +$118.00 and +$21.00.
(Verified: computed over raw/2026-10-07…2026-10-09)

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
