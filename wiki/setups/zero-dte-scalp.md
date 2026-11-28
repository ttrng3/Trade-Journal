# 0DTE scalp

Manual trading buys same-day-expiry calls and puts on SPY, SPXW and TSLA and closes them within the session, often
re-entering the same strike several times. Expiry day leaves no room for a position to come back, so the result is
decided by entry timing and by how many times a losing strike is re-entered.

## Evidence

- **2026-11-27: four strikes, 37 contracts, two green, -$395.00, and NVDA replaces the usual names.** The two
  deep ladders lost **-$1,022.00** (150C **-$612.00** at **twelve** deep, 148C **-$410.00** at **ten**) and the
  two shallow strikes made **+$627.00** (146C **+$374.00** at **five**, SPY 723C **+$253.00** at **two**). The
  page's definition names SPY, SPXW and TSLA as the underlyings of this book; **three** of the four strikes
  here are NVDA, which until this month appeared on the later-dated side.
  See [[mistakes/deep-ladder]]. (Verified: raw/2026-11-27.json)

  **The whole same-day loss was recoverable and the settlement proves it.** Every one of the four strikes
  settled in the money and holding them all would have returned **+$4,232.00** against the **-$395.00** taken.
  This is the first compiled session where the same-day book's loss is entirely a timing result rather than a
  tenor result: the strikes were right, the exits were not.
  See [[what-ifs/exit-before-the-close]]. (Verified: raw/2026-11-27.json)

- **2026-11-25: six strikes, 32 contracts, three green, -$679.00 — and the loss is all in the deep ladders.**
  The three that went seven or eight contracts deep lost **-$1,057.00** (TSLA 372.5C **-$465.00**, QQQ 603P
  **-$450.00**, NVDA 148C **-$142.00**); the three that stopped at five or fewer made **+$378.00** (QQQ 611P
  **+$142.00**, QQQ 610P **+$138.00**, NVDA 143C **+$98.00**). QQQ ran both shapes inside ten minutes, an
  eight-deep **603P** that lost and a five-deep **610P** that made money.
  See [[mistakes/deep-ladder]]. (Verified: raw/2026-11-25.json)

  No bars file was delivered for this session, so none of these exits is scored against the bell and the two
  dumps among them are not scored against settlement either. The strikes are compiled; the what-ifs are not.
  (Verified: raw/2026-11-25.json, sources.bars = missing)

- **2026-11-24: three strikes, seven contracts, two green, -$79.00 — and all three exits beat the bell.** SPY
  11-24 718C **+$99.00** on one contract (**2.07 → 3.06**, 09:34:14 → 09:43:23), QQQ 11-24 635P **+$39.00** on one
  (**2.28 → 2.67**, bought and sold inside **14 seconds**, the shortest hold compiled), and SPY 11-24 715P
  **-$217.00** over five, which is the whole of the loss. SPY closed **718.79** and QQQ **638.12**, so both puts
  settled worthless and the 718C was worth **$79.00** held against the **$306.00** taken: the three strikes took
  **$1,316.00** against **$79.00** of held-to-close value, **+$1,237.00** for exiting.
  See [[what-ifs/exit-before-the-close]].

  The 715P is also an instance of [[mistakes/dump-below-the-ladder]] — four contracts bought **2.38** down to
  **1.72** and sold together at **1.46** — and it is the third consecutive session in which the same-day book is
  small and roughly flat while the result is decided elsewhere. Here "elsewhere" is one day out: the four NVDA
  11-25 strikes took **30** contracts for **-$255.00**, four times the same-day book's size.
  (Verified: raw/2026-11-24.json)
- **2026-11-23: three strikes, 17 contracts, all three green, +$180.00 — and irrelevant to the session.** The
  same-day book made **+$180.00** on a day the account took **+$18,160.00** in cash: SPY 11-23 726C **+$97.00**
  over **12** contracts and seven cycles, SPY 11-23 722C **+$54.00** on one and TSLA 11-23 387.5P **+$29.00** on
  four. It is the first all-green same-day session since 2026-10-30 and the first put traded since 2026-11-13.
  All of the session's result is carry. See [[days/2026-11-23]] and [[setups/later-expiry-swing]].
  (Verified: raw/2026-11-23.json)
- **2026-11-23: the 726C is the page's cleanest re-entry sequence, and the add-down leg is still the losing
  half.** Seven one-contract round trips between **10:49:53** and **11:34:50** returned **+$179.00**, every one
  green. Then five contracts were laddered **1.55 → 0.74** between 11:35:58 and 11:42:32 and taken off together
  at **11:50:22** at **0.98** for **-$82.00**. Same strike, same hour, same underlying: scalped one at a time it
  made money seven times out of seven, and laddered downward it lost. The exit price cleared the two cheapest
  buys, so it is not an instance of [[mistakes/dump-below-the-ladder]] — the first full-position one-fill exit
  compiled that does. (Verified: raw/2026-11-23.json)
