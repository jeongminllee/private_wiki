# Review and Verification Policy

Implementation completion and task acceptance are separate events.

A Builder completing its assigned task does not mean the change is accepted.

The Director owns final acceptance.

The purpose of review and verification is to preserve final-result quality even when
implementation and exploration are delegated to less expensive models.

---

# Verification

Verification is execution-based validation.

Default role:

> Luna / Verifier

The Verifier should run the smallest set of commands that provides meaningful
confidence in the change.

Examples:

- targeted unit tests
- relevant integration tests
- lint
- type checking
- build
- smoke test
- focused benchmark or runtime check

Run broader validation when the risk level, repository conventions, or observed
failures require it.

---

## Verifier Responsibilities

The Verifier must:

1. use the actual implementation produced
2. run the relevant commands
3. report the exact commands used
4. report pass or failure
5. summarize failures
6. avoid modifying source code
7. avoid fixing discovered problems
8. avoid spawning subagents
9. report uncertainty honestly
10. escalate when validation cannot establish sufficient confidence

Large logs should be summarized.

Example:

STATUS:
FAILED

SUMMARY:
Authentication tests failed.

CHANGES:
none

EVIDENCE:
Two refresh-token tests fail consistently.

VALIDATION:
`pytest tests/auth -q`

RESULT:
143 passed, 2 failed

RISKS:
Refresh-token behavior is not currently safe to accept.

CONFIDENCE:
HIGH

ESCALATION:
Implementation requires rework.

---

# Independent Review

Independent review is reasoning-based validation.

Default role:

> Terra / Reviewer

The Reviewer should receive:

- original requirement
- relevant constraints
- completed diff
- relevant validation results
- only the project context required to evaluate the change

Avoid providing unnecessary Builder rationale before review.

The goal is an independent assessment, not confirmation of the Builder's reasoning.

---

## Reviewer Responsibilities

The Reviewer must:

1. read the applicable `AGENTS.md` instructions
2. inspect the complete relevant diff
3. inspect enough surrounding code to understand the change
4. inspect relevant call sites
5. inspect relevant tests
6. identify concrete regressions or defects
7. continue reviewing after finding the first issue
8. report actionable findings
9. remain read-only
10. avoid spawning subagents
11. distinguish concrete issues from speculative preferences
12. escalate when architectural or product judgment is required

Do not report stylistic preferences unless they violate repository rules or create a
concrete engineering problem.

The official goal is defect discovery, not commentary volume.

---

# Finding Severity

## BLOCKER

The change must not be accepted.

Examples:

- security vulnerability
- data loss
- build failure
- severe correctness failure
- destructive unintended behavior
- violation of a critical project constraint

## MAJOR

The implementation is likely incorrect or introduces a meaningful regression.

Examples:

- broken edge case
- incorrect state handling
- compatibility regression
- missing required behavior
- invalid cross-module assumption

## MINOR

A concrete issue exists but does not invalidate the core implementation.

Examples:

- incomplete error handling
- meaningful maintainability defect
- missing test for an important boundary

Pure stylistic preference is not a finding.

---

# Acceptance Policy

## LOW Risk

Required:

- implementation complete
- relevant verification passes when meaningful
- no known unresolved correctness issue

Reviewer:

- optional

Sol may accept after successful verification and its own final quality check.

---

## MEDIUM Risk

Required:

- implementation complete
- Verifier passes
- Reviewer has no BLOCKER or MAJOR findings
- Sol evaluates remaining MINOR findings and residual risk

---

## HIGH Risk

Required:

- implementation complete
- Verifier passes
- Reviewer has no unresolved BLOCKER or MAJOR findings
- Sol explicitly evaluates architecture, constraints, and remaining risk
- confidence is sufficient for the impact of the change

High-risk changes are never accepted solely because tests pass.

---

# Quality Floor

Final acceptance must not be relaxed merely because a cheaper model performed the
work.

A delegated implementation should be held to the same acceptance criteria that would
apply if Sol had implemented it directly.

If Reviewer, Verifier, or Sol cannot establish adequate confidence:

> escalate, rework, or gather more evidence.

Do not accept lower engineering quality as a cost-saving measure.

---

# Rework

When verification or review fails:

1. return findings to Sol
2. Sol determines whether rework is appropriate
3. Sol determines whether the previous role/model remains appropriate
4. Sol creates a new bounded Builder task if needed
5. the changed implementation is verified again
6. review again when required by risk

Do not create automatic retry loops.

Do not let Reviewer or Verifier modify the implementation themselves.

If repeated rework suggests that the assigned capability is insufficient, escalate
rather than continuing cheap retries.

---

# Final Acceptance

Before final acceptance, Sol should be able to answer:

- Did the implementation satisfy the original objective?
- Were the relevant constraints preserved?
- Was the change actually validated?
- Was the validation sufficient for the risk level?
- Are review findings resolved or consciously accepted?
- Is remaining risk understood?
- Would this result be acceptable if cost were not a consideration?

Only then is the task DONE.
