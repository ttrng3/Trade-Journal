# Dump below the ladder

Closing a whole add-down position in a single fill priced below every buy in it. The ladder is built down, the last
add is made, and then the entire position is sold at once at a price under even the cheapest contract in it, so the
averaging-down is paid for twice: once on the way down and again on the exit. It is distinct from
[[setups/zero-dte-scalp]], which asks whether the strike should have been traded, and from
[[mistakes/overnight-0-1-dte]], which is about what happens when a ladder is *not* closed. Here the ladder is
closed, immediately, at the worst available price.

The test is mechanical: a sell fill that takes at least half the open position, at a premium below the minimum buy
premium of the lots it closes.

## Evidence

- **2026-11-27: two instances, 22 contracts, -$980.00, and the first session where the two disagree about
  whether the dump was the error.** Both are full-position one-fill exits below their own floor, both same-day
  expiry, both NVDA. The **150C** took **12** contracts at **0.4800** at 09:47:02 against a **0.75** floor
  (**-36.0%**), **-$612.00**, **61** seconds after the last add; the **148C** took **10** at **0.6400** at
  10:05:18 against **0.78** (**-17.9%**), **-$368.00** on the dumped leg, **283** seconds after the last add.
  (Verified: raw/2026-11-27.json)

  **This session has bars, so both were scored at once, and they split.** NVDA closed **150.04**. The 150C
  settled **$0.04** in the money, so dumping **36.0%** below the floor still beat holding by **+$528.00**; the
  148C settled **2.04** in the money, so dumping on the better terms gave up **+$1,400.00**. Every same-day
  instance scored before this session fell on the "dump beats holding" side of the 2026-11-23 split. One no
  longer does, and it is the one that was dumped less badly. What decides it is where the close lands relative
  to the strike, which the exit price does not know.
  (Verified: raw/2026-11-27.json; see [[what-ifs/exit-before-the-close]])

  The **-36.0%** is the deepest discount since this count began on 2026-11-10, past the **-30.3%** of
  2026-11-25. Two deeper ones sit in the raw files outside the counted window: **-48.3%** on 2026-10-07
  (TSLA 385C, 9 contracts) and **-47.4%** on 2026-10-22 (SPXW 7690C, 7 contracts).
  (Verified: computed over raw/2026-10-07…raw/2026-11-27)

  **A third ladder, twice as deep, did not trip the test and did not lose.** NVDA 12-04 160C went **fifteen**
  deep and was taken off one contract at a time across **4 hours 21 minutes** for **+$194.00** realized. The
  page's shape is the one-fill exit, not the ladder, and this session is the clearest evidence of that it has:
  the deepest ladder of the day was the profitable one. See [[mistakes/deep-ladder]].
  (Verified: raw/2026-11-27.json)

