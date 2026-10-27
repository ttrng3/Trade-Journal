# Later-expiry swing

A manual option position opened with days rather than hours left on it, carried through at least one overnight and
closed on a later session. It is the opposite trade to [[setups/zero-dte-scalp]]: the position is allowed to be wrong
for a while, so the result turns on the move rather than on entry timing within one session.

## Evidence
- **2026-10-26: SPY 10-28 764C was scalped intraday, not swung, and it ran beside its own 0DTE twin.** Four
  contracts bought between 09:41:12 and 10:09:36 at 3.66–3.80 for **$1,500.00** and all four sold between
  09:56:05 and 10:11:02 at 3.94–4.19 for **$1,636.00**, **+$136.00**, two days before expiry. As with AAPL 10-30
  on 2026-10-23, the two SPY next-day calls on 2026-10-22 and the TSLA 400C on 2026-10-19 and 2026-10-20, a
  later-dated contract opened and closed inside one session is not this setup and the result belongs to the day.
  What is new is that the same strike was traded at both expiries at once: the fifteen 0DTE 764 calls returned
  **+$246.00** and these four **+$136.00**, so the near leg made more on nearly four times the contracts while
  the later leg returned more per contract — **$34.00** against **$16.40**. One session is not a comparison of
  the two books, but it is the first time they have been run side by side on one strike.
  See [[setups/zero-dte-scalp]]. (Verified: raw/2026-10-26.json)
- **2026-10-26: still nothing open, for the second session running.** Every strike was net flat at the bell and no
  position opened during the month remains open once this session's fills are in. The three negative net
  quantities the month shard shows are September positions closed on 2026-10-02, not open risk.
  (Verified: raw/2026-10-26.json; open positions computed over data/fills/2026-10.json)
- **2026-10-23: the carry closed two seconds after the bell, and it was the right exit.** The eight TSLA 10-23
  387.5 calls left open on 2026-10-22 for **$789.00** were sold in one fill at **09:30:02** at 0.18 for
  **$144.00**. TSLA closed at **372.22**, **$15.28** below the strike, so holding any longer returned nothing: the
  **-$645.00** was already lost at Thursday's bell and the opening exit recovered what was left. The cost belongs
  to the decision to carry, not to the exit. (Verified: raw/2026-10-23.json; carry cost raw/2026-10-22.json)
- **2026-10-23: AAPL 10-30 350C was scalped intraday, not swung.** Two contracts bought at 14:32:06 and 14:47:43
  for **$548.00** and both sold at 15:02:50 and 15:15:22 for **$597.00**, **+$49.00**, a week before expiry. As
  with the two SPY next-day calls on 2026-10-22 and the TSLA 400C on 2026-10-19 and 2026-10-20, a later-dated
  contract opened and closed inside one session is not this setup and the result belongs to the day. It was also
  the only later-dated contract traded that session and the last position closed.
  (Verified: raw/2026-10-23.json)
- **2026-10-22 to 2026-10-23: TSLA 10-23 387.5C, the third completed swing and the worst.** Twenty-two contracts
  were bought across the whole of 2026-10-22, 09:30:48 to 15:59:32, at 0.75–2.05 for **$3,059.00**; fourteen were
  sold the same session for **$2,530.00**, **+$260.00** on their FIFO cost. The **eight** left open at the bell
  carried **$789.00** of cost and were sold on 2026-10-23 at 0.18 for **$144.00**: the overnight carry returned
  **-$645.00**, two and a half times the **+$260.00** the intraday round trips made. TSLA closed 2026-10-22 at
  **374.57**, already **$12.93** below the strike. (Verified: raw/2026-10-22.json; carry computed over
  data/fills/2026-10.json)
- **2026-10-22: holding was wrong here and the morning said otherwise for hours.** The three exits in the first ten
  minutes were each followed by TSLA rallying **+11.72**, **+8.91** and **+5.37** over the next 30 minutes, so the
  carry looked vindicated all morning; the strike was never reached. This is the mirror of the 2026-10-20 case on
  the 400C, where the post-exit rally was real and the close confirmed it.
  (Verified: raw/2026-10-22.json)
- **2026-10-22: two SPY next-day calls were scalped intraday, not swung.** SPY 10-23 768C, 18 contracts for
  **+$80.00**, and SPY 10-23 766C, 5 contracts for **+$142.00**, both opened and closed inside the session. As with
  the 400C on 2026-10-19 and 2026-10-20, a later-dated contract traded inside one session is not this setup; both
  results belong to the day. (Verified: raw/2026-10-22.json)
