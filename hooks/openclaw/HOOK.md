---
name: uncertainty-reduction-loop
description: Injects an uncertainty-reduction-loop reminder during OpenClaw agent bootstrap.
metadata: {"openclaw":{"emoji":"🔎","events":["agent:bootstrap"]}}
---

# Uncertainty Reduction Loop Hook

Injects a short reminder that uncertain work should move through explicit hypothesis, experiment, execution, validation, learning, and next-action selection.

## What It Does

- Fires on `agent:bootstrap`.
- Adds a virtual reminder file for uncertainty-reduction discipline.
- Skips sub-agent sessions to avoid bootstrap amplification.

## Configuration

Enable only when the user explicitly wants recurring uncertainty-loop reminders:

```bash
openclaw hooks enable uncertainty-reduction-loop
```
