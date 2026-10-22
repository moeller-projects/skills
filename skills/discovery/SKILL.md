---
name: discovery
description: Use when the problem is vague, assumptions need pressure-testing, or options must be compared before commitment. Do not use when scope is fixed and the output must be an executable task breakdown with dependencies and done criteria.
metadata:
  title: Discovery
  version: "1.1.4"
  summary: Explore ambiguous problems, test assumptions, compare options, and produce decision-ready plans.
  invocation: "model"
---
# Discovery

## Purpose

Explore unclear problems, challenge assumptions, surface blind spots, generate options, and turn ambiguity into a decision-ready plan.


## Workflow

1. MUST restate the problem, constraints, and success bar; if the problem remains vague after restatement, interview in frontier rounds (see `rules/frontier-rounds.md`): map open decisions as a design tree, ask the whole askable frontier per round — numbered questions, each with a recommended answer worded so "yes" accepts it. Facts are the agent's job (code, docs, tools); the user answers decisions, never lookups. Frontier rounds remain the default; ask one targeted question only when a blocking contradiction is discovered mid-execution and the rest of the frontier cannot be answered coherently.
2. MUST audit assumptions, risks, unknowns, and hidden dependencies.
3. MUST generate a small set of materially different options.
4. MUST compare tradeoffs, pressure-test MVP scope, and note blind spots.
5. MUST recommend a path with explicit next steps and open questions. Do not act on the result until the user confirms shared understanding.

## Output Contract

Default:

```text
problem:
- ...

assumptions:
- ...

options:
1. ...

recommendation:
- ...

next:
- ...
```

## Handoffs

- Hand off to `spec-writing` when exploration resolves the problem into a concrete requirement or policy-writing task.
- Hand off to `task-planning` when scope is fixed and the next output must be an executable task plan with dependencies and done criteria.
- Hand off terminology conflicts and hard-to-reverse decisions surfaced during exploration to `domain-modeling`.

## Error Handling

1. Local: Frontier rounds are the default when ambiguity remains. Ask one targeted question only when a blocking contradiction is discovered mid-execution and the rest of the frontier cannot be answered coherently.
2. Flow: Skip option comparison if only one viable path exists; state the reasoning explicitly.
3. Recovery: Return to the problem restatement step if new information invalidates prior assumptions.

## Validation Checklist

- [ ] Problem restated with constraints and success bar.
- [ ] Assumptions audited before options are generated.
- [ ] At least 2 materially different options (unless only 1 is viable; ruled-out list required).
- [ ] Recommendation includes blind spots.
- [ ] Open questions listed and gated.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — read when formatting a discovery result.
- `assets/examples/happy-path.md` — read when an example with multiple viable options is needed.
- `assets/examples/edge-case.md` — read when documenting a single viable option and its ruled-out alternatives.
- `scripts/validate-output.py` — run when validating a candidate output; only execute when explicitly authorized.
- `tests/run-validation.py` — run when validating the skill implementation; only execute when test execution is explicitly authorized.
- `tests/validation-checklist.md` — read when reviewing the skill's validation requirements.

## References

- See `references/workflow.md` when applying the detailed workflow or frontier-round guidance.
- See `references/examples.md` when a compact decision-artifact example is needed.

## Rules

- `rules/assumption-audit.md` — read before generating options to separate facts, assumptions, and unknowns.
- `rules/option-generation.md` — read when multiple strategy paths need comparison.
- `rules/decision-readiness.md` — read when preparing the recommendation and next steps.
- `rules/frontier-rounds.md` — read when interviewing the user about unresolved decisions.
