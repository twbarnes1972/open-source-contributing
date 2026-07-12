# Escalation Handling Workflow

How agents write to [ESCALATIONS.md](../ESCALATIONS.md) -- the agent-to-human channel -- and how
those items are triaged and cleared. Mirrors [instruction_handling.md](./instruction_handling.md)
(human -> agent). This workflow is agent -> human.

---

## The three escalation mechanisms

An agent has three distinct ways to surface something to the human. They differ by **what they block**
and **who owns the next move**. Picking the right one is the whole game:

| Mechanism | Scope | Blocks | Who acts next | Lives in |
|-----------|-------|--------|---------------|----------|
| **`[QUESTION]`** | one task | **pauses that task** mid-execution -- the agent stops and waits | human answers, agent resumes | the task file |
| **`## Pending`** | a goal / epic | gates **go-live / acceptance**, *not* the build -- work proceeds against mocks; items wait | human provides the credential / decision / access | `ESCALATIONS.md` |
| **`## Revisit`** | one decision | **nothing** -- async transparency | human may veto later, or it stands | `ESCALATIONS.md` |

The distinction that matters most: **`[QUESTION]` vs `## Pending`.** `[QUESTION]` is "I cannot finish
*this task* without an answer right now" -- it pauses one task. `## Pending` is "this whole class of
work is gated on something only you can provide (a credential, a sign-in, a policy decision, external
infra), and I am building against mocks until then" -- it gates a *goal*, the build keeps moving, and
the item stands across many sessions until you clear it.

---

## The core principle

**`ESCALATIONS.md` is a *queue*, not a log.** It holds only what is currently outstanding. A resolved
item **leaves the file** -- it is never archived in place. That is what keeps the file bounded and
removes the in-file "Resolved" log that, in practice, never gets cleared.

Traceability does not come from `ESCALATIONS.md` growing forever. It comes from two durable homes:

- **The task graph** -- any item that *changed course* (a reverted decision, or a blocker that forced a
  different path) is recorded on its **subject task** plus a **pivot/follow-up task**. Decisions live
  where the work lives.
- **Triage artifacts** -- each `## Revisit` triage session emits one dated file under
  `tasks/working_artifacts/escalation-triage/`. These are the bounded, prunable record of *endorsed*
  items, kept only to support the **scoping review** (was this even worth flagging?). Git history is the
  deep backup for everything.

---

## When to Escalate

| Situation | Lane | Example |
|-----------|------|---------|
| **Goal-gating dependency you can't self-provide** -- credential, sign-in, external infra, a policy/architecture decision that's the human's to make | `## Pending` | "Live Teams send needs a one-time device-code sign-in by you to mint the refresh token. Built + mock-tested; waits on this." |
| **Non-obvious call you made and moved past** -- you chose an approach, with a reasonable but reversible default | `## Revisit` | "Held the cursor on errored turns so a transient LLM outage self-heals. Veto if you'd want a dedicated dead-letter table instead." |
| **Design tradeoff** -- one approach over another, worth a veto window | `## Revisit` | "Used keyword routing instead of embedding similarity. Faster, less flexible. Reversal cost low." |
| **Codebase concern / spec conflict** -- something seems wrong, or the task contradicts conventions | `## Revisit` | "Task says add a migration, but the project auto-creates tables at startup." |
| **Quality feedback on the task spec** -- could be improved for future tasks | `## Revisit` | "Acceptance criteria mix implementation detail with behavior -- harder to verify." |

### Do NOT escalate (use another mechanism)

| Situation | Use instead |
|-----------|-------------|
| **Blocked -- can't finish *this task* without an answer now** | `[QUESTION]` in the task file (pauses the task) |
| **Bug found in existing code** | Fix it if in scope, or create a task in `tasks/open/` |
| **Task is done** | Standard completion workflow + commit |
| **Need to communicate with another agent** | Not supported -- work independently |

---

## Lane 1 -- `## Pending`: the operator-blocker register

A standing register of things that **gate a goal or epic but not the build**. The agent keeps building
against mocks/stubs; each affected task lands test-green and *waits* on its blocker. Only the human can
clear these.

**Recommended conventions** (this is the battle-tested shape -- adopt as much as fits the project):

- **Give each blocker a short stable id** (`H1`, `H2`, …) so tasks and sessions can reference it.
- **Group by what only the operator can provide** -- e.g. *Credentials / external access*, *Operator
  knowledge / policy*, *Architecture decisions I'm making (veto if wrong)*. The third group is the
  agent surfacing calls it is empowered to make but wants on the record.
- **State what it gates, explicitly:** "These block Epic 1 go-live, NOT the build. Implementation
  proceeds now against mocked IMAP/Graph/LLM; each task lands test-green and waits."
- **Link the gating task** -- the register is a view; the authoritative blocker list lives on the
  epic/plan task (e.g. a "Human-Blocker Register" section). Keep them in sync.
- **Clear inline, then let it leave.** When the operator resolves a blocker, mark it inline
  (`✅ RESOLVED — <how>` / `CLEARED <date>`) and keep that line *briefly* for session narrative. Once
  the dependent work has consumed the resolution, the item **leaves the file** (its durable record is on
  the task it unblocked). The register stays short.

