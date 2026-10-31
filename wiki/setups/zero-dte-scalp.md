# 0DTE scalp

Manual trading buys same-day-expiry calls and puts on SPY, SPXW and TSLA and closes them within the session, often
re-entering the same strike several times. Expiry day leaves no room for a position to come back, so the result is
decided by entry timing and by how many times a losing strike is re-entered.

## Evidence
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
Seen on 12 of 18 compiled days. Counting only same-day strikes bought and sold in equal size: **45 strikes, 311
contracts, 30 green, +$1,713.00**. By day those round trips returned **-$729.00, +$118.00, +$21.00, +$127.00,
+$188.00, +$462.00, +$67.00, -$806.00, +$967.00, +$324.00, +$395.00** and **+$579.00** — the net has now risen on
four consecutive sessions and more than doubled over the last two. The strike count is still the steadier reading:
**30 green of 45**, **66.7%**, moving 52.0% → 58.3% → 60.5% → 63.4% → 66.7% over the last five sessions, a rise
every time, while the net changed sign once in the same stretch. The seven strikes added by 2026-10-29 and
2026-10-30 were **all** green, the longest clean run on the page.

Two strikes are excluded because they closed or left a carried position rather than round-tripping — TSLA 10-07
385C and TSLA 10-16 377.5C — and a third, TSLA 10-23 387.5C, closed Thursday's carry on 2026-10-23 and belongs to
[[setups/later-expiry-swing]]. The four sessions 2026-10-12 to 2026-10-15 contribute nothing: their raw days were
frozen with no fills, as were 2026-10-27 and 2026-10-28, whose **63** fills reached the repo after those days were
already written. (Verified: computed over raw/2026-10-07…raw/2026-10-30; late fill counts computed over
data/fills/2026-10.json)

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
