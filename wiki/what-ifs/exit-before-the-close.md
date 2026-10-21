# Exit before the close

A same-day option closed for a small gain that would have been worth far more held to expiry, where the next half
hour of price action agreed with the exit and the session close did not. It is the mirror of an early stop: nothing
went wrong in the window the post-exit candles cover, so the exit cannot be faulted on the evidence the day page
normally carries. Only the settlement price shows the cost.

## Evidence
- **2026-10-19 and 2026-10-20 reversed the ledger.** The two sessions added **+$3,386.00**, turning a running
  **-$2,937.00** through 2026-10-16 into **+$449.00** across all 20 compiled same-day strikes. On the evidence to
  2026-10-16 exiting early looked like the expensive habit; across 20 strikes it is now slightly the cheaper one.
  (Verified: computed over raw/2026-10-07…raw/2026-10-20)
- 2026-10-20: SPY 10-20 768C. Nineteen contracts bought for **$3,179.00** and all nineteen sold for **$3,590.00**,
  **+$411.00**. SPY closed at **769.01**, so the call settled only **$1.01** in the money, **$101.00** a contract.
  Held, the nineteen were worth **$1,919.00** — **-$1,260.00** against cost. Exiting beat holding by **$1,671.00**,
  the largest margin either way so far. (Verified: raw/2026-10-20.json)
- 2026-10-20: the same session also shows the other side, small. SPY 10-20 766C, two contracts for **$236.00** sold
  for **$287.00**, settled **$3.01** in the money. Held they were worth **$602.00**, so exiting cost **$315.00**.
  Two same-day SPY calls, three strikes apart, opposite answers. (Verified: raw/2026-10-20.json)
- 2026-10-19: SPY 10-19 767C. Sixteen contracts bought for **$1,842.00** and all sixteen sold for **$2,030.00**.
  SPY closed at **766.54**, **$0.46** short of the strike, so the whole position settled worthless and holding
  would have returned **-$1,842.00**. Exiting beat holding by **$2,030.00**. (Verified: raw/2026-10-19.json)
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
Seen on 7 compiled days, over **20 same-day strikes** with a settlement price. Exiting beat holding on **12** of
them and cost money on **8**, and the net is **+$449.00** in favour of exiting. The distribution is what matters,
not the net: the two largest single entries are **+$2,030.00** (2026-10-19) and **-$4,304.00** (2026-10-16), so a
single strike still moves the total by more than every other strike combined.
(Verified: computed over raw/2026-10-07…raw/2026-10-20)

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
4. **Added 2026-10-20: drop "exiting early is costing money" as a working conclusion.** It was read off one strike
   on 2026-10-16 and two sessions reversed it — 12 of 20 strikes now favour exiting and the net is **+$449.00**.
   What survives is that the result is driven by tails, not by the typical strike: the two biggest entries are
   **+$2,030.00** and **-$4,304.00**. Size the position, not the exit rule.
   (Verified: computed over raw/2026-10-07…raw/2026-10-20)
