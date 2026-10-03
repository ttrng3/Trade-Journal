# Intent: each month, the master backup lands on Drive and last month's CSVs move out of Raw Records

**Status:** accepted 2026-10-03
**Source:** chat, 2026-10-03

**Problem.** The monthly backup Action has made its master file every month since 2026-09-24 (`backup-2026-10-01`: 23,720 fills, 49 months, restore check passes). The file exists only as a GitHub release, and a release dies with the repo. `docs/backup.md` says to download it to Drive by hand each month; that never happened, and the `Backups/` folder didn't exist until 2026-10-03. Meanwhile `Raw Records/` kept every CSV ever dropped, and the nightly sync re-reads all of them on every run.

**Outcome.** These are true from 2026-11-01 on, with nobody present:
1. On the 1st of each month, or the first time the Mac is awake after it, the month's master file is in Drive `09 Trading/Trade Journal/Backups/`. It is byte-identical to the release asset and passes `restore.js --check`.
2. Every CSV in `Raw Records/` whose fills are all already in the journal moves to `Backups/CSVs to <date>/`. Each one is copied, its size and hash are checked, and only then is the original removed. A CSV not yet synced stays where it is.
3. Raw Records then holds only CSVs added since, and Ty keeps adding one each day.
4. If any step fails, nothing is removed, and Ty sees a Mac notification plus a line in `Backups/backup-log.md`.

Ty's choices, 2026-10-03:
- **Layout:** "Raw Records empty, Backups keeps all" (nothing is deleted).
- **Runner:** "Mac job on the 1st".

**Who and what is affected.**
- Ty's Mac: a launchd job.
- Drive: `09 Trading/Trade Journal/Raw Records/` and `Backups/`.
- Repo `ttrng3/Trade-Journal`: a new `tools/` script and `docs/backup.md`.
- Pipeline Wiring, section 5: the job is a new Mac dependency.
- The nightly sync routine is unchanged; it finds fewer CSVs.

**Constraints.**
- "File operation safety — copy, verify size, then delete" (root CLAUDE.md): no `mv`; copy, verify, then remove.
- Public repo: the script names no personal path or account. The Drive path is set in the local launchd file, which is outside the repo.
- The job never writes to the repo or `data/`, and never touches Ty's working tree. It reads the public repo through a fresh clone.
- Mac dependency is debt against the autonomy objective. It must be named on the wiring page, and the job must catch up after sleep.
- Changes reach `main` through a PR and Ty's ship.

**Open questions.**
- None. Layout and runner were decided in chat on 2026-10-03.
