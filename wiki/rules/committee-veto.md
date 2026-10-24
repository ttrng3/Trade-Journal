# Committee veto

Every v7 skip carries the gates that voted against the setup: structure, levels, candle, volume, timeframes and
committee. The committee gate is on every veto, so the question is never whether it fired but which of the other gates
came with it, and whether that combination blocked setups that would have worked.

## Evidence
- **2026-10-23 makes it ten consecutive sessions with no bot record — a full fortnight of trading.** The bundle is
  present, `holiday` false, 12 symbols of one-minute bars, collected 2026-10-24T03:30:24Z, and carries **0 v7
  records** and **0 skips**. The last session with any bot record is 2026-10-09. The collector has now delivered a
  complete bundle on ten consecutive sessions while the bots have produced nothing, which is as clean a separation
  of the two faults as the data can give.
  (Verified: raw/2026-10-23.json; computed over raw/2026-10-12…raw/2026-10-23)
- **2026-10-22 makes it nine consecutive sessions with no v7 record, and names the sweep side explicitly.** The
  bundle is present, `holiday` false, 12 symbols of one-minute bars, collected 2026-10-23T03:30:22Z, and its own
  `sources` block reads **`v7: 0`** and **`sweep: false`** — not an empty log but **no sweep log found at all**.
  That is the collector reporting the bots' files missing, not the bots reporting no setups. Nothing below has
  moved since 2026-10-09. (Verified: raw/2026-10-22.json; computed over raw/2026-10-12…raw/2026-10-22)
- **2026-10-21 makes it eight consecutive sessions with no v7 record.** The bundle is present, `holiday` false, 12
  symbols of one-minute bars, **0 v7 rows and no sweep log** — the same shape as the seven before it. Nothing below
  has moved since 2026-10-09. (Verified: raw/2026-10-21.json; computed over raw/2026-10-12…raw/2026-10-21)
- **2026-10-12 to 2026-10-20: seven consecutive compiled sessions with no v7 record at all.** Every one of the
  seven bundles is present and complete — 12 symbols of one-minute bars each — and every one carries **0 v7 rows
  and no sweep log**. No skip means no gate vote, so none of the counts below has moved since 2026-10-09. The
  collector is delivering; what is silent is the bots.
  (Verified: computed over raw/2026-10-12…raw/2026-10-20)
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
Seen on 3 of 13 compiled days, and on none since 2026-10-09. Across 166 resolved skips, taking them all would have
returned **-48.83R**: -41.46R on 2026-10-07, +1.61R on 2026-10-08 and -8.98R on 2026-10-09. The veto is net
protective over those three days, but it was net costly on one of them, and the **ten** sessions since have added
no evidence either way. (Verified: computed over raw/2026-10-07…raw/2026-10-23)

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
4. **Added 2026-10-20: the gate question is on hold and the wiring question is open.** Seven consecutive sessions
   with a complete bundle and zero v7 rows is long enough that the next tune should establish whether the bots are
   running at all before any gate is adjusted. (Verified: computed over raw/2026-10-12…raw/2026-10-20)
5. **Added 2026-10-21: it is eight sessions, a full trading week and a half.** The collector has not missed a day,
   so whatever is silent is upstream of it. Establish that before the next tune touches a gate.
   (Verified: computed over raw/2026-10-12…raw/2026-10-21)
6. **Added 2026-10-22: the bundle says where to look.** `sources.sweep` is **`false`**, which is the collector
   saying it found no sweep log to read — a different fault from a log that exists and is empty, and a narrower
   thing to check than "are the bots running". Start with whether the bots' output files exist at the paths
   `tools/bot-collect.py` reads on the Mac. Nine sessions is long enough that this should precede any gate work.
   (Verified: raw/2026-10-22.json; computed over raw/2026-10-12…raw/2026-10-22)
7. **Added 2026-10-23: ten sessions, and the question is no longer a gate question at all.** Two full trading
   weeks with a complete bundle every day and not one v7 record or skip. Nothing on this page can move until the
   bots write something, so the gate work should be closed as blocked rather than carried forward each session as
   an open item. The single check that unblocks it is the one from 2026-10-22: whether the files
   `tools/bot-collect.py` reads exist on the Mac at all.
   (Verified: computed over raw/2026-10-12…raw/2026-10-23)

See [[what-ifs/coin-skips]] for the one symbol where the veto already looks wrong, and
[[what-ifs/cancelled-sweep-orders]] for the sweep bot, where cancellation rather than a vote is what prevented the
trades.
