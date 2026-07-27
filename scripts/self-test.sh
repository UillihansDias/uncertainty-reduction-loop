#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/url-self-test.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

REPORT="$TMP_DIR/report.json"
BAD_REPORT="$TMP_DIR/bad-report.json"

"$SCRIPT_DIR/init-url-report.sh" "$REPORT" >/dev/null
"$SCRIPT_DIR/validate-url-report.py" "$REPORT" >/dev/null

python3 - "$REPORT" "$BAD_REPORT" <<'PY'
import json
import sys
from pathlib import Path

source = Path(sys.argv[1])
dest = Path(sys.argv[2])
data = json.loads(source.read_text())
data["iterations"][0]["validate"]["validation_status"] = "VALIDATED|PARTIALLY_VALIDATED|INVALIDATED|INCONCLUSIVE"
dest.write_text(json.dumps(data, indent=2) + "\n")
PY

if "$SCRIPT_DIR/validate-url-report.py" "$BAD_REPORT" >/dev/null 2>&1; then
  echo "INVALID: validator accepted placeholder enum strings" >&2
  exit 1
fi

if [[ -n "${QUICK_VALIDATE:-}" ]]; then
  python3 "$QUICK_VALIDATE" "$SKILL_ROOT" >/dev/null
fi

echo "VALID: uncertainty-reduction-loop self-test passed"
