# Task Management

**Related:**
- [Task Formatting](./task_formatting.md) -- Standard format and category-specific sections
- [Instruction Handling](./instruction_handling.md) -- How tasks are created from INSTRUCTIONS.md
- [Complexity Criteria](./complexity_criteria.md) -- 5-dimension scoring rubric for task complexity

## Task ID Prefixes

| Prefix | Category | Example Use |
|--------|----------|-------------|
| FEAT | Feature | Software Engineering, Feature Requests, Features |
| ISSUE | Issue | Debugging, Error Resolution, Code Fixes |
| BUG | Issue (alias) | Defect/fix tasks. Shares the `category:issue` label with `ISSUE`; both are recognized. Prefer `BUG` for new defect tasks. |
| INF | Infrastructure | Docker, databases, messaging |
| SVC | Services | Backend APIs and applications |
| WRK | Workers | Background processing workers |
| MON | Monitoring | Prometheus, Grafana, observability |
| FE | Front-End | User interface components |
| TST | Testing | Test framework and integration tests |
| DOC | Documentation | Documentation tasks |
| INIT | Initialization | Project setup tasks |
| PLAN | Planning spike | A task whose deliverable is **decisions + a decomposition**, not a build (e.g. a strategy/architecture spike that spawns execution tasks). Closes when the decisions are ratified and the child tasks exist. |
| DEPLOY | Release / deployment | The work of shipping a release to an environment. A `DEPLOY` task owns one `dev→main` PR and its traceability manifest (see the deploy playbook). |
| GTSK | General Task | All other tasks |

> **Category vs workstream.** The prefix above answers *"what kind of work is this?"* (exactly
> one per task). It is **orthogonal** to the **workstream** — the *lane/gate* that answers
> *"which gate governs when this ships?"* (also exactly one per task, carried in the
> `**Workstream:**` header field). See [`workstreams.md`](./workstreams.md) and
> [Task Formatting](./task_formatting.md) for the two-axes model. Don't encode a lane as a prefix.

## Dependencies

Every task file must include a `## Dependencies` section with a `| Blocked By |` table row. This is parsed by the dependency analyzer and orchestrator to determine execution order.

```
| Blocked By | SVC-0001, INF-0002 |
```

Use `| Blocked By | None |` when there are no blockers. When creating a new task, review existing open tasks in `tasks/open/` to identify any that must complete first.

## Task Lifecycle

```
tasks/open/[TASK-ID].md  ->  Work in Progress  ->  tasks/closed/[TASK-ID].md
```

## Key Task Files

| File | Purpose |
|------|---------|
| `tasks/task_list.md` | Master index of all tasks (open and closed) |

## Key Task Directories
| Directory| Purpose |
|------|---------|
| `tasks/open/` | Individual open task files |
| `tasks/closed/` | Completed task archive |
