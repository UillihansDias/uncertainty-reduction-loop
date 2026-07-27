# uncertainty-reduction-loop

Uncertainty-reduction-loop skill for OpenClaw. It turns unclear research, debugging, experimentation, and engineering work into explicit evidence-producing iterations.

In plain terms: it prevents an agent from treating plausible reasoning as proof. Each loop proposes, implements, runs, validates, learns, and selects the next action.

## Main File

- `SKILL.md`

## Structure

```text
.
├── SKILL.md                         # Skill definition and workflow
├── README.md                        # This file
├── assets/
│   ├── template.json                # Machine-readable loop report template
│   ├── ERRORS.md                    # Log template for experiment/tool errors
│   ├── FEATURE_REQUESTS.md          # Log template for missing validation capabilities
│   ├── LEARNINGS.md                 # Log template for reusable investigation learnings
│   └── SKILL-TEMPLATE.md            # Template for extracting validated loops into skills
├── hooks/
│   └── openclaw/
│       ├── HOOK.md                  # Hook metadata
│       ├── handler.js               # Bootstrap reminder handler (JS)
│       └── handler.ts               # Bootstrap reminder handler (TS)
├── references/
│   ├── examples.md                  # Invocation patterns and edge cases
│   ├── hooks-setup.md               # Hook configuration for Claude Code, Codex, OpenClaw
│   └── openclaw-integration.md      # Full OpenClaw workspace setup guide
└── scripts/
    ├── activator.sh                 # UserPromptSubmit hook reminder
    ├── error-detector.sh            # PostToolUse hook reminder for failures
    ├── extract-skill.sh             # Scaffolds a new skill from a validated loop
    ├── init-url-report.sh           # Creates an uncertainty-loop report JSON
    └── validate-url-report.py       # Validates an uncertainty-loop report JSON
```

## What It Does

Each invocation runs bounded iterations:

1. **Propose** - define a testable hypothesis and disconfirming evidence.
2. **Implement** - create the smallest reversible experiment.
3. **Run** - execute against reality and capture actual output.
4. **Validate** - decide whether the result is trustworthy using `VALIDATED`, `PARTIALLY_VALIDATED`, `INVALIDATED`, or `INCONCLUSIVE`.
5. **Learn** - update the working model while separating observation from interpretation.
6. **Select** - choose the next action by expected uncertainty reduction.

## How It Helps OpenClaw

- Makes debugging and research evidence-first.
- Prevents unvalidated claims such as "fixed" or "working".
- Forces failed experiments to be preserved as useful information.
- Gives long investigations an explicit budget and stop condition.
- Produces reviewable state, validation status, confidence, limits, and next action.

## Use With OpenClaw

Give this repository folder to the OpenClaw install that should use the skill. OpenClaw should copy the repository into its own skills directory and register it from there.

Expected installed shape:

```text
~/.openclaw/skills/uncertainty-reduction-loop/
├── SKILL.md
├── assets/
├── hooks/
├── references/
└── scripts/
```

To fetch the repository first:

```bash
git clone https://github.com/UillihansDias/uncertainty-reduction-loop.git
```

Do not install from a user-specific Desktop path. The Desktop copy is only a source repository for handoff, review, and GitHub publishing.

For agents or OpenClaw installers, the skill entrypoint is:

```text
uncertainty-reduction-loop/SKILL.md
```

## Hook Setup (Optional)

Enable the bootstrap reminder only when recurring loop reminders are wanted:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/uncertainty-reduction-loop
openclaw hooks enable uncertainty-reduction-loop
```

## Learnings Directory

Create optional local logs:

```bash
mkdir -p ~/.openclaw/workspace/.learnings
cp assets/LEARNINGS.md ~/.openclaw/workspace/.learnings/LEARNINGS.md
cp assets/ERRORS.md ~/.openclaw/workspace/.learnings/ERRORS.md
cp assets/FEATURE_REQUESTS.md ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
```

## Safety Boundaries

- No invented observations, commands, test results, measurements, or source material.
- No completion claims without execution and validation.
- No silent retries with changed conditions.
- No irreversible or high-risk experiments when a reversible one can produce evidence.
- Approval required before production, user-data, security, finance, or external-party impact.

## References

- [Examples and edge cases](references/examples.md)
- [Hook setup guide](references/hooks-setup.md)
- [OpenClaw integration](references/openclaw-integration.md)
