# ISSUE-0001 — implementation & validation results (2026-07-12)

Work done on local clone `C:\Data\open-source\sqlalchemy`, branch
`issue-13428-staticpool-lost-commits` (off `main` @ `07e2c9f4e`), editable install in
`.venv`, SQLAlchemy 2.1.0b4, SQLite 3.50.4, Python 3.14.

## Baseline

`repro_staticpool.py` (agent-email-tool artifact) against clean `main`: silent loss
reproduces in both variants (sync StaticPool and default aiosqlite `:memory:`) — 0 rows
where 1 committed, no error anywhere.

## Track A — StaticPool interleave warning (commit `cee185174`)

- `pool/impl.py`: StaticPool gains a live-checkout counter and two zero-false-positive
  detection points, keyed on driver `in_transaction` (sqlite3 direct; async adapters via
  `driver_connection`):
  - **checkout-time** (`_do_get`): sole connection checked out while a transaction begun via
    an earlier still-open checkout is in progress.
  - **reset-time** (per-instance `reset` event listener, record-identity-guarded against
    `recreate()` dispatch propagation): pool rollback-on-return about to discard an
    in-progress transaction while other checkouts remain open.
- Verified: warning fires in the repro (sync), in deterministic writer-first async, and at
  the destructive pool rollback for raw-connection checkin. Warning-only — loss still
  occurs; no behavior change.
- **Coverage finding**: rollbacks issued at the engine layer (e.g. `Session.rollback()`,
  session close resetting its own transaction) happen before the pool sees the connection,
  with `transaction_was_reset=True` suppressing the pool-level rollback — so pool-level
  detection is inherently partial (canonical orderings caught; reverse ordering with the
  destructive rollback at engine level is invisible to the pool). Full detection would need
  the dialect `do_rollback` choke point, where transaction ownership is ill-defined. This
  strengthens the memdb/docs position.
- Tests: 5 new cases in `test/engine/test_pool.py::StaticPoolTest` (2 positive, 3 negative).
  Suites green: `test/engine/test_pool.py` 133+new, `test/engine/` + `test/ext/asyncio/`
  845 passed / 186 skipped (warnings are errors in their test config → suite-wide
  no-false-positive evidence). One suite fix along the way: the counter lock is class-level
  so `test_recreate_state`'s `__dict__` comparison still holds.

## Track B — memdb VFS (commit `f570a1c7d`)

- **Discovery: no code change needed.** `sqlite:///file:/name?vfs=memdb&uri=true` already
  works end-to-end on `main` — `_is_url_file_db()` classifies it as a file DB (database
  value ≠ `:memory:`, mode ≠ memory) → QueuePool / AsyncAdaptedQueuePool → one real
  connection per checkout, one shared in-memory database.
- **Footguns found (now documented):**
  - Name must begin with `/` (`file:/name`); relative names give each connection a private
    DB — my first probe false-positived because QueuePool handed back the same pooled
    connection.
  - No WAL on memdb: a pending write blocks *readers* on other connections →
    `database is locked` after `timeout`. Correct-but-serialized vs StaticPool's
    concurrent-but-silently-unsafe.
  - DB lifetime = at least one open connection; `engine.dispose()` discards it.
  - Requires SQLite ≥ 3.36.
- `memdb_validation.py` (alongside this file): repro ordering → committed row SURVIVES
  (1 vs 0 on StaticPool), interference loud; async concurrent writer/reader → row survives;
  concurrent writers → loud lock error. All pass.
- Deliverables: pysqlite docs (StaticPool shared-state warning + new
  `Sharing a Memory Database Across Connections (memdb)` section, anchor `pysqlite_memdb`),
  aiosqlite pooling-behavior warning cross-linking it, StaticPool docstring warning
  (in Track A commit), changelog `unreleased_21/13428.rst`, 2 new dialect tests
  (pool classification + two-connection sharing round-trip, version-gated).
  `test/dialect/sqlite/` + `test/engine/test_pool.py`: 405 passed.

## Branch summary

```
f570a1c7d Document memdb VFS sharing; test StaticPool interleave warnings
cee185174 Warn on interleaved transaction use of StaticPool's single connection
  6 files changed, 277 insertions(+), 1 deletion(-)
```

Reply draft v2 (evidence-based) in `reply-draft-13428-2026-07-12.md` — offers docs and/or
warning via Gerrit, discloses the pool-level detection coverage limit.
