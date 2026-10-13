---
name: prototype
description: Build throwaway code that answers one design question. Use when a design question is hard to settle on paper — sanity-checking whether a state model or logic feels right, or exploring what a UI should look like — and a runnable artifact would resolve it faster than discussion. Do not use for production implementation (use plan-execution or test-driven-development), reproducing a bug (use debugging), or questions that a quick discussion can settle.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Prototype
  version: "1.0.2"
  summary: Answer one design question with throwaway, trivially-runnable code, then record the verdict in its spec or ticket; production edits require a separate implementation scope.
  invocation: model
---

# Prototype

## Purpose

A prototype is **throwaway code that answers a question**. The question decides the shape; getting the branch wrong wastes the whole prototype.


## Workflow

1. **Name the question** the prototype must answer, in one sentence. If you cannot, the prototype has no purpose — go back to `discovery`.
2. **Pick the branch:**
   - *Logic / state model* → a single shareable HTML file (or minimal script) that pushes the state machine through the cases hard to reason about on paper, drivable by a non-developer.
   - *UI* → several radically different variations on one route or page, switchable without editing code (URL param or a small switcher).
   If genuinely ambiguous, default to whichever branch matches the surrounding code (backend module → logic; page or component → UI) and state the assumption at the top of the artifact.
3. **Build it under the prototype rules** (below).
4. **Report the verdict**: the question, the answer the prototype gave, and what should change in the real design.
5. **Capture**: fold any validated decision into the real design by recording it in the spec or ticket it informed; production code edits belong to a separate, explicitly authorized implementation scope. Keep the prototype itself as a primary source on a clearly-marked throwaway branch or scratch path, pointed at from that spec or ticket. The main branch keeps only the validated decision.

## Prototype Rules

1. **Throwaway from day one, and clearly marked as such** — placed near the code it prototypes, named so no reader mistakes it for production.
2. **Trivial to run** — one command or one double-click; no setup thinking required.
3. **No persistence by default** — state lives in memory; persistence is what the prototype is *checking*, not something it depends on.
4. **Skip the polish** — no tests, no error handling beyond what makes it runnable, no abstractions. The point is to learn fast.
5. **Surface the state** — after every action or variant switch, render the full relevant state so the user sees what changed.

## Output Contract

```text
question: <the one-sentence design question>
branch: logic|ui
artifact: <absolute path or throwaway branch>
verdict: <the answer the prototype gave>
fold_back:
- <what should change in the real design, or "none — idea rejected">
capture: <where the prototype is preserved as a primary source>
```

`verdict` MUST answer the stated question; "it works" is not a verdict.

## Handoffs

- Hand off a settled design to `spec-writing` or `task-planning`.
- Hand off a rejected idea's load-bearing reason to `domain-modeling` (ADR) so it is not re-litigated.

## Error Handling

1. If the prototype cannot be made trivially runnable in the project's environment, shrink the question until it can.
2. If the user starts treating the prototype as the implementation, stop and restate the throwaway contract before continuing.

## Validation Checklist

- [ ] The question is one sentence and the verdict answers it.
- [ ] The artifact is marked throwaway and trivial to run.
- [ ] No tests, persistence, or polish were added.
- [ ] The validated decision was folded back; the prototype was captured out of the main branch.