- **2026-11-25: two instances, 16 contracts, -$915.00, and the two fastest gaps the page has recorded.** Both are
  full-position one-fill exits below the floor of their own ladder, both same-day expiry. TSLA 11-25 372.5C,
  **8** contracts at **0.4813** at 09:45:00 against a **0.69** floor (**-30.3%**), **-$465.00**, **85** seconds
  after the last add; QQQ 11-25 603P, **8** at **1.07** at 09:55:22 against **1.24** (**-13.7%**), **-$450.00**,
  **45** seconds after the last add. The QQQ ladder was built and gone inside **2 minutes 55 seconds** start to
  finish. (Verified: raw/2026-11-25.json)

  The **-30.3%** is the deepest discount since this count began on 2026-11-10, against the **-1.0%** to
  **-28.9%** range the 2026-11-20 block recorded. It is not the deepest in the raw files: a **-47.4%**
  full-position exit on 2026-10-22 (SPXW 7690C, 7 contracts) predates the counted window.
  (Verified: computed over raw/2026-10-07…raw/2026-11-25)

  **A third ladder of the same size lost without tripping the test.** NVDA 11-25 148C went **seven** deep,
  **1.43** down to **0.54**, and left in one fill at **0.73** — above its own floor, so the test correctly does
  not count it, and it still lost **-$142.00**. The three deepest ladders of the session were its only three
  losers, which is the question this page has been asking from the other end since 2026-11-23. It now has its own
  page: [[mistakes/deep-ladder]]. (Verified: raw/2026-11-25.json)

  **The three NVDA legs this page left open are now scored.** The 2026-11-24 block said nothing would be claimed
  about NVDA 11-25 160C, 162.5C and 165C until this run priced them. There is no bars file for 2026-11-25, but
  NVDA's own same-day options bound it: the 143C was bought at **1.87** at 09:43:21, and a call cannot trade
  below intrinsic, so NVDA was at or below **144.91** at that moment. The three strikes needed **160.00** or
  better, a rise of at least **10.4%** in the remaining session. All three dumps therefore beat holding to
  expiry, keeping **$2,968.00** of proceeds that would otherwise have settled at zero, and the same is true of
  the **157.5C** that was not dumped. **Of 24 occurrences, 22 are scored and the two new ones are not**: their
  expiry is the session this run compiles, and without bars the close cannot be priced. The same premium trick
  only narrows them. QQQ was at or above **607.47** at 10:16:45, from the 611P sold at **3.53**, so the **603P**
  needed a fall of more than **4.47** points (**0.74%**) over the rest of the session to be worth anything —
  possible, so nothing is claimed. TSLA was at or below **372.98** at 09:45:00, from the dumped call's own price,
  and needed to finish above **372.50**.
  Likely (basis: raw/2026-11-25.json 143C premium at 09:43:21; raw/2026-11-24.json for the strikes and
  proceeds; no bars file for 2026-11-25, so the close is not priced and the bound stops at 09:49:01.)

- **2026-11-24: four instances in 19 minutes, 18 contracts, -$735.00 on the legs — and three of them cannot be
  scored yet.** Every one of them is a full-position one-fill exit below the floor of the lots it closed, FIFO:
  NVDA 11-25 165C, **5** contracts at **1.03** at 09:47:04 against a **1.10** floor (**-6.4%**), **-$188.00**;
  SPY 11-24 715P, **4** at **1.46** at 10:00:17 against **1.72** (**-15.1%**), **-$226.00**; NVDA 11-25 162.5C,
  **4** at **1.09** at 10:04:07 against **1.37** (**-20.4%**), **-$147.00**; NVDA 11-25 160C, **5** at **1.55**
  at 10:05:54 against **1.70** (**-8.8%**), **-$174.00**. All four ladders were built down and taken out whole
  inside the same 19-minute window, and all four lost on the leg.

  The scoring is split by horizon, which is the lesson 2026-11-23 forced onto this page. The SPY put was same-day
  expiry: SPY fell from **719.33** at the dump to **713.80** by 10:30, **$1.20** inside the strike, so holding
  half an hour would have helped — but SPY closed **718.79** and it settled worthless, so the dump beat holding to
  expiry by **$584.00**. The three NVDA legs expire **2026-11-25**, the session after this one. At the
  2026-11-24 close NVDA was **155.48**, leaving **160.00** and **162.50** and **165.00** out of the money by
  **$4.52** to **$9.52** with no intrinsic, but that is not their expiry and nothing is claimed about them until
  the next run prices them.

  The session's own control is on the same underlying in the same hour. NVDA 11-25 157.5C took **10** contracts
  the same way and was never closed in one fill — six sells of one or two between 10:55:33 and 12:10:05 — and
  returned **+$199.00**, while the three NVDA strikes that were dumped returned **-$454.00** on the dumped legs.
  Same underlying, same tenor, same ladder-down entry, opposite exit shape, opposite sign.
  (Verified: raw/2026-11-24.json)