- **2026-11-20: the same-day book was the least bad part of the worst-but-one session.** Four same-day strikes
  realized **-$5.00** on closed contracts and **+$194.00** in session cash, two green and two red, on a day the
  account gave up **-$3,195.00**. SPY 11-20 720C made **+$139.00**, SPXW 7300C **+$40.00**, SPY 714C lost
  **-$15.00** and SPY 729C **-$169.00**. All four settled worthless and all four were exited, so none of the
  loss came from holding to the bell. See [[days/2026-11-20]] and [[setups/later-expiry-swing]].
  (Verified: raw/2026-11-20.json; computed over data/fills/2026-11.json)
- **2026-11-20: SPY 11-20 720C is the session's control, and it is the same control 2026-11-13 produced.** Four
  contracts laddered down 1.49 → 1.17 and sold in **three** separate fills at 1.52, 1.70 and 1.76 for
  **+$139.00** — the day's only strike sold above its own ladder and its only clear winner. SPY 714C and 729C
  were same-day calls on the same underlying in the same hour, each closed in one fill below its buy, each red.
  Same setup, same morning, three exits against one. (Verified: raw/2026-11-20.json)
- **2026-11-13: four same-day strikes, one green, -$1,003.00, and every loser closed by a single dump fill.**
  NVDA 165C **-$360.00** on ten contracts, NVDA 162.5C **-$348.00** on nine, META 635C **-$197.00** on six and
  SPY 751P **-$98.00** on three; the fifth same-day strike, NVDA 167.5C, closed Thursday's carry and so is not a
  round trip. All five were sold below every buy in their own ladder. This page has penalised add-down since
  2026-10-07 without ever finding it losing on a completed round trip, and the separation is now explicit: the
  ladder is not what loses, the exit taken at the bottom of it is.
  See [[mistakes/dump-below-the-ladder]] and [[days/2026-11-13]]. (Verified: raw/2026-11-13.json)
- **2026-11-11: three same-day strikes, two green, -$841.00, and the whole loss is one strike.** SPXW 7635C lost
  **-$1,125.00** on **19** contracts — the joint third heaviest same-day position compiled — while NVDA 175C
  returned **+$187.00** on eleven and NVDA 172.5C **+$97.00** on one. The SPXW ladder ran **2.60** down to
  **0.55**, a **78.8%** fall and the deepest compiled, and **13** of the 19 went out in one fill at **0.60**.
  The six bought back afterwards at 0.55–0.75 and sold at 0.85–0.90 made **+$150.00**.
  See [[days/2026-11-11]]. (Verified: raw/2026-11-11.json)
- **2026-11-11 and 2026-11-12 both break the entry-time cut proposed on 2026-11-02, per session.** On 2026-11-11
  the one loser of six strikes was opened **09:39:51**, second of the day; on 2026-11-12 the only red line was
  opened **15:30:47** and was a carry rather than a round trip. The aggregate cut survives and is now the
  strongest read on this page — across every compiled session strikes first filled **before 10:00** are **34
  green of 42**, **81.0%**, for **+$2,785.00**; **10:00–11:00** are **14 of 26**, **53.8%**, for **-$966.00**;
  and **after 11:00** are **8 of 18**, **44.4%**, for **-$1,287.00**. Monotonic in both green rate and net across
  three buckets and **86** round trips. (Verified: computed over raw/2026-10-07…raw/2026-11-13)
- **2026-11-12: one same-day strike, green, +$183.00, and the only 0DTE strike compiled that was re-opened in the
  last hour.** SPY 756C took one contract at 09:34:05 at 1.60 out at 2.73 three minutes later, then three more
  at 15:06:47–15:18:10 at 1.72–1.30 sold a minute after the last at 1.74. SPY settled **$1.20** in the money, so
  the four contracts were worth **$480.00** held against **$795.00** taken. See [[days/2026-11-12]].
  (Verified: raw/2026-11-12.json)
- **2026-11-10: the first session compiled with no same-day strike at all.** Sixty fills across three strikes, all
  of them 1, 2 or 8 days out, so this page takes nothing from the session and the four-session gap in its series
  2026-11-03 to 2026-11-09 is joined by a fifth day that genuinely traded none.
  See [[days/2026-11-10]]. (Verified: raw/2026-11-10.json)
