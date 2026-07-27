#!/usr/bin/env bash
# extract-skill.sh
# Usage: ./scripts/extract-skill.sh <skill-name> [--dry-run]
#
# Scaffolds a new skill directory from a validated uncertainty-reduction loop.
# Uses assets/SKILL-TEMPLATE.md as the base.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_FILE="$SKILL_ROOT/assets/SKILL-TEMPLATE.md"

usage() {
  echo "Usage: $0 <skill-name> [--dry-run]"
  echo ""
  echo "  skill-name   Lowercase, hyphen-separated (e.g. concurrency-debug-loop)"
  echo "  --dry-run    Show what would be created without writing files"
  exit 1
}

SKILL_NAME=""
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --*)       echo "Unknown flag: $arg"; usage ;;
    *)         SKILL_NAME="$arg" ;;
  esac
done

if [[ -z "$SKILL_NAME" ]]; then
  usage
fi

if [[ ! "$SKILL_NAME" =~ ^[a-z][a-z0-9-]*$ ]]; then
  echo "Error: skill-name must be lowercase and contain only letters, digits, and hyphens."
  exit 1
fi

SKILLS_DIR="${SKILLS_DIR:-$(cd "$SKILL_ROOT/.." && pwd)}"
OUTPUT_DIR="$SKILLS_DIR/$SKILL_NAME"

if [[ "$DRY_RUN" == true ]]; then
  echo "=== DRY RUN - no files will be written ==="
  echo ""
  echo "Would create:"
  echo "  $OUTPUT_DIR/"
  echo "  $OUTPUT_DIR/SKILL.md          (from assets/SKILL-TEMPLATE.md)"
  echo "  $OUTPUT_DIR/assets/"
  echo "  $OUTPUT_DIR/references/"
  echo "  $OUTPUT_DIR/scripts/"
  echo ""
  echo "Next steps after creation:"
  echo "  1. Edit $OUTPUT_DIR/SKILL.md with the validated loop pattern"
  echo "  2. Update .learnings/LEARNINGS.md with Status: promoted_to_skill"
  echo "  3. Add Skill-Path: skills/$SKILL_NAME to the learning metadata"
  echo "  4. Validate the new skill in a fresh session"
  exit 0
fi

if [[ -d "$OUTPUT_DIR" ]]; then
  echo "Error: $OUTPUT_DIR already exists. Aborting to avoid overwriting."
  exit 1
fi

echo "Creating skill scaffold: $OUTPUT_DIR"

mkdir -p "$OUTPUT_DIR/assets"
mkdir -p "$OUTPUT_DIR/references"
mkdir -p "$OUTPUT_DIR/scripts"

if [[ -f "$TEMPLATE_FILE" ]]; then
  sed "s/skill-name-here/$SKILL_NAME/g" "$TEMPLATE_FILE" > "$OUTPUT_DIR/SKILL.md"
  echo "  Created SKILL.md (from template)"
else
  echo "Error: template not found at $TEMPLATE_FILE" >&2
  exit 1
fi

echo ""
echo "Done. Scaffold created at: $OUTPUT_DIR"
