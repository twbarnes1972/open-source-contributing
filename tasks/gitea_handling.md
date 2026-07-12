# Gitea Issue Handling

Defines the **tasks ↔ Gitea-Issues** bidirectional routine — parallel to
[`instruction_handling.md`](instruction_handling.md) (human → agent intake) and
[`escalation_handling.md`](escalation_handling.md) (agent → human).

**Files-first.** The `tasks/` files are the source of truth / the agent's working layer; Gitea
Issues are the **team-facing** tracker. Gitea-origin issues enter through the triage gate below
rather than crowding `INSTRUCTIONS.md`.

> **Scaffold stub.** The routine below is the convention; the concrete API wiring (which
> `gitea` CLI / `gitea-tracker` calls run at each boundary) is filled in per project. Until the
> sync is wired, run the triage steps manually at session boundaries.

## Triage-in (session start)

1. Pull inbound Gitea Issues for this repo (open, not yet linked to a task file).
2. For each: decide **track** or **decline**.
   - **Track** → create a `tasks/open/<PREFIX>-NNNN.md` file (per
     [`task_formatting.md`](task_formatting.md)), set its `**Workstream:**` / `**Owner:**` /
     `**Epic:**` fields, and label the Gitea issue `tracked` + the matching `workstream/*` label.
   - **Decline** → comment the reason on the issue and close, or label `needs-triage` if it
     needs the operator.
3. New, uncategorized issues carry `needs-triage` until step 2 dispositions them.

## Sync-out (session end)

1. Walk the session's task changes.
2. **Create** missing Gitea Issues for tasks that should be team-visible; link issue ↔ task ID.
3. **Update** existing issues: status, assignee (from `**Owner:**`), `workstream/*` label (from
   `**Workstream:**`, scoped-exclusive), milestone (from `**Epic:**`), and links to PRs.
4. Close Gitea Issues whose task files moved to `tasks/closed/`.

## Field → Gitea mapping

| Task field | Gitea representation |
|------------|----------------------|
| `**Workstream:**` | scoped-exclusive label `workstream/<lane>` |
| `**Owner:**` | issue assignee (`agent`/`unassigned` → no assignee) |
| `**Epic:**` | milestone |
| Category prefix | `category:*` label |

This routine is **agent-automatable** (anti-chore): the agent runs it at session boundaries via
the Gitea REST API, not as a manual owner ritual. See [`workstreams.md`](workstreams.md) for the
lane definitions and the label scope.

<!-- version: v2026.06.11.01 -->
