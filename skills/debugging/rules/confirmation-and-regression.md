# Rule: Confirm and Regress

> Impact: critical

## Description

Require a falsifiable causal experiment before calling a root cause confirmed, then verify the original failure and encode the causal contract in a regression check.

## Apply When

- A likely cause has been identified and a fix is being considered or applied.

## Checks

- The suspected cause's removal prevents the failure or its reintroduction recreates it.
- The original repro passes after the narrow fix.
- A regression check fails before the fix and passes after it, or the blocker is explicit.
- Residual risks and escalation conditions are reported.

## Anti-Pattern

Calling a correlated change the root cause, or declaring success from a new test without rerunning the original repro.
