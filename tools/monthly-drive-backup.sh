#!/bin/bash
# Monthly Drive backup (work/261003-monthly-drive-backup/spec.md, docs/backup.md).
# Run daily by a launchd job on Ty's Mac; acts once a month, when this month's master
# file isn't in Backups/ yet. In that run it copies the master from the public release
# and moves every CSV in Raw Records/ whose fills are already in the journal.
# Copy, check size and SHA-256, then remove; any failure removes nothing.
# TJ_DRIVE_DIR is the Drive folder that holds Raw Records/ (set in the local plist,
# never in this repo).
set -euo pipefail

: "${TJ_DRIVE_DIR:?set TJ_DRIVE_DIR to the Trade Journal folder on Drive}"
RAW="$TJ_DRIVE_DIR/Raw Records"
BK="$TJ_DRIVE_DIR/Backups"
LOG="$BK/backup-log.md"
YM=$(date -u +%Y-%m)
FILE="trade-journal-backup-$YM-01.json.gz"
URL="https://github.com/ttrng3/Trade-Journal/releases/download/backup-$YM-01/$FILE"
TMP=$(mktemp -d)
NOW=$(date '+%Y-%m-%d %H:%M %Z')

notify() { osascript -e "display notification \"$1\" with title \"Trade Journal backup\"" >/dev/null 2>&1 || true; }
fail() { mkdir -p "$BK"; echo "- $NOW — FAILED: $1. Nothing was removed." >> "$LOG"; notify "Failed: $1"; exit 1; }
trap 'rm -rf "$TMP"' EXIT
trap 'fail "unexpected error at line $LINENO"' ERR
sha() { shasum -a 256 < "$1" | cut -c1-64; }

[ -d "$RAW" ] || fail "Raw Records folder not found"
[ -f "$BK/$FILE" ] && exit 0   # this month is done

code=$(curl -sL -o "$TMP/$FILE" -w '%{http_code}' "$URL")
[ "$code" = "404" ] && exit 0  # release not published yet; try again tomorrow
[ "$code" = "200" ] || fail "download returned HTTP $code"

git clone -q --depth 1 https://github.com/ttrng3/Trade-Journal.git "$TMP/repo"
node "$TMP/repo/tools/restore.js" "$TMP/$FILE" --data-dir "$TMP/repo/data" --check >/dev/null || fail "$FILE did not pass restore --check"

mkdir -p "$BK"
cp "$TMP/$FILE" "$BK/$FILE.part"
[ "$(sha "$TMP/$FILE")" = "$(sha "$BK/$FILE.part")" ] || { rm -f "$BK/$FILE.part"; fail "master copy did not match"; }
mv "$BK/$FILE.part" "$BK/$FILE"   # one file, same folder: a rename, not a bulk move

DEST="$BK/CSVs to $(date +%Y-%m-%d)"
moved=0; left=0
shopt -s nullglob
for f in "$RAW"/*.csv; do
  name=$(basename "$f"); one="$TMP/one"; rm -rf "$one"; mkdir "$one"; cp "$f" "$one/"
  if ! out=$(node "$TMP/repo/tools/sync.js" --csv-dir "$one" --data-dir "$TMP/repo/data" --check 2>/dev/null) \
     || ! grep -q '"changedFiles": \[\]' <<<"$out"; then left=$((left+1)); continue; fi
  mkdir -p "$DEST"
  [ -e "$DEST/$name" ] && fail "$name already exists in $(basename "$DEST")"
  cp "$f" "$DEST/$name"
  s1=$(stat -f%z "$f"); s2=$(stat -f%z "$DEST/$name")
  if [ "$s1" -gt 0 ] && [ "$s1" = "$s2" ] && [ "$(sha "$f")" = "$(sha "$DEST/$name")" ]; then
    rm "$f"; moved=$((moved+1))
  else
    fail "copy of $name did not match; it is still in Raw Records"
  fi
done

echo "- $NOW — saved $FILE; moved $moved CSV(s) to $(basename "$DEST"); left $left not yet synced in Raw Records." >> "$LOG"
