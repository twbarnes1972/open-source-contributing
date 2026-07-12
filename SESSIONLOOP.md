# Session Instructions

How to open and close a working session. Keep this short -- the checklist, not the philosophy.

---

## Starting a New Session

- push/pull and resolve any merge conflicts
- Read `CLAUDE.md` for project context (layout, conventions, tooling status)
- Read `SESSION.md` for carryover state (in-flight tasks, resume hints, open questions)
- Read `ESCALATIONS.md` (per [tasks/escalation_handling.md](./tasks/escalation_handling.md)): review the `## Pending` blocker register (act on anything newly resolvable; flag anything now stale), and **report the `## Revisit` count** -- if it has crossed ~10 items, prompt for a triage session
- Read `FEEDBACK.md` `## From Agent` and `## From Human` -- route any pending items per [tasks/feedback_handling.md](./tasks/feedback_handling.md)
- Use the session-planning tool

---

## Ending a Session

- Review any changes not committed for items having secrets, sensitive information, or other non-persistent data that should be added to `.gitignore`
- Make sure any instructions in `INSTRUCTIONS.md` that have been tasked are properly handled per: `tasks/instruction_handling.md`
- Make sure `tasks/task_list.md` appropriately reflects the current disposition of open and closed tasks
- Update **and trim** `SESSION.md` so it reflects this session's end state -- current focus, in-flight tasks, new open questions -- keeping it a bounded current-state view per [tasks/session_handling.md](./tasks/session_handling.md)
- For anything that needs to be addressed, pick the right channel:
    - **durable project facts / conventions** -> `CLAUDE.md`
    - **transient session-to-session carryover** -> `SESSION.md`
    - **a goal-gating blocker only the human can clear** -> `ESCALATIONS.md` `## Pending` register; **a non-obvious autonomous call to surface for veto** -> `ESCALATIONS.md` `## Revisit` (per `tasks/escalation_handling.md`)
    - **process/collaboration calibration (either direction)** -> `FEEDBACK.md` (per `tasks/feedback_handling.md`)
- **Mutual feedback moment** -- either side offers one line about how the session went per [tasks/feedback_handling.md](./tasks/feedback_handling.md). Genuinely optional; skip if nothing to flag. Write entries to FEEDBACK.md, not the session file. Positive feedback is welcome too.
- push/pull and resolve any merge conflicts
