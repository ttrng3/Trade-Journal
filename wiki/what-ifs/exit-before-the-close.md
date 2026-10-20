# Exit before the close

A same-day option closed for a small gain that would have been worth far more held to expiry, where the next half
hour of price action agreed with the exit and the session close did not. It is the mirror of an early stop: nothing
went wrong in the window the post-exit candles cover, so the exit cannot be faulted on the evidence the day page
normally carries. Only the settlement price shows the cost.

## Evidence
- 2026-10-16: QQQ 10-16 720P. Five contracts bought for **$639.00** and all five sold by 10:19:58 for **$766.00**,
  a **+$127.00** day. QQQ closed at **709.86**, so the put settled **$10.14** in the money, **$1,014.00** a
  contract. Held, the five were worth **$5,070.00**: **+$4,431.00** instead of +$127.00, and **$4,304.00** forgone.
  (Verified: raw/2026-10-16.json)
- 2026-10-16: the 10-candle window hid it completely. QQQ rose after every one of the four exits, **+1.46**,
  **+2.01**, **+1.98** and **+1.98** over the following 30 minutes, so each exit read as correct at the time and
  for half an hour after. (Verified: raw/2026-10-16.json)
- 2026-10-16: for contrast, the same session's TSLA 10-16 377.5C was exited on the same logic twelve minutes earlier
  and that exit was right — TSLA closed at **354.59** against a 377.50 strike, so holding would have cost the full
  **$378.00**. One rule, two opposite outcomes, one day. (Verified: raw/2026-10-16.json)

## Count so far
Seen once on 5 compiled days: 1 same-day strike exited before a move that settled in the money, **$4,304.00**
forgone. Against it, 1 same-day strike on the same session where exiting saved **$378.00**.
(Verified: computed over raw/2026-10-07…raw/2026-10-16)

## What to do about it
Proposals only; Ty decides.

1. Record the settlement price of every same-day strike traded, not just the next 10 candles. One day's evidence
   already shows the two disagreeing, and the day page would have read "exits were fine" on the candles alone.
   (Verified: raw/2026-10-16.json)
2. Do not turn this into "hold 0DTE to expiry". The same session's other strike expired worthless, and holding it
   would have cost **$378.00**; a single pair of opposite outcomes settles nothing.
   (Verified: raw/2026-10-16.json)
3. The testable question is narrower: when a same-day position is closed for a gain of under $100 per contract and
   the underlying later settles further the trade's way, how often and by how much. That needs more than one day.
   (Assumption: one observation, no rule proposed yet)
