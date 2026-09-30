# Spec (approved)

Status: approved with the intent.

- `monthly-backup.yml`: cron `30 2 1 * *` becomes `0 6 1 * *` (13:00 Hanoi), two hours after the 04:00 UTC sync; the header comment says why.
- `docs/backup.md`: the schedule sentence matches.
- Nothing else changes. Promise: if shipped before 06:00 UTC on 1 Oct (a Thursday, so a sync day), the 1 Oct backup runs after that morning's sync and its fill count equals `data/index.json` `totalFills` at 06:00 UTC.
