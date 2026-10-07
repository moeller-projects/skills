# Rule: Handoff Consumption

> Impact: critical

## Description

When input arrives as an ado-gateway handoff JSON rather than freeform text, apply these constraints:

- Reject the input if the JSON is malformed or if `producer` is not `ado-gateway`.
- Require `work_item.title` and `work_item.description` to be present and non-empty before generating any spec content.
- Treat `pr_comments` as review context only — never promote a PR comment into a functional requirement.
- Never invent requirements that are not supported by the handoff or direct input; if acceptance criteria are missing, leave the AC section incomplete and list the gap as an open question.
- Surface missing fields as open questions, not as placeholder text.

## Apply When

- Input is a JSON object with a `producer` field.

## Anti-Pattern

Treating PR comment content as authoritative requirements, or fabricating requirements to fill gaps in the handoff.
