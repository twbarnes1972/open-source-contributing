# Discussions

Registry of upstream threads (GitHub discussions, issues, PRs) we are engaged in — the
monitoring layer for open source contributions. Each row is a live engagement; the *depth*
(context, evidence, next steps, outcome) lives in the row's **owning task**, never here.

**This file is a queue, not a log.** It holds only current engagements plus a small staging
section of recent conclusions. Concluded rows are periodically offloaded to
`tasks/working_artifacts/discussion-archive/` per
[tasks/discussion_handling.md](./tasks/discussion_handling.md), which also defines the row
format, states, and the session-start check-in routine.

---

## Active

| Thread | Repo | Kind | Task | State | Last checked | Next action |
|--------|------|------|------|-------|--------------|-------------|
| [#13428](https://github.com/sqlalchemy/sqlalchemy/discussions/13428) | sqlalchemy/sqlalchemy | Discussion | [ISSUE-0001](./tasks/open/ISSUE-0001.md) | waiting-on-maintainer | 2026-07-12 | [Reply v3 posted](https://github.com/sqlalchemy/sqlalchemy/discussions/13428#discussioncomment-17615486) 22:07Z; [zzzeek demo scripts](https://github.com/sqlalchemy/sqlalchemy/discussions/13428#discussioncomment-17615506) crossed at 22:09Z (his shared-cache demo shape verified non-discriminating — passes on StaticPool too; ours already posted the interleaved-shape data). Holding. Watch for: his read of our post, docs rewrite landing (check its examples exercise the interleaved shape), Gerrit invitation |
| [#36884](https://github.com/anthropics/claude-code/issues/36884) | anthropics/claude-code | Issue | [ISSUE-0002](./tasks/open/ISSUE-0002.md) | needs-our-reply | 2026-07-12 | Stale-closed 2026-07-07 ("not planned", never triaged) with our [root-cause comment](https://github.com/anthropics/claude-code/issues/36884#issuecomment-4474702923) on it — reopen-vs-consolidate **on hold**: permission-probe is re-verifying against the current release, report due via INSTRUCTIONS.md |
| [#57132](https://github.com/anthropics/claude-code/issues/57132) | anthropics/claude-code | Issue | [ISSUE-0002](./tasks/open/ISSUE-0002.md) | needs-our-reply | 2026-07-12 | Natural primary thread now — `hwaterer` (2026-06-10) points readers to our #36884 analysis; candidate target for consolidated root-cause post, **on hold** pending permission-probe re-verification |
| [#15921](https://github.com/anthropics/claude-code/issues/15921) | anthropics/claude-code | Issue | [ISSUE-0002](./tasks/open/ISSUE-0002.md) | waiting-on-maintainer | 2026-07-12 | Our [multi-bug comment](https://github.com/anthropics/claude-code/issues/15921#issuecomment-4474820813) posted 2026-05-18; latest activity is user venting, nothing owed — watch |

## Recently concluded

_Staging area — rows land here when their owning task closes, and are swept to a dated
archive artifact when this section crosses ~10 rows (see
[tasks/discussion_handling.md](./tasks/discussion_handling.md))._

| Thread | Repo | Task | Outcome | Concluded |
|--------|------|------|---------|-----------|
