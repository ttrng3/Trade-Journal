#!/bin/bash
# Monthly Drive backup (work/261003-monthly-drive-backup/spec.md, docs/backup.md).
# Run daily by a launchd job on Ty's Mac; acts once a month, until this month's master
# file is in Backups/. In that run it moves every CSV in Raw Records/ whose fills are
# already in the journal, then saves the master LAST: a run that fails part-way leaves
# the month unfinished, so the next day's run picks up where it stopped.
# Copy, check size and SHA-256, then remove. TJ_DRIVE_DIR is the Drive folder that
# holds Raw Records/ (set in the local plist, never in this repo).
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
moved=0; left=0

notify() { echo "NOTIFY: $1" >&2; osascript -e "display notification \"$1\" with title \"Trade Journal backup\"" >/dev/null 2>&1 || true; }
log() { mkdir -p "$BK" 2>/dev/null; echo "- $NOW — $1" >> "$LOG" 2>/dev/null || true; }
fail() {
  trap - ERR
  notify "Failed: $1"
  log "FAILED: $1. $moved CSV(s) had already moved (each verified first); nothing else was removed."
  exit 1
}
trap 'rm -rf "$TMP"' EXIT
trap 'fail "unexpected error at line $LINENO"' ERR
# SHA-256 of a file; an unreadable file is a failure, never an empty string.
sha() { local h; h=$(shasum -a 256 < "$1" 2>/dev/null | cut -c1-64) || return 1; [ ${#h} -eq 64 ] || return 1; echo "$h"; }

[ -d "$RAW" ] || fail "Raw Records folder not found"
[ -f "$BK/$FILE" ] && exit 0   # this month is done

code=$(curl -sL --retry 5 --retry-connrefused --retry-delay 30 -o "$TMP/$FILE" -w '%{http_code}' "$URL") || code=000
if [ "$code" = "404" ]; then
  [ "$(date -u +%d)" -le 03 ] && exit 0      # not published yet; try again tomorrow
  fail "no $FILE release by day 3 (the backup Action may have failed or run on another date)"
fi
if [ "$code" = "000" ]; then
  [ "$(date -u +%d)" -le 03 ] && exit 0      # offline; try again tomorrow
  fail "could not reach GitHub since the 1st"
fi
[ "$code" = "200" ] || fail "download returned HTTP $code"

git clone -q --depth 1 https://github.com/ttrng3/Trade-Journal.git "$TMP/repo"
node "$TMP/repo/tools/restore.js" "$TMP/$FILE" --data-dir "$TMP/repo/data" --check >/dev/null || fail "$FILE did not pass restore --check"

DEST="$BK/CSVs to $(date +%Y-%m-%d)"
shopt -s nullglob
for f in "$RAW"/*.csv; do
  name=$(basename "$f"); one="$TMP/one"; rm -rf "$one"; mkdir "$one"; cp "$f" "$one/"
  out=$(node "$TMP/repo/tools/sync.js" --csv-dir "$one" --data-dir "$TMP/repo/data" --check 2>/dev/null) || out=""
  # movable only if it parsed at least one fill and every fill is already in the journal
  ok=$(node -e 'try{const o=JSON.parse(process.argv[1]);const i=o.imports||[];process.stdout.write(o.changedFiles&&o.changedFiles.length===0&&i.length===1&&i[0].seen>0&&i[0].fresh===0?"yes":"no")}catch(e){process.stdout.write("no")}' "$out")
  if [ "$ok" != "yes" ]; then left=$((left+1)); continue; fi
  mkdir -p "$DEST"
  [ -e "$DEST/$name" ] && fail "$name already exists in $(basename "$DEST")"
  cp "$f" "$DEST/$name"
  s1=$(stat -f%z "$f"); s2=$(stat -f%z "$DEST/$name"); h1=$(sha "$f") || fail "could not read $name"; h2=$(sha "$DEST/$name") || fail "could not read the copy of $name"
  if [ "$s1" -gt 0 ] && [ "$s1" = "$s2" ] && [ "$h1" = "$h2" ]; then
    rm "$f"; moved=$((moved+1))
  else
    fail "copy of $name did not match; it is still in Raw Records"
  fi
done

mkdir -p "$BK"
cp "$TMP/$FILE" "$BK/$FILE.part"
m1=$(sha "$TMP/$FILE") || fail "could not read the downloaded master"; m2=$(sha "$BK/$FILE.part") || fail "could not read the master copy"
[ "$m1" = "$m2" ] || { rm -f "$BK/$FILE.part"; fail "master copy did not match"; }
mv "$BK/$FILE.part" "$BK/$FILE"   # one file, same folder, after its hash matched

log "saved $FILE; moved $moved CSV(s) to $(basename "$DEST"); left $left in Raw Records (not yet synced or unreadable)."
