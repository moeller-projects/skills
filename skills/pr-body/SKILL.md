---
name: pr-body
description: Write the body of a pull request. Use when creating or updating a PR description, when a change is about to be opened for review, or when a PR body needs to explain a diff. Produces the smallest visual that makes the change clear, before/after evidence that it works, and a merge-danger call with blast radius. Do not use for reviewing a PR's content (use pr-review), planning the commits and branches behind it (use git-workflow), or managing a stacked PR (use gh-stack).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: PR Body
  version: "1.0.2"
  summary: Write PR bodies with the smallest clarifying visual, before/after evidence, and an honest call on what merging risks, including explicit verification gaps when proof is not authorized.
  invocation: model
allowed-tools: read_file
---

# PR Body

## Purpose

Produce a PR body a reviewer can act on in one read: the smallest visual that makes the change clear, evidence the change works, and an honest call on what merging risks.


## Output Contract

Produce exactly this structure:

```markdown
## Summary

<the smallest visual that makes the key point clear>

## Evidence

- **Before:** <screenshot, output, or failing test run>
  **After:** <screenshot, output, or passing test run>

## Merge Danger

**Door:** <one-way or two-way>

**Blast Radius:** <one-word scope of potential impact, with optional one-line ramifications>
```

## Rules

- No preambles; prose stays brief. Use the project's domain vocabulary (read `GLOSSARY.md` if the repo has one).
- **Summary** picks the smallest adequate view: pseudocode for logic, a call tree for control flow, a shallow file tree for layout or ownership, a diff-sketch when the surrounding shape already exists and only the delta matters, Mermaid only for genuinely graph-shaped relationships. Several small visuals beat one exhaustive one; do not use every form.
- **Evidence** is before/after and concrete. Screenshots for visual changes; execution output or the exact failing-then-passing test otherwise.
- **Merge Danger** names the door: two-way (cheap to roll back) or one-way (destructive, schema, data, or hard-to-reverse), plus blast radius — who or what breaks if this is wrong: consumers, layout, mobile, migrations, downstream stacks.
- Match the repo's PR template when one exists; this contract fills any section the template leaves open.

## Handoffs

- Hand off review of the PR's content to `pr-review`.
- Hand off unverified evidence claims to `verification-before-completion`. Run the before/after proof only when the user explicitly authorizes that covered operation; otherwise use existing observed evidence and identify the precise verification gap.
- Hand off stack management for stacked PRs to `gh-stack`.

## Error Handling

1. If before/after evidence cannot be produced (no runnable environment or explicit authorization), state what was observed instead and mark the precise verification gap explicitly — never fabricate a run.
2. If the change is too large for one clarifying visual, say so and recommend splitting the PR via `git-workflow` before writing the body.

## Validation Checklist

- [ ] Summary leads with a visual, not prose.
- [ ] The visual is the smallest one that makes the change clear.
- [ ] Evidence shows observed before and after runs when authorized and available; otherwise existing observed evidence and the precise verification gap are stated.
- [ ] Merge danger names door type and blast radius.
- [ ] Domain vocabulary matches the project's glossary.
