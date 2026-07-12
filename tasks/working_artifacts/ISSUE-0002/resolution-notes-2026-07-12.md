<!--
Resolution-note drafts for the claude-code permission-matcher engagement (ISSUE-0002).
Source: permission-probe freshness report (both bugs FIXED, verified 2026-07-12 on
claude.exe 2.1.207 native CLI). Post as: twbarnes1972.
Status: POSTED 2026-07-12 as twbarnes1972 (operator-approved).
  Draft A → https://github.com/anthropics/claude-code/issues/57132#issuecomment-4953010768
  Draft B → https://github.com/anthropics/claude-code/issues/15921#issuecomment-4953010807

Scope discipline (from the report): our verification covers the NATIVE CLI only. #15921's
OP symptom (Bash rules ignored in the VS Code *extension*) was never root-caused by us and is
NOT claimed fixed. Notes claim only what was verified.

Post targets: #57132 (open, our natural primary thread) and #15921 (open, multi-bug).
#36884 is closed/not_planned — optional third note (see ISSUE-0002); low visibility.
-->

## Draft A — for #57132 (open)

https://github.com/anthropics/claude-code/issues/57132

---

Following up: this appears **fixed** in current Claude Code. I re-ran the reproducer from my
earlier comment against the native CLI (`claude.exe` 2.1.207, Windows) in an isolated config
sandbox, and path-globbed allow rules under `~/.claude/` now match at runtime — an
`Edit(<glob>)` allow that previously showed as loaded but never matched is now honored
(allowed, no prompt), with a no-rule control still correctly blocked. Path-globbed deny rules
also take effect now.

I don't know exactly which release fixed it — it landed somewhere between 2.1.145 and 2.1.207
with no changelog note I could find — so if you're on an older build an upgrade is the fix.
For reference, the underlying matcher change appears to be an added content-matching path
rather than removal of the old reject filter (the original `ruleContent`-reject line is still
in the 2.1.207 binary), which is consistent with the behavior now working while the old code
path remains.

Verification was native-CLI only; I didn't test the VS Code extension surface.

## Draft B — for #15921 (open)

https://github.com/anthropics/claude-code/issues/15921

---

Update on the two matcher bugs I reported here earlier: both are **fixed** in the current
native CLI (`claude.exe` 2.1.207, Windows), verified with a reproducer in an isolated config
sandbox.

- Path-globbed `Read`/`Edit`/`Write`(and related) allow **and** deny rules now match (they
  were previously silent no-ops).
- `"defaultMode": "bypassPermissions"` in `settings.json` now activates the mode instead of
  being silently rejected. (One caveat: my sandbox had already accepted the bypass-mode
  warning dialog once, so first-time activation may still require that acknowledgment — I
  couldn't isolate that variable.)

The fix landed silently somewhere between 2.1.145 and 2.1.207, so upgrading is the remedy if
you're on an older build.

**Scope:** I verified the **native CLI only.** This thread's original report is about
`Bash`/`Write`/`Edit` rules being ignored specifically in the **VS Code extension** — I did
not root-cause or test that surface, and I'm **not** claiming it's fixed. Anyone still seeing
the extension-specific behavior should treat that as open and worth a fresh reproduction on
the current extension build.
