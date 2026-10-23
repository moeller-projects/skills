# Reply Style

## Language

- Write each reply in the language of the latest reviewer comment it answers.
- If the thread mixes languages, use the latest reviewer comment's language. If uncertain, use English.
- Keep code identifiers, API names, paths, SHAs, error messages, and quoted technical terms unchanged.

## Content rules

- State what was verified and what changed. Do not use gratitude or performative agreement (for example, “good catch” or “thanks for flagging”).
- Describe changes, not verification. Claim a test result only when it was observed after explicit test authorization; otherwise omit test claims from the reply.
- Cite fixes with a short commit SHA of at least 7 characters. Grouped threads cite the same SHA.
- Keep replies short, inside the thread, and without headings.

## Per-label shapes

| Label | Reply content |
|---|---|
| `accept` | What was verified, what changed, and the commit SHA. |
| `push-back` | The specific technical reason the current design holds; invite discussion without dismissiveness. |
| `unclear` | What is understood and exactly what needs clarification. |
| `answer` | A direct answer with a code or documentation reference. |
| `already-fixed` | The verified commit SHA and one sentence on how it addressed the point. |
| `out-of-scope` | Why it is valid but outside this PR, plus the follow-up and whether to record it. |

## Optional humanizer pass

Use only if a skill named `humanizer` is available. Read its `SKILL.md` first. Skip it if its language support is unsuitable. Apply it to reply bodies only, never triage output, commits, or code. Preserve every SHA, backticked token, path, number, error string, and the reply language exactly; discard output that changes an invariant or weakens a technical claim. Record whether it ran or why it was skipped.

## Posting hygiene

Reply bodies may contain backticks, quotes, and reviewer-derived text. Do not interpolate them into shell source. Pass the approved body as one `--content` argument using the tool's argument API. If only a shell is available, read it from a quoted temporary file into one argument without re-parsing it as shell code; delete the temporary file after posting.
