# CR-022D: Register v12 Amendment — Canonical-Admission Register Refresh

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-15
**Admission authority**: yes (register refresh amendment)
**Depends on**: CR-022C (register v12 line); the catalog population programme's canonical admission wave (per-repo CR-XX-CAT-NN canonical-admission CRs, all landed CI-green)
**Amends**: CR-022C observational values (landed CRs immutable; corrections recorded here)

## 1. Problem Statement

The canonical admission wave promoted the full candidate corpora of nine programme repos to the canonical slot (17,244 promoted records + the 500 pre-existing owner PlatformService records = 17,744 canonical). The register still reads those rows skeleton/0 (platform-services 500).

## 2. Change

| Row | Change |
|---|---|
| dea-catalog-ai-ml-models | skeleton/0 -> populated/1000 |
| dea-catalog-model-deployments | skeleton/0 -> populated/1000 |
| dea-catalog-guardrails | skeleton/0 -> populated/1196 |
| dea-catalog-event-streams | skeleton/0 -> populated/1026 |
| dea-catalog-technology-radar | skeleton/0 -> populated/2442 |
| dea-catalog-patterns | skeleton/0 -> populated/2282 |
| dea-catalog-data-products | skeleton/0 -> populated/2557 |
| dea-catalog-risk-register | skeleton/0 -> populated/2716 |
| dea-catalog-platform-services | populated/500 -> populated/3025 |

Each promoted record completed its provenance ladder (candidate preserved -> corroborated -> reviewed -> canonical; actor of record per CR-BP-118) with its published-document evidence citations preserved from admission. Intake queues remain live and admitted-closed (candidates 0). Register totals: **27 populated / 27 skeleton** of 54. `register_version` stays **12**.

## 3. Verification

1. Register parses; `register_version: 12` unchanged.
2. Reconciler post-merge: no NEW findings vs the documented baseline (8 × R2 private-token, references ×2 — both documented).
3. Canonical counters quoted from the repos' own regenerated CATALOG.yaml (per-repo gates green at the promotion PRs).

## 4. Acceptance Criteria

1. The nine rows carry the refreshed values and CR-022D provenance notes.
2. `register_version: 12`, 54 entries, 27 populated / 27 skeleton.
3. Reconciler run post-merge reports no finding not present in the documented baseline.

## 5. NOT-List

1. **No new records**: this refresh records the canonical admission wave's outcome; no admissions happen in this repo.
2. **No reconciler changes**; no visibility changes (CR-022A owner decisions stay open).
3. **No register version bump**: snapshot-value amendment only.
