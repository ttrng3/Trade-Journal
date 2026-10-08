# Stop inside the noise

A stop placed so close to entry that ordinary quote movement reaches it before the setup has a chance to resolve. The
tell is a trade that dies in seconds rather than being proved wrong, and a fill meaningfully past the stop price,
because a stop inside the spread also gets the worst of the slippage.

## Evidence
- 2026-10-07: v7-2, META put. Entry 724.16 at 14:06:41, stop at 724.5957, which is 0.4357 away or 0.06% of the
  underlying. Stopped at 14:06:59, **18 seconds** after entry. The fill came at 724.6907, 0.0950 past the stop, so
  slippage alone cost 0.22R and turned a 1R loss into r -1.22 and -$87.90.
  (Verified: raw/2026-10-07.json)
- 2026-10-07: for contrast, v7-4 on the same underlying the same session used a 2.8414 stop, survived 41 minutes and
  ended directionally right at r +0.19. (Verified: raw/2026-10-07.json)

## Count so far
Seen once on 1 compiled day, costing **-$87.90** and 0.22R of pure slippage.
(Verified: computed over raw/2026-10-07…2026-10-07)

## What to do about it
Proposals only, for the Friday tune. On this one instance the direction was also wrong, since META rose 0.63 over the
next 10 candles, so a wider stop would have lost too. That makes this a sizing and slippage finding rather than proof
the trade should have been held: the 0.22R given to slippage is the part that was avoidable. Worth checking whether v7
ever places a stop below some floor relative to the underlying's recent range, and what those trades return as a
group, before changing anything.
