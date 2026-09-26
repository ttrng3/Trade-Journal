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

## One surface, on purpose

    schedule → cloud routine → source → GitHub → Pages

**GitHub Pages is the only published surface.** Ty ruled on 2026-09-23 that he
wants control over what exists of his work, so there is no claude.ai artifact
copy of this dashboard: the Pages URL above is the address, full stop.

**The rule, as Ty set it on 2026-09-26:** where a GitHub Pages link already
exists, Pages is the only surface and no claude.ai artifact may exist for the
same content. An artifact is the fallback only for work that has no Pages link.
A mirror artifact existed for a few hours on 2026-09-23 and was deleted; a
second one was recreated on 2026-09-24 and deleted on 2026-09-26, and the
routine no longer has the Artifact tool at all. Do not recreate one, and do not
add an artifact URL to this repo. `tools/build-fragment.py`
is kept only because it is the one thing that can derive a standalone fragment
of this page if it is ever needed; nothing in the refresh calls it.

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
