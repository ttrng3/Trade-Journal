# Spec (approved)

Status: approved by Ty's ship of this PR (the intent records his instruction).

- `monthly-backup.yml`: cron `30 2 1 * *` becomes `17 6 1 * *` (13:17 Hanoi), after the 04:00 UTC sync (routine cron `0 4 * * 2-6`), off the top of the hour; the header comment says why.
- `docs/backup.md`: the schedule sentence matches.
- Nothing else changes. Promise: if shipped before 06:17 UTC on 1 Oct (a Thursday, so a sync day), the 1 Oct backup runs after that morning's sync and its fill count equals `data/index.json` `totalFills` at 06:17 UTC.