- **2026-11-23 reverses the verdict on 2026-11-20's eight dumps, on the two that can be priced.** Friday's
  instances were scored against Friday's close and all eight were called right. The next session re-prices two of
  them. TSLA 11-25 385C: **6** contracts dumped at **1.01** for **$606.00** at 12:03:28 Friday; the **2**
  contracts of the same strike carried into Monday sold at **5.70** and **9.95**, so those six were worth
  **$3,420.00 to $5,970.00** at prices actually filled — **$2,814.00 to $5,364.00** given up. NVDA 11-25 149C:
  **9** contracts dumped at **0.95** and **0.78** for **$804.00**; NVDA closed Monday at **165.19**, putting
  intrinsic alone at **16.19**, so the nine were worth at least **$14,571.00** — a floor of **$13,767.00** given
  up. See [[days/2026-11-23]] and [[days/2026-11-20]].
  (Verified: raw/2026-11-20.json, raw/2026-11-23.json)
- **The horizon was the whole of the disagreement.** Friday's three same-day dumps settled worthless and nothing
  changes for them; exiting returned the full premium. The five later-expiry dumps had **5** days or **56** left
  and were scored as if they expired at Friday's bell. Of those five, two are priced or bounded above and both
  gave up multiples of what they took; NVDA 01-15 190C, SPY 11-25 728C and SPY 11-20 729C are not traded on
  2026-11-23 and are out of the money at its close, so **nothing is claimed about them** — the 190C in particular
  had **53** days left and a 175C of the same expiry fetched **6.05–8.50** that morning. A dump of a position
  with time left cannot be scored at the session close; it needs the horizon stated with it.
  (Verified: raw/2026-11-20.json, raw/2026-11-23.json)
- **2026-11-23: the first full-position one-fill exit compiled that clears its own floor, so the count does not
  move.** SPY 11-23 726C was laddered **1.55 → 0.74** over five contracts between 11:35:58 and 11:42:32 and all
  five went out at **11:50:22** at **0.98** — the whole position in one fill, **-$82.00**, **470 seconds** after
  the last add. At **0.98** the price is above the **0.93** and **0.74** buys, so it fails the page's mechanical
  test and is **not** an instance. It is the nearest miss recorded and worth keeping: the shape here is the
  one-fill exit, and what the test isolates is the exit *below the floor*, not the one-fill exit itself.
  The count stands at **18**. (Verified: raw/2026-11-23.json)
- **2026-11-20: eight occurrences in one session, all eight red for -$1,888.00, and all eight right.** This is
  the most instances any compiled session holds, one more than 2026-11-13's seven, over **33** contracts:
  **$4,958.00** of cost against **$3,070.00** of proceeds, a **38.1%** bleed. NVDA 01-15 190C **9** contracts at
  **0.90** against a ladder built across three sessions 2.42 → 1.06, **-$639.00**; TSLA 11-25 385C **6** at
  **1.01** against 2.40 → 1.30, **-$412.00**; NVDA 11-25 149C **6** at **0.95** against 1.85 → 1.11,
  **-$286.00**, and then **3** more at **0.78** against 0.95 → 0.83, **-$39.00**; SPY 11-25 728C **5** at
  **1.03** against 1.90 → 1.31, **-$263.00**; SPY 11-20 729C **1** at **0.30** against **1.99**, **-$169.00**;
  SPXW 11-20 7300C **2** at **0.75** against 1.25 → 0.90, **-$65.00**; SPY 11-20 714C **1** at **1.55** against
  **1.70**, **-$15.00**. See [[days/2026-11-20]]. (Verified: raw/2026-11-20.json)
- **2026-11-20 is the page's first counterexample on the exit, and it is unanimous.** On every one of the eight,
  the underlying was lower at the close than at the moment of the dump — NVDA **140.31 → 125.81**, TSLA
  **352.94 → 345.99**, SPY **700.46 → 690.81**, SPX **7,094.2 → 6,908.1** by the SPY × 10 proxy — and the three
  same-day strikes among them all settled worthless. Holding would have lost more in all eight cases. Seventeen
  of the eighteen instances this page has recorded lost money on the leg; this is the first session where that
  loss was unavoidable by the time the sell was made, because the position should not have been there.
  (Verified: raw/2026-11-20.json)