A `## Pending` item that, once answered, *forces a change of direction* follows the **reverted/blocked**
path (record on subject task + pivot task) below.

---

## Lane 2 -- `## Revisit`: the autonomous veto-log

A **non-blocking** audit trail of non-obvious calls the agent made and moved past during autonomous /
unattended work. The operator's **async veto queue**: each entry is a decision the agent already shipped,
parked here so you can veto it later. Nothing waits on it.

**Each entry should carry:**
- **Date + session + task/issue id**, and a one-line title of the call.
- **What was decided** and the *non-obvious* part (why this over the obvious alternative).
- **Reversal cost** (low / med / high) -- how expensive it is to undo if vetoed.
- **An explicit veto window** -- "Veto if you'd rather X" -- naming the specific alternative.
- **Deploy state** if relevant ("landed + committed, not yet deployed -- ships on next worker restart").

This lane is where the **When to Escalate** judgment is exercised most: log the calls a reviewer would
want to catch; don't log the obvious ones.

### How `## Revisit` items leave -- triage

At a **triage session** (see Cadence), every `## Revisit` item resolves to exactly one outcome, then
**leaves the queue**:

**a. Endorsed (the common case).** The decision stands. Endorsement is **assumed by task sign-off** --
accepting a task on its acceptance criteria already endorses the calls underneath -- so it is *not*
re-documented on the task. Instead: record a one-liner in the current triage artifact
(`subject-task · short title · endorsed`) and remove the item. These one-liners exist only to feed the
scoping review; they are disposable.

**b. Reverted / Blocked (more work needed).** The decision is overturned, or a blocker forces a different
path. The durable record goes on the **task graph**:
1. Update the **subject task** (even if closed): `**Post-close revision (YYYY-MM-DD):** <decision> → see <pivot task id>`.
2. File the **pivot/follow-up task** (per [task_management.md](./task_management.md)); link it back.
3. Record the disposition in the triage artifact as an index line (subject → pivot).
4. Remove the item from `## Revisit`.

---

## How to write an entry

```markdown
### [YYYY-MM-DD] TASK-ID: Short description
Context and what you decided or observed. 2-4 sentences.
For ## Pending: what you need + what it gates. For ## Revisit: the call, reversal cost, and the veto window.
```

Use the current (absolute) date, name the task, be specific, keep it short. The human can read the
code/task for the rest.

---

## Cadence

- **At session-start**, the agent **reads `ESCALATIONS.md`**: it reviews the `## Pending` register
  (acting on anything newly resolvable, flagging anything now stale) and **reports the `## Revisit`
  count**. When the un-triaged `## Revisit` queue crosses **~10 items**, it prompts the operator for a
  triage session. The operator may call one any time. The trigger is depth, not a fixed clock.

---

## The triage artifact

One file per triage session: `tasks/working_artifacts/escalation-triage/triage-YYYY-MM-DD.md` (modeled on
`tasks/working_artifacts/task-sessions/`; the folder is created on first triage). Contents:

1. **Endorsed** -- one line per item (`date · subject-task · short title`). The scoping-review corpus.
2. **Reverted / Blocked** -- decision + subject-task + pivot-task references (the durable record is on
   the tasks; this is the index).
3. **Scoping note** -- which items probably should *not* have been escalated.

---

## Escalation scoping (the feedback loop)

The artifacts' real payoff: periodically read the endorsed pile and ask *"which of these didn't need to
be a `## Revisit` entry at all?"* Over-logged calls are noise; consistently endorsed-as-obvious
categories should stop being logged. Under-logging hides real decisions. This grades and tightens the
agent's judgment about what is worth surfacing -- the one reason endorsed items are kept at all.

---

## Pruning

- **`ESCALATIONS.md`** needs no pruning -- it is always just the current queue (cleared register items
  and triaged Revisit items both leave).
- **Triage artifacts** are self-contained and disposable; once a scoping review has consumed a batch,
  old ones may be deleted/archived (the decisions that mattered are on tasks).
- **Git history** (`git log -p ESCALATIONS.md`) is the deep backup for any item's full original text.

---

## Relationship to other channels

```
INSTRUCTIONS.md    Human → Agent   "Do this"                intake, becomes tasks
ESCALATIONS.md     Agent → Human   "Check / unblock this"   two lanes:
  ├ ## Pending     Agent → Human   "Only you can unblock"   gates a goal/epic; build proceeds on mocks
  └ ## Revisit     Agent → Human   "I decided X — veto?"    non-blocking autonomous veto-log
[QUESTION]         Agent → Human   "I'm stuck on THIS"      pauses one task, waits for an answer
SESSION.md         carryover       "where we are"           bounded; see session_handling.md
```

The blocking story is two-tiered: **`[QUESTION]`** pauses a *single task* and waits; **`## Pending`**
is a standing register of *goal-gating* blockers where the build keeps moving against mocks. **`## Revisit`**
blocks nothing -- it is fire-and-forget transparency the operator can veto. Use `[QUESTION]` only when you
genuinely cannot proceed on the task in front of you.

<!-- version: v2026.06.20.01 -->
