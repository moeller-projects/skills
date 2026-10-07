# Scrutineer — Output Template

```text
verdict: approve | request-changes | comment
summary: <one line: what the changeset does and its overall quality>

findings:
- [blocker|major|minor|nit] path:line — issue
  why: <why it matters>
  suggestion: <concrete change>

out-of-scope:
- <pre-existing issue or follow-up — one-line reason>

risk:
- <what could still go wrong after merge>
```

Rules:

- Exactly one verdict line.
- `findings:` contains `- none` when the changeset is clean; never fabricate nits.
- `out-of-scope:` contains `- none` when nothing was observed.
- Every finding references a line inside the changeset.