- **2026-11-20 and 2026-11-13 bound the page from opposite ends.** Both are dump-heavy sessions — eight
  instances and seven — and both are among the two worst compiled, **-$3,195.00** and **-$4,006.00**. On
  2026-11-13 the dumps were wrong: META 11-13 635C was sold at 0.72 and settled **$6.99 in the money**,
  **-$3,762.00** against holding. On 2026-11-20 they were right on all eight. The difference is not the exit
  method, which is identical, but what the underlying did afterwards. The cost the page measures is paid when
  the ladder is built downward; whether the sell adds to it or saves money is decided by the tape.
  (Verified: raw/2026-11-20.json, raw/2026-11-13.json)
- **2026-11-13: seven occurrences in one session, all seven red, -$3,597.00 on the dumped legs.** QQQ 11-18 700C
  dumped **17** contracts at **1.00** at 10:26:13 against a ladder built 2.94 → 1.32, **-$1,925.00** and the
  largest single instance recorded; NVDA 11-18 180C **12** at **1.43** against 2.02 → 1.56, **-$447.00**; NVDA
  11-13 165C **10** at **0.606** against 1.21 → 0.69, **-$360.00**; NVDA 11-13 162.5C **9** at **0.52** against
  1.10 → 0.69, **-$348.00**; NVDA 11-13 167.5C **9** at **0.56** against 1.35 → 0.63, **-$222.00**; META 11-13
  635C **6** at **0.72** against 1.36 → 0.83, **-$197.00**; SPY 11-13 751P **3** at **1.16** against 1.61 →
  1.34, **-$98.00**. The session realized **-$4,006.00**, the worst compiled, and these legs are **90%** of it.
  See [[days/2026-11-13]]. (Verified: raw/2026-11-13.json)
- **2026-11-13 carries the page's cleanest control.** QQQ 11-18 700C and QQQ 11-18 695C are the same underlying
  and the same expiry, with ladders built within half an hour of each other. The 700C was dumped in one fill and
  lost **-$1,925.00**. The 695C was sold in **six** separate fills 12:06:59–15:51:46 at 2.15–2.75 and returned
  **+$43.00** — the session's only green strike. Nothing else distinguishes them.
  (Verified: raw/2026-11-13.json)
- **2026-11-13: the META dump is also the session's largest settlement miss.** The six contracts sold at **0.72**
  closed **$6.99 in the money** and were worth **$4,194.00** held to expiry against the **$432.00** taken,
  **-$3,762.00**. The dump did not merely take the worst price of the ladder; it took it on the one strike of the
  five settled that session that finished in the money. See [[what-ifs/exit-before-the-close]].
  (Verified: raw/2026-11-13.json)
- **2026-11-11: SPXW 11-11 7635C, 13 contracts at 0.60 against a ladder built 2.60 → 0.85, -$1,275.00, and the
  re-entry behind it made money.** The dump came **167 seconds** after the last add. Six contracts were then
  bought back at 0.55–0.75 and sold at 0.85–0.90 for **+$150.00**. Same strike, same half hour, opposite result,
  separated only by whether the exit was taken at the bottom of the ladder. See [[days/2026-11-11]].
  (Verified: raw/2026-11-11.json)
- **2026-11-10: NVDA 11-11 172.5C twice in one session, -$499.00 and -$69.00.** Eight contracts bought
  10:31:16–10:47:36 from 2.34 to 1.45 were sold at **1.2712500001** at 10:53:26, **350 seconds** after the last
  add; four bought 11:57:21–12:03:36 at 1.04–1.10 were sold at **0.91** at 14:39:36. The middle cycle of the same
  strike, **5** contracts bought at 1.24–1.25 and sold at **1.78**, was the only one not dumped and the only one
  that made money, **+$269.00**. See [[days/2026-11-10]]. (Verified: raw/2026-11-10.json)
- **2026-11-12 is the counterexample that bounds the page, and it is a near miss.** The session's one losing
  group, **15** TSLA 11-13 395C contracts sold in one fill at **2.594**, sits below the group's **3.0288**
  average cost but **above** its four cheapest buys, so it does not meet the test. It lost **-$445.00** on
  **$4,846.00** of cost — a **9.2%** bleed against the **40.7%** of the ten qualifying instances — on a session
  that was otherwise six strikes green for **+$1,007.00**. Selling below average cost is ordinary; selling below
  the floor of the ladder is what this page measures. See [[days/2026-11-12]]. (Verified: raw/2026-11-12.json)

