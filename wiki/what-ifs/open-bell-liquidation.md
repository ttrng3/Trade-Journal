# Open-bell liquidation

Closing a whole carried book into the first minutes of a gap-up session, before the opening move has finished
setting its range. The exit is right in direction — the gap is the reason the position is worth anything — and the
question is only what the same contracts fetched a few minutes later. It is distinct from
[[what-ifs/exit-before-the-close]], which needs a settlement price and so covers same-day strikes only; these
positions have days left and no settlement to score against.

The test uses only prices actually filled that morning: each strike's proceeds against what the same contracts
would have returned at that strike's own best fill of the session.

## Evidence

- **2026-11-24: the carried book was one contract, and the measure cannot be taken.** AAPL 12-04 360C, carried
  out of 2026-11-23 at **1.95**, was sold at **09:38:16** at **2.35** for a **+$40.00** carry leg. One contract in
  one fill has no first-fill-versus-best-fill spread, and the session did not gap: AAPL opened into **350.33** at
  09:39 against a **354.19** close. The two contracts of the same strike bought that morning went out at **2.45**
  and **2.76** by 09:39:15, so the carried contract was sold at the lowest of the three prints its own strike
  traded that minute — **$0.41** below the best, **$41.00** on one contract. Too small to score, recorded so the
  session is not missing from the series. (Verified: raw/2026-11-24.json, raw/2026-11-23.json)
- **2026-11-23: 18 contracts in 22 minutes, and 19.8% of the proceeds left on the table at the day's own
  prices.** Five strikes carried out of 2026-11-20 were sold between **09:30:00** and **09:51:50** for
  **$18,111.00**. Priced at each strike's best fill that morning the same **18** contracts return
  **$21,706.00** — a difference of **$3,595.00**, against a realized gain of **+$14,931.00**. Per strike: TSLA
  12-04 400C **$770.00**, NVDA 11-25 145C **$1,300.00**, SPY 11-25 725C **$580.00**, NVDA 01-15 175C **$520.00**
  and TSLA 11-25 385C **$425.00**. See [[days/2026-11-23]].
  (Verified: raw/2026-11-23.json)
- **2026-11-23: the dispersion inside a single strike reached 1.85× in eight minutes.** TSLA 12-04 400C sold at
  **5.75** at 09:30:00 and at **10.65** at 09:37:51, **+85.2%**; TSLA 11-25 385C at **5.70** then **9.95**,
  **+74.6%**. The other three ran the other way: NVDA 11-25 145C **22.50 → 16.00** (**-28.9%**), NVDA 01-15 175C
  **8.50 → 6.05** (**-28.8%**) and SPY 11-25 725C **7.64 → 4.81** (**-37.0%**), each a later fill at a worse
  price. Waiting was not reliably better — it was reliably *different*, by up to 85% on the same contract inside
  one eight-minute window. (Verified: raw/2026-11-23.json)
- **2026-11-23: the underlyings kept going after every exit, which is why the up-dispersion is not luck.** NVDA
  was **162.30** at the 09:30:02 fill and **159.54** at 09:34:05, then made **169.56** by 10:00 and **170.72** by
  10:21, closing **165.19** — above every exit level. TSLA was **382.04** at the first fill and reached
  **390.28**, closing **385.88**. SPY was **721.42**, dipped to **717.51** at the 09:35:19 fill and closed
  **722.42**. Three of the five strikes were sold, in part, into the morning's low rather than its range.
  (Verified: raw/2026-11-23.json)

## Count so far

**Added 2026-11-24.** Still **one** scorable session. 2026-11-24 carried **1** contract into the session and is
recorded above but not scored: a single fill has no spread to measure, and the session did not gap. The
measure therefore stands unchanged at **5** strikes, **18** contracts, **15** fills, **$3,595.00** and **19.8%**,
and proposal 1 below still needs three or four more gap sessions. (Verified: raw/2026-11-24.json)
One session, **5** strikes, **18** contracts, **15** fills. Proceeds **$18,111.00**; at each strike's best fill of
the morning **$21,706.00**; difference **$3,595.00**, **19.8%**. **2** of the 5 strikes improved after their first
fill and **3** got worse, so the page has no directional finding yet — what it has is a magnitude: the price range
a single carried contract traded through in the first twenty minutes of a gap-up session was **1.85×** at the
widest and **1.41×** at the narrowest, on all five strikes at least **1.40×**.
(Verified: computed over raw/2026-11-23.json)

## What to do about it
Proposals only; Ty decides.

1. **Record the first-fill-versus-best-fill spread on every carried book from here on.** One session cannot say
   whether selling the open is costly or merely noisy, and the measure is cheap: it needs only the fills already
   in the raw day. Three or four gap sessions will settle it.
2. **If the spread persists, the lever is scaling the exit, not delaying it.** On 2026-11-23 the strikes sold in
   several fills across the twenty minutes captured both tails; a single fill captures one. SPY 11-20 720C on
   2026-11-20 is the same observation from a losing session — the only strike sold piecemeal was the only clear
   winner. See [[setups/zero-dte-scalp]].
3. **Do not read this page as an argument for holding longer.** It measures minutes inside one session. The
   overnight question is [[setups/later-expiry-swing]], where the same book's record is **+$12,947.83** over
   **112** contracts with **$14,931.00** of that from this one session.
