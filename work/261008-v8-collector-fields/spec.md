# Spec: v8-collector-fields

**Approved:** 2026-10-08 (as the intent)

**Intent:** accepted 2026-10-08 · **Status:** approved

## Requirements
1. `V7_KEEP` adds, for v8 rows: `v` on `start` and `open`; on `open` `grade`, `grade_why`, `entry_tags`, `dte`, `bid`, `ask`, `spread_pct`, `oi`, `opt_volume`, `risk_usd`, `entries_last_hour`; on `fill` `mid_at_exit`, `spread_paid`; on `close` `r_option`, `risk_usd`.
2. New row kinds and exactly these fields (what v8 writes in each, orb-options PR #4):
   | Kind | Fields kept | What they hold |
   |---|---|---|
   | `entry_start` | ts, symbol, qty, price, bid, ask, grade, grade_why | the entry order's price and quote; the grade and its reason words |
   | `bot_halt` | ts, reason, bot, id, grade_why | `id` = the journal's trade id or null (`run.py` `adopt_orphan`, `open_trade`) |
   | `presession` | ts, bars, events, stop_file, hwm_file | `bars` = {symbol: true/false}; `events` = event tag words (FOMC/CPI); two booleans |
   | `flat_check` | ts, positions | `positions` = a count (`run.py` `len(held)`) |
   | `backstop` | ts, id, qty, price, stop | `id` = the trade id (`broker.py` `place_guard`, `id=trade_id`) |
   | `flat_order` | ts, id, qty, price, active_from | `id` = the trade id (same line); `active_from` = a time string |
   | `stray_fill` | ts, local, qty | `local` = the option's contract name (e.g. `SPY 261009C00775000`) |
   | `oca_check` | ts, id, status_filled, fill_shares, guard_qty, flat_qty, open_qty | `id` = the trade id (`run.py`, `id=t["id"]`); counts only |
3. Never kept: `order_id`, `exit_order_id`, `exit_oca`, `guard_oca`, `oca`, `settings_sha`, `tune_sha`. No kept field holds a broker id or an account id; `id` on every kind is the journal's own trade id.
4. The dedup key adds `bot` and `local`, so two rows of a kind with no `id` at the same second (two `bot_halt`, two `stray_fill`) are both kept.

## Design
`tools/bot-collect.py`: the `V7_KEEP` dict and the dedup key. No other file changes.

## Conflicts
Loaded: repo `CLAUDE.md`, entity separation. The bundle goes to private Drive; the public repo gets only what `postexit.py` parses (unchanged: it reads `open`, `fill`, `close`, `stop_move`, `green` and `bar` rows by name).

| Rule (by name) | What in the design touches it | Resolution |
|---|---|---|
| Never write personal data or ids into this public repo | New fields reach Drive only | Requirements 2–3; `postexit.py` unchanged |
| v7 days | v7 already writes `entry_start` rows and `entry_tags` on `open` | They now reach the bundle too (10/07: 4 `entry_start` rows, `entry_tags` on 4 `open` rows); every other v7 row is identical |

## Security
Not a Supabase repo; Pages serves only `.pages-allow`, untouched.

## Promise
- `python3 tools/bot-collect.py --day 2026-10-07 --out <f> --no-upload` → every row fits `V7_KEEP`, none holds `order_id` or `settings_sha` (measured 2026-10-08: 197 rows, allowlisted True, no order ids True).
- Base vs head on 2026-10-07: `fill`, `close`, `start`, `bar`, `drill` rows identical; `open` rows gain only `entry_tags`; 4 `entry_start` rows added (measured 2026-10-08: base 193 rows, head 197).
- Verifier PASS 2026-10-08 (both checks above; no broker-id keys; base and head bars identical).
- The first v8 day (3d, Fri 2026-10-09) is checked the same way, with the bundle searched for any key named `order_id`, `exit_order_id`, `oca`, `exit_oca`, `guard_oca`, `settings_sha` or `tune_sha` (a plain text search for "sha" also hits the skip reason "no shape").

## Out of scope
Using the new fields in the wiki or the weekly report.
