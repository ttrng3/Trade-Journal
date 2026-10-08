# Committee veto

Every v7 skip carries the gates that voted against the setup: structure, levels, candle, volume, timeframes and
committee. The committee gate is on every veto, so the question is never whether it fired but which of the other gates
came with it, and whether that combination blocked setups that would have worked.

## Evidence
- 2026-10-07: committee appeared on all 176 v7 skips. Structure came with 151, volume 149, timeframes 121, candle 84,
  levels 84. The share of skips behind each gate that reached target first: structure 23.8%, committee 22.2%,
  volume 20.8%, candle 17.9%, levels 14.3%, timeframes 13.2%. (Verified: raw/2026-10-07.json)
- 2026-10-07: timeframes is the most selective gate on this evidence, blocking a winner only 13.2% of the time, and
  structure the least at 23.8%. (Verified: raw/2026-10-07.json)

## Count so far
Seen on 1 of 1 compiled days. Across 141 resolved skips, taking them all would have returned **-41.46R**, so the veto
is net protective. (Verified: computed over raw/2026-10-07…2026-10-07)

## What to do about it
Proposals only, for the Friday tune. No gate change is justified by one day. The useful next step is to keep this
gate table per day so a gate that keeps blocking winners separates from one that is doing its job; if the ordering
above holds for a week, structure is the gate to examine first and timeframes the one to leave alone.
See [[what-ifs/coin-skips]] for the one symbol where the veto already looks wrong.
