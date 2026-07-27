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

## Install the Skill

From the Desktop copy:

```bash
openclaw skills install /Users/uillihansdias/Desktop/uncertainty-reduction-loop --as uncertainty-reduction-loop
```

From git:

```bash
openclaw skills install git:https://github.com/UillihansDias/uncertainty-reduction-loop.git --as uncertainty-reduction-loop
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
python3 /path/to/skill-creator/scripts/quick_validate.py /Users/uillihansdias/Desktop/uncertainty-reduction-loop
```

Check hook registration:

```bash
openclaw hooks list
```

Check skill visibility:

```bash
openclaw skills check
```
