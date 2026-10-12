# Rule: Evidence and Bisection

> Impact: high

## Description

Rank hypotheses from observed evidence and narrow one variable at a time. Use binary search when the search space has a reliable good/bad boundary.

## Apply When

- Multiple causes, commits, inputs, configurations, or dependencies could explain the same symptom.

## Checks

- Read stack traces bottom-up and distinguish wrappers from causal frames.
- Record each experiment and change only one variable.
- Use `git bisect` or binary search when applicable; preserve the original repro.

## Anti-Pattern

Changing code, dependencies, and configuration together, then treating improvement as proof of one cause.