- **2026-11-03 to 2026-11-09 were not blank after all, and this page cannot use them.** The export filed on
  2026-11-15 added **404** fills for 2026-11-03 to 2026-11-06, days whose `raw/` files were frozen with no fills
  on the runs of 2026-11-04 to 2026-11-09. Those fills are in `data/fills/2026-11.json` and will never reach a
  day page, so the same-day strikes among them are absent from every count on this page. This is the fourth
  instance of the freeze-then-file problem, after 2026-10-12 to 2026-10-15 and 2026-10-27 to 2026-10-28.
  (Verified: computed over data/fills/2026-11.json; raw/2026-11-03.json, raw/2026-11-04.json,
  raw/2026-11-05.json, raw/2026-11-06.json)
- **2026-11-02: the worst 0DTE session compiled, -$1,867.00 over eight strikes, and the heaviest same-day book.**
  Only **1** of the eight was green. **93** contracts went through the book — more than the 71 of 2026-10-23 and
  the 70 of 2026-10-22, the two previous heaviest — carrying **$12,366.00** of cost for **$10,499.00** of
  proceeds, a **15%** bleed. It is **2.3×** the previous worst session, **-$806.00** on 2026-10-22, and it ends a
  four-session green run. (Verified: raw/2026-11-02.json; computed over raw/2026-10-07…raw/2026-11-02)
- **2026-11-02: this session turned the page's whole compiled history negative.** The running net went
  **+$1,713.00** → **-$154.00**, the first sign change in six sessions, and the green rate fell **66.7%** →
  **58.5%** after five consecutive rises. One session removed **$1,867.00** from a total that had taken twelve
  sessions to build to $1,713.00, which puts this book's net in the same position
  [[what-ifs/exit-before-the-close]] reached on 2026-10-21: not a statistic at this sample size.
  (Verified: computed over raw/2026-10-07…raw/2026-11-02)
- **2026-11-02: the loss is the clock, not the strike.** Every same-day strike opened after **10:16:11** lost —
  SPY 763C **-$227.00**, SPXW 7680C **-$430.00**, SPY 761C **-$349.00**, SPXW 7675C **-$125.00**, SPXW 7660C
  **-$120.00**, QQQ 693C **-$335.00**, SPXW 7645C **-$345.00**, seven for **-$1,931.00** — while the one strike
  opened in the first three minutes, SPY 760C, returned **+$64.00** over two and a half hours and **30** fills.
  The five positions opened before 10:16:11 were all green for **+$1,409.00**, four of them later-dated. Entry
  time has not been separated from result on this page before and it cuts this session completely.
  (Verified: raw/2026-11-02.json)
- **2026-11-02: the SPX book is over half the loss and the second SPX-heavy session is as bad as the first.**
  Four SPXW strikes returned **-$1,020.00** of the **-$1,867.00** on **31** contracts, against **-$885.00** over
  five strikes on 2026-10-22. SPXW 7680C, **-$430.00** on eleven contracts bought 10:52:14–11:10:44 and closed
  by 11:23:06, is the session's largest single loss and a **32%** give-back on premium held for minutes. Both
  SPX-heavy sessions compiled are among the three worst on this page. See [[rules/spx-after-1200]].
  (Verified: raw/2026-11-02.json, raw/2026-10-22.json)
- **2026-11-02: re-entry failed as a tell for the seventh session running, and in the most direct way yet.** The
  single green strike, SPY 760C, took **10** buy fills after its own first exit — the most re-entered position of
  the session — while SPXW 7675C took **none**, was closed in one fill four contracts at a time, and lost
  **-$125.00**. The 2026-10-07 and 2026-10-08 shape, heavy re-entry on the losers, has now failed on six of the
  last seven sessions. (Verified: raw/2026-11-02.json)
- **2026-11-02: size still predicts nothing, now across six readings.** The heaviest same-day strikes compiled are
  **22**, **20**, **19**, **19**, **16** and **16** contracts returning **-$45.00**, **+$79.00**, **+$411.00**,
  **+$64.00**, **+$188.00** and **-$349.00** — three green, one near flat, two red, and this session supplied both
  a 19-contract winner and a 16-contract loser. (Verified: computed over raw/2026-10-07…raw/2026-11-02)
- **2026-10-30: four strikes, four green, +$579.00, and the deepest add-down compiled.** Fourteen TSLA 395 calls
  were bought in **5m 28s** down a ladder from 1.73 to **0.65** for **$1,473.00** and all fourteen sold for
  **$1,678.00**, **+$205.00**; eight TSLA 392.5 calls returned **+$267.00**, SPY 761C **+$61.00** and SPY 760P
  **+$46.00**. The whole book was opened and closed between 09:30:50 and 10:51:50. It is the sixth session of
  twelve in which every same-day strike was green, and the second running.
  (Verified: raw/2026-10-30.json; computed over raw/2026-10-07…raw/2026-10-30)
