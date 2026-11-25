# Later-expiry swing

A manual option position opened with days rather than hours left on it, carried through at least one overnight and
closed on a later session. It is the opposite trade to [[setups/zero-dte-scalp]]: the position is allowed to be wrong
for a while, so the result turns on the move rather than on entry timing within one session.

## Evidence

- **2026-11-24: the carry empties out at +$40.00, and the busiest intraday later-dated session compiled returns
  +$204.00.** The single contract carried out of 2026-11-23 — AAPL 12-04 360C, basis **1.95** — was sold at
  **09:38:16** at **2.35**, a **+$40.00** carry leg, and nothing was carried out of this session. The book ended
  flat for the first time since **2026-11-17**.

  The session's own tenor ladder is the clearest one compiled, because the underlying and the hour are nearly
  held constant. NVDA was traded at four tenors on the same morning: **11-25** (one day out) **30** contracts for
  **-$255.00**, **12-18** (24 days) **6** contracts for **+$186.00**, **01-15** (52 days) **4** contracts for
  **+$30.00**. Add SPY 11-25 725C **+$83.00** and TSLA 11-25 385C **+$160.00**, both one day out and both single
  contracts, and the intraday later-dated book for the session is **8** strikes, **42** contracts, **5 green**,
  **+$204.00** — eight strikes being the most in one session on this measure, against a previous high of five
  (2026-11-12).

  The NVDA 12-18 ladder deserves its own line: six contracts bought down **4.54 → 4.10** and sold in six separate
  fills at **4.45**, **4.45**, **4.60**, **4.75**, **4.85** and **4.60**, **+$186.00**, the day's largest strike
  result. It was built exactly like the near-dated ladders that were dumped whole for **-$735.00** and exited
  nothing like them. See [[mistakes/dump-below-the-ladder]]. (Verified: raw/2026-11-24.json, raw/2026-11-23.json)
- **2026-11-23: the carry record reverses in one session, +$14,931.00 over 18 contracts.** The five later-expiry
  positions carried out of 2026-11-20 on **$3,180.00** of cost were sold into Monday's gap for **$18,111.00**,
  **5.70×** cost: NVDA 11-25 145C **+$7,054.00** (**+1,092%**), TSLA 12-04 400C **+$2,508.00** (**+255%**), NVDA
  01-15 175C **+$2,181.00** (**+312%**), SPY 11-25 725C **+$1,821.00** (**+278%**) and the two contracts of TSLA
  11-25 385C that Friday's dump left behind **+$1,367.00** (**+690%**). Before this session, overnight holding of
  later expiries was **-$1,983.17** over **94** contracts across **16** closing sessions, positive on **5** of
  them; it is now **+$12,947.83** over **112** across **17**, positive on **6**. See [[days/2026-11-23]].
  (Verified: raw/2026-11-23.json; carry legs computed over data/fills/2026-10.json and data/fills/2026-11.json)
- **2026-11-23: the gap did the work, not the tenor.** From Friday's close to the 09:33 candle NVDA went
  **125.81 → 162.30** (**+29.00%**), TSLA **345.99 → 382.04** (**+10.42%**) and SPY **690.81 → 721.42**
  (**+4.43%**). Two of the five strikes never came into the money at all — NVDA 01-15 175C closed **$9.81** out
  and SPY 11-25 725C **$2.58** out — and still returned **+312%** and **+278%**, so most of the result is the
  underlying's move repriced into time still on the clock, not intrinsic value. The page's standing argument for
  the longer tenor, that a bad day can be waited out, finally has an instance where the waiting was what paid.
  (Verified: raw/2026-11-20.json, raw/2026-11-23.json)
- **2026-11-23: the exposure was unchanged, only the outcome.** The **$3,180.00** went into the weekend as four
  ladders built downward into a **-12.34%** NVDA session plus two leftovers, with no exit plan recorded on
  [[days/2026-11-20]]. One contract was carried out of this session: AAPL 12-04 360C, **$195.00**, **11** days to
  run — **6.1%** of the risk carried the session before. The method that produced **+$14,931.00** here produced
  **-$3,389.00** of later-expiry cash on Friday. (Verified: raw/2026-11-23.json, raw/2026-11-20.json)
