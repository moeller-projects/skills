# Happy-Path Example — Code Quality Engine

## Scenario

A PR mixes a null-pointer bug fix with broad variable renaming across 15 files.

## Input

- `userService.ts:42` — `user.profile.name` accessed without null check; crashes when profile is absent.
- PR also renames `userId` → `userID` in 15 files unrelated to the bug.

## Expected Output

```text
findings:
- [critical] userService.ts:42 — null dereference on user.profile.name
  why: profile can be absent for OAuth users; causes uncaught TypeError in prod
  fix: guard with `user.profile?.name ?? ''` before access

- [low] 15 files — rename userId → userID
  why: style preference, no behavioral impact
  fix: defer to a separate cleanup PR

patch-plan:
1. userService.ts:42 — apply null guard (critical, isolated change)
2. Defer rename — separate PR, zero risk, zero urgency

risk:
- None after patch; the guard uses existing optional-chaining support in the codebase
```

## Why This Is Correct

- Critical bug surfaces first.
- Style cleanup is identified but deferred to keep the patch minimal.
- Patch plan is ordered safest-first.
- Risk is stated explicitly as none after the fix.
