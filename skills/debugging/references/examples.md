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

## Hypothesized From Static Evidence

When no authorized or runnable loop exists, static source/trace analysis MAY produce a hypothesis, but it MUST name the missing experiment and avoid causal confirmation:

```text
status: hypothesized
root_cause:
- finding: parser reads a field that the source fixture no longer emits
- evidence: bottom trace frame and source inspection support the mismatch; execution is unavailable
repro_steps:
- not run: required local fixture is unavailable
fix:
- not applied
verification:
- not run: no authorized runnable environment
regression_check:
- not run: no executable seam
open_risks:
- hypothesis remains unconfirmed until the fixture and command are available
```

## Fixed

Use `status: fixed` only when the original reproduction passes after the change and a regression check was added or an explicit, evidence-based blocker is documented.
