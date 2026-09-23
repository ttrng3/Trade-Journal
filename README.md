# Trade Journal

A private Webull options journal. **This repo is the source of truth** —
`data/fills/<YYYY-MM>.json` holds the fills, `data/index.json` is the manifest,
and https://ttrng3.github.io/Trade-Journal/ renders them. The page is the same
engine that runs inside Claude, reading the static snapshot.

    Webull CSV (Google Drive) → cloud routine → GitHub → Pages

`docs/nightly-sync.md` is the runbook and outranks the routine prompt and any
stored memory. `tools/sync.js` is the whole pipeline; run it with `--check` to
see what a sync would change without writing.

## One surface, on purpose

    schedule → cloud routine → source → GitHub → Pages

**GitHub Pages is the only published surface.** Ty ruled on 2026-09-23 that he
wants control over what exists of his work, so there is no claude.ai artifact
copy of this dashboard: the Pages URL above is the address, full stop.

A mirror artifact existed for a few hours that day and was deleted. Do not
recreate one, and do not add an artifact URL to this repo. `tools/build-fragment.py`
is kept only because it is the one thing that can derive a standalone fragment
of this page if it is ever needed; nothing in the refresh calls it.
