---
name: setup-wizard
description: Generate an interactive bash wizard that walks a human through steps only they can perform — provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Use when a procedure blocks on human-only actions that are tedious to redo or re-explain. Do not use for steps the agent can perform itself (automate those directly instead) or for a short, fully documented procedure where a README checklist suffices.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Setup Wizard
  version: "1.0.2"
  summary: Turn human-only procedures into interactive bash wizards with captured values and confirmation gates.
  invocation: model
---

# Setup Wizard

## Purpose

Turn a manual procedure only a human can perform into an interactive bash script: it opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, CI secrets), confirms before irreversible actions, and shows progress through the stages. If the agent could do the step itself, it should — wizards are for genuine human-in-the-loop walls.


## Workflow

1. **Scope the procedure from the repo, not from questions.** Read `.env*`, `README`, compose files, framework config, and CI workflows — every `secrets.*` / `vars.*` reference is a value the wizard must produce. List every stage in order and, for each captured value: where the human gets it, where it gets written, and whether it is secret. Confirm this list with the user before writing code.
2. **Map each stage's journey** to concrete instructions a stranger could follow: which URL, what to click, where the value is shown, which variable it fills. Where the current UI or command is unknown, say so and ask or check the docs — never invent steps that may not exist.
3. **Author the script** with these mechanics:
   - One `stage` function per step, in dependency order; clear the screen per stage so only the current step is visible.
   - Before writing any file secret, require the target to be both untracked and git-ignored; approval cannot waive either condition. Create it with restrictive permissions (`umask 077`, then `chmod 600`) and never echo/log secret values. Refuse a tracked, unignored, or broadly readable target; select a safe secret store instead.
   - Hidden entry for secrets (`read -s`); idempotent upserts into `.env`; CI secret writes only for values CI actually references. Re-running must detect an existing matching value and skip or ask before replacement.
   - External provisioning/migration steps MUST be explicitly confirmed, detect already-completed state, and offer safe resume/skip; do not claim an action was executed unless the user reports its result.
   - A `confirm` gate before any irreversible action; a closing summary of what was captured and where it landed.
4. **Document platform prerequisites and fallback**: state required shell/browser/credential-manager support, provide a manual URL-copy fallback when `open` is unavailable, and never run the interactive wizard in tests.
5. **Verify statically, never end-to-end**: `bash -n`, `shellcheck` if available, `chmod +x`. Trace that every scoped value is captured and lands where step 1 said, and every secret name matches a CI `secrets.*` reference exactly. Do not run it — it opens browsers and blocks on human input.
6. **Hand off**: tell the user how to run it. Wizards are ephemeral by default — built for one run, deleted when done. Commit only when the user wants a repeatable setup path, and then link it from the README.

## Output Contract

```text
wizard:
  path: <absolute script path>
  stages: <count>
  values:
  - name: <variable or secret name>
    source: <where the human gets it>
    target: <.env key | CI secret | none>
    secret: true|false
verification: <bash -n / shellcheck result and the static trace outcome>
run: <exact command the user runs>
```

Every CI secret name in `values` MUST match a `secrets.*` reference found in the repo's workflows.

## Handoffs

- Hand off the procedure's irreversible production steps to `operations` for rollout review.
- Hand off values that need to come out of a running system (not a dashboard) to the agent itself — automate instead.

## Error Handling

1. If a stage's UI or command cannot be confirmed, mark it `VERIFY` in the script with instructions to check current docs — never write confident steps you invented.
2. If the procedure turns out to be agent-runnable after all, say so and stop building the wizard.

## Validation Checklist

- [ ] Every stage traces to concrete, confirmed instructions.
- [ ] The repo was read before the user was asked.
- [ ] Secrets use hidden entry and land in the right stores.
- [ ] Irreversible actions sit behind confirmation gates.
- [ ] The script passed static verification; it was never run end-to-end by the agent.
- [ ] Ephemeral by default; committed only on explicit request.
