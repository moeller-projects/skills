---
name: debugging
description: Diagnose LOCAL development failures from stack traces, error messages, failing tests, regressions, or unexpected behavior. Use when the user reports something failing, broken, or behaving unexpectedly and the root cause is unknown. Reproduce a minimal deterministic failure first, rank evidence-backed hypotheses, bisect and isolate variables, confirm the root cause, apply and verify the fix, and add a regression check. Do not use for live production incidents (use incident-response), code-quality or security review without a failure (use code-review), designing test suites from scratch (use test-strategy), or PR review (use pr-review).
license: Proprietary
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Debugging
  version: "1.0.0"
  summary: Find and verify root causes of local development failures through deterministic reproduction and evidence.
allowed-tools: read_file
---

# Debugging

## Purpose

Find the confirmed root cause of a local development failure, fix it, and preserve a regression check without confusing symptoms for causes.

## Use When

- A stack trace or error message needs diagnosis.
- Tests fail, behavior regresses after a change, or the user says it is failing or broken.
- A local development command produces unexpected behavior.
- The failure can be investigated with repository, environment, and reproducible local evidence.

## Avoid When

- The issue is a live production incident; use `incident-response`.
- The request is code-quality or security review without a concrete failure; use `code-review`.
- The user is designing a test suite from scratch; use `test-strategy` after root cause is found if coverage is missing.
- The request is a pull-request review; use `pr-review`.

## Workflow

1. Capture the exact symptom, command, inputs, environment, recent changes, and expected behavior.
2. Reproduce first with the smallest deterministic repro; record the observed output and status.
3. Read stack traces bottom-up, separate the triggering symptom from causal evidence, and form ranked hypotheses.
4. Isolate one variable at a time. Bisect commits, inputs, configuration, or dependencies when the search space supports it.
5. Confirm the root cause with a falsifiable experiment before changing code; do not label a hypothesis confirmed from correlation alone.
6. Apply the narrowest maintainable fix and verify it against the original repro and relevant nearby behavior.
7. Add a regression check that fails before the fix and passes after it.
8. Stop and escalate when reproduction is impossible, required state or ownership is unavailable, or safe local evidence cannot distinguish hypotheses; preserve artifacts and state the next owner/action.

## Output Contract

Return exactly these fields:

```text
status: reproduced|hypothesized|confirmed|fixed
root_cause:
- finding: <cause or best current hypothesis>
- evidence: <observations or experiments supporting it>
repro_steps:
- <ordered deterministic command/input/environment step>
fix:
- <change made, or "not applied" if diagnosis is not fixed>
verification:
- <result of rerunning the original repro and relevant checks>
regression_check:
- <test or check added/run, or explicit reason it cannot yet be added>
open_risks:
- <remaining uncertainty, impact, or "none">
```

`status` MUST be one of the four listed values. `root_cause.evidence`, `repro_steps`, `fix`, `verification`, `regression_check`, and `open_risks` MUST be non-empty. Do not claim confirmation or a fixed result without evidence.

## Handoffs

- Hand off live production incidents to `incident-response`.
- Hand off code-quality or security review without a concrete failure to `code-review`.
- Hand off test-suite design after the root cause is confirmed and a coverage gap remains to `test-strategy`.
- Hand off pull-request review requests to `pr-review`.

## Error Handling

1. If reproduction is nondeterministic, capture timing, environment, state, and multiple observations; reduce variables before theorizing.
2. If reproduction fails, report `status: hypothesized`, preserve the attempted steps and evidence, and identify the missing prerequisite rather than inventing a cause.
3. If hypotheses remain tied, run the smallest experiment that distinguishes them; do not patch both causes at once.
4. If required logs, source, ownership, or local state are unavailable, stop and escalate with the exact evidence gap and a safe next action.

## Validation Checklist

- [ ] Scope is a local development failure, not a neighboring workflow.
- [ ] Environment, state, inputs, expected behavior, and exact observed failure are captured.
- [ ] A minimal deterministic reproduction is attempted before theorizing.
- [ ] Stack traces are read bottom-up and symptom is separated from cause.
- [ ] Hypotheses are ranked by evidence and variables are isolated one at a time.
- [ ] Bisect or binary search is used when applicable.
- [ ] Root cause is confirmed by a falsifiable experiment before the fix is claimed.
- [ ] Original reproduction is rerun after the fix.
- [ ] A regression check is added or its blocker is explicit.
- [ ] Uncertainty, residual risks, and escalation conditions are stated.

See `tests/validation-checklist.md` for the full checklist; run `tests/run-validation.py` only when test execution is explicitly authorized.

## Assets

- `assets/templates/output.md` — use as the response skeleton for every diagnosis.
- `assets/examples/happy-path.md` — use for a confirmed local regression with a minimal reproduction.
- `scripts/validate-output.py` — use to mechanically validate output fields and status.
- `tests/run-validation.py` — run only when test execution is explicitly authorized.
- `tests/validation-checklist.md` — consult when checking completeness; run its checks only when authorized.

## References

- `references/workflow.md` — consult for the detailed diagnosis flow, evidence standards, and escalation.
- `references/examples.md` — consult for status transitions and representative cases.

## Rules

- `rules/reproduce-first.md`
- `rules/evidence-and-bisection.md`
- `rules/confirmation-and-regression.md`
