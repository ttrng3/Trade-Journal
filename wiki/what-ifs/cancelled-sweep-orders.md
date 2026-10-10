# Cancelled sweep orders

The sweep bot arms a limit entry and cancels it when its condition lapses. Both cancellations recorded so far went on
to reach their target before their stop, so the cancellation rule — not a committee vote — is what kept the sweep bot
flat.

## Evidence
- 2026-10-09: SPY call, limit armed 12:20:00, cancelled 13:21:00 as `expired`, entry 777.33, stop 776.73, target
  779.10. Target reached at 14:50, **+2.95R** had it filled and run to target.
  (Verified: raw/2026-10-09.json)
- 2026-10-07: SPY call, limit armed 11:35:00, cancelled 11:36:00 because the `target traded before the pullback`,
  entry 774.37, stop 773.62, target 775.12. Target reached at 11:37, **+1.00R** had it filled.
  (Verified: raw/2026-10-07.json)
- 2026-10-08: the sweep bot produced no record at all, so there is nothing to count for that session.
  (Verified: raw/2026-10-08.json)

## Count so far
Seen on 2 of 3 compiled days. Both cancellations resolved target first, worth **+3.95R** in total had they been taken
and held to target. The sweep bot has taken no live trade on any compiled day.
(Verified: computed over raw/2026-10-07…2026-10-09)

## What to do about it
Proposals only, for the Friday tune. Two instances with the same outcome is suggestive and nothing more, and the two
cancellations had different reasons — one order expired unfilled, the other was cancelled because price reached the
target without offering the pullback. Those are not one problem:

1. The 2026-10-07 case is arguably the rule working: the setup was gone because the move had already happened, and a
   fill would have required chasing. (Verified: raw/2026-10-07.json)
2. The 2026-10-09 case is the one worth costing out, because the order simply timed out after an hour and the target
   came 89 minutes later. Whether the arm window is too short is answerable once there are more than two records.
   (Verified: raw/2026-10-09.json)
3. Log every armed sweep order with its arm time, cancel time, cancel reason and `first_hit`, so expiry-type
   cancellations separate from condition-type ones. The sweep bot is on a 30-session paper forward test under
   [[hypothesis-ledger]] H04, which is the right place for this count to land.
