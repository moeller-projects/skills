---
name: ste-clarity
description: >
  Rewrite, lint, or explain English text in ASD-STE100-inspired Simplified
  Technical English (STE) so it reads fast for humans and parses unambiguously
  for machines, translation pipelines, and non-native readers. Use when the
  user mentions STE, ASD-STE100, Simplified Technical English, "80% STE", or
  Karpathy-style explanations; asks to disambiguate, simplify, de-jargon, or
  controlled-language-rewrite a tool description, error message, system
  prompt, README, PR description, changelog, status report, or inter-agent
  instruction; or wants a plain-language lint of prose. Ships a deterministic
  linter (scripts/ste_lint.py) for the structural rules and optional diagram,
  interactive-HTML, and explainer-video output formats. Not for creative,
  marketing, or persuasive copy, and not a certified STE-compliance checker.
license: MIT
compatibility: Requires Python 3.8+ to run scripts/ste_lint.py (stdlib only). The rewriting guidance works without it.
metadata:
  title: STE Clarity
  version: "1.0.1"
  summary: Rewrite and lint technical English with ASD-STE100-inspired clarity rules.
  origin: Synthesized from danyuchn/asd-ste100-skill and prithivrajmu/asd-ste100 (both MIT)
---

# STE Clarity — Simplified Technical English rewriting and linting

ASD-STE100 is a controlled language the aerospace industry built so maintenance
instructions cannot be misread. It removes the two main sources of misreading:
words with more than one meaning and sentences with more than one possible
structure. This skill applies that discipline to everyday technical prose —
tool descriptions, error messages, prompts, READMEs, status reports — for
readers who cannot ask a follow-up question: a downstream agent, a translation
pipeline, or a person skimming under time pressure.

## Pick the level

| Level | When | What changes |
|---|---|---|
| **Standard** (default) | Explanations, READMEs, PR descriptions, changelogs, reviews, status reports | Enforce all structural rules. Treat lexical rules (fixed vocabulary) as advisory: prefer plain words and consistent terms, but allow reasonable range. |
| **Strict** | Procedures, error messages, tool/function descriptions, inter-agent instructions, safety text; or the user says "strict", "100%", "full STE" | Enforce everything, including hard length caps, one-word-one-meaning, no contractions, no Latin abbreviations. |

Infer the level from the text type when the user does not say. Do not announce
the level unless the user asks for the rule table.

## Core rules

### Structural — always enforce (both levels)

1. One idea per sentence. One instruction per sentence in procedures.
2. Length caps: aim ≤20 words; hard cap 25 words (Strict: 20 for procedures).
3. Active voice; name the actor. Passive only when the actor is genuinely
   unknown or irrelevant.
