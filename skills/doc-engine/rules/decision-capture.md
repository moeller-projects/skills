# Rule: Decision Capture

> Impact: high

## Description

When a significant engineering decision is made, capture it as a durable record with enough context, reasoning, and tradeoff information that a future contributor can understand why the decision was made without reconstructing the conversation from scratch.

## Apply When

Document ONLY when the output is one of:
- An architectural decision that affects how the system is structured or how components interact.
- A reusable pattern that will recur in the codebase and should be followed consistently.
- A failure lesson where something went wrong and a concrete change was made as a result.
- A workflow or process insight that materially changes how the team or agent works.

## When Not to Apply

Do NOT produce a decision record for:
- One-off debugging sessions with no generalizable lesson.
- Temporary experiments or spikes where the output is "we tried X and discarded it."
- Speculative ideas or proposals that have not been decided.
- Decisions with confidence below roughly 60% — if the reasoning is still uncertain, wait.

## Output Format

A decision record must contain all five fields:

```text
decision:
  context: <what situation or problem prompted this decision>
  decision: <what was decided, stated concisely>
  reasoning: <why this option was chosen over alternatives>
  tradeoffs: <what is accepted or given up by this choice>
  reuse_scope: <where and when this decision applies — team, repo, module, pattern>
```

## Checks

- All five fields are present and non-empty.
- `reasoning` names at least one alternative that was considered and rejected.
- `reuse_scope` is specific enough to tell a future reader whether this decision applies to their situation.
- The record does not require reading the surrounding conversation to make sense.

## Anti-Pattern

Capturing a debugging session as an architectural decision because it felt significant at the time. Or writing a decision record for a proposal that has not been approved, creating the false impression that it is settled. Or omitting `tradeoffs` to make the decision look unambiguously correct.
