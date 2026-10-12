# Debugging — Output Template

```text
status: reproduced|hypothesized|confirmed|fixed
root_cause:
- finding: <cause or best current hypothesis>
- evidence: <specific observation, trace frame, bisect result, or experiment>
repro_steps:
- <exact command/input/state/environment step>
fix:
- <narrow fix, or "not applied">
verification:
- <original repro result and relevant nearby checks>
regression_check:
- <test/check added and result, or blocker>
open_risks:
- <remaining uncertainty or none>
```

Use `hypothesized` when evidence is insufficient for confirmation. Use `confirmed` after a falsifiable experiment establishes the cause; use `fixed` only after the original reproduction passes and the regression check is addressed.
