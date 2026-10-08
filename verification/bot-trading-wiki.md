# Verification: the trading wiki

## Promise
For a finished session, the Mac bundle carries only allowlisted bot fields; `raw/<day>.json` holds every Webull
fill of that day, every bot exit and every skipped setup with a 10-candle path (written once, never overwritten);
`wiki-check.py` passes; and `wiki.html` renders a wiki page with working `[[links]]`, at phone width, with
injected HTML neutralised and a hostile page address falling back to the index.

## Clean state
Run on the Mac from the repo root (a worktree is fine). Pick a finished session `D` that has a sweep or v7 log,
e.g. `2026-10-06`. Work in a scratch folder `$S` outside the repo; nothing under `raw/` or `wiki/` in the repo is
written. Serve the scratch site with `python3 -m http.server 8765 --bind 127.0.0.1 --directory $S/site` and
kill it afterwards (`lsof -ti:8765 | xargs kill`).

## Steps
1. `python3 tools/bot-collect.py --day D --out $S/b.json --no-upload` → one JSON line with `v7_rows`, `sweep_lines`,
   `bars` > 0.
2. `python3 tools/postexit.py --day D --bundle $S/b.json --raw-dir $S/raw` → `{"file":…,"manual":n,"bots":n,…}`.
   Run it a second time → `{"exists": true, …}`, and the file's sha256 is unchanged.
3. `python3 tools/wiki-check.py --day D --bundle $S/b.json --raw-dir $S/raw` → `RAW OK … paths=complete`.
4. `python3 tools/postexit.py --day D --raw-dir $S/raw-nobundle` (no bundle) → writes the file with
   `"bots_bundle": "missing"`, manual count unchanged; `wiki-check.py --day D --raw-dir $S/raw-nobundle` → `RAW OK`.
   **Late CSV:** pick a weekday `E` with no fills in its shard (e.g. one in a month with no shard yet), and make
   `$S/bE.json`, a copy of the D bundle with `"day"` set to `E`. `postexit.py --day E --bundle $S/bE.json --raw-dir
   $S/raw-late` → `{"deferred": true, …}` and no file; the same with `--final` → writes `raw-late/E.json` with
   `manual` 0. With **no** bundle, `postexit.py --day E --final --raw-dir $S/raw-empty` → `{"skipped": true, …}` and
   no file (nothing to journal).
   **Holiday:** copy the D bundle with `"holiday": true` and `bars_1m.SPY = []` → `postexit.py --day D --bundle <copy>
   --raw-dir $S/raw-hol` prints `{"holiday": true, …}` and writes nothing.
5. Build `$S/site`: copy `wiki.html`; write `wiki/index.md` linking `[[days/D]]`, a day page citing `raw/D.json`
   with a table and a `[[what-ifs/x]]` link, the page `what-ifs/x.md`, and `what-ifs/evil.md` containing
   `<img src=x onerror="window.__xss=1"><script>window.__xss=2</script>`.
   `python3 tools/wiki-check.py --wiki-dir $S/site/wiki` → `WIKI OK … dangling=0 uncited=0`.
6. In a **fresh** headless Chrome profile at 390×844, open `http://127.0.0.1:8765/wiki.html#p=days/D`, then
   `#p=what-ifs/evil`, then `#p=../../index`, evaluating the step-6 expression on each. Screenshot the day page.
7. `node tools/sync.js --csv-dir <empty dir> --check` → `"changedFiles": []` (the journal is untouched).

## Invariants
Steps 1–4 and 7, in one Python run (print the object): `scrub` is `tools/postexit.py`'s, imported.

```python
{
 "bundle_fields_allowlisted": all(set(r) <= {"kind"} | set(V7_KEEP[r["kind"]]) for r in b["v7"]),  # V7_KEEP from tools/bot-collect.py
 "bundle_no_broker_ids": not re.search(r'"(conId|account|acct|orderId|permId)"', open(f"{S}/b.json").read()),
 "raw_manual_equals_shard": len(raw["manual"]) == sum(f["t"].startswith(D) for f in shard.values()),
 "raw_written_once": sha_before == sha_after,
 "raw_ok": "RAW OK" in check_day_out,
 "nobundle_still_writes_manual": nb["sources"]["bots_bundle"] == "missing" and len(nb["manual"]) == len(raw["manual"]),
 "no_fills_day_deferred": deferred_out.get("deferred") is True and not existed_after_defer,  # checked before the --final run
 "final_writes_no_fills_day": os.path.exists(f"{S}/raw-late/{E}.json") and late["manual"] == [],
 "empty_day_skipped": empty_out.get("skipped") is True and not os.path.exists(f"{S}/raw-empty/{E}.json"),
 "holiday_not_written": holiday_out.get("holiday") is True and not os.path.exists(f"{S}/raw-hol/{D}.json"),
 "scrub_keeps_setups": scrub("bot1_st_flip") == "bot1_st_flip" and scrub("bot2_late_momo") == "bot2_late_momo",
 "scrub_catches_ids": scrub("acct DU" + "1" * 7) == "acct [id]" and scrub("order " + "8" * 7) == "order [id]"
                      and scrub("exec " + "a1b2" * 3) == "exec [id]",   # ids built at run time, none typed here
 "reasons_scrubbed": not any(re.search(r"\b(?=(?:[A-Za-z_-]*\d){5})[A-Za-z0-9_-]{6,}\b", s["why"] or "") for s in raw["skips"]),
 "wiki_ok": "dangling=0 uncited=0" in check_wiki_out,
 "journal_untouched": sync_check["changedFiles"] == [],
}
```

