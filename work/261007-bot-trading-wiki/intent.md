# Intent: a self-updating trading wiki on the journal page — daily lessons from Ty's and the bots' trades, and a weekly one-page report

**Status:** accepted 2026-10-07
**Source:** chat, 2026-10-07

**Problem.** The journal page shows Ty's Webull fills, but nothing turns trades into lessons, and the bots'
trades are not on it at all. The bots (v7 and the sweep V0 forward test, repo orb-options) leave raw logs on the
Mac only. On 2026-10-07 the lessons surfaced only because Ty asked by hand: the 10:00 drill bought a call against
the chart by design; the sweep's 11:35 SPY call was cancelled because its target sat below the opening-range high;
v7 skipped a SPY long at 11:09 that would have won, because lagging 3m/15m structure still voted bearish. Nobody
checks what price did after an exit, and a week later none of this is recorded.

**Outcome.** Ty's words: "raw data (daily journaling) as source code, an LLM as a compiler to transform
unorganized input into a structured, interlinked wiki and then spit out the one page report each week"
(Karpathy's LLM-wiki method). Checkable as:
1. After every session close, with no one asking, a raw day file is added holding: Ty's Webull trades for the
   day, every bot trade (drills labelled as drills), every setup a bot saw and skipped, and what price did in the
   next few candles after each exit and each skip ("how that trade played out").
2. The same run has Claude update the wiki: pages by concept (mistake patterns, setups, what-ifs, rules, days),
   linked to each other; a new day adds evidence to existing pages instead of only adding a dated entry.
3. Every Friday after the close, a one-page weekly report compiled from the wiki: winners and losers, entries and
   exits, how the market continued after each exit, the what-ifs, and proposed changes for the Friday tune.
4. Ty reads the wiki and the weekly report at https://ttrng3.github.io/Trade-Journal/, next to his Webull
   journal, on his phone.

**Who and what is affected.** Ty. Repo Trade-Journal (new wiki section on the page, new published files, the
daily routine or a new job). Read only, never written: the Webull fills already in `data/`, v7's journal
(`out/v7/` in orb-options' v7 agent-bot worktree) and the sweep forward log (`orb-options/sweep/out/forward/`).
The Cowork preview of the journal page (artifact mirror contract).

**Constraints.**
- The bots and their timeline are untouched: no change to v7, the sweep bot, drills or schedules (Ty, 2026-10-07).
  Tuning happens Fridays only (rule "journal is behaviour, not a score", 2026-10-06).
- No backtests; the what-ifs use only the session's own real prices.
- Raw day files are never edited after they're written; the wiki is what changes.
- The existing journal (fills, `index.html` engine, sync, serialization, backups) keeps working unchanged.
- Repo rules: changes reach `main` by PR and Ty's ship; a new kind of published file needs a `.pages-allow` line in
  its own PR first; public on purpose, so no tokens, preview ids, account ids or personal data by value.
- Bot data lives on the Mac, so whatever reads it runs on the Mac (tested, not assumed: see CLAUDE.md "Known
  mistakes", 2026-09-23).
- Light theme, Apple design standard; any new colour is a token.
- Personal entity only; no work-entity content.

**Decisions (Ty, 2026-10-07).**
- Page: https://ttrng3.github.io/Trade-Journal/, so the bots' trades are read next to the Webull journal. This is
  Ty's say-so to widen what the public page serves.
- Weekly report: Friday after the close.
- "How the trade played out": the next 10 three-minute candles (30 minutes) after each exit or skip, plus where
  price was at the close (accepted as proposed).
- Both Ty's manual trades and the bots' trades.
- The daily wiki update runs with the existing 11:00 Hanoi sync, so Ty's trades and the bots' are compiled together.

**Open questions.** none known
