#!/usr/bin/env python3
"""Machine half of verification/journal.md: is what Pages serves what main says, and is main sound?

Run from an up-to-date checkout of main, on the Mac (never from the routine: runbook, live-site fetches):
  git pull --ff-only && python3 tools/verify_live.py --forbid WORD [WORD ...]

--forbid takes words that must never appear in this personal repo (work entities' and their dashboards'
names, any person's handle that leaked before). The runner supplies them, so this public repo never names
them. Without them the entity check fails rather than passing unchecked. Here the check reads every tracked
file, not only the served ones: this repo must not name a work entity anywhere (Ty, 2026-09-30).

Prints one JSON object of verdicts and exits 0 only when every verdict is true.
Personal traces, Drive ids and preview tags are reported by count and file, never by value.
"""
import argparse, collections, datetime as dt, glob, hashlib, html, json, pathlib, re, shutil, subprocess, sys, tempfile, time, unicodedata, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://ttrng3.github.io/Trade-Journal/"
# Tracked but never served (.pages-allow); each must exist on main and answer 404 live.
PRIVATE = ["README.md", "CLAUDE.md", "REVIEW.md", "docs/nightly-sync.md", "docs/backup.md", "data/.last-check",
           "tools/sync.js", "tools/parse-webull.js", "tools/backup.js", "tools/restore.js", "tools/build-fragment.py",
           "tools/reconcile.py", "tools/verify_live.py", "verification/journal.md", ".github/scripts/freshness.py",
           ".pages-allow"]
FIELDS = ["k", "p", "price", "qty", "side", "sym", "t", "tif"]  # runbook "The tools": fixed fill fields
# Storage links, full email addresses, and bare handles (a word followed by an at-sign and no domain).
TRACES = re.compile(r"/personal(?=/)|sharepoint\.com|1drv\.ms|"
                    r"[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}|\b[a-z][a-z0-9._-]{2,}@(?![\w-])", re.I)
BENIGN = re.compile(r"users\.noreply\.github\.com$|^[A-Z0-9_]+@$")  # GitHub's commit address; @UPPER@ markers
DRIVE_ID = re.compile(r"(?<![A-Za-z0-9_-])(?:1[A-Za-z0-9_-]{32}(?:[A-Za-z0-9_-]{11})?|0B[A-Za-z0-9_-]{26})(?![A-Za-z0-9_-])")
PREVIEW_TAG = re.compile(r"(?<![\w-])\d{10}-[0-9a-f]{4}(?![\w-])")  # a Cowork preview version tag
HEARTBEAT_MAX = 4  # the status page's watchdog for this Tue–Sat pipeline; also freshness.py's MAX_RUN_AGE_DAYS
DATA_MAX = 14      # MAX_DATA_AGE_DAYS default in .github/scripts/freshness.py


def get(path, tries=2):
    """One retry on a network error or a 5xx: a blip must not read as a mismatch."""
    url = f"{LIVE}{path}?v={int(time.time())}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "verify-live"}), timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return get(path, tries - 1) if e.code >= 500 and tries > 1 else (e.code, b"")
    except Exception as e:
        return get(path, tries - 1) if tries > 1 else (str(e), b"")