## Count so far

**Added 2026-11-27, counting 2026-11-27.** The count goes to **26** occurrences over **180** contracts,
**-$9,958.00** on the dumped legs, **26 of 26** red. The two new instances add **22** contracts and
**-$980.00**, and the streak on the leg itself is still unbroken.
(Verified: raw/2026-11-27.json; cumulative carried from the 2026-11-25 reading)

**The streak on the leg no longer means the dump was wrong.** Both new instances were scorable the same day
because the session has bars, and one beat holding by **+$528.00** while the other gave up **+$1,400.00**. The
2026-11-23 split said same-day dumps beat holding and the error is in the adds; that holds for every same-day
instance scored before this session and fails for one of the two added here. The page should stop stating it as
a rule for same-day strikes and state it as a tendency with a measured exception.
(Verified: raw/2026-11-27.json)

By tenor both new instances expire the day they were traded, taking the page to **14** same-day, **5** at 1 DTE,
**6** at 5 DTE and **1** at 56 DTE. The per-session distribution reads **2**, **1**, **0**, **7**, **8**, **4**,
**2**, **2**. The gaps between last add and dump are **61s** and **283s**; the **61s** is the second fastest
recorded, behind the **45s** of 2026-11-25. (Verified: raw/2026-11-27.json)

**Scored count moves for the first time in three sessions: 24 of 26 scored, 2 open.** The two instances left
open by 2026-11-25 are still open, because scoring them needs the 2026-11-25 close and that session has no bars
file; nothing this session produces can price it. The two added here were scored on arrival.
(Verified: raw/2026-11-27.json, raw/2026-11-25.json sources.bars = missing)

**One discrepancy to settle, recorded rather than silently fixed.** Re-running the mechanical test over
2026-11-10…2026-11-27 returns **25** instances, **179** contracts and **-$9,222.00**, one instance fewer than
the carried count, and the gap is on 2026-11-20: the recount finds **7** there where the carried distribution
records **8**. The cumulative above is the carried figure, as this page's convention has always been. The
2026-11-20 block predates the "at least half the open position" wording, which is the likely cause. A session
with the time for it should recount that block from `raw/` and restate the cumulative once.
(Verified: computed over raw/2026-11-10…raw/2026-11-27 against the carried 2026-11-25 reading)

**Added 2026-11-25, counting 2026-11-25.** The count goes to **24** occurrences over **158** contracts,
**-$8,978.00** on the dumped legs, **24 of 24** red. The two new instances add **16** contracts and
**-$915.00**, and no instance of this shape has yet made money on the leg it closed.
(Verified: raw/2026-11-25.json; cumulative carried from the 2026-11-24 reading)

By tenor the base tilts back to same-day: both new instances expire the day they were traded, taking the page to
**12** same-day, **5** at 1 DTE, **6** at 5 DTE and **1** at 56 DTE. The per-session distribution reads **2**,
**1**, **0**, **7**, **8**, **4**, **2**.

**The speed finding is back, at least for this pair.** The two gaps between last add and dump are **45s** and
**85s**, the two fastest on the page, against the eighteen-instance median of **472** seconds recorded on
2026-11-23. The 2026-11-20 block retired "a ladder is completed and then abandoned inside about three minutes"
because only one of eight landed inside three minutes; both of these do, and two instances do not restore a
finding that eight broke. What holds across all **24** is the shape itself, not its timing.
(Verified: raw/2026-11-25.json; prior median from the 2026-11-23 reading)

