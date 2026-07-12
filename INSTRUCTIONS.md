
# Instructions

---
**Related:**
- [Instruction Handling Workflow](./instruction_handling.md) -- How to process items in this document
- [Task Management](./task_management.md) -- Instructions for Managing Tasks

---

## Items

_(no items pending intake)_

---

## Processing

| # | Item | Task ID | Status |
|---|------|---------|--------|

---

## Completed

### 2026-07-12 — Second intake (1 item — created)
Processed the permission-probe hand-off (claude-code permission-matcher findings, their ISSUE-0001) into [ISSUE-0002](./tasks/open/ISSUE-0002.md) (Medium). Investigation, workaround hook, and publication (github.com/twbarnes1972/permission-probe) were done in the origin repo; this task owns the three upstream `anthropics/claude-code` threads where root-cause comments were posted 2026-05-18 as `twbarnes1972` (#36884 primary disassembly, #57132 cross-link, #15921 multi-bug). Live state discovered at intake via `gh`: **#36884 was stale-closed 2026-07-07 ("not planned") with our analysis un-triaged on it**; #57132 is open with a community anti-stale comment pointing to our analysis (natural primary thread now); #15921 open, nothing owed. Pending decision carried in the task: reopen #36884 vs consolidate onto #57132 — operator approval + a freshness check against the current release (analysis targets 2.1.143.a06) before any new upstream post. All three threads registered in DISCUSSIONS.md → ISSUE-0002. This intake also drove two `discussion_handling.md` refinements: multi-thread engagements (one task, many rows) and "Issues we report" rules (verified-fix conclusion; stale-closure is a decision point, not a conclusion).

### 2026-07-12 — First intake (1 item — created)
Processed the agent-email-tool hand-off (SQLAlchemy StaticPool silent lost-commits, their ISSUE-0018) into [ISSUE-0001](./tasks/open/ISSUE-0001.md) (Medium). The task owns the open-source-facing half: monitor/engage upstream discussion [#13428](https://github.com/sqlalchemy/sqlalchemy/discussions/13428) (posted 2026-07-12 as `twbarnes1972`, answering unresolved 2021 discussion #6987), and drive a fix if maintainers are receptive — concurrent-checkout guard in `StaticPool` (`pool/impl.py:452`) and/or docs warnings (`aiosqlite.py`, `pysqlite.py`, StaticPool docstring), submitted via Gerrit (not GitHub PRs). Sequencing directive carried into the task: wait for maintainer reaction before investing in a patch; check #13428 at each session start (gh CLI authed as `twbarnes1972`). Local clone ready at `C:\Data\open-source\sqlalchemy` (`main` @ `07e2c9f4e`). Evidence artifacts remain in agent-email-tool (ISSUE-0018/0017 + working artifacts: repro, matrix runner, as-posted draft). py-cog's test-fixture knock-on was handed to that repo directly — explicitly out of this task's scope.

---
