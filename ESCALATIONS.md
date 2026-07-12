# Escalations

Agent-to-human **queue** with two lanes. This is a queue, not a log: a resolved item **leaves the
file** (its durable record goes on the task graph or a dated triage artifact under
`tasks/working_artifacts/escalation-triage/`). See
[tasks/escalation_handling.md](./tasks/escalation_handling.md) for the full lifecycle.

- **`## Pending`** — the operator-blocker register. Things only you can provide (a credential, a
  sign-in, a decision) that gate **go-live / acceptance**, *not* the build. The agent keeps building
  against mocks; each affected task lands test-green and waits here. (Task-scoped blocks that pause a
  single task go in the task file as `[QUESTION]`, not here.)
- **`## Revisit`** — the non-blocking autonomous veto-log. Non-obvious calls the agent made and moved
  past, parked for async veto. Triaged on a ~10-item threshold.

---

## Pending

_(Operator-blocker register. Group by what only you can provide; give each a stable id; state what it
gates; mark resolved inline, then let it leave. None outstanding.)_


## Revisit

_(Autonomous veto-log: decision · reversal cost · explicit veto window. None outstanding.)_
