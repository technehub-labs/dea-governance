# CR-013: Catalog Portfolio and Ownership Register

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-30
**Admission authority**: yes (register admission)
**Depends on**: CR-012 (EGV-001 canonical governance authority; EGV-008 provenance); DEA-ID-000 (foundation paper)
**Companion**: metamodel CR-MET-014 (org-wide lifecycle audit, PR #202); dea-catalog-information-assets CR-IA-CAT-01..04

## 1. Problem Statement

Metamodel change requests CR-018, CR-020, and CR-022 dispose catalog-side effects to "the catalog portfolio map" and "the catalog-ownership register" owned by `CR-013 (dea-governance)`. No such register exists: the governance repository holds CR-012 (the standard) and the foundation paper only. Meanwhile the org has accumulated 45 catalog repositories named as `catalog_repo` values in the metamodel, created and populated without a single ratification record, and the metamodel's entity `lifecycle` field drifted from reality (audited and backfilled separately by metamodel CR-MET-014, whose dispositions cite this register as their observation source).

## 2. Objective

Establish the catalog portfolio and ownership register as the governance-layer record of which catalog repositories exist, which metamodel entity allocations they own, and what their observed realization state is at registration time; and ratify the newest catalog, `dea-catalog-information-assets`, at creation.

## 3. The Register

`registers/catalog-portfolio.yaml` records all 45 repositories named by metamodel `catalog_repo` values, each with: owned entity ids, observed state (`populated` / `skeleton` / `missing`), canonical record count at the 2026-10-30 audit snapshot, ratification date, and notes. The register is descriptive at the governance layer: the metamodel remains the canonical authority for entity-type contracts (EGV-001), and the metamodel `lifecycle` field remains the normative expression of realization maturity.

## 4. Ratifications and Findings

Ratified at creation by this CR:

- `dea-catalog-information-assets` (`dea:InformationAsset`) - stood up 2026-10-29/30 under CR-IA-CAT-01..04; populated with 7 canonical records carrying the first classification crosswalks into `dea-catalog-information-classes` (CR-IC-CAT-10); the named unblock for the capabilities U-2 `realization.information` residual.

Findings recorded in the register (follow-ups, not fixed here):

1. **Naming drift (2):** the metamodel's `catalog_repo` for `dea:BusinessProcess` points at `dea-catalog-processes` while the org's processes work repository is `dea-catalog-business-processes`; likewise `dea-catalog-digital-business-service-factory` vs `dea-catalog-business-services` for services. Reconciliation (repoint or rename) requires per-entity verification and cross-repo coordination.
2. **Stale metamodel `existing` (3):** `dea:BusinessService`, `dea:SolutionComponent`, and `dea:PerformanceMetric` are `lifecycle: existing` while their registered repos show no canonical content at the snapshot. Downgrade or repoint decisions belong to the metamodel change process.
3. **Empty-index anomaly (1):** `dea-catalog-metrics` carries a present-but-empty `CATALOG.yaml`.

## 5. Maintenance Rule

A new catalog repository MUST be recorded in this register in the same programme that creates it (the bootstrap or foundation CR sequence). The register entry cites the creating CR series; the metamodel CR that backfills the entity's `lifecycle` cites the register as its observation source. State and count fields are refreshed when a reconciliation audit runs (CR-MET-014 precedent); they are informational.

## 6. NOT-list

1. No change to CR-012's normative requirements (EGV-001..012); this CR adds a register, not a rule.
2. No catalog repository is created, renamed, or repointed by this CR.
3. No metamodel content changes (CR-MET-014 owns the lifecycle backfill).
4. No ownership transfers: all registered repositories carry the org owner; per-catalog functional ownership stays in each catalog's own governance fields.

## 7. Definition of Done

1. `registers/catalog-portfolio.yaml` parses and covers all 45 `catalog_repo` values named by the metamodel at 2026-10-30.
2. Register row and CHANGELOG entry landed in this PR.
3. Metamodel CR-MET-014 merged (dependency satisfied; PR #202).
