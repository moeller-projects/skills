---
name: research
description: Investigate a question against high-trust primary sources and capture findings as a cited Markdown file. Use when the user wants a topic researched, documentation or API facts gathered, a library or tool evaluated, or reading legwork delegated to a background agent while they keep working. Do not use for debugging a concrete failure (use debugging), codebase exploration (use codebase-onboarding), or a question that a quick inline answer can settle.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Research
  version: "1.0.1"
  summary: Delegate investigation to a background agent; capture cited findings from primary sources as Markdown.
  invocation: model
---

# Research

## Purpose

Investigate a question against **primary sources** — official docs, source code, specifications, first-party APIs — and capture the findings as a cited Markdown file. Follow every claim back to the source that owns it; never cite a secondary write-up of a source you could have read.


## Workflow

1. Sharpen the question into a testable form: what decision does the answer support?
2. Prefer a background agent so the main session keeps working; the agent's brief names the question, the decision riding on it, and the output path.
3. Investigate primary sources only. When a secondary source surfaces a claim, open the primary source it points to and cite that instead.
4. Write one Markdown file: findings organized by sub-question, every factual claim carrying its source URL or path, and a short "what this means for the decision" closing section.
5. Save where the repo already keeps such notes — match the existing convention; if none exists, put it somewhere sensible and say where.
6. Report the path and a three-line summary; the file carries the detail.

## Output Contract

```text
question: <the sharpened question>
report_path: <absolute path of the Markdown file>
key_findings:
- <finding — source>
confidence: <what remains unverified or conflicting, or "none">
```

Every key finding MUST name its primary source. A claim no primary source could be found for goes under `confidence`, not `key_findings`.

## Handoffs

- Hand off decisions the findings unblock to `discovery` or `spec-writing`.
- Hand off training-level knowledge gaps the findings reveal to `guided-learning`.

## Error Handling

1. If primary sources conflict, report both with their dates and state which is authoritative for the user's context and why.
2. If the question cannot be answered from accessible sources, say so, list what was searched, and name what access would unblock it.

## Validation Checklist

- [ ] Every cited claim traces to a primary source.
- [ ] The file states the decision the research supports.
- [ ] Conflicting or unverifiable claims are marked, not smoothed over.
- [ ] The report lives where the repo keeps such notes.
