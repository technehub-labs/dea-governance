# CR-020: Business Services Populated (Register v11)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-10
**Admission authority**: yes (register refresh)
**Depends on**: CR-019 (the R5 audit rule whose watch findings pointed at this repo); dea-catalog-business-services CR-SVC-016 (the index repair this refresh reconciles against)
**Lands after**: the services CR-SVC-016 PR (this refresh must not merge first, or R3 would flag registered-populated against the still-old index)

## 1. Problem Statement

The register records `dea-catalog-digital-business-service-factory` as `state: skeleton, canonical_count: 0`. That reading was green against the repo's index, but the index itself lied: the vendored regenerator probed the colon-form `<entity_id>.yaml` for the canonical file while every record file on disk carries the hyphen form, so `read_canonical_yaml` found nothing and all 535 admitted records classified `candidate`. The same hyphen-form infer_state defect was repaired per-repo in stakeholders (CR-CATALOG-STRUCT-12) and metrics; dea-metaframework v2.7.0 is the source fix. The services repo's CR-SVC-016 re-vendors the v2.7.0 regenerator (as part of the CR-SVC-016 shard-layout move), and the regenerated index now reads truthfully: `canonical: 535, candidates: 0`.

## 2. Objective

Reconcile the register row to the observed truth: `state: populated`, `canonical_count: 535`; `register_version` 10 -> 11. R3 then stays green against the post-CR-SVC-016 index, and the R5 watch tier clears both of the repo's hot-directory findings (the shard move took `entities/v1-alpha` from 536 to 25 entries and `contributions/queue` from 518 to 24).

## 3. Verification

Reconciler run after both CRs land (expected): `Findings: 0` for this repo's rows; remaining org findings unchanged from the CR-019 first run (the roles R5 finding, until its own repo CR lands).

## 4. Files

- `registers/catalog-portfolio.yaml`: the DBSF row (populated/535 + dated note); `register_version` 11; snapshot 2026-11-10.

## 5. Acceptance Criteria

1. Register parses (CI parse job green).
2. Reconciler R3 reports no state-truth finding for `dea-catalog-digital-business-service-factory` after CR-SVC-016 is on its default branch.
3. `register_version: 11`.

## 6. NOT-List

- **No naming-drift reconciliation**: the repo rename (declared `dea-catalog-digital-business-service-factory`, actual `dea-catalog-business-services`) remains CR-013 section 6 / CR-MET-014 finding 2 follow-up.
- **No roles-row change**: the roles finding is a directory-size remediation (its own repo CR), not a state refresh.
