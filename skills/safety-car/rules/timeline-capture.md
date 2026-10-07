# Rule: Timeline Capture

> Impact: high

## Description

Record events as they happen with UTC timestamps, actor, action, and observation. The timeline is the incident's memory — lose it and the postmortem becomes fiction.

## Apply When

- From incident declaration until resolution.

## Checks

- Every entry carries a UTC timestamp, an actor, and an action or observation.
- Reconstructed entries are marked as estimates.
- Mitigations and their observed effects are both recorded.

## Anti-Pattern

Rebuilding the timeline from chat scrollback two days later and presenting guesses as facts.
