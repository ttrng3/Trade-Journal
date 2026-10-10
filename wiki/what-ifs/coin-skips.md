# COIN skips

v7 vetoes COIN setups at roughly the same rate as everything else, but COIN is the one symbol where the skipped
setups go on to work. On the first compiled day it was the only symbol with a positive net R had the skips been taken.

## Evidence
- 2026-10-09: no COIN skips at all. v7 ran on SPY and QQQ only this session, so the COIN count did not move.
  (Verified: raw/2026-10-09.json)
- 2026-10-08: 2 COIN skips, 1 reached target first and 1 stopped first, **+0.50R** if taken. The target-first one was
  a call vetoed at 09:54:17 by structure, candle and timeframes, worth +1.50R; the stop-first one was a put vetoed at
  09:33:28 by volume. Both resolved at 10:29. (Verified: raw/2026-10-08.json)
- 2026-10-07: 18 COIN skips, 13 reached target before stop and 5 stopped first, worth **+13.93R** if taken. COIN
  supplied 13 of the day's 40 target-first skips while contributing only 5 of the 102 stop-first ones.
  (Verified: raw/2026-10-07.json)

## Count so far
Seen on 2 of 3 compiled days, 20 COIN skips in total, running **+14.43R** had they been taken. Over the same three
days the whole resolved v7 skip set would have returned -48.83R, so COIN remains the one symbol pulling the other way.
(Verified: computed over raw/2026-10-07…2026-10-09)

## What to do about it
For the Friday tune, proposals only:

1. Do not loosen the filter globally. On 2026-10-07 the whole resolved skip set was -41.46R, so a blanket loosening
   buys the QQQ and NVDA losses (-14.66R and -12.36R) to reach COIN's +13.93R.
   (Verified: computed over raw/2026-10-07.json)
2. Treat COIN as its own case and check whether a lower vote threshold on COIN alone is justified once more days are
   compiled. One day is one day: 18 skips is too small a sample to change a threshold on.
3. Until then, log COIN skips and their `first_hit` separately so the count builds.
4. Three days in, the sample has barely grown: 18 of the 20 COIN skips are from one session, and the symbol did not
   appear at all on 2026-10-09. Nothing here is yet strong enough to move a threshold.
   (Verified: computed over raw/2026-10-07…2026-10-09)