**The open instances swapped rather than cleared.** The three left open by 2026-11-24 were bounded this session
from NVDA's own same-day premiums rather than from bars, and all three beat holding to expiry; the two added
today take their place as unscored, because 2026-11-25 has no bars file and both expire that day. **22 of 24
scored, 2 open**, and these two will stay open unless a later run prices the 2026-11-25 close. The page's 2026-11-23 split
therefore stands unchanged: for same-day strikes the dump beats holding and the error is in the adds, while for
strikes with days left on them the sell is an error too — the 2026-11-20 later-dated dumps gave up at least
**8.8×** their realized loss in value that existed one session later. Both new instances are same-day, so they
fall on the first side of that split and neither tests the second.
(Verified: raw/2026-11-25.json; raw/2026-11-20.json via the 2026-11-24 reading)


**Added 2026-11-24, counting 2026-11-24.** The count goes to **22** occurrences over **142** contracts,
**-$8,063.00** on the dumped legs, **22 of 22** red. The four new instances add **18** contracts and
**-$735.00**, and the streak is unbroken: no instance of this shape has ever made money on the leg it closed.

Four in one session is the second-heaviest reading compiled, behind the ten of 2026-11-10 to 2026-11-13, and it
arrived on a session of **88** fills and **+$570.00** of cash — this shape does not need a bad day to appear. The
discount to the floor ranged **-6.4%** to **-20.4%**, against a prior range on this page that the 2026-11-20
block put at **-1.0%** to **-28.9%**, so nothing about the depth is new; the clustering is. All four fell in
**19 minutes**, 09:47:04 to 10:05:54, which is the tightest cluster recorded and the first time four separate
ladders were taken out inside one.

**Three of the four are unscored by design.** Of the 22 occurrences, **19** have been scored against a horizon
and **3** are open pending the 2026-11-25 close. That is the first time this page carries unscored instances, and
it is the direct consequence of 2026-11-23: a verdict without its horizon is not a verdict.
(Verified: raw/2026-11-24.json; cumulative computed over raw/2026-10-07…raw/2026-11-24)

**Added 2026-11-24, counting 2026-11-23.** **No new instance.** The count stays at **18** occurrences over
**124** contracts, **-$7,328.00** on the dumped legs, **18 of 18** red. 2026-11-23 produced one full-position
one-fill exit that cleared its own ladder floor and is therefore not counted.

What this session changes is the scoring, not the count. The 2026-11-20 block below reads "all eight lost on the
leg and all eight beat holding", and that second clause is now wrong for at least two of the eight: measured at
the next session's prices rather than Friday's close, TSLA 11-25 385C gave up **$2,814.00–$5,364.00** and NVDA
11-25 149C at least **$13,767.00**. Against **-$1,888.00** of realized loss on Friday's eight legs, the two
priceable later-expiry dumps alone gave up **at least 8.8×** that figure in value that existed one session
later. The page's conclusion that "the usable rule is about the adds, not the sell" survives for same-day
strikes and does not survive for strikes with days left on them — for those, the sell is the error too.
(Verified: raw/2026-11-20.json, raw/2026-11-23.json)


**Added 2026-11-23, counting 2026-11-20.** **18** occurrences across five sessions, over **124** contracts:
**$18,333.00** of cost against **$11,005.00** of proceeds, **-$7,328.00** on the dumped legs and a **40.0%**
bleed. **18 of 18 lost.** Still no instance has made money on the leg itself. The distribution by session is now
**2**, **1**, **0**, **7**, **8**, and the two heaviest sessions are the last two compiled. By tenor the base has
shifted decisively away from same-day: the eight new instances are **3** same-day, **4** at 5 DTE and **1** at 56
DTE, taking the whole page to **9** same-day, **2** at 1 DTE, **6** at 5 DTE and **1** at 56 DTE. The single
largest instance is still **-$1,925.00** (2026-11-13, 5 DTE); the largest of the new eight is **-$639.00**, and
it is the longest-dated position the page has ever recorded, a **56 DTE** call laddered across three sessions.

The speed finding weakened. The eight new gaps between last add and dump are **78s**, **295s**, **594s**,
**895s**, **903s**, **1,705s**, **3,410s** and one of **76,594s** (the SPY 729C bought the previous session),
against a prior median of **183 seconds**. Only one of the eight landed inside three minutes. The eighteen-instance
median is now **472 seconds**. "A ladder is completed and then abandoned inside about three minutes" held over
four sessions from one week and does not survive the fifth; what survives is that the whole position goes in one
fill, at a price under the floor of its own ladder.

