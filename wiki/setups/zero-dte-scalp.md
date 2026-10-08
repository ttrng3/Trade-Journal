# 0DTE scalp

Manual trading buys same-day-expiry calls and puts on SPY, SPXW and TSLA and closes them within the session, often
re-entering the same strike several times. Expiry day leaves no room for a position to come back, so the result is
decided by entry timing and by how many times a losing strike is re-entered.

## Evidence
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
Seen on 1 of 1 compiled days: 7 round trips, 1 winner, **-$729.00**.
(Verified: computed over raw/2026-10-07…2026-10-07)

## What to do about it
Proposals only. The number to carry forward is round trips per strike against result per strike, because on this day
the four most re-entered strikes were all losers while the least re-entered was the winner. That is one day and could
easily be noise, so the useful action now is to keep the count rather than change the approach. The post-exit paths
for the same session were close to even, 16 of 28 continuing the trade's way, so this is not yet evidence that exits
were early.
