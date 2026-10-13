# Debugging — Output Template

```text
status: reproduced|hypothesized|confirmed|fixed
root_cause:
- finding: <cause or best current hypothesis>
- evidence: <specific observation, trace frame, bisect result, or experiment>
repro_steps:
- <exact command/input/state/environment step, or "not run: <missing prerequisite and attempted evidence>">
fix:
- <narrow fix, or "not applied">
verification:
- <authorized original repro result, or "not run: authorization/prerequisite unavailable">
regression_check:
- <authorized check and result, or blocker/missing seam>
open_risks:
- <remaining uncertainty or none>
```

Use `hypothesized` when evidence is insufficient for confirmation. Use `confirmed` after a falsifiable experiment establishes the cause; use `fixed` only after the original reproduction passes and the regression check is addressed.
