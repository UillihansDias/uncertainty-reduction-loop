# Quality Rubric

Use this rubric when auditing whether an uncertainty-reduction loop was worth running and whether its conclusion is trustworthy.

## 10/10 Loop

- Trigger fit is explicit: the task was uncertain enough to justify the loop, or the agent chose a lighter form for a small task.
- The hypothesis is distinguishable from competing explanations.
- The prediction is concrete enough that the result can support, weaken, or falsify the hypothesis.
- The experiment changes one major variable where practical and preserves a baseline.
- The run records actual output, including failed commands and environmental details that affect interpretation.
- Validation checks whether the experiment measured the intended thing, not merely whether a command passed.
- Alternative explanations are named and either ruled out, bounded, or left as remaining uncertainty.
- The learning step separates observation from interpretation.
- The next action is chosen by information value, reversibility, cost, and risk.
- The final conclusion is no stronger than the evidence and includes reproduction instructions or a clear reason they are unavailable.

## Common Failure Modes

- Treating plausible reasoning as evidence.
- Marking a test pass as `VALIDATED` without checking whether it covers the original uncertainty.
- Repeating the same failed command without changing the hypothesis, inputs, environment, or validation method.
- Running a broad refactor as an "experiment" when a smaller reversible check would work.
- Hiding inconclusive results in a polished summary.
- Letting the loop continue after two iterations that add no new information.
- Using the full template for a deterministic one-command task.

## Depth Control

Use the lightest loop that can protect correctness:

- **Micro loop**: one paragraph for a quick uncertain command, source check, or bug guess.
- **Compact loop**: one visible iteration using the template in `references/examples.md`.
- **Full report**: JSON report plus validation for long-running investigations, handoffs, audits, or reusable learnings.

Skip the loop when the task is deterministic, low-risk, and directly verifiable in one step.
