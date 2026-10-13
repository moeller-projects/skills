---
name: codebase-design
description: Shared vocabulary and discipline for designing deep modules — a lot of behavior behind a small interface, placed at a clean seam, testable through that interface. Use when designing or improving a module's interface, deciding where a test seam belongs, evaluating whether an abstraction earns its place, or making code more testable and navigable. Do not use for domain terminology (use domain-modeling) or for reviewing an existing diff (use pr-review).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Codebase Design
  version: "1.0.3"
  summary: Design deep modules — small interfaces over real behavior, at clean seams, testable through the interface.
allowed-tools: read_file
---

# Codebase Design

## Purpose

Design **deep modules**: a lot of behavior behind a small interface, placed at a clean seam, testable through that interface. The aim is leverage for callers, locality for maintainers, and testability for everyone. This skill is the shared vocabulary other skills consult — a reference, not a session to run.


## Vocabulary

- Use these terms for findings that need precise module vocabulary; do not replace them when they accurately describe the design:

- **Module**: anything with an interface and an implementation — scale-agnostic (function, class, package).
- **Interface**: everything a caller must know to use the module correctly — the signature plus invariants, ordering constraints, error modes, configuration, and performance characteristics.
- **Depth**: leverage at the interface — how much behavior a caller or test can exercise per unit of interface learned. Deep = lots of behavior, small interface. Shallow = interface nearly as complex as the implementation.
- **Seam**: the location where a module's interface lives — where behavior can be altered without editing in that place. Where the seam goes is its own design decision, distinct from what sits behind it.
- **Adapter**: a concrete thing satisfying an interface at a seam — describes role, not substance.
- **Leverage**: what callers get from depth — one implementation paying back across N call sites and M tests.
- **Locality**: what maintainers get from depth — change, bugs, and knowledge concentrate in one place; fix once, fixed everywhere.

## Principles

- Depth is a property of the interface, not the implementation. A deep module may be internally composed of small swappable parts; they are not part of the interface. Modules can have internal seams (private, for their own tests) as well as the external seam callers use.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam; two adapters means a real one.** Do not introduce a seam unless something actually varies across it.

## Designing for testability

1. Accept dependencies, don't create them (pass the gateway in; never `new` it inside).
2. Return results, don't produce side effects (compute the discount; don't mutate the cart).
3. Small surface area: fewer methods means fewer tests; fewer parameters means simpler setup.

## Workflow (when designing, not just consulting)

1. State the module's purpose in one sentence using the project's domain vocabulary.
2. Sketch the smallest interface that delivers it; ask what can be hidden, not what can be exposed.
3. Apply the deletion test and the one-adapter rule before committing to a seam.
4. Prefer existing seams over new ones; the ideal number of seams in a codebase is small.
5. Record a shape decision as an ADR via `domain-modeling` only when it is hard to reverse, surprising without context, and the result of a real trade-off; otherwise keep it in the design notes.

## Handoffs

- Hand off domain naming questions to `domain-modeling`.
- Hand off the diff-level review of a designed change to `pr-review`.
- Hand off test-at-seam design to `test-strategy` and per-test discipline to `test-driven-development`.

## Validation Checklist

- [ ] The interface is smaller than the behavior it exposes (depth).
- [ ] The module survives the deletion test.
- [ ] Every seam has at least the prospect of two adapters.
- [ ] Tests can reach all behavior through the interface alone.
- [ ] Precise module terms are defined when findings rely on them.
