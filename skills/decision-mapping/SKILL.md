---
name: decision-mapping
description: Chart a large, uncertain effort as a decision map, resolve its open questions, and hand off a clear route to specification.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Decision Mapping
  version: "1.0.2"
  summary: Chart a large, uncertain effort as a decision map, resolve open questions, and hand off a clear route to specification.
  invocation: user
---
# Decision Mapping

## Purpose

Chart the way through an effort too big and foggy for one session. The output is **decisions, not deliverables**: a shared map of decision tickets that shrinks the fog until the route to the destination is clear — then it hands off; it does not build.

## Concepts

- **Destination**: what reaching the end looks like — a spec to hand off, a decision to lock, or a change to make. Named first; it fixes the scope.
- **Map**: a single canonical artifact (an issue on the tracker, or a Markdown file) holding the destination, notes, and an index of decisions so far. The map is an index, not a store — a decision lives in exactly one place, its ticket.
- **Ticket**: one decision or investigation, sized to one session, with blocking edges to the tickets that gate it. Refer to tickets by *name*, never bare numbers, in anything a human reads.
- **Frontier**: the open, unblocked, unclaimed tickets — what can be worked now.
- **Fog**: in-scope questions you can sense but cannot yet state precisely. Write them loosely under "Not yet specified"; they graduate into tickets as the frontier advances. The test: ticket when the question is already sharp, fog when it is not.
- **Out of scope**: work ruled beyond the destination. Not fog — it never graduates.

## Workflow

**Charting (first session):**

1. Name the destination through a `discovery` interview — it shapes every ticket.
2. Fan out breadth-first: surface the open decisions and the first steps takeable now. If no fog surfaces, you don't need a map — stop and proceed with `discovery` directly.
3. Create the map with destination and notes; sketch the fog into "Not yet specified".
4. Create the tickets you can already state sharply, then wire their blocking edges in a second pass.
5. Kick off `research` for tickets that are pure fact-finding. Stop — charting is one session's work.

**Working the map (later sessions):**

1. Load the map's low-resolution view, not every ticket body.
2. Pick the first frontier ticket (or the one the user named) and claim it before working. Reconcile the map's claimed, resolved, and closed ticket states against the canonical index before acting; preserve each ticket's resolution source.
3. Resolve it by type: research (delegate to `research`), prototype (via `prototype`), conversation (via `discovery` + `domain-modeling`), or task (manual work that unblocks a decision).
4. Record the resolution on the ticket, close it, and append a one-line pointer to the map's decision index. Re-running this reconciliation MUST be idempotent: existing canonical entries and resolution sources are preserved rather than duplicated or overwritten.
5. Graduate any fog the answer made specifiable into new tickets; close tickets the answer ruled out of scope. Resolve one ticket per session by default so each decision gets enough investigation and a clear record; finish multiple tickets in one session only when the same evidence or conversation directly resolves them. Pure research tickets remain the exception.
**When the way is clear:** hand off to `spec-writing`, which collapses the map's linked decisions into a buildable spec — not straight to implementation, which would throw the linked detail away.

## Output Contract

```text
destination: <what reaching the end looks like>
map: <path or URL of the map artifact>
frontier:
- <ticket name — type — why it is takeable now>
fog:
- <suspected question not yet sharp enough to ticket, or "none">
resolved_this_session:
- <ticket name — decision — where it was recorded, or "none">
```

## Handoffs

- Hand off fact-finding tickets to `research`, look-and-feel questions to `prototype`.
- Hand off terminology and decision records to `domain-modeling`.
- Hand off a cleared map to `spec-writing`, then the normal flow.

## Error Handling

1. If the destination cannot be named after one interview round, the effort is actually several — say so and split it before charting.
2. If a resolution invalidates standing tickets, update or close them the same session; stale maps mislead every future session.
3. If a ticket's question turns out to be unanswerable without building something, convert it to a `prototype` ticket rather than guessing.

## Validation Checklist

- [ ] The destination is named before any ticket exists.
- [ ] The map indexes decisions; detail lives in tickets.
- [ ] Every ticket is one decision, sized to one session, with explicit blocking edges.
- [ ] Fog is recorded loosely, never pre-sliced into fake tickets.
- [ ] By default, at most one non-research ticket was resolved; multiple resolutions are justified only when the same evidence or conversation directly resolved them.
- [ ] A cleared map hands off to spec-writing, not to implementation.
