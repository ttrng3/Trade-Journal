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
**10** occurrences across the four sessions 2026-11-10 to 2026-11-13, over **91** contracts: **$13,375.00** of
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
