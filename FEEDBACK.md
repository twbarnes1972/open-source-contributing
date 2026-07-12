# Feedback

Bidirectional calibration channel between the human and agents. Used to surface friction, misalignments, and patterns worth adjusting -- from either side, after a session or mid-flight when something feels off.

**Distinguished from other channels:**

| Channel | Direction | Scope | Nature |
|---------|-----------|-------|--------|
| [INSTRUCTIONS.md](./INSTRUCTIONS.md) | Human -> Agent | Actionable directives that become tasks | Do this |
| [ESCALATIONS.md](./ESCALATIONS.md) | Agent -> Human | Task-level concerns, assumptions, design tradeoffs | Check this |
| **FEEDBACK.md** | **Bidirectional** | **Process, collaboration, and session-shape observations** | **Calibrate how we work** |
| `[QUESTION]` in task files | Agent -> Human | Blocking -- needs answer before task continues | I'm stuck |

Related: [tasks/feedback_handling.md](./tasks/feedback_handling.md) -- format, triggers, and interactive feedback session moderator guide.

---

## From Agent

_(Agent-originated feedback about how sessions or collaboration felt. Non-blocking. Human reviews and acknowledges or acts on at session start. Examples: felt whipsawed by rapid direction changes, scope shifted mid-execution without re-alignment, context was thin, instructions conflicted.)_

- **2026-07-12** — Productive session. The "implement and test on the clone before suggesting
  anything upstream" directive was the right call and clearly raised the quality of the #13428
  engagement — it caught our own cache=shared error before it reached a maintainer and turned a
  speculative reply into a validated one. Worth keeping as a standing norm for this repo:
  no untested upstream suggestions.

---

## From Human

_(Human-originated feedback about agent behavior, output quality, or process. Agent acknowledges, saves to memory if it's a behavioral pattern, or spawns a task if it's a process gap. Examples: over/under-engineered, output padded or buried the answer, missed an obvious boundary, ignored prior guidance.)_

---

## Resolved

_(Addressed items -- moved here with a short resolution note and date. Periodically pruned; git history is the archive.)_
