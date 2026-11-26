# Deep ladder

Adding down a single strike until six or more contracts are open before anything is sold. The test is mechanical
and reads only the entries: take a strike bought and sold in equal size within one session, walk its fills in
time order, and record the largest open position it ever reached. Six or more is a deep ladder; five or fewer is
a shallow one.

It is about the adds, not the exit. [[mistakes/dump-below-the-ladder]] tests the sell — whether the whole
position left in one fill below its own floor — and this page tests how big the position was allowed to get
before any sell happened at all. The two overlap often and are not the same: a deep ladder can be taken off in
pieces, and a shallow one can still be dumped. This page exists because the dump page asked, on 2026-11-23, why
the ladder was built downward into positions that then had to be abandoned, and the depth turns out to answer
more than the exit does.

## Evidence

- **2026-11-25: the cut is clean in both tails, the first session where it is.** Three strikes went seven or
  eight deep and **all three lost**, **-$1,057.00**: TSLA 11-25 372.5C **8** contracts **-$465.00**, QQQ 11-25
  603P **8** contracts **-$450.00**, NVDA 11-25 148C **7** contracts **-$142.00**. Eight strikes never went
  past **five** and **all eight made money**, **+$1,251.00**, the largest being NVDA 12-04 160C at **+$270.00**
  over seven contracts traded in two cycles of four and three. Eleven strikes, no exception either way.
  (Verified: raw/2026-11-25.json)

  The session also separates depth from tenor, which matters because tenor is the cut this wiki has leaned on.
  The three deep ladders are all same-day expiry, but the shallow eight contain three same-day strikes that made
  **+$378.00** between them, and the same underlying ran both shapes inside ten minutes: QQQ's **603P** went
  eight deep and lost **$450.00** while its **610P** stopped at five and made **$138.00**. TSLA did the same, a
  dumped eight-deep **372.5C** against a four-deep **380C** opened **33** seconds earlier that made **$88.00**.
  (Verified: raw/2026-11-25.json)

## Count so far

**Added 2026-11-25, computed over every compiled raw day.** Across **36** sessions and **117** strikes bought and
sold in equal size, depth splits the book:

- **Five or fewer: 76 strikes, 57 green (75.0%), +$3,569.00**, averaging **+$46.96** a strike.
- **Six exactly: 15 strikes, 6 green (40.0%), -$343.00**, averaging **-$22.87**.
- **Seven or more: 26 strikes, 14 green (53.8%), -$2,555.00**, averaging **-$98.27**.

Everything **six or deeper** is **41** strikes and **-$2,898.00**. The green rate at depth seven or more is
**53.8%**, not far off a coin, so this is not a shape that loses often; it is a shape that loses large when it
loses. (Verified: computed over raw/2026-10-07…raw/2026-11-25)

**Crossed with tenor, the account's whole compiled loss sits in one corner.** Deep and same-day is **28**
strikes, **39.3%** green, **-$3,238.00**; deep and later-dated is **13** strikes, **69.2%** green, **+$340.00**;
shallow and same-day is **48** strikes, **68.8%** green, **+$1,009.00**; shallow and later-dated is **28**
strikes, **85.7%** green, **+$2,560.00**. The decomposition is exact: the same-day book's **-$2,229.00** on
[[setups/zero-dte-scalp]] is **-$3,238.00** of deep ladders plus **+$1,009.00** of shallow ones, and the
later-dated intraday **+$2,900.00** on [[setups/later-expiry-swing]] is **+$340.00** plus **+$2,560.00**.
(Verified: computed over raw/2026-10-07…raw/2026-11-25)

That reframes the tenor finding rather than replacing it. Same-day expiry is not losing money on its own: the
shallow same-day book is **+$1,009.00** over **48** strikes. What loses is depth on same-day expiry, and depth
carries signal inside both tenors — **+$21.02** against **-$115.64** a strike within same-day, and **+$91.43**
against **+$26.15** within later-dated. Both cuts are real and depth is the one with the losing corner.
(Verified: computed over raw/2026-10-07…raw/2026-11-25)

The base is **36** sessions from one account and the depth bands are uneven: **76** strikes sit at five or fewer
against **15** at exactly six, so the middle band is thin and its **-$343.00** should not be read as a level.
The ordering of the three bands is monotonic in average result, which the earlier size tests on
[[setups/zero-dte-scalp]] never produced.
(Verified: computed over raw/2026-10-07…raw/2026-11-25)

## What to do about it
Proposals only, for the Friday tune; Ty decides.

1. **Record the deepest open position per strike, every session, as its own line.** It is computable from the
   fills already in `raw/`, needs no collector change, and it is the first cut in this wiki whose average result
   orders monotonically across three bands. (Verified: computed over raw/2026-10-07…raw/2026-11-25)
2. **A cap at five contracts per strike is the obvious test and it is testable.** The shallow book is **76**
   strikes at **+$3,569.00** and **75.0%** green; the question a cap asks is what the deep **41** would have
   returned had they stopped at five, which `raw/` can answer for every one of them because the ladder's fills
   and times are all recorded. That measurement should come before the rule.
   (Verified: computed over raw/2026-10-07…raw/2026-11-25)
3. **Watch it against same-day expiry specifically.** The deep same-day corner is **-$3,238.00** over **28**
   strikes, which is more than the whole compiled loss of the same-day book. If only one thing is capped, cap
   depth on expiry day. (Verified: computed over raw/2026-10-07…raw/2026-11-25)
4. **Do not retire the dump test.** Depth explains more of the money, but the dump test catches a distinct and
   still unbroken shape, and on 2026-11-25 one seven-deep ladder lost while clearing its own floor. Keep both
   lines. (Verified: raw/2026-11-25.json; see [[mistakes/dump-below-the-ladder]])
