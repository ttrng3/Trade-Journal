# Spec

Status: approved by Ty 02/10 ("approve 11", in chat).

- `verification/journal.md`: promise, clean state, 4 steps (script, live page in an overlay-free browser, console, preview), invariants, adversary, sanctioned substitutes, evidence, not covered, traps. Step 2 never clears a browser's storage.
- `tools/verify_live.py` (stdlib plus `node` for the dry run; not served): 16 verdicts as JSON, exit 0 only when all pass: well-formed ordered shards with a file each; `data/journal.json` absent; each month file matches its `shardInfo`, keeps the fixed serialization and fields and holds only its own month; `totalFills` is their sum; no duplicate fill; the sync's dry run with no CSV changes nothing; live equals `main`; private files exist and 404 (and `data/journal.json` 404s); heartbeat ≤ 4 days and data ≤ 14 days; every tracked text file read; no personal traces, Drive ids or preview tags; and no work-entity word, supplied at run time, in any tracked file.
- No change to the page, data, `.pages-allow` or runbooks.
- Promise: once #10 is merged, step 1 prints `"pass": true` against the live site and step 2 prints four trues; each drill breakage fails its own verdict and an untouched copy passes.
