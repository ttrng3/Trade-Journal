# Trading wiki — compile runbook

Canonical for the wiki step of the daily routine. The routine runs it **after the Webull sync and before the
preview step**, so the preview stays the last step. The wiki holds Ty's own trades only.

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
  `postexit.py --day <that day> --final --bars <its own Bars/<that day>.json>`, which writes it whether or not
  fills came. A Friday deferred on Saturday lands on Tuesday. The deferral covers one run of lateness: a CSV filed
  before the next run is kept; one filed later than that is not (the day is then frozen without it).

Do steps 1–2 for every day this run writes, then compile (steps 3–6) each of them, oldest first.

## Steps

1. **Bars.** For each day this run writes, look in `09 Trading/Trade Journal/Raw Records/Bars/` for that day's
   `<day>.json` with the Drive connector and download it. It is written by the Mac at 10:30 Hanoi. If it is
   absent, go on without it: the trades are still compiled, and their price paths read "bars missing".
2. **Raw day.** `python3 tools/postexit.py --day <day> --bars <file or omit>`. It writes `raw/<day>.json` and
   refuses to overwrite one that exists (that is correct on a re-run: compile from the existing file).
   If it printed `{"deferred": true}`, `{"holiday": true}` or `{"skipped": true}` (no fills and no bars: nothing
   to journal), skip the check and the compile for that day; none of these writes a file. If it printed
   `{"refused": true}` (exit 2), the bars file carries fields outside the bars format: write nothing for that day
   and report it. If it printed `{"exists": true}`, the day was written by an earlier run: skip the check and
   compile from the existing file. Otherwise `python3 tools/wiki-check.py --day <day>` must print `RAW OK …`. If it
   fails, stop the wiki step, push nothing under `raw/` or `wiki/`, and report the FAIL lines. A
   `WARN manual path missing` line does not stop the step; say it on the day page.
3. **Compile.** Read `raw/<day>.json` and the current `wiki/`. Write or update, in place:
   - `wiki/days/<day>.md` — the day (template below). It must contain the text `raw/<day>.json`.
   - The concept pages the day touches, under `wiki/mistakes/`, `wiki/setups/`, `wiki/what-ifs/`, `wiki/rules/`.
     Reuse a page when one fits; create one only when none does. Never delete a page or an evidence line.
   - `wiki/index.md` — the map: latest weekly report first, then the last 10 days, then every concept page by
     section, each as a `[[link]]`.
4. **Saturday only.** Write `wiki/weekly/<yyyy-Www>.md` for the ISO week of `<day>` (template below), link it at
   the top of `wiki/index.md`, then `python3 tools/wiki-check.py --weekly wiki/weekly/<yyyy-Www>.md` must print
   `WEEKLY OK …`. If a day of that week was deferred, the report says which; the run that later writes that day
   also updates that week's report.
5. **Check.** `python3 tools/wiki-check.py` must print `WIKI OK … dangling=0 uncited=0`, and
   `python3 tools/scan_public.py --files <every file this run changed>` must print `scan: 0 hit(s)`. On a scan hit,
   write nothing and report the `REFUSED file:line` lines. Fix any broken link or missing citation before pushing.
6. **Push.** One commit, `wiki: <day>`, holding `raw/<day>.json` and the changed `wiki/` files, pushed the same way
   the runbook pushes data (`docs/nightly-sync.md`, "Pushing"). A wiki failure never blocks or undoes the
   journal's own data push.
7. **Preview.** The preview step that follows also sends `wiki.html` and every `wiki/` file this run changed as
   supporting files of the same preview (changed files only), then republishes the page alone, as the README
   describes. Never a second preview; its URL is never written anywhere.

## Mac bars collector

`tools/bars-collect.py` runs on the Mac at 10:30 Hanoi, Tuesday to Saturday (launchd `com.ty.journal-bars`), and
copies `Raw Records/Bars/<day>.json` to Drive with rclone: one-minute bars for Ty's usual underlyings plus every
underlying in his newest fills month. It pulls market bars only, from Alpaca, with its own key file
(`~/.config/trade-journal/alpaca.env`, mode 600), and opens no other project's files. Log:
`~/Library/Logs/journal-bars.log`. This is the pipeline's one Mac dependency; the routine itself stays cloud-only.
Each run uploads every weekday of the last 7 days that has no bars file on Drive yet, so a Mac asleep for days
catches up on wake. A weekday with no bars for any symbol is uploaded with `"holiday": true`.

Install or reinstall, on the Mac, from the main checkout:

    sed -e "s|__HOME__|$HOME|g" tools/com.ty.journal-bars.plist > ~/Library/LaunchAgents/com.ty.journal-bars.plist
    launchctl bootout gui/$(id -u)/com.ty.journal-bars 2>/dev/null; launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.ty.journal-bars.plist

Run once by hand: `launchctl kickstart gui/$(id -u)/com.ty.journal-bars`, then read the log's last line.

The upload uses the rclone Drive remote named `igdrive:` (set up for the Instagram bridge) and reaches
`Raw Records/Bars/` by its path from My Drive (`--drive-root-folder-id root`), never through the Drive for desktop
mount: macOS does not let a launchd job read that mount. A Mac whose remote has another name sets
`TJ_RCLONE_REMOTE` (e.g. `gdrive:`) in the plist's `EnvironmentVariables`.

## Rules for every page

- **Numbers come from `raw/` only, copied or computed in code** (`python3 -c …` over the raw files). Never from
  memory, never estimated. Each number carries its source: `(Verified: raw/2026-10-06.json)`.
- **After an exit:** `after.candles` are the next 10 three-minute candles. Say plainly whether holding would
  have helped (price went further the trade's way) or hurt. A path with `proxy` (SPX via SPY × 10) says so.
- **Public repo.** No account numbers, no broker ids, no personal data, no work-entity names, no preview URL,
  and nothing `tools/scan_public.py` refuses. **No person's name beside money:** Ty's own trades are "Manual
  trades" on every page, never his name.
- Links are `[[section/page]]` without `.md`, e.g. `[[mistakes/tight-stop]]`. Slugs are lowercase kebab-case.
- Plain prose, short. No filler, no "overall", no em-dash chains.

## Templates

**Day page** (`wiki/days/<day>.md`):

    # <day> (<weekday>)
    Source: raw/<day>.json · bars: present|missing

    ## Result
    One or two sentences: the manual net and the key number. (Verified: raw/<day>.json)

    ## Manual trades
    Round trips by underlying: entry, exit, P&L, what price did after the exit.

    ## Lessons carried to the next session
    At most three, each linked to its concept page.

**Concept page** (`mistakes/`, `setups/`, `what-ifs/`, `rules/`):

    # <Name>
    What it is, in two sentences.

    ## Evidence
    - <day>: one line, with the number and (Verified: raw/<day>.json) — newest first.

    ## Count so far
    Times seen, and the $ it cost or would have made. (Verified: computed over raw/<first>…<last>)

    ## What to do about it
    The proposed change, for the Friday tune. Proposals only; Ty decides.

**Weekly report** (`wiki/weekly/<yyyy-Www>.md`), one page, under 600 words, ty-report-standard:

    # Week <yyyy-Www>
    The answer first: the week's result in one sentence with its key number, labelled.

    ## What worked
    ## What cost money
    ## What-ifs (holding longer)
    ## Proposed for the Friday tune
    ## Risks and tripwires

Every paragraph, list item or table row that holds a number also holds its label (`Verified: raw/…`,
`Likely (basis: …)` or `Assumption: …`); `wiki-check.py --weekly` fails it otherwise.
