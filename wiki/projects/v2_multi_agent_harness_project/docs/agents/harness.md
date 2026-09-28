# Multi-Agent Engineering Harness

This document describes the repository's quality-preserving Sol / Terra / Luna
multi-agent engineering harness.

It is an overview for maintainers. Operational instructions are defined in
`AGENTS.md`, the policy documents under `docs/agents/`, and the orchestrator skill.

---

## Purpose

The harness is designed to:

1. preserve strong final-result engineering quality
2. use Sol-level reasoning where it materially improves the result
3. delegate bounded implementation, exploration, review, and verification work
4. reduce unnecessary high-cost reasoning and context growth
5. keep responsibility boundaries explicit
6. escalate when a lower-capability role cannot establish sufficient confidence

Cost optimization is subordinate to the quality floor.

The target is not the cheapest possible execution.

The target is to preserve Sol-level final-result quality as closely as practical while
using Terra and Luna where their assigned roles can be completed reliably.

---

## Architecture

```text
                         User
                           |
                           v
                    Sol / Director
                           |
                   Plan / Decompose
                           |
             +-------------+-------------+
             |                           |
             v                           v
       Luna / Scout                Terra / Builder
     Explore / Inspect             Implement / Fix
             |                           |
             +-------------+-------------+
                           |
                           v
                    Implementation
                           |
             +-------------+-------------+
             |                           |
             v                           v
      Luna / Verifier              Terra / Reviewer
     Execute / Validate           Independent Review
             |                           |
             +-------------+-------------+
                           |
                           v
                    Sol / Director
                  Accept / Rework
                           |
                           v
                          User
```

Sol remains the final quality gate.

---

## Roles

| Role | Preferred model | Primary responsibility | Source writes |
|---|---|---|---|
| Director / Architect | Sol | planning, architecture, integration, acceptance | as needed |
| Builder | Terra | implementation, debugging, refactoring, tests | bounded write scope |
| Reviewer | Terra | independent defect-focused review | no |
| Scout | Luna | repository exploration and bounded investigation | no |
| Verifier | Luna | tests, lint, type checks, builds, log summarization | no |

Role selection comes before model selection.

A cheaper model must not be kept on a task when its capability or confidence is
insufficient.

---

## Execution Model

### 1. Direct path

Small, obvious, tightly scoped work may be completed directly by Sol when delegation
would add more overhead than value.

### 2. Delegated path

For non-trivial work:

1. Sol identifies the objective, constraints, scope, and risk.
2. Sol decides whether delegation provides a clear benefit.
3. Scout work goes to Luna when repository exploration can be isolated.
4. Bounded implementation work goes to Terra.
5. Completed changes are verified and, when appropriate, independently reviewed.
6. Sol evaluates the evidence and makes the final acceptance decision.
7. Work is escalated or reworked when confidence is insufficient.

---

## Quality Principle

Quality is a hard constraint.

A delegated implementation is held to the same acceptance standard that would apply
if Sol had implemented it directly.

The harness must not:

- accept known lower-quality work to reduce cost
- weaken validation because a cheaper model produced the change
- continue repeated cheap retries when capability is clearly insufficient
- hide failed validation or unresolved risk
- allow a read-only role to silently expand into an implementation role

When cost and quality conflict, preserve quality.

---

## Escalation Model

```text
Luna
  |
  | implementation, complex debugging,
  | insufficient confidence
  v
Terra
  |
  | architecture, security, public API,
  | high-impact decision
  v
Sol
```

Escalation is expected behavior when a task exceeds a role boundary.

It is not considered failure.

---

## Document Map

### `AGENTS.md`

Repository-level agent entry point.

Contains:

- quality policy
- repository map
- role definitions
- model mapping
- execution entry point
- core operating rules
- project-specific commands and constraints

### `docs/agents/routing.md`

Defines:

- direct execution versus delegation
- Scout / Builder / Architect / Verifier / Reviewer routing
- risk classification
- delegation triggers
- parallelism
- quality escalation

### `docs/agents/handoff.md`

Defines:

- delegation packet format
- bounded scope
- structured return format
- evidence and confidence reporting
- escalation handoff

### `docs/agents/review.md`

Defines:

- verification policy
- independent review policy
- severity levels
- risk-based acceptance
- rework
- quality floor

### `.agents/skills/orchestrator/SKILL.md`

Defines the executable orchestration workflow used for non-trivial software-engineering
tasks.

---

## Repository Integration

The project's normal root `README.md` remains the project introduction and should not
be replaced by this harness documentation.

Project-level layout:

```text
project/
├── README.md
├── AGENTS.md
├── docs/
│   └── agents/
│       ├── harness.md
│       ├── routing.md
│       ├── handoff.md
│       └── review.md
└── .agents/
    └── skills/
        └── orchestrator/
            └── SKILL.md
```

Before use in a real repository:

1. update the Repository Map in `AGENTS.md`
2. add the actual test, lint, type-check, build, and smoke-test commands
3. add durable project-specific constraints
4. add links to architecture documentation where relevant
5. verify that the configured Codex environment supports the intended multi-agent
   behavior and model routing

---

## Maintenance Rule

Keep `AGENTS.md` concise and operational.

Put detailed harness rationale here rather than expanding `AGENTS.md` indefinitely.

When the harness behavior changes, update the relevant policy document and keep this
overview synchronized with the actual execution model.
