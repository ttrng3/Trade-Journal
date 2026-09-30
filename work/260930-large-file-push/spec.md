# Spec

Status: approved by Ty 30/09 ("Approve the 4 specs but skip Teams", in chat).

Evidence (checked 30/09): since 2026-09-24 the five fill runs (`8bf3820`, `b15a638`, `88f27af`, `70f95e4`, `2663407`) each changed `.last-check`, the 2026-09 shard and `index.json` in one commit authored by the Claude bot account; the five heartbeat-only runs changed `.last-check` alone, authored `ttrng3`. The 2026-09-30 run log states it pushed with shell git through the session's credential proxy because `create_or_update_file` would pass the 351 KB shard inline.

- `docs/nightly-sync.md`: new section *Pushing*: shell `git push` is the path for any run that changes a month shard; the GitHub MCP file tools are the fallback for small files (heartbeat); a non-fast-forward refusal gets one `git pull --rebase` and a second push; any other refusal, or a second one, is reported BLOCKED, the shard is not re-sent through the file tools, the heartbeat still goes out alone through the file tools with `newest-source=BLOCKED: push refused`, the preview step runs as usual, and the next run catches up; the runbook says the 14-day data-age check is the only automatic alarm for repeated refusals (it re-reads every CSV and dedups by key). The "a few KB" sentence, the Mac-bound "push" bullet, *Verifying a run* (how to confirm `main` moved after a shell push) and *Credentials* are corrected to match.
- `CLAUDE.md`: the one line saying the push uses the MCP file tools points at *Pushing*.
- Docs only: no workflow, code, data or routine prompt change.
- Rejected: splitting month shards smaller (changes the 80 KB page engine; too many moving parts).
- Known gap, left for Ty: the routine prompt still names the MCP tools as primary. The prompt says the runbook wins, so the runbook now governs; rewording the prompt is a routine change and gets its own go-ahead.
- Promise (checkable): the next fill run's commit changes the shard, `index.json` and `.last-check` in one commit and its report names shell git as the path; `git diff main -- tools data index.html .github` is empty for this PR.
