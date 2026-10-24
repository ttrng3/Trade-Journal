# SPX after 12:00

Ty's rule, set 2026-10-24 from the 5A review of 19–23 Oct: no SPX entries at or after 12:00 ET. It runs as a
two-week trial, 23 Oct to 6 Nov 2026, with a P&L-by-time-bucket review on Sat 7 Nov, and the page flags it as
`spxpm` on any SPXW or SPX entry at or after 12:00. The older all-day `SPXW` flag stays. This page collects what
the rule would have caught, session by session, so the review has evidence rather than a recollection.
(Verified: work/261024-personal-rules/spec.md)

## Evidence
- **2026-10-23, day one of the trial: five of six SPX entries fall after 12:00, and they made money.** All five
  buys on SPXW 7660C — 13:16:16, 13:24:30, 13:33:06, 13:43:38 and 13:56:18, one contract each at 0.90–1.45 for
  **$585.00** — are at or after 12:00 and would be flagged. The strike returned **+$215.00**, sold between
  13:21:42 and 13:58:28 for **$800.00**, the day's third-best result. The one SPX entry before 12:00, SPXW 7675C
  at 10:26:44, returned **+$70.00**. So on the first session the rule covers, the flagged book beat the unflagged
  one. (Verified: raw/2026-10-23.json)
- **2026-10-23: the trial's first session is the opposite of the case that motivated the rule.** The review window
  the rule came from, 19–23 Oct, recounts `spxpm` at **10 trades / -$1,115.00** across the week, and the whole of
  that loss sits on 2026-10-22, where five SPXW strikes gave back **-$885.00**. One session later the same flag
  catches a winner. See [[setups/zero-dte-scalp]].
  (Verified: work/261024-personal-rules/spec.md; raw/2026-10-22.json, raw/2026-10-23.json)

## Count so far
One session of the trial compiled, 2026-10-23. Flagged on it: **5 entries on 1 strike, +$215.00**. Unflagged SPX
on the same session: 1 entry on 1 strike, **+$70.00**.

The two figures on this page must not be added. The page's own recount of `spxpm` reads 10 trades and
**-$1,115.00** over the custom range 2026-10-19 → 2026-10-23, which **includes** 2026-10-23, so Friday's flagged
entries are inside both numbers; the recount also counts trades as the Rules card counts them, not as entry fills.
The trial verdict needs sessions from 2026-10-23 onward counted once, and at present that is this one session.
(Verified: raw/2026-10-23.json; work/261024-personal-rules/spec.md)

## What to do about it
Proposals only; Ty decides at the 7 Nov review.

1. Read the trial on its own window, not on the week that prompted it. The 19–23 Oct recount is the reason the rule
   exists and cannot also be its test, and it overlaps the trial by one session (2026-10-23), so that session must
   not be counted on both sides. Only sessions from 23 Oct onward belong in the verdict, counted once.
   (Verified: work/261024-personal-rules/spec.md)
2. Keep the flagged and unflagged SPX books side by side per session, as above. One session in, the flagged side is
   ahead, which is the outcome least likely to be noticed if only the total is reported.
   (Verified: raw/2026-10-23.json)
3. Note that every SPX result on this page is settled against the **SPY × 10 proxy**, since the collector carries
   no SPX bars. It does not affect the realized P&L the rule is judged on, only any settlement claim.
   (Verified: raw/2026-10-23.json)
