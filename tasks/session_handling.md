# Session-Carryover Handling Convention

How [SESSION.md](../SESSION.md) stays useful and bounded -- the lifecycle for session-to-session
carryover. Parallel to [escalation_handling.md](./escalation_handling.md) (the ESCALATIONS queue) and
[instruction_handling.md](./instruction_handling.md) (the INSTRUCTIONS queue).

---

## The purpose comes first (this overrides the mechanics below)

**SESSION.md is the agent's own working-memory handoff -- it is more for the agent than the operator.**
Its one job is that the *next* session picks up with the right context. **That goal outranks every rule
in this file.** A trimming mechanic that drops something the next session needs has failed, no matter how
tidy it leaves the file.

So: **curate, don't mechanically truncate.** Each session, the agent decides what live context best
serves the next pickup -- synthesizing or rewriting the current-state when that beats keeping N verbatim
entries; keeping more when an arc is mid-flight, less when things are clean.

## The core principle

**SESSION.md is a *current-state view*, not a log** (same principle as `ESCALATIONS.md`). It holds the
standing focus plus what the next session needs to resume. Older per-session detail **leaves the file**
-- it is not retained inline. That is what keeps it bounded.

Traceability does not come from SESSION.md growing forever. It comes from:
- **The per-session archive** -- a full, verbatim session wrap written per session under
  `tasks/working_artifacts/task-sessions/` (the `session-planner` skill writes these if the project
  uses it; otherwise write the wrap by hand at session end). **That file is the durable record** --
  SESSION.md does not need to duplicate it.
- **The task graph + git history** -- decisions live on their task files; git holds every prior
  revision of SESSION.md as the deep backup.

> **If the project has no per-session archive** (no `session-planner`, no hand-written wraps), then
> SESSION.md's recent-session region *is* the only narrative record -- so trim it more conservatively,
> and lean on git history before deleting anything not captured on a task.

## What SESSION.md keeps (the live region)

Mapped to the SESSION.md section shape:

1. **`## Current Focus`** -- the START-HERE for the next session: what to pick up first, plus any
   standing operating-context / directive ("X is LIVE -- coordinate before disrupting"). **Rewritten to
   reflect *now*** every session, not left to go stale.
2. **`## In-Flight Tasks`** -- tasks started but not closed, with one-line status. Drop rows as tasks
   close.
3. **`## Open Questions`** -- questions raised but unresolved. Resolve in place, or promote a blocking
   one to a `[QUESTION]` in the task file.
4. **`## Recent Sessions`** -- a *guide* of ~2-3 recent session summaries for continuity. **Guide, not
   rule** -- keep one well-synthesized current-state if that serves better, or more if a multi-session
   arc is live. A pointer to `tasks/working_artifacts/task-sessions/` covers everything older.

## What leaves (and where it goes)

Everything older than the live region leaves SESSION.md. When a per-session archive exists, trimming is
usually just **deleting the now-redundant inline copy** -- the durable record already exists.

**Before deleting an old inline entry, confirm it is archived.** If a session predates the
per-session-file practice (or its SESSION.md entry was ever richer than its archive), copy the delta
into that file first -- or, for a one-time backlog cut spanning many sessions, write the lot verbatim
into a single `tasks/working_artifacts/task-sessions/SESSION-archive-YYYY-MM-DD.md` batch file (git is
the per-line backup either way). **Never drop an entry that has no archived home.**

## Cadence

At **session end** (a step in [SESSIONLOOP.md](../SESSIONLOOP.md) "Ending a Session"):

1. Write this session's wrap into `## Recent Sessions` (most recent first).
2. **Trim**: drop `## Recent Sessions` entries that fall outside the ~2-3 live region (they're archived
   under `task-sessions/`). **Refresh** `## Current Focus`, `## In-Flight Tasks`, and `## Open Questions`
   so they reflect *now*.

No fixed size target -- judge by usefulness -- but if SESSION.md is climbing toward **~50 KB** it is
overdue for a trim.

## Pruning

- **SESSION.md** needs no internal pruning beyond the session-end trim -- keeping the live region small
  *is* the prune.
- **Per-session archive files** are self-contained; old ones may be thinned/deleted once nothing
  references them (git remains the deep backup).
- **Git history** is the deep backup for any prior SESSION.md state, full text.

<!-- version: v2026.06.16.01 -->