- **2026-11-20: the later-expiry book lost -$3,389.00 in cash while the same-day book made +$194.00, the widest
  split either way on record.** Eight of the session's twelve strikes had 5 or more days to run and they took
  **46** of the **61** fills and **$6,660.00** of the **$7,825.00** bought. On closed contracts the split is
  **-$1,552.00** later against **-$5.00** same-day, and every one of the **18** contracts carried into the
  weekend — **$3,180.00** of cost — is a later expiry. See [[days/2026-11-20]].
  (Verified: raw/2026-11-20.json; computed over data/fills/2026-11.json)
- **2026-11-20: extra time bought nothing on a -12.34% NVDA day.** NVDA 01-15 190C had **56** days left and
  still lost **-$639.00**, the session's largest, dumped at **0.90** against a ladder built to **1.06** across
  three sessions. NVDA 11-25 145C and 01-15 175C were never sold at all and finished **$19.19** and **$49.19**
  out of the money. The usual argument for the longer tenor — that a bad day can be waited out — requires the
  position to be held, and on this session four later-expiry strikes were dumped and four were held without any
  exit plan at all. (Verified: raw/2026-11-20.json)
- **The three largest later-expiry losses on record are the three most recent sessions that traded them.**
  **-$3,389.00** (2026-11-20), **-$2,781.00** (2026-11-13) and **-$2,402.00** (2026-11-10). Later-expiry cash has
  been negative on **7** of the **18** compiled sessions and positive on **10**, so the count is not the story;
  the size is. The three November losses are each larger than the largest later-expiry gain outside
  2026-11-11's **+$4,990.00**. (Verified: computed over raw/2026-10-07…raw/2026-11-20)
- **2026-11-10 → 2026-11-11: the fifth swing, NVDA 11-18 185C, +$1,112.00 over its whole life and the page's
  second winner.** Eleven contracts bought 09:37:41–11:57:36 on 2026-11-10 from **3.75** down to **2.62** for
  **$3,358.00**; two were sold the same day at 3.85 and 4.00 and the remaining **9** were held overnight with
  **8** days to expiry, then sold 07:54:55–10:40:42 the next morning at 3.70–4.50 for **$3,685.00**. The carry
  leg alone was **+$937.55** on an average-cost basis. It is the largest swing compiled by contracts and by
  result, and the first since 2026-10-09 to make money.
  See [[days/2026-11-10]], [[days/2026-11-11]] and [[mistakes/overnight-0-1-dte]].
  (Verified: raw/2026-11-10.json, raw/2026-11-11.json; whole life computed over data/fills/2026-11.json)
- **2026-11-13: three swings opened and still open, 4 contracts, and the first time this page ends a week
  unresolved.** NVDA 11-18 180C (**2** contracts, 5 DTE), QQQ 11-18 695C (**1**, 5 DTE) and SPCX 11-20 150C
  (**1**, 7 DTE) were all open at the bell with **-$724.00**, **+$43.00** and **-$175.00** of realized cash
  behind them. The export this run read ends 2026-11-13T15:51:46, so their outcomes are not in the repo and are
  excluded from every total on this page. See [[days/2026-11-13]].
  (Verified: raw/2026-11-13.json; open positions computed over data/fills/2026-11.json)
- **2026-11-12: five later-dated strikes opened and closed inside the session for +$824.00, the best intraday
  reading this page has recorded and five of the day's six green strikes.** SPY 11-13 757C **+$265.00**, TSLA
  11-13 400C **+$243.00**, NVDA 11-18 175C **+$205.00** at **+33.3%** on two contracts, TSLA 11-13 397.5C
  **+$60.00** and TSLA 11-13 395C **+$51.00**. Four of the five are next-day expiry.
  See [[days/2026-11-12]]. (Verified: raw/2026-11-12.json)
- **2026-11-11: two intraday later-dated strikes, both green, +$1,305.00.** SPXW 11-12 7660C **+$770.00** at
  **+32.9%** on seven contracts, closing with **2** at **5.80** above every buy in its ladder, and TSLA 11-13
  395C **+$535.00** at **+53.5%** on three. The same add-down shape that lost **-$1,125.00** on the 0DTE strike
  beside them, held one expiry further out. See [[days/2026-11-11]]. (Verified: raw/2026-11-11.json)
