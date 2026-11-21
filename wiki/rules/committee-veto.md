# Committee veto

Every v7 skip carries the gates that voted against the setup: structure, levels, candle, volume, timeframes and
committee. The committee gate is on every veto, so the question is never whether it fired but which of the other gates
came with it, and whether that combination blocked setups that would have worked.

## Evidence
- **2026-11-19 makes it twenty-nine consecutive sessions with no bot record, and it is the fourth identical
  reading in a row.** The bundle is present and complete — `holiday` **false**, **12** symbols of one-minute bars,
  **390** each, 09:30 through 15:59, collected **2026-11-20T03:30:27Z** — and `sources` reads **`v7: 0`** and
  **`sweep: false`**. The last session with any bot record is still 2026-10-09, **41** days back. All **32**
  compiled days carry a complete bundle, so nothing here changes the reading established on 2026-10-22: the fault
  is upstream of `tools/bot-collect.py`, and the check that would settle it has not been done.
  `Bots/2026-11-20.json` is already on Drive, collected **2026-11-21T03:30:29Z**, and reads `v7: 0` and
  `sweep: false` too, but that day is deferred and nothing is claimed for it here.
  See [[days/2026-11-19]].
  (Verified: raw/2026-11-19.json; Drive listing of `Raw Records/Bots/`, read 2026-11-21; computed over
  raw/2026-10-12…raw/2026-11-19)
- **2026-11-18 makes it twenty-eight consecutive sessions with no bot record, and it is the third identical
  reading in a row.** The bundle is present and complete — `holiday` **false**, **12** symbols of one-minute bars,
  **390** each, 09:30 through 15:59, collected **2026-11-19T03:30:26Z** — and `sources` reads **`v7: 0`** and
  **`sweep: false`**. The last session with any bot record is still 2026-10-09, **40** days back. All **31**
  compiled days carry a complete bundle, so nothing here changes the reading established on 2026-10-22: the fault
  is upstream of `tools/bot-collect.py`, and the check that would settle it has not been done.
  `Bots/2026-11-19.json` is already on Drive, collected **2026-11-20T03:30:27Z**, and reads `v7: 0` and
  `sweep: false` too, but that day is deferred and nothing is claimed for it here.
  See [[days/2026-11-18]].
  (Verified: raw/2026-11-18.json; Drive listing of `Raw Records/Bots/`, read 2026-11-20; computed over
  raw/2026-10-12…raw/2026-11-18)
- **2026-11-17 makes it twenty-seven consecutive sessions with no bot record, and it is the reading this page
  called from the bundle a day early.** The 2026-11-16 line said `Bots/2026-11-17.json` was already on Drive and
  read `v7: 0` and `sweep: false`, and the compiled day confirms it: bundle present, `holiday` false, **12**
  symbols of one-minute bars, **390** each, collected **2026-11-18T03:30:24Z**, `sources` reading **`v7: 0`** and
  **`sweep: false`** — the twenty-seventh identical reading in a row. The last session with any bot record is
  still 2026-10-09, now **39** days back. All **30** compiled days read `bots_bundle: present`;
  `Bots/2026-11-18.json` is on Drive, collected **2026-11-19T03:30:26Z**, and reads the same, though that day is
  deferred and is not counted here. Per proposal 8 this page stays paused, and the Mac-side check from 2026-10-22
  is now **22** compiled sessions old and undone.
  (Verified: raw/2026-11-17.json; Drive listing of `Raw Records/Bots/`, read 2026-11-19; computed over
  raw/2026-10-12…raw/2026-11-17)
- **2026-11-16 makes it twenty-six consecutive sessions with no bot record, and it reads exactly as the previous
  line predicted.** The bundle is present, `holiday` false, **12** symbols of one-minute bars, **390** each,
  collected **2026-11-17T03:32:25Z**, and its `sources` block reads **`v7: 0`** and **`sweep: false`** — the
  twenty-sixth identical reading in a row. The last session with any bot record is still 2026-10-09, now **38**
  days back. All **29** compiled days read `bots_bundle: present`, so the collector is delivering and what it
  delivers holds no v7 records; `Bots/2026-11-17.json` is on Drive already, collected **2026-11-18T03:30:24Z**,
  and reads the same, though that day is deferred and is not counted here. Per proposal 8 this page stays paused,
  and the Mac-side check from 2026-10-22 is now **21** compiled sessions old and undone.
  (Verified: raw/2026-11-16.json; Drive listing of `Raw Records/Bots/`, read 2026-11-18; computed over
  raw/2026-10-12…raw/2026-11-16)
