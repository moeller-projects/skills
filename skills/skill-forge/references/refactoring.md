# Refactoring and auditing existing skills

Read this when improving, auditing, or repairing an existing skill.

## Contents

- [Audit rubric](#audit-rubric)
  - [1. Spec compliance](#1-spec-compliance-must-be-zero-errors)
  - [2. Description](#2-description-triggering)
  - [3. Context budget](#3-context-budget)
  - [4. Structure](#4-structure)
  - [5. Scripts](#5-scripts)
  - [6. Anti-patterns to fix on sight](#6-anti-patterns-to-fix-on-sight)
- [Evaluation-driven iteration](#evaluation-driven-iteration)
- [Triggering optimization](#triggering-optimization-description-tuning)

## Audit rubric

Work through these categories in order. Fix earlier categories first — a skill
with a broken description gains nothing from polished scripts.

### 1. Spec compliance (must be zero errors)

Run `python3 scripts/validate_skill.py <skill-dir> --strict`. Verify: SKILL.md
exists and parses; `name`/`description` present; name format and directory-name
match; description ≤1024 chars; compatibility ≤500 chars; no unknown frontmatter
fields.

### 2. Description (triggering)

- Does it say what the skill does AND when to use it, in imperative framing?
- Does it cover trigger contexts where the user doesn't name the domain?
- Is it over-broad (would fire on near-miss tasks that need a different skill)?
  Add boundary clauses.
- Near-miss test: list 3 prompts that share keywords but should NOT trigger;
  check the description would exclude them.

### 3. Context budget

- Body >500 lines or ~5k tokens → split detail into `references/`.
- Flag any sentence explaining things the agent already knows (what a CSV is,
  how HTTP works). Cut or compress.
- Duplicated information across SKILL.md and references → keep one home.
- Exhaustive edge-case coverage → trust agent judgment for rare cases.

### 4. Structure

- Every bundled file referenced from SKILL.md, with a stated when-to-read
  condition; no reference chains deeper than one level.
- Empty or unused `scripts/`, `references/`, `assets/` directories → delete.
- Forbidden clutter (README.md, CHANGELOG.md, etc.) → delete.
- Absolute or machine-specific paths → relative to skill root.

### 5. Scripts

When the user explicitly requests script execution, run each script (or a representative sample). Otherwise inspect scripts statically without running them. In either case, check: non-interactive; `--help`; actionable error messages; structured stdout vs diagnostics on stderr; pinned dependencies; idempotency; bounded output. If the agent would rewrite the same helper logic on every run, extract it into a tested script.

### 6. Anti-patterns to fix on sight

- "When to use" sections in the body (invisible at discovery) → fold into
  description.
- Rigid ALWAYS/NEVER rules without rationale → reasoning-based instructions.
- Option menus with no default → pick a default, demote alternatives.
- One-off answers hard-coded for a single task → generalize into a procedure.
- Generic filler ("follow best practices", "handle errors appropriately") →
  replace with the specific practice, or delete.

## Evaluation-driven iteration

When production-grade means *measurably* better, use structured evals rather
than vibes. The execution gate below applies to all evaluation runs.
1. **Test cases** in `evals/evals.json` inside the skill: realistic prompts,
   human-readable expected outputs, optional input files. Start with 2-3; vary
   phrasing and include one edge case.
2. **Execution gate:** Run eval cases only when the user explicitly requests
   evaluation execution in the current conversation. Otherwise inspect the
   cases, assertions, and expected output statically; do not run them.
3. **Run each case twice** — with the skill and without (or against a snapshot
   of the old version) — in clean sessions, saving outputs under
   `<workspace>/iteration-N/<eval-name>/{with_skill,without_skill}/outputs/`.
   Record tokens and duration per run.
4. **Assertions**: after seeing first outputs, add verifiable statements
   ("output is valid JSON", "chart has labeled axes"). Avoid vague or brittle
   ones. Grade each PASS/FAIL with quoted evidence; use scripts for mechanical
   checks, LLM judgment for the rest.
5. **Benchmark**: aggregate pass rates, time, tokens into `benchmark.json`;
   compute the delta between configurations. A skill that triples tokens for a
   2-point gain is a bad trade.
6. **Analyze**: drop assertions that always pass in both configs; fix ones that
   always fail; tighten instructions where results vary run-to-run; read
   transcripts of time/token outliers.
7. **Iterate**: feed failed assertions + human feedback + transcripts + current
   SKILL.md to an LLM; ask for generalized, lean fixes. Repeat until feedback is
   consistently empty or improvements plateau.

## Triggering optimization (description tuning)

When the problem is that the skill fires at the wrong times:

1. Write ~20 eval queries: 8-10 should-trigger (varied phrasing, explicitness,
   detail, complexity) and 8-10 should-NOT-trigger — near-misses sharing
   keywords, not obviously irrelevant prompts.
2. Split 60/40 into train/validation sets (mixed labels in both, fixed split).
3. **Execution gate:** Run trigger queries only when the user explicitly
   requests evaluation execution in the current conversation. Otherwise inspect
   the query set statically; do not run it.
4. **Run each query ~3 times with the skill installed; compute trigger rates;
   threshold 0.5.**
5. Revise the description against *train* failures only: broaden for missed
   triggers, add specificity/boundaries for false triggers. Never hard-code
   keywords from failed queries — address the general category. Watch the
   1024-char limit.
6. Stop after ~5 iterations or at plateau; select the iteration with the best
   *validation* pass rate (not the last one — later ones may overfit).
7. Sanity-check the final description with 5-10 fresh queries never used in
   optimization.
