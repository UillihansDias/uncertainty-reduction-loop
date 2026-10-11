---
name: uncertainty-reduction-loop
description: "Run evidence-first loops for uncertain debugging, research, experiments, benchmarks, and validation-heavy engineering work."
---

# Uncertainty Reduction Loop

## Objective

Reduce uncertainty through explicit, testable iterations. Use the lightest loop that protects correctness; do not add ceremony to deterministic work.

1. propose one hypothesis or approach
2. implement the smallest useful experiment
3. run it against reality
4. validate whether the result is trustworthy
5. learn what changed in the working model
6. select the next action by information value

Each iteration must produce evidence that supports an idea, weakens an idea, reveals a flawed test, exposes a new uncertainty, or changes what should be attempted next.

## Safety Boundary

- Do not invent observations, measurements, commands, test results, or source material.
- Do not claim to have run an experiment that was only described.
- Do not confuse absence of evidence with evidence of absence.
- Do not hide failed experiments.
- Do not change success criteria after seeing the outcome without recording the change.
- Do not cherry-pick favorable measurements.
- Prefer reversible experiments before irreversible or high-risk changes.
- Obtain approval before actions that may affect production systems, user data, security, finances, or external parties.

## Trigger Fit

Use this skill when at least one is true:

- the cause, answer, implementation, or best approach is unknown
- a plausible fix or conclusion needs evidence before it is trusted
- a command, benchmark, source check, or reproduction produced surprising output
- the work can drift through retries, guesses, or broad edits without learning
- the result will be handed off, reused, promoted, or used to justify a decision

Skip or compress the loop when the task is deterministic, low-risk, and directly verifiable in one step.

Depth:

- **Micro loop**: one concise paragraph for small uncertainties.
- **Compact loop**: one visible iteration using `references/examples.md`.
- **Full report**: JSON report plus script validation for long investigations, audits, handoffs, or reusable learnings.

## Supporting Resources

- Read `references/examples.md` when examples, edge cases, or invocation patterns are needed.
- Read `references/quality-rubric.md` when auditing loop quality or deciding how much process is warranted.
- Read `references/openclaw-integration.md` when installing, enabling, or adapting the skill for OpenClaw workspaces.
- Read `references/hooks-setup.md` only when the user explicitly wants hook reminders.
- Use `assets/template.json` when a machine-readable uncertainty-loop report is needed.
- Run `scripts/init-url-report.sh` to create an empty report from `assets/template.json`.
- Run `scripts/validate-url-report.py` before returning or storing a machine-readable report.
- Run `scripts/self-test.sh` after editing the skill package or report schema.
- Persist reusable outcomes in the active workspace's `.learnings/LEARNINGS.md`; `assets/LEARNINGS.md` defines its entry format, not a substitute for the live ledger.
- Use `assets/ERRORS.md` and `assets/FEATURE_REQUESTS.md` only when a durable error or capability backlog is useful.
- Use `hooks/openclaw/` only when the user explicitly wants an OpenClaw bootstrap reminder for the loop.

## Required State

Maintain and update this state after every iteration:

```text
Objective:
Current uncertainty:
Current hypothesis:
Predicted observation:
Experiment:
Validation method:
Observed result:
Interpretation:
Remaining uncertainty:
Next action:
Iteration number:
```

Do not rely on implicit memory of previous attempts.

## Persistent Learning

The `Learn` step updates the current investigation's working model. When it yields a reusable lesson, also persist that lesson so a later invocation can benefit from it. This is the default, not an optional setup step.

1. **Choose the right scope.** Use the current agent's workspace `.learnings/LEARNINGS.md` for cross-project methods and tool behavior. If the finding is specific to a project, use that project's `.learnings/LEARNINGS.md` instead. Do not copy private project details into a broader ledger.
2. **Recall before experimenting.** Search the applicable ledger for related entries and treat them as dated candidate knowledge, not current proof. Recheck environment-dependent claims before relying on them.
3. **Create the ledger when needed.** If the target ledger does not exist, create its parent directory and initialize it from `assets/LEARNINGS.md` before appending. Never write accumulated entries back into the skill's installed `assets/` directory.
4. **Record only reusable knowledge.** Persist validated corrections, repeatable methods, recurring tool/environment behavior, or knowledge gaps that would change a future decision. Do not log routine task facts, raw transcripts, secrets, personal data, or unsupported guesses. A provisional but useful hypothesis may be recorded with `Status: pending` and an explicit validation question.
5. **Append and deduplicate.** Preserve existing entries. Before adding, search for the same pattern; if it recurs, update that entry's recurrence count and evidence dates rather than creating a duplicate. Include a concise source/evidence reference that can be checked later.
6. **Promote cautiously.** Keep a one-off lesson `pending`. Mark it `promoted` only after independent recurrence or explicit user confirmation, and only then propose or make a narrow change to durable guidance when authorized. A ledger entry does not itself rewrite this skill, workspace instructions, or configuration.
7. **Report persistence honestly.** State whether a learning was appended, updated, or not recorded. If persistence is blocked, say why; do not imply it will be remembered.

At the start of a qualifying loop, inspect only the relevant ledger and entries. For micro-loops with no reusable finding, do not create an empty log entry; still say that no durable learning was identified when that distinction matters.

## Workflow

### 1. Propose

Form one testable hypothesis or approach.

Include:
- the uncertainty being addressed
- the proposed explanation or intervention
- the expected result if correct
- an observation that would weaken or falsify it

Reject the proposal and refine it first if it is too vague, unrelated to the objective, merely restates the problem, cannot be distinguished from competing explanations, or is broader than the available evidence requires.

Required record:

```text
Hypothesis:
Reason for testing it:
Prediction:
Disconfirming evidence:
```

### 2. Implement

