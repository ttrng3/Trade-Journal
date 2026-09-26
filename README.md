# Trade Journal

A private Webull options journal. **This repo is the source of truth** —
`data/fills/<YYYY-MM>.json` holds the fills, `data/index.json` is the manifest,
and https://ttrng3.github.io/Trade-Journal/ renders them. The page is the same
engine that runs inside Claude, reading the static snapshot.

    Webull CSV (Google Drive) → cloud routine → GitHub → Pages

`docs/nightly-sync.md` is the runbook and outranks the routine prompt and any
stored memory. `tools/sync.js` is the whole pipeline; run it with `--check` to
see what a sync would change without writing.

A full backup of `data/` is attached to a release on the 1st of each month;
`docs/backup.md` covers where it lands and how `tools/restore.js` feeds it back.

## One address, one preview

    schedule → cloud routine → source → GitHub → Pages (the address) → artifact (Cowork preview)

**https://ttrng3.github.io/Trade-Journal/ is the only link.** A claude.ai
artifact exists as the Cowork preview of this page, refreshed by the routine as
the last step of every run, but its URL is never written here, in a Drive doc,
or in a run report — Ty ruled on 2026-09-24 and again on 2026-09-26 that content
with a Pages address gets no second link. The preview must exist: "no artifact
link" means the URL stays out of sight, never that the artifact goes. It was
wrongly deleted on 2026-09-23 and again on 2026-09-26 by reading the rule as
"no artifact"; do not make that a third time. Only the routine prompt carries
the URL, because the job needs a publish target. `tools/build-fragment.py`
derives the fragment the artifact needs from `index.html`.

## What the page itself can save

Nothing in the browser can write to this repo, so the Pages build is a
**nightly snapshot plus a per-browser overlay**. A Webull CSV dropped on the
page (or picked with *Import Webull CSV*) is parsed and merged at once, and the
new fills, together with notes and settings saved on the page, live in that
browser's `localStorage` on top of the snapshot. They survive reloads. They do
not reach other devices until the same export is put in `Raw Records/` on
Drive and the nightly sync commits it; at the next load the overlay prunes any
fill the snapshot now carries, so it never disagrees with the repo and never
grows. The status line in the header says how many fills are overlay-only.

## Look

`index.html` is hand-maintained — `tools/sync.js` and the nightly routine write
`data/` only and never touch it. Its visual system is Apple HIG. **Light only — Ty ruled 2026-09-24** (dark mode ran for one morning and was withdrawn): the page stays light whatever the viewer's system setting, and there is no dark theme. Do not add one back. Base tokens sit in the first `<style>`, then
`<style id="apple-layer">` adds materials, translucent header and accessibility
fallbacks; the TradingView embed is pinned to its light theme. `--accent`
means *positive P&L* (green); interactive chrome is `--blue`. Any new colour must
be a token — no raw hex on screen.
