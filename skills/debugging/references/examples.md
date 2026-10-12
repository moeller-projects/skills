# Debugging Examples

## Reproduced but Not Confirmed

```text
status: reproduced
root_cause:
- finding: failure occurs while loading configuration
- evidence: deterministic repro and bottom stack frame; competing causes remain
repro_steps:
- run the command with the captured local environment file
fix:
- not applied
verification:
- original failure reproduced twice
regression_check:
- not yet possible before cause is confirmed
open_risks:
- environment parsing and missing secret are not yet distinguished
```

## Hypothesized After a Missing Prerequisite

Use `status: hypothesized` when the failure cannot be reproduced because required state, credentials, or data is unavailable. Preserve the attempted repro and state exactly what must be obtained.

## Fixed

Use `status: fixed` only when the original reproduction passes after the change and a regression check was added or an explicit, evidence-based blocker is documented.
