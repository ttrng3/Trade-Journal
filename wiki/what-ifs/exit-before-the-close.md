# Exit before the close

A same-day option closed for a small gain that would have been worth far more held to expiry, where the next half
hour of price action agreed with the exit and the session close did not. It is the mirror of an early stop: nothing
went wrong in the window the post-exit candles cover, so the exit cannot be faulted on the evidence the day page
normally carries. Only the settlement price shows the cost.

## Evidence
- **2026-10-26 is the first session where every same-day strike settled in the money and exiting still beat
  holding on all of them — and it is the margin that does it, not the direction.** Two strikes, both settled in:
  SPY 764C by **$1.29** against a **765.29** close and NVDA 215C by **$0.97** against **215.97**. Held, the
  fifteen SPY calls were worth **$1,935.00** against the **$2,205.00** taken and the two NVDA calls **$194.00**
  against **$219.00**, so exiting beat holding by **$270.00** and **$25.00**. Average exit premiums were
  **$1.47** and **$1.10** against intrinsics of **$1.29** and **$0.97** — 18 and 12.5 cents a contract of time
  value that the settlement did not pay for. Across the nine earlier sessions 13 same-day strikes settled in the
  money and exiting beat holding on just **2**; this session takes that to **4 of 15**.
  (Verified: raw/2026-10-26.json; computed over raw/2026-10-07…raw/2026-10-26)
- **2026-10-26 refutes the page's own framing from the other side: the candles said hold 20 times out of 21 and
  holding would have lost.** SPY rose over the following 30 minutes after **all nineteen** SPY exits, by
  **1.12** to **2.50**, and the close went further the same way on the 0DTE strike; NVDA rose after one of its
  two exits. The page opens by saying the post-exit window cannot fault an exit. Here the window *endorsed*
  holding, unanimously on SPY, and the settlement still favoured the exit. The window is no better as evidence
  for holding than against it: half an hour of favourable movement says nothing about an expiry four hours out.
  This is the mirror of 2026-10-21, where both measures said hold and holding won.
  (Verified: raw/2026-10-26.json, raw/2026-10-21.json)
- **2026-10-26 is the quietest update this ledger has had, which is proposal 5's demonstration.** Two strikes
  moved the net by **+$295.00**, from **+$15,712.00** to **+$16,007.00** — the smallest single-session move of
  the ten, against **+$9,035.00** on 2026-10-22 and **-$3,780.00** on 2026-10-16. The count moved usefully and
  the net did not: exiting is now right on **30 of 41** strikes, **73.2%**, after **71.8%** and **66.7%** on the
  two sessions before. (Verified: computed over raw/2026-10-07…raw/2026-10-26)
- **2026-10-26: NVDA 215C is the narrowest call this ledger holds.** Two contracts, **$141.00** of cost for
  **$219.00**, and exiting beat holding by **$25.00** — against a next-narrowest of **$113.00** on 2026-10-08.
  A strike this close is the undecidable case proposal 6 asked to be recorded as undecided rather than counted;
  it is counted here, and it is worth noting that it could go either way on a cent of settlement.
  (Verified: raw/2026-10-26.json; computed over raw/2026-10-07…raw/2026-10-26)
- **2026-10-23: the two strikes that settled in the money are exactly the two where holding won, and the candles
  said so both times.** Twelve same-day strikes with a settlement price: ten settled worthless and exiting took
  **$7,677.00** that holding would have returned as nothing, while SPY 762P cost **$780.00** and TSLA 370C
  **$207.00**. The day's net is **+$6,690.00**. What makes the session useful is not the net but that the two
  wrong exits were both visible at the time — the post-exit candles went the trade's way in both cases — which is
  the opposite of the 2026-10-16 case the page opens with.
  (Verified: raw/2026-10-23.json; computed over raw/2026-10-07…raw/2026-10-23)
- **2026-10-23: SPY 762P is the cleanest counter-case compiled — both measures said hold and the exit was taken
  anyway.** The session's only put: seven contracts bought 11:43:39 to 12:04:24 for **$835.00**, six sold at
  12:00:12 at 0.96 and one at 12:05:23 at 1.07 for **$683.00**, **-$152.00**. SPY **fell** after both exits,
  **-1.22** and **-0.58** over the next 30 minutes, which is the put's direction, and closed at **759.91**, so the
  put settled **$2.09** in the money. Held, the seven were worth **$1,463.00**: **+$628.00** instead of -$152.00,
  **$780.00** forgone. The page's own framing — "nothing went wrong in the window the post-exit candles cover" —
  does not apply here. (Verified: raw/2026-10-23.json)