What has changed most is the reading, not the count. Through 2026-11-13 every instance lost on the leg **and**
the session's exits were a mixed bag against settlement. On 2026-11-20 all eight lost on the leg and all eight
beat holding. The leg's loss is therefore not evidence that the sell was the error — it is arithmetic, since a
sell below the ladder floor is a loss by construction. The question the page should be asking is why the ladder
was built downward **124** times into positions that then had to be abandoned.
(Verified: computed over raw/2026-11-10…raw/2026-11-20)

**Through 2026-11-13.** **10** occurrences across the four sessions 2026-11-10 to 2026-11-13, over **91** contracts: **$13,375.00** of
cost against **$7,935.00** of proceeds, **-$5,440.00** on the dumped legs and a **40.7%** bleed. **10 of 10 lost.**
No instance has yet made money.

The distribution by session is **2**, **1**, **0**, **7** — the pattern is not spread evenly; seven of the ten are
2026-11-13, which is also the worst session compiled. By underlying it is NVDA **6**, QQQ **1**, SPXW **1**, META
**1**, SPY **1** and TSLA **0**, and by tenor same-day **6**, 1 DTE **2** and 5 DTE **2** — so it is not a 0DTE
phenomenon, and the single largest instance, **-$1,925.00**, had **five** days to expiry.

The exit comes fast. Nine of the ten fills landed within **15 minutes** of the strike's last add and six within
**3 minutes 30 seconds**: the gaps are **57s**, **102s**, **138s**, **157s**, **167s**, **199s**, **350s**,
**790s**, **883s** and one outlier of **9,360s** (2h 36m, the 2026-11-10 four-contract leg). The median is
**183 seconds**. A ladder is completed and then abandoned inside about three minutes.
(Verified: computed over raw/2026-11-10…raw/2026-11-13)

Four compiled sessions is a short base and three of them come from one week, so the size of the effect is not
settled. What is unusual is that there is no counterexample at all yet: across every one of the ten the leg lost,
and on the two sessions where the same strike was also exited another way — NVDA 172.5C on 2026-11-10 and SPXW
7635C on 2026-11-11 — the other way made money.

## What to do about it
Proposals only, for the Friday tune; Ty decides.

1. **Measure it, as its own line, from here on.** The test is already mechanical: a sell fill taking ≥50% of the
   open position below the minimum buy price of the lots it closes. Record occurrences, contracts and leg P&L per
   session. With **10 of 10** red it is the strongest single-session-shape reading in the wiki and the cheapest to
   keep. (Verified: computed over raw/2026-11-10…raw/2026-11-13)
2. **Split the exit from the ladder before judging the ladder.** [[setups/zero-dte-scalp]] has penalised add-down
   since 2026-10-07 and has never found it losing on a completed round trip. 2026-11-10 and 2026-11-11 each show
   the same strike making money on a non-dumped cycle in the same hour. The evidence points at the exit, not the
   averaging-down. (Verified: raw/2026-11-10.json, raw/2026-11-11.json)
3. **The obvious rule — do not sell the whole position below the cheapest contract in it — is not yet testable as
   a rule.** It says what not to do and nothing about what to do instead, and the post-exit windows disagree with
   each other: on 2026-11-11 the SPX proxy rose **22.00** points after the dump, so holding would have helped,
   while 2026-11-13's META dump was wrong against settlement but its own ten candles rose only **6.89**. Measure
   first. (Verified: raw/2026-11-11.json, raw/2026-11-13.json)
4. **Check whether the trigger is time or price.** The median gap between last add and dump is **183 seconds**,
   which is short enough that the exit looks like a reaction to the add rather than to a level. The number worth
   recording is the underlying's move between the last add and the dump, which `raw/` does not currently hold for
   entries — only `after` paths for exits. That is a collector change, not a trading one.
   (Verified: computed over raw/2026-11-10…raw/2026-11-13; raw/schema.json)
