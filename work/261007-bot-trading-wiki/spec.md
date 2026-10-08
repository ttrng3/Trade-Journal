# Spec: bot-trading-wiki

**Intent:** accepted 2026-10-07 · **Status:** approved
**Approved:** 2026-10-07

## Requirements
1. Every trading day, with no one asking, a raw day file is written once and never edited. It holds Ty's Webull
   fills for that session, every bot trade (drills marked `drill`), every setup a bot saw and skipped or cancelled,
   and the price path after each exit and each skip. (Intent, Outcome 1.)
2. "How the trade played out" = the next 10 three-minute candles of the underlying after the exit or skip time,
   plus the session close; for a skipped or cancelled setup, also whether its target or its stop traded first
   later that day. (Intent, Decisions.)
3. The same run has Claude update a wiki of linked Markdown pages by concept: mistake patterns, setups, what-ifs,
   rules, and one page per day. A new day adds evidence to the existing concept pages. (Outcome 2.)
4. On the run after Friday's session (Saturday 11:00 Hanoi), a one-page weekly report compiled from the wiki:
   winners and losers, entries and exits, how the market continued after each exit, the what-ifs, and proposed
   changes for the Friday tune. (Outcome 3, Decisions.)
5. Ty reads the wiki and the weekly report on his phone from https://ttrng3.github.io/Trade-Journal/, next to the
   Webull journal. (Outcome 4.)
6. It runs inside the existing 11:00 Hanoi sync, so Ty's trades and the bots' are compiled together. (Decisions.)
7. The journal, the bots and their timeline are unchanged. (Constraints.)

## Design

**Data flow**

    Mac, 10:30 Hanoi Tue–Sat (launchd)            cloud routine, 11:00 Hanoi (existing)
    bot logs + 1-min bars ──rclone──▶ Drive ──▶  Webull sync (unchanged) ──▶ raw/<day>.json ──▶ Claude compiles wiki/ ──▶ GitHub ──▶ Pages
                                     Raw Records/Bots/<day>.json                                       └─ Saturday: wiki/weekly/<yyyy-Www>.md

**1. Mac collector (new, `tools/bot-collect.py`, launchd `com.ty.bot-collect`, 10:30 Hanoi Tue–Sat).**
Reads, never writes, the bots' own files for the last session:
- v7: `journal-<day>.jsonl` (looked up under `orb-options/out/v7/` and `orb-options/.claude/worktrees/*/out/v7/`,
  since v7 runs from a worktree today).
- sweep: `orb-options/sweep/out/forward/<day>.log`.

It keeps an **allowlist of fields** (kind, time, symbol, side, setup, prices, stop, targets, R, P&L, the skip
reasons from `votes`) and drops everything else, so contract ids, conIds, equity details beyond the start line,
and anything new a bot adds later never reach the public repo by default. It fetches 1-minute bars for the session
(Alpaca, keys already in `orb-options/.env`, read in place, never copied) for the bots' symbols plus Ty's usual
underlyings (SPY, QQQ, IWM, TSLA, META, AMZN, NFLX, AMD, NVDA, AAPL, GOOGL, COIN), resampled to 3-minute.
Writes one bundle to `Drive: 09 Trading/Trade Journal/Raw Records/Bots/<day>.json` with rclone.
If the Mac was asleep at 10:30, launchd runs the job on wake.

**2. Routine (existing `Trade Journal daily sync`).** The prompt gains one step, placed **before** its preview
step so the preview stays last: "compile the wiki: follow `docs/wiki.md`." Everything else lives in the repo, which the prompt already says wins.
`docs/wiki.md` tells the run to:
- (a) read the day's Webull fills from the just-synced month shard and the Bots bundle from Drive;
- (b) run `python3 tools/postexit.py` → writes `raw/<day>.json` (requirements 1–2; all numbers computed in code,
  none by the model). If `raw/<day>.json` already exists it is not overwritten;
- (c) as the compiler, update `wiki/`: `days/<day>.md`, and the concept pages under `mistakes/`, `setups/`,
  `what-ifs/`, `rules/`, linked with `[[page]]`; every claim cites its raw day; a page is edited in place, not
  duplicated;
- (d) on Saturday, write `wiki/weekly/<yyyy-Www>.md` (one page, under 600 words, ty-report-standard: answer
  first, labelled numbers, risks last) and point `wiki/index.md` at it;
