# Triage Labels

## Labels and verdict mapping

| Label | Meaning | `review-response` verdict | Planned action |
|---|---|---|---|
| `accept` | Reviewer is right; a change is needed. | `accepted` | Apply an approved fix and cite its commit. |
| `push-back` | Reasoned disagreement. | `declined` | Explain the technical reason and invite discussion. |
| `unclear` | The requested change is ambiguous. | `clarification-needed` | Ask exactly what is unclear; do not guess. |
| `answer` | Reviewer asked a question and no code change is needed. | `answered` | Answer with code or documentation evidence. |
| `already-fixed` | A later commit already addressed it. | `accepted` | Cite the verified commit; do not claim a new change. |
| `out-of-scope` | Valid feedback belongs outside this PR. | `declined` | Explain scope and ask whether to record a follow-up. |
| `awaiting-reviewer` | The last speaker is the PR author. | none | Skip and report the thread. |

## Thread state rules

- Sort comments by `comment_id` and inspect the full conversation.
- Identify the PR author by matching `author_id` to `pull_request.created_by.id`; display names are not reliable identity keys.
- If either stable identity is absent, do not guess who spoke last. Ask or leave the thread unclassified.
- For active threads, if the PR author is the latest meaningful speaker and no reviewer followed up, label `awaiting-reviewer`.
- For resolved threads, skip only when the latest meaningful comment is from the PR author or there is no meaningful comment; retain a thread whose latest meaningful speaker is a reviewer.
- The normalized handoff has no reliable status-transition timestamp. Do not claim a reviewer comment occurred after resolution unless the payload proves that order.
- Outdated diff anchors alone are not a skip reason.

## Grouping and batching

- Threads with one root cause may share one commit naming all included thread IDs; each thread still gets its own reply.
- Present approvals in batches of at most 10, grouped by file or priority, blocking first.

## Triage output shape

```text
threads:
- T-12 [accept] /src/order.ts:42 — <point> — evidence: <what the code shows> — plan: <one-line change>
- T-15 [push-back] /src/auth.ts:88 — <point> — evidence: <what breaks or context missing>
- T-17 [unclear] /src/db.ts:10 — <what is ambiguous>
- T-18 [answer] general — <question>
- T-20 [already-fixed] commit abc1234 addresses it
- T-21 [out-of-scope] route to a follow-up
skipped_threads:
- T-09 awaiting-reviewer
```