def age_days(stamp):
    """Days since an ISO stamp ('...Z', '+00:00', 3/6-digit fractions); None if unreadable."""
    try:
        t = dt.datetime.fromisoformat(stamp.strip().replace("Z", "+00:00"))
        t = t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
        return round((dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 86400, 1)
    except (ValueError, AttributeError):
        return None


def norm(t):
    """Compare as a reader sees it: entities decoded, tags removed, NFC, case-folded."""
    return unicodedata.normalize("NFC", re.sub(r"<[^>]*>", "", html.unescape(str(t or "")))).casefold()


def git(*args):
    """Raise on a git failure: an empty answer must never read as "nothing to check"."""
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forbid", nargs="*", default=[])
    forbid = [norm(w) for w in ap.parse_args().forbid if w.strip()]
    v, info, live = {}, {}, {}

    try:
        d = json.loads((ROOT / "data/index.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        d, info["index_error"] = {}, str(e)
    d = d if isinstance(d, dict) else {}
    shards = [str(s) for s in d.get("shards", [])]
    files = sorted(pathlib.Path(f).stem for f in glob.glob(str(ROOT / "data/fills/*.json")))

    v["shards_well_formed"] = bool(shards) and all(re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", s) for s in shards) \
        and shards == sorted(set(shards))
    v["shard_files_match"] = shards == files
    v["journal_json_absent"] = not (ROOT / "data/journal.json").exists()  # CLAUDE.md: stays removed

    # Each month file: its manifest entry's counts, the fixed serialization, the fixed fields, its own month.
    raws, fills, info["shard_problems"] = {}, {}, {}
    for s in files:
        try:
            raws[s] = (ROOT / f"data/fills/{s}.json").read_text(encoding="utf-8")
            fills[s] = json.loads(raws[s])
        except (OSError, ValueError):
            info["shard_problems"][s] = "unreadable"
    shard_info = {str(x.get("id")): x for x in d.get("shardInfo", []) if isinstance(x, dict)}
    keys = collections.Counter()
    for s, f in fills.items():
        probs = []
        if not isinstance(f, dict):
            info["shard_problems"][s] = "not an object"
            continue
        si = shard_info.get(s, {})
        if si.get("fills") != len(f) or si.get("bytes") != len(raws[s].encode("utf-8")):
            probs.append("shardInfo")
        if raws[s].rstrip("\n") != json.dumps(f, sort_keys=True, separators=(",", ":"), ensure_ascii=False):
            probs.append("serialization")
        for k, x in f.items():
            keys[k] += 1
            if not isinstance(x, dict) or sorted(x) != FIELDS or x.get("k") != k:
                probs.append("fields")
                break
            if str(x.get("t", ""))[:7] != s:
                probs.append("wrong month")
                break
        if probs:
            info["shard_problems"][s] = sorted(set(probs))
    v["shards_sound"] = not info["shard_problems"] and set(shard_info) == set(files)
    info["total_fills"] = sum(len(f) for f in fills.values() if isinstance(f, dict))
    v["total_fills_match"] = d.get("totalFills") == info["total_fills"]
    info["duplicate_fills"] = sum(1 for c in keys.values() if c > 1)
    v["no_duplicate_fills"] = info["duplicate_fills"] == 0  # dedup is on content (runbook)

    # The sync's own dry run with no CSVs must change nothing (CLAUDE.md Commands; serialization test).
    empty = tempfile.mkdtemp()
    try:
        r = subprocess.run(["node", "tools/sync.js", "--csv-dir", empty, "--check"], cwd=ROOT, capture_output=True, text=True, timeout=120)
        out = json.loads(r.stdout[r.stdout.find("{"):]) if "{" in r.stdout else {}
        info["sync_check"] = {"exit": r.returncode, "changedFiles": out.get("changedFiles")}
        v["sync_check_clean"] = r.returncode == 0 and out.get("changedFiles") == []
    except (OSError, ValueError, subprocess.TimeoutExpired) as e:
        info["sync_check"], v["sync_check_clean"] = str(e), False
    finally:
        shutil.rmtree(empty, ignore_errors=True)

    served = ["index.html", "data/index.json"] + [f"data/fills/{s}.json" for s in files]
    for p in served:
        st, body = get(p)
        live[p] = body
        info[p] = {"status": st, "live": hashlib.sha256(body).hexdigest()[:12],
                   "main": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12] if (ROOT / p).exists() else None}
    v["served_equals_main"] = all(info[p]["status"] == 200 and info[p]["live"] == info[p]["main"] for p in served)
    info["served_mismatch"] = [p for p in served if info[p]["status"] != 200 or info[p]["live"] != info[p]["main"]]
    for p in served:
        del info[p]

    work = sorted(glob.glob(str(ROOT / "work/*/intent.md")))[:1]  # any one work file, found at run time
    private = PRIVATE + [str(pathlib.Path(w).relative_to(ROOT)) for w in work]
    info["private_status"] = {p: get(p)[0] for p in private + ["data/journal.json"]}
    info["private_missing_on_main"] = [p for p in private if not (ROOT / p).exists()] + ([] if work else ["work/*/intent.md"])
    v["private_not_served"] = all(s == 404 for s in info["private_status"].values()) and not info["private_missing_on_main"]

    beat = ((ROOT / "data/.last-check").read_text(encoding="utf-8").split() or [""])[0] if (ROOT / "data/.last-check").exists() else ""
    info["heartbeat_age_days"], info["data_age_days"] = age_days(beat), age_days(str(d.get("generatedUtc", "")))
    # -1 allows clock skew; a stamp further in the future (a wrong year) would otherwise pass forever.
    v["heartbeat_fresh"] = info["heartbeat_age_days"] is not None and -1 <= info["heartbeat_age_days"] <= HEARTBEAT_MAX
    v["data_fresh"] = info["data_age_days"] is not None and -1 <= info["data_age_days"] <= DATA_MAX

    # Served files, live and on main, then every other tracked text file on main (the repo is public).
    texts = {f"live:{p}": b.decode("utf-8", "replace") for p, b in live.items()}
    texts.update({f"main:{p}": (ROOT / p).read_text(encoding="utf-8") for p in served if (ROOT / p).exists()})
    info["unreadable"] = []
    try:
        tracked = [x for x in git("ls-files", "-z").split("\0") if x]
    except subprocess.CalledProcessError:
        tracked = []
    info["tracked_files"] = len(tracked)
    for p in tracked:
        if p in served:
            continue
        try:
            texts[f"main:{p}"] = (ROOT / p).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pass  # binary file
        except OSError:
            info["unreadable"].append(p)
    v["all_tracked_read"] = bool(tracked) and not info["unreadable"]

    hits = {p: sum(1 for m in TRACES.finditer(t) if not BENIGN.search(m.group(0))) for p, t in texts.items()}
    info["traces"] = {p: n for p, n in hits.items() if n}
    v["no_personal_traces"] = not info["traces"]
    info["drive_ids_tracked"] = {k: len(DRIVE_ID.findall(t)) for k, t in texts.items() if DRIVE_ID.search(t)}
    v["no_drive_ids_tracked"] = not info["drive_ids_tracked"]
    info["preview_tags_tracked"] = {k: len(PREVIEW_TAG.findall(t)) for k, t in texts.items() if PREVIEW_TAG.search(t)}
    v["no_preview_tags_tracked"] = not info["preview_tags_tracked"]
    info["forbid_checked"] = len(forbid)
    info["forbidden_in"] = sorted(k for k, t in texts.items() if any(w in norm(t) for w in forbid))
    v["no_forbidden_words"] = bool(forbid) and not info["forbidden_in"]  # every tracked file: personal repo

    print(json.dumps({"pass": all(v.values()), "verdicts": v, "info": info}, ensure_ascii=False, indent=1))
    sys.exit(0 if all(v.values()) else 1)


if __name__ == "__main__":
    main()
