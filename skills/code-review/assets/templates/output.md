# Code Review — Output Template

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

## Fast-Path (single finding or clean review, same contract)

```text
findings:
- [<severity>] <file>:<line> — <issue>
  why: <why this matters, based on evidence>
  fix: <exact change>

patch-plan:
1. <single safest change, or checks recorded for a clean review>

risk:
- <residual risk, or none>
```

For a clean review, use `findings: - none`; never invent a severity-ranked performance defect without measurements.

## Rules

- Sort findings by severity: critical → high → medium → low.
- Every finding requires location, issue, why, and fix.
- List patch steps in safe application order (least risky first).
- State residual risk explicitly, including `none`.
