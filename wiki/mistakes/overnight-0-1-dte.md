# Overnight 0–1 DTE

Leaving a contract open overnight when it expires that day or the next. The position has one session left to work
and no time value to fall back on, so an open that gaps the wrong way takes most of the premium before any decision
can be made. It is distinct from [[setups/later-expiry-swing]], where the hold is the point; here the hold is what
is left after a scalp was not finished.

## Evidence
- **2026-11-18: three of the four contracts expired in this session and the outcome is permanently outside the
  record.** NVDA 11-18 180C (**2**) and QQQ 11-18 695C (**1**) reached **0** days to expiry here, SPCX 11-20 150C
  (**1**) reached **2**, and all four are still open in the shard, which still ends **2026-11-13T15:51:46**; this
  Wednesday added **0** fills. The 2026-11-16 and 2026-11-17 entries below both named this run as the last one
  that could record the resolution, because the day is written `--final` here. No export arrived — the newest is
  still **2026-11-15T16:23:09Z**, **107.7** hours before this run's fire time — so the carry that this page has
  tracked since 2026-11-13 closes with its result unknown rather than measured. It is not counted as a win or a
  loss in any figure on this page, and it never can be.
  See [[days/2026-11-18]] and [[setups/later-expiry-swing]].
  (Verified: open positions and fill dates computed over data/fills/2026-11.json; raw/2026-11-18.json;
  Drive modifiedTime of the Raw Records exports, read 2026-11-20; docs/wiki.md, "Which day")
- **2026-11-17: the same four contracts sat through a second uncovered session, this one at 1 DTE, and the expiry
  itself is outside the record.** NVDA 11-18 180C (**2**), QQQ 11-18 695C (**1**) and SPCX 11-20 150C (**1**) are
  still open in the shard, which ends **2026-11-13T15:51:46**; this Tuesday added **0** fills. The two 11-18
  strikes stood at **1** day to expiry here, down from **5** when bought, and SPCX at **3**, down from **7** —
  so three of the four contracts spent their last full session in exactly the tenor this page is about, having
  been opened outside it. They expired the next session, 2026-11-18, which this run deferred and the next run
  freezes `--final`. Nothing is claimed about the outcome: no export covers either day, and if none is filed
  before that run the resolution of **3** of the **4** contracts never reaches a page.
  See [[days/2026-11-17]] and [[setups/later-expiry-swing]].
  (Verified: open positions and fill dates computed over data/fills/2026-11.json; raw/2026-11-17.json;
  docs/wiki.md, "Which day")
- **2026-11-16: the same four contracts sat through a session the export does not cover, and their tenor halved
  while nobody was looking.** NVDA 11-18 180C (**2**), QQQ 11-18 695C (**1**) and SPCX 11-20 150C (**1**) are
  still open in the shard, which ends **2026-11-13T15:51:46**; this Monday added **0** fills, so the position is
  unchanged on the record. What did change is time: the two 11-18 strikes went from **5** days to expiry when
  bought to **2** at this session, and SPCX from 7 to **4**. A 5+ DTE carry is only a 5+ DTE carry on the day it
  is opened, and this page's tenor buckets are keyed on that day — three of these four contracts entered 0–1 DTE
  territory two sessions later without a single fill to mark it. Nothing is claimed about their outcome: the
  export for this session has not been filed. See [[days/2026-11-16]] and [[setups/later-expiry-swing]].
  (Verified: open positions and fill dates computed over data/fills/2026-11.json; raw/2026-11-16.json)
- **2026-11-13: four contracts went out over the weekend across three strikes, all 5+ DTE, and the export cannot
  say what happened.** NVDA 11-18 180C (**2**), QQQ 11-18 695C (**1**) and SPCX 11-20 150C (**1**) were open at
  the bell. The CSV this run read ends **2026-11-13T15:51:46**, so these are recorded as open, not as resolved,
  and nothing is claimed about their outcome. See [[days/2026-11-13]].
  (Verified: raw/2026-11-13.json; open positions computed over data/fills/2026-11.json)
