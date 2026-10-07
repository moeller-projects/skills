---
name: ops-engine
description: Use when planning or reviewing CI/CD, infrastructure, containers, Kubernetes, rollout safety, or operational risk. Do not use when the task is pure application refactoring or documentation-only work.
allowed-tools:
  - read_file
title: Ops Engine
version: 5.0.1
summary: Plan safer delivery across CI/CD, containers, Kubernetes, reliability, threat modeling, and rollback decisions.
---

# Ops Engine

## Purpose

Handle DevOps, CI/CD, containers, Kubernetes, reliability, threat modeling, deployment safety, and operational risk with explicit safeguards.

## Use When

- Creating or reviewing CI/CD workflows.
- Working with Docker, containers, or Kubernetes.
- Threat modeling a service or deployment path.
- Designing resilience, rollback, or release safety plans.
- Analyzing operational or deployment risk.

## Avoid When

- The task is pure application refactoring.
- The task is pure documentation.
- Security review of application or library code is needed — that belongs to `code-quality-engine`; ops-engine covers infrastructure, deployment, and cluster security only.

## Workflow

1. MUST define the system boundary, change surface, and operational risk; if scope is unclear, stop until confirmed.
2. MUST identify delivery, security, and runtime failure modes.
3. MUST design the safest plan for build, release, runtime, and rollback.
4. MUST verify reproducibility, least privilege, and observability needs.
5. MUST deliver the plan with checks, rollback, and security notes; MUST stop for human approval before any irreversible production step.

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

- Accepts work from `repo-engine` once the operational or deployment surface is identified.
- Accepts work from `spec-engine` when an approved spec includes infrastructure or deployment requirements.
- Terminal skill — output is the final artifact; no downstream handoff.

## Error Handling

1. Local: If a check command fails, retry once with verbose output before escalating.
2. Flow: Abort the plan if threat model surfaces an unacceptable risk without a mitigation path.
3. Recovery: Roll back to the last known-good state; preserve rollback artifacts before any destructive step.

## Human-in-the-Loop

Stop and request explicit human approval before:
- Executing any production deployment or migration.
- Running destructive operations (delete, overwrite, drain, scale to zero).
- Finalizing a rollback that cannot be reversed.

## Validation Checklist

- [ ] Risks listed before the plan with likelihood and impact.
- [ ] Every destructive step has a rollback entry with artifact.
- [ ] Human approval gate present before any production or destructive step.
- [ ] Unacceptable risk without mitigation aborts the plan.
- [ ] Every check is a concrete, executable command.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — Kubernetes liveness probe scenario
- `assets/examples/edge-case.md` — unacceptable risk abort scenario
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/examples.md` for sample operational plans.

## Rules

- `rules/_sections.md`
- `rules/deployment-safety.md`
- `rules/ci-cd-reproducibility.md`
- `rules/kubernetes-safety.md`
- `rules/threat-model-boundaries.md`
- `rules/resilience-rollback.md`