- **2026-10-30: the add-down reading finally has a counterweight, and it is not on the round trip.** The
  fourteen-contract ladder made money on the scalp and lost **-$5,084.00** against the settlement, because TSLA
  ran to **399.83** and left the strike **$4.83** in the money. Add-down has still never lost on a round trip in
  the compiled set; what the ladder selects for is strikes that keep running after the exit, which this page
  cannot see and [[what-ifs/exit-before-the-close]] can. (Verified: raw/2026-10-30.json)
- **2026-10-29: three strikes, three green, +$395.00, all closed by 11:07.** QQQ 713P **+$329.00** over nine
  contracts in **42 minutes**, SPY 768C **+$61.00** over four and SPY 768P **+$5.00** over one. The session's
  losses were all in next-day expiry, not here, and the two strikes that lost were the two that were not flat at
  the bell. See [[mistakes/overnight-0-1-dte]]. (Verified: raw/2026-10-29.json)
- **2026-10-26: two strikes, both green, +$324.00, and the narrowest book compiled.** Seventeen contracts across
  SPY 764C (**+$246.00** on 15) and NVDA 215C (**+$78.00** on 2), on two underlyings against Friday's five. It is
  the fifth session of the ten in which every same-day strike was green, and the first since 2026-10-21 on which
  the book's running sign held rather than flipped.
  (Verified: raw/2026-10-26.json; computed over raw/2026-10-07…raw/2026-10-26)
- **2026-10-26: the one add-down of the session was the clearest compiled, and it cost nothing.** Six of the
  fifteen SPY 764C contracts were bought in **96 seconds** between 10:31:38 and 10:33:14 on a falling ladder —
  1.64, 1.64, 1.61, 1.54, 1.51, 1.45 for **$939.00** — at the highest premiums paid all day, then all six were
  sold between 10:34:00 and 10:36:12 at 1.62–1.79 for **$1,010.00**, **+$71.00** inside five minutes. The shape
  this page has penalised since 2026-10-07 is re-entering a strike at a worse price; here the worse price was
  paid deliberately and recovered immediately, so the mechanism is not the ladder but how long the position is
  then held. (Verified: raw/2026-10-26.json)
- **2026-10-26: the heaviest-strike reading stays dead.** SPY 764C at 15 contracts is the joint sixth heaviest
  same-day position compiled and returned **+$246.00**. The six heaviest are now 22, 20, 19, 16, 15 and 15
  contracts returning **-$45.00**, **+$79.00**, **+$411.00**, **+$188.00**, **+$540.00** and **+$246.00**: five
  green, one near flat, and still no relationship between size and magnitude.
  (Verified: computed over raw/2026-10-07…raw/2026-10-26)
- **2026-10-26: a strike traded at two expiries at once, both green.** Alongside the 0DTE 764 calls, four SPY
  10-28 764 calls were run from 09:41:12 to 10:11:02 for **+$136.00**. The near leg made more on nearly four
  times the contracts, and the pair is the first clean side-by-side comparison of the two books on one strike —
  the only earlier instance, TSLA 385C on 2026-10-07, left neither leg flat. The later leg belongs to
  [[setups/later-expiry-swing]] and not to this count. (Verified: raw/2026-10-26.json, raw/2026-10-07.json)
- **2026-10-23: the best 0DTE session compiled, +$967.00 over eleven strikes, the day after the worst.** Eight of
  the eleven were green, 71 contracts in all, and the swing from **-$806.00** to **+$967.00** in one session is
  **$1,773.00** — larger in magnitude than any single session's result before it. The book went from **-$552.00**
  to **+$415.00**, the fifth consecutive update on which the sign of that total has changed.
  (Verified: raw/2026-10-23.json; computed over raw/2026-10-07…raw/2026-10-23)
- **2026-10-23: the heaviest strike won again, and this time so did the second heaviest.** TSLA 375C took **15**
  contracts for **+$540.00**, the day's best, and SPY 761C took **14** for **-$54.00**. Across every compiled
  session the five heaviest 0DTE strikes are now 22, 20, 19, 16 and 15 contracts returning **-$45.00**,
  **+$79.00**, **+$411.00**, **+$188.00** and **+$540.00**: four green, one flat, and no relationship between
  size and magnitude. Size has now failed to predict the result in both directions often enough that it should be
  dropped as a read. (Verified: computed over raw/2026-10-07…raw/2026-10-23)
