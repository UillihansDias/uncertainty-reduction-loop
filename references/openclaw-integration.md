# OpenClaw Integration

Setup and usage guide for integrating the uncertainty-reduction-loop skill with OpenClaw.

## Workspace Structure

```text
~/.openclaw/
├── workspace/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   ├── MEMORY.md
│   └── memory/
├── skills/
│   └── uncertainty-reduction-loop/
│       └── SKILL.md
└── hooks/
    └── uncertainty-reduction-loop/
        ├── HOOK.md
        └── handler.ts
```

## Add the Skill to OpenClaw

This repository is meant to be handed to OpenClaw as a complete skill package. The receiving OpenClaw install should copy the repository into its own skills directory and register it from there.

Expected target shape:

```text
~/.openclaw/skills/uncertainty-reduction-loop/
├── SKILL.md
├── assets/
├── hooks/
├── references/
└── scripts/
```

If obtaining the repository from GitHub first:

```bash
git clone https://github.com/UillihansDias/uncertainty-reduction-loop.git
```

If installing from a local checkout with the OpenClaw CLI:

```bash
openclaw skills install ./uncertainty-reduction-loop --as uncertainty-reduction-loop
openclaw skills info uncertainty-reduction-loop
```

Avoid user-specific Desktop paths in install documentation. They are local source locations, not portable installation instructions.

The skill entrypoint OpenClaw should detect is:

```text
uncertainty-reduction-loop/SKILL.md
```

## Install the Hook (Optional)

Copy the hook to OpenClaw's hooks directory:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/uncertainty-reduction-loop
```

Enable the hook:

```bash
openclaw hooks enable uncertainty-reduction-loop
```

## Persistent Learning Ledger

The default cross-project ledger is the active agent workspace's `.learnings/LEARNINGS.md`. The skill reads relevant entries before an investigation and appends reusable findings after validation. Project-specific lessons belong in that project's own `.learnings/LEARNINGS.md`; do not copy project-private details into the workspace ledger.

Create the starter ledger once if it does not exist:

```bash
mkdir -p ~/.openclaw/workspace/.learnings
cp assets/LEARNINGS.md ~/.openclaw/workspace/.learnings/LEARNINGS.md
```

Error and feature-request logs are optional:

```bash
cp assets/ERRORS.md ~/.openclaw/workspace/.learnings/ERRORS.md
cp assets/FEATURE_REQUESTS.md ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
```

## Report Template

Create and validate a machine-readable report:

```bash
./scripts/init-url-report.sh ./uncertainty-loop-report.json
./scripts/validate-url-report.py ./uncertainty-loop-report.json
./scripts/self-test.sh
```

## Promotion Decision Tree

```text
Did a loop produce a reusable investigation pattern?
├── No -> Keep the result task-local; do not add a ledger entry.
└── Yes -> Is it a tool gotcha?
    ├── Yes -> Promote to TOOLS.md or a tool-specific skill.
    └── No -> Is it a workflow rule?
        ├── Yes -> Promote to AGENTS.md or a reusable skill.
        └── No -> Record as pending in .learnings/LEARNINGS.md until recurrence is proven.
```

One-off observations remain `pending`. Promote a finding to durable operating guidance only after independent recurrence or explicit user confirmation. A ledger entry does not automatically edit a skill or workspace policy.

## OpenClaw-Specific Triggers

| Trigger | Action |
|---------|--------|
| Unclear bug or failure | Run the full loop |
| Test passes but coverage is uncertain | Validate before completion |
| Command fails during experiment | Treat failure as evidence |
| Two attempts add no new information | Stop, reframe, or escalate |
| User asks for a repeatable investigation pattern | Extract a skill from the validated loop |

## Verification

Check skill structure:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/uncertainty-reduction-loop
```

Check hook registration:

```bash
openclaw hooks list
```

Check skill visibility:

```bash
openclaw skills check
```
