# Examples

## Invocation: Debug an unclear failure

User request:
> Use the uncertainty-reduction loop to investigate why the import job intermittently drops rows.

Expected behavior:
1. State one hypothesis, such as concurrency, malformed input, timeout, or stale state.
2. Define predicted and disconfirming observations.
3. Reproduce or instrument the smallest representative case.
4. Run the experiment and capture actual output.
5. Validate whether the result covers the original failure.
6. Select the next experiment or completion decision.

## Invocation: Evaluate competing approaches

User request:
> Compare two caching strategies, but I am not sure which one is correct.

Expected behavior:
1. Define the uncertainty and success criteria before measuring.
2. Test one major variable at a time.
3. Record inputs, environment, and baseline.
4. Validate that the benchmark measures the intended behavior.
5. Report remaining uncertainty and recommended next action.

## Edge Case: Successful-looking output

Condition:
- A test passes after a code change.

Expected behavior:
- Do not immediately declare completion.
- Check whether the test covers the original failure.
- Consider mocks, stale state, cache, randomness, and regression risk.
- Use `VALIDATED` only when the completion gate is satisfied.

## Edge Case: Inconclusive result

Condition:
- The command failed because the environment lacked a dependency.

Expected behavior:
- Mark execution as `failed_to_run`.
- Mark validation as `INCONCLUSIVE`.
- Learn that the experiment did not test the hypothesis.
- Select environment repair, a different experiment, or escalation.

## Compact Iteration Template

```text
## Iteration N

### 1. Propose
Hypothesis:
Prediction:
Disconfirming evidence:

### 2. Implement
Experiment:
Changed variable:
Baseline:

### 3. Run
Procedure:
Observed result:
Execution status:

### 4. Validate
Checks performed:
Alternative explanations:
Status:
Confidence:

### 5. Learn
Supported:
Weakened:
Still unknown:

### 6. Select
Next action:
Reason:
Continue or stop:
```

## Final Reporting Template

```text
## Objective

## What was tested

## Evidence obtained

## Validation performed

## What was learned

## Conclusion

## Remaining uncertainty

## Recommended next action
```
