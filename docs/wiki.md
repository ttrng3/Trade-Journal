# Trading wiki — compile runbook

Canonical for the wiki step of the daily routine. The routine runs it **after the Webull sync and before the
preview step**, so the preview stays the last step. Spec: `work/261007-bot-trading-wiki/spec.md`.

The method is Karpathy's LLM wiki: `raw/<day>.json` is the source (written once, never edited), you are the
compiler, and `wiki/` is the compiled output, organised by concept and linked. A new day adds evidence to the
pages that already exist; it does not only append a dated log.

## Which day

The routine fires 11:00 Hanoi, Tuesday to Saturday. Compile the **previous US session**: the run's Hanoi date
minus one day (Tuesday's run compiles Monday's session, Saturday's compiles Friday's). Call it `<day>`.

## Steps

1. **Bundle.** With the Drive connector, look in `09 Trading/Trade Journal/Raw Records/Bots/` for `<day>.json` and
   download it. It is written by the Mac at 10:30 Hanoi. If it is absent, go on without it: Ty's trades are still
   compiled, and the day page says "bot bundle missing".
2. **Raw day.** `python3 tools/postexit.py --day <day> --bundle <file or omit>`. It writes `raw/<day>.json` and
   refuses to overwrite one that exists (that is correct on a re-run: compile from the existing file).
   Then `python3 tools/wiki-check.py --day <day> [--bundle <file>]` must print `RAW OK …`. If it fails, stop the
   wiki step, push nothing under `raw/` or `wiki/`, and report the FAIL lines. A `WARN manual path missing` line
   (Ty traded an underlying the collector had no bars for) does not stop the step; say it on the day page.
3. **Compile.** Read `raw/<day>.json` and the current `wiki/`. Write or update, in place:
   - `wiki/days/<day>.md` — the day (template below). It must contain the text `raw/<day>.json`.
   - The concept pages the day touches, under `wiki/mistakes/`, `wiki/setups/`, `wiki/what-ifs/`, `wiki/rules/`.
     Reuse a page when one fits; create one only when none does. Never delete a page or an evidence line.
   - `wiki/index.md` — the map: latest weekly report first, then the last 10 days, then every concept page by
     section, each as a `[[link]]`.
4. **Saturday only.** Write `wiki/weekly/<yyyy-Www>.md` for the ISO week of `<day>` (template below), link it at
   the top of `wiki/index.md`, then `python3 tools/wiki-check.py --weekly wiki/weekly/<yyyy-Www>.md` must print
   `WEEKLY OK …`.
5. **Check.** `python3 tools/wiki-check.py` must print `WIKI OK … dangling=0`. Fix any dangling link before pushing.
6. **Push.** One commit, `wiki: <day>`, holding `raw/<day>.json` and the changed `wiki/` files, pushed the same way
   the runbook pushes data (`docs/nightly-sync.md`, "Pushing"). A wiki failure never blocks or undoes the
   journal's own data push.
7. **Preview.** The preview step that follows also sends `wiki.html` and every `wiki/` file this run changed as
   supporting files of the same preview (changed files only), then republishes the page alone, as the README
   describes. Never a second preview; its URL is never written anywhere.

## Mac collector

The bots run on the Mac and write only there, so `tools/bot-collect.py` runs there at 10:30 Hanoi, Tuesday to
Saturday (launchd `com.ty.bot-collect`), and copies `Raw Records/Bots/<day>.json` to Drive with rclone. It reads
the bots' files, never writes them, and keeps only allowlisted fields. Log: `~/Library/Logs/bot-collect.log`.
This is the pipeline's one Mac dependency; the routine itself stays cloud-only.

Install or reinstall, on the Mac, from the main checkout (the account is the one in the Drive for desktop folder
name `~/Library/CloudStorage/GoogleDrive-<account>`, so it is never written into this repo):

    acct=$(ls ~/Library/CloudStorage | sed -n 's/^GoogleDrive-//p' | head -1)
    sed -e "s|__HOME__|$HOME|g" -e "s|__ACCOUNT__|$acct|g" tools/com.ty.bot-collect.plist > ~/Library/LaunchAgents/com.ty.bot-collect.plist
    launchctl unload ~/Library/LaunchAgents/com.ty.bot-collect.plist 2>/dev/null; launchctl load ~/Library/LaunchAgents/com.ty.bot-collect.plist

Run once by hand: `launchctl start com.ty.bot-collect`, then read the log's last line (`uploaded`).

## Rules for every page

- **Numbers come from `raw/` only, copied or computed in code** (`python3 -c …` over the raw files). Never from
  memory, never estimated. Each number carries its source: `(Verified: raw/2026-10-06.json)`.
- **Drills are not trades.** v7 drills (`"drill": true`) are wiring tests; list them under "Drills" on the day
  page and never count them in win/loss, P&L or a mistake.
- **Skips are what-ifs.** A skip's `first_hit` says whether the setup would have reached its target or its stop
  first. Count them per bot and per reason; a reason that keeps blocking winners is a what-if page.
- **After an exit:** `after.candles` are the next 10 three-minute candles. Say plainly whether holding would
  have helped (price went further the trade's way) or hurt. A path with `proxy` (SPX via SPY × 10) says so.
- **Public repo.** No account numbers, no broker ids, no personal data, no work-entity names, no preview URL.
- Links are `[[section/page]]` without `.md`, e.g. `[[mistakes/tight-stop]]`. Slugs are lowercase kebab-case.
- Plain prose, short. No filler, no "overall", no em-dash chains.

## Templates

**Day page** (`wiki/days/<day>.md`):

    # <day> (<weekday>)
    Source: raw/<day>.json · bot bundle: present|missing

    ## Result
    One or two sentences: Ty's net, each bot's net, the key number. (Verified: raw/<day>.json)

    ## Ty's trades
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
