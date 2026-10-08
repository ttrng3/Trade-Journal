# Spec: v8-collector-fields

**Approved:** 2026-10-08 (as the intent)

**Intent:** accepted 2026-10-08 · **Status:** approved

## Requirements
1. `V7_KEEP` adds, for v8 rows: `v` on `start` and `open`; on `open` `grade`, `grade_why`, `entry_tags`, `dte`, `bid`, `ask`, `spread_pct`, `oi`, `opt_volume`, `risk_usd`, `entries_last_hour`; on `fill` `mid_at_exit`, `spread_paid`; on `close` `r_option`, `risk_usd`.
2. New row kinds: `entry_start`, `bot_halt`, `presession`, `flat_check`, `backstop`, `flat_order`, `stray_fill`, `oca_check`, each without order ids, OCA group names or hashes.
3. Never kept: `order_id`, `exit_order_id`, `exit_oca`, `guard_oca`, `oca`, `settings_sha`, `tune_sha`.

## Design
One dict in `tools/bot-collect.py`. No other file changes.

## Conflicts
Loaded: repo `CLAUDE.md`, entity separation. The bundle goes to private Drive; the public repo gets only what `postexit.py` parses, which is unchanged.

| Rule (by name) | What in the design touches it | Resolution |
|---|---|---|
| Never write personal data or ids into this public repo | New fields reach Drive only | Requirement 3; `postexit.py` unchanged |

## Security
Not a Supabase repo; Pages serves only `.pages-allow`, untouched.

## Promise
`python3 tools/bot-collect.py --day 2026-10-07 --out <f> --no-upload` → the bundle's v7 rows all fit `V7_KEEP` and none holds `order_id` or `settings_sha` (measured 2026-10-08: 197 rows, allowlisted True, no order ids True). The first v8 day (3d, Fri 2026-10-09) is checked the same way.

## Out of scope
Using the new fields in the wiki or the weekly report.
