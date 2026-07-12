# Discussion Handling Convention

How upstream engagements are registered, checked, and concluded — the lifecycle for
[DISCUSSIONS.md](../DISCUSSIONS.md). Parallel to
[escalation_handling.md](./escalation_handling.md) (which governs the ESCALATIONS queue) and
modeled on its queue-not-log pattern.

---

## The core principle

**A discussion is a monitored entity, not a second kind of task.** The work side of an
engagement — context, evidence, acceptance criteria, outcome — lives in its **owning task**
under `tasks/`. `DISCUSSIONS.md` is only the monitoring index: which upstream threads we are
in, what state each is in, when we last looked. One row per thread, one owning task per row.

**`DISCUSSIONS.md` is a queue, not a log.** It holds Active rows plus a small
`## Recently concluded` staging section. Concluded rows leave the file on a periodic sweep.
Traceability does not come from this file:

- **The owning task** is the durable record — outcome and history land in its
  `## Work Completed` when it closes.
- **Archive artifacts** under `tasks/working_artifacts/discussion-archive/` are the bounded,
  disposable index of concluded engagements, kept to support periodic review (response
  latency, which upstreams engage, what outcomes we actually get). Git history is the deep
  backup for everything.

## Registering an engagement

When a thread is opened upstream (or we join an existing one):

1. Ensure an owning task exists (per [task_management.md](./task_management.md)) — the task
   records why we're engaged and what "done" means.
2. Add a row to `## Active` in DISCUSSIONS.md:

   | Column | Content |
   |--------|---------|
   | Thread | `[#NNNN](url)` — link to the discussion/issue/PR |
   | Repo | `owner/repo` |
   | Kind | Discussion / Issue / PR |
   | Task | Link to the owning task file |
   | State | One of the states below |
   | Last checked | `YYYY-MM-DD` — stamped by every check-in |
   | Next action | One line: what we're waiting for or should do next |

## States

| State | Meaning |
|-------|---------|
| `needs-our-reply` | Someone responded; the ball is in our court. Highest urgency. |
| `waiting-on-maintainer` | We posted; awaiting upstream response. |
| `patch-in-flight` | A change we drove is submitted (PR / Gerrit) and under review. |
| `dormant` | No activity for 30+ days. Still checked, but a candidate for a nudge or a conscious abandon (decide on the owning task). |

## The check-in routine (session start)

Run at every session start (see [SESSIONLOOP.md](../SESSIONLOOP.md)) — it costs seconds:

1. For each `## Active` row, fetch activity since `Last checked` with `gh`
   (authed as `twbarnes1972`; full path on this workstation:
   `& "C:\Program Files\GitHub CLI\gh.exe"`):
   - **Discussions** (GraphQL only):
     ```
     gh api graphql -f query='{ repository(owner: "OWNER", name: "REPO") {
       discussion(number: NNNN) { comments(last: 10) { nodes {
         author { login } createdAt bodyText
         replies(last: 5) { nodes { author { login } createdAt bodyText } } } } } } }'
     ```
   - **Issues / PRs** (REST):
     ```
     gh api repos/OWNER/REPO/issues/NNNN/comments --jq '.[] | {user: .user.login, created_at, body}'
     ```
2. Disposition per row:
   - **New substantive activity** → set `needs-our-reply`, record the development on the
     owning task, and surface it to the operator if the reply needs judgment (tone,
     commitment, technical position). Routine acknowledgments the agent may post directly.
   - **No activity** → stamp `Last checked`; if 30+ days idle, set `dormant`.
   - **Thread resolved upstream** → follow *Concluding* below.
3. Report a one-line summary in the session start notes (e.g. "2 active, no new replies").

## Concluding

A row concludes **when its owning task closes** — one close point, no drift. On task close:

1. Record the outcome in the task's `## Work Completed` (merged / fixed independently /
   rejected with rationale / consciously abandoned).
2. Move the row from `## Active` to `## Recently concluded` with a one-line outcome and date.

## Offload sweep

When `## Recently concluded` crosses **~10 rows** (or on operator request), sweep it to a
dated artifact: `tasks/working_artifacts/discussion-archive/archive-YYYY-MM-DD.md` — the
concluded rows verbatim, plus an optional one-line observation per engagement (responsiveness,
what worked). Then clear the staging section. Artifacts are self-contained and disposable once
any review has consumed them; the durable record stays on the tasks.

<!-- version: v2026.07.12.01 -->
