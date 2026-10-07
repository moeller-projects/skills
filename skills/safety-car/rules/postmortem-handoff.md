# Rule: Postmortem Handoff

> Impact: high

## Description

An incident ends with owned follow-ups, not with silence. Separate trigger, root cause, and contributing factors so follow-ups fix causes, not symptoms.

## Apply When

- Declaring an incident resolved, or writing the postmortem.

## Checks

- Trigger, root cause, and contributing factors are stated separately.
- Unknown root cause is admitted and tracked as a follow-up, never fabricated.
- Every follow-up has a named owner.
- Permanent fixes are handed off to pit-crew (infrastructure) or mechanic (code).

## Anti-Pattern

"Restarted the server, closing the ticket" — no cause, no follow-up, guaranteed repeat.
