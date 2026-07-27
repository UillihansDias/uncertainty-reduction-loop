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

## Create Learnings Directory

Create optional logs for reusable learnings and experiment failures:

```bash
mkdir -p ~/.openclaw/workspace/.learnings
cp assets/LEARNINGS.md ~/.openclaw/workspace/.learnings/LEARNINGS.md
cp assets/ERRORS.md ~/.openclaw/workspace/.learnings/ERRORS.md
cp assets/FEATURE_REQUESTS.md ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
```

## Report Template

Create and validate a machine-readable report:

```bash
./scripts/init-url-report.sh ./uncertainty-loop-report.json
./scripts/validate-url-report.py ./uncertainty-loop-report.json
```

## Promotion Decision Tree

```text
Did a loop produce a reusable investigation pattern?
├── No -> Keep the result task-local.
└── Yes -> Is it a tool gotcha?
    ├── Yes -> Promote to TOOLS.md or a tool-specific skill.
    └── No -> Is it a workflow rule?
        ├── Yes -> Promote to AGENTS.md or a reusable skill.
        └── No -> Keep in .learnings/LEARNINGS.md until recurrence is proven.
```

## OpenClaw-Specific Triggers

| Trigger | Action |
|---------|--------|
| Unclear bug or failure | Run the full loop |
| Test passes but coverage is uncertain | Validate before completion |
| Command fails during experiment | Treat failure as evidence |
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
