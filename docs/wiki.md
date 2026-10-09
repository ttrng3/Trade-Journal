# Trading wiki — compile runbook

Canonical for the wiki step of the daily routine. The routine runs it **after the Webull sync and before the
preview step**, so the preview stays the last step. Spec: `work/261007-bot-trading-wiki/spec.md`.

The method is Karpathy's LLM wiki: `raw/<day>.json` is the source (written once, never edited), you are the
compiler, and `wiki/` is the compiled output, organised by concept and linked. A new day adds evidence to the
pages that already exist; it does not only append a dated log.

## Which day

The routine fires 11:00 Hanoi, Tuesday to Saturday. The **previous US session** is the run's Hanoi date minus
one day (Tuesday's run compiles Monday's session, Saturday's compiles Friday's). Call it `<day>`.

A raw day is written once, so it must not be written before Ty's CSV has arrived. Each run therefore handles:
- **`<day>`** with `postexit.py --day <day>`. If the shard has no fills for it yet, it prints `{"deferred": true}`
  and writes nothing: Ty may file the export after 11:00 (CLAUDE.md "Known mistakes", 2026-09-26).
- **Every earlier weekday in the last 7 days that has no `raw/<that day>.json`, and is later than the oldest day
  file already in `raw/`** (a deferred day, or a run that failed), with
  `postexit.py --day <that day> --final --bundle <its own Bots/<that day>.json>`, which writes it whether or not
  fills came. A day Ty did not trade therefore lands one run late, with its bot trades; a Friday deferred on
  Saturday lands on Tuesday. The deferral covers one run of lateness: a CSV filed before the next run is kept; one
  filed later than that is not (the day is then frozen without it).
- **The very first run** (no `raw/YYYY-MM-DD.json` yet; `raw/schema.json` does not count) writes `<day>` with
  `--final` and catches up nothing, so no day from before the collector ran is frozen without its bots, and every
  later run has a first day to count from.

Do steps 1–2 for every day this run writes, then compile (steps 3–6) each of them, oldest first.

## Steps

1. **Bundle.** For each day this run writes, look in `09 Trading/Trade Journal/Raw Records/Bots/` for that day's
   `<day>.json` with the Drive connector and download it.
   It is written by the Mac at 10:30 Hanoi. If it is absent, go on without it: the manual trades are still
   compiled, and the day page says "bot bundle missing".
2. **Raw day.** `python3 tools/postexit.py --day <day> --bundle <file or omit>`. It writes `raw/<day>.json` and
   refuses to overwrite one that exists (that is correct on a re-run: compile from the existing file).
   If it printed `{"deferred": true}`, `{"holiday": true}` or `{"skipped": true}` (no fills and no bundle: nothing
   to journal), skip the check and the compile for that day; none of these writes a file. If it printed
   `{"exists": true}`, the day was written by an earlier run: skip the check (the shard may have grown since) and
   compile from the existing file. Otherwise `python3 tools/wiki-check.py --day <day> [--bundle <file>]`
   must print `RAW OK …`. If it fails, stop the
   wiki step, push nothing under `raw/` or `wiki/`, and report the FAIL lines. This check runs for **every** raw
   day the run writes, catch-up days included. A `WARN manual path missing` line
   (Ty traded an underlying the collector had no bars for) does not stop the step; say it on the day page.
3. **Compile.** Read `raw/<day>.json` and the current `wiki/`. Write or update, in place:
   - `wiki/days/<day>.md` — the day (template below). It must contain the text `raw/<day>.json`.
   - The concept pages the day touches, under `wiki/mistakes/`, `wiki/setups/`, `wiki/what-ifs/`, `wiki/rules/`.
     Reuse a page when one fits; create one only when none does. Never delete a page or an evidence line.
   - `wiki/hypothesis-ledger.md` — never compiled from a day. Leave it as it is unless the day's bundle shows a
     `setup` value (other than `drill`) that no row's `bundle name` holds; then add an `untested` row for it in the
     bots and setups table with the next `H` id. Agent rows are added only by the session that builds the agent.
     Rows are added or appended to, never rewritten.
   - `wiki/index.md` — the map: latest weekly report first, then the Hypothesis ledger link, then the last 10 days, then every concept page by
     section, each as a `[[link]]`.
4. **Saturday only.** Write `wiki/weekly/<yyyy-Www>.md` for the ISO week of `<day>` (template below), link it at
   the top of `wiki/index.md`, then `python3 tools/wiki-check.py --weekly wiki/weekly/<yyyy-Www>.md` must print
   `WEEKLY OK …`. If a day of that week was deferred, the report says which; the run that later writes that day
   also updates that week's report.
5. **Check.** `python3 tools/wiki-check.py` must print `WIKI OK … dangling=0 uncited=0`. Fix any broken link or
   missing citation before pushing.
6. **Push.** One commit, `wiki: <day>`, holding `raw/<day>.json` and the changed `wiki/` files, pushed the same way
   the runbook pushes data (`docs/nightly-sync.md`, "Pushing"). A wiki failure never blocks or undoes the
   journal's own data push.