- **2026-10-23: re-entry count did not pick the loser.** The two most re-entered strikes, 15 and 14 contracts,
  returned +$540.00 and -$54.00, while the day's worst, TSLA 372.5C at **-$281.00**, took five contracts and was
  closed in a single exit six minutes after the last buy. The 2026-10-07 and 2026-10-08 shape — heavy re-entry on
  the losers — has now failed on five of the last six sessions. (Verified: raw/2026-10-23.json)
- **2026-10-23: the same-day book spread across five underlyings, the widest compiled.** TSLA four strikes, SPY
  three, SPXW two, META one, NVDA one. The TSLA book made **+$598.00** and the SPY book lost **-$136.00**; SPXW
  returned **+$285.00** and the two single-strike names **+$220.00** between them. All eleven were opened and
  closed inside the session. The session's sixth underlying, AAPL, was a 10-30 contract and is not in this book.
  (Verified: raw/2026-10-23.json)
- **2026-10-22: the worst 0DTE session compiled, -$806.00 over six strikes, and the first SPX-heavy one.** Five
  SPXW strikes returned **-$885.00** and the one SPY strike **+$79.00**. It ends the five-session green run and it
  is larger than 2026-10-07's **-$729.00**. (Verified: raw/2026-10-22.json)
- **2026-10-22: the loss is turnover, not direction.** The five SPX strikes carried **$7,260.00** of premium and
  gave back **-$885.00** — a 12% bleed on money that was in the market for minutes. The worst, 7690C, was bought
  across four minutes and closed 15 minutes later for **-$505.00**; 7680C's last buy at 14:02:05 was followed by
  its first sell 16 seconds later. Re-entering the same expiring strike at a worse price is the mechanism.
  (Verified: raw/2026-10-22.json)
- **2026-10-22 breaks the "heaviest strike wins" reading of 2026-10-19 and 2026-10-20.** The two heaviest 0DTE
  strikes ever compiled are now this session's SPXW 7710C at **22** contracts for **-$45.00** and SPY 767C at
  **20** contracts for **+$79.00** — both within $80 of flat. The four heaviest are 22, 20, 19 and 16 contracts
  returning **-$45.00**, **+$79.00**, **+$411.00** and **+$188.00**, so size now predicts neither sign nor
  magnitude. Both the 2026-10-07 claim and its 2026-10-19 counterclaim are dead.
  (Verified: computed over raw/2026-10-07…raw/2026-10-22)
- 2026-10-21: one same-day strike, green, **+$67.00** on two contracts of SPY 769C, bought and sold inside 21
  minutes. The smallest session compiled, and the fifth green one in a row. (Verified: raw/2026-10-21.json)
- 2026-10-21: size and result moved together again, in the other direction — the smallest position of the five
  green sessions produced the smallest gain, while the same strike held to settlement was worth **+$529.00**.
  See [[what-ifs/exit-before-the-close]]. (Verified: raw/2026-10-21.json)
- 2026-10-20: two same-day strikes, **both green**, **+$462.00** — the best 0DTE session compiled. SPY 768C took 19
  contracts for +$411.00 and SPY 766C two for +$51.00. (Verified: raw/2026-10-20.json)
- 2026-10-19: one same-day strike, green, **+$188.00** on 16 contracts of SPY 767C, round-tripped in six clusters
  across the session. (Verified: raw/2026-10-19.json)
- **2026-10-19 and 2026-10-20 break the size correlation.** The most re-entered strike of each session — 16 buy
  fills, then 19 — was the session's biggest winner. With 2026-10-16 that is three consecutive counterexamples to
  the 2026-10-07 and 2026-10-08 pattern where the most re-entered strikes lost. Across all compiled days the three
  heaviest 0DTE strikes are now 19, 16 and 7 contracts, and the first two are the two largest wins.
  (Verified: computed over raw/2026-10-07…raw/2026-10-20)
- 2026-10-16: two same-day strikes, **both green**, the first clean 0DTE day compiled. QQQ 720P round-tripped
  5-for-5 at **+$127.00**; TSLA 377.5C took **$378.00** of buys and **$524.00** of sells but closed a contract
  carried in from earlier in the week, so it is **+$146.00** of net cash rather than a round trip. Net cash across
  the two strikes was **+$273.00**. (Verified: raw/2026-10-16.json)
- 2026-10-16: re-entry did not pick the loser this time. Six buy fills on TSLA and five on QQQ, and both strikes
  ended green — the opposite of 2026-10-07 and 2026-10-08, where the most re-entered strikes were the ones that
  lost. The size-is-the-tell correlation now has a counterexample.
  (Verified: computed over raw/2026-10-07…raw/2026-10-16)
