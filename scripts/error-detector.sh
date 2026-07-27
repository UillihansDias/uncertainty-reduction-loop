#!/usr/bin/env bash
# error-detector.sh
# Hook: PostToolUse (Bash)
# Purpose: Fires when a command returns a non-zero exit code and reminds the
#          agent to treat the failure as evidence, not noise.
#
# Security note: CLAUDE_TOOL_OUTPUT may contain sensitive data.
# This script does NOT log or forward it; it only checks the exit status.

TOOL_EXIT_CODE="${CLAUDE_TOOL_RESULT_EXIT_CODE:-}"

if [[ "$TOOL_EXIT_CODE" != "0" && -n "$TOOL_EXIT_CODE" ]]; then
  cat <<'EOF'
<uncertainty-reduction-error-detected>
A command failed during the current session. Treat the failure as observed evidence.

Actions:
1. Record the command or procedure, inputs, environment, observed output, and execution status.
2. Decide whether the result invalidates the hypothesis, exposes a flawed test, or creates a new uncertainty.
3. Do not silently retry with changed conditions.
4. Select the next action by information value.
</uncertainty-reduction-error-detected>
EOF
fi
