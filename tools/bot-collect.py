#!/usr/bin/env python3
"""Mac collector for the trading wiki: one bundle per session, pushed to Drive for the 11:00 routine.

  python3 tools/bot-collect.py                    # the last finished session, upload to Drive
  python3 tools/bot-collect.py --day 2026-10-07 --out /tmp/b.json --no-upload

Reads, never writes, the bots' own files in ~/Projects/orb-options:
  v7     out/v7/journal-<day>.jsonl (main checkout or any worktree; replay/ is ignored)
  sweep  sweep/out/forward/<day>.log
Only the fields in V7_KEEP and the sweep lines in SWEEP_KEEP leave this Mac (to Drive, which is private).
Sweep lines stay whole so postexit.py can parse them; postexit.py writes only parsed fields, and reasons with
id-like tokens scrubbed, into the public repo.

Adds 1-minute bars (Alpaca, keys read in place from orb-options/.env) for every symbol a bot touched
plus Ty's usual underlyings, then copies the bundle to Raw Records/Bots/<day>.json on Drive with rclone.
The Drive folder id is read at run time from the Drive for desktop mount, so it is never stored here.
Standard library only: the Mac's system python has no requests.
"""
import argparse
import datetime as dt
import glob
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ORB = os.path.expanduser("~/Projects/orb-options")
RAW_RECORDS = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-{}/My Drive/Claude Workspace/"
                                  "09 Trading/Trade Journal/Raw Records")
REMOTE = os.environ.get("TJ_RCLONE_REMOTE", "igdrive:")   # an rclone Drive remote; the root is overridden per call
USUAL = ["SPY", "QQQ", "IWM", "TSLA", "META", "AMZN", "NFLX", "AMD", "NVDA", "AAPL", "GOOGL", "COIN"]
V7_KEEP = {
    "start": ["ts", "mode"],
    "drill": ["ts", "drill_at"],
    "open": ["ts", "id", "bot", "symbol", "setup", "d", "qty", "entry", "entry_premium", "stop", "t1", "t2", "R",
             "entry_time"],
    "fill": ["ts", "id", "qty", "price", "rule", "spot"],
    "close": ["ts", "id", "bot", "symbol", "setup", "pnl", "r", "last_rule", "at"],
    "stop_move": ["ts", "id", "leg", "role", "old", "new", "move"],
    "green": ["ts", "id", "spot"],
    "bar": ["ts", "symbol", "bar", "d", "ready", "setups", "all_agree", "signal", "entry", "stop", "R", "t1", "t2",
            "votes"],
}
SWEEP_KEEP = ("Sweep bot", "Started after", "ARMED", "CANCELLED", "SKIPPED", "NOT FILLED", "ENTRY", "EXIT")


def last_session(now=None):
    """The latest weekday whose 16:00 ET close has passed."""
    now = (now or dt.datetime.now(ET)).astimezone(ET)
    d = now.date() if now.hour >= 16 else now.date() - dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d.isoformat()


def v7_events(day):
    paths = glob.glob(f"{ORB}/out/v7/journal-{day}.jsonl") + glob.glob(f"{ORB}/.claude/worktrees/*/out/v7/journal-{day}.jsonl")
    out, seen = [], set()
    for p in sorted(set(paths)):
        for line in open(p):
            r = json.loads(line)
            key = (r.get("kind"), r.get("ts"), r.get("id"), r.get("symbol"), r.get("bar"))
            if key in seen:                      # the same day's journal in two checkouts: count each row once
                continue
            seen.add(key)
            keep = V7_KEEP.get(r.get("kind"))
            if keep is None:
                continue
            if r["kind"] == "bar" and (r.get("ready") or not r.get("setups")):
                continue                         # only setups the bot saw and did not take
            row = {"kind": r["kind"]}
            row.update({k: r[k] for k in keep if k in r})
            if r["kind"] == "bar":               # the votes, reduced to the vote numbers and the reason words
                row["votes"] = {k: {"vote": v.get("vote"), "why": v.get("why")} for k, v in (r.get("votes") or {}).items()}
            out.append(row)
    return out, sorted(set(paths))


