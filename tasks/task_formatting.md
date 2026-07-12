# Task Formatting

Defines the standard format for task files in `tasks/open/` and `tasks/closed/`.

---

## Common Elements (All Tasks)

Every task file must include these sections in order:

### Header

```markdown
# [TASK-ID]: [Title]

**Created:** YYYY-MM-DD
**Status:** Open | In Progress | Closed
**Closed:** YYYY-MM-DD  <- only when closed
**Priority:** Low | Medium | High | Critical
**Category:** [Category name from task_management.md]
**Workstream:** [Lane from workstreams.md]
**Owner:** [person | agent | unassigned]
**Epic:** [umbrella task ID / milestone]  <- optional
```

### Coordination fields

Three header fields position a task on the **work-coordination** axes. They are lightweight
metadata; the file is the source of truth and they sync to Gitea (workstream → scoped label,
owner → assignee, epic → milestone) per [`gitea_handling.md`](./gitea_handling.md).

| Field | Question it answers | Cardinality | Allowed values |
|-------|---------------------|-------------|----------------|
| `**Workstream:**` | *Which gate governs when it ships?* | exactly 1 | A lane defined in [`workstreams.md`](./workstreams.md). |
| `**Owner:**` | *Who is accountable for moving it?* | exactly 1 | A person, `agent` (any autonomous agent), or `unassigned`. |
| `**Epic:**` | *Which larger work-product does it serve?* | 0 or 1 | An umbrella task ID (e.g. `FEAT-0075`) or a Gitea milestone name. Omit if none. |

`Workstream` and `Owner` are expected on new tasks. `Epic` is optional. Retrofit onto existing
tasks is **incremental** — tag a task the next time you touch it.

### The two axes — category vs workstream (never conflate)

A task is classified on **two independent dimensions**:

| Axis | Question | Where it lives |
|------|----------|----------------|
| **Category** (prefix `FEAT`/`BUG`/`INF`/`PLAN`/…) | *What kind of work is this?* | the task ID prefix ([`task_management.md`](./task_management.md)) |
| **Workstream** (lane) | *Which gate governs when it ships?* | the `**Workstream:**` field ([`workstreams.md`](./workstreams.md)) |

Same category can sit in different lanes, so a workstream is **not** a prefix. Rules:

1. **Single-valued.** Exactly one workstream per task — keeps the board scannable.
2. **Cross-lane influence = a dependency edge, not a second lane.** If lane A's work unlocks
   lane B, record it as a `## Dependencies` / `## Related` edge, not a second `Workstream`.
3. **A task that genuinely spans lanes is a decomposition smell** — usually an epic that should
   split into per-lane children.

### Decomposition (`FEAT-0042a`) vs epic membership (`Epic:`) — don't conflate

- **Hierarchical sub-task** (ID suffix, e.g. `FEAT-0042a`/`b`): decomposes **one deliverable**
  into children under a single **review gate** — the parent task. The orchestrator feeds every
  child's markdown to the parent as acceptance context.
- **`Epic:` field**: groups **independent tasks across categories** toward a larger outcome.
  Members are not sub-tasks of one parent and need no shared gate.

Rule of thumb: **suffix nesting = decomposition; `Epic:` field = work-product membership.**

### Required Sections

| Section | Description |
|---------|-------------|
| `## Summary` | Brief description of what the task is and why it exists. |
| `## Acceptance Criteria` | Bullet list of conditions that must be true for the task to be considered complete. The count of criteria items (`- [ ]` / `- [x]`) also feeds into orchestrator budget scaling -- tasks with >10 criteria receive additional budget per the [complexity criteria](./complexity_criteria.md) budget tiers. |

### Optional Sections (include when applicable)

