# Scrutineer — Detailed Workflow

## 1. Scope the review

- Obtain the diff: pull request diff, `git diff`, patch file, or staged changeset.
- If the diff is truncated or unavailable, stop and ask for it. Do not reconstruct the change from the final file state.
- Note the stated intent (PR title, description, linked ticket). Review against that intent.

## 2. Read the changeset

- Read every changed hunk once before writing anything.
- Open surrounding files only where a hunk cannot be judged in isolation (callers, type definitions, schema).
- Track three buckets while reading: defects, questions, observations outside the diff.

## 3. Verify before reporting

- Confirm each suspected defect against the actual code path. Trace the data, check the caller, read the type.
- If confirmation is impossible from available context, report it as a question (`[minor] ... — question: does X handle Y?`), not as a defect.
- Never report style preferences as findings unless the repository has an enforced convention the change violates.

## 4. Sort and phrase

- Order findings: blocker → major → minor → nit.
- Severity guide:
  - blocker: defect, data loss, security hole, broken behavior — must not merge
  - major: correctness risk, missing error handling on a critical path, contract break
  - minor: clarity, small robustness, inconsistent naming
  - nit: taste-level suggestion, explicitly non-blocking
- Write each finding for the author: file:line, what, why, suggested change.

## 5. Fence the scope

- Move anything the author did not introduce into out-of-scope with a one-line reason.
- Name follow-up work explicitly so it can be ticketed instead of forgotten.

## 6. Issue the verdict

- approve: no blocker or major findings remain.
- request-changes: at least one blocker or major finding exists.
- comment: informational review, no merge assertion.
- State residual risk: what could still go wrong after merge, even on approve.

## 7. Re-review

- On re-review, check prior findings first and mark each as resolved or still open.
- Review only the new commits plus previously flagged hunks, unless the changeset was rewritten wholesale.
