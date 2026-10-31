# CR-016: Metrics Undercount Correction and Reconciler v2

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-31
**Admission authority**: yes (register refresh)
**Depends on**: CR-014 (the reconciler), CR-015 (the standing survey this CR corrects)
**Companion**: metamodel CR-MET-014 (whose audit undercounted metrics by the same defect) and CR-MET-013 (whose canonical Unit records are referenced by the metrics corpus this CR counts)

## 1. Problem Statement

The owner challenged CR-015's org-wide total (4,019 canonical records), stating the metrics catalog should carry over 6,000 entities and the org total should exceed 9,000. The investigation vindicated the challenge: `dea-catalog-metrics`'s CATALOG.yaml is **4 MB**, and the GitHub contents API returns no body for files over 1 MB — every index-based observation (the CR-MET-014 audit, the CR-015 survey, the reconciler) silently read it as empty. The corpus is **4,428 metric records** under a bespoke index schema. `dea-catalog-roles` carries the same schema family (1,252 records: 1 canonical, 1,242 proposed, 10 active). The org-wide record census is **9,699**, not 4,019.

## 2. Changes

1. **Reconciler v2** (`registers/reconcile_portfolio.py`): size-safe index reads (raw first — serves any size; git-blobs fallback); bespoke-schema handling — when the org counts block is absent, the filesystem census (entity YAML blob count from the same tree) supplies the canonical figure instead of reading a zero; unreadable indexes are findings, never silent zeros.
2. **Register v7**: metrics → populated, 4,428, `index: bespoke`, with the owner-index split recorded (5 admitted / 4,423 candidate); roles → bespoke flag with the 1,252-record corpus note; snapshot unchanged (2026-10-31).
3. **Standing-report addendum**: the correction table, the defect explanation, and the method lesson (a "0" from a large repository is a diagnosis, not an answer).

## 3. Consequences

- `dea:PerformanceMetric` lifecycle `existing` (metamodel CR-MET-014) is **vindicated** — the undercount that made it look stale was the same defect.
- The stale-`existing` family shrinks to BusinessService + SolutionComponent (dbsf: 18 candidates, 0 canonical — genuinely unadmitted).
- The reconciler now detects this defect class mechanically: rerunning it against the pre-v7 register produced exactly the metrics finding; against v7 it is clean.

## 4. NOT-list

1. No metrics or roles catalog content changes (owner-active repos).
2. No metamodel lifecycle changes (PerformanceMetric was already correct).
3. No claim that the bespoke indexes are contract-conformant — their adoption of the org index discipline remains the owners' follow-up.

## 5. Definition of Done

1. Reconciler v2 detects the pre-v7 register drift and is clean against v7.
2. Register v7 + addendum landed; register row + CHANGELOG entry.
