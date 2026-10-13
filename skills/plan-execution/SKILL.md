---
name: plan-execution
description: Execute a confirmed implementation plan task by task until done, with per-task proof and review. Use when you have a confirmed plan or task breakdown and the user wants it implemented — inline in this session, through fresh subagents per task, or with parallel agents for independent problem domains. Covers continuous execution without check-in pauses, ledgered rulings on plan defects, per-task review gates, and a final whole-branch review. Do not use when no confirmed plan exists yet (use task-planning or spec-writing), when requirements are still unclear (use discovery), or for a single trivial task that needs no plan.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Plan Execution
  version: "1.0.2"
  summary: Execute a confirmed plan to completion with per-task proof, review gates, and ledgered rulings.
---
# Plan Execution

## Purpose

Turn a confirmed plan into finished work. The plan already did the thinking: execute it exactly, review each task before moving on, and leave a record that survives your own forgetting. Verification evidence is required only when the user explicitly authorizes the relevant command; otherwise report implementation separately from unrun verification.


## Workflow

1. Set up: establish an isolated workspace via `git-worktrees` (never start implementation on the default branch without explicit user consent). Read the plan and its spec; the spec is the binding authority when they conflict. Keep a progress ledger file — context and todo lists are a live view, the ledger is the record; after any context loss, trust the ledger and `git log` over recollection, and never re-implement tasks whose commits already exist.
2. Pre-flight: scan the plan for cross-task interface conflicts — for every task consuming what an earlier task produces, check that producer and consumer agree. Rule on each conflict against the spec before Task 1.
3. Choose the execution mode:
   - **Subagent mode** (preferred when available): dispatch one fresh implementer per task with a review after each.
   - **Inline mode**: execute tasks yourself when the user chose it or no subagent tool exists — never fabricate a dispatch.
   - **Parallel dispatch**: only for independent problem domains with no shared state and no overlapping write scopes (e.g. unrelated failing test files); related failures are investigated together, not split.
4. Execute continuously. Do not pause to ask "should I continue?" between tasks. Only four things stop you: an irreversible or destructive operation; a security-sensitive action; a side effect outside the workspace that norms require asking about (merge, push to a shared branch, publish); or a plan so broken every path forward is a guess.
5. **Verify each performed operation independently.** Before choosing commands, check every operation the command may perform: test execution, dependency restore, compilation/build, packaging, migration, or deployment. Run only operations explicitly authorized and only when prerequisites already exist. If a requested test command would implicitly restore or build, report that conflict and select a no-restore/no-build form when available; otherwise do not run it. Record each skipped operation explicitly in the ledger and output (for example, “tests run; restore/build not run”).
6. When output contradicts the plan: if the code is wrong, use `debugging` — never patch a symptom to make output match. If the plan is wrong, rule on the smallest spec-satisfying change and ledger it as `Ruling: <finding> — <decision and why> — <cost if wrong>`; deviating without a ledgered ruling is a decision made in secret.
7. After all tasks: one fresh whole-branch review (a reviewer subagent if available). Critical and important findings get one fix pass; minor findings go to the ledger.
8. Hand off the finished branch to `branch-integration`.

## Subagent Dispatch Contract

- One dispatch describes one task — never the session's history. Include: one line of project context, the task brief as the single source of requirements (exact values, signatures, and test cases verbatim), interfaces and rulings from earlier tasks the brief cannot know, and the expected report format. Do not paste accumulated prior-task summaries into later dispatches.
- An implementer never dispatches its own subagents — review arrives from the controller, after the report.
- Handle the four report statuses: DONE → dispatch the task review; DONE_WITH_CONCERNS → read concerns, address correctness or scope doubts before review; NEEDS_CONTEXT → supply what is missing and re-dispatch; BLOCKED → change something before retrying (more context, a smaller task split, or a ledgered plan ruling) — never force an unchanged retry.
- The per-task review is a gate, not a formality: it checks spec compliance AND code quality against the task's diff (the full range since the task's base commit, never `HEAD~1`). Give the reviewer the brief, the report, and the diff — never pre-judge findings by telling it what to ignore. Implementer self-review never replaces it.
- Dispatch implementation subagents sequentially — parallel implementers conflict. Reserve parallel dispatch for independent domains.

## Output Contract

Return exactly these fields:

```text
status: complete|in_progress|blocked
mode: subagent|inline|parallel
tasks:
- id: <task id>
  status: done|in_progress|blocked
  evidence: <observed verification, or "not run — not authorized">
  review: <verdict, or "pending">
rulings:
- <finding — decision — cost if wrong, or "none">
final_review:
- <whole-branch verdict and fix-pass result, or "pending">
open_risks:
- <minor findings parked in the ledger, or "none">
verification:
- <implemented-work status and authorized verification status>
```

`status` MUST be one of the three listed values. A task is `done` when the implementation exists and its review gate passes; authorized verification evidence is also required when the user requested that verification. If verification was not explicitly authorized, report it as unrun rather than treating it as an implementation failure. `complete` requires a clean final review and must distinguish implemented work from verification that was not run.

## Handoffs

- Hand off workspace isolation to `git-worktrees`.
- Hand off per-task test discipline to `test-driven-development`; wrong-code failures to `debugging`.
- Hand off review of the finished branch's diff to `code-review` or `pr-review` when a full review is requested.
- Hand off incoming review feedback during execution to `review-response`.
- Hand off completion claims and the distinction between implemented work and unrun verification to `verification-before-completion`, then the finished branch to `branch-integration`.

## Error Handling

1. If context is lost mid-plan, resume from the ledger and `git log` at the first task without a completion record; completed tasks' commits exist even when memory does not.
2. If a subagent reports BLOCKED, diagnose the class of blocker — missing context, oversized task, defective plan — and change that one thing before re-dispatching.
3. If the plan is so broken that every path forward is a guess, stop and surface the defect to the user with the specific contradictions found.
4. If parallel agents' changes conflict on integration, stop dispatching, resolve the overlap yourself, and re-run the full suite only when the user explicitly authorized test execution; otherwise report verification as unrun.

## Validation Checklist

- [ ] Execution ran from an isolated workspace, not the default branch.
- [ ] A ledger recorded task completions and every ruling.
- [ ] Pre-flight checked cross-task interfaces before Task 1.
- [ ] When test execution was authorized, every task was watched failing, then passing; otherwise verification was reported as unrun.
- [ ] Every completed task passed a review gate; self-review never replaced it.
- [ ] Dispatches contained one task with exact values — never session history.
- [ ] Execution ran continuously; only the four named conditions stopped it.
- [ ] A fresh whole-branch review ran before handoff, with critical findings fixed; authorized verification was run when requested and otherwise reported as unrun.
- [ ] Parallel dispatch was used only for independent domains with disjoint write scopes.
