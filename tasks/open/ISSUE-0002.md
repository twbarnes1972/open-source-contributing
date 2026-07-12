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

- [ ] Reopen-vs-consolidate decision made with the operator and recorded here: ask to reopen
      #36884, or move/summarize the root-cause analysis onto #57132 (now the natural primary
      thread) so it lives on an open issue.
- [ ] Before any new upstream post: freshness check — confirm the findings still reproduce on
      the current claude-code release (analysis targets 2.1.143.a06, posted 2026-05-18).
- [ ] Root-cause analysis ends up on (or linked prominently from) an open, maintainer-visible
      thread; surviving threads protected from silent stale-closure while un-triaged.
- [ ] All three DISCUSSIONS.md rows checked each session start; substantive replies engaged.
- [ ] If a fix ships: re-run the permission-probe reproducer matrix against the new release
      before concluding (per discussion_handling.md "Issues we report").
- [ ] Task closes on a real outcome — fix verified, rejected with rationale, or consciously
      abandoned — recorded in `## Work Completed`, with rows concluded in DISCUSSIONS.md.

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

<!-- version: v2026.07.12.01 -->
