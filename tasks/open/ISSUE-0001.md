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

## Status Notes

- **2026-07-12 — maintainer direction (first reply).**
  [CaselIT replied](https://github.com/sqlalchemy/sqlalchemy/discussions/13428#discussioncomment-17614458)
  (same maintainer who suspected StaticPool in 2021's #6987): *"I guess the docs could do a
  better job here, but ultimately I'm not sure this can behave any differently unless we were
  to enforce a single checked out connection at a time, using an AssertionPool or similar."*
  Read: **docs warning — receptive; behavioral guard — skeptical** (hard exclusivity is the
  only mechanism he sees, and it would break legitimate usage), matching this task's
  Implementation Notes prediction. Next move: confirm a Gerrit docs patch would be accepted,
  gently probe whether a warn-not-raise middle ground is worth anything, and mention
  AssertionPool visibility for test suites. Reply drafted at
  `tasks/working_artifacts/ISSUE-0001/reply-draft-13428-2026-07-12.md` — awaiting operator
  approval before posting.

- **2026-07-12 — both fix tracks implemented and validated locally** (operator directive: no
  untested suggestions upstream). Branch `issue-13428-staticpool-lost-commits` on the local
  clone (off `main` @ `07e2c9f4e`), 2 commits, 277 insertions, all relevant suites green.
  **Track A** — StaticPool interleave warning (checkout-time + reset-time, driver
  `in_transaction`-keyed, zero false positives across their pool/engine/asyncio suites;
  warning-only). Coverage finding: engine-layer rollbacks are invisible to the pool, so
  detection is inherently partial — disclosed in the draft. **Track B** — the memdb VFS URL
  form (`sqlite:///file:/name?vfs=memdb&uri=true`) **already works on main**, giving each
  session its own connection: repro's lost row survives, contention is loud. Footguns
  (leading slash, no WAL, lifetime, 3.36+) documented in new pysqlite/aiosqlite docs
  sections + tests + changelog. Full detail:
  `tasks/working_artifacts/ISSUE-0001/validation-results-2026-07-12.md`. Reply draft
  rewritten (v2, evidence-based) — offers docs and/or warning via Gerrit; awaiting operator
  approval to post.

- **2026-07-12 — zzzeek engaged; docs rewrite in flight; cache=shared claim corrected.**
  [zzzeek posted twice](https://github.com/sqlalchemy/sqlalchemy/discussions/13428#discussioncomment-17615242):
  recommends `file::memory:?cache=shared&uri=true` + QueuePool/NullPool, and confirms the
  decade-old memory-db docs section is being rewritten now ("im having claude rewrite it
  now"). Validated his recipe against the repro: **no silent loss** (sync + aiosqlite; loud
  immediate `database table is locked` on contention). Reconciled our original post's
  "cache=shared also loses rows" claim — it was a **URL-spelling artifact**: the
  `mode=memory&cache=shared` spelling trips `_is_url_file_db()`'s mode check → single-
  connection pool (StaticPool/SingletonThreadPool) → same loss; forced QueuePool on the
  identical URL → no loss. The loss follows the pool in every configuration. Reply draft
  **v3** corrects our claim publicly, feeds validated cache=shared + memdb data (incl. the
  spelling gotcha and a possible `_is_url_file_db` improvement) to the in-flight rewrite,
  and answers CaselIT on the detection prototype. **Time-sensitive** — the rewrite is
  happening now; awaiting operator approval to post.

- **2026-07-12 — reply v3 POSTED** (operator-approved):
  [discussioncomment-17615486](https://github.com/sqlalchemy/sqlalchemy/discussions/13428#discussioncomment-17615486)
  (22:07Z). State → waiting-on-maintainer. Next expected: docs rewrite lands, a Gerrit
  invitation for docs/warning/classification fix, or follow-up questions. Maintainer
  direction criterion effectively satisfied (docs: yes — rewrite underway; guard: prototype
  offered, no commitment sought).

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

<!-- version: v2026.07.12.04 -->
