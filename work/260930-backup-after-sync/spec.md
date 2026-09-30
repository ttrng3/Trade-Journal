# Spec

Status: approved by Ty 30/09 ("approve for all eight specs", in chat).

- `monthly-backup.yml`: cron `30 2 1 * *` becomes `17 6 1 * *` (13:17 Hanoi), after the 04:00 UTC sync (routine cron `0 4 * * 2-6`), off the top of the hour; the header comment says why.
- `docs/backup.md`: the schedule sentence matches.
- Nothing else changes.
- Promise (checkable): the 1 Oct backup is built from a commit at or after that morning's sync commit (the release notes name the commit; compare it with the sync's `data/.last-check` commit).
- Timing: shipped before 02:30 UTC on 1 Oct (09:30 Hanoi), there is one clean backup at 06:17. Shipped later, the old schedule has already made an early backup; the 06:17 run then replaces the file with `--clobber`, but the release notes keep the early commit id.
