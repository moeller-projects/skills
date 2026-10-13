# Debugging — Validation Checklist

Run this checklist before accepting a diagnosis as complete. Execute automated validation only when test execution is explicitly authorized.

## Trigger and Boundary Check

- [ ] The failure is local development work.
- [ ] Live production, standalone review, test-suite design, and PR review requests are handed off.

## Evidence Check

- [ ] Exact command, inputs, environment, state, expected behavior, and observed output are recorded.
- [ ] Minimal deterministic reproduction is attempted first when authorized and runnable; otherwise the supplied evidence and missing prerequisite are recorded.
- [ ] Stack trace is read bottom-up; symptom and cause are distinguished.
- [ ] Hypotheses are ranked and variables isolated one at a time; static source/trace hypotheses name their missing experiment.
- [ ] Bisect or binary search is used when practical.

## Root Cause and Fix Check

- [ ] Root cause includes non-empty `finding` and `evidence`; confirmation requires a falsifiable experiment.
- [ ] Fix is narrow and does not claim unsupported behavior.
- [ ] Original reproduction is rerun after the fix when reproduction execution is explicitly authorized; otherwise supplied evidence is retained and verification is reported as unrun.
- [ ] Relevant nearby behavior is checked when the relevant execution is explicitly authorized.
- [ ] Regression check fails before the fix or its limitation is documented; run the check only when test execution is explicitly authorized.

## Output Mechanics

- [ ] `status` is exactly `reproduced`, `hypothesized`, `confirmed`, or `fixed`.
- [ ] Required fields are present and non-empty: `root_cause`, `repro_steps`, `fix`, `verification`, `regression_check`, `open_risks`.
- [ ] `root_cause` contains non-empty `evidence`.
- [ ] Open risks and escalation conditions are explicit.

## Error Format

```text
error: <what prevented diagnosis or verification>
evidence-gap: <missing state, reproduction, source, or ownership>
recovery: <next experiment or escalation action>
```