- **2026-11-13 makes it twenty-five consecutive sessions with no bot record, and the missing-bundle worry of
  2026-11-09 is resolved: nothing was lost.** `Bots/2026-11-10.json` was absent from Drive when the 2026-11-11
  run looked, which that run read as the first break in the complete-bundle record. It was not a break. The Mac
  collector uploaded **2026-11-10**, **2026-11-11**, **2026-11-12**, **2026-11-13** and **2026-11-16** in one
  catch-up burst between **03:30:29Z** and **03:32:25Z** on 2026-11-17, exactly the behaviour `docs/wiki.md`
  describes for a Mac that has been asleep. All **28** compiled days now read `bots_bundle: present`, so the
  basis for saying the fault sits upstream of `tools/bot-collect.py` is restored in full: the collector delivers,
  and what it delivers contains no v7 records.
  (Verified: raw/2026-11-10.json, raw/2026-11-11.json, raw/2026-11-12.json, raw/2026-11-13.json; Drive listing of
  `Raw Records/Bots/`, read 2026-11-17)
- **2026-11-10 to 2026-11-13: four more identical readings, and the bundles are complete in every respect except
  the records.** Each has `holiday` false, one-minute bars for **12** symbols, and `sources` reading **`v7: 0`**
  and **`sweep: false`**. Collected at 2026-11-17T03:30:29Z, 03:30:55Z, 03:31:19Z and 03:31:58Z. The last session
  with any bot record is still 2026-10-09, now **35** days back, and the Mac-side check named on 2026-10-22 is
  still undone **16** compiled sessions after the session that named it. Per proposal 8 this page stays paused.
  (Verified: raw/2026-11-10.json, raw/2026-11-11.json, raw/2026-11-12.json, raw/2026-11-13.json; computed over
  raw/2026-10-12…raw/2026-11-13)
- **2026-11-16's bundle is on Drive and its day is not yet compiled.** The collector delivered
  `Bots/2026-11-16.json` at 03:32:25Z on 2026-11-17, but the Webull export this run read ends 2026-11-13, so the
  session has no fills in the shard and `tools/postexit.py` deferred it. If its bot records are also empty the
  streak will read twenty-six when it lands. Nothing is claimed about it here.
  (Verified: Drive listing of `Raw Records/Bots/`, read 2026-11-17; data/index.json)
- **2026-11-09 makes it twenty-one consecutive sessions with no bot record, and the collector missed the next
  morning.** The bundle is present, `holiday` false, 12 symbols of one-minute bars, 390 each, collected
  2026-11-10T03:30:25Z, and its `sources` block reads **`v7: 0`** and **`sweep: false`** — the twenty-first
  identical reading in a row. The last session with any bot record is 2026-10-09, 31 days ago. New, and the reason
  this line is not just a count: **`Bots/2026-11-10.json` is absent from Drive**, the first missing bundle against
  24 compiled days that all read `bots_bundle: present`. The complete-bundle-every-day fact was the whole basis
  for saying the fault sits upstream of `tools/bot-collect.py`; one missed upload weakens it, and 2026-11-10 is
  uncompilable as a result. Per proposal 8 this page stays paused; the Mac-side check from 2026-10-22 is now
  fourteen compiled sessions old and undone.
  (Verified: raw/2026-11-09.json; computed over raw/2026-10-12…raw/2026-11-09; Drive listing of
  `Raw Records/Bots/`, read 2026-11-11)
