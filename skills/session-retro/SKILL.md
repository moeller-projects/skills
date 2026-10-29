---
name: session-retro
description: "User-invoked only: Turn a completed session's observed failures into improvements to the agent environment—navigation, checks, standards, tooling, and steering."
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Session Retro
  version: "1.0.3"
  summary: Turn a completed session's observed failures into improvements to the agent environment—navigation, checks, standards, tooling, and steering.
  invocation: user
---

# Session Retro

## Purpose

Look back at a session and improve what the *next* session starts from: navigation, automated checks, coding standards, steering files, tooling. The unit of improvement is the agent's environment, not the code that was written.

## Workflow

1. Read the primary sources of the session being reviewed: its transcript or logs if available, else the user's account. Default to the current session if none is named.
2. Classify every observed failure or friction into exactly one improvement category:
   - **Navigation** — the agent took long to find the right files or facts → a navigation pointer in `AGENTS.md` or an index doc.
   - **Automated checks** — a mistake a deterministic check could have caught → a lint rule, typecheck, test, pre-commit hook, or CI job. Read the repo's existing check commands first; a check that exists but is unwired or silently broken is the finding, not a reinvention. A repo with no guardrail at all is itself a finding.
   - **Coding standards** — a mistake only judgment catches (cross-file consistency, style matching) → a rule in the standards doc a reviewer applies. Mechanical violations get deterministic checks, full stop; standards docs are reserved for judgment calls.
   - **Steering files** — bloated `AGENTS.md`/global instructions → move detail out to pointed-at docs; hunt instructions that change nothing about behavior (no-ops) and delete them.
   - **Tool economy** — expensive or token-inefficient tool usage → streamlined commands or better tooling.
   - **Information access** — the agent lacked a crucial fact → tee logs, read-only access, or a reference doc.
   - **Skills** — a skill misfired, was missing, or contradicted another → a fix routed to `skill-forge`.
3. Present candidates to the user ordered by severity, each with its category and the concrete artifact it would change. Recommendations are advisory: do not edit, create tickets, run checks, or orchestrate follow-up work until the user explicitly approves a candidate.
4. Apply only what the user approves.

## Output Contract

```text
session: <what was reviewed>
findings:
- severity: high|medium|low
  observation: <what actually happened in the session, with evidence>
  category: navigation|checks|standards|steering|tooling|access|skills
  improvement: <the concrete environment change proposed>
  artifact: <file or config it would change>
```

Every finding MUST cite observed session evidence; a hypothetical improvement ("it would be better if…") is not a finding.

## Handoffs

- Hand off code-level defects found during review to `debugging`.
- Hand off skill creation or repair to `skill-forge`.
- Hand off production-incident learning to `incident-response` (postmortem).

## Error Handling

1. If no session logs exist, interview the user about what went wrong; never invent observations.
2. If a proposed check already exists, verify whether it runs in CI/pre-commit before proposing it; an unwired check is the finding.

## Validation Checklist

- [ ] Every finding cites observed session evidence.
- [ ] Mechanical mistakes map to deterministic checks, not prose rules.
- [ ] Existing checks were inspected before proposing new ones.
- [ ] Improvements target the environment, not the code from the session.
- [ ] Findings are ordered by severity.
