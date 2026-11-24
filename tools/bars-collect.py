#!/usr/bin/env python3
"""Mac collector for the trading wiki: one bars file per session, pushed to Drive for the 11:00 routine.

  python3 tools/bars-collect.py                    # every recent session missing from Drive, uploaded
  python3 tools/bars-collect.py --day 2026-10-07 --out /tmp/b.json --no-upload

Pulls 1-minute market bars (Alpaca) for Ty's usual underlyings plus every underlying in his newest fills month
(read from this repo's public data on GitHub), and copies Raw Records/Bars/<day>.json to Drive with rclone.
It reads its Alpaca key from its own file, ~/.config/trade-journal/alpaca.env (ALPACA_KEY=..., ALPACA_SECRET=...,
mode 600), and opens no other project's files. rclone reaches the folder by its path from My Drive, so no Drive
id or account is stored here, and the job works under launchd. Standard library only.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
KEYS = os.path.expanduser(os.environ.get("TJ_ALPACA_ENV", "~/.config/trade-journal/alpaca.env"))
REMOTE = os.environ.get("TJ_RCLONE_REMOTE", "igdrive:")   # an rclone Drive remote, read from My Drive's root
BARS = "Claude Workspace/09 Trading/Trade Journal/Raw Records/Bars"
ROOT = ["--drive-root-folder-id", "root"]
FILLS = "https://raw.githubusercontent.com/ttrng3/Trade-Journal/main/data/fills/{month}.json"
USUAL = ["SPY", "QQQ", "IWM", "TSLA", "META", "AMZN", "NFLX", "AMD", "NVDA", "AAPL", "GOOGL", "COIN"]


def last_session(now=None):
    """The latest weekday whose 16:00 ET close has passed."""
    now = (now or dt.datetime.now(ET)).astimezone(ET)
    d = now.date() if now.hour >= 16 else now.date() - dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d.isoformat()


def load_keys(path=KEYS):
    if not os.path.exists(path):
        sys.exit(f"no key file at {path}: Ty creates it with his own market-data key")
    env = {}
    for line in open(path):
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    if not env.get("ALPACA_KEY") or not env.get("ALPACA_SECRET"):
        sys.exit(f"{path} lacks ALPACA_KEY or ALPACA_SECRET")
    return env


def traded_underlyings(day, fetch=None):
    """Underlyings Ty traded in the day's month, from the repo's own public fills file."""
    url = FILLS.format(month=day[:7])
    try:
        body = fetch(url) if fetch else urllib.request.urlopen(url, timeout=60).read().decode()
    except (urllib.error.URLError, OSError):
        return set()
    shard = json.loads(body) if body else {}
    return {re.match(r"[A-Z]+", f["sym"]).group() for f in shard.values() if f.get("sym")}


def bars(sym, day, env, feed="sip"):
    """1-minute bars 09:30-16:00 ET as [HH:MM, o, h, l, c]. SIP is free once the data is over 15 min old;
    a 403 (data too recent for the free plan) falls back to IEX."""
    start = dt.datetime.fromisoformat(day + "T09:30").replace(tzinfo=ET)
    end = dt.datetime.fromisoformat(day + "T16:00").replace(tzinfo=ET)
    rows, token, tries = [], None, 0
    while True:
        q = {"timeframe": "1Min", "start": start.isoformat(), "end": end.isoformat(), "limit": 10000,
             "feed": feed, "adjustment": "raw"}
        if token:
            q["page_token"] = token
        req = urllib.request.Request(f"https://data.alpaca.markets/v2/stocks/{sym}/bars?" + urllib.parse.urlencode(q),
                                     headers={"APCA-API-KEY-ID": env["ALPACA_KEY"], "APCA-API-SECRET-KEY": env["ALPACA_SECRET"]})
        try:
            body = json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429 and tries < 6:
                tries += 1
                time.sleep(5)
                continue
            if e.code == 429:
                sys.exit(f"Alpaca rate limit did not clear after 6 tries ({sym} {day})")
            if e.code == 403 and feed == "sip":
                return bars(sym, day, env, "iex")
            raise
        rows += body.get("bars") or []
        token = body.get("next_page_token")
        if not token:
            break
    out = []
    for b in rows:
        t = dt.datetime.fromisoformat(b["t"].replace("Z", "+00:00")).astimezone(ET)
        if t < end:
            out.append([t.strftime("%H:%M"), b["o"], b["h"], b["l"], b["c"]])
    return out


def collect(day, env, fetch_bars=bars, fetch=None):
    syms = set(USUAL) | traded_underlyings(day, fetch)
    syms = {"SPY" if s in ("SPX", "SPXW") else s for s in syms}           # no index bars: postexit proxies SPX via SPY
    b1 = {s: fetch_bars(s, day, env) for s in sorted(syms)}
    return {"day": day, "collected_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "holiday": not any(b1.values()), "symbols": len(b1), "bars_1m": b1}


def recent_sessions(n_days=7):
    last = dt.date.fromisoformat(last_session())
    days = [last - dt.timedelta(days=i) for i in range(n_days)]
    return sorted(d.isoformat() for d in days if d.weekday() < 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=None, help="one day; default: every recent session missing from Drive")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-upload", action="store_true")
    a = ap.parse_args()
    env = load_keys()
    if a.no_upload:
        day = a.day or last_session()
        b = collect(day, env)
        out = a.out or os.path.join(tempfile.mkdtemp(), f"{day}.json")
        json.dump(b, open(out, "w"), separators=(",", ":"))
        print(json.dumps({"day": day, "holiday": b["holiday"], "symbols": b["symbols"],
                          "bars": sum(len(v) for v in b["bars_1m"].values()), "file": out}))
        return

    def ls():
        r = subprocess.run(["rclone", "lsf", f"{REMOTE}{BARS}/"] + ROOT, capture_output=True, text=True)
        if r.returncode != 0 and "directory not found" in r.stderr:
            parent = subprocess.run(["rclone", "lsf", f"{REMOTE}{BARS.rsplit('/', 1)[0]}/"] + ROOT, capture_output=True, text=True)
            if parent.returncode != 0:
                sys.exit("Raw Records not reachable on Drive by path: " + parent.stderr.strip()[-300:])
            return []                            # first run: copyto creates Bars/
        if r.returncode != 0:
            sys.exit("rclone lsf failed: " + r.stderr.strip()[-300:])
        return r.stdout.split()
    have = set(ls())
    days = [a.day] if a.day else [d for d in recent_sessions() if f"{d}.json" not in have]
    for day in days:
        b = collect(day, env)
        out = os.path.join(tempfile.mkdtemp(), f"{day}.json")
        json.dump(b, open(out, "w"), separators=(",", ":"))
        r = subprocess.run(["rclone", "copyto", out, f"{REMOTE}{BARS}/{day}.json"] + ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"rclone failed for {day}: " + r.stderr.strip()[-300:])
        print(json.dumps({"day": day, "holiday": b["holiday"], "symbols": b["symbols"]}))
    missing = [d for d in days if f"{d}.json" not in set(ls())]
    if missing:
        sys.exit("UPLOAD NOT FOUND ON DRIVE: " + ", ".join(missing))
    print("uploaded" if days else "nothing missing")


if __name__ == "__main__":
    main()
