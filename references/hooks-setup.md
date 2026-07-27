# Hook Setup Guide

Configure optional uncertainty-reduction-loop reminders for AI coding agents.

## Overview

Hooks can inject a compact reminder when work may otherwise drift into unvalidated conclusions:

- **UserPromptSubmit**: remind the agent to consider a loop for uncertain tasks.
- **PostToolUse (Bash)**: remind the agent to treat command failures as evidence.
- **OpenClaw `agent:bootstrap`**: inject a virtual reminder file for each main session.

## Claude Code Setup

Project-level `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "debug|investigate|uncertain|experiment|validate|benchmark|why",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/uncertainty-reduction-loop/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/uncertainty-reduction-loop/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

## Codex CLI Setup

Create `.codex/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "debug|investigate|uncertain|experiment|validate|benchmark|why",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/uncertainty-reduction-loop/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

## OpenClaw Setup

Enable the bundled OpenClaw hook:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/uncertainty-reduction-loop
openclaw hooks enable uncertainty-reduction-loop
```

## Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds agent to evaluate whether an uncertainty loop is warranted |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Treats failed commands as loop evidence |
| `scripts/extract-skill.sh` | Manual | Scaffolds a new skill from a validated loop |

## Verification

### Test Activator Hook

```bash
./scripts/activator.sh
```

Expected output contains `<uncertainty-reduction-reminder>`.

### Test Report Scripts

```bash
./scripts/init-url-report.sh /tmp/uncertainty-loop-report.json
./scripts/validate-url-report.py /tmp/uncertainty-loop-report.json
```

Expected validation output:

```text
VALID: uncertainty loop report schema passed
```

## Troubleshooting

### Hook Not Triggering

1. Check script permissions: `chmod +x scripts/*.sh`.
2. Verify paths are relative to the project root or use absolute paths.
3. Restart the session after hook configuration changes.

### Too Much Overhead

Use only `UserPromptSubmit`, skip `PostToolUse`, and narrow the matcher to uncertainty-heavy terms.
