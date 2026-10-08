#!/usr/bin/env python3
"""Write raw/<day>.json: the session's trades and skips with what price did next. Format: raw/schema.json.

  python3 tools/postexit.py --day 2026-10-06 --bundle <Bots/2026-10-06.json or missing> [--data-dir data] [--raw-dir raw]

Runs in the 11:00 routine (docs/wiki.md), after the Webull sync. Every number is computed here, none by the model.
Never overwrites: if raw/<day>.json exists it prints {"exists": true} and stops, so a raw day is written once.
A missing bundle (the Mac collector did not deliver) still writes Ty's trades; their price paths need the
bundle's bars, so they are marked "bars missing" instead.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

N_CANDLES = 10
ID_LIKE = re.compile(r"\b(?=(?:[A-Za-z_-]*\d){5})[A-Za-z0-9_-]{6,}\b")
HEX_ID = re.compile(r"\b(?=[0-9a-fA-F]*\d)[0-9a-fA-F]{8,}\b")            # hex order or exec ids   # 5+ digits: order ids, account numbers, contract codes (not bot1_st_flip)


def scrub(text):
    """Free-text reasons go to a public repo: replace any token that looks like an id."""
    return HEX_ID.sub("[id]", ID_LIKE.sub("[id]", text)) if isinstance(text, str) else text
PROXY = {"SPX": ("SPY", 10.0), "SPXW": ("SPY", 10.0)}   # Alpaca has no index bars


def underlying(opt_sym):
    return re.match(r"[A-Z]+", opt_sym).group()


def three_min(m1):
    """[HH:MM, o, h, l, c] 1-minute bars -> 3-minute candles keyed from 09:30."""
    out, cur = [], None
    for t, o, h, l, c in m1:
        mins = int(t[:2]) * 60 + int(t[3:]) - 570
        slot = 570 + (mins // 3) * 3
        start = f"{slot // 60:02d}:{slot % 60:02d}"
        if cur and cur[0] == start:
            cur[2], cur[3], cur[4] = max(cur[2], h), min(cur[3], l), c
        else:
            cur = [start, o, h, l, c]
            out.append(cur)
    return out


class Prices:
    def __init__(self, bundle):
        self.m1 = (bundle or {}).get("bars_1m", {})
        self.m3 = {s: three_min(v) for s, v in self.m1.items()}

    def series(self, sym):
        base, mult = PROXY.get(sym, (sym, 1.0))
        return base, mult

    def after(self, sym, t):
        """The next N_CANDLES 3-minute candles that start at or after t (HH:MM[:SS]), and the session close."""
        base, mult = self.series(sym)
        m3 = self.m3.get(base)
        if not m3:
            return {"missing": f"no bars for {base}"}
        hhmm = t[:5]
        nxt = [c for c in m3 if c[0] > hhmm or (c[0] == hhmm and len(t) == 5)][:N_CANDLES]
        r = lambda x: round(x * mult, 2)
        res = {"candles": [[c[0], r(c[1]), r(c[2]), r(c[3]), r(c[4])] for c in nxt], "close": r(self.m1[base][-1][4]),
               "session_last": m3[-1][0]}            # the last 3-minute candle that day (13:00 close on a half day)
        if mult != 1.0:
            res["proxy"] = f"{base} x {mult:g}"
        return res

    def first_hit(self, sym, t, d, stop, target):
        """Which of target and stop the 1-minute bars reach first after t; d = +1 long, -1 short."""
        base, mult = self.series(sym)
        for bt, o, h, l, c in self.m1.get(base, []):
            if bt <= t[:5]:
                continue
            h, l = h * mult, l * mult
            hit_t = h >= target if d > 0 else l <= target
            hit_s = l <= stop if d > 0 else h >= stop
            if hit_t and hit_s:
                return "both in one minute", bt
            if hit_t:
                return "target", bt
            if hit_s:
                return "stop", bt
        return "neither", None


def bundle_exists(path):
    return bool(path) and os.path.exists(path)


def manual(day, data_dir, px):
    path = os.path.join(data_dir, "fills", day[:7] + ".json")
    shard = json.load(open(path)) if os.path.exists(path) else {}   # a month with no trades yet has no shard
    rows = []
    for f in sorted(shard.values(), key=lambda f: f["t"]):
        if not f["t"].startswith(day):
            continue
        u = underlying(f["sym"])
        row = {"sym": f["sym"], "underlying": u, "side": f["side"], "t": f["t"][11:19], "qty": f["qty"], "premium": f["price"]}
        if f["side"] == "SELL":
            row["after"] = px.after(u, row["t"]) if px.m1 else {"missing": "bars missing (no bot bundle)"}
        rows.append(row)
    return rows


def why_v7(votes):
    zero = [k for k, v in (votes or {}).items() if not v.get("vote")]
    words = [f"{k}: {v['why']}" for k, v in (votes or {}).items() if v.get("why") and not v.get("vote")]
    out = "no vote from " + ", ".join(zero) + (f" ({'; '.join(words)})" if words else "") if zero else "not all agreed"
    return scrub(out)


def v7_rows(bundle, px):
    opens = {r["id"]: r for r in bundle["v7"] if r["kind"] == "open"}
    fills = {r["id"]: r for r in bundle["v7"] if r["kind"] == "fill"}
    moves, greens = {}, {}
    for r in bundle["v7"]:
        if r["kind"] == "stop_move":
            moves.setdefault(r["id"], []).append({"t": r["ts"][11:19], "leg": r.get("leg"), "role": r.get("role"),
                                                  "old": r.get("old"), "new": r.get("new"), "move": r.get("move")})
        elif r["kind"] == "green":
            greens.setdefault(r["id"], r["ts"][11:19])
    trades, skips = [], []
    for c in (r for r in bundle["v7"] if r["kind"] == "close"):
        o = opens.get(c["id"], {})
        sym, d = c.get("symbol") or o.get("symbol"), o.get("d", 1)
        exit_t = (c.get("at") or c["ts"])[11:19]
        trades.append({"bot": "v7", "id": f"v7-{len(trades) + 1}", "setup": scrub(c.get("setup")), "drill": c.get("setup") == "drill",
                       "symbol": sym, "dir": "call" if d > 0 else "put", "entry_t": str(o.get("entry_time", ""))[11:19],
                       "entry": o.get("entry"), "stop": o.get("stop"), "t1": o.get("t1"), "t2": o.get("t2"),
                       "exit_t": exit_t, "exit": fills.get(c["id"], {}).get("spot"), "exit_rule": scrub(c.get("last_rule")),
                       "pnl": round(c.get("pnl", 0), 2), "r": round(c.get("r", 0), 2),
                       "green_t": greens.get(c["id"]), "stop_moves": moves.get(c["id"], []), "after": px.after(sym, exit_t)})
    rnd = lambda x: round(x, 2) if isinstance(x, (int, float)) else None
    for b in (r for r in bundle["v7"] if r["kind"] == "bar"):
        t, d = b["ts"][11:19], b.get("d") or 1
        stop, target = b.get("stop"), b.get("t2")
        if isinstance(stop, (int, float)) and isinstance(target, (int, float)):
            hit, hit_t = px.first_hit(b["symbol"], t, d, stop, target)
        else:
            hit, hit_t = "unknown (no stop or target logged)", None
        skips.append({"bot": "v7", "symbol": b["symbol"], "dir": "call" if d > 0 else "put", "t": t, "kind": "skipped",
                      "setup": scrub(", ".join(b.get("setups", []))), "why": why_v7(b.get("votes")),
                      "entry": rnd(b.get("entry")), "stop": rnd(stop), "target": rnd(target),
                      "first_hit": hit, "first_hit_t": hit_t, "after": px.after(b["symbol"], t)})
    return trades, skips, []


NUM = r"(-?\d+(?:\.\d+)?)"


def sweep_rows(bundle, px):
    trades, skips, armed, open_, unparsed = [], [], {}, {}, []
    for line in bundle["sweep"]:
        t, text = line["t"], line["text"]
        if text.startswith("ARMED"):
            m = re.match(rf"ARMED (\S+) (calls|puts) · (\w+) {NUM} on the stock · stop {NUM} · target {NUM}", text)
            if m:
                armed[m[1]] = {"t": t, "dir": "call" if m[2] == "calls" else "put", "order": m[3],
                               "entry": float(m[4]), "stop": float(m[5]), "target": float(m[6])}
        elif text.startswith(("CANCELLED", "SKIPPED", "NOT FILLED")):
            sym = text.split()[2 if text.startswith("NOT FILLED") else 1].rstrip(":")
            a = armed.pop(sym, None)
            kind = "skipped" if text.startswith("SKIPPED") else "cancelled"
            why = scrub(text.split(":", 1)[-1].strip())
            if a:
                d = 1 if a["dir"] == "call" else -1
                hit, hit_t = px.first_hit(sym, t, d, a["stop"], a["target"])
                skips.append({"bot": "sweep", "symbol": sym, "dir": a["dir"], "t": t, "kind": kind,
                              "setup": f"{a['order']} entry armed {a['t']}", "why": why,
                              "entry": a["entry"], "stop": a["stop"], "target": a["target"],
                              "first_hit": hit, "first_hit_t": hit_t, "after": px.after(sym, t)})
            else:                                  # no ARMED line before it: keep it, with no levels to test
                skips.append({"bot": "sweep", "symbol": sym, "dir": None, "t": t, "kind": kind, "setup": "not armed",
                              "why": why, "entry": None, "stop": None, "target": None,
                              "first_hit": "unknown (not armed)", "first_hit_t": None, "after": px.after(sym, t)})
        elif text.startswith("ENTRY"):
            m = re.match(rf"ENTRY (\S+) (\d+)x (\S+) @ {NUM} · stock {NUM} · stop {NUM} .*· target {NUM}", text)
            if m:
                a = armed.pop(m[1], {})
                open_[m[1]] = {"t": t, "qty": int(m[2]), "contract": m[3], "premium": float(m[4]), "entry": float(m[5]),
                               "stop": float(m[6]), "target": float(m[7]),
                               "dir": a.get("dir") or ("call" if re.search(r"\d{6}C\d", m[3]) else "put")}
        elif text.startswith("EXIT"):
            m = re.match(rf"EXIT (\S+) \(([^)]+)\) stock {NUM} · {NUM}R · option {NUM} -> {NUM}", text)
            if m and m[1] in open_:
                o = open_.pop(m[1])
                pnl = round((float(m[6]) - o["premium"]) * o["qty"] * 100, 2)
                trades.append({"bot": "sweep", "id": f"{m[1]}-{o['t']}", "setup": "sweep V0", "drill": False,
                               "symbol": m[1], "dir": o["dir"], "entry_t": o["t"], "entry": o["entry"], "stop": o["stop"],
                               "t1": o["target"], "t2": o["target"], "exit_t": t, "exit": float(m[3]), "exit_rule": scrub(m[2]),
                               "pnl": pnl, "r": float(m[4]), "after": px.after(m[1], t)})
            else:                                  # kept, so a format change shows up instead of blocking the day
                unparsed.append({"bot": "sweep", "t": t, "line": scrub(text)})
    return trades, skips, unparsed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True)
    ap.add_argument("--bundle", default=None, help="the Bots/<day>.json from Drive; omit or give a missing path if absent")
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--raw-dir", default="raw")
    ap.add_argument("--final", action="store_true",
                    help="write even when the shard has no Webull fills for the day (the next run's recheck)")
    a = ap.parse_args()
    out = os.path.join(a.raw_dir, a.day + ".json")
    if os.path.exists(out):
        print(json.dumps({"exists": True, "file": out}))
        return
    sp = os.path.join(a.data_dir, "fills", a.day[:7] + ".json")
    has_fills = os.path.exists(sp) and any(f["t"].startswith(a.day) for f in json.load(open(sp)).values())
    if not has_fills and not bundle_exists(a.bundle):
        # no fills and no bundle: nothing to journal (a holiday with the Mac off, or a day nothing ran). Never write it.
        print(json.dumps({"skipped": True, "day": a.day, "why": "no Webull fills and no bot bundle"}))
        return
    if not has_fills and not a.final:
        # Ty's CSV may arrive after this run (CLAUDE.md, 2026-09-26). Freezing now would lose his trades for good,
        # so the day waits for the next run, which writes it with --final whether or not fills have come.
        print(json.dumps({"deferred": True, "day": a.day, "why": "no Webull fills for this day yet"}))
        return
    bundle = json.load(open(a.bundle)) if a.bundle and os.path.exists(a.bundle) else None
    if bundle and bundle.get("day") != a.day:
        sys.exit(f"bundle is for {bundle.get('day')}, not {a.day}")
    if bundle and bundle.get("holiday"):
        print(json.dumps({"holiday": True, "day": a.day, "why": "no bars for any symbol: the market was closed"}))
        return
    px = Prices(bundle)
    man = manual(a.day, a.data_dir, px)
    bots, skips, unparsed = [], [], []
    if bundle:
        for f in (v7_rows, sweep_rows):
            t, s, u = f(bundle, px)
            bots += t
            skips += s
            unparsed += u
    raw = {"day": a.day, "written_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "sources": {"webull_fills": len(man), "bots_bundle": "present" if bundle else "missing"},
           "manual": man, "bots": bots, "skips": skips, "unparsed_exits": unparsed}
    os.makedirs(a.raw_dir, exist_ok=True)
    with open(out, "w") as f:
        json.dump(raw, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps({"file": out, "manual": len(man), "bots": len(bots), "skips": len(skips),
                      "bundle": raw["sources"]["bots_bundle"]}))


if __name__ == "__main__":
    main()
