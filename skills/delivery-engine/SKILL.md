---
name: delivery-engine
description: Use when confirmed scope must be broken into atomic tasks with dependencies, estimates, and done criteria. Do not use when requirements are still being written or the user wants option comparison or plan critique before scope is fixed.
allowed-tools:
  - read_file
title: Delivery Engine
version: 1.0.1
summary: Break work into atomic, shippable tasks with explicit dependencies, critical path, estimates, and definitions of done.
---

# Delivery Engine

## Purpose

Turn a confirmed scope into a structured, executable task list that a team can commit to and track — with explicit dependencies, unknowns surfaced early, estimates marked for reliability, and a clear critical path.

## Use When

- Breaking a spec, feature, or brief into executable tasks.
- Planning a refactor or migration across multiple steps.
- Estimating delivery scope before sprint commitment.
- Identifying the critical path for a body of work.
- Surfacing delivery unknowns before implementation starts.

## Avoid When

- Requirements still need to be written — use spec-engine first.
- The task is code review or refactoring — use code-quality-engine.
- The task is architectural decision-making — use thinking-engine.
- Scope is too vague to produce atomic tasks — clarify before proceeding.

## Workflow

1. Confirm scope, constraints, and success bar; if scope is ambiguous, ask one question before proceeding.
2. Break the work into atomic vertical slices — each task must be independently shippable, not a layer or phase.
3. Map dependencies between tasks; identify which dependencies are hard blockers versus soft ordering preferences.
4. Assign size estimates (S / M / L) and mark any estimate as unreliable when the work is poorly understood.
5. Define done for each task — a concrete, verifiable completion condition.
6. Surface all unknowns as named items; never bury them inside a task description.
7. Identify the critical path — the dependency chain that determines the earliest possible completion date.

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

- Consume `spec-engine` output when scope, requirements, and acceptance criteria are stable enough to decompose into executable tasks.
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

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — feature delivery planning scenario
- `assets/examples/edge-case.md` — unknown-blocked plan scenario
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/examples.md` for sample delivery plans.

## Rules

- `rules/_sections.md`
- `rules/vertical-slicing.md`
- `rules/unknown-exposure.md`
- `rules/estimate-integrity.md`
- `rules/critical-path.md`