Step 6, in the page:

```js
({h1: document.querySelector('article h1')?.textContent || '',
  internal_links: [...document.querySelectorAll('article a[href^="#p="]')].length,
  tables_wrapped: [...document.querySelectorAll('article table')].every(t => t.parentElement.classList.contains('tbl')),
  no_hscroll: document.documentElement.scrollWidth <= innerWidth,
  xss_fired: window.__xss || 0,
  error_shown: !!document.querySelector('article .err')})
```
Day page: `h1` starts with `D`, `internal_links ≥ 1`, `tables_wrapped`, `no_hscroll`, `xss_fired == 0`.
Evil page: `xss_fired == 0`. Hostile address `#p=../../index`: renders the index (its `h1`), `error_shown` false.

## Adversary
- **A stranger on the public site** gets the compiled wiki only. `raw/` is not served (`!raw/*.json` in
  `.pages-allow`); after merge `curl -o /dev/null -w '%{http_code}' …/raw/schema.json` → `404`, `…/wiki.html` → `200`.
- **A bot that starts logging something new** (a broker id, an account field) cannot leak it: the collector keeps
  only `V7_KEEP` fields and `SWEEP_KEEP` lines → `bundle_fields_allowlisted`, `bundle_no_broker_ids`; free-text
  reasons are scrubbed of id-like tokens before they reach `raw/` → `reasons_scrubbed`.
- **A market holiday** (no SPY bars) is never written as a day → `holiday_not_written`.
- **A wiki page carrying HTML** (the compiler copies a symbol or reason text that contains markup) → sanitised by
  DOMPurify → `xss_fired == 0` on `what-ifs/evil`.
- **A crafted address** (`#p=../../index`, `#p=//evil`) → the page path is checked against `^[A-Za-z0-9][A-Za-z0-9\-/]*$` (upper case for `weekly/2026-W41`)
  and falls back to the index.
- **A second run the same day** (routine retried) → `raw_written_once`.
- **The Mac off at 10:30** → no bundle → `nobundle_still_writes_manual`; the day page says "bot bundle missing".
- **Ty files the CSV after 11:00** → the day has no fills yet → `no_fills_day_deferred`, then the next run's
  `--final` writes it → `final_writes_no_fills_day` (with his fills, if they arrived by then).

## Sanctioned substitutes
- Before merge, `wiki/` on main holds no compiled day, so step 6 runs on the scratch site built in step 5 from
  hand-written pages. It proves the renderer, links, sanitising and phone layout; it does not prove the routine's
  compile (that is the first daily run's check, below).
- The upload to Drive is skipped (`--no-upload`) so a protocol run never writes to Drive. Proving the upload is
  the install step in `docs/wiki.md` ("Run once by hand … `uploaded`").

## Evidence
The invariants object from steps 1–4 and 7, the three step-6 objects, and one screenshot of the day page at
390 px wide, saved to disk.

**After merge, on the first compiled run** (not part of a pre-merge run): `wiki-check.py --day <day>` and
`wiki-check.py` on `main` print their OK lines, and a fresh-profile screenshot of
`https://ttrng3.github.io/Trade-Journal/wiki.html` shows the latest day page. On the first Saturday run,
`wiki-check.py --weekly wiki/weekly/<yyyy-Www>.md` prints `WEEKLY OK`.

## Not covered
- Whether the compiler's prose is right: the checks prove links, citations, counts and labels, not judgment.
- The Cowork preview's copy of the wiki (step 4 of `verification/journal.md` covers the preview itself).
- Option-premium what-ifs: paths are the underlying's price.

## Traps
- A session that is still open (or closed less than 15 minutes ago) gets a 403 for SIP bars on the free plan;
  the collector falls back to IEX, so bars from a same-day run differ slightly from the next day's.
- The Webull shard and the 11:00 run are a day apart from the session: the run on Hanoi day `N` compiles US
  session `N − 1`.
- Never read `localStorage` in Ty's own Chrome for this; the wiki keeps none, and the journal's keys are his.
