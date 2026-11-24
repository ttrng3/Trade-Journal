#!/usr/bin/env python3
"""Refuse to publish words that must never be public in this repo.

  python3 tools/scan_public.py --all                 # every tracked file (the pre-push hook, the Pages workflow)
  python3 tools/scan_public.py --files a.md b.json   # just these (the routine, before each write)
  python3 tools/scan_public.py --dir _site           # every file under a folder (the Pages workflow's output)

The list lives here only as SHA-256 hashes (tools/scan_terms.sha256), so this file and the hash file name no term.
Text is lowercased and split on anything but a-z, 0-9, # and @; every 1-, 2- and 3-word run is hashed with PREFIX and
looked up. Exit 1 on any hit, printing file:line and the hash's line number in the list (never the term);
exit 0 when clean. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

PREFIX = "tj-scan-v1:"
TOKEN = re.compile(r"[a-z0-9#@]+")        # "@" stays inside a word: actions/checkout@v7 is one token
HERE = Path(__file__).resolve().parent
LIST = HERE / "scan_terms.sha256"
SKIP_SUFFIX = (".png", ".jpg", ".gif", ".ico", ".gz", ".zip", ".pdf", ".woff", ".woff2")


def digest(gram: str) -> str:
    return hashlib.sha256((PREFIX + gram).encode()).hexdigest()


def load(path: Path = LIST) -> dict:
    return {h: i for i, h in enumerate((x.strip() for x in path.read_text().splitlines()), 1) if h and not h.startswith("#")}


def hits_in(text: str, table: dict) -> list:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        toks = TOKEN.findall(line.lower())
        for size in (1, 2, 3):
            for i in range(len(toks) - size + 1):
                k = table.get(digest(" ".join(toks[i:i + size])))
                if k:
                    out.append((n, k))
    return out


def scan(files, table, root: Path) -> list:
    found = []
    for f in files:
        p = root / f
        if not p.is_file() or str(f).endswith(SKIP_SUFFIX) or p.resolve() == LIST.resolve():
            continue
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        found += [(str(f), n, k) for n, k in hits_in(text, table)]
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--files", nargs="+")
    g.add_argument("--dir")
    ap.add_argument("--list", default=str(LIST))
    a = ap.parse_args(argv)
    table = load(Path(a.list))
    if a.all:
        root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
        files = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True).stdout.split("\n")
    elif a.dir:
        root = Path(a.dir)
        files = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]
    else:
        root, files = Path("."), a.files
    found = scan([f for f in files if f], table, root)
    for f, n, k in found:
        print(f"REFUSED {f}:{n} matches list entry {k}")
    print(f"scan: {len(found)} hit(s) in {len({f for f, _, _ in found})} file(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
