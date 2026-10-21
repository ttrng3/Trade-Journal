# Later-expiry swing

A manual option position opened with days rather than hours left on it, carried through at least one overnight and
closed on a later session. It is the opposite trade to [[setups/zero-dte-scalp]]: the position is allowed to be wrong
for a while, so the result turns on the move rather than on entry timing within one session.

## Evidence
- 2026-10-13 to 2026-10-19: **TSLA 10-23 410C closed, and it was not the first one's result.** The strike ran for
  five sessions, 14 contracts bought for **$2,256.00** and 14 sold for **$2,216.00**: **-$40.00** over its whole
  life. The leg that was actually carried over a weekend — four contracts bought 2026-10-15 and 2026-10-16 for
  **$615.00** — was closed on 2026-10-19 inside a day that realized **+$84.00** on the strike on FIFO cost.
  (Verified: raw/2026-10-19.json; whole-life and FIFO cost computed over data/fills/2026-10.json)
- 2026-10-19 and 2026-10-20: TSLA 10-23 400C was traded **intraday on both sessions**, +$91.00 then +$83.00, never
  held overnight. A later-dated contract scalped inside a session is not this setup, and both results belong to
  the day rather than to the swing. (Verified: raw/2026-10-19.json, raw/2026-10-20.json)
- 2026-10-20: the clearest cost of exiting a later-dated position early. The three 400C contracts were sold between
  09:34:49 and 09:50:37 into 366–367, TSLA rose after every exit — **+5.74**, **+8.32**, **+6.29** over the next 10
  candles — and the session closed at **373.81**. (Verified: raw/2026-10-20.json)
- 2026-10-16: TSLA 10-23 410C opened, **7 days** to expiry. Three contracts at 1.69, 1.34 and 1.35 for **$438.00**,
  none sold, carried into the next session. No result yet; it is the second later-expiry position compiled and the
  only one currently open. (Verified: raw/2026-10-16.json)
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
Seen twice on 10 compiled days, and **both are now closed**: TSLA 10-16 400C **+$753.00** and TSLA 10-23 410C
**-$40.00** over its whole life, so **1 winner of 2** and **+$713.00** together. **No position is open** after
2026-10-20. Against the two, same-day strikes round-tripped in equal size now return **+$187.00** over 18 strikes,
and 2 near-dated contracts -$333.00. The later-expiry book is still ahead, but on a single large winner.
(Verified: computed over raw/2026-10-07…raw/2026-10-20; whole-life and open position computed over
data/fills/2026-10.json)

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
