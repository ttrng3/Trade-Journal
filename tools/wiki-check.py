#!/usr/bin/env python3
"""Checks for the trading wiki. Each mode prints one pass line, or FAIL lines, and exits non-zero on a fail.

  python3 tools/wiki-check.py                                  # WIKI OK pages=<n> dangling=0 uncited=0
  python3 tools/wiki-check.py --day 2026-10-06               # RAW OK manual=<n> paths=complete
  python3 tools/wiki-check.py --weekly wiki/weekly/2026-W41.md # WEEKLY OK words=<n> unlabelled=0

Links are [[path]] relative to wiki/ without .md, e.g. [[days/2026-10-06]] or [[mistakes/chasing]].
"""
import argparse
import glob
import json
import os
import re
import sys

LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
LABEL = re.compile(r"Verified|Likely|Assumption|raw/\d{4}-\d{2}-\d{2}")


def wiki(root):
    pages = sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True))
    names = {os.path.relpath(p, root)[:-3] for p in pages}
    dangling, uncited = [], []
    for p in pages:
        text = open(p).read()
        for m in LINK.finditer(text):
            if m[1].strip() not in names:
                dangling.append(f"{os.path.relpath(p, root)} -> [[{m[1]}]]")
        if os.path.relpath(p, root).startswith("days/"):
            day = os.path.basename(p)[:-3]
            if f"raw/{day}.json" not in text:
                uncited.append(f"{os.path.relpath(p, root)} does not cite raw/{day}.json")
    for b in dangling + uncited:
        print("FAIL", b)
    ok = not dangling and not uncited
    print(f"WIKI {'OK' if ok else 'FAIL'} pages={len(pages)} dangling={len(dangling)} uncited={len(uncited)}")
    return ok


def raw(day, raw_dir, data_dir):
    rp = os.path.join(raw_dir, day + ".json")
    if not os.path.exists(rp):
        print(f"FAIL no raw/{day}.json")
        print("RAW FAIL manual=0 paths=incomplete")
        return False
    r = json.load(open(rp))
    bad, warn = [], []
    sp = os.path.join(data_dir, "fills", day[:7] + ".json")
    shard = json.load(open(sp)) if os.path.exists(sp) else {}
    n_manual = sum(1 for f in shard.values() if f["t"].startswith(day))
    if len(r["manual"]) != n_manual:
        bad.append(f"manual fills {len(r['manual'])} != shard {n_manual}")
    paths = [x["after"] for x in r["manual"] if x["side"] == "SELL"]
    for a in paths:
        if "missing" in a:            # no bars file, or an underlying outside the collector's list: say so, don't block
            warn.append(f"manual path missing: {a['missing']}")
            continue
        last = a["candles"][-1][0] if a["candles"] else None
        end = a.get("session_last", "15:57")      # a half day ends at 13:00
        if a["candles"] and len(a["candles"]) < 10 and last < end:
            bad.append(f"short path ({len(a['candles'])} candles, last {last})")
        if "close" not in a:
            bad.append("path without close")
    for x in sorted(set(warn)):
        print("WARN", x)
    for x in bad:
        print("FAIL", x)
    ok = not bad
    print(f"RAW {'OK' if ok else 'FAIL'} manual={len(r['manual'])} "
          f"paths={'complete' if ok else 'incomplete'}")
    return ok


def weekly(path):
    text = open(path).read()
    words = len(re.findall(r"\S+", text))
    unl = []
    for block in re.split(r"\n\s*\n|\n(?=[-*|] )", text):
        b = block.strip()
        if not b or b.startswith("#") or set(b) <= set("|-: "):
            continue
        if re.search(r"\d", re.sub(r"\[\[[^\]]+\]\]|\d{4}-W\d{2}|\d{4}-\d{2}-\d{2}", "", b)) and not LABEL.search(b):
            unl.append(b[:80])
    for u in unl:
        print("FAIL unlabelled:", u)
    ok = words < 600 and not unl
    print(f"WEEKLY {'OK' if ok else 'FAIL'} words={words} unlabelled={len(unl)}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day")
    ap.add_argument("--weekly")
    ap.add_argument("--wiki-dir", default="wiki")
    ap.add_argument("--raw-dir", default="raw")
    ap.add_argument("--data-dir", default="data")
    a = ap.parse_args()
    if a.day:
        ok = raw(a.day, a.raw_dir, a.data_dir)
    elif a.weekly:
        ok = weekly(a.weekly)
    else:
        ok = wiki(a.wiki_dir)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
