# Rule: Confirm and Regress

> Impact: critical

## Description

Require a falsifiable causal experiment before calling a root cause confirmed, then verify the original failure and encode the causal contract in a regression check.

## Apply When

- A likely cause has been identified and a fix is being considered or applied.

## Checks

- Test the suspected cause's prediction: remove it to prevent the failure, or reintroduce it to recreate the failure.
- Record residual risks and escalation conditions when evidence remains incomplete.

## Anti-Pattern

Calling a correlated change the root cause, or declaring success from a new check without authorized evidence for the original failure.
