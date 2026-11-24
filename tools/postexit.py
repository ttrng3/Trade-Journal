#!/usr/bin/env python3
"""Write raw/<day>.json: Ty's trades with what price did next. Format: raw/schema.json.

  python3 tools/postexit.py --day 2026-10-06 --bars <Bars/2026-10-06.json or missing> [--data-dir data] [--raw-dir raw]

Runs in the 11:00 routine (docs/wiki.md), after the Webull sync. Every number is computed here, none by the model.
Never overwrites: if raw/<day>.json exists it prints {"exists": true} and stops, so a raw day is written once.
A missing bars file (the Mac collector did not deliver) still writes Ty's trades; their price paths need the bars,
so they are marked "bars missing" instead. A bars file carrying any key outside BARS_KEYS is refused: exit 2,
nothing written.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

N_CANDLES = 10
ID_LIKE = re.compile(r"\b(?=(?:[A-Za-z_-]*\d){5})[A-Za-z0-9_-]{6,}\b")
HEX_ID = re.compile(r"\b(?=[0-9a-fA-F]*\d)[0-9a-fA-F]{8,}\b")            # hex order or exec ids; ID_LIKE: 5+ digits (order ids, account numbers, contract codes)
BARS_KEYS = {"day", "holiday", "bars_1m", "collected_utc", "symbols", "feed"}


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
    def __init__(self, bars):
        self.m1 = (bars or {}).get("bars_1m", {})
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


def bars_exist(path):
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
            row["after"] = px.after(u, row["t"]) if px.m1 else {"missing": "bars missing (no bars file)"}
        rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True)
    ap.add_argument("--bars", default=None, help="the Bars/<day>.json from Drive; omit or give a missing path if absent")
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--raw-dir", default="raw")
    ap.add_argument("--final", action="store_true",
                    help="write even when the shard has no Webull fills for the day (the next run's recheck)")
    a = ap.parse_args()
    out = os.path.join(a.raw_dir, a.day + ".json")
    if os.path.exists(out):
        print(json.dumps({"exists": True, "file": out}))
        return
    bars = json.load(open(a.bars)) if bars_exist(a.bars) else None
    extra = sorted(set(bars) - BARS_KEYS) if isinstance(bars, dict) else []
    if extra:
        print(json.dumps({"refused": True, "day": a.day, "why": f"bars file carries keys outside the bars format: {extra}"}))
        sys.exit(2)
    sp = os.path.join(a.data_dir, "fills", a.day[:7] + ".json")
    has_fills = os.path.exists(sp) and any(f["t"].startswith(a.day) for f in json.load(open(sp)).values())
    if not has_fills and not bars:
        # no fills and no bars: nothing to journal (a holiday with the Mac off, or a day nothing ran). Never write it.
        print(json.dumps({"skipped": True, "day": a.day, "why": "no Webull fills and no bars file"}))
        return
    if not has_fills and not a.final:
        # Ty's CSV may arrive after this run (CLAUDE.md, 2026-09-26). Freezing now would lose his trades for good,
        # so the day waits for the next run, which writes it with --final whether or not fills have come.
        print(json.dumps({"deferred": True, "day": a.day, "why": "no Webull fills for this day yet"}))
        return
    if bars and bars.get("day") != a.day:
        sys.exit(f"bars file is for {bars.get('day')}, not {a.day}")
    if bars and bars.get("holiday"):
        print(json.dumps({"holiday": True, "day": a.day, "why": "no bars for any symbol: the market was closed"}))
        return
    px = Prices(bars)
    man = manual(a.day, a.data_dir, px)
    raw = {"day": a.day, "written_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "sources": {"webull_fills": len(man), "bars": "present" if bars else "missing"}, "manual": man}
    os.makedirs(a.raw_dir, exist_ok=True)
    with open(out, "w") as f:
        json.dump(raw, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps({"file": out, "manual": len(man), "bars": raw["sources"]["bars"]}))


if __name__ == "__main__":
    main()