- **2026-11-13: QQQ 11-18 700C, -$1,925.00, the largest single loss this page has recorded.** Seventeen contracts
  bought 09:39:57–10:11:30 from 2.94 down to 1.32 for **$3,625.00**, all seventeen sold at **10:26:13** at
  **1.00**, below every buy. Being further from expiry did not protect it: the loss is **-53.1%** of premium in
  47 minutes. See [[mistakes/dump-below-the-ladder]]. (Verified: raw/2026-11-13.json)
- **2026-11-10: SPY 11-12 751C, +$470.00 over 21 contracts and 29 fills, and the morning leg made more than the
  strike kept.** Six bought 09:37:07–09:50:42 at 3.80–3.30 sold 09:58:32–10:09:21 at 4.20–5.00 for
  **+$616.00**; two afternoon legs then returned **-$262.00** and **+$116.00**. The one loss of the three is the
  eight-contract exit at **2.23** at 12:35:01. See [[days/2026-11-10]]. (Verified: raw/2026-11-10.json)
- **2026-11-02: four more later-dated contracts opened and closed inside one session, all green, and together
  they out-earned the eleven before them.** TSLA 11-06 425C took **10** contracts for **+$450.00**, TSLA 11-13
  430C **6** for **+$415.00**, SPY 11-03 760C **8** for **+$325.00** and TSLA 11-04 412.5C **1** for
  **+$155.00** — **+$1,345.00** on **25** contracts carrying **$6,773.00**, a **+19.9%** return on premium. The
  eleven earlier intraday later-dated positions returned **+$627.00** in total, so one session more than doubled
  the group. None is this setup and each result sits on its day page, but the group keeps extending and keeps
  winning. (Verified: raw/2026-11-02.json; computed over raw/2026-10-07…raw/2026-11-02)
- **2026-11-02: the later-dated book is now ahead of the same-day book on realized cash, which reverses this
  page's own reading.** Intraday later-dated positions stand at **+$1,972.00** over **15** and completed swings at
  **+$204.00** over **4**, while same-day strikes round-tripped in equal size stand at **-$154.00** over **53**.
  Through 2026-10-30 this page recorded the opposite — the 0DTE book ahead of every later-dated measure — and a
  single session changed both sides of it. See [[setups/zero-dte-scalp]].
  (Verified: computed over raw/2026-10-07…raw/2026-11-02)
- **2026-11-02: TSLA 11-04 412.5C is the best return on premium the group holds.** One contract bought at
  **09:55:41** at 2.55 and sold at **10:11:57** at **4.10**: **+$155.00**, **+60.8%** in sixteen minutes, against
  the **+35.0%** of TSLA 11-06 410C on 2026-10-30. The smallest position of the session returned the most per
  dollar committed, and it was two days from expiry — the shortest later-dated tenor traded that session.
  (Verified: raw/2026-11-02.json, raw/2026-10-30.json)
- **2026-11-02: the whole later-dated book was closed by 10:16:11, before the session's losses began.** All four
  positions were opened between 09:33:07 and 09:55:41 and every one was out by **10:16:11**; every strike opened
  after that time lost, seven of them for **-$1,931.00**. Holding days rather than hours is this page's premise,
  and on this session none of the four used it. (Verified: raw/2026-11-02.json)
- **2026-10-28 → 2026-10-29: GOOG 11-20 375C is the fourth swing, the longest-dated position compiled, and it
  lost 87% overnight.** One contract bought 2026-10-28 at 14:46:17 at **1.43** and sold 2026-10-29 at 09:36:16 at
  **0.19**, **-$124.00**, with **23** days still to run. Distance from expiry cushioned it barely: **87%** of the
  premium went against **94%** and **96%** on the two 1-DTE carries closed the next morning, so three more weeks of
  time value bought seven points of protection on a position that still lost almost all of itself overnight. The raw day carries no price path for it — GOOG is outside the collector's symbol list —
  so there is no post-exit reading. See [[mistakes/overnight-0-1-dte]].
  (Verified: raw/2026-10-29.json; whole life computed over data/fills/2026-10.json)
