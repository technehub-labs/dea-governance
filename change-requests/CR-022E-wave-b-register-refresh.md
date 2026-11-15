# CR-022E: Register v12 Amendment — Skeleton-Advance Register Refresh

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-15
**Admission authority**: yes (register refresh amendment)
**Depends on**: CR-022D (register v12 line); the skeleton-advance wave (per-repo CR-XX-CAT-NN series, all landed CI-green)
**Amends**: CR-022D observational values (landed CRs immutable; corrections recorded here)

## 1. Problem Statement

The skeleton-advance wave admitted evidence-backed candidate corpora into six remaining kit skeletons and promoted them to canonical. The register still reads those rows skeleton/0.

## 2. Change

| Row | Change | Source corpus |
|---|---|---|
| dea-catalog-change-initiatives | skeleton/0 -> populated/999 | World Bank Documents & Records API (Project Documents) |
| dea-catalog-ecosystem-platforms | skeleton/0 -> populated/103 | curated platform registry (platforms' own published pages; honest-to-source size) |
| dea-catalog-experiments | skeleton/0 -> populated/1200 | ClinicalTrials.gov API v2 study registry |
| dea-catalog-financial-resources | skeleton/0 -> populated/1500 | NASDAQ Trader symbol directory |
| dea-catalog-investment-initiatives | skeleton/0 -> populated/999 | World Bank Documents & Records API (financed-operation documents) |
| dea-catalog-strategic-objectives | skeleton/0 -> populated/180 | UN 2030 Agenda SDG framework (goals + targets; honest-to-source size) |

Batch CRs that landed under numbers colliding with their series' foundation/groundwork CRs were renumbered by per-repo naming-correction CRs (CR-CHI-CAT-05, CR-EP-CAT-05, CR-EXP-CAT-05, CR-FR-CAT-06, CR-II-CAT-05; BC-01A precedent). Register totals: **33 populated / 21 skeleton** of 54. `register_version` stays **12**.

## 3. Verification

1. Register parses; `register_version: 12` unchanged.
2. Reconciler post-merge: no NEW findings vs the documented baseline (8 × R2 private-token, references ×2).
3. Canonical counters quoted from the repos' own regenerated CATALOG.yaml (per-repo gates green at the promotion PRs).

## 4. Acceptance Criteria

1. The six rows carry the refreshed values and CR-022E provenance notes.
2. `register_version: 12`, 54 entries, 33 populated / 21 skeleton.
3. Reconciler run post-merge reports no finding not present in the documented baseline.

## 5. NOT-List

1. **No canonical admissions in this repo**; no reconciler changes; no visibility changes.
2. **No metamodel work**: the four no-layout private repos (agent-foundry, ontologies, reference-architecture, solution-hub) and the two empty repos (infrastructure-components, integration-interfaces) have no metamodel entity allocations — populating them honestly requires metamodel entity decisions (owner); recorded as recommendations, not enacted.
3. **No register version bump**: snapshot-value amendment only.
