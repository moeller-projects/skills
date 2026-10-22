---
name: task-planning
description: Use when confirmed scope must be broken into atomic tasks with dependencies, estimates, and done criteria. Do not use when requirements are still being written or the user wants option comparison or plan critique before scope is fixed.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Task Planning
  version: "1.1.3"
  summary: Break work into atomic, shippable tasks with explicit dependencies, critical path, estimates, and definitions of done.
---

# Task Planning

## Purpose

Turn a confirmed scope into a structured, executable task list that a team can commit to and track — with explicit dependencies, unknowns surfaced early, estimates marked for reliability, and a clear critical path.

## Use When

- Breaking a spec, feature, or brief into executable tasks.
- Planning a refactor or migration across multiple steps.
- Estimating delivery scope before sprint commitment.
- Identifying the critical path for a body of work.
- Surfacing delivery unknowns before implementation starts.

## Avoid When

- Requirements still need to be written — use spec-writing first.
- The task is code review or refactoring — use code-review.
- The task is architectural decision-making — use discovery.
- Scope is too vague to produce atomic tasks — clarify before proceeding.
- Executing a confirmed plan — use `plan-execution`.

## Workflow

1. Confirm scope, constraints, and success bar; if scope is ambiguous, ask one question before proceeding.
2. Select independently shippable vertical slices, then consult `references/workflow.md` for decomposition, dependencies, estimates, done criteria, unknowns, and critical path.
3. Deliver the task graph and surface blockers before implementation.

## Output Contract

Default:

```text
tasks:
- id: T-01
  title: ...
  estimate: S|M|L
  estimate_reliability: high|low
  depends_on: []
  done_when: ...

dependencies:
- T-01 → T-02: reason

risks:
- ...

critical_path:
- T-01 → T-03 → T-05

unknowns:
- U-01: ...

validation:
- ...
```

## Handoffs

- Consume `spec-writing` output when scope, requirements, and acceptance criteria are stable enough to decompose into executable tasks.
- Hand off execution of the confirmed task graph to `plan-execution`.
- After producing the task graph, hand off to implementation or review skills only when a downstream request targets code, tests, docs, or operations work.

## Error Handling

1. Local: If a task cannot be made atomic, split it or mark it as a spike with an explicit timebox.
2. Flow: If an unknown blocks all tasks, stop and surface it before estimating; do not fabricate a plan around unresolved uncertainty.
3. Recovery: If scope changes after the plan is produced, re-run from step 2 for affected tasks only; do not silently update estimates.

## Validation Checklist

- [ ] Every task is independently shippable (no horizontal layers).
- [ ] Every task has a concrete done_when condition.
- [ ] Unreliable estimates are marked explicitly.
- [ ] All unknowns are named — none hidden inside task descriptions.
- [ ] Critical path is identified.
- [ ] Dependencies distinguish blockers from ordering preferences.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — read when producing the standard task graph.
- `assets/examples/happy-path.md` — read when planning a clear feature delivery.
- `assets/examples/edge-case.md` — read when unknowns block planning.
- `scripts/validate-output.py` — run when validating output structure.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate skill output.
- `tests/validation-checklist.md` — read when reviewing planning requirements.

## References

- Read `references/workflow.md` for decomposition details after selecting vertical slices.
- Read `references/examples.md` when comparing sample delivery plans.

## Rules

- `rules/vertical-slicing.md` — read when ensuring tasks are independently shippable.
- `rules/unknown-exposure.md` — read when surfacing blockers and unknowns.
- `rules/estimate-integrity.md` — read when assigning estimates.
- `rules/critical-path.md` — read when identifying the critical path.
