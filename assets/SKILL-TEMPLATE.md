# Skill Template

Template for creating skills extracted from validated uncertainty-reduction loops. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Use when this validated investigation pattern applies. Include trigger conditions, evidence requirements, and validation expectations."
---

# Skill Name

Briefly state the uncertainty, failure mode, or investigation pattern this skill addresses.

## When To Use

- Trigger 1
- Trigger 2
- Trigger 3

## Required Evidence

- Baseline:
- Experiment:
- Validation method:
- Disconfirming evidence:

## Workflow

1. Propose the hypothesis or approach.
2. Implement the smallest reversible test.
3. Run it and capture actual output.
4. Validate the result and alternative explanations.
5. Learn what changed in the working model.
6. Select the next action.

## Completion Gate

Declare completion only when execution, validation, remaining uncertainty, and reproduction instructions are recorded.

## Source

Extracted from a validated uncertainty-reduction loop.
- Learning ID: LRN-YYYYMMDD-XXX
- Original Objective:
- Extraction Date: YYYY-MM-DD
```

---

## Extraction Checklist

Before creating a skill from a loop:

- [ ] The loop reached `VALIDATED` or explicitly bounded partial validation.
- [ ] The pattern is broadly reusable.
- [ ] Observations are separated from interpretation.
- [ ] The solution is not project-specific unless the skill is intentionally project-specific.
- [ ] The skill name is lowercase and hyphenated.
- [ ] The description includes clear trigger conditions.
- [ ] The completion gate is explicit.

After creating:

- [ ] Update the originating learning with `promoted_to_skill`.
- [ ] Add `Skill-Path: skills/skill-name`.
- [ ] Validate the new skill in a fresh session.
