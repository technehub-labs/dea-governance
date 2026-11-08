# CR-018: Stakeholders Populated (Register v9)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-08
**Depends on**: CR-013 (the register); `dea-catalog-stakeholders` CR-CATALOG-STRUCT-12/13/14 (PRs #15/#16/#17); dea-architecture-framework CR-AR-FMWK-16 (PR #35, v0.9.1); dea-metamodel CR-MET-021 (PR #210)

## 1. Problem Statement

The Stakeholders catalog — one of the six owner-active repos deliberately left alone by the 2026-11-02 advancement programme, and carrying a steward_note flagging possible infer_state misclassification exposure plus a "records present" claim that was inaccurate (contributions/ was empty) — advanced to a populated, enriched state on 2026-11-08 under the owner's directive. The register still reads `state: skeleton`, `canonical_count: 0`.

## 2. The update

`registers/catalog-portfolio.yaml`: the `dea-catalog-stakeholders` row moves to `state: populated`, `canonical_count: 11`, ratified '2026-11-08'; the stale steward_note is replaced by the resolution record. `register_version` 8 → 9; `snapshot_date` '2026-11-08'.

What landed behind the count (the verification chain):

- **CR-CATALOG-STRUCT-12 (PR #15)** — foundation modernization: OpenDEAM pin v0.2.1 → v0.9.0 (allocation unchanged), record schema realigned to the metamodel v1.0.0 Stakeholder schema as a closed-world projection, regenerator re-vendored from dea-metaframework `origin/main` carrying CR-ECF-011 + the PR #58 hyphen-form infer_state fix (the exact exposure the steward note warned about — RESOLVED), pointer/schema record gates wired into CI.
- **CR-CATALOG-STRUCT-13 (PR #16)** — population contract: `docs/FOUNDATIONS.md` (Actors boundary, three evidence channels, id minting per id-system §2.5), `docs/RECORD-STANDARD.md`, `catalog-research/CANDIDATE-REGISTER.md` (honest zeros: C-001 enterprise anchor, C-002..004 customers/partners/investors), ES-003 relationship types registered (`enforces`, `publishes`).
- **CR-CATALOG-STRUCT-14 (PR #17)** — first canonical tranche: 11 records (3 organisation/governance/community capacities + 8 regulators one-to-one with the regulations catalog's eight active records; 7 `enforces` + 1 `publishes`), deferred edges documented, all five workflows green, `CATALOG.yaml` canonical: 11.
- **CR-AR-FMWK-16 (PR #35) + CR-MET-021 (PR #210)** — the lifecycle mirrors promoted `scaffold` → `existing` on both the root model (v0.9.1) and the metamodel, resolving the `check_catalog_index_matches_model` stale-scaffold warning.

The prior note's "records present" clause is recorded as inaccurate in the replacement row (survey false-positive class — the 1 MB / contents-API lesson's sibling; here simply a wrong claim caught by direct verification).

## 3. NOT-list

1. No catalog content changes in this PR (the tranche is the catalog's own CR).
2. No other register rows change — the other five owner-active repos stay as recorded.
3. No claim about the bespoke corpora (metrics/roles) — out of scope here.

## 4. Definition of Done

- AC-01 `registers/catalog-portfolio.yaml`: stakeholders row `state: populated`, `canonical_count: 11`, `register_version: 9`.
- AC-02 `registers/reconcile_portfolio.py` exits with `Findings: 0` (offline mode; the weekly online R1–R4 run covers the network half).
- AC-03 CHANGELOG entry; CR index row.