def sweep_lines(day):
    p = f"{ORB}/sweep/out/forward/{day}.log"
    if not os.path.exists(p):
        return [], None
    keep = []
    for line in open(p):
        t, _, text = line.rstrip("\n").partition("  ")
        if text.startswith(SWEEP_KEEP):
            keep.append({"t": t.replace(" ET", ""), "text": text})
    return keep, p


def load_env():
    env = {}
    for line in open(f"{ORB}/.env"):
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


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
                                     headers={"APCA-API-KEY-ID": env["ALPACA_PAPER_KEY"],
                                              "APCA-API-SECRET-KEY": env["ALPACA_PAPER_SECRET"]})
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


def drive_folder_id(account):
    path = RAW_RECORDS.format(account)
    raw = subprocess.run(["xattr", "-p", "com.google.drivefs.item-id#S", path], capture_output=True, text=True)
    if raw.returncode != 0 or not raw.stdout.strip():
        sys.exit(f"cannot read the Drive id of Raw Records (is Drive for desktop running?): {path}")
    return raw.stdout.strip()


def collect(day, env):
    v7, v7_paths = v7_events(day)
    sweep, sweep_path = sweep_lines(day)
    syms = set(USUAL) | {r["symbol"] for r in v7 if r.get("symbol")}
    syms |= {l["text"].split()[1].rstrip(":") for l in sweep if l["text"].startswith(("ARMED", "CANCELLED", "ENTRY", "EXIT"))}
    b1 = {s: bars(s, day, env) for s in sorted(syms)}
    return {
        "day": day,
        "collected_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "holiday": not b1.get("SPY"),            # no SPY bars on a weekday = the market was closed
        "sources": {"v7": len(v7_paths), "sweep": bool(sweep_path)},
        "v7": v7,
        "sweep": sweep,
        "bars_1m": b1,
    }


def recent_sessions(n_days=7):
    """Weekdays in the last n_days calendar days, up to the last finished session."""
    last = dt.date.fromisoformat(last_session())
    days = [last - dt.timedelta(days=i) for i in range(n_days)]
    return sorted(d.isoformat() for d in days if d.weekday() < 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=None, help="one day; default: every recent session missing from Drive")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-upload", action="store_true")
    ap.add_argument("--account", default=os.environ.get("TJ_DRIVE_ACCOUNT", ""),
                    help="the Google account in the Drive for desktop folder name (CloudStorage/GoogleDrive-<account>)")
    a = ap.parse_args()
    env = load_env()
    if a.no_upload:
        day = a.day or last_session()
        b = collect(day, env)
        out = a.out or os.path.join(tempfile.mkdtemp(), f"{day}.json")
        json.dump(b, open(out, "w"), separators=(",", ":"))
        print(json.dumps({"day": day, "holiday": b["holiday"], "v7_rows": len(b["v7"]), "sweep_lines": len(b["sweep"]),
                          "symbols": len(b["bars_1m"]), "bars": sum(len(v) for v in b["bars_1m"].values()), "file": out}))
        return
    if not a.account:
        sys.exit("set TJ_DRIVE_ACCOUNT (the launchd plist does) or pass --account")
    fid = drive_folder_id(a.account)
    ls = lambda: subprocess.run(["rclone", "lsf", f"{REMOTE}Bots/", "--drive-root-folder-id", fid],
                                capture_output=True, text=True).stdout.split()
    have = set(ls())
    # A Mac asleep for days runs this once on wake; launchd merges the missed runs, so every recent session
    # without a bundle on Drive is collected now, not only the last one.
    days = [a.day] if a.day else [d for d in recent_sessions() if f"{d}.json" not in have]
    for day in days:
        b = collect(day, env)
        out = os.path.join(tempfile.mkdtemp(), f"{day}.json")
        json.dump(b, open(out, "w"), separators=(",", ":"))
        r = subprocess.run(["rclone", "copyto", out, f"{REMOTE}Bots/{day}.json", "--drive-root-folder-id", fid],
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"rclone failed for {day}: " + r.stderr.strip()[-300:])
        print(json.dumps({"day": day, "holiday": b["holiday"], "v7_rows": len(b["v7"]), "sweep_lines": len(b["sweep"])}))
    missing = [d for d in days if f"{d}.json" not in set(ls())]
    if missing:
        sys.exit("UPLOAD NOT FOUND ON DRIVE: " + ", ".join(missing))
    print("uploaded" if days else "nothing missing")


if __name__ == "__main__":
    main()