- (e) run `python3 tools/wiki-check.py` (0 dangling links, every day page cites a raw file) before pushing.

No bundle (Mac off): the run compiles Ty's trades alone and says "bot bundle missing" in its report and on the
day page.

**3. Page.** New `wiki.html`, one static file: renders `wiki/*.md` with marked.js (cdnjs), turns `[[page]]` into
links, opens on the latest weekly report, then the day pages, then the concept pages. Same light Apple tokens as
`index.html` (copied, not linked). `index.html` gets one link, "Wiki", in its header; nothing else in it changes.

**4. Files.** The existing Cowork preview also carries `wiki.html` and the `wiki/*.md` files (supporting files,
changed ones only per run). New: `tools/bot-collect.py` (Mac), `tools/postexit.py`, `tools/wiki-check.py`, `docs/wiki.md`,
`wiki.html`, `raw/`, `wiki/`, the launchd plist (kept in `tools/`, installed to `~/Library/LaunchAgents/`).
Changed: `index.html` (one link), `.pages-allow`, README (one paragraph), the routine prompt (one line), the
Pipeline Wiring page (row + dated entry).

**SPX trades** (230 of Ty's 2,227 fills in `data/fills/2026-08.json`–`2026-10.json` are SPXW; counted 2026-10-07 at `e603b28`): Alpaca has no index bars, so their price path uses SPY ×
10. **Assumption:** close enough for "what happened next" (direction and size of the move), not for exact P&L;
each SPX line on the page says it is a proxy.

## Conflicts
Loaded: kernel `standing-instructions.md`, workspace `CLAUDE.md`, repo `CLAUDE.md`, `docs/nightly-sync.md`,
`README.md`, the artifact mirror contract, ty-report-standard, secure-pages. apple-design not loaded: this is a
static page, and ty-report-standard's visual section governs static pages.

| Rule (by name) | What in the design breaks it | Resolution, or question for Ty |
|---|---|---|
| "Public on purpose; do not widen what is served" (repo `CLAUDE.md`) | `wiki.html` and `wiki/` are new published files | Ty's say-so is in the intent (2026-10-07). `.pages-allow` lines go in **their own PR first**, as the repo requires: `wiki.html`, `wiki/*.md`, `wiki/*/*.md`, `@wiki/`, `!raw/*.json`, `@raw/`. Raw day files are not served by Pages, but they are readable in the public repo, like the fills. |
| "Strategic objective — true autonomy" (workspace `CLAUDE.md`) | The collector runs on the Mac | Unavoidable: the bots run on the Mac and write only there. Recorded as Mac debt. If the bots move to a server later, the collector moves with them. The routine itself stays cloud-only. |
| The routine's own "never use a remote-devices/Mac tool" | — | Kept. The Mac pushes to Drive; the routine only reads Drive, as it already does for the CSVs. |
| "Routine updates use the live config" (memory) | The prompt gains one line | Built from a same-turn `get`, appending one line only, then the update is read back and diffed against the `get`: the only change may be that line. |
| "Artifact mirror contract" | The preview is built from `index.html` only; `wiki.html` is a second page | **Ty, 2026-10-07: the Cowork preview shows the wiki as well.** The same preview (never a second artifact) carries `wiki.html` as a supporting page and the changed `wiki/*.md` as supporting files, so its Wiki link opens the wiki inside the preview. The routine's existing preview step publishes only the wiki files that changed that run, then republishes the page alone, per the contract's mechanics. Its URL stays out of sight. |
| Pipeline Wiring page (artifact mirror contract) | A pipeline change | Row update + dated section-7 entry, in the ship turn. |
| "Light only" + any new colour is a token (README "Look") | New page | `wiki.html` copies `index.html`'s tokens; no new colour. |
| No credential in the repo (runbook "Credentials") | The collector needs Alpaca keys and a Drive token | Both stay on the Mac: keys read in place from `orb-options/.env`; rclone's own config holds the Drive token. Nothing credential-like enters this repo. |
| "Raw day never edited" vs. a re-run | A second run the same day | `postexit.py` refuses to overwrite an existing `raw/<day>.json`; the wiki may change, the raw file may not. |
| Entity separation | — | Personal journal, personal bots; no work-entity content. None found. |
| Bots untouched (intent) | — | The collector only reads bot files. None found. |

## Security
```
## Security (secure-pages, 2026-10-07)
1 Secrets ........ PASS (tree 0, history 0, no JWTs)
2 Visibility ..... PUBLIC — PASS (fills are public by Ty's ruling 2026-09-29; bot logs checked: no account ids, no tokens)
3 Pages .......... PASS (Actions workflow, `.pages-allow` allowlist; raw/ will be listed as not published)
4 Supabase ....... N/A (not used)
Verdict: safe to ship, provided the collector's field allowlist is the only path bot data takes into the repo
```

## Promise
Measured on the first trading-day run after merge (target: the 11:00 Hanoi run on 2026-10-09 or the first run
after merge, whichever is later) and on the first Saturday run after merge (target 2026-10-10, else 2026-10-17):

1. `raw/<day>.json` exists on `main`; its bot trade count equals the `close` rows in that day's v7 journal plus the
   sweep log's `EXIT` lines; its manual fill count equals the fills that day in the month shard; every exit and skip has
   10 three-minute candles and a close. Check: `python3 tools/wiki-check.py --day <day>`. Pass line:
   `RAW OK trades=<n> skips=<n> manual=<n> paths=complete`.
2. Wiki links: `python3 tools/wiki-check.py` prints `WIKI OK pages=<n> dangling=0 uncited=0`.
3. Saturday: `wiki/weekly/<yyyy-Www>.md` exists, under 600 words, every number labelled. Pass line from
   `wiki-check.py --weekly`: `WEEKLY OK words=<n> unlabelled=0`.
4. On the phone: the verifier opens https://ttrng3.github.io/Trade-Journal/wiki.html at 390 px wide, and the
   screenshot shows the weekly report (Saturday) or the latest day page (other days) with working links.
5. `node tools/sync.js --csv-dir <empty> --check` still prints `"changedFiles": []` (journal untouched).

This becomes `verification/bot-trading-wiki.md` in Stage 4.

## Changes during the build
- Review of PR #14 (2026-10-07): the wiki step runs before the preview refresh, not after it, so each run's
  preview carries that run's wiki. Raw files described as readable in the public repo, not private.
- Review of PR #15 (2026-10-08): Promise 1 counts finished bot trades, i.e. v7 `close` rows plus sweep `EXIT`
  lines (a trade still open at the bell has no exit to follow). A manual exit on an underlying outside the
  collector's list prints `WARN manual path missing` instead of failing the day. Weekly page names keep the ISO
  capital W (`weekly/2026-W41`). The two cdnjs scripts carry SRI hashes.
- Review round 2 of PR #15 (2026-10-08): a day with no Webull fills yet is **deferred**, not frozen; the next run
  writes it with `--final` (docs/wiki.md "Which day"), so a CSV filed before the next run is kept (one
  run of lateness; a CSV filed later than that is not). A v7 skip with no
  stop or target logged is recorded as `first_hit: unknown` instead of stopping the day.
- **For Ty's ship:** rebuilding `build/artifact.html` for the Wiki link also catches the Cowork preview up with
  the rules-check feature already on `main` (`work/261003-rules-check`), which was merged without a fragment
  rebuild. Shipping #15 accepts that catch-up here rather than in its own PR.
- Review round 3 of PR #15 + the v8 split (2026-10-08): Ty approved the split ("proceed with the split", relayed
  by the v8 session): Trade-Journal stays the compiler, wiki and weekly report and computes every path-dependent
  number (MFE/MAE, post-exit paths, target-or-stop-first, shadow exits); v8 (orb-options, built by tytr3-69)
  writes only decision-time facts and sends its field list before it builds; the collector's allowlist keeps
  dropping unknown fields. v7's `stop_move` and `green` rows are now collected and attached to each bot trade.
  Catch-up days download their own bundle and pass `RAW OK` before compiling; pages say "Manual trades", never a
  name beside money; `wiki-check.py` reports `uncited=` apart from `dangling=`; the rclone remote is settable.

## Out of scope
- Any change to the bots, their schedules or drills, and any automatic tuning. The weekly report proposes; Ty
  decides on Friday.
- Backtests or what-ifs beyond the session's own prices.
- Option-price what-ifs (the path is the underlying's; option prices after exit need quote history we don't keep
  for Ty's trades).
- Telegram or push alerts for the wiki.
- Moving the bots off the Mac.
