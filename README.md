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

Ty ruled on 2026-09-23 that the repo URL is what gets used internally and that
the same information must not sit in two places. Until that day a claude.ai
artifact database was the source and this repo was a read-only mirror; the
artifact was deleted and the flow inverted. GitHub Pages is the only reader —
do not recreate an artifact copy.

The renderer still carries a `window.claude.use('db')` branch from that era. It
is inert outside an artifact (the guard falls through to the static snapshot)
and is left in place deliberately rather than risking an edit to the engine.
