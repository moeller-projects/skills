---
name: operations
description: Use when planning or reviewing CI/CD, infrastructure, containers, Kubernetes, rollout safety, or operational risk. Do not use when the task is pure application refactoring or documentation-only work, or when reviewing application/library security (use `code-review`; operations covers infrastructure, deployment, and cluster security).
metadata:
  title: Operations
  version: "1.0.6"
  summary: Plan safer delivery across CI/CD, containers, Kubernetes, reliability, threat modeling, and rollback decisions.
---

# Operations

## Purpose

Handle DevOps, CI/CD, containers, Kubernetes, reliability, threat modeling, deployment safety, and operational risk with explicit safeguards.

## Workflow
1. MUST define the system boundary, change surface, and operational risk; if scope is unclear, stop until confirmed.
2. MUST identify delivery, security, and runtime failure modes.
3. MUST design the safest plan for build, release, runtime, and rollback.
4. MUST verify reproducibility, least privilege, and observability needs.
5. MUST deliver the plan with checks, rollback, and security notes. Each destructive step MUST carry its own explicit human approval; approval for another step or the word production MUST NOT substitute for it.
6. MUST stop with an explicit `BLOCKED`/`ABORT` representation when prerequisites are absent; do not present executable steps after the abort.
7. MUST preserve the production artifact before destructive work and tie rollback to its exact namespace, cluster/context, and environment. Rollback MUST include a recovery check.

## Output Contract

Default:

```text
risk:
- ...

plan:
1. ...

checks:
- ...

rollback:
- ...

security:
- ...
```

## Handoffs

- Accepts work from `codebase-onboarding` once the operational or deployment surface is identified.
- Accepts work from `spec-writing` when an approved spec includes infrastructure or deployment requirements.
- Terminal skill — output is the final artifact; no downstream handoff.

## Error Handling

1. Local: If a check command fails, retry once with verbose output before escalating.
2. Flow: Abort the plan if threat model surfaces an unacceptable risk without a mitigation path.
3. Recovery: Roll back to the last known-good state; preserve rollback artifacts before any destructive step.

## Human-in-the-Loop

Stop and request explicit human approval before each affected step:
- Executing any production deployment or migration; approval MUST be recorded on that step.
- Running destructive operations (delete, overwrite, drain, scale to zero).
- Finalizing a rollback that cannot be reversed; preserve artifact and recovery context.

## Validation Checklist

- [ ] Risks listed before the plan with likelihood and impact.
- [ ] Every destructive step has a rollback entry with artifact.
- [ ] Human approval gate present before any production or destructive step.
- [ ] Unacceptable risk without mitigation aborts the plan.
- [ ] Every check is a concrete, executable command.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — read when formatting the operational plan.
- `assets/examples/happy-path.md` — read for a Kubernetes liveness-probe scenario.
- `assets/examples/edge-case.md` — read when an unacceptable risk must abort the plan.
- `scripts/validate-output.py` — run when validating an operational plan.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to validate skill output.
- `tests/validation-checklist.md` — read when checking the skill's validation requirements.

## References

- `references/examples.md` — read for sample operational plans.

## Rules

- `rules/deployment-safety.md` — read when planning deployment safeguards.
- `rules/ci-cd-reproducibility.md` — read when reviewing reproducibility.
- `rules/kubernetes-safety.md` — read when changing Kubernetes resources.
- `rules/threat-model-boundaries.md` — read when defining security boundaries.
- `rules/resilience-rollback.md` — read when planning resilience or rollback.