- **2026-10-29 and 2026-10-30: three more later-dated contracts opened and closed inside one session, all green.**
  SPY 10-30 766P took **10** contracts on 2026-10-29 for **+$64.00** in 43 minutes; TSLA 11-06 410C took **2** on
  2026-10-30 for **+$144.00**, a **+35.0%** return on premium in fourteen minutes and the best of the group; SPY
  11-02 765C took **1** for **+$13.00**. None is this setup and each result sits on its day page, but the group
  keeps extending and keeps winning. (Verified: raw/2026-10-29.json, raw/2026-10-30.json)
- **2026-10-26: SPY 10-28 764C was scalped intraday, not swung, and it ran beside its own 0DTE twin.** Four
  contracts bought between 09:41:12 and 10:09:36 at 3.66–3.80 for **$1,500.00** and all four sold between
  09:56:05 and 10:11:02 at 3.94–4.19 for **$1,636.00**, **+$136.00**, two days before expiry. As with AAPL 10-30
  on 2026-10-23, the two SPY next-day calls on 2026-10-22 and the TSLA 400C on 2026-10-19 and 2026-10-20, a
  later-dated contract opened and closed inside one session is not this setup and the result belongs to the day.
  What is new is that the same strike was traded at both expiries at once: the fifteen 0DTE 764 calls returned
  **+$246.00** and these four **+$136.00**, so the near leg made more on nearly four times the contracts while
  the later leg returned more per contract — **$34.00** against **$16.40**. One session is not a comparison of
  the two books, but it is the first time they have been run side by side on one strike.
  See [[setups/zero-dte-scalp]]. (Verified: raw/2026-10-26.json)
- **2026-10-26: still nothing open, for the second session running.** Every strike was net flat at the bell and no
  position opened during the month remains open once this session's fills are in. The three negative net
  quantities the month shard shows are September positions closed on 2026-10-02, not open risk.
  (Verified: raw/2026-10-26.json; open positions computed over data/fills/2026-10.json)
- **2026-10-23: the carry closed two seconds after the bell, and it was the right exit.** The eight TSLA 10-23
  387.5 calls left open on 2026-10-22 for **$789.00** were sold in one fill at **09:30:02** at 0.18 for
  **$144.00**. TSLA closed at **372.22**, **$15.28** below the strike, so holding any longer returned nothing: the
  **-$645.00** was already lost at Thursday's bell and the opening exit recovered what was left. The cost belongs
  to the decision to carry, not to the exit. (Verified: raw/2026-10-23.json; carry cost raw/2026-10-22.json)
- **2026-10-23: AAPL 10-30 350C was scalped intraday, not swung.** Two contracts bought at 14:32:06 and 14:47:43
  for **$548.00** and both sold at 15:02:50 and 15:15:22 for **$597.00**, **+$49.00**, a week before expiry. As
  with the two SPY next-day calls on 2026-10-22 and the TSLA 400C on 2026-10-19 and 2026-10-20, a later-dated
  contract opened and closed inside one session is not this setup and the result belongs to the day. It was also
  the only later-dated contract traded that session and the last position closed.
  (Verified: raw/2026-10-23.json)
- **2026-10-22 to 2026-10-23: TSLA 10-23 387.5C, the third completed swing and the worst.** Twenty-two contracts
  were bought across the whole of 2026-10-22, 09:30:48 to 15:59:32, at 0.75–2.05 for **$3,059.00**; fourteen were
  sold the same session for **$2,530.00**, **+$260.00** on their FIFO cost. The **eight** left open at the bell
  carried **$789.00** of cost and were sold on 2026-10-23 at 0.18 for **$144.00**: the overnight carry returned
  **-$645.00**, two and a half times the **+$260.00** the intraday round trips made. TSLA closed 2026-10-22 at
  **374.57**, already **$12.93** below the strike. (Verified: raw/2026-10-22.json; carry computed over
  data/fills/2026-10.json)
- **2026-10-22: holding was wrong here and the morning said otherwise for hours.** The three exits in the first ten
  minutes were each followed by TSLA rallying **+11.72**, **+8.91** and **+5.37** over the next 30 minutes, so the
  carry looked vindicated all morning; the strike was never reached. This is the mirror of the 2026-10-20 case on
  the 400C, where the post-exit rally was real and the close confirmed it.
  (Verified: raw/2026-10-22.json)
