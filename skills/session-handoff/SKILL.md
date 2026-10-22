---
name: session-handoff
description: User-invoked only: Create a portable handoff document that lets a fresh agent or colleague continue work with its state, decisions, next action, and references.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Session Handoff
  version: "1.0.4"
  summary: Create a portable handoff document that lets a fresh agent or colleague continue work with its state, decisions, next action, and references.
  invocation: user
---

# Session Handoff

## Purpose

Write a handoff document a fresh agent — with zero memory of this session — can continue the work from. Portability is the point: new session, new harness, new directory, or a colleague.

## Workflow

1. Ask (or infer from the request) what the *next* session will be used for; tailor the document to that purpose.
2. Inventory what already exists as durable artifacts — specs, plans, ADRs, issues, commits, diffs — and reference them by path or URL. Never duplicate their content unless the recipient cannot access the source.
3. For another machine, harness, or colleague, verify delivery is accessible (shared URL, synced repository, or attached archive). If references are not accessible, include the full portable contents or a clearly named export and say what is missing.
4. Record reference roots and repository revision (commit/hash or explicit uncommitted state), plus how relative paths resolve; do not hand off ambiguous local paths.
5. Write what exists nowhere else: the current state, the decisions made in conversation and why, the exact next action, open questions, and traps already discovered.
6. Include a "suggested skills" section naming which skills the next agent should invoke, so the route through the catalog survives the transition.
7. Redact secrets, tokens, and personal data before writing.
8. Save to the OS temporary directory (not the workspace) unless the user asked otherwise; report the absolute path.

## Output Contract

```text
handoff:
  path: <absolute path written>
  purpose: <what the next session is for>
state: <where the work stands right now>
decisions:
- <decision made in conversation and why — only what no artifact records>
next_action: <the exact first step for the next agent>
suggested_skills:
- <skill name — why it applies>
open_questions:
- <unresolved item, or "none">
references:
- path_or_url: <accessible path or URL>
  root: <repository/reference root used to resolve relative paths>
  revision: <commit/hash, tag, or "uncommitted">
  access: <how recipient can access it>
portable_contents:
- <full content or export path for anything inaccessible; "none" when all references are accessible>
```

`next_action` MUST be concrete enough to execute without re-reading this conversation. `references` MUST cover anything the handoff omits deliberately.

## Handoffs

- Hand off improvement of the agent environment discovered during the session to `session-retro`.
- Hand off finished, verified work to `branch-integration` before handing off mid-flight.

## Error Handling

1. If the session contains no state beyond durable artifacts, say so and point at the artifacts instead of writing a near-empty document.
2. If sensitive material is entangled with necessary context, redact and note the redaction; never carry secrets into the handoff.

## Validation Checklist

- [ ] The document stands alone for a zero-context reader.
- [ ] Existing artifacts are referenced, not duplicated.
- [ ] The next action is exact and executable.
- [ ] Suggested skills are named with reasons.
- [ ] Secrets and personal data are redacted.
