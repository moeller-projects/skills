---
name: debugging
description: Diagnose LOCAL development failures from stack traces, error messages, failing tests, regressions, or unexpected behavior. Use when the user reports something failing, broken, or behaving unexpectedly and the root cause is unknown. Reproduce a minimal deterministic failure first, rank evidence-backed hypotheses, isolate variables, confirm the root cause, and apply the narrowest fix. Accept user-reported failure evidence as ground truth; run reproduction, build, dependency-install, or test commands only when the user explicitly authorizes that operation, and report unrun verification. Do not use for live production incidents (use incident-response), code-quality or security review without a failure (use code-review), designing test suites from scratch (use test-strategy), or PR review (use pr-review).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Debugging
  version: "1.1.6"
  summary: Find and verify root causes of local development failures through deterministic reproduction and evidence.
---

# Debugging

## Purpose

Find the confirmed root cause of a local development failure, fix it, and preserve a regression check without confusing symptoms for causes.

## Workflow

1. Capture the exact symptom, command, inputs, environment, recent changes, and expected behavior. Treat a user-reported failure and supplied evidence as ground truth; do not require rerunning it.
2. Build a tight red-capable feedback loop before theorizing when reproduction execution is explicitly authorized and runnable. If no authorized or runnable loop exists, preserve supplied trace/source evidence and label causal statements as hypotheses; do not claim confirmation or a fix.
3. Read stack traces bottom-up, separate triggering symptoms from causal evidence, and form ranked hypotheses. Static source/trace reasoning MAY produce a useful hypothesis without a loop, but MUST state the missing experiment and prediction.
4. Isolate one variable at a time and bisect when the search space supports it. Tag temporary debug logs uniquely and remove them before completion.
5. Confirm a root cause only with a falsifiable experiment; correlation, static plausibility, and a passing unrelated check are insufficient.
6. Apply the narrowest maintainable fix only after appropriate evidence. Verify against the original repro and nearby behavior only when explicitly authorized.
7. Add a regression check that fails before the fix and passes after it when execution is authorized; otherwise record the missing seam.
8. Stop and escalate when required state, ownership, or safe evidence is unavailable, preserving artifacts and the next owner/action.

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
- <result of authorized checks, or "not run: explicit authorization was not provided">
regression_check:
- <authorized check result, or "not run: explicit authorization was not provided; explain any missing seam">
open_risks:
- <remaining uncertainty, impact, or "none">
```

`status` MUST be one of the four listed values. `root_cause` MUST contain non-empty `finding` and `evidence` list items; every other listed section MUST contain at least one meaningful item. Use `hypothesized` when only static source/trace reasoning or supplied evidence is available and the causal experiment cannot run. Do not claim `confirmed` or `fixed` without evidence establishing causality and the authorized verification result.

## Handoffs

- Use `verification-before-completion` for the general completion-proof and evidence gate.
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
- [ ] User-supplied failure evidence, environment, state, inputs, expected behavior, and exact observed failure are captured.
- [ ] A tight red-capable loop was built or its absence is documented.
- [ ] Stack traces are read bottom-up and symptom is separated from cause.
- [ ] Hypotheses are ranked, falsifiable, and state their predictions.
- [ ] Variables are isolated one at a time; debug logs carry a unique tag.
- [ ] Bisect or binary search is used when applicable.
- [ ] Root cause is confirmed by a falsifiable experiment before the fix is claimed.
- [ ] Authorized original reproduction and regression checks are reported; unauthorized runs are explicitly marked not run.
- [ ] All debug instrumentation is removed before done is declared.
- [ ] Uncertainty, residual risks, and escalation conditions are stated.

See `tests/validation-checklist.md` for the full checklist; run `tests/run-validation.py` only when test execution is explicitly authorized.

## Assets

- `assets/templates/output.md` — use as the response skeleton for every diagnosis.
- `assets/examples/happy-path.md` — consult for a confirmed local regression with a minimal reproduction.
- `scripts/validate-output.py` — run to mechanically validate output fields and status when output validation is needed; use `--help` for usage without validating.
- `tests/run-validation.py` — run only when test execution is explicitly authorized; use `--help` for non-executing usage.
- `tests/validation-checklist.md` — consult when checking completeness; run its checks only when authorized.

## References

- `references/workflow.md` — consult when the diagnosis needs detailed flow, evidence standards, or escalation guidance.
- `references/examples.md` — consult when status transitions or representative cases are needed.

## Rules

- `rules/reproduce-first.md` — consult before forming hypotheses for any reported local failure; apply its evidence-capture details.
- `rules/evidence-and-bisection.md` — consult when multiple causes or a reliable good/bad boundary require hypothesis ranking or bisection.
- `rules/confirmation-and-regression.md` — consult when a likely cause is identified or a fix/regression check is being considered; run checks only with explicit authorization.

