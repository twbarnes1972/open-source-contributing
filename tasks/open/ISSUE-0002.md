# ISSUE-0002: claude-code permission-matcher engagement — own three upstream issue threads (hand-off from permission-probe ISSUE-0001)

**Created:** 2026-07-12
**Status:** Open
**Priority:** Medium
**Category:** Issue tracking
**Workstream:** Active build
**Owner:** agent

---

## Summary

Own the open-source-facing half of the claude-code permission-matcher findings from
permission-probe (their `tasks/closed/ISSUE-0001.md`; investigation, workaround hook, and
publication all done there). Root-cause comments were posted 2026-05-18 as `twbarnes1972` to
three `anthropics/claude-code` issues. This task covers monitoring those threads, the
now-pending reopen-vs-consolidate decision (the primary thread was stale-closed), and
verifying any eventual fix against the reproducer before concluding.

One engagement, three threads — each has its own row in [DISCUSSIONS.md](../../DISCUSSIONS.md)
per [discussion_handling.md](../discussion_handling.md).

## Background

Two independent bugs verified by disassembling `claude.exe` 2.1.143.a06:

1. **`XIq` matcher filter** — any permission rule with parens content
   (`Edit(/path/**)` → `ruleContent`) is unconditionally rejected before matching. Path-globbed
   allow *and* deny rules are silent no-ops for `Read`/`Edit`/`Write`/`Glob`/`NotebookRead`/
   `NotebookEdit`/`Skill` and `mcp__server__tool(arg)`. `Bash(...)`/`PowerShell(...)` work only
   because they have their own content matchers.
2. **`bypassPermissions` launch-time gate** — `"defaultMode": "bypassPermissions"` in
   settings.json is silently rejected; the enabling flag only flips via CLI launch args.

Full narrative, methodology, and reproducer:
`permission-probe/tasks/working_artifacts/ISSUE-0001/INVESTIGATION.md`; workaround hook and
picomatch-exoneration probe published at https://github.com/twbarnes1972/permission-probe
(GPL-3.0 with standing Anthropic grant).

## Steps to Reproduce

Condensed (full four-row matrix in permission-probe ISSUE-0001): with
`Edit(/home/me/**)` in `permissions.allow` and cwd `/home/me/project-a`, run
`claude --print --debug "permission,tool" -- "Edit /home/me/project-b/notes.md ..."` —
the Edit is blocked despite matching the allow glob. Deny rules fail symmetrically.

## Expected vs Actual Behavior

- **Expected:** path-globbed allow/deny rules match; `defaultMode: bypassPermissions` activates.
- **Actual:** both are silent no-ops (details in Background / permission-probe ISSUE-0001).

## Root Cause

Established at the code level in permission-probe ISSUE-0001 (`XIq` reject line;
`isBypassPermissionsModeAvailable` launch-time gate). Not in picomatch (independently verified).

## Thread state (as of 2026-07-12)