- **2026-10-22: two SPY next-day calls were scalped intraday, not swung.** SPY 10-23 768C, 18 contracts for
  **+$80.00**, and SPY 10-23 766C, 5 contracts for **+$142.00**, both opened and closed inside the session. As with
  the 400C on 2026-10-19 and 2026-10-20, a later-dated contract traded inside one session is not this setup; both
  results belong to the day. (Verified: raw/2026-10-22.json)
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

**Added 2026-11-24, counting 2026-11-24, and the gap this page flagged is closed for the intraday measure.**

Carry legs — a sell whose matched buy is from an earlier session, on a contract that has not reached expiry — go
to **+$12,987.83** over **113** contracts and **42** legs across **18** closing sessions, **7** of them positive.
This session contributes one leg, one contract, **+$40.00**. Nothing is carried out of it, so the next session
starts with no carry for the first time since 2026-11-17 and the measure pauses there.

**The intraday later-dated book is now computed over every compiled raw day: 36 strikes, 254 contracts, 28 green,
+$2,027.00.** The 2026-11-17 reading of **25 strikes, 195 contracts, 22 green, +$2,347.00** stopped at
2026-11-13, and this page has since said that folding 2026-11-16 to 2026-11-20 into it was work for a session
with the time for it. The three sessions that had positions on this measure are 2026-11-20 **-$588.00** (2
strikes, 14 contracts, 0 green), 2026-11-23 **+$64.00** (1, 3, 1) and 2026-11-24 **+$204.00** (8, 42, 5). The
method reproduces the earlier figure exactly at 2026-11-13, so the series is continuous.

The book stays the consistently positive part — **28 green of 36** — but it is **$320.00** below its 2026-11-13
peak, and both of its losing sessions are in the last three weeks: QQQ 11-18 700C **-$1,925.00** (2026-11-13) and
the 2026-11-20 pair **-$588.00**. Against the same-day book at **-$1,550.00** over **70** strikes the spread is
**$3,577.00**, narrower than the **$4,162.00** recorded on 2026-11-13. Tenor remains the most durable cut this
wiki has; it is no longer widening. See [[setups/zero-dte-scalp]].
(Verified: computed over raw/2026-10-07…raw/2026-11-24; carry legs computed over data/fills/2026-10.json and
data/fills/2026-11.json)

**Added 2026-11-24, counting 2026-11-23.** Overnight holding of later expiries, measured as carry legs — a sell
whose matched buy is from an earlier session, on a contract that has not reached expiry — now stands at
**+$12,947.83** over **112** contracts and **41** legs across **17** closing sessions, **6** of them positive.
This session alone is **+$14,931.00** over **18** contracts and **5** legs. Without it the record is
**-$1,983.17** over **94**, which is what every earlier reading of this page described. A single gap moved the
cumulative figure by **$14,931.00** and flipped its sign, so the carry's expectancy is not estimable from
seventeen sessions: the distribution has one leg that is **6.7×** the largest of the other sixteen sessions
(**+$7,054.00**, NVDA 11-25 145C, against **+$1,057.00**, NVDA 11-18 185C on 2026-11-11), and the worst is **-$2,125.00**
(TSLA 11-11 425C, 2026-11-04).

The prior counts on this page are not restated here. The swing taxonomy they use — whole-life results per
strike, counted as five swings of which four closed — was last computed on 2026-11-17 against raw days through
2026-11-13, and the sessions 2026-11-16 to 2026-11-20 were never folded into it. The carry-leg measure above
covers every session in both shards and is the one this update extends; re-deriving the whole-life swing count
over the gap is work for a session with the time for it.
(Verified: computed over data/fills/2026-10.json and data/fills/2026-11.json)

Seen four times on 19 compiled days, and **all four are closed**: TSLA 10-16 400C **+$753.00**, TSLA 10-23 410C
**-$40.00**, TSLA 10-23 387.5C **-$385.00** and GOOG 11-20 375C **-$124.00** over their whole lives, so **1 winner
of 4** and **+$204.00** together. No fifth swing has been opened. The page still rests entirely on the single large
winner of 2026-10-09 and has lost on all three positions since. **No position is open** anywhere in October after
2026-10-30 or in November after 2026-11-02, so nothing has been held overnight since the week of 2026-10-26.

