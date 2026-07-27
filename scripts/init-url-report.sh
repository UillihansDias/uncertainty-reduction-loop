#!/usr/bin/env bash
set -euo pipefail

# Create an uncertainty-reduction-loop report from the bundled template.
# Usage:
#   ./scripts/init-url-report.sh [output-path]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_PATH="${1:-./uncertainty-loop-report.json}"

if [ -e "$OUTPUT_PATH" ]; then
  echo "Refusing to overwrite existing file: $OUTPUT_PATH" >&2
  exit 1
fi

cp "$SKILL_ROOT/assets/template.json" "$OUTPUT_PATH"
echo "Created uncertainty loop report: $OUTPUT_PATH"