| Thread | Our comment (2026-05-18) | State |
|--------|--------------------------|-------|
| [#36884](https://github.com/anthropics/claude-code/issues/36884) | [primary root-cause + disassembly](https://github.com/anthropics/claude-code/issues/36884#issuecomment-4474702923) | **Stale-closed 2026-07-07 by github-actions as "not planned"** — never maintainer-triaged |
| [#57132](https://github.com/anthropics/claude-code/issues/57132) | [cross-link comment](https://github.com/anthropics/claude-code/issues/57132#issuecomment-4474764284) | Open. `hwaterer` ([2026-06-10](https://github.com/anthropics/claude-code/issues/57132#issuecomment-4667362004)) posted anti-stale, points readers to our #36884 analysis, notes #57132 has the accurate surface-agnostic title |
| [#15921](https://github.com/anthropics/claude-code/issues/15921) | [multi-bug comment (both findings)](https://github.com/anthropics/claude-code/issues/15921#issuecomment-4474820813) | Open. Latest activity ([2026-07-07](https://github.com/anthropics/claude-code/issues/15921#issuecomment-4905019332)) is user frustration; nothing owed |

## Dependencies

| Blocked By | None |

## Acceptance Criteria

- [x] Reopen-vs-consolidate decision made with the operator and recorded here: **moot** — the
      freshness check found both bugs already fixed upstream, so there is no analysis to
      relocate and no reopen to request (see 2026-07-12 status note).
- [x] Before any new upstream post: freshness check — **done** by permission-probe: verified
      on `claude.exe` 2.1.207 (native CLI), both bugs fixed (fix landed silently in
      2.1.145–2.1.207). Full method/logs in `permission-probe/tasks/closed/ISSUE-0004.md`.
- [x] Root-cause analysis ends up on (or linked prominently from) an open, maintainer-visible
      thread — satisfied historically (our analysis on #36884, cross-linked from open #57132
      by `hwaterer`); now superseded by resolution notes announcing the fix.
- [ ] All three DISCUSSIONS.md rows checked each session start; substantive replies engaged.
- [x] If a fix ships: re-run the permission-probe reproducer against the new release before
      concluding — **done** (that is exactly the freshness report; per discussion_handling.md
      "Issues we report", terminal event is a verified fix, satisfied here).
- [ ] Resolution notes posted on #57132 and #15921 (drafts ready; operator approval pending),
      each stamped; #15921 note scoped to native-CLI only (VS Code extension symptom NOT
      claimed fixed).
- [ ] Task closes on a "fixed independently upstream" outcome — recorded in `## Work
      Completed`, with all three rows concluded in DISCUSSIONS.md.

## Status Notes

- **2026-07-12 — freshness check delegated.** The operator has permission-probe re-running the
  verification against the current claude-code release (suspicion: the permission matcher was
  overhauled — a recent `claude doctor` run had to fix MCP wildcard permission settings).
  permission-probe will report results back via this repo's INSTRUCTIONS.md intake. The
  reopen-vs-consolidate decision (and any upstream post) is **on hold** until that report
  lands. If the bugs are fixed: verify which release fixed them, then conclude all three
  threads (post a resolution note on #57132/#15921 so followers know, per the operator's
  call) and close this task on a "fixed independently upstream" outcome.

- **2026-07-12 — freshness report received; both bugs FIXED upstream.** permission-probe
  verified on `claude.exe` 2.1.207 (native CLI, isolated `CLAUDE_CONFIG_DIR` sandbox):
  **Bug 1** (`XIq` matcher) — path-globbed allow rules now match (`permissionDecisionMs=3`,
  no-rule control blocked), deny rules override bare allows; confirmed in both `--print`/SDK
  and the interactive TUI. The old `ruleContent`-reject line is *still in the 2.1.207 binary*
  — upstream added a separate content-matching path rather than removing the filter.
  **Bug 2** (`bypassPermissions` gate) — `defaultMode: bypassPermissions` in settings.json
  now activates (caveat: sandbox had `bypassPermissionsModeAccepted: true` pre-seeded, so
  first-time activation may still need the warning-dialog acknowledgment). Bonus: the
  TUI-vs-`--print` MCP-allow divergence (permission-probe ISSUE-0004) also fixed. Fix version
  unknown — silent, no maintainer comment on any tracked thread. **Disposition:** reopen-vs-
  consolidate is moot; conclude all three threads via resolution notes. Drafts at
  `tasks/working_artifacts/ISSUE-0002/resolution-notes-2026-07-12.md` (#57132 + #15921;
  #15921 scoped native-CLI-only, VS Code extension Bash symptom explicitly not claimed).
  **#36884** is closed/not_planned — an optional third note there is low-visibility; skipping
  unless the operator wants it. Awaiting operator approval to post; on approval, stamp drafts,
  flip rows to a concluded state, fill `## Work Completed`, and close as "fixed independently
  upstream".

## Implementation Notes

- `gh` CLI authed as `twbarnes1972`; full path on this workstation:
  `& "C:\Program Files\GitHub CLI\gh.exe"`.
- Outward-facing posts (reopen request, consolidation comment) need operator approval first.
- The as-posted comment URLs above were recovered via the API on 2026-07-12; the draft files in
  permission-probe were never stamped — if convenient during any future permission-probe
  session, stamp them there (not this repo's deliverable).

## Related

- Hand-off source: `permission-probe/tasks/closed/ISSUE-0001.md` (full characterization,
  acceptance history) and `permission-probe/tasks/working_artifacts/ISSUE-0001/`
  (INVESTIGATION.md, upstream-comment drafts).
- Published workaround: https://github.com/twbarnes1972/permission-probe
  (`file-deny-guard.py` PreToolUse hook, `probe.js` picomatch probe).
- Upstream threads: anthropics/claude-code#36884 (closed), #57132, #15921.
- Sibling engagement pattern: [ISSUE-0001](./ISSUE-0001.md) (SQLAlchemy #13428).

<!-- version: v2026.07.12.03 -->
