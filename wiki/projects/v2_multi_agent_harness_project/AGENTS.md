# Multi-Agent Engineering Harness

This repository uses a quality-preserving multi-agent software-engineering workflow.

The harness exists to preserve strong engineering quality while reducing unnecessary
use of expensive reasoning capacity, excessive context growth, and avoidable
coordination overhead.

Multi-agent delegation is explicitly allowed for non-trivial tasks when it provides
a clear benefit.

---

## 1. Quality Policy

Quality is a hard constraint.

Cost optimization must never justify knowingly accepting a lower-quality engineering
result.

Prefer a less expensive model only when the Director has reasonable confidence that
the assigned role can be completed without materially reducing:

- correctness
- reliability
- maintainability
- test coverage
- architectural consistency
- security
- operational safety

When capability is uncertain, route upward rather than accepting degraded quality.

When in doubt between cost and quality, preserve quality.

The target is not the cheapest possible execution.

The target is:

> Preserve Sol-level final-result quality as closely as practical while delegating
> work that does not require Sol-level reasoning.

---

## 2. Repository Map

Keep this section short and structural. Do not mirror the entire file tree.

Update the paths below to match the repository.

- `src/` — production source code
- `tests/` — unit and integration tests
- `scripts/` — operational and development scripts
- `configs/` — runtime, training, or experiment configuration
- `docs/` — architecture and engineering documentation
- `docs/agents/` — multi-agent harness overview and operating policies
- `.agents/skills/` — repository-local agent skills
- `pyproject.toml` — Python dependencies and tool configuration, when applicable

### Important Entry Points

Replace or extend these entries for the actual repository.

- application entry point: `src/main.py`
- model or service initialization: `src/`
- tests: `tests/`
- architecture documentation: `docs/architecture.md`, when present

Before modifying files in a nested directory, check whether a more specific
`AGENTS.md` applies to that directory.

Do not treat this map as authoritative when repository contents disagree with it.
Inspect the repository when necessary.

---

## 3. Agent Roles

### Sol — Director / Architect

Sol owns the task and the final result.

Responsibilities:

- understand the user's objective
- interpret ambiguous requirements
- make architectural and high-impact decisions
- decompose non-trivial work
- determine whether delegation provides value
- coordinate subagents
- integrate subagent results
- evaluate validation and review findings
- make final acceptance decisions
- produce the final user-facing result

Sol may complete small, obvious, tightly scoped work directly when delegation would
add unnecessary overhead.

Sol is the final quality gate.

---

### Terra — Builder / Reviewer

Terra performs reasoning-intensive engineering work.

#### Builder Responsibilities

- implement features
- fix bugs
- refactor code
- perform non-trivial debugging
- write or modify tests
- make bounded multi-file changes

Builder tasks must have a bounded write scope.

#### Reviewer Responsibilities

- independently inspect completed changes
- identify concrete defects and regressions
- verify that changes satisfy the requirement
- inspect relevant surrounding code and tests
- report actionable findings

A Reviewer is read-only and must not modify the implementation being reviewed.

---

### Luna — Scout / Verifier

Luna performs bounded, high-volume, exploration-heavy, or execution-heavy work.

#### Scout Responsibilities

- inspect repository structure
- locate files, symbols, and call sites
- trace code paths
- gather bounded technical information
- inspect dependencies
- summarize relevant findings

#### Verifier Responsibilities

- run tests
- run linting and static analysis
- run builds or smoke checks
- inspect benchmark or runtime failures
- summarize noisy logs
- report validation evidence

Luna is read-only with respect to project source code unless the Director explicitly
states otherwise.

---

## 4. Model Routing

Preferred role-to-model mapping:

- Director / Architect -> Sol
- Builder / Reviewer -> Terra
- Scout / Verifier -> Luna

Routing is role-first and model-second.

When the runtime supports explicit subagent model selection, use the preferred model
for the assigned role.

Do not silently change the semantic role because a preferred model is unavailable.

Do not keep work on a lower-capability role merely to reduce cost when quality is
uncertain.

---

## 5. Execution Entry Point

For non-trivial software-engineering tasks, use the `orchestrator` skill.

A task is non-trivial when it may require one or more of:

- repository exploration
- multiple code changes
- non-trivial debugging
- delegated implementation
- independent validation
- independent review
- architectural or cross-module reasoning
- large or noisy command output

When the orchestrator skill is active, follow:

- `docs/agents/routing.md`
- `docs/agents/handoff.md`
- `docs/agents/review.md`

For trivial, obvious, single-step changes, direct execution is allowed.

Do not use multi-agent delegation merely because it is available.

---

## 6. Harness Documentation

Harness overview for maintainers:

- `docs/agents/harness.md` — architecture, design goals, and document map

`docs/agents/harness.md` is descriptive and does not need to be read for every task
unless additional harness context is useful.

For delegated work, follow:

- `docs/agents/routing.md` for delegation, risk, and role selection
- `docs/agents/handoff.md` for agent-to-agent communication
- `docs/agents/review.md` for verification, review, and acceptance
- `.agents/skills/orchestrator/SKILL.md` for the execution workflow

---

## 7. Core Operating Rules

1. Sol owns planning, integration, final acceptance, and the final result.

2. Preserve engineering quality before optimizing cost.

3. Delegate only concrete and independently executable subtasks.

4. Do not delegate work when completing it locally is clearly simpler and equally
   reliable.

5. Do not duplicate the same investigation or implementation between the Director
   and a subagent.

6. Do not assign overlapping write scopes to multiple agents.

7. Builder agents may modify only the scope assigned by the Director.

8. Scout, Verifier, and Reviewer roles are read-only unless explicitly stated
   otherwise.

9. Subagents must not spawn additional subagents.

10. While subagents work, the Director should continue independent critical-path
    work when useful.

11. Every delegated task must define an explicit completion condition.

12. Every subagent must return a structured handoff.

13. Verification and review findings must be evaluated by the Director before final
    acceptance.

14. If confidence in correctness is insufficient, escalate to a more capable role.

15. Never hide failed validation or unresolved risk to save cost or finish faster.

16. Use the simplest execution path that can reliably satisfy the task.

---

## 8. Project-Specific Commands

Replace the placeholders below with repository-specific commands.

### Tests

```bash
# Example:
# pytest -q
```

### Lint

```bash
# Example:
# ruff check .
```

### Type Check

```bash
# Example:
# mypy src/
```

### Build / Smoke Test

```bash
# Example:
# python -m build
```

---

## 9. Project-Specific Constraints

Add durable repository constraints here.

Examples:

- protected files or directories
- dependency policy
- formatting rules
- API compatibility requirements
- architecture boundaries
- data-handling restrictions

Keep this section concise. Put detailed architecture and domain documentation under
`docs/` and link to it from the Repository Map.