- 2026-10-16: the day's realized result is not the interesting number. The QQQ put settled **$10.14** in the money
  after being sold at 1.18–1.94, so the same five contracts held to expiry were worth **$5,070.00** against the
  **$766.00** taken. See [[what-ifs/exit-before-the-close]]. (Verified: raw/2026-10-16.json)
- 2026-10-12 to 2026-10-15: no same-day-expiry trade is recorded on any of the four days. Those raw days were
  frozen before Ty's export arrived, so the fills the shard now holds for them are not in `raw/` and cannot be
  compiled. (Verified: computed over raw/2026-10-12…raw/2026-10-15; data/fills/2026-10.json)
- 2026-10-09: three same-day contracts round-tripped for **+$21.00** — SPY 776C +$94.00, TSLA 387.5C +$25.00, QQQ 750P
  -$98.00 — and trading stopped at 11:20:03, before midday. The session's real gain was a later-expiry position, not
  these. (Verified: raw/2026-10-09.json)
- 2026-10-08: four same-day contracts round-tripped for **+$118.00**, three of them winners, the first positive 0DTE
  day compiled. Size was small: 1, 1, 5 and 2 contracts against the 3-to-7 of 2026-10-07.
  (Verified: raw/2026-10-08.json)
- 2026-10-07 to 2026-10-09: across the three compiled days, 13 same-day-expiry contracts round-tripped inside the week
  for **-$615.00** with 5 winners. The one eight-day contract traded in the same period returned +$753.00, so the
  same-day book is where the week's losses sit. (Verified: computed over raw/2026-10-07…2026-10-09)
  See [[setups/later-expiry-swing]].
- 2026-10-08: re-entry stayed heavy on the losers and light on the winners. TSLA 10-09 380C took 7 buy fills and lost
  -$213.00, while the three SPY winners took 1, 1 and 5. That is the same shape as 2026-10-07.
  (Verified: raw/2026-10-08.json)
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

**Added 2026-11-27, counting 2026-11-27.** Same-day strikes bought and sold in equal size stand at **80 strikes,
568 contracts, 46 green, -$2,624.00**, seen on **21** of **37** compiled days. The new session returned
**-$395.00** (4 strikes, 37 contracts, 2 green) and the green rate goes **57.9% → 57.5%**, its eleventh reading:
52.0%, 58.3%, 60.5%, 63.4%, 66.7%, 58.5%, 55.7%, 58.2%, 58.6%, 57.9%, **57.5%**. Eleven readings sit inside
**14.7** points and the last six inside **2.9**, so this is the steadiest series the wiki keeps.
(Verified: computed over raw/2026-10-07…raw/2026-11-27)

**The depth decomposition still accounts for the headline exactly, and both halves grew.** Same-day strikes that
went six or deeper are **30** strikes, **36.7%** green, **-$4,260.00**; those at five or fewer are **50**
strikes, **70.0%** green, **+$1,636.00**. The shallow same-day book has now been profitable across **37**
sessions and improved by **$627.00** on a session the book lost money, which is the cleanest statement of this
page's finding yet: the loss is not expiry day, it is depth on expiry day.
See [[mistakes/deep-ladder]]. (Verified: computed over raw/2026-10-07…raw/2026-11-27)

**What is new is that this session's loss was not a tenor cost at all.** All four strikes settled in the money
and holding the book would have returned **+$4,232.00**. Across the compiled set this page's **-$2,624.00** is
smaller than that one session's foregone gain, so the same-day book's whole recorded loss is now less than what
a single session left on the table by exiting early. Expiry day removes the room to be wrong; it did not remove
the move here. See [[what-ifs/exit-before-the-close]].
(Verified: raw/2026-11-27.json; computed over raw/2026-10-07…raw/2026-11-27)

**Added 2026-11-25, counting 2026-11-25.** Same-day strikes bought and sold in equal size stand at **76 strikes,
531 contracts, 44 green, -$2,229.00**, seen on **20** of **36** compiled days. The new session returned
**-$679.00** (6 strikes, 32 contracts, 3 green), the book's worst session since 2026-11-13, and the green rate
goes **58.6% → 57.9%**, its tenth reading: 52.0%, 58.3%, 60.5%, 63.4%, 66.7%, 58.5%, 55.7%, 58.2%, 58.6%,
**57.9%**. Ten readings sit inside **14.7** points and the last five inside **2.9**.
(Verified: computed over raw/2026-10-07…raw/2026-11-25)

