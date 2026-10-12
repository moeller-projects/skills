# Rule: Reproduce First

> Impact: critical

## Description

Establish a minimal, deterministic failure before theorizing or editing. Capture enough environment and state for another engineer to repeat it.

## Apply When

- Any local error, failing test, regression, or unexpected behavior is reported.

## Checks

- Record exact command, inputs, expected and observed output, exit status, environment, and state.
- Reduce unrelated setup while preserving the failure.
- For intermittent failures, record repeated observations and varying state.

## Anti-Pattern

Guessing from an error message and patching code before reproducing the failure.
