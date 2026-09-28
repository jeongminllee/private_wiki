# Agent Handoff Protocol

All delegated work must use a bounded task specification and structured return
format.

The handoff protocol exists to:

- reduce ambiguity
- prevent duplicate work
- protect write scope
- minimize unnecessary context transfer
- make validation and escalation explicit
- preserve enough evidence for Sol to make a final quality decision

---

# Delegation Packet

Every delegated task should contain the following fields.

## TASK

A short description of the concrete work to perform.

## ROLE

One of:

- Builder
- Scout
- Reviewer
- Verifier

## OBJECTIVE

Describe the intended outcome.

Focus on what must be achieved rather than prescribing unnecessary implementation
details.

## SCOPE

Define the repository area relevant to the task.

Examples:

- `src/auth/`
- `src/model_loader.py`
- `tests/inference/`

## WRITE SCOPE

For Builder tasks, explicitly state which files or directories may be modified.

For read-only roles:

> WRITE SCOPE: none

## CONTEXT

Include only information needed to execute the task correctly.

Prefer:

- relevant requirement
- relevant architecture constraint
- known file or symbol references
- important prior findings

Avoid unnecessary conversation history.

## CONSTRAINTS

List important restrictions.

Examples:

- do not change the public API
- do not modify database schemas
- do not add dependencies
- do not edit files outside the assigned write scope
- do not spawn subagents
- preserve existing behavior outside the stated objective

## DONE WHEN

Define observable completion conditions.

Examples:

- the requested implementation exists
- the regression test passes
- all relevant call sites are identified
- the requested validation command completes
- all actionable review findings are reported

## RETURN

Specify task-specific information that must be included in the handoff.

---

# Example — Scout

TASK:
Locate model initialization logic.

ROLE:
Scout

OBJECTIVE:
Identify every path responsible for loading the inference model.

SCOPE:
src/

WRITE SCOPE:
none

CONTEXT:
The application appears to initialize inference during startup.

CONSTRAINTS:
Do not modify files.
Do not spawn subagents.

DONE WHEN:
All relevant files, symbols, and call relationships have been identified.

RETURN:
Relevant files, functions, call flow, and any suspicious duplicate loading paths.

---

# Example — Builder

TASK:
Fix incorrect inference device assignment.

ROLE:
Builder

OBJECTIVE:
Ensure the model is moved to the configured device before inference.

SCOPE:
src/model_loader.py
tests/

WRITE SCOPE:
src/model_loader.py
tests/test_model_loader.py

CONTEXT:
Scout identified `load_model()` as the shared initialization path.

CONSTRAINTS:
Do not change the public API.
Do not add dependencies.
Do not modify files outside WRITE SCOPE.
Do not spawn subagents.

DONE WHEN:
The regression test and existing model-loader tests pass.

RETURN:
Modified files, implementation summary, validation performed, remaining risks, and
anything requiring Sol judgment.

---

# Standard Return Format

Every Scout, Builder, and Verifier returns:

STATUS:
DONE | BLOCKED | FAILED

SUMMARY:
A concise description of the result.

CHANGES:
Files changed and what changed.
Use `none` for read-only work.

EVIDENCE:
Relevant files, symbols, outputs, or observations supporting the result.

VALIDATION:
Commands or other evidence used to validate the result.

RISKS:
Known uncertainty, remaining risk, or `none`.

CONFIDENCE:
HIGH | MEDIUM | LOW

ESCALATION:
Decision or additional work required from another role, or `none`.

---

# Reviewer Return Format

Reviewer uses:

STATUS:
PASS | CHANGES_REQUESTED | BLOCKED

SUMMARY:
Overall review result.

FINDINGS:
Actionable findings ordered by severity.

EVIDENCE:
Relevant files, symbols, tests, or call sites supporting the findings.

VALIDATION:
Code, tests, call sites, or commands inspected.

RISKS:
Remaining uncertainty or unverified areas.

CONFIDENCE:
HIGH | MEDIUM | LOW

ESCALATION:
Decision required from Sol, or `none`.

---

# Confidence Guidance

## HIGH

Use when:

- the relevant scope was inspected adequately
- evidence is direct
- validation supports the conclusion
- no material unknowns remain

## MEDIUM

Use when:

- the main conclusion is supported
- some non-critical uncertainty remains
- validation is partial but meaningful

## LOW

Use when:

- important context is missing
- evidence is indirect
- validation is insufficient
- multiple materially different interpretations remain

LOW confidence should usually trigger escalation rather than silent acceptance.

---

# Handoff Rules

1. Return conclusions and evidence, not private reasoning transcripts.

2. Do not return large logs unless explicitly requested.

3. Summarize noisy command output.

4. Include file and symbol references whenever possible.

5. Distinguish facts from uncertainty.

6. A BLOCKED result must clearly explain what decision or information is required.

7. Do not expand the task scope without Director approval.

8. Do not hide failed validation.

9. Do not claim validation that was not actually executed.

10. Do not overstate confidence to avoid escalation.

11. Keep handoffs concise enough for the Director to integrate without reconstructing
    the entire subagent session.

12. If source code was changed outside WRITE SCOPE, report it explicitly as a process
    violation.

13. If a lower-capability role cannot establish sufficient confidence, escalate rather
    than guessing.
