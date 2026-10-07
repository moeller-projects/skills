# Rule: Standard Sections

> Impact: medium

## Description

Structure output as status, severity, impact, timeline, mitigation, root-cause, follow-ups, and comms so anyone joining the incident mid-flight can catch up in one read.

## Apply When

- Emitting any incident artifact, live or post-incident.

## Checks

- Status and severity are declared before any detail.
- Timeline is separated from mitigation actions.
- Follow-ups are separated from the incident narrative.

## Anti-Pattern

A chat-style incident log where the current status and the next action are buried in prose.