7. **Preview.** The preview step that follows also sends `wiki.html` and every `wiki/` file this run changed as
   supporting files of the same preview (changed files only), then republishes the page alone, as the README
   describes. Never a second preview; its URL is never written anywhere. `wiki/hypothesis-ledger.md` is sent on every run whether or not it changed, so the preview always holds it.

## Mac collector

The bots run on the Mac and write only there, so `tools/bot-collect.py` runs there at 10:30 Hanoi, Tuesday to
Saturday (launchd `com.ty.bot-collect`), and copies `Raw Records/Bots/<day>.json` to Drive with rclone. It reads
the bots' files, never writes them, and keeps only allowlisted fields. Log: `~/Library/Logs/bot-collect.log`.
This is the pipeline's one Mac dependency; the routine itself stays cloud-only. Each run uploads **every** weekday
of the last 7 days that has no bundle on Drive yet, so a Mac asleep for days catches up on wake (launchd merges
missed runs into one). A weekday with no bars for any symbol is uploaded with `"holiday": true`.

Install or reinstall, on the Mac, from the main checkout:

    sed -e "s|__HOME__|$HOME|g" tools/com.ty.bot-collect.plist > ~/Library/LaunchAgents/com.ty.bot-collect.plist
    launchctl unload ~/Library/LaunchAgents/com.ty.bot-collect.plist 2>/dev/null; launchctl load ~/Library/LaunchAgents/com.ty.bot-collect.plist

Run once by hand: `launchctl start com.ty.bot-collect`, then read the log's last line (`uploaded`).

The upload uses the rclone Drive remote named `igdrive:` (set up for the Instagram bridge) and reaches
`Raw Records/Bots/` by its path from My Drive (`--drive-root-folder-id root`), never through the Drive for desktop
mount: macOS does not let a launchd job read that mount (first install, 2026-10-08). A Mac whose remote has another name sets `TJ_RCLONE_REMOTE` (e.g. `gdrive:`) in the
plist's `EnvironmentVariables`.

## Rules for every page

- **Numbers come from `raw/` only, copied or computed in code** (`python3 -c …` over the raw files). Never from
  memory, never estimated. Each number carries its source: `(Verified: raw/2026-10-06.json)`.
  One exception: `wiki/hypothesis-ledger.md` copies its numbers from the bots' study records (not in this repo),
  cited per table as `(Verified: study records)`; nothing on it is recomputed.
- **Drills are not trades.** v7 drills (`"drill": true`) are wiring tests; list them under "Drills" on the day
  page and never count them in win/loss, P&L or a mistake.
- **Skips are what-ifs.** A skip's `first_hit` says whether the setup would have reached its target or its stop
  first. Count them per bot and per reason; a reason that keeps blocking winners is a what-if page.
- **After an exit:** `after.candles` are the next 10 three-minute candles. Say plainly whether holding would
  have helped (price went further the trade's way) or hurt. A path with `proxy` (SPX via SPY × 10) says so.
- **Public repo.** No account numbers, no broker ids, no personal data, no work-entity names, no preview URL.
  **No person's name beside money:** Ty's own trades are "Manual trades" on every page, never his name.
- Links are `[[section/page]]` without `.md`, e.g. `[[mistakes/tight-stop]]`. Slugs are lowercase kebab-case.
- Plain prose, short. No filler, no "overall", no em-dash chains.

## Templates

**Day page** (`wiki/days/<day>.md`):

    # <day> (<weekday>)
    Source: raw/<day>.json · bot bundle: present|missing

    ## Result
    One or two sentences: the manual net, each bot's net, the key number. (Verified: raw/<day>.json)

    ## Manual trades
    Round trips by underlying: entry, exit, P&L, what price did after the exit.

    ## Bot trades
    One line per trade: bot, setup, entry → exit, rule, R, P&L, and what the next 10 candles did.

    ## Drills
    Wiring tests only, not counted.

    ## Skipped and cancelled setups
    Counts by bot: target first / stop first / neither, and the reasons that blocked the winners.

    ## Lessons carried to the next session
    At most three, each linked to its concept page.

**Concept page** (`mistakes/`, `setups/`, `what-ifs/`, `rules/`):

    # <Name>
    What it is, in two sentences.

    ## Evidence
    - <day>: one line, with the number and (Verified: raw/<day>.json) — newest first.

    ## Count so far
    Times seen, and the $ or R it cost or would have made. (Verified: computed over raw/<first>…<last>)

    ## What to do about it
    The proposed change, for the Friday tune. Proposals only; Ty decides.

**Weekly report** (`wiki/weekly/<yyyy-Www>.md`), one page, under 600 words, ty-report-standard:

    # Week <yyyy-Www>
    The answer first: the week's result in one sentence with its key number, labelled.

    ## What worked
    ## What cost money
    ## What-ifs (holding longer, skipped setups, cancelled orders)
    ## Proposed for the Friday tune
    ## Risks and tripwires

Every paragraph, list item or table row that holds a number also holds its label (`Verified: raw/…`,
`Likely (basis: …)` or `Assumption: …`); `wiki-check.py --weekly` fails it otherwise.