- **2026-11-06 makes it twenty consecutive sessions with no bot record.** The bundle is present, `holiday` false,
  12 symbols of one-minute bars, 390 each, collected 2026-11-07T03:30:29Z, and its `sources` block reads
  **`v7: 0`** and **`sweep: false`** — the twentieth identical reading in a row; 2026-11-05 was the nineteenth, on
  a bundle collected 2026-11-06T03:30:25Z. The last session with any bot record is 2026-10-09, 28 days ago.
  Recorded for the count only: per proposal 8 this page stays paused, and the Mac-side check from 2026-10-22 is
  now eleven compiled sessions old and undone.
  (Verified: raw/2026-11-05.json, raw/2026-11-06.json; computed over raw/2026-10-12…raw/2026-11-06)
- **2026-11-04 makes it eighteen consecutive sessions with no bot record.** The bundle is present, `holiday`
  false, 12 symbols of one-minute bars, 390 each, collected 2026-11-05T03:30:25Z, and its `sources` block reads
  **`v7: 0`** and **`sweep: false`** — the eighteenth identical reading in a row. The last session with any bot
  record is 2026-10-09, 26 days ago. Recorded for the count only: per proposal 8 this page stays paused, and the
  Mac-side check from 2026-10-22 is now nine compiled sessions old and undone.
  (Verified: raw/2026-11-04.json; computed over raw/2026-10-12…raw/2026-11-04)
- **2026-10-28 makes it thirteen consecutive sessions with no bot record.** The bundle is present, `holiday`
  false, 12 symbols of one-minute bars, collected 2026-10-29T03:30:49Z, and its `sources` block reads **`v7: 0`**
  and **`sweep: false`** — the thirteenth identical reading in a row. The last session with any bot record is
  2026-10-09, 19 days ago. Recorded for the count only: per proposal 8 this page stays paused, and the Mac-side
  check from 2026-10-22 is now four sessions old and undone.
  (Verified: raw/2026-10-28.json; computed over raw/2026-10-12…raw/2026-10-28)
- **2026-10-26 makes it eleven consecutive sessions with no bot record.** The bundle is present, `holiday` false,
  12 symbols of one-minute bars, collected 2026-10-27T03:30:25Z, and its `sources` block reads **`v7: 0`** and
  **`sweep: false`** — the eleventh identical reading in a row. The last session with any bot record is
  2026-10-09, seventeen days ago. The check named on 2026-10-22, whether the files `tools/bot-collect.py` reads
  exist on the Mac at all, is now two sessions old and undone; nothing on this page can move until it is.
  (Verified: raw/2026-10-26.json; computed over raw/2026-10-12…raw/2026-10-26)
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
Seen on 3 of 32 compiled days, and on none since 2026-10-09. Across 166 resolved skips, taking them all would have
returned **-48.83R**: -41.46R on 2026-10-07, +1.61R on 2026-10-08 and -8.98R on 2026-10-09. The veto is net
protective over those three days, but it was net costly on one of them, and the **twenty-nine** sessions since have
added no evidence either way. (Verified: computed over raw/2026-10-07…raw/2026-11-19)

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
8. **Added 2026-10-26: eleven sessions, and the item to carry is the check, not the page.** Proposal 7 asked for
   the gate work to be closed as blocked; this session adds nothing but another identical reading, which is the
   argument for doing that rather than restating it each day. The only thing worth carrying forward is the
   one-line check from 2026-10-22, and until it is done this page should be read as paused, not open.
   (Verified: computed over raw/2026-10-12…raw/2026-10-26)

9. **Added 2026-11-09: the separation this page relied on has a crack in it.** Proposals 4 through 8 all rest on
   the collector delivering a complete bundle every session while the bots produce nothing, which held for 24
   compiled days. `Bots/2026-11-10.json` did not arrive, so the next check should cover the collector as well as
   the bots: whether `tools/bot-collect.py` ran on 2026-11-11 at all (its log is
   `~/Library/Logs/bot-collect.log`), and whether the bots' own output files exist at the paths it reads. Both are
   Mac-side and neither can be done from the routine.
   (Verified: Drive listing of `Raw Records/Bots/`, read 2026-11-11; computed over raw/2026-10-07…raw/2026-11-09;
   docs/wiki.md, "Mac collector")

See [[what-ifs/coin-skips]] for the one symbol where the veto already looks wrong, and
[[what-ifs/cancelled-sweep-orders]] for the sweep bot, where cancellation rather than a vote is what prevented the
trades.