- 2026-10-13 to 2026-10-19: **TSLA 10-23 410C closed, and it was not the first one's result.** The strike ran for
  five sessions, 14 contracts bought for **$2,256.00** and 14 sold for **$2,216.00**: **-$40.00** over its whole
  life. The leg that was actually carried over a weekend — four contracts bought 2026-10-15 and 2026-10-16 for
  **$615.00** — was closed on 2026-10-19 inside a day that realized **+$84.00** on the strike on FIFO cost.
  (Verified: raw/2026-10-19.json; whole-life and FIFO cost computed over data/fills/2026-10.json)
- 2026-10-19 and 2026-10-20: TSLA 10-23 400C was traded **intraday on both sessions**, +$91.00 then +$83.00, never
  held overnight. A later-dated contract scalped inside a session is not this setup, and both results belong to
  the day rather than to the swing. (Verified: raw/2026-10-19.json, raw/2026-10-20.json)
- 2026-10-20: the clearest cost of exiting a later-dated position early. The three 400C contracts were sold between
  09:34:49 and 09:50:37 into 366–367, TSLA rose after every exit — **+5.74**, **+8.32**, **+6.29** over the next 10
  candles — and the session closed at **373.81**. (Verified: raw/2026-10-20.json)
- 2026-10-16: TSLA 10-23 410C opened, **7 days** to expiry. Three contracts at 1.69, 1.34 and 1.35 for **$438.00**,
  none sold, carried into the next session. No result yet; it is the second later-expiry position compiled and the
  only one currently open. (Verified: raw/2026-10-16.json)
- 2026-10-08 to 2026-10-09: TSLA 10-16 400C, 8 days to expiry when first bought. Four contracts accumulated across
  Thursday at 1.62, 1.46, 1.34 and 1.25 premium, **$567.00** in total, none sold that day. All four were sold on
  Friday morning between 09:30:22 and 09:50:54 at 2.84, 2.86, 3.15 and 4.35 for **$1,320.00**, a **+$753.00** round
  trip. (Verified: raw/2026-10-08.json, raw/2026-10-09.json)
- 2026-10-07 to 2026-10-09: that single position made more than the thirteen same-day contracts of the week lost
  together. Grouping every contract that round-tripped inside the week by how far its expiry sat from its first
  trade: same-day expiry **-$615.00** over 13 contracts with 5 winners, one- and two-day expiry **-$333.00** over 2
  contracts with none, and the one eight-day contract **+$753.00**.
  (Verified: computed over raw/2026-10-07…2026-10-09)
- 2026-10-08: the two TSLA 10-09 calls traded that day, at 1 and 2 days to expiry, both lost: 380C -$213.00 and 385C
  -$120.00. Near-dated is not the same as later-dated and lost like the 0DTE book.
  (Verified: computed over raw/2026-10-07…2026-10-09)

## Count so far
Seen three times on 14 compiled days, and **all three are now closed**: TSLA 10-16 400C **+$753.00**, TSLA 10-23
410C **-$40.00** and TSLA 10-23 387.5C **-$385.00** over their whole lives, so **1 winner of 3** and **+$328.00**
together. The one carried leg of the third cost **-$645.00** on its own. **No position is open** anywhere in the
month after 2026-10-26, the second consecutive session that has ended flat. Against the three, same-day strikes
round-tripped in equal size now return **+$739.00** over 38 strikes, and 2 near-dated contracts -$333.00, so the
0DTE book has overtaken the later-expiry book on realized cash while the latter still rests on the single large
winner of 2026-10-09 and has lost on both positions since.

Distinct from the three swings, **eight** later-dated contracts have now been opened and closed inside a single
session — TSLA 10-09 380C, TSLA 10-23 400C twice, MSFT 10-21 532.5C, SPY 10-23 768C and 766C, AAPL 10-30 350C and
SPY 10-28 764C — returning **-$213.00, +$91.00, +$83.00, +$38.00, +$80.00, +$142.00, +$49.00** and **+$136.00**:
**+$406.00** over the eight, 7 of 8 green. They are not this setup and each result sits on its day page, but as a
group they now outnumber the swings and are the only part of the later-dated book that is consistently positive.
(Verified: computed over raw/2026-10-07…raw/2026-10-26; whole-life and open positions computed over
data/fills/2026-10.json)

## What to do about it
Proposals only, for the Friday tune. **One position is not a strategy** and the sample here is a single contract in a
rising TSLA, so nothing about expiry choice is established. What the week does establish is that the result was
dominated by the one trade that was not 0DTE, which the same-day totals hide.

1. Keep realized result bucketed by days-to-expiry at first trade, so the comparison builds on more than one
   contract. (Verified: computed over raw/2026-10-07…2026-10-09)
2. Note that the exits here were not obviously early or late: 3 of the 4 sells saw TSLA continue up afterwards, but
   the net move across the four was -0.85. (Verified: raw/2026-10-09.json)
3. Do not read this as "hold longer" applied to the 0DTE book: those contracts expire the same day, so the choice is
   not available to them. The question is which book gets the size, and three days cannot answer it.