- **2026-10-23 makes the put asymmetry the most interesting thing on this page.** Split the 39 strikes by side:
  **33 calls** return **+$21,276.00** with exiting right on 26 of them, while **6 puts** return **-$5,564.00**
  with exiting right on only 2. Puts are 6 of 39 strikes but **4 of the 11 misses**, and those four carry
  **-$6,326.00** of cost — including the three largest put misses, which are the first, third and fourth largest
  misses overall: **-$4,304.00** (QQQ 720P, 2026-10-16), **-$906.00** (QQQ 753P, 2026-10-08) and **-$780.00**
  (SPY 762P, 2026-10-23). Six strikes is a small sample and the two profitable put exits are real, so this is a
  question, not a finding: it is the first split of this ledger that does not reverse every session.
  (Verified: computed over raw/2026-10-07…raw/2026-10-23)
- **2026-10-23: the day the morning TSLA exits were right, which reverses Thursday.** TSLA 375C, fifteen contracts
  for **$1,547.00** sold for **$2,087.00** in nine exits inside 25 minutes: TSLA was **lower** 30 minutes later
  after 7 of the 9 and closed **$2.78** below the strike, so the whole position settled worthless. On 2026-10-22
  the same morning pattern on the same underlying was followed by rallies of **+11.72**, **+8.91** and **+5.37**
  and looked wrong all day. Same trade shape, same symbol, opposite answer one session apart.
  (Verified: raw/2026-10-23.json, raw/2026-10-22.json)
- **2026-10-22 is the first session where every same-day strike agreed, and it broke the aggregate.** Six same-day
  strikes, all six settled worthless: five SPXW calls at 7670–7710 against a **7639.70** proxy close, and SPY 767C
  against **763.97**. Holding the six would have cost the full **$9,841.00** of premium they carried; exiting
  returned **$9,035.00** more than holding. That single session took the running total from **-$13.00** to
  **+$9,022.00**. (Verified: raw/2026-10-22.json; computed over raw/2026-10-07…raw/2026-10-22)
- **2026-10-22 shows what the aggregate is worth.** One ordinary session moved it by **$9,035.00**, from
  **-$13.00** to **+$9,022.00**, on a sample of 27 strikes. The proposal added 2026-10-21 said to stop reporting
  the net; this is the demonstration, and it happens to point the other way from the 2026-10-16 tail.
  (Verified: computed over raw/2026-10-07…raw/2026-10-22)
- **2026-10-22: the clean case where the candles and the close agreed 15 times out of 15.** SPY 10-22 767C, twenty
  contracts for **$2,581.00** sold for **$2,660.00**, **+$79.00**. SPY was lower 30 minutes after **every one of
  the 15 exits**, by **0.15** to **3.77**, and closed **$3.03** below the strike. The usual defence of an exit and
  the usual refutation of it are both absent: nothing here argues for holding. (Verified: raw/2026-10-22.json)
- **2026-10-22: the largest single pro-exit entry so far.** SPXW 10-22 7710C, 22 contracts carrying **$3,625.00**,
  sold for **$3,580.00** across 14 exits, then settled **70.30** out of the money. Holding returned **-$3,625.00**,
  so exiting beat it by **$3,580.00** — second only in magnitude to the **-$4,304.00** of 2026-10-16, and opposite
  in sign. The two tails now face each other. (Verified: raw/2026-10-22.json)
- **2026-10-21 erased the reversal with two contracts.** SPY 10-21 769C, two contracts bought for **$291.00** and
  both sold for **$358.00**, **+$67.00**. SPY closed at **773.10**, so the call settled **$4.10** in the money,
  **$410.00** a contract. Held, the two were worth **$820.00**: **+$529.00** instead of +$67.00, so exiting cost
  **$462.00**. That one strike took the running total from **+$449.00** to **-$13.00** across 21 strikes — the
  smallest position in the series moving the aggregate further than the direction the previous two sessions had
  established. (Verified: raw/2026-10-21.json; computed over raw/2026-10-07…raw/2026-10-21)
