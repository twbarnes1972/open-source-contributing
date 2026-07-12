# CLAUDE.md

Durable operational facts for this repo. See [README.md](./README.md) for what the project is
and [SESSIONLOOP.md](./SESSIONLOOP.md) for session start/end procedure.

## What this repo does

Manages open source contributions on GitHub — upstream issues, discussions, and PRs — from
first finding to merged/resolved outcome. Findings are usually **handed off from other repos**
already characterized (root cause + repro); this repo owns the upstream conversation, not the
original investigation. Full lifecycle in the README.

## GitHub identity & tooling

- **All upstream activity is posted as `twbarnes1972`.**
- **`gh` CLI is installed but NOT on this session's PATH.** Invoke via full path:
  `& "C:\Program Files\GitHub CLI\gh.exe"` (PowerShell) or `"/c/Program Files/GitHub CLI/gh.exe"`
  (bash). Authed as `twbarnes1972` (keyring), scopes `repo`, `read:org`, `gist`.
- **Posting is outward-facing** — draft in `tasks/working_artifacts/<task>/`, get operator
  approval, then post and stamp the draft with the posted URL. Re-check the thread for new
  activity immediately before posting.
- GitHub discussions need the **GraphQL API** (`gh api graphql`), not REST. Issue/PR comments
  use REST (`gh api repos/OWNER/REPO/issues/N/comments`).

## Discussion registry

[DISCUSSIONS.md](./DISCUSSIONS.md) is the monitoring index of live upstream threads (one row
per thread, depth lives in the owning task). Checked every session start; concluded rows sweep
to `tasks/working_artifacts/discussion-archive/`. Lifecycle in
[tasks/discussion_handling.md](./tasks/discussion_handling.md). Multi-thread engagements = one
task, many rows. A row concludes only on a **verified** outcome, not a maintainer claim.

## Per-project upstream notes

- **SQLAlchemy uses Gerrit** (`gerrit.sqlalchemy.org`), not GitHub PRs — GitHub is a read-only
  mirror. Offer patches "via Gerrit"; a change is one squashed commit + a `Change-Id` trailer.
- **Local clones for active engagements:** `C:\Data\open-source\sqlalchemy` (branch
  `issue-13428-staticpool-lost-commits` holds the ISSUE-0001 fix work, off `main` @ `07e2c9f4e`).

## Task system

Standard stackagentic-library scaffold (task-manager). Categories in
[tasks/categories.md](./tasks/categories.md); upstream engagements currently use the `ISSUE`
prefix. This repo is now a git repo (remote `origin` = `git@github.com:twbarnes1972/open-source-contributing.git`,
default branch `main`), so task-manager root detection works from any subdirectory.
