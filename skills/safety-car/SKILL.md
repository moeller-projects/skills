---
name: safety-car
description: Use when responding to a live production incident — triage, mitigation-first stabilization, timeline capture, comms, and postmortem follow-ups. Do not use when the task is planned deployment or rollback design (use pit-crew), non-urgent code defects (use mechanic), or writing specs for permanent fixes before the incident is stable.
allowed-tools:
  - read_file
title: Safety Car
version: 2.0.0
summary: Respond to live production incidents with mitigation-first triage, disciplined timelines, clear comms, and durable follow-ups.
---

# Safety Car

## Purpose

Respond to live production incidents: stabilize first, capture a trustworthy timeline, keep communication factual, and convert every incident into durable follow-ups once the fire is out.

## Use When

- A production system is down, degraded, or corrupting data.
- Triaging an alert, user report, or suspected incident.
- Coordinating a mitigation, hotfix, or emergency rollback under time pressure.
- Running incident communication (status page, stakeholder updates).
- Writing a postmortem or follow-up plan after an incident.

## Avoid When

- The task is planned deployment, release, or rollback design — use `pit-crew`.
- The task is a non-urgent code defect — use `mechanic`.
- The task is specifying the permanent fix in detail before the incident is stable — mitigate first, then hand off.
- There is no incident and no incident artifact (postmortem request without an incident is a doc task — use `press-officer`).

## Workflow

1. MUST declare the incident: state severity (SEV1 / SEV2 / SEV3), current impact, and who is affected; if severity cannot be determined, declare the higher severity and downgrade later.
2. MUST mitigate before diagnosing: stop the bleeding (rollback, feature flag, failover, rate limit) before hunting root cause. If no safe mitigation exists, say so and escalate rather than experimenting in production.
3. MUST capture the timeline as events happen: UTC timestamp, actor, action, observation. Reconstructed timelines are marked as estimates.
4. MUST keep comms factual: what is impacted, what is being done, next update time. No speculation, no blame.
5. MUST identify root cause only after mitigation is verified; distinguish trigger, root cause, and contributing factors.
6. MUST end with follow-ups that have owners; an incident without follow-ups is not closed.

## Severity Guide

| Severity | Meaning | Examples |
|---|---|---|
| SEV1 | Service down or data loss for all/most users | full outage, corrupted writes, breached data |
| SEV2 | Major feature down or degraded for a significant subset | checkout failing, elevated error rates |
| SEV3 | Minor degradation, workaround exists | slow dashboard, one region elevated latency |

## Output Contract

Default:

```text
status: investigating | mitigated | monitoring | resolved
severity: SEV1 | SEV2 | SEV3

impact:
- ...

timeline:
- HH:MMZ actor — action/observation

mitigation:
1. ...

root-cause:
- ...

follow-ups:
- ...

comms:
- ...
```

During live response, emit the contract after each status change. Post-incident, emit it once in resolved form.

## Handoffs

- Hand off to `pit-crew` for permanent infrastructure, deployment, or reliability fixes once the incident is stable.
- Hand off to `mechanic` for the permanent code fix once the fire is out.
- Hand off to `press-officer` when the postmortem must become a durable document for a wider audience.
- Terminal skill during live response — nothing outranks stabilization.

## Error Handling

1. Local: If observability is unavailable (no logs, no dashboards), state the blind spot explicitly and fall back to user reports and synthetic checks.
2. Flow: If a mitigation makes things worse, revert it immediately, record it on the timeline, and return to the last known-good state before trying anything new.
3. Recovery: If root cause remains unknown at resolution, close the incident as `monitoring` with follow-ups for the investigation — never fabricate a cause.

## Human-in-the-Loop

Request explicit approval before:

- Any destructive mitigation (data deletion, mass session revocation, draining a region).
- Declaring an incident resolved while monitoring shows unresolved symptoms.
- Publishing external communications (status page, customer email).

## Validation Checklist

- [ ] Severity declared with current impact.
- [ ] Mitigation precedes root-cause analysis on the timeline.
- [ ] Timeline entries carry UTC timestamps.
- [ ] No speculative root cause stated as fact.
- [ ] Every follow-up has an owner.
- [ ] Destructive mitigations had explicit approval.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — concrete output template
- `assets/examples/happy-path.md` — SEV2 API outage end to end
- `assets/examples/edge-case.md` — incident with observability blind spots
- `scripts/validate-output.py` — validates output structure

## References

- See `references/workflow.md` for the detailed workflow.
- See `references/examples.md` for sample incident artifacts.

## Rules

- `rules/_sections.md`
- `rules/mitigate-first.md`
- `rules/timeline-capture.md`
- `rules/comms-discipline.md`
- `rules/postmortem-handoff.md`
