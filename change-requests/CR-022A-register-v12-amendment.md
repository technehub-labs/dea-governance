# CR-022A: Register v12 Amendment — Verification Findings Recording

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-12
**Admission authority**: yes (register refresh amendment)
**Depends on**: CR-022 (register v12, merged PR #21); CR-MET-022 (dea-metamodel, merged PR #211); CR-API-CAT-02 in dea-catalog-api-contracts (owner population, PR #3)
**Amends**: CR-022 (landed CRs are immutable; this amendment records what its §4 verification surfaced)

## 1. Problem Statement

CR-022's post-merge verification (reconciler run 43220126714, dispatched 2026-11-12 12:41 UTC) reported **12 findings**. Triaging each class:

1. **R3 × 1 — api-contracts**: `registered state 'skeleton' but observed 'populated' (canonical=627)`. TRUE, and the register row was stale within hours of the v12 snapshot: the owner's CR-API-CAT-02 (PR #3, merged 2026-11-12 15:58 +08:00) landed 627 canonical API contract records between the CR-022 snapshot (taken from the 2026-11-11/12 sweep) and the reconciler run. The reconciler is correct; the register refreshes.
2. **R2 × 8 — the newly-registered private repos**: agent-foundry, infrastructure-components, integration-interfaces, ontologies, permission-probe, reference-architecture, solution-hub, taxonomy are all `private: true` (the two archived ones are also private). The weekly workflow's default `GITHUB_TOKEN` cannot see other org-private repos, so its `GET /repos/{org}/{repo}` 404s — indistinguishable from a nonexistent repo, hence "R2: does not exist". **The repos exist** (verified with an authenticated token during the sweep and again today). This is the exact finding class resolved on 2026-11-08 when the owner flipped 8 then-private repos public. Resolution is an owner visibility decision (flip public, per precedent) or an infrastructure decision (org-read PAT in the workflow); neither is this amendment's call, so the rows carry a documented red-by-design note.
3. **R5 × 3 — directory-size true findings**: roles `entities/v1-alpha` at 1,252 (pre-existing, red by design since CR-019) **plus two new true findings from registering `dea-catalog-references`**: `dea/application` and `media-types/application` each hold 1,812 entries — over the 800 shard trigger, needing a references shard CR (the CR-MET-024 recipe). Registering the repo didn't create the condition; it surfaced it. The finding is honest and stays until a shard CR lands, joining roles in the documented-red set.

Also noted: the R5 *watch* on api-contracts `entities/v1-alpha` at 628 entries (627 records + directory listing semantics) is non-failing and below the 800 trigger.

## 2. Change

1. **api-contracts row refresh**: `state: skeleton → populated`, `canonical_count: 0 → 627`, with the CR-API-CAT-02 provenance note.
2. **R2-visibility note appended to the 8 private rows**: documents the token-visibility limitation, the red-by-design status, and the two resolution paths (owner flip-public precedent 2026-11-08; org-read PAT).
3. **Register v12 totals restated**: 44 → 54 entries stands; populated/skeleton becomes **19 populated / 35 skeleton** (api-contracts crosses).
4. **Named follow-ups** (recorded here, not enacted): references shard CR (2 R5 true findings); the owner's private-repo visibility decision (8 R2 red-by-design rows); roles shard CR (pre-existing).

## 3. Verification

Post-merge reconciler dispatch is expected to report **11 findings, zero of them unexpected**: 8 × R2 (documented red-by-design on their rows), 3 × R5 (roles 1 + references 2; documented). R3 green on every row including the refreshed api-contracts; R1/R4 green (CR-MET-022 merged before CR-022; unchanged by this amendment).

## 4. Acceptance Criteria

1. Register parses; `register_version` stays **12** (an amendment does not bump the version).
2. api-contracts row reads populated/627 with the CR-API-CAT-02 note.
3. The 8 private rows carry the R2-visibility note.

## 5. NOT-List

1. **No visibility changes**: this amendment does not flip any repo public and does not modify the reconciler workflow (owner decisions, named only).
2. **No reconciler changes**: R1–R6 semantics untouched; the red-by-design documentation lives in register notes, not in code exceptions.
3. **No shard work**: the references and roles shard CRs are named, not written here.
4. **No CR-022 file edits**: landed CRs are immutable; this is a separate amendment CR.
