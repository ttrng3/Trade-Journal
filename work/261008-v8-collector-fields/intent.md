# Intent: let the collector carry the v8 bot's decision-time fields

**Status:** accepted 2026-10-08 (Ty, "do the four items now", after "updated field list for the Trade-Journal collector" was listed; the field list itself was accepted by the Trade-Journal session on 2026-10-08, except broker order ids and the settings fingerprints)
**Source:** chat, 2026-10-08

**Problem.** `tools/bot-collect.py` keeps only v7 fields (`V7_KEEP`). The v8 bot (orb-options PR #4) writes grades, contract facts, R on the option, spread paid and several new row kinds; the collector drops them, so the wiki and the weekly report can't use them.

**Outcome.** The collector's allowlist carries v8's decision-time fields and new row kinds to the private Drive bundle. Broker order ids, OCA group names and settings hashes still never leave the Mac. On v7 days, `entry_start` rows and `entry_tags` on `open` rows (which v7 already writes) now reach the bundle too; every other v7 row is unchanged.

**Who and what is affected.** `tools/bot-collect.py` (Mac job `com.ty.bot-collect`); the Drive bundle. Nothing published changes: `postexit.py` writes only the fields it parses into the public repo.

**Constraints.** Public repo: no ids by value; entity separation (personal).

**Open questions.** none known
