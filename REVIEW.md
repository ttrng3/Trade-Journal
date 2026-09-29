# REVIEW.md

What the reviewer agent (`agents/reviewer.md` in claude-config) checks on every PR to this repo. The three passes run in order, each in full. The last section holds this repo's own rules.

This file is never served: it is not in `.pages-allow`.

## Severity
- **Critical:** it will break something live or publish something it must not. A secret or token, personal data by value in a public repo, a newly served path that shouldn't be, a broken deploy, data loss, a gate bypass.
- **High:** wrong behaviour that will show up. A bug on a path that runs, a broken reference, a diff that does something other than what the PR says, a house rule broken in a way Ty would have to undo.
- **Medium:** it's wrong but contained. An edge case that isn't hit yet, a doc that disagrees with the code, a missing test for a changed behaviour.
- **Low:** clarity, naming, a stale comment.

When unsure between two levels, pick the higher one and say why.

## Pass 1: Bugs
- [ ] Logic: off-by-one, inverted condition, wrong variable, an unreachable branch, loop bounds.
- [ ] Edge cases: empty input, a missing file, a first run, a name with spaces or accents, a timezone (Hanoi is UTC+7; cron is UTC).
- [ ] References resolve: every path, heading anchor, script flag, workflow job name and file named in the diff exists in `files/` or in the base.
- [ ] Shell: quoting, `set -e` interactions, `$?` after a pipe, BSD vs GNU flags (the Mac runs BSD tools).
- [ ] Syntax: YAML, JSON, Python (3.9 on the Mac: no `match`, no `X | Y` types), HTML.
- [ ] The diff does what the PR description says, and nothing it doesn't say.

## Pass 2: Security
- [ ] Secrets by pattern: `ghp_`, `github_pat_`, `sk-`, `sk-ant-`, `AKIA`, `xox[bp]-`, private-key headers, `eyJ…` JWTs (a Supabase **service_role** JWT is always Critical), passwords in URLs, `?token=`/`?key=` in a link.
- [ ] Personal data **by value** in a public repo: a name with money, a phone number, an email address, an account number, an ID number. Referring to where the value lives is fine; the value itself isn't.
- [ ] Anything newly published: a path added to `.pages-allow`, or any new file in a repo still on legacy Pages.
- [ ] Workflow permissions widened (`permissions:`, `pull_request_target`, `secrets: inherit`), or a new third-party action not pinned to a sha.
- [ ] Test fixtures build fake secrets at run time; a token-shaped string typed into a file is a finding even if it's fake.

## Pass 3: House rules
- [ ] **Never by value:** a sensitive value is referenced, not quoted, in any file of a public repo, including `work/` docs.
- [ ] **Artifact mirror contract:** no Cowork preview URL and no artifact id in anything public or anything Ty is shown. (A registry row that records an id on the private Drive mount is the exception.)
- [ ] **Entity separation:** OMNI and ECOPM data, names and numbers never cross into each other's repo or page.
- [ ] **One change per `work/` folder:** the PR names its `work/<yymmdd>-<slug>/`; `intent.md` says accepted; `spec.md` says approved; the diff matches the spec's promise, with nothing extra.
- [ ] **`gate/` untouched** while it is frozen (until 2026-10-05).
- [ ] **One PR per merge command:** nothing in the diff merges or batches PRs (`gh pr merge` in a loop, the merge API).
- [ ] **Verify before you assert:** every number in a doc or page has a source named beside it or in its section.

## Repo-specific rules
Rules specific to Trade-Journal. **Every standing ruling in the README and in `docs/nightly-sync.md` (the runbook, which outranks the routine prompt) applies as well; a PR that breaks one is at least High, and Critical where a line below says so.** The lines below are the ones most often at risk.

- **`index.html` is hand-maintained.** `tools/sync.js` and the nightly routine write `data/` only (README, "Look"). A sync-side change that touches `index.html` is High.
- **Serialization is fixed.** Month files are minified with keys sorted and fill fields in alphabetical order (`k,p,price,qty,side,sym,t,tif`); the manifest uses a one-space indent. With no new fills, `node tools/sync.js --check` must report `"changedFiles": []` (runbook, "The tools"). A diff that breaks either is High: every month file would rewrite, burying the real change.
- **Dedup on content, never on filename.** Existing keys win (runbook, "Dedup on content"). A filename-based dedup is High: on 2026-09-23 it would have dropped 100 real fills (runbook, "Dedup on content").
- **The integrity guard stays.** `sync.js` refuses to run when `totalFills` disagrees with the month files. Removing or weakening that is High.
- **One source of truth.** `data/journal.json` was removed; bringing it back is High. No single file may approach the 1 MB contents-API cap (runbook, "Why the snapshot is sharded").
- **Timestamps.** `meta.snapshotAt` is stored verbatim with milliseconds; `generatedUtc` is the same instant in seconds (runbook, "Timestamps"). Swapping or reformatting them is High.
- **The heartbeat stays.** `data/.last-check` is written every run; the watchdog thresholds are 4 and 14 days because the sync runs Tue–Sat (runbook, "The heartbeat"). A diff that stops writing it is High.
- **Case.** The repo and site are `Trade-Journal`, capital T and J; lowercase 404s. A lowercase link is High.
- **No credentials.** The PAT was revoked on 2026-09-23; a token or a token-in-URL push is **Critical** (runbook, "Credentials").
- **Never fetch the live site from a routine** (runbook, "Verifying a run"). Such an instruction is High.
- **Backup and restore.** `tools/restore.js` checks every file's SHA-256 and the fill count before writing (docs/backup.md). Weakening that check is High.
- **Light only, ruled 2026-09-24 by Ty.** No dark theme; any new colour is a token. `--accent` means positive P&L and interactive chrome is `--blue` (README, "Look").
- **One address, one preview.** `https://ttrng3.github.io/Trade-Journal/` is the only link. A Cowork preview URL or artifact id anywhere in the repo is **Critical** (the repo is public).
- **Don't widen what is published.** A new path in `.pages-allow`, or a new kind of data in `data/`, is High and needs Ty. (Carried from Omni-TMDV's REVIEW.md; not stated in this repo's own files.)
- **Entity separation.** This is Ty's personal trading journal. Any OMNI or ECOPM data is **Critical**.
