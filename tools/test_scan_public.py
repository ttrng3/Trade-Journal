"""Tests for the publish scan, the bars collector and postexit's refusal. They use a list of made-up words only."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scan_public as S  # noqa: E402

spec = importlib.util.spec_from_file_location("bars_collect", HERE / "bars-collect.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

FAKE = ["zorblax", "quuxy fizz", "grault waldo plugh"]


@pytest.fixture
def table(tmp_path):
    p = tmp_path / "list.sha256"
    p.write_text("# test list\n" + "\n".join(S.digest(t) for t in FAKE) + "\n")
    return p


def run(table, *args):
    return S.main(["--list", str(table), *args])


def test_a_hit_exits_1_and_names_file_and_line_never_the_word(tmp_path, table, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "a.md").write_text("clean line\nhere is a ZorBlax inside\n")
    assert run(table, "--files", "a.md") == 1
    out = capsys.readouterr().out
    assert "REFUSED a.md:2 matches list entry" in out and "zorblax" not in out.lower()


def test_two_and_three_word_phrases_across_punctuation_are_caught(tmp_path, table, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "b.md").write_text("quuxy-fizz\n")
    (tmp_path / "c.md").write_text("grault_waldo plugh\n")
    assert run(table, "--files", "b.md") == 1 and run(table, "--files", "c.md") == 1


def test_a_clean_file_exits_0(tmp_path, table, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "d.md").write_text("quuxy alone, fizz alone, checkout@v7 stays one token\n")
    assert run(table, "--files", "d.md") == 0


def test_dir_mode_scans_every_file_under_it(tmp_path, table):
    site = tmp_path / "_site"
    (site / "wiki").mkdir(parents=True)
    (site / "wiki" / "x.md").write_text("zorblax\n")
    assert run(table, "--dir", str(site)) == 1


def test_the_real_hash_file_holds_no_readable_word():
    for line in S.LIST.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        assert len(line) == 64 and all(c in "0123456789abcdef" for c in line)


def test_the_repo_scans_clean():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True).stdout.strip()
    files = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True).stdout.split("\n")
    assert S.scan([f for f in files if f], S.load(), Path(root)) == []


# ---- bars collector ----

def test_bars_collect_keeps_market_bars_only_and_maps_spx_to_spy(monkeypatch):
    fills = json.dumps({"a": {"sym": "SPXW261124C06700000"}, "b": {"sym": "HOOD261128P00100000"}})
    seen = []
    got = B.collect("2026-11-24", {"ALPACA_KEY": "k", "ALPACA_SECRET": "s"},
                    fetch_bars=lambda s, d, e: seen.append(s) or [["09:30", 1, 1, 1, 1]], fetch=lambda url: fills)
    assert set(got) == {"day", "collected_utc", "holiday", "symbols", "bars_1m"}
    assert "HOOD" in seen and "SPY" in seen and "SPXW" not in seen and got["holiday"] is False


def test_bars_collect_opens_no_other_projects_files(monkeypatch, tmp_path):
    opened = []
    real_open = open
    monkeypatch.setattr("builtins.open", lambda f, *a, **k: opened.append(str(f)) or real_open(f, *a, **k))
    keys = tmp_path / "alpaca.env"
    keys.write_text("ALPACA_KEY=k\nALPACA_SECRET=s\n")
    B.load_keys(str(keys))
    B.collect("2026-11-24", {"ALPACA_KEY": "k", "ALPACA_SECRET": "s"}, fetch_bars=lambda s, d, e: [], fetch=lambda u: "{}")
    assert opened == [str(keys)]
    assert "Projects/" not in (HERE / "bars-collect.py").read_text()


def test_a_missing_key_file_stops_with_a_plain_message(tmp_path):
    with pytest.raises(SystemExit, match="no key file"):
        B.load_keys(str(tmp_path / "none.env"))


# ---- postexit refuses a bars file with any other field ----

def test_postexit_refuses_a_bars_file_carrying_other_fields(tmp_path):
    bad = tmp_path / "b.json"
    bad.write_text(json.dumps({"day": "2026-11-24", "bars_1m": {}, "extra_rows": [1]}))
    r = subprocess.run([sys.executable, str(HERE / "postexit.py"), "--day", "2026-11-24", "--bars", str(bad),
                        "--data-dir", str(tmp_path / "data"), "--raw-dir", str(tmp_path / "raw")], capture_output=True, text=True)
    assert r.returncode == 2 and '"refused": true' in r.stdout and not (tmp_path / "raw").exists()
