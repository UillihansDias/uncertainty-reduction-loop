#!/usr/bin/env bash
# activator.sh
# Hook: UserPromptSubmit
# Purpose: Injects a lightweight uncertainty-reduction reminder.
# Overhead target: ~50-100 tokens.

cat <<'EOF'
<uncertainty-reduction-reminder>
Use the uncertainty-reduction-loop skill when the answer, cause, or implementation is not known in advance.

Rules:
- State a testable hypothesis before changing or concluding.
- Run the smallest useful experiment against reality.
- Validate success and consider alternative explanations.
- Use exactly one validation status: VALIDATED, PARTIALLY_VALIDATED, INVALIDATED, or INCONCLUSIVE.
- Do not call something fixed, solved, confirmed, or working before execution and validation.
- Preserve failed experiments as evidence.
</uncertainty-reduction-reminder>
EOF
