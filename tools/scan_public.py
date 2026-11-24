#!/usr/bin/env python3
"""Refuse to publish words that must never be public in this repo.

  python3 tools/scan_public.py --all                 # every tracked file (the pre-push hook, the Pages workflow)
  python3 tools/scan_public.py --files a.md b.json   # just these (the routine, before each write)
  python3 tools/scan_public.py --dir _site           # every file under a folder (the Pages workflow's output)
  python3 tools/scan_public.py --push < refs         # every file of every commit being pushed (.githooks/pre-push)

The list lives here only as SHA-256 hashes (tools/scan_terms.sha256), so this file and the hash file name no term.
Text is accent-folded (NFKD), lowercased and split on anything but a-z, 0-9, # and @; a word joined by @ or # is also
checked part by part (except a version pin such as checkout@v7); every 1-, 2- and 3-word run is hashed with PREFIX and
looked up. Exit 1 on any hit, printing file:line and the hash's line number in the list (never the term);
exit 0 when clean. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

PREFIX = "tj-scan-v1:"
TOKEN = re.compile(r"[a-z0-9#@]+")        # "@" stays inside a word: actions/checkout@v7 is one token
HERE = Path(__file__).resolve().parent
LIST = HERE / "scan_terms.sha256"
PIN = re.compile(r"^[a-z0-9]+@v\d+$")            # an action or package version pin, e.g. checkout@v7
ZERO = "0" * 40
SKIP_SUFFIX = (".png", ".jpg", ".gif", ".ico", ".gz", ".zip", ".pdf", ".woff", ".woff2")


def digest(gram: str) -> str:
    return hashlib.sha256((PREFIX + gram).encode()).hexdigest()


def load(path: Path = LIST) -> dict:
    return {h: i for i, h in enumerate((x.strip() for x in path.read_text().splitlines()), 1) if h and not h.startswith("#")}


def fold(line: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", line) if not unicodedata.combining(c)).lower()


def hits_in(text: str, table: dict) -> list:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        toks = TOKEN.findall(fold(line))
        parts = [x for t in toks for x in ([t] if PIN.match(t) else (re.split(r"[@#]", t) or [t])) if x]
        seen = set()
        for seq in (toks, parts):
            for size in (1, 2, 3):
                for i in range(len(seq) - size + 1):
                    k = table.get(digest(" ".join(seq[i:i + size])))
                    if k and (n, k) not in seen:
                        seen.add((n, k))
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


def scan_push(lines, table, root: Path) -> list:
    """For each pushed ref (stdin of pre-push: local-ref local-sha remote-ref remote-sha), scan every file each new
    commit adds or changes, as that commit holds it."""
    found = []
    for line in lines:
        f = line.split()
        if len(f) != 4 or f[1] == ZERO:
            continue
        rng = [f[1], "--not", "--remotes"] if f[3] == ZERO else [f"{f[3]}..{f[1]}"]
        commits = subprocess.run(["git", "rev-list", *rng], cwd=root, capture_output=True, text=True).stdout.split()
        for c in commits:
            names = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "--diff-filter=AMRC", "--root", c],
                                   cwd=root, capture_output=True, text=True).stdout.split("\n")
            for name in (x for x in names if x and not x.endswith(SKIP_SUFFIX) and not x.endswith("scan_terms.sha256")):
                blob = subprocess.run(["git", "show", f"{c}:{name}"], cwd=root, capture_output=True, text=True, errors="ignore")
                found += [(f"{c[:7]}:{name}", n, k) for n, k in hits_in(blob.stdout, table)]
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--files", nargs="+")
    g.add_argument("--dir")
    g.add_argument("--push", action="store_true")
    ap.add_argument("--list", default=str(LIST))
    a = ap.parse_args(argv)
    table = load(Path(a.list))
    if a.all:
        root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
        files = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True).stdout.split("\n")
    elif a.push:
        root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
        found = scan_push(sys.stdin.read().splitlines(), table, root)
        for f, n, k in found:
            print(f"REFUSED {f}:{n} matches list entry {k}")
        print(f"scan: {len(found)} hit(s) in {len({f for f, _, _ in found})} file(s)")
        return 1 if found else 0
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
