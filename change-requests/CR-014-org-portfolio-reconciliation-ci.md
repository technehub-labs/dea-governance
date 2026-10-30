# CR-014: Org-Level Portfolio Reconciliation CI

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-02
**Admission authority**: yes (register refresh)
**Depends on**: CR-013 (the register); CR-CATALOG-STRUCT-10 (dea-metaframework; the programme this CI guards)
**Companion**: metamodel CR-MET-014 (the manual audit this CI makes continuous)

## 1. Problem Statement

CR-013 established the catalog-portfolio register with a manual audit snapshot (2026-10-30). Nothing reconciles it continuously: the metamodel's `catalog_repo` allocations, the register, and GitHub reality can drift independently. The audit itself proved the need: the first run of the reconciler (2026-11-02) found `dea-catalog-processes` populated with 3,722 canonical records where the two-day-old snapshot recorded skeleton (0) — real drift, detected within 48 hours of the snapshot being taken. The governance repository also has no CI of any kind.

## 2. Objective

Make the portfolio register continuously reconciled (org-level CI), and give dea-governance a basic repository CI (parse + authorship).

## 3. The Reconciler

`registers/reconcile_portfolio.py` (stdlib + pyyaml; token-gated GitHub reads, no clones):

| Rule | Check |
|---|---|
| R1 completeness | every metamodel `catalog_repo` value appears in the register (the CR-013 maintenance rule) |
| R2 existence | registered repos exist; `missing`-registered repos are actually absent |
| R3 state truth | registered state matches observed `CATALOG.yaml` counts (populated requires canonical > 0; skeleton requires canonical == 0) |
| R4 ownership | every metamodel entity allocated to a registered repo appears in that repo's register entry |

`.github/workflows/reconcile-portfolio.yml` runs it weekly (cron), on demand, and on register changes, failing on findings. Offline mode (no token) still enforces R1/R4.

## 4. Repository CI

`.github/workflows/ci.yml`: a parse job over all tracked YAML, and the authorship cardinal-rule gate vendored at run time from dea-metaframework v2.6.0 (the same pinned pattern every catalog uses).

## 5. Register refresh riding this CR

The processes entry is refreshed to observed reality (populated, 3,722 canonical; register_version 2, snapshot 2026-11-02) — the drift the reconciler's first run detected. The business-processes naming question (which of `dea-catalog-processes` / `dea-catalog-business-processes` is the canonical home) remains a named follow-up; the register records both facts.

## 6. NOT-list

1. No CR-012 normative requirement changes.
2. No metamodel content changes (the BusinessProcess lifecycle correction belongs to the metamodel's wave-boundary CR).
3. No per-catalog CI changes; the reconciler reads, never writes.

## 7. Definition of Done

1. `reconcile_portfolio.py` exits 0 against the refreshed register with a token, and exercises R1-R4.
2. Both workflows valid; parse + authorship pass on this repository's content.
3. Register row and CHANGELOG entry landed in this PR.