4. Simple tenses: present, past, future with "will". Keep a compound tense
   only when it carries information the simple form cannot ("the job has
   finished" — output ready now; "may have failed" — a hedge).
5. Use the verb, not a noun made from it: "analyze the log", not "perform an
   analysis of the log".
6. No phrasal verbs where a single verb exists: "start", not "spin up".
7. No semicolons anywhere (STE Rule 8.1). Split into two sentences.
8. Maximum 3 nouns in a row in a noun cluster.
9. Do not drop subjects, verbs, articles, or "that" to save space.
10. Numbered list for steps; list or table for 3+ items. One topic per
    paragraph, ≤6 sentences, main point first.

### Lexical — enforce in Strict, prefer in Standard

- One word for one thing: pick a term and reuse it; never rotate synonyms
  ("user"/"customer"/"client") within one document.
- Plain words over formal ones: "use", "start", "before", "because", "to" —
  not "utilize", "commence", "prior to", "in order to".
- Delete marketing adjectives that claim quality without measuring it:
  seamless, robust, powerful, cutting-edge, effortless. Keep the measurement
  that earns the claim, if the source gives one.
- Keep necessary technical terms (API, cache, container) and code names.
  Define a domain term once if it is not common English.

The official standard fixes its vocabulary with a ~900-word approved
dictionary that ASD does not permit to be redistributed, so it is not bundled
here. Apply the underlying principle (plainest common word, used the same way
every time) and never claim dictionary-verified compliance. For certified STE
documentation, request the standard free of charge from asd-ste100.org. Read
`references/rules-reference.md` when you need the full rule categories, the
tense and safety-text details, or source citations.

## Guard rails — these outrank the style rules

- **Keep every fact.** Never drop a number, condition, exception, or scope
  qualifier to make a sentence shorter. Write two sentences instead.
- **Keep the confidence of the source.** "May have failed" stays "may have
  failed". Upgrading a hedge to a fact changes the claim, and hedges are
  exactly what a length cap tempts you to cut. When the tense rule and this
  rule conflict, this rule wins.
- **Add no facts.** A rewrite that reads better because it supplies a cause,
  frequency, or mechanism has stopped being a rewrite.
- **Keep code unchanged.** Never rewrite code blocks, identifiers, commands,
  or quoted error text.
- **Stop when clear.** The goal is removing ambiguity, not the shortest text.
- **Compliant input stays untouched.** If the text already complies, say so.

## Process

1. Pick the level (Standard or Strict).
2. Read the whole input for meaning before rewriting anything.
3. Scan for the six mechanical habits that make prose hard to parse: synonym
   rotation, hedge stacking, nominalization, marketing adjectives, run-on
   sentences (semicolons, em dashes joining ideas), soft phrasal verbs.
4. Rewrite sentence by sentence, fixing violations while preserving meaning
   exactly. If a rewrite would drop needed precision, keep the longer phrasing
   and note it.
5. **Validate the rewrite with the linter** before delivering:

   ```bash
   echo "$REWRITTEN_TEXT" | python3 scripts/ste_lint.py
   ```

   Fix every advisory-free finding and re-run until clean (exit 0). Review
   advisory findings (passive voice, compound tenses) one by one: fix them
   unless a guard rail says to keep them. The linter checks structure only —
   it cannot verify that meaning survived, which is what step 4 is for. Use
   `--json` for structured output, `--baseline N` when adopting on existing
   docs, `--disable rule1,rule2` to silence named rules, `--selftest` to
   verify the script itself. To see what a finding looks like, run it on
   `examples/linter-fixture.md`, which violates rules on purpose.
6. Deliver the output (below).

## Output

**Default: the rewritten or explained text, and nothing else.** No preamble,
no level announcement, no violation count, no rule summary, no closing offer.
One permitted addition: a single `Kept as-is:` line naming any phrase you
deliberately left long, and the precision it preserves.

**On request ("show the diff", "which rules", "before/after"): the rule
table.**

```markdown
| Rule | Before | After |
|---|---|---|
| Active voice | "The file is deleted by the job." | "The job deletes the file." |

Level: Strict. 7 violations fixed.
```

Follow it with one line on anything deliberately not simplified, and why.

Worked before/after examples, including the modality cases that most often go
wrong, are in `examples/before-after.md`. Consult it when a rewrite feels
lossy and you are unsure whether the guard rails permit it.

## Beyond text: diagram, HTML, video

When the user asks for a diagram, an interactive HTML explainer, or a
3Blue1Brown-style explainer video — or when the subject has 3+ interacting
parts and a diagram would obviously beat prose — read
`references/output-formats.md` for the format rules. All text inside those
formats (labels, captions, narration) follows the same STE rules and guard
rails. Do not build HTML or video unless asked; offering it in one line is
allowed.

## Boundaries

- Not for creative, marketing, or persuasive copy — STE is deliberately flat
  and literal. Decline and say why.
- Not a certified STE checker: no official dictionary is bundled, so never
  claim aerospace-grade compliance.
- Never silently drop a safety condition, exception, or scope qualifier.
- STE fixes the form of a text, not its substance. If the input has nothing to
  say, say so instead of polishing it.
