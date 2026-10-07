# Delivery Engine — Output Template

## Default (tasks + dependencies + risks + critical path + unknowns + validation)

```text
tasks:
- id: T-01
  title: <what the task delivers — end-to-end shippable slice>
  estimate: S|M|L
  estimate_reliability: high|low
  depends_on: []
  done_when: <concrete, verifiable completion condition>

- id: T-02
  title: ...
  estimate: M
  estimate_reliability: high
  depends_on: [T-01]
  done_when: ...

dependencies:
- T-01 → T-02: <why T-02 needs T-01 to complete first>

risks:
- <risk description> — <likelihood: low|medium|high> / <impact: low|medium|high|critical>

critical_path:
- T-01 → T-02 → T-05

unknowns:
- U-01: <what must be resolved> — owner: <person or team>

validation:
- <how to confirm the full delivery is complete and correct>
```

## Spike Template (task with unresolved uncertainty)

A spike is a regular task entry within the full output. Place it under `tasks:` alongside any follow-on work it unblocks:

```text
tasks:
- id: T-01
  title: Spike — <what needs to be understood>
  timebox: <hours or days>
  estimate_reliability: low
  depends_on: []
  done_when: Decision recorded in ADR or equivalent; T-02 unblocked.

- id: T-02
  title: <follow-on task enabled by spike outcome>
  estimate: M
  estimate_reliability: low
  depends_on: [T-01]
  done_when: <concrete, verifiable condition>

dependencies:
- T-01 → T-02: T-02 cannot be scoped until the spike decision is recorded.

risks:
- Spike may conclude the approach is not viable — impact: high / likelihood: low

critical_path:
- T-01 → T-02

unknowns:
- U-01: <what must be resolved> — owner: <person or team>

validation:
- Spike outcome is documented; T-02 estimate updated to high reliability before work begins.
```

## Fast Path (small, single-engineer delivery)

For small, low-risk work use the same schema with abbreviated entries. All required sections must still be present:

```text
tasks:
- id: T-01
  title: <title>
  estimate: S|M|L
  estimate_reliability: high
  depends_on: []
  done_when: <condition>

- id: T-02
  title: <title>
  estimate: S|M|L
  estimate_reliability: high
  depends_on: [T-01]
  done_when: <condition>

dependencies:
- T-01 → T-02: <reason>

risks:
- <risk> — low / low

critical_path:
- T-01 → T-02

unknowns: none

validation:
- <how to confirm completion>
```

## Rules

- Every task must be independently shippable — no horizontal layers.
- `done_when` must be concrete and verifiable, not subjective ("works correctly" is not a done condition).
- Mark `estimate_reliability: low` whenever the task depends on an unresolved unknown or unvalidated assumption.
- Unknowns live in the `unknowns:` section, not inside task titles.
- Critical path must list task IDs in order, not just name the area of risk.
