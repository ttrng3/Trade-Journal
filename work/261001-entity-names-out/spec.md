# Spec (awaiting Ty)

Status: awaits Ty's "approve" with the intent.

- `index.html`: the stylesheet comment drops its "modelled on …" note. No visible change; the page's code is otherwise untouched.
- `REVIEW.md`: both entity-separation rules say "no work entity's data, names or numbers" instead of naming them.
- `tools/build-fragment.py`: the comment compares with "renderers that put <title> first" instead of a named repo.
- `tools/reconcile.py`: the docstring's shape table reads "shape A–D" plus this repo's own `shards[]` row. No code change.
- `work/260930-heartbeat-status-only/spec.md`: "the status page's collector" instead of the named repo.
- `build/artifact.html`: rebuilt with `python3 tools/build-fragment.py` from the new page.
- Git history keeps the old wording (Ty's 01/10 ruling for history).
- Promise: a case-insensitive search of every tracked file for the work entities' and their dashboards' names finds nothing; the page renders as before.