**The page's headline number has an explanation now, and it is not expiry day.** Split by how deep the ladder
was allowed to get before anything was sold, the **-$2,229.00** decomposes exactly: same-day strikes that went
six or deeper are **28** strikes, **39.3%** green, **-$3,238.00**, and same-day strikes that stayed at five or
fewer are **48** strikes, **68.8%** green, **+$1,009.00**. The shallow same-day book is profitable across
**36** sessions. What this page has been measuring as a tenor effect is, on the compiled set, a depth effect
inside a tenor. See [[mistakes/deep-ladder]].
(Verified: computed over raw/2026-10-07…raw/2026-11-25)

That does not clear same-day expiry. Depth hurts more here than it does on later dates — **-$115.64** a strike
against **+$26.15** for deep later-dated strikes — so expiry day is where the shape is expensive, and three
sessions ago this page recorded that the one-day-out book was four times the size of the same-day book and three
times the loss. The ordering to keep is that depth and tenor are both real and the losing corner is their
intersection. (Verified: computed over raw/2026-10-07…raw/2026-11-25)

**Size as a count of contracts still predicts nothing.** The 2026-11-02 reading retired it and this session
agrees in isolation: the **32** contracts here returned **-$679.00** while the **17** of 2026-11-23 returned
**+$180.00**, but the **8** of 2026-11-20 returned **+$164.00** and the **93** of 2026-11-02 were the page's
largest session. The cut that works is not how many contracts a session traded, it is how many were open on one
strike at one time. (Verified: computed over raw/2026-10-07…raw/2026-11-25)


**Added 2026-11-24, counting 2026-11-24.** Same-day strikes bought and sold in equal size stand at **70 strikes,
499 contracts, 41 green, -$1,550.00**, seen on **19** of **35** compiled days. The new session returned
**-$79.00** (3 strikes, 7 contracts, 2 green), so the net falls after two rises, and the green rate goes
**58.2% → 58.6%**, its ninth reading: 52.0%, 58.3%, 60.5%, 63.4%, 66.7%, 58.5%, 55.7%, 58.2%, **58.6%**. Nine
readings now sit inside **14.7** points and the last four inside **2.9**.

**Three consecutive sessions where this book is small and not where the money is.** 2026-11-20 **+$194.00** in
cash, 2026-11-23 **+$180.00**, 2026-11-24 **-$79.00** — **$453.00** of range across three sessions whose results
were **-$3,195.00**, **+$15,175.00** and **+$375.00**. The page's 2026-11-23 note said the attention these pages
give the 0DTE book is out of proportion to **$1,471.00**; it is now out of proportion to **$1,550.00**.

**What is worth keeping from this session is the tenor boundary, not the 0DTE total.** Seven same-day contracts
returned **-$79.00** while **30** contracts one day out returned **-$255.00** and **10** contracts 24 and 52 days
out returned **+$216.00**. The one-day-out book is not on this page and is not a swing either, and on this
session it was four times the size of the same-day book and three times the loss.
See [[setups/later-expiry-swing]]. (Verified: computed over raw/2026-10-07…raw/2026-11-24)

**Added 2026-11-24, counting 2026-11-20 and 2026-11-23.** Same-day strikes bought and sold in equal size stand at
**67 strikes, 492 contracts, 39 green, -$1,471.00**, seen on **18** of **34** compiled days. The two new sessions
returned **+$164.00** (3 strikes, 8 contracts, 2 green) and **+$180.00** (3 strikes, 17 contracts, 3 green), so
the net has risen twice after three consecutive falls, and the green rate goes **55.7% → 58.2%**. The series now
reads 52.0%, 58.3%, 60.5%, 63.4%, 66.7%, 58.5%, 55.7%, **58.2%**, an eight-reading spread of 14.7 points around
a net that has swung **$1,867.00** in one session. Both new sessions are small: **25** contracts between them
against **93** in 2026-11-02 alone.

The page's standing finding — that size predicts neither sign nor magnitude — is untouched, and a sharper one
now sits beside it. On 2026-11-23 the same-day book was **+$180.00** while the later-expiry carry was
**+$14,931.00**, and on 2026-11-20 it was **+$194.00** in cash while the later-expiry book was **-$3,389.00**.
Two consecutive sessions where the same-day book is small and roughly flat and the whole result is decided
elsewhere. The 0DTE book has returned **-$1,471.00** over **34** compiled days; it is not where this account
makes or loses money, and the attention it gets on these pages is out of proportion to **$1,471.00**.
See [[setups/later-expiry-swing]].
(Verified: computed over raw/2026-10-07…raw/2026-11-23)

