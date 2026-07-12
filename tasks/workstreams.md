# Workstreams

Defines the **workstream** axis for this project — the *lane* a task sits in, distinguished by
the **gate** that governs *when* it can be built/shipped. Orthogonal to the category prefix.

> **Scaffold template.** This file ships the *axis*, the `**Workstream:**` field, and the rules.
> The **lane values** below are an **example** — replace the table in *The workstreams* with the
> lanes that match how your project actually gates work. Keep the *Two axes* and *Rules* sections.

## Two orthogonal axes — don't conflate them

A task is classified on **two independent dimensions**:

| Axis | Question it answers | Where it lives |
|------|---------------------|----------------|
| **Category** (prefix `FEAT`/`BUG`/`INF`/`PLAN`/…) | *What kind of work is this?* | the task ID prefix ([`task_management.md`](task_management.md)) |
| **Workstream** (this file) | *Which gate governs when this ships?* | the `**Workstream:**` field in the task header |

The same category can sit in different lanes (an `INF` task may be *Infrastructure* *or*
*Decision-gated* — same kind of work, different gate). So a workstream is **not** a prefix; it's
a lane label orthogonal to it.

## The workstreams

> **EXAMPLE — replace with your project's lanes.** Each lane should name a distinct *gate* (a
> condition that governs when its tasks may ship), not a kind of work.

| Workstream | Gate / timing | What belongs here |
|------------|---------------|-------------------|
| **Maintenance** | None — continuous | Correctness defects and hardening of already-shipped surface; fix + deploy as they arise. |
| **Active build** | Build now | Work being driven toward a near-term ship. |
| **Decision-gated** | Frozen until a named decision | Work that only pays off once a pending decision lands; don't build ahead of it. |
| **Roadmap** | Deferred to a future phase | Planned-but-not-now capability, sequenced behind a phase or milestone. |

## Rules

1. **Single-valued.** A task is in **exactly one** workstream — the lane whose gate governs it.
   Keeps the board scannable and the "which gate?" question unambiguous.
2. **Cross-lane influence = a dependency edge, not a second lane.** If one lane's work *unlocks*
   another, record it as an `Enables:` / `Related` edge in `## Dependencies` / `## Related` —
   **not** by tagging the task with two workstreams.
3. **A task that genuinely spans lanes is a decomposition smell.** It's usually an *epic* that
   should split into per-lane children (group them with the `**Epic:**` field, not a second lane).

## Task-file field

Every task carries a header field naming exactly one lane from the table above:

```markdown
**Workstream:** Maintenance | Active build | Decision-gated | Roadmap
```

## Gitea mapping

When work syncs to Gitea Issues, each workstream maps to a **scoped, exclusive** label under the
`workstream/` scope (e.g. `workstream/maintenance`). Gitea's **Exclusive** flag enforces "one
`workstream/*` label per issue" — Rule 1 enforced by the tool, not by discipline. The file-side
`**Workstream:**` field is the source of truth; [`gitea_handling.md`](gitea_handling.md) maps it
to/from the label.

<!-- version: v2026.06.11.01 -->
