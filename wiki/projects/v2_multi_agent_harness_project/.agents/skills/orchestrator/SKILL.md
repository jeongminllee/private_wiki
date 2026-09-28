---
name: orchestrator
description: Coordinate non-trivial software-engineering work using Sol as Director, Terra as Builder or Reviewer, and Luna as Scout or Verifier while preserving final-result quality. Use when work benefits from repository exploration, delegated implementation, independent review, noisy validation, or parallel non-overlapping tasks. Do not use for trivial single-step edits where delegation adds unnecessary overhead.
---

# Multi-Agent Orchestrator

Coordinate software-engineering work according to the repository's quality-preserving
multi-agent policy.

Read and follow:

- `AGENTS.md`
- `docs/agents/routing.md`
- `docs/agents/handoff.md`
- `docs/agents/review.md`

The Director owns the complete task and final result.

Quality is a hard constraint.

Cost and context efficiency may be optimized only when doing so does not materially
reduce correctness, reliability, maintainability, architectural consistency, security,
or validation confidence.

---

# 1. Understand the Objective

Before delegating:

1. identify the user's actual objective
2. identify important constraints
3. inspect the Repository Map in `AGENTS.md`
4. identify the likely repository scope
5. check whether more specific nested `AGENTS.md` instructions apply
6. determine whether an architectural or high-impact decision is required
7. determine whether delegation provides a clear benefit
8. determine the quality and risk level required for acceptance

Do not delegate merely because subagents are available.

For small, obvious, tightly scoped tasks, complete the work locally.

---

# 2. Acquire Only the Required Repository Context

Use the repository structure and project documentation to orient the task.

Do not assume the Repository Map is complete or perfectly current.

Inspect the actual repository when necessary.

Before modifying a nested area:

- check applicable `AGENTS.md`
- inspect relevant source
- inspect relevant tests
- inspect linked architecture documentation when the task depends on it

Avoid loading unrelated repository context.

---

# 3. Classify the Work

Classify each useful work unit as one of:

- DIRECT
- ARCHITECT
- SCOUT
- BUILDER
- VERIFIER
- REVIEWER

Use `docs/agents/routing.md`.

Choose the semantic role before choosing the model.

---

# 4. Create Bounded Work Units

Before spawning a subagent, create a delegation packet containing:

TASK
ROLE
OBJECTIVE
SCOPE
WRITE SCOPE
CONTEXT
CONSTRAINTS
DONE WHEN
RETURN

Every delegated task must be independently executable.

Do not delegate vague goals such as:

> Improve the project.

Prefer bounded goals such as:

> Identify every call site of `load_model()` under `src/` and return the call flow
> without modifying files.

---

# 5. Select the Agent

Preferred model mapping:

- Builder -> Terra
- Reviewer -> Terra
- Scout -> Luna
- Verifier -> Luna

Sol remains Director and Architect.

When spawning an agent, explicitly select the preferred model when the runtime
supports model override.

Do not keep a task on a lower-capability model merely because it is cheaper.

If capability is uncertain, preserve quality and escalate.

If explicit model override is unavailable, preserve the assigned role and apply the
same quality rules rather than silently weakening acceptance criteria.

Do not spawn subagents from subagents.

---

# 6. Minimize Context Transfer

Give each subagent only the information required for its bounded task.

Prefer:

- requirement
- relevant repository scope
- applicable constraints
- necessary architecture context
- completion condition
- useful prior findings

Avoid sending unnecessary conversation history.

For independent review, avoid passing the Builder's internal rationale unless the
Reviewer specifically requires clarification.

The goal is context efficiency without information starvation.

---

# 7. Execute Independent Work

While a subagent works, continue useful work that does not duplicate the delegated
task.

Example:

Scout:
- repository investigation

Director:
- requirement analysis
- architecture planning

may proceed in parallel.

Do not perform the same investigation independently after delegating it.

---

# 8. Protect Write Scope

Only Builder roles may modify source code by default.

Never assign overlapping write scopes to concurrent agents.

Scout:
read-only

Verifier:
read-only

Reviewer:
read-only

If another role discovers that code changes are required, return BLOCKED or request
escalation instead of modifying the code.

---

# 9. Collect Structured Handoffs

Require the return formats defined in:

`docs/agents/handoff.md`

Do not ask agents to return long private reasoning transcripts.

Prefer:

- result
- changed files
- evidence
- validation
- findings
- risk
- confidence
- escalation

Summarize noisy output before adding it to Director context.

Treat LOW confidence as a signal that more evidence or escalation may be required.

---

# 10. Verify the Implementation

After code-changing work, determine the risk level using
`docs/agents/routing.md`.

LOW:
run Verifier when meaningful.

MEDIUM:
run Verifier and Reviewer.

HIGH:
run Verifier and Reviewer, then perform explicit Sol acceptance.

Verifier and Reviewer may run concurrently after implementation because both are
read-only.

Use validation strong enough for the risk level.

Do not reduce validation merely to save cost.

---

# 11. Apply the Quality Gate

Before accepting delegated work, evaluate:

- correctness
- requirement satisfaction
- architectural consistency
- test and validation evidence
- reviewer findings
- remaining uncertainty
- confidence level
- security and operational implications when relevant

A cheaper execution path must satisfy the same acceptance criteria that would apply to
a Sol-only implementation.

If sufficient confidence cannot be established:

> escalate, rework, or gather more evidence.

Never accept degraded quality because the delegated path was cheaper.

---

# 12. Handle Failure and Escalation

A subagent may return:

DONE
BLOCKED
FAILED

Reviewer may return:

PASS
CHANGES_REQUESTED
BLOCKED

Do not treat BLOCKED as agent failure.

Evaluate the reason.

Examples:

Luna -> Terra:
implementation or complex debugging required

Terra -> Sol:
architecture or high-impact decision required

Reviewer -> Sol:
trade-off or requirement ambiguity requires decision

Verifier -> Sol:
implementation failed validation

Low confidence -> more capable role or more evidence

The Director decides the next action.

Do not automatically retry indefinitely.

Do not repeatedly use a cheaper model when repeated failure indicates insufficient
capability.

---

# 13. Rework

When rework is required:

1. inspect the finding
2. determine whether the original implementation scope is still valid
3. determine whether the previous role/model remains appropriate
4. create a new bounded Builder task
5. perform the change
6. verify the new implementation
7. review again when required by risk

Reviewer and Verifier do not fix their own findings.

Repeated failure should trigger capability escalation rather than cheap retry loops.

---

# 14. Final Acceptance

Before marking the task complete, confirm:

- the objective was satisfied
- constraints were preserved
- delegated work was integrated
- relevant verification passed
- required review completed
- unresolved risk is understood
- confidence is appropriate for the risk level
- the final engineering quality would still be acceptable if cost were ignored

Sol owns the final acceptance decision and user-facing response.

---

# 15. Agent Lifecycle

Use subagents only while they have useful work.

When an agent has completed its assigned task and its structured handoff has been
collected, close the agent and release the slot.

Do not leave completed subagents active unnecessarily.
