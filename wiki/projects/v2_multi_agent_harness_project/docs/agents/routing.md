# Agent Routing Policy

This document defines how the Director decides whether to work locally or delegate a
subtask.

Routing is role-first and model-second.

Quality is a hard constraint. Cost optimization is allowed only inside a role boundary
where the Director has sufficient confidence that quality will not materially degrade.

---

## 1. Direct Execution

The Director should complete work locally when delegation would add more coordination
overhead than value.

Prefer direct execution when most of the following are true:

- the required change is small and obvious
- the relevant file or symbol is already known
- repository exploration is unnecessary
- the change has a narrow scope
- there is no useful parallel work
- validation output is expected to be small
- independent review would provide little additional value
- Sol-level reasoning is already required and delegation would duplicate work

Example:

> Rename one local variable in an already identified function.

Do not create a subagent merely because delegation is available.

---

## 2. Scout Routing

Route work to Luna as Scout when the task is primarily:

- repository exploration
- file or symbol discovery
- call-site discovery
- dependency inspection
- code-path tracing
- bounded technical investigation
- information gathering
- log inspection

Typical verbs:

- find
- locate
- inspect
- search
- trace
- identify
- summarize

Scout tasks should normally be read-only.

Example:

> Locate every path that loads the inference model and return the files, functions,
> and call relationships.

---

## 3. Builder Routing

Route work to Terra as Builder when the task primarily requires:

- feature implementation
- bug fixing
- refactoring
- test implementation
- non-trivial debugging
- behavior changes
- bounded multi-file code changes

Typical verbs:

- implement
- fix
- modify
- refactor
- debug
- add
- migrate

Builder tasks must have a bounded write scope.

Example:

> Fix device assignment in `src/model_loader.py` without changing the public API.

---

## 4. Architect Routing

Keep work with Sol when it requires:

- architectural decisions
- ambiguous requirement interpretation
- cross-module design
- security-sensitive decisions
- public API design
- major dependency decisions
- compatibility trade-offs
- irreversible or high-impact changes
- reasoning whose failure would materially affect system quality

Architectural decisions may be informed by Scout, Builder, Reviewer, or Verifier
findings, but the decision remains owned by Sol.

---

## 5. Verifier Routing

Use Luna as Verifier when completed work needs execution-based validation.

Typical tasks:

- run unit tests
- run integration tests
- run lint
- run type checks
- run builds
- run smoke tests
- inspect benchmark failures
- summarize large test output

Verifier tasks are read-only with respect to source code.

The Verifier reports failures but does not fix them.

---

## 6. Reviewer Routing

Use Terra as Reviewer when independent reasoning about a completed change is
valuable.

Review is recommended when:

- several files changed
- behavior changed materially
- implementation logic is non-trivial
- regression risk exists
- the task crosses module boundaries
- the Director wants an independent second opinion
- tests alone cannot establish sufficient confidence

The Reviewer is read-only.

The Reviewer should evaluate the implementation independently rather than merely
validate the Builder's rationale.

---

# Risk Classification

The Director classifies code-changing work as LOW, MEDIUM, or HIGH risk.

## LOW

Examples:

- localized implementation
- isolated bug fix
- simple internal refactor
- test-only changes
- small non-public behavior changes

Default validation:

> Verifier when meaningful.

Independent review is optional.

---

## MEDIUM

Examples:

- multi-file behavior change
- shared utility modification
- complex state handling
- substantial refactoring
- non-trivial inference or data-processing logic
- changes where local correctness is not enough to establish system correctness

Default validation:

> Verifier + Reviewer

---

## HIGH

Examples:

- authentication or authorization
- security-sensitive logic
- persistence or data migration
- concurrency
- deployment-critical configuration
- public API breaking changes
- destructive operations
- major architecture changes

Default validation:

> Verifier + Reviewer + explicit Sol acceptance

High-risk architectural decisions remain with Sol.

---

# Delegation Trigger

Delegation is useful when one or more of the following conditions apply:

1. repository exploration can be isolated
2. implementation can be independently scoped
3. useful work can run in parallel
4. validation will generate large or noisy output
5. an independent review materially reduces risk
6. the task spans multiple concerns that can be separated cleanly
7. delegating a bounded lower-reasoning task preserves quality while reducing
   expensive context or reasoning usage

Delegation is not useful when coordination overhead exceeds the expected benefit or
when delegation would materially reduce confidence in the result.

---

# Quality Escalation Rule

Never continue with a lower-capability role merely to reduce cost.

Escalate when:

- confidence in correctness is low
- the task exceeds the assigned role's reasoning boundary
- multiple materially different solutions require judgment
- architectural context is required
- security or reliability implications are unclear
- validation cannot establish sufficient confidence
- the assigned role lacks enough context to make a safe decision
- the result would otherwise be accepted mainly because it is cheaper

When in doubt between cost and quality, preserve quality.

Escalation is a quality-preservation mechanism, not an execution failure.

---

# Parallelism

Default maximum parallel subagents:

- one Builder
- one Scout

Additional agents should be used only when work scopes are clearly independent.

Never assign overlapping write scopes.

Reviewer and Verifier may run in parallel after implementation is complete because
both roles are read-only.

Parallelism should reduce wall-clock or context burden without creating coordination
risk.

---

# Escalation

Agents must stop and escalate instead of making decisions outside their role.

## Luna -> Terra or Sol

Escalate when:

- implementation is required
- several valid fixes exist
- the root cause requires complex debugging
- the requested task cannot be completed read-only
- confidence in a technical conclusion is insufficient

## Terra -> Sol

Escalate when:

- architecture must change
- requirements conflict
- a public API decision is required
- a security trade-off is required
- the assigned write scope is insufficient
- a major dependency change is necessary
- implementation requires a high-impact product or engineering decision

Escalation is not failure.

It is correct behavior when the task exceeds the assigned role boundary.

---

# Routing Priority

Use this conceptual order:

1. Determine whether Sol-level judgment is required.
2. If not, determine whether direct execution is simpler and equally reliable.
3. If delegation is useful, choose the role that matches the work.
4. Use the preferred model for that role.
5. Escalate immediately when confidence or capability becomes insufficient.
6. Verify and review according to risk before acceptance.

Do not optimize model cost before identifying the correct role and quality
requirements.
