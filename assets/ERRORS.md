# Errors Log

Command failures, exceptions, invalid experiments, and unexpected behaviors encountered during uncertainty-reduction loops.

---

<!-- Format:

## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | wont_fix
**Area**: propose | implement | run | validate | learn | select

### Summary
Brief description of what failed.

### Error
```text
Actual error message or observed failure.
```

### Context
- Iteration number
- Hypothesis being tested
- Command or procedure attempted
- Environment details if relevant

### Suggested Fix
Next experiment, validation repair, or rollback.

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- Pattern-Key: optional stable key for recurrence tracking

---
-->
