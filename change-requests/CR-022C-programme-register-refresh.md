# CR-022C: Register v12 Amendment — Population-Programme Observational Refresh

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-15
**Admission authority**: yes (register refresh amendment)
**Depends on**: CR-022/CR-022A/CR-022B (register v12 line); the catalog population programme (2026-11 directive, tools/ingest-kit in the workspace)
**Amends**: CR-022B observational values (landed CRs immutable; corrections recorded here)

## 1. Problem Statement

The 2026-11-13/15 catalog population programme admitted gated candidate corpora into nine skeleton catalogs and surfaced two register-truth findings:

1. **dea-catalog-platform-services was never a skeleton.** The owner had landed 500 PlatformService records (colon-form subtree layout, version 1.0.0) that the pre-programme vendored regenerator never counted; the programme's v2.8.0 shard-aware re-vendor (part of each repo's groundwork CR) now counts them canonical 500. Same false-negative family as CR-016 (metrics) and the CR-022B tenets correction, inverted direction this time (records present, index 0). State flips skeleton → populated / 500.
2. **dea-catalog-skills is owner-active.** While the programme was in flight, the owner landed a 735-record Skill candidate corpus on main (CR-DEA-SKL-01, roles-style bulk ingestion with hash-locked manifest). The programme's kit-bring-up PR was built on a stale base and was closed unmerged; skills comes off the programme scope (the repo is owner-active under the AGENTS.md rule). Its 1,000-candidate programme baseline is not met (735); topping up is the owner's call.

Additionally, the programme admitted candidate corpora (informational — candidates do not change register `state`/`canonical_count`): guardrails 1,196; risk-register 2,716; technology-radar 2,442; patterns 2,282 (18 ArchitecturePattern + 1,046 Technology + batch renumbering correction); data-products 2,557; model-deployments 1,000; platform-services 2,525; ai-ml-models 1,000; event-streams 1,026 (825 baseline + 201 supplement). Every repo also landed the intake workflow (queue gate + admission tool), pin bump v2.6.0 → v2.8.0 with the shard-aware toolchain re-vendor, and CR naming corrections where the driver's first pass omitted the house `CR-` prefix (per-repo naming-correction CRs, BC-01A precedent).

## 2. Change

| Row | Change | Basis |
|---|---|---|
| `dea-catalog-platform-services` | `state` skeleton → **populated**; `canonical_count` 0 → **500** | pre-existing owner corpus now counted by the v2.8.0 re-vendor; programme candidates 2,525 noted |
| `dea-catalog-skills` | notes only: owner-active corpus (735 proposed, CR-DEA-SKL-01), programme superseded | observed origin main @ a7b13b7 |

Register totals: **19 populated / 35 skeleton** of 54 (platform-services crosses). `register_version` stays **12**.

## 3. Verification

1. Register parses; `register_version: 12` unchanged.
2. Reconciler post-merge: no NEW findings vs the CR-022A baseline (8 × R2 private, 3 × R5 shard-triggers). platform-services is R3-visible: registered populated matches observed canonical 500 > 0.
3. Candidate counters quoted from the repos' own CATALOG.yaml `counts.candidates` (post-batch, regen-verified per repo).

## 4. Acceptance Criteria

1. The two rows carry the refreshed values and CR-022C provenance notes.
2. `register_version: 12`, 54 entries, 19 populated / 35 skeleton.
3. Reconciler run post-merge reports no finding not present in the CR-022A baseline.

## 5. NOT-List

1. **No canonical admissions**: all programme corpora are candidate-state; canonical counters unchanged except the platform-services owner records counted by the corrected toolchain.
2. **No reconciler changes**; no visibility changes (CR-022A owner decisions stay open).
3. **No metamodel work**: the PlatformService schema-backfill follow-up is named, not enacted.
4. **No register version bump**: snapshot-value amendment only.
