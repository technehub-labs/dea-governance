# CR-019: Org-Wide Directory-Size Audit (Reconciler R5)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-10
**Admission authority**: register notes repair only (register_version 9 -> 10; no observational field changed)
**Depends on**: CR-014 (the reconciler and its weekly CI); CR-CATALOG-STRUCT-11 in dea-metaframework (the PR-time counterpart, CST-017)
**Companion**: entity-storage-layout.md §4 v1.1.0 (dea-metaframework), CR-MET-024 (dea-catalog-metrics; the sharding remedy both gates name)

## 1. Problem Statement

The ratified storage contract pins the numbers (entity-storage-layout.md §1/§4: GitHub truncates a directory listing at 1,000 entries; shard before any directory approaches 800) but, outside `dea-catalog-metrics`' own layout guard, nothing enforces them anywhere in the org, and nothing watches the org weekly. The owner directed (2026-11-09) an org-wide audit and enforcement scheme: when any repo develops a directory nearing the cap, the metrics-sharding / processes-containment approach is employed. The metaframework half of that scheme (CST-017, per-repo PR-time enforcement) is CR-CATALOG-STRUCT-11; it only reaches a repo when that repo re-syncs its toolchain pin. The org-level half needs to cover every registered repo regardless of pin state, on a schedule.

## 2. Objective

Add rule R5 (directory-size audit) to the portfolio reconciler, so the weekly `reconcile-portfolio` run censuses every directory of every registered repo and fails on any directory at or over the 800-entry shard trigger.

## 3. The Rule

| Rule | Check |
|---|---|
| R5 directory-size | for each registered repo, the recursive git tree of `main` yields an immediate-entry count per directory (files + subdirectories, exactly what a GitHub listing shows); a directory at or over 800 entries is a FAIL finding; 500+ entries print a non-failing watch line so a fast-growing intake surfaces early |

Design decisions, mirroring the reconciler's existing conventions:

- **Register-driven scope**: R5 runs for every registered repo that R2 finds existing and non-missing. It runs *before* the index read, so bespoke-index repos (metrics, roles) are audited too; their R3 state exemption does not exempt their directory sizes.
- **Tracked content only**: the git tree is the tracked content, so local-only noise (an untracked `.venv`) can never fire the rule.
- **No finding on incomplete data**: a truncated tree payload prints a WARN and skips the repo for R5 (the CR-014 transport rule).
- **Thresholds are the ratified ones**: 800 = the §4 shard trigger (the same constant as `dea-catalog-metrics/tests/test_layout.py` and CST-017); 500 = the watch tier. Neither is configurable per repo.
- **Remedy named in the finding**: the CR-MET-024 recipe (first-letter shard, ids unchanged), so the failure message carries its own fix.

`.github/workflows/reconcile-portfolio.yml` step name now enumerates R1..R5; schedule unchanged.

## 4. Counting Semantics and the Pre-Merge Regression

The trees API lists subdirectories as explicit `tree` objects. The first implementation counted those objects into their parents and derived directories from path prefixes, double-counting every directory (a 536-entry directory reported 1,071; a 604-entry shard reported 1,207). Caught by comparing the first live run against the local clone census before anything shipped. The counting now lives in a pure function, `_entry_counts_from_tree_entries()`: blobs contribute one entry to their parent; directories are derived once from path prefixes; explicit `tree` objects are not counted again; submodule entries (type commit) are skipped (no catalog repo uses them). Unit tests pin the semantics in `registers/test_reconcile_directory_counts.py` (the reconciler's first unit tests), run by a new `reconciler-units` job in `ci.yml`.

## 5. First-Run Observations (2026-11-10, live)

R5 verified against the live org before landing (reconciler run with a real token):

| Repo | Directory | Entries | Verdict |
|---|---|---|---|
| dea-catalog-roles | entities/v1-alpha | 1,252 | **FAIL finding at landing** (over GitHub's 1,000 cap; flat corpus, bespoke index) |
| dea-catalog-digital-business-service-factory | entities/v1-alpha | 536 | watch |
| dea-catalog-digital-business-service-factory | contributions/queue | 518 | watch |
| dea-catalog-metrics | entities/v1-alpha/c | 604 | watch |

R1..R4 produced no findings in the same run. Remediation carriers: business-services sharding (its own repo CR, in flight), metrics shard-c subdivide (its repo CR; its local 800-guard will trip first), roles sharding (its repo CR; bespoke corpus). Until those land, the weekly job carries the roles finding: that is the gate working, not a defect.

## 6. Files

- `registers/reconcile_portfolio.py`: R5 constants, `_entry_counts_from_tree_entries()`, `_directory_entry_counts()`, the R5 branch in the online loop, docstring rule table.
- `registers/test_reconcile_directory_counts.py`: new; census semantics unit tests (listing semantics; no-double-count regression).
- `.github/workflows/reconcile-portfolio.yml`: step name enumerates R5.
- `.github/workflows/ci.yml`: new `reconciler-units` job.
- `registers/catalog-portfolio.yaml`: `register_version` 9 -> 10, `snapshot_date` -> 2026-11-10; the metrics entry's stale "root-position records" clause (named as a follow-up by CR-MET-024's NOT-list) repaired, with the repair dated in place. No observational field changed.

## 7. Acceptance Criteria

1. `registers/test_reconcile_directory_counts.py` passes (2 tests), and the `reconciler-units` CI job runs it.
2. A live reconciler run censuses all 44 registered repos and reports exactly the §5 table: 1 R5 finding (roles), 3 watch lines; R1..R4 findings unchanged from their pre-CR state (0 in the 2026-11-10 run).
3. A truncated-tree payload for any repo produces `WARN: R5 skipped for <repo> (...)` and no finding.
4. Offline mode (no token) unchanged: R1/R4 enforced, R2/R3/R5 skipped with the warning.

## 8. NOT-List

- **No new workflow**: R5 rides the existing weekly `reconcile-portfolio` schedule.
- **No per-repo threshold configuration**: the thresholds are the ratified §4 numbers.
- **No register re-snapshot**: the observational fields are untouched; version bump covers the notes repair only.
- **No remediation in this repo**: sharding lands in the repos that own the hot directories.
- **No issue/comment bot**: enforcement remains the failed scheduled job (CR-014 convention).