Distinct from the four swings, **fifteen** later-dated contracts have now been opened and closed inside a single
session — TSLA 10-09 380C, TSLA 10-23 400C twice, MSFT 10-21 532.5C, SPY 10-23 768C and 766C, AAPL 10-30 350C, SPY
10-28 764C, SPY 10-30 766P, TSLA 11-06 410C, SPY 11-02 765C, SPY 11-03 760C, TSLA 11-04 412.5C, TSLA 11-06 425C and
TSLA 11-13 430C — returning **+$1,972.00** over the fifteen with **14** green. They outnumber the swings nearly
four to one and are the only part of the later-dated book that is consistently positive: **+$1,972.00** scalped
against **+$204.00** swung, on far less capital at risk per contract. **Seven** of the fifteen are TSLA and
**six** SPY; the TSLA seven carry **+$1,125.00** of the **+$1,972.00**, and three of those seven are from
2026-11-02 alone.

Against both, same-day strikes round-tripped in equal size now return **-$154.00** over 53 strikes, so as of
2026-11-02 the intraday later-dated book is ahead of the 0DTE book on realized cash for the first time — the
reverse of what this section recorded through 2026-10-30. Overnight holding of any tenor cost **-$1,694.67**
across October over 23 carry events; November has recorded none.
See [[mistakes/overnight-0-1-dte]].
(Verified: computed over raw/2026-10-07…raw/2026-11-02; whole-life and carries computed over
data/fills/2026-10.json; open positions computed over data/fills/2026-10.json and data/fills/2026-11.json)

**Added 2026-11-17, counting 2026-11-10 to 2026-11-13.** The swings become **5**, of which **4 are closed** and
**2 green**: TSLA 10-16 400C **+$753.00**, TSLA 10-23 410C **-$40.00**, TSLA 10-23 387.5C **-$385.00**, GOOG
11-20 375C **-$124.00** and NVDA 11-18 185C **+$1,112.00**, together **+$1,316.00**. The page no longer rests on
the single 2026-10-09 winner, but it now rests on two, and the three losses between them are unchanged. **Three
further swings are open** as of 2026-11-13 and are excluded.

The intraday later-dated book, still the consistent part, goes to **25** strikes, **195** contracts, **22** green,
**+$2,347.00**. The ten added this week returned **+$375.00** with **8** green, and the whole of the shortfall
against the previous reading is one strike: QQQ 11-18 700C at **-$1,925.00**, the first intraday later-dated
position to lose more than **$220.00**. Without it the ten returned **+$2,300.00**.

Against the same-day book the gap has widened sharply. 0DTE round trips now stand at **-$1,815.00** over **61**
strikes while intraday later-dated strikes stand at **+$2,347.00** over **25** — a **$4,162.00** spread, against
the **$2,126.00** spread recorded on 2026-11-02, on roughly a third as many positions. Tenor remains the most
durable cut this wiki has, and it survived the worst session compiled.
See [[setups/zero-dte-scalp]] and [[mistakes/overnight-0-1-dte]].
(Verified: computed over raw/2026-10-07…raw/2026-11-13; whole-life, carries and open positions computed over
data/fills/2026-10.json and data/fills/2026-11.json)

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
4. **Added 2026-11-02: give the intraday later-dated book its own page or its own count, because it is no longer
   a footnote.** Fifteen positions, **14** green, **+$1,972.00**, against four swings at **+$204.00** and a 0DTE
   book at **-$154.00**. It is described here as "not this setup" and its results are sent to the day pages, which
   means the one consistently positive part of the book has no page of its own.
   (Verified: computed over raw/2026-10-07…raw/2026-11-02)
5. **Added 2026-11-02: separate tenor from holding time before crediting either.** All four of this session's
   later-dated winners were closed inside **43 minutes** and none was held overnight, so what they share with the
   0DTE losers is the holding period and what differs is the expiry. The testable number is result per contract
   against days-to-expiry at first fill, holding time held constant, which proposal 1 already asks for and
   fifteen positions can now start to answer. (Verified: raw/2026-11-02.json)
