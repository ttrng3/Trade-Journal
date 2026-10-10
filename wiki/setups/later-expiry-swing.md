# Later-expiry swing

A manual option position opened with days rather than hours left on it, carried through at least one overnight and
closed on a later session. It is the opposite trade to [[setups/zero-dte-scalp]]: the position is allowed to be wrong
for a while, so the result turns on the move rather than on entry timing within one session.

## Evidence
- 2026-10-08 to 2026-10-09: TSLA 10-16 400C, 8 days to expiry when first bought. Four contracts accumulated across
  Thursday at 1.62, 1.46, 1.34 and 1.25 premium, **$567.00** in total, none sold that day. All four were sold on
  Friday morning between 09:30:22 and 09:50:54 at 2.84, 2.86, 3.15 and 4.35 for **$1,320.00**, a **+$753.00** round
  trip. (Verified: raw/2026-10-08.json, raw/2026-10-09.json)
- 2026-10-07 to 2026-10-09: that single position made more than the thirteen same-day contracts of the week lost
  together. Grouping every contract that round-tripped inside the week by how far its expiry sat from its first
  trade: same-day expiry **-$615.00** over 13 contracts with 5 winners, one- and two-day expiry **-$333.00** over 2
  contracts with none, and the one eight-day contract **+$753.00**.
  (Verified: computed over raw/2026-10-07…2026-10-09)
- 2026-10-08: the two TSLA 10-09 calls traded that day, at 1 and 2 days to expiry, both lost: 380C -$213.00 and 385C
  -$120.00. Near-dated is not the same as later-dated and lost like the 0DTE book.
  (Verified: computed over raw/2026-10-07…2026-10-09)

## Count so far
Seen once on 3 compiled days: 1 completed later-expiry round trip, 1 winner, **+$753.00**. Against it, 13 same-day
contracts returned -$615.00 and 2 near-dated contracts -$333.00.
(Verified: computed over raw/2026-10-07…2026-10-09)

## What to do about it
Proposals only, for the Friday tune. **One position is not a strategy** and the sample here is a single contract in a
rising TSLA, so nothing about expiry choice is established. What the week does establish is that the result was
dominated by the one trade that was not 0DTE, which the same-day totals hide.

1. Keep realized result bucketed by days-to-expiry at first trade, so the comparison builds on more than one
   contract. (Verified: computed over raw/2026-10-07…2026-10-09)
2. Note that the exits here were not obviously early or late: 3 of the 4 sells saw TSLA continue up afterwards, but
   the net move across the four was -0.85. (Verified: raw/2026-10-09.json)
3. Do not read this as "hold longer" applied to the 0DTE book: those contracts expire the same day, so the choice is
   not available to them. The question is which book gets the size, and three days cannot answer it.
