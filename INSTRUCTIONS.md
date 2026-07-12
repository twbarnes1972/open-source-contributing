
# Instructions

---
**Related:**
- [Instruction Handling Workflow](./instruction_handling.md) -- How to process items in this document
- [Task Management](./task_management.md) -- Instructions for Managing Tasks

---

## Items

- **Freshness-check report from permission-probe (for [ISSUE-0002](./tasks/open/ISSUE-0002.md)) — both root-caused bugs are FIXED upstream, verified 2026-07-12 on claude.exe 2.1.207 (Windows native CLI).** This is the report ISSUE-0002's 2026-07-12 status note is waiting on; its freshness-check acceptance criterion is now satisfied. Findings:
  - **Bug 1 (`XIq` matcher):** path-globbed `Edit(...)` allow rules now match (allowed with `permissionDecisionMs=3`; negative control with no rule correctly blocked), and path-globbed deny rules now override bare allows — verified in BOTH `--print`/sdk-cli and the interactive TUI (`entrypoint=cli`, driven programmatically via ConPTY/pywinpty). The `XIq` reject line (`ruleValue.ruleContent!==void 0 → return false`) is **still present** in the 2.1.207 binary (minified as `pto`, offset ~232912623) — upstream fixed behavior by adding a separate content-matching path, not by removing the filter.
  - **Bug 2 (`bypassPermissions` gate):** `"defaultMode": "bypassPermissions"` in settings.json now activates (`ctx.mode=bypassPermissions` in debug log, no "setMode rejected" line). Caveat: test sandbox had `bypassPermissionsModeAccepted: true` seeded in `.claude.json`, so activation may be conditional on prior acceptance of the bypass warning dialog.
  - **Bonus (permission-probe ISSUE-0004, now closed):** the TUI-vs-`--print` divergence on bare MCP allow rules is also fixed (TUI: `permissionDecisionMs=0`, no prompt).
  - **Fix version unknown** — landed silently somewhere in 2.1.145–2.1.207; no maintainer comment on any tracked thread. All tests ran in an isolated `CLAUDE_CONFIG_DIR` sandbox with no hooks. Full method, logs, and reproducer results: `permission-probe/tasks/closed/ISSUE-0004.md` § Resolution (2026-07-12); README deprecation note + INVESTIGATION.md compatibility-table annotation landed same day.
  - **Consequences for ISSUE-0002:** reopen-vs-consolidate on #36884 is moot. Per the operator call already recorded in the task's status note, conclude all three threads: post resolution notes on #57132 and #15921 so followers know (drafting owed; needs operator approval before posting per task's implementation notes). **Scope caution for the #15921 note:** our verification covers the native CLI only — the thread's third failure mode (Bash rules ignored specifically in the VS Code extension, the OP's primary symptom) was never root-caused by us and is NOT covered; recent commenters there (2026-06-25, 2026-07-02, 2026-07-07 — the last is user `cveld`'s frustration comment, not ours) are largely VS Code extension users who may still be affected. Word the resolution note to claim only what was verified.

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
