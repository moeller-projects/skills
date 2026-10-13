---
name: domain-modeling
description: Build and sharpen a project's domain model as a shared language between the user and the agent. Use when discussing codebase terminology, resolving fuzzy or overloaded terms, or recording a hard-to-reverse decision as an ADR. Challenge terms against the glossary and stress-test with edge-case scenarios. Glossary or ADR file edits occur only when the user explicitly requests that artifact change; discussion alone does not authorize mutation. Do not use for general technical documentation (use technical-writing) or for module interface design (use codebase-design).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Domain Modeling
  version: "1.0.2"
  summary: Keep the project's shared language sharp; propose glossary terms and ADRs, and mutate artifacts only when explicitly requested.
  invocation: model
---

# Domain Modeling

## Purpose

Maintain a shared language between user and agent so both stop translating jargon. A precise glossary makes conversations shorter, code consistently named, and the codebase easier to navigate. This is the *active* discipline — changing the model. Merely *reading* a glossary for vocabulary is a habit any skill can have, not this skill.

## Use When

- A conversation uses vague, overloaded, or conflicting domain terms.
- Writing or editing a `GLOSSARY.md` at the repo root (follow `GLOSSARY-MAP.md` if the repo has multiple contexts).
- A hard-to-reverse, non-obvious decision was just made and needs an ADR in `docs/adr/`.

## Avoid When

- General documentation work — use `technical-writing`.
- Designing a module's interface or shape — use `codebase-design`.

## Workflow

1. **Challenge against the glossary.** When a term conflicts with existing glossary language, call it out immediately: "Your glossary defines X as A, but you seem to mean B — which is it?"
2. **Sharpen fuzzy language.** When terms are vague or overloaded, propose a precise canonical term: "Do you mean the Customer or the User? Those are different things."
3. **Stress-test with scenarios.** Invent concrete edge-case scenarios that force precision about boundaries between concepts.
4. **Cross-reference with code.** When the user states how something works, check whether the code agrees; surface contradictions: "The code cancels entire Orders, but you said partial cancellation is possible — which is right?"
5. **Update only when authorized.** If the user explicitly requests a glossary edit, write the resolved term to `GLOSSARY.md` immediately (create lazily, follow `GLOSSARY-MAP.md` when present). If the user explicitly requests an ADR, record it in `docs/adr/`. Otherwise return the proposed definition or decision in the output contract without mutating files. A glossary contains definitions only: no specs, scratch notes, or implementation details.
6. **Offer ADRs sparingly** — only when all three hold: the decision is hard to reverse, surprising without context, and the result of a real trade-off. Numbered `docs/adr/NNNN-<dash-case-title>.md`.

## Output Contract

```text
terms_resolved:
- term: <canonical term>
  definition: <one or two sentences, no implementation detail>
  replaced: <fuzzy or conflicting usage, or "none">
adrs:
- <NNNN-title — the decision and the trade-off recorded, or "none">
contradictions:
- <glossary-vs-code or user-vs-code mismatch surfaced, or "none">
```

## Handoffs

- Hand off module-shape questions the terminology exposes to `codebase-design`.
- Hand off decisions that need a full design interview to `discovery`.

## Error Handling

1. If the user rejects a proposed term, return the rejection reason as a decision-record candidate; write an ADR only when explicitly requested and when the decision is hard to reverse, surprising, and a real trade-off. Link `decision-mapping` when available.
2. If the codebase contradicts both the glossary and the user, surface the three-way mismatch and ask which is authoritative before proposing any file mutation.

## Validation Checklist

- [ ] Resolved terms are written to the glossary immediately only when the user explicitly authorized a glossary edit; otherwise no file mutation occurs.
- [ ] Glossary entries carry no implementation details.
- [ ] Fuzzy terms were challenged with concrete scenarios, not accepted.
- [ ] ADRs were offered only for hard-to-reverse, surprising, real trade-offs and written only when explicitly requested.
- [ ] Code contradictions were surfaced, not papered over.
