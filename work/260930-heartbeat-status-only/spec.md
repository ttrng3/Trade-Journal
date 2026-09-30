# Spec

Status: approved by Ty 30/09 ("approve for all four", in chat).

- `tools/sync.js`: on a run that writes files, the heartbeat line becomes `<generatedUtc> newest-source=<YYYY-MM-DD of the newest fill this run added> new fills`, or `<generatedUtc> newest-source=no new fills`. No CSV names, no counts. The first token stays the stamp. The date is tracked as fills are added, not taken from each import's last field.
- `docs/nightly-sync.md`, "The heartbeat": one paragraph documenting that format and that readers use only the stamp.
- Not covered: `data/index.json` `meta.imports` (served) still holds CSV names and counts; changing it is Ty's call in its own work folder.
- Unchanged: the run's stdout summary (not committed), the BLOCKED heartbeat line the runbook already defines, quiet nights (the routine writes those), commit messages (the routine prompt writes them).
- Readers checked: `.github/scripts/freshness.py` reads only the first `\S+` token; pipeline-wiring's `tools/collect_status.py` splits on the first space and no longer publishes the note.
- Promise (checkable): a dry run on a scratch copy with one sample fill writes `<stamp> newest-source=<date> new fills`; `freshness.py` on that copy prints `stale=false`; the next real fill run's `.last-check` contains no `.csv` and no digit run other than the stamp and date.