- **2026-11-12 → 2026-11-13: the month's first 0–1 DTE carry, 1 contract, -$94.00, and the cheapest instance
  compiled.** NVDA 11-13 167.5C bought at **15:30:47** at **1.50**, twenty-six minutes before the close and with
  one day to expiry, went out the next morning at **09:41:34** at **0.56** inside the nine-contract dump that
  opened that session. The strike's whole life was **-$372.00**. It is the eighth event in this bucket and the
  fifth loser; at one contract it is also the smallest, which is the only reason it cost less than October's.
  See [[rules/1550-flat]] and [[mistakes/dump-below-the-ladder]].
  (Verified: raw/2026-11-12.json, raw/2026-11-13.json; whole life computed over data/fills/2026-11.json)
- **2026-11-10 → 2026-11-11: 9 contracts of NVDA 11-18 185C, the largest carry compiled and the largest winner,
  +$937.55.** Eleven were bought 09:37:41–11:57:36 on 2026-11-10 from 3.75 down to 2.62; two were sold the same
  day and the other nine were left on. They were sold out 07:54:55–10:40:42 the next morning at 3.70–4.50,
  average **4.0944** against the **3.0527** average of the eleven, and the strike's whole life was
  **+$1,112.00**. The first fill, **2** contracts at **4.50**, came **before the open** and was the best of the
  nine. At **8** days to expiry this is a 5+ DTE carry and belongs beside [[setups/later-expiry-swing]], not in
  the 0–1 DTE bucket — the distinction this page has argued for since 2026-10-29 now has its clearest case.
  (Verified: raw/2026-11-10.json, raw/2026-11-11.json; carry and whole life computed over data/fills/2026-11.json)
- **2026-11-10: the carry itself was an unfinished ladder, which is the mechanism, not the decision.** Nine of
  the eleven contracts bought that session were still open at the bell, and the strike was never exited — there
  is no sell fill on it after 10:09:59. Adding down and then stopping is what produced the position.
  See [[mistakes/dump-below-the-ladder]]. (Verified: raw/2026-11-10.json)
- **2026-11-02: nothing carried in, nothing carried out, and the first session of November leaves this page
  empty.** All **12** strikes were net flat and the last fill of the day was at **12:39:28**, three hours and
  seventeen minutes before the **15:57** session end; the November shard holds **no** open position after the
  session. October ended flat as well, so no contract of any tenor has been held overnight since the night of
  2026-10-29 → 2026-10-30. The session still lost **-$522.00**, all of it inside the day, which is the point of
  separating this page from the scalp: flat at the bell removes this cost and no other.
  See [[rules/1550-flat]] and [[setups/zero-dte-scalp]]. (Verified: raw/2026-11-02.json; open positions computed
  over data/fills/2026-11.json)
- 2026-10-29 → 2026-10-30: **5** contracts, **-$605.00**, the largest carry cost compiled. SPY 10-30 770C, **2**
  contracts at average **1.25**, went out at **0.08** for **-$234.00**; TSLA 10-30 410C, **3** contracts at
  average **1.2867**, went out at 0.07, 0.05 and 0.03 for **-$371.00**. Both were closed inside the first **84
  seconds** of Friday and both strikes settled out of the money, by **$14.31** and **$10.17**, so the exits were
  right and the whole cost belongs to carrying. The two strikes stood at **+$139.00** and **-$71.00** on the legs
  that round-tripped on Thursday, so the carry is what made them losers: **-$192.00** and **-$305.00** all in.
  (Verified: raw/2026-10-29.json, raw/2026-10-30.json; carry and whole life computed over data/fills/2026-10.json)
