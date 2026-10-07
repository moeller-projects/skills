# Test Engine — Output Template

## Default (test-plan + coverage-gaps + cases + risk)

```text
test-plan:
1. <test type and target behavior>
2. <test type and target behavior>

coverage-gaps:
- <behavior or path not currently tested>

cases:
- case: <name>
  given: <precondition>
  when: <action>
  then: <observable outcome>
  type: unit|integration|e2e
  priority: critical|high|medium|low

risk:
- <testing risk or coverage gap that remains after this plan>
```

## Fast-Path (single test case, same contract)

```text
test-plan:
1. <lowest-cost test that proves the behavior>

coverage-gaps:
- <what still remains out of scope>

cases:
- case: <name>
  given: <precondition>
  when: <action>
  then: <observable outcome>
  type: unit|integration|e2e
  priority: critical|high|medium|low

risk:
- <remaining testing risk>
```

## Rules

- Choose the lowest-cost test level that proves the behavior.
- Skip E2E tests when the test environment is unavailable; note the gap.
- Include failure cases alongside happy-path cases.
- Every case must be independently runnable without shared mutable state.