Turn the proposal into the smallest reversible experiment that can produce useful evidence.

Rules:
- Change one major variable at a time where practical.
- Avoid unrelated refactoring during an experiment.
- Preserve a baseline for comparison.
- Record relevant configuration, inputs, versions, and environment assumptions.
- Make the experiment repeatable.
- Do not alter tests merely to force a preferred result.

Required record:

```text
Experiment:
Controlled variables:
Changed variable:
Baseline:
Expected evidence:
```

### 3. Run

Execute the experiment against reality. Do not claim something works because the implementation appears reasonable.

Rules:
- Capture actual output.
- Preserve error messages and unexpected behavior.
- Inspect observations before summarizing them.
- Distinguish between `not run`, `failed to run`, and `ran and failed`.
- Do not silently retry with changed conditions.

Required record:

```text
Command or procedure:
Inputs:
Environment:
Observed output:
Execution status:
```

### 4. Validate

Decide whether the observed result is trustworthy and whether it measured the intended property. Validation is mandatory even when the result appears successful.

Check measurement validity, test adequacy, alternative explanations, reproducibility, and regression risk. Consider caching, randomness, leakage, stale state, mocks, environmental differences, changed variables, and simpler explanations.

Assign exactly one status:

```text
VALIDATED
PARTIALLY_VALIDATED
INVALIDATED
INCONCLUSIVE
```

Required record:

```text
Validation method:
Validation evidence:
Alternative explanations considered:
Validation status:
Confidence:
```

Do not mark the task complete with `PARTIALLY_VALIDATED`, `INVALIDATED`, or `INCONCLUSIVE` unless further validation is impossible. If making that exception, report the limitation explicitly and do not represent the result as confirmed.

### 5. Learn

Convert the outcome into an explicit update to the working model. Separate observation from interpretation.

Identify:
- which assumptions were supported
- which assumptions were weakened
- what the experiment did not establish
- what new uncertainty appeared
- whether confidence changed
- whether the original framing remains appropriate

Required record:

```text
Supported assumptions:
Weakened assumptions:
What was not established:
New information:
Remaining uncertainty:
Confidence update:
```

Then decide whether the result is reusable. If so, append or update the scoped ledger entry under `Persistent Learning`; distinguish observed evidence from interpretation and retain unresolved validation as pending.

### 6. Select

Choose the next action based on expected information value, not habit.

Available actions include refining the hypothesis, testing a competing hypothesis, improving validation, reducing scope, gathering missing evidence, reverting an unsuccessful intervention, accepting the result, stopping because further investigation has low value, or escalating because required access or judgment is unavailable.

Balance uncertainty reduction, relevance, cost, reversibility, risk, and ability to distinguish competing explanations.

Required record:

```text
Candidate next actions:
Selected action:
Reason:
Expected uncertainty reduction:
Stop or continue:
```

If continuing, return to Step 1 with an updated hypothesis.

## Software Engineering Application

For debugging or implementation tasks:

```text
Propose: state the suspected cause or implementation approach.
Implement: make the smallest relevant code or configuration change.
Run: execute the targeted test, reproduction, build, or benchmark.
Validate: confirm original coverage, run relevant regressions, and check for misleading passes.
Learn: explain what the output reveals about the system and prior assumptions.
Select: choose the next patch, test, investigation, rollback, or completion decision.
```

Before declaring a software task complete:
- reproduce the original issue when possible
- add or identify a test that would fail without the fix
- verify that test passes with the fix
- run relevant existing tests
- inspect failures rather than repeatedly rerunning them
- review the diff for unrelated changes
- report tests that were not run and why

## Iteration Control

Before starting work that could expand indefinitely, establish an iteration or resource budget, such as:

```text
Maximum iterations: 5
Time budget: 45 minutes
Maximum risky changes: 1
```

When the budget is reached:

1. summarize what has been learned
2. identify the highest-value unresolved uncertainty
3. state why further work is blocked or not currently worthwhile
4. recommend the next experiment
5. do not fabricate closure

Stop and reconsider the strategy when two consecutive experiments produce no new information, the same hypothesis repeats without stronger evidence, retries change no meaningful variable, validation repeatedly fails for the same reason, or the investigation depends on unavailable evidence.

## Quality Gate

A strong loop has:

- a hypothesis that could be weakened by a specific observation
- a baseline or comparison point
- actual output, not only a plan
- validation that checks the measurement, not only the command exit status
- named alternative explanations
- a next action selected by information value
- a final conclusion bounded to what was tested

Reject the loop as too weak when it hides uncertainty, retries without changing conditions, changes success criteria after seeing output, or uses a broad implementation as a substitute for a focused experiment.

## Completion Gate

Declare completion only when all applicable conditions are met:

- the objective has been addressed
- the result has been executed, not merely proposed
- the result has been validated
- relevant regressions or alternative explanations have been considered
- remaining uncertainty is documented
- the conclusion does not exceed the evidence
- the final state is reproducible or clearly bounded
- no critical unresolved failure is hidden

Required completion record:

```text
Final conclusion:
Evidence:
Validation status:
Confidence:
Known limitations:
Remaining risks:
Reproduction instructions:
```

Do not use words such as `fixed`, `solved`, `confirmed`, or `working` unless the completion gate has been satisfied. Prefer narrower language when evidence is incomplete: `the result supports`, `the issue was not reproduced after`, `this resolves the tested case`, `the evidence is consistent with`, or `this remains unverified under`.

## Output Contract

For active work, use the compact iteration template from `references/examples.md` when the loop needs to be visible.

For final reports, include:

1. objective
2. what was tested
3. evidence obtained
4. validation performed
5. what was learned
6. conclusion
7. remaining uncertainty
8. recommended next action
9. persistent learning recorded, updated, or not applicable
