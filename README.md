# Trade Journal

A private Webull options journal. **This repo is the source of truth** —
`data/fills/<YYYY-MM>.json` holds the fills, `data/index.json` is the manifest,
and https://ttrng3.github.io/Trade-Journal/ renders them. The page is the same
engine that runs inside Claude, reading the static snapshot.

    Webull CSV (Google Drive) → cloud routine → GitHub → Pages

`docs/nightly-sync.md` is the runbook and outranks the routine prompt and any
stored memory. `tools/sync.js` is the whole pipeline; run it with `--check` to
see what a sync would change without writing.

## Artifact mirror

The chain is **repo-first**, the same shape KSNB has always used:

    schedule → cloud routine → source → GitHub → Pages → artifact mirrored after

**The repo is the source of truth and Pages is the live surface.** The artifact
is a **mirror**, published *after* the repo is correct, and never authoritative.
**Its URL is not recorded here on purpose.** The Pages link above is this page's
address; a claude.ai artifact link would be a second address for the same thing,
and a private one most readers of this repo could not open anyway. The routine
prompt holds the target URL, because that is the only place that needs it. If the two ever disagree, the repo
wins and the artifact is what gets corrected.

How a refresh mirrors it, in this order:

1. Write and verify the repo first. Do not touch the artifact until `main` has
   moved and you have read the commit back.
2. Publish the changed data paths — data/index.json and the changed data/fills/<YYYY-MM>.json — with the artifact's `url` set.
   Files you omit are kept, so a refresh is a small write.
3. Republish the page only when the **renderer** changed, and then publish the
   `tools/build-fragment.py` output, never `index.html` itself. The artifact
   service wraps what you give it, so a complete document nests inside another,
   the inner `<head>` is discarded, and the page renders **blank with no
   console error**. To tell that apart from the other blank cause, read the
   artifact's `index.html` back and count `<html>` tags: two means it nested,
   one means the markup is fine and it is the same-call publish problem.
4. **A failed mirror must never make you undo or retry the repo write.** Report
   it and stop; the site is already correct.

`tools/reconcile.py` diffs this repo's `data/` against the artifact's copy and
says which side is newer.

**Why the ordering is stated this bluntly.** On 2026-09-23 the TMDV artifact was
found *ahead* of its repo, carrying four fixes that had never been committed,
and the ECOPM artifact was found a whole renderer generation *behind*. Neither
was caught by the freshness guards, because both read data timestamps and the
drift was in the page. Repo-first is what keeps that from recurring.

The renderer still carries a `window.claude.use('db')` branch from that era. It
is inert outside an artifact (the guard falls through to the static snapshot)
and is left in place deliberately rather than risking an edit to the engine.