| Section | When to Include |
|---------|-----------------|
| `## Dependencies` | Task is blocked by or related to other tasks. **Required for orchestrator scheduling.** |
| `## Background` | Task needs context beyond the summary. |
| `## Questions and Answers` | Q&A was needed during intake or implementation. |
| `## Implementation Notes` | Directives for how to execute (e.g., "use planning mode", "requires research"). |
| `## Work Completed` | When closing a task, document what was done. |
| `## Complexity Assessment` | Scored against the [complexity criteria](./complexity_criteria.md) rubric (scope, ambiguity, risk, integration, testing). Used by the orchestrator for model routing and budget allocation. |
| `## Related` | Links to planning docs, commits, PRs, other tasks. |

### Dependencies Format

The `## Dependencies` section must include a `Blocked By` table row for the dependency analyzer to parse. This is how the orchestrator determines execution order.

**With blockers:**
```markdown
## Dependencies

| Blocked By | SVC-0001, INF-0002 |
```

**No blockers:**
```markdown
## Dependencies

| Blocked By | None |
```

The analyzer matches: `| Blocked By | <comma-separated task IDs> |` or `| Dependencies | ... |` (legacy). Free-text dependency notes (library names, external services) can follow below the table row.

---

## Category-Specific Sections

Additional sections required or recommended based on the task category.

| Prefix | Section | Required | Description |
|--------|---------|----------|-------------|
| FEAT | `## User Story` | Required | "As a [user], I want [goal] so that [reason]." |
| FEAT | `## UI/UX Considerations` | Optional | Mockups, layout notes, or user flow. |
| ISSUE | `## Steps to Reproduce` | Required | Numbered steps to trigger the issue. |
| ISSUE | `## Expected vs Actual Behavior` | Required | What should happen vs what does happen. |
| ISSUE | `## Root Cause` | Optional | Analysis of why the issue occurs (fill in during or after fix). |
| INF | `## Affected Services` | Required | Which services/containers are impacted. |
| INF | `## Rollback Plan` | Optional | How to revert if something goes wrong. |
| SVC | `## API Endpoints` | Optional | New or modified endpoints (method, path, description). |
| WRK | `## Trigger / Schedule` | Required | What triggers the worker (event, cron, manual). |
| WRK | `## Input / Output` | Optional | What data the worker consumes and produces. |
| MON | `## Metrics / Alerts` | Required | What is being measured or alerted on. |
| MON | `## Dashboards` | Optional | Grafana/monitoring dashboard references. |
| FE | `## Affected Components` | Required | Which UI components are impacted. |
| FE | `## UI Mockups` | Optional | Screenshots, ASCII mockups, or design links. |
| TST | `## Test Scope` | Required | What is being tested and boundaries. |
| TST | `## Test Cases` | Optional | Specific test cases as a checklist. |
| DOC | `## Target Audience` | Optional | Who the documentation is for. |
| DOC | `## Files to Update` | Required | List of files to create or modify. |
| INIT | `## Prerequisites` | Required | What must exist before this task can start. |
| INIT | `## Setup Steps` | Optional | Ordered steps to complete the initialization. |
| GTSK | -- | -- | No additional required sections. |

---

## Version Tracking

Every task file must include a version comment as the **very last line** of the file:

```markdown
<!-- version: v2026.02.28.02 -->
```

Format: `<!-- version: vYYYY.MM.DD.## -->` where `##` is a zero-padded sequence number starting at `01`. Increment the sequence number each time the file is updated on the same date.

---

## Template

```markdown
# [TASK-ID]: [Title]

**Created:** YYYY-MM-DD
**Status:** Open
**Priority:** Medium
**Category:** [Category]
**Workstream:** [Lane from workstreams.md]
**Owner:** unassigned
**Epic:** [umbrella ID / milestone, or omit]

---

## Summary

[What and why.]

## [Category-specific required sections]

[...]

## Dependencies

| Blocked By | None |

## Acceptance Criteria

- [ ] [Condition 1]
- [ ] [Condition 2]

## Questions and Answers

[If applicable.]

## Implementation Notes

[If applicable -- e.g., "Use planning mode before implementing."]

## Related

- [Links to other tasks, planning docs, commits.]

<!-- version: vYYYY.MM.DD.01 -->
```
