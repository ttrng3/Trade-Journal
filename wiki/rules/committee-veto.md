# Committee veto

Every v7 skip carries the gates that voted against the setup: structure, levels, candle, volume, timeframes and
committee. The committee gate is on every veto, so the question is never whether it fired but which of the other gates
came with it, and whether that combination blocked setups that would have worked.

## Evidence
- 2026-10-09: committee again appeared on all 26 v7 skips. Volume came with 23, levels 21, structure 19, candle 17,
  timeframes 8. Of the 12 that resolved, the share behind each gate that reached target first: candle 12.5%,
  levels 11.1%, volume 10.0%, committee 8.3%, structure 0.0%, timeframes 0.0%. (Verified: raw/2026-10-09.json)
- 2026-10-08: committee appeared on all 13 v7 skips. Timeframes came with 11, volume 10, structure 9, candle 5,
  levels 1. All 13 resolved, and the share behind each gate that reached target first: candle 60.0%,
  timeframes 54.5%, committee 46.2%, structure 44.4%, volume 40.0%, levels 0.0%. (Verified: raw/2026-10-08.json)
- **The 2026-10-07 ordering did not hold.** Timeframes was the most selective gate on day one at 13.2%, then the
  least selective on day two at 54.5%, then the most selective again on day three at 0.0%. Structure moved 23.8% to
  44.4% to 0.0% over the same three sessions. (Verified: computed over raw/2026-10-07…2026-10-09)
- 2026-10-07: committee appeared on all 176 v7 skips. Structure came with 151, volume 149, timeframes 121, candle 84,
  levels 84. The share of skips behind each gate that reached target first: structure 23.8%, committee 22.2%,
  volume 20.8%, candle 17.9%, levels 14.3%, timeframes 13.2%. (Verified: raw/2026-10-07.json)
- 2026-10-07: timeframes is the most selective gate on this evidence, blocking a winner only 13.2% of the time, and
  structure the least at 23.8%. (Verified: raw/2026-10-07.json)

## Count so far
Seen on 3 of 3 compiled days. Across 166 resolved skips, taking them all would have returned **-48.83R**: -41.46R on
2026-10-07, +1.61R on 2026-10-08 and -8.98R on 2026-10-09. The veto is net protective over three days, but it was
net costly on one of them. (Verified: computed over raw/2026-10-07…2026-10-09)

## What to do about it
Proposals only, for the Friday tune. The proposal carried out of 2026-10-07 was to watch whether the per-gate
ordering held for a week and, if it did, to examine structure first and leave timeframes alone. **It did not hold**,
and on this evidence no gate can be ranked: the per-gate target-first shares swing by 40 points or more between
sessions on samples of 1 to 13 resolved skips per gate. Reading a ranking off a single day was the mistake.
(Verified: computed over raw/2026-10-07…2026-10-09)

1. Stop ranking gates per day. Pool the per-gate counts across all compiled days and only read a share once a gate
   has a few dozen resolved skips behind it. (Verified: computed over raw/2026-10-07…2026-10-09)
2. The one stable fact is that committee is on every veto, 215 of 215 v7 skips over three days, so it carries no
   information on its own and should not be reported as a reason.
   (Verified: computed over raw/2026-10-07…2026-10-09)
3. Note that v7's symbol list narrowed to SPY and QQQ by 2026-10-09, so later days are not comparable with
   2026-10-07's ten symbols without splitting by symbol. (Verified: raw/2026-10-09.json)

See [[what-ifs/coin-skips]] for the one symbol where the veto already looks wrong, and
[[what-ifs/cancelled-sweep-orders]] for the sweep bot, where cancellation rather than a vote is what prevented the
trades.
