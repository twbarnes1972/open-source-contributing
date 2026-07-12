# ISSUE-0001: SQLAlchemy StaticPool silent lost-commits — own upstream discussion #13428, drive potential fix

**Created:** 2026-07-12
**Status:** Open
**Priority:** Medium
**Category:** Issue tracking
**Workstream:** Active build
**Owner:** agent

---

## Summary

Own the open-source-facing half of a silent-data-loss finding in SQLAlchemy, handed off from
agent-email-tool (their ISSUE-0018; repo-local remediation already done there). The finding is
posted upstream as https://github.com/sqlalchemy/sqlalchemy/discussions/13428 (account
`twbarnes1972`, posted 2026-07-12). This task covers: monitoring and engaging that discussion,
and — if maintainers are receptive — driving an upstream change (concurrent-checkout guard in
`StaticPool` and/or prominent docs warnings).

## Background

SQLAlchemy auto-selects `StaticPool` for in-memory SQLite URLs (`sqlite+aiosqlite://`,
`.../:memory:`) — one shared DBAPI connection handed to every checkout with no exclusivity.
Concurrently-open sessions (one session per asyncio task — the *recommended* pattern)
interleave transaction demarcations on that single connection. Driver-independent (repros with
sync pysqlite + explicit StaticPool) and version-independent (SQLA 2.0.50/2.0.51 ×
aiosqlite 0.19.0/0.22.1, Py 3.14.5). `cache=shared` named-memory URIs also lose rows; only
file-backed SQLite is safe.

Discussion #13428 was posted as the root-cause answer to SQLAlchemy's **unresolved 2021
discussion #6987** (same symptom; maintainer CaselIT had suspected "something funny going on
with the StaticPool" but no mechanism was ever identified).

## Steps to Reproduce

1. Create an in-memory SQLite engine (`sqlite+aiosqlite:///:memory:` or sync `:memory:` with
   explicit `StaticPool`).
2. Open two sessions concurrently (e.g. one per asyncio task).
3. Session A inserts a row (flushed, not yet committed); session B (read-only) closes,
   emitting its close-`ROLLBACK` on the shared connection.
4. Session A commits.

Minimal generic repro (sync + async variants):
`agent-email-tool/tasks/working_artifacts/issue-0018-aiosqlite-staticpool/repro_staticpool.py`;
config/version matrix runner in the same directory (`matrix.py`).

## Expected vs Actual Behavior

- **Expected:** session A's committed row persists — or, at minimum, an error/warning that two
  sessions are sharing one connection's transaction state.
- **Actual:** session B's close-`ROLLBACK` silently discards session A's flushed-but-uncommitted
  INSERT; A's later `COMMIT` commits nothing. No error, warning, or log at any layer.

## Root Cause

`StaticPool` (`lib/sqlalchemy/pool/impl.py:452`) memoizes a single `_ConnectionRecord` and
returns it to every checkout with no concurrency tracking, while
`get_pool_class` (`lib/sqlalchemy/dialects/sqlite/aiosqlite.py:294`) silently auto-selects it
for `:memory:` URLs. Concurrent checkouts therefore share one live transaction scope.

## Dependencies

| Blocked By | None |

Sequencing (not a blocker): patch work should wait for maintainer reaction on #13428 —
SQLAlchemy has strong opinions on pool internals and will usually sketch the acceptable shape.

## Acceptance Criteria

- [ ] Discussion #13428 checked for maintainer activity at each session start while this task
      is open; substantive replies answered promptly (gh CLI, account `twbarnes1972`).
- [ ] Maintainer direction established and recorded here: guard, docs warning, both, or
      wontfix/infeasible with rationale.
- [ ] If maintainers endorse a docs warning: patch prepared on the local clone covering
      `aiosqlite.py` docs (~line 66), `pysqlite.py` docs blocks (lines 268–304), and the
      `StaticPool` docstring — and submitted via SQLAlchemy's Gerrit flow.
- [ ] If maintainers endorse a checkout guard: design confirmed against their sketched shape
      before implementation in `pool/impl.py`, then submitted via Gerrit.
- [ ] Task closes on a real outcome — change merged, fixed independently upstream, rejected
      with rationale, or consciously abandoned — recorded in `## Work Completed`.
- [ ] If a fix or docs change lands, a resolution pointer is posted back to the original 2021
      discussion #6987.

## Implementation Notes

- **First action each session: check #13428 for replies.** `gh` CLI is installed and OAuth'd
  as `twbarnes1972` on this workstation (`gh api`, keyring token) — checking/replying is
  scriptable.
- **Local clone ready:** `C:\Data\open-source\sqlalchemy`
  (git@github.com:sqlalchemy/sqlalchemy.git, `main` @ `07e2c9f4e`, cloned 2026-07-12).
- **Fix surfaces surveyed on that clone:**
  - `lib/sqlalchemy/pool/impl.py:452` — `StaticPool`; a concurrent-checkout guard
    (detect second simultaneous checkout of the sole record → raise/warn) would live here.
    Its docstring advertises asyncio compatibility with no concurrency caveat.
  - `lib/sqlalchemy/dialects/sqlite/aiosqlite.py:294` — `get_pool_class` auto-selection;
    docs text at line 66 (docs-warning target #1).
  - `lib/sqlalchemy/dialects/sqlite/pysqlite.py:268–304` — sync-side docs recommending
    StaticPool for memory DBs (docs-warning target #2).
- **Contribution flow:** SQLAlchemy uses **Gerrit** (per their CONTRIBUTING), not GitHub PRs.
- A guard may be infeasible if brief session overlap on a StaticPool without transaction
  collision is legitimate — expect maintainers to raise this; don't argue past it.
- Knock-on remediation in py-cog (test fixtures) was handed to that repo directly
  (2026-07-12) — **not this task's concern**; listed to avoid duplicate outreach.

## Related

- Upstream: https://github.com/sqlalchemy/sqlalchemy/discussions/13428 (ours, live) and
  https://github.com/sqlalchemy/sqlalchemy/discussions/6987 (2021, unresolved, same symptom).
- Evidence (in agent-email-tool): `tasks/closed/ISSUE-0018.md` (full characterization,
  config/version matrix, decisions); `tasks/closed/ISSUE-0017.md` (original symptom);
  `tasks/working_artifacts/issue-0018-aiosqlite-staticpool/` (repro, matrix runner,
  as-posted upstream draft stamped with the URL).

<!-- version: v2026.07.12.01 -->
