
# Instructions

---
**Related:**
- [Instruction Handling Workflow](./instruction_handling.md) -- How to process items in this document
- [Task Management](./task_management.md) -- Instructions for Managing Tasks

---

## Items

### 2026-07-12 — SQLAlchemy: StaticPool silent lost-commits — own the discussion + potential upstream fix (hand-off from agent-email-tool ISSUE-0018)

**What this is:** agent-email-tool found, root-caused, and reported upstream a
silent-data-loss behavior in SQLAlchemy; the repo-local remediation is done there. This item
hands the *open-source-facing* half to this repo: monitor/engage the discussion, and drive a
potential upstream patch if maintainers are receptive.

**The finding (fully characterized):** SQLAlchemy auto-selects `StaticPool` for in-memory
SQLite URLs (`sqlite+aiosqlite://`, `.../:memory:`) — one shared DBAPI connection handed to
every checkout with no exclusivity. Concurrently-open sessions (one session per asyncio
task, the *recommended* pattern) interleave their transaction demarcations on that single
connection: a read session's close-`ROLLBACK` silently discards another session's
flushed-but-uncommitted INSERT; the later `COMMIT` commits nothing. No error/warning/log at
any layer. Driver-independent (repros with sync pysqlite + explicit StaticPool — aiosqlite
exonerated) and version-independent (SQLA 2.0.50/2.0.51 × aiosqlite 0.19.0/0.22.1, Py
3.14.5). `cache=shared` named-memory URIs also lose rows; only file-backed is safe.

**Live upstream thread (posted 2026-07-12, account twbarnes1972):**
https://github.com/sqlalchemy/sqlalchemy/discussions/13428 ("Usage Questions") — posted as
the root-cause answer to their **unresolved 2021 discussion #6987** (same symptom;
maintainer CaselIT had suspected "something funny going on with the StaticPool" but no
mechanism was ever identified). Asks for either a concurrent-checkout guard or a prominent
docs warning. **First action for this repo: watch for maintainer replies and engage** — gh
CLI is installed + OAuth'd as twbarnes1972 on this workstation (`gh api`, keyring token), so
checking/replying is scriptable.

**Local clone ready:** `C:\Data\open-source\sqlalchemy` (git@github.com:sqlalchemy/sqlalchemy.git,
`main` @ `07e2c9f4e`, cloned 2026-07-12).

**Lay of the land for a fix (surveyed on that clone):**
- `lib/sqlalchemy/pool/impl.py:452` — `StaticPool` itself. Minimal: a memoized single
  `_ConnectionRecord` returned to every checkout, no concurrency tracking. Its docstring
  advertises asyncio compatibility with no concurrency caveat (same gap as the docs). A
  **concurrent-checkout guard** (detect a second simultaneous checkout of the sole record →
  raise/warn) would live here.
- `lib/sqlalchemy/dialects/sqlite/aiosqlite.py:294` — `get_pool_class` auto-selecting
  StaticPool for `:memory:` URLs (the silent default that makes innocent users hit this);
  its docs text at line 66. **Docs warning** target #1.
- `lib/sqlalchemy/dialects/sqlite/pysqlite.py:268–304` — sync-side docs blocks recommending
  StaticPool for memory DBs. **Docs warning** target #2 (plus the StaticPool docstring).
- Sequencing advice: wait for maintainer reaction on #13428 before investing in a patch —
  SQLAlchemy has strong opinions on pool internals and will usually sketch the acceptable
  shape (or explain why a guard is infeasible, e.g. legitimate brief session overlap on a
  StaticPool without transaction collision). Contribution flow note: SQLAlchemy uses
  **Gerrit** for changes (their CONTRIBUTING describes it), not GitHub PRs.

**Evidence artifacts (in agent-email-tool):**
- `tasks/closed/ISSUE-0018.md` — full characterization, config/version matrix, decisions.
- `tasks/closed/ISSUE-0017.md` — where the symptom was first hit (live triage race).
- `tasks/working_artifacts/issue-0018-aiosqlite-staticpool/` — `repro_staticpool.py`
  (minimal generic repro, sync + async variants), `matrix.py` (config/version matrix
  runner), `upstream-sqlalchemy-issue-draft.md` (as-posted text, stamped with the URL).
- Related knock-on: py-cog was handed the test-fixture remediation via its own
  INSTRUCTIONS.md intake (2026-07-12) — not this repo's concern, listed to avoid duplicate
  outreach.

---

## Processing

| # | Item | Task ID | Status |
|---|------|---------|--------|

---

## Completed



---
