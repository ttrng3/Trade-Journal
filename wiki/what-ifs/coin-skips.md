# COIN skips

v7 vetoes COIN setups at roughly the same rate as everything else, but COIN is the one symbol where the skipped
setups go on to work. On the first compiled day it was the only symbol with a positive net R had the skips been taken.

## Evidence
- 2026-10-07: 18 COIN skips, 13 reached target before stop and 5 stopped first, worth **+13.93R** if taken. COIN
  supplied 13 of the day's 40 target-first skips while contributing only 5 of the 102 stop-first ones.
  (Verified: raw/2026-10-07.json)

## Count so far
Seen on 1 of 1 compiled days. Running total **+13.93R** of blocked setups that reached target first, against the
-41.46R that taking every resolved v7 skip would have returned the same day.
(Verified: computed over raw/2026-10-07…2026-10-07)

## What to do about it
For the Friday tune, proposals only:

1. Do not loosen the filter globally. On 2026-10-07 the whole resolved skip set was -41.46R, so a blanket loosening
   buys the QQQ and NVDA losses (-14.66R and -12.36R) to reach COIN's +13.93R.
   (Verified: computed over raw/2026-10-07.json)
2. Treat COIN as its own case and check whether a lower vote threshold on COIN alone is justified once more days are
   compiled. One day is one day: 18 skips is too small a sample to change a threshold on.
3. Until then, log COIN skips and their `first_hit` separately so the count builds.
