# SPX after 12:00

Ty's rule, set 2026-10-24 from the 5A review of 19–23 Oct: no SPX entries at or after 12:00 ET. It runs as a
two-week trial, 23 Oct to 6 Nov 2026, with a P&L-by-time-bucket review on Sat 7 Nov, and the page flags it as
`spxpm` on any SPXW or SPX entry at or after 12:00. The older all-day `SPXW` flag stays. This page collects what
the rule would have caught, session by session, so the review has evidence rather than a recollection.
(Verified: work/261024-personal-rules/spec.md)

## Evidence
- **2026-11-02, the trial's second compiled session: one of four SPX strikes is flagged, and every SPX strike
  lost.** The flagged strike is SPXW 7645C, whose **7** entries all fall between **12:17:30** and **12:30:37** —
  bought down a ladder from 2.35 to **1.10** for **$1,170.00**, all seven closed 12:27:55–12:33:49 at 0.95–1.35
  for **$825.00**, **-$345.00**, or **-$49.29** a contract. The three unflagged strikes took **24** entries all
  before 12:00: 7680C **-$430.00** on 11 contracts, 7675C **-$125.00** on 4 and 7660C **-$120.00** on 9,
  **-$675.00** on **$3,000.00** of cost, or **-$28.12** a contract. On this session the rule would have blocked
  the **worse** book per contract and left the larger loss in place. (Verified: raw/2026-11-02.json)
- **2026-11-02: the whole SPX book is over half the session's same-day loss, and the midday drift into SPX is the
  shape worth naming.** The four SPXW strikes cost **-$1,020.00** of the session's **-$1,867.00** same-day result
  on **31** contracts. The entries walk down the clock and down the strikes — 7680C from **10:52:14**, then
  7675C, then 7660C, then 7645C from **12:17:30** — four strikes in ninety minutes, each opened after the one
  before was already losing. The rule as written catches only the last of the four.
  See [[setups/zero-dte-scalp]]. (Verified: raw/2026-11-02.json)
- **2026-11-02: across both compiled trial sessions the flagged side is still ahead, which is the opposite of what
  the rule assumes.** Flagged: **12** entries on **2** strikes, **12** contracts, **-$130.00**, or **-$10.83** a
  contract. Unflagged: **25** entries on **4** strikes, **25** contracts, **-$605.00**, or **-$24.20** a
  contract. Two sessions is not a verdict and the two point opposite ways per contract — flagged better overall,
  worse on this session — but the rule has yet to catch the expensive half on either of them.
  (Verified: raw/2026-10-23.json, raw/2026-11-02.json)
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
Two sessions of the trial compiled, 2026-10-23 and 2026-11-02, the only two since 23 Oct on which SPX was traded.
Counted once each:

| Session | Flagged (entry ≥ 12:00) | Unflagged (entry < 12:00) |
| --- | --- | --- |
| 2026-10-23 | 5 entries, 1 strike, **+$215.00** | 1 entry, 1 strike, **+$70.00** |
| 2026-11-02 | 7 entries, 1 strike, **-$345.00** | 24 entries, 3 strikes, **-$675.00** |
| Both | 12 entries, 2 strikes, **-$130.00** (**-$10.83**/contract) | 25 entries, 4 strikes, **-$605.00** (**-$24.20**/contract) |

(Verified: raw/2026-10-23.json, raw/2026-11-02.json)

The trial window closes **6 Nov** with the review on **Sat 7 Nov**, so at most four more sessions can be added,
and SPX has been traded on only two of the seven sessions compiled since the rule was set. (Verified:
work/261024-personal-rules/spec.md; computed over raw/2026-10-23…raw/2026-11-02)

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
4. **Added 2026-11-02: the rule's cut is one strike wide on the session that would have tested it.** Four SPX
   strikes were opened between 10:52:14 and 12:17:30 and only the last is flagged, yet the first three carry
   **-$675.00** of the session's **-$1,020.00** SPX loss. If the concern is midday SPX, a 12:00 line placed on the
   entry fill misses a book that was already three strikes deep by 12:00. Worth putting to the 7 Nov review as a
   question about where the line goes, not whether there should be one. (Verified: raw/2026-11-02.json)
5. **Added 2026-11-02: the trial will finish under-powered and should say so rather than return a verdict.** Two
   compiled sessions, **2** flagged strikes and **12** flagged contracts in total, with at most four sessions
   left. A rule judged on twelve contracts over two sessions cannot be confirmed or rejected; the honest output of
   7 Nov is the table above plus however many sessions arrive, and a decision to extend or drop the trial.
   (Verified: computed over raw/2026-10-23…raw/2026-11-02; work/261024-personal-rules/spec.md)