- 2026-10-29: **the carried contracts were the late ones.** Of the ten TSLA 410 calls bought that session the
  three left on were bought at 15:26:06, 15:36:02 and 15:45:32 at 1.42, 1.26 and 1.18 — the three cheapest fills
  of the ten. The last SPY 770C buy was at **16:01:36**, after the bell, into a position already being closed.
  Adding down into the close is the mechanism; the carry is the consequence. See [[rules/1550-flat]].
  (Verified: raw/2026-10-29.json)
- 2026-10-27 → 2026-10-28: **1** contract of NVDA 10-28 217.5C bought at **1.66** and sold next morning at
  **2.00**, **+$34.00**. The one 0–1 DTE carry in the compiled set that worked, and the smallest.
  (Verified: computed over data/fills/2026-10.json; raw/2026-10-27.json and raw/2026-10-28.json are frozen with
  no fills, so this carry has no day page)
- 2026-10-22 → 2026-10-23: **8** contracts of TSLA 10-23 387.5C left open for **$789.00** were sold at 09:30:02
  for **$144.00**, **-$645.00**. TSLA closed **$15.28** below the strike, so again the exit was right and the cost
  was the carry. (Verified: raw/2026-10-22.json, raw/2026-10-23.json)
- 2026-10-15 → 2026-10-16: **1** contract of TSLA 10-16 377.5C, **-$11.00**. 2026-10-06 → 2026-10-07: **5**
  contracts of TSLA 10-07 385C, **+$112.00**. 2026-10-01 → 2026-10-02: **2** contracts of META 10-02 750C,
  **+$131.00**. The three oldest instances, and the two winners are both from the first week of the month.
  (Verified: computed over data/fills/2026-10.json)

## Count so far
**7** carry events in October over **22** contracts, green on **3**, for a net of **-$984.00**. The split is the
point: the three winners are **+$131.00**, **+$112.00** and **+$34.00** — **+$277.00** over **8** contracts — and
the four losers are **-$645.00**, **-$371.00**, **-$234.00** and **-$11.00**, **-$1,261.00** over **14**. No
winner has exceeded **$131.00** and two losers have exceeded **$230.00**, so the distribution is not symmetric
around a coin flip even though the count nearly is. The largest event by size, **8** contracts, is also the largest
loss, and the three biggest losers — **8**, **3** and **2** contracts — carry **-$1,250.00** of the **-$1,261.00**.

Against the other tenors: carries with **2–4** days left are **6** events, **11** contracts, **1** green,
**-$794.00**; carries with **5+** days are **10** events, **19** contracts, **2** green, **+$83.33**. Every bucket
is negative or near zero, and all tenors together are **-$1,694.67** over **23** events — so overnight holding has
cost money across the month regardless of expiry, and the 0–1 DTE bucket is simply where the single largest hits
are. (Verified: computed over data/fills/2026-10.json)

**November has recorded no carry of any tenor.** The month's only session with fills, 2026-11-02, ended with every
strike flat and nothing was carried into it, so the running figures above are still October's. The **five**
sessions compiled since — [[days/2026-11-03]], [[days/2026-11-04]], [[days/2026-11-05]], [[days/2026-11-06]] and
[[days/2026-11-09]] — are all frozen with no fills, so none adds a carry event nor rules one out: the shard holds
nothing for any of the five. A full week and a day have now been compiled without a single carry event recorded
either way.
(Verified: computed over data/fills/2026-11.json; raw/2026-11-03.json, raw/2026-11-04.json, raw/2026-11-05.json,
raw/2026-11-06.json, raw/2026-11-09.json)

**Added 2026-11-09: treat those five as unknown, not flat.** Of the eleven zero-manual pages compiled so far,
**six** have since received fills — **117** in all, including **5** on 2026-10-27 and **58** on 2026-10-28, both
of which were described as frozen on earlier pages and are not frozen any more. A page frozen blank has a better
than even record of later turning out to have traded, so the absence of a November carry event is an absence of
evidence here, not evidence of absence. The nine-day filing gap behind these five is the cause.
(Verified: computed over data/fills/2026-10.json, data/fills/2026-11.json and raw/2026-10-07…raw/2026-11-09;
Drive modifiedTime of the Raw Records export, read 2026-11-11)

