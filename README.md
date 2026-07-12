# Open Source Contributing

Home base for managing open source contributions on GitHub — upstream issues, discussions, and pull requests, tracked from first finding to merged (or resolved) outcome.

Other project repos occasionally uncover something that belongs upstream: a bug in a dependency, a gap in its docs, a behavior worth a discussion thread. Those projects fix or work around the problem locally, then hand the *open-source-facing* half off to this repo — where it becomes a tracked task with a lifecycle, instead of a forgotten browser tab.

---

## What lives here

- **Upstream engagements** — issues and discussions opened on GitHub projects: monitoring maintainer responses, answering follow-ups, keeping threads moving.
- **Patches and pull requests** — when maintainers are receptive, driving a fix from local repro to submitted PR to merge.
- **Hand-offs from other repos** — findings characterized elsewhere (with root cause and repro) that need someone to own the upstream conversation. Example: the SQLAlchemy `StaticPool` silent lost-commits finding, root-caused in `agent-email-tool` and handed here to engage the upstream thread and drive a potential fix.
- **Contribution history** — closed tasks form a record of what was reported, argued, patched, and merged, and under which account.

## Contribution lifecycle

```
finding (often from another repo)
   → intake item in INSTRUCTIONS.md
   → task in tasks/open/ (repro, links, upstream thread, acceptance criteria)
   → engage upstream: issue / discussion / PR
   → monitor and respond across sessions
   → outcome recorded, task closed to tasks/closed/
```

A task closes on a real outcome — merged, fixed independently, rejected with rationale, or consciously abandoned — not just on "posted upstream".

## Workflow

This repo uses the [stackagentic-library](https://gitea.msiportal.io/msidevopsmaster/stackagentic-library) task management system. The moving parts:

| File / directory | Role |
|---|---|
| [INSTRUCTIONS.md](INSTRUCTIONS.md) | Human → Agent intake queue. New contributions and hand-offs land here. |
| [ESCALATIONS.md](ESCALATIONS.md) | Agent → Human concerns raised during autonomous work. |
| [FEEDBACK.md](FEEDBACK.md) | Bidirectional process-calibration channel. |
| [SESSION.md](SESSION.md) / [SESSIONLOOP.md](SESSIONLOOP.md) | Session-to-session carryover state and the start/end checklist. |
| `tasks/open/` → `tasks/closed/` | Task lifecycle. One markdown file per contribution effort. |
| `tasks/working_artifacts/` | Bulky companions to a task — repro scripts, logs, draft patches. |
| [tasks/task_formatting.md](tasks/task_formatting.md), [tasks/categories.md](tasks/categories.md) | Task file format and ID prefixes. |

Day-to-day operations use the `task-manager` CLI from stackagentic-library (already installed machine-wide).

## Conventions

- **GitHub account:** upstream activity is posted as `twbarnes1972`.
- **Hand-offs must arrive characterized.** An intake item from another repo should carry the root cause, a minimal repro, version matrix, and links to any upstream thread already opened. This repo owns the conversation, not the original investigation.
- **Every engagement gets a task file** — the upstream thread URL, current state, and next expected action live in the task, so any session can pick up monitoring where the last one left off.
- **Monitoring is recurring work.** Open engagements are checked at session start (see SESSIONLOOP.md); waiting on a maintainer is a task state, not a reason to lose the thread.