- **2026-10-21 is the case where the candles agreed with the settlement.** Both exits were followed by SPY rising,
  **+1.58** and **+0.95** over the next 30 minutes, and the close went further the same way. The usual defence of
  an exit — that the next half hour looked fine — is not available here. (Verified: raw/2026-10-21.json)
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
Seen on 10 compiled days, over **41 same-day strikes** with a settlement price. Exiting beat holding on **30** of
them and cost money on **11**, and the net is **+$16,007.00**. The distribution is still the whole story and the
net is still worthless as a statistic: it has read **-$2,937.00**, **+$449.00**, **-$13.00**, **+$9,022.00**,
**+$15,712.00** and **+$16,007.00** on consecutive updates, changing sign on three of the six. The two largest
single entries are **-$4,304.00** (2026-10-16) and **+$3,580.00** (2026-10-22); the smallest is **$25.00**
(2026-10-26). What has become stable is the *count*: exiting has been right on **30 of 41** strikes, **73.2%**,
rising through **57.1%**, **66.7%** and **71.8%** over the three sessions before, and the eleven misses still
carry the money — the four largest are **-$4,304.00**, **-$1,059.00**, **-$906.00** and **-$780.00**, three of
them puts. Split by side, calls are **+$21,571.00** over 35 strikes and puts **-$5,564.00** over 6; no put has
been traded since 2026-10-23, so that side has not moved.

The cut that 2026-10-26 added is **settlement margin**. Of the 41 strikes, **15** settled in the money and
**26** settled worthless; exiting was right on **26 of 26** of the worthless ones by construction and on only
**4 of 15** of the rest. So the whole of this ledger's risk sits in the in-the-money tail, and within that tail
what separates the 4 from the 11 is how far past the strike the close landed relative to the premium taken.
(Verified: computed over raw/2026-10-07…raw/2026-10-26)

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
5. **Added 2026-10-21: stop reporting the net at all.** Two contracts took it from +$449.00 to -$13.00 in one
   session, which is the clearest possible demonstration that the sign of this total carries no information at 21
   strikes. Report the per-strike distribution and the two tails; leave the aggregate out of the weekly until the
   sample is large enough that one strike cannot flip it.
   (Verified: computed over raw/2026-10-07…raw/2026-10-21)
6. **Added 2026-10-22: separate the proxy-settled strikes from the rest.** Five of the six strikes this session
   were SPXW, and the collector carries no SPX bars, so their settlement check is the **SPY × 10** proxy. Here the
   margin was 30 to 70 points and the answer is safe either way, but a strike within a few points of the proxy
   close is not decidable and should be recorded as undecided rather than counted in this ledger.
   (Verified: raw/2026-10-22.json)
7. **Added 2026-10-22: the net is now confirmed useless and proposal 5 stands.** It has read -$2,937.00,
   +$449.00, -$13.00 and +$9,022.00 on four consecutive updates. Report the count of strikes each way and the two
   tails, and nothing else, until the sample is large enough that one session cannot move it by $9,035.00.
   (Verified: computed over raw/2026-10-07…raw/2026-10-22)

8. **Added 2026-10-23: split this ledger by call and put before anything else.** It is the only cut that has not
   reversed on the next session: 33 calls **+$21,276.00** with exiting right 26 times, 6 puts **-$5,564.00** with
   exiting right twice, and three of the four largest misses are puts. The action is to keep the two counts
   separately from here on, not to change an exit rule on six strikes. If the put side still reads this way at
   fifteen or twenty strikes, the question becomes whether a falling underlying is being treated as a reason to
   close a put. (Verified: computed over raw/2026-10-07…raw/2026-10-23)
9. **Added 2026-10-23: the candles are not always the alibi.** The page opens by saying the post-exit window
   cannot fault these exits. On both of this session's misses the window went the trade's way and the close went
   further, so both were visible without the settlement price. Record, per miss, whether the 10-candle window
   agreed with the exit or not — that separates the misses that were knowable at the time from the ones only
   settlement reveals. (Verified: raw/2026-10-23.json)
10. **Added 2026-10-26: split this ledger on settlement margin, not on in-the-money or not.** All 26 strikes that
    settled worthless favoured exiting by construction, and only **4 of the 15** that settled in the money did,
    so the only question this ledger really asks is what happens in that tail. The measurable version is
    intrinsic-at-settlement minus average exit premium, per contract: on 2026-10-26 it was **-$0.18** and
    **-$0.125** and exiting won, on 2026-10-16 it was **+$8.61** on the QQQ put and holding won by $4,304.00.
    Record that one number per strike and the 11 misses should separate from the 4 cleanly, which neither the net
    nor the 10-candle window does. (Verified: computed over raw/2026-10-07…raw/2026-10-26)
11. **Added 2026-10-26: drop the 10-candle window as evidence either way.** Proposal 9 asked whether the window
    agreed with each miss. Run on this session it agreed with holding on 20 of 21 exits and holding lost on both
    settled strikes, so the window has now been wrong in both directions — it hid the cost completely on
    2026-10-16 and it argued for a hold that would have lost on 2026-10-26. Keep recording it, because it is what
    a decision could actually see at the time, but stop treating agreement or disagreement with it as evidence
    about the exit. (Verified: raw/2026-10-26.json, raw/2026-10-16.json)