**Added 2026-11-17: November has carries now, and the 2026-11-09 warning on this page was right.** The nine-day
filing gap closed on 2026-11-15 and brought **669** fills for 2026-11-03 to 2026-11-13. Three carry events fall in
the new window and **4** contracts are still open, so the earlier line that "November has recorded no carry of any
tenor" was an absence of evidence, exactly as the 2026-11-09 paragraph above predicted. It is not corrected here by
deletion but superseded: the shard now holds what those sessions did.

The **0–1 DTE** bucket becomes **8** events over **23** contracts, **3** green, **-$1,078.00** — October's seven
plus 2026-11-12 → 2026-11-13 at **-$94.00**. The split the page has tracked holds: no winner exceeds **$131.00**
and the losers now run **-$645.00**, **-$371.00**, **-$234.00**, **-$94.00** and **-$11.00**.

The **5+ DTE** bucket gains its largest and best instance, **+$937.55** on nine contracts, taking it from
**+$83.33** over 10 events to **+$1,020.88** over **11**, with **3** of 11 green. That bucket is no longer
"negative or near zero", and it is no longer carried by the single 2026-10-09 event: removing both the +$753.00 of
2026-10-09 and this one still leaves **-$669.67**, so the tenor reading is that 5+ DTE carries are bimodal — two
large winners and nine small losers — rather than profitable.

Across all tenors November's two **closed** carries are **+$843.55** over 10 contracts against October's
**-$1,694.67** over 23 events, which is the first positive month this page has recorded and rests on one event.
The four open contracts are deliberately excluded from every figure above.
(Verified: computed over data/fills/2026-10.json and data/fills/2026-11.json; raw/2026-11-10.json,
raw/2026-11-11.json, raw/2026-11-12.json, raw/2026-11-13.json)

**Added 2026-11-18: one carry event is now uncountable, and the page should say so permanently.** The 2026-11-13
carry of **4** contracts across three strikes is the only event in the compiled set whose resolution no page will
ever hold: **3** of the **4** expired in a session frozen `--final` with no export, and the fourth, SPCX 11-20
150C, expires 2026-11-20. Every bucket figure above therefore describes **23** October events plus November's two
closed carries and excludes this one, which is a gap in the evidence rather than a neutral result. The cause is
filing latency, not a trading decision: **107.7** hours between the newest export and this run.
(Verified: open positions computed over data/fills/2026-11.json; computed over raw/2026-10-07…raw/2026-11-18;
Drive modifiedTime of the Raw Records exports, read 2026-11-20)

## What to do about it
Proposals only, for the Friday tune; Ty decides.

1. **Treat "flat at the bell" as the measurement, not an aspiration, and count the exceptions per week.** Five of
   the month's twenty-three carry events fall on or after 2026-10-22, and the two most expensive are both in that
   window. (Verified: computed over data/fills/2026-10.json)
2. **Separate the add-down from the carry before judging either.** Add-down has not lost on a round trip in the
   compiled set, including the deepest one on 2026-10-30; what loses is the part of the ladder that never gets
   sold. The number worth keeping is contracts bought after 15:00 that were still open at the bell — on
   2026-10-29 that is **4** of the **5** carried. See [[setups/zero-dte-scalp]].
   (Verified: raw/2026-10-29.json, raw/2026-10-30.json)
3. **Do not read the exits as mistimed.** On all four losing events the strike settled out of the money, so
   selling at the open beat holding to expiry every time. The decision under review is the previous afternoon's,
   not the morning's. (Verified: computed over data/fills/2026-10.json)
4. **One bucket is not a verdict on tenor.** The 5+ DTE bucket is positive only because of one **+$753.00**
   event of **4** contracts closed on 2026-10-09; without it that bucket is **-$669.67** over **9** events.
   See [[setups/later-expiry-swing]]. (Verified: computed over data/fills/2026-10.json)