Seen on 13 of 19 compiled days. Counting only same-day strikes bought and sold in equal size: **53 strikes, 404
contracts, 31 green, -$154.00**. By day those round trips returned **-$729.00, +$118.00, +$21.00, +$127.00,
+$188.00, +$462.00, +$67.00, -$806.00, +$967.00, +$324.00, +$395.00, +$579.00** and **-$1,867.00** — four
consecutive rises, then a single session larger in magnitude than any before it, which took the net negative over
the page's whole history. The strike count moved the same way for the first time: **31 green of 53**, **58.5%**,
after 52.0% → 58.3% → 60.5% → 63.4% → 66.7%, five rises and then an 8.2-point fall. **93** of the 404 contracts
belong to this one session, the heaviest same-day book compiled, and **7 of its 8** strikes lost.

Two strikes are excluded because they closed or left a carried position rather than round-tripping — TSLA 10-07
385C and TSLA 10-16 377.5C — and a third, TSLA 10-23 387.5C, closed Thursday's carry on 2026-10-23 and belongs to
[[setups/later-expiry-swing]]. The four sessions 2026-10-12 to 2026-10-15 contribute nothing: their raw days were
frozen with no fills, as were 2026-10-27 and 2026-10-28, whose **63** fills reached the repo after those days were
already written. (Verified: computed over raw/2026-10-07…raw/2026-11-02; late fill counts computed over
data/fills/2026-10.json)

**Added 2026-11-17, counting 2026-11-11 to 2026-11-13.** Same-day strikes bought and sold in equal size now stand
at **61 strikes, 467 contracts, 34 green, -$1,815.00**, seen on **16** of **28** compiled days. The three new
sessions returned **-$841.00**, **+$183.00** and **-$1,003.00**, so the net has fallen for a second and third
consecutive update after 2026-11-02's **-$1,867.00** single-session drop, and the green rate has gone **58.5%** →
**55.7%**, its second fall and its lowest reading since 2026-10-08. As the page's own 2026-11-02 note says, the
net is not the number to report; strikes green of strikes traded is, and that series now reads 52.0%, 58.3%,
60.5%, 63.4%, 66.7%, 58.5%, **55.7%**.

The heaviest same-day strikes compiled are now **22**, **20**, **19**, **19**, **19** and **16** contracts
returning **-$45.00**, **+$79.00**, **+$411.00**, **+$64.00**, **-$1,125.00** and **+$188.00** — the new
19-contract entry, SPXW 7635C on 2026-11-11, is the largest loss any heavy strike has produced, which leaves size
predicting neither sign nor magnitude for the eighth consecutive reading.

**The real finding of this week is not on this page.** Ten exits across 2026-11-10 to 2026-11-13 closed a whole
add-down position below every buy in it, and all ten lost, for **-$5,440.00** on the legs. That cuts the week far
more cleanly than size, re-entry count, underlying or tenor ever have, and it is now tracked separately at
[[mistakes/dump-below-the-ladder]]. (Verified: computed over raw/2026-10-07…raw/2026-11-13)

## What to do about it
Proposals only. The number to carry forward is round trips per strike against result per strike, because on this day
the four most re-entered strikes were all losers while the least re-entered was the winner. That is one day and could
easily be noise, so the useful action now is to keep the count rather than change the approach. The post-exit paths
for the same session were close to even, 16 of 28 continuing the trade's way, so this is not yet evidence that exits
were early.

Three days in, the pattern that survives is size rather than direction: the two positive 0DTE days were the two small
ones, 4 and 3 contracts, and the one heavy day, 7 contracts with 3-to-7 re-entry per strike, is the whole of the
-$615.00. That is still a correlation across three days and not a tested rule.
(Verified: computed over raw/2026-10-07…2026-10-09)

**Added 2026-11-02: record entry time per strike and read this book on it.** Entry time is the only cut that has
separated a whole session: every same-day strike opened after **10:16:11** lost, seven for **-$1,931.00**, and the
five positions opened before it were all green for **+$1,409.00**. Size, re-entry count and underlying have each
failed as reads across the compiled set; this one has one session behind it and is therefore a measurement to
start, not a rule to adopt. The number to keep is the time of a strike's first fill against its result.
(Verified: raw/2026-11-02.json)

**Added 2026-11-02: stop reporting this page's net, as [[what-ifs/exit-before-the-close]] already decided for
its own.** The total has read **-$275.00**, **+$187.00**, **+$254.00**, **-$552.00**, **+$415.00**, **+$739.00**,
**+$1,134.00**, **+$1,713.00** and **-$154.00** on nine consecutive updates, changing sign four times, and one
session has now moved it by **$1,867.00**. Report strikes green of strikes traded and the two tails.
(Verified: computed over raw/2026-10-07…raw/2026-11-02)
