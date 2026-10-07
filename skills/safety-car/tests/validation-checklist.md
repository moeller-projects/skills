# Safety Car — Validation Checklist

Run this checklist before accepting an incident artifact as complete.

## Trigger Check

- [ ] Task involves a live incident, incident triage, or a postmortem of a real incident.
- [ ] Task is NOT a planned deployment (pit-crew), a non-urgent defect (mechanic), or pure documentation (press-officer).

## Declaration Check

- [ ] Severity is declared as SEV1, SEV2, or SEV3 with current impact.
- [ ] Uncertain severity was declared at the higher tier.
- [ ] Incident lead and channel are named for live incidents.

## Mitigation Check

- [ ] Mitigation precedes root-cause analysis on the timeline.
- [ ] Mitigations are reversible, or destructive ones had explicit approval.
- [ ] One variable changed at a time; each attempt and effect recorded.
- [ ] "No safe mitigation exists" was stated explicitly when applicable, not skipped.

## Timeline Check

- [ ] Every entry has a UTC timestamp, an actor, and an action or observation.
- [ ] Reconstructed entries are marked as estimates.

## Comms Check

- [ ] Updates state impact, current action, and next update time.
- [ ] Suspected causes are labeled suspected; no blame appears anywhere.
- [ ] External communications had explicit approval.

## Closure Check

- [ ] Trigger, root cause, and contributing factors are stated separately.
- [ ] Unknown root cause is admitted as unknown — never fabricated.
- [ ] Every follow-up has an owner.
- [ ] Permanent fixes are handed off to pit-crew (infrastructure) or mechanic (code).
