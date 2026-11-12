# CR-022B: Register v12 Amendment — Snapshot-Count Refresh and the Tenets Correction

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-12
**Admission authority**: yes (register refresh amendment)
**Depends on**: CR-022 (register v12, merged PR #21); CR-022A (merged PR #22); the 2026-11-12 portfolio recon (observation source, `repo-recon-2026-11-12.md` in the workspace)
**Amends**: CR-022/CR-022A observational values (landed CRs immutable; corrections recorded here)

## 1. Problem Statement

The 2026-11-12 recon (fresh census of all 77 synced clones against register v12) flagged rows whose observational values no longer match the repos' own indexes and files:

1. **dea-catalog-stakeholders**: register 11; the repo's index reads `canonical: 12, retired: 11, entities: 23, research_files: 92` — the owner's stakeholder work continued after the v9 tranche (pushed 2026-11-11); all 11 v9-tranche records now carry retired status and 12 records are canonical/active.
2. **dea-catalog-information-assets**: register 7 (the 2026-10-30 creation-audit snapshot); the index reads `canonical: 25` — the advancement programme grew the catalog without a register refresh.
3. **dea-catalog-metrics**: register 4,428; the repo's bespoke index reads `total: 4433, admitted: 5, candidate: 4428`. The v7 figure was the corpus size, not a canonical count; the canonical (= admitted) figure is 5.
4. **dea-catalog-organizational-units**: the row's `'records present'` clause is a survey false-positive — `entities/` holds no entity records on main (4 yaml files, none records; index `canonical: 0`).
5. **dea-catalog-tenets — the material correction**: register `populated / 8` citing "CR-TEN-02 populated 8 tenet records". Verified false against the repo itself: CR-TEN-02 (PR #5) delivered the entity-system gate + registry only (its own record says "gate vacuously CONFORMANT (0 entities in file_globs)"); kit PR #6 added the empty `entities/v1-alpha` scaffold; the repo's CATALOG.yaml reads `canonical: 0, entities: 0`. **No tenet record exists on origin main.** The 8-record owner rewrite exists only on the unpushed workspace branch `local/tenets-owner-rewrite-wip`. The erroneous reading arose from auditing the pre-migration local clone whose main carried that unpushed WIP — the survey false-positive class this register has now hit three times (stakeholders v9 note-fix, org-units here, tenets here).

## 2. Change

| Row | Field | Old → New | Basis |
|---|---|---|---|
| `dea-catalog-stakeholders` | `canonical_count` | 11 → 12 | repo index (recon 2026-11-12) |
| `dea-catalog-information-assets` | `canonical_count` | 7 → 25 | repo index (recon 2026-11-12) |
| `dea-catalog-metrics` | `canonical_count` | 4,428 → 5 | repo bespoke index `admitted: 5`; field semantics made explicit (canonical = admitted; corpus 4,433 documented in the note) |
| `dea-catalog-tenets` | `state` | populated → **skeleton** | repo index `canonical: 0`; CR-TEN-02 delivered no records |
| `dea-catalog-tenets` | `canonical_count` | 8 → 0 | same |
| `dea-catalog-organizational-units` | `notes` | 'records present' → corrected census wording | recon 2026-11-12 |

Register totals: **18 populated / 36 skeleton** of 54 (tenets un-populates; CR-022A's 19/35 shifts). `register_version` stays **12**; `snapshot_date` stays 2026-11-12.

## 3. Named follow-ups (not enacted here)

1. **dea-metamodel**: CR-MET-016 promoted `dea:Tenet` lifecycle `scaffold → existing` citing "owner-side CR-TEN series, 8 canonical" — the same erroneous observation. A metamodel correction CR should re-observe Tenet against the verified truth (skeleton/0 on origin; CR-MET-017 BusinessCapability correction precedent). Landing the owner-rewrite branch as a proper PR would re-validate the promotion honestly instead.
2. **dea-catalog-tenets**: push the owner rewrite (`local/tenets-owner-rewrite-wip`: 8 tenet records + documentation standard, 2026-11-01) through PR review; it supersedes kit PR #6 per the register's standing note.
3. The R2-private and R5-shard decisions from CR-022A remain open owner decisions (unchanged).

## 4. Verification

1. Register parses (CI parse job); `register_version: 12` unchanged.
2. Reconciler post-merge: no NEW findings vs the CR-022A baseline (11 documented: 8 × R2 private, 3 × R5 shard-triggers). stakeholders and information-assets are R3-visible (non-bespoke): registered `populated` matches observed `populated` (canonical 12 / 25 > 0) — R3 green on both. tenets and metrics are bespoke (R3 skips); org-units bespoke-index-free but state skeleton/canonical 0 matches its index.
3. The five rows' values match the repos' own indexes/files as quoted above (recon evidence, 2026-11-12).

## 5. Acceptance Criteria

1. The five rows carry the refreshed values and CR-022B provenance notes.
2. `register_version: 12`, 54 entries, 18 populated / 36 skeleton.
3. Reconciler run post-merge reports no finding not present in the CR-022A baseline.

## 6. NOT-List

1. **No metamodel lifecycle change**: the Tenet promotion correction is named, not enacted (cross-repo, per-entity verification rule).
2. **No record/index changes in any catalog repo**; no branch pushes (the tenets WIP stays on its local branch until the owner directs a PR).
3. **No reconciler changes**; no visibility changes (CR-022A's owner decisions stay open).
4. **No register version bump**: snapshot-value amendment only.
