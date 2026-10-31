# Overnight 0–1 DTE

Leaving a contract open overnight when it expires that day or the next. The position has one session left to work
and no time value to fall back on, so an open that gaps the wrong way takes most of the premium before any decision
can be made. It is distinct from [[setups/later-expiry-swing]], where the hold is the point; here the hold is what
is left after a scalp was not finished.

## Evidence
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
**7** carry events this month over **22** contracts, green on **3**, for a net of **-$984.00**. The split is the
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
