#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   REPO=owner/name GITHUB_TOKEN=... ./scripts/cron_tick.sh
#
# This script is intentionally local-output only. If changes are found,
# an Agent should review the JSON and send exactly one useful Octo group update.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="$ROOT/state/last-scan.json"
LOG="$ROOT/run-log.md"
OUT="$ROOT/state/last-scan-output.json"
: "${REPO:?set REPO=owner/name}"

mkdir -p "$ROOT/state"
python3 "$ROOT/scripts/scan_issues.py" --repo "$REPO" --state "$STATE" > "$OUT"

TS="$(date '+%Y-%m-%d %H:%M:%S %z')"
SCANNED="$(python3 - <<'PY' "$OUT"
import json,sys
j=json.load(open(sys.argv[1])); print(j.get('scanned',''))
PY
)"
CHANGES="$(python3 - <<'PY' "$OUT"
import json,sys
j=json.load(open(sys.argv[1])); print(len(j.get('changes',[])))
PY
)"
{
  echo
  echo "## $TS"
  echo "- repo: $REPO"
  echo "- scanned issues: $SCANNED"
  echo "- actionable changes: $CHANGES"
  if [ "$CHANGES" = "0" ]; then
    echo "- group message: not sent (no effective output)"
  else
    echo "- group message: pending Agent review and @主考 update"
  fi
} >> "$LOG"

cat "$OUT"
