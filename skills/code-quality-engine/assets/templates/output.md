# Code Quality Engine — Output Template

## Default (findings + patch plan + risk)

```text
findings:
- [critical|high|medium|low] <file>:<line> — <issue>
  why: <why this matters>
  fix: <exact change to make>

patch-plan:
1. <first change — file and action>
2. <second change — file and action>

risk:
- <residual risk after applying patch>
```

## Fast-Path (single finding, same contract)

```text
findings:
- [<severity>] <file>:<line> — <issue>
  fix: <exact change>

patch-plan:
1. <single safest change>

risk:
- <residual risk>
```

## Rules

- Sort findings by severity: critical → high → medium → low.
- Include `why` only when the reason is non-obvious.
- List patch steps in safe application order (least risky first).
- Omit `risk` only when the patch has no residual risk.
