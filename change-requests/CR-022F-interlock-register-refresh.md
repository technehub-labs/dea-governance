# CR-022F: Register v12 Amendment — Interlock, Skeleton-Advance and Visibility Refresh

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-16
**Admission authority**: yes (register refresh amendment)
**Depends on**: CR-022E (register v12 line); skills CR-DEA-SKL-02 (interlock completion, PR #4); intangible-resources CR-INR-CAT-02..05 (corpus + canonical admission)
**Amends**: CR-022E observational values + CR-022A visibility notes (landed CRs immutable; corrections recorded here)

## 1. What this CR records

1. **Skills<->roles interlock completed** (skills CR-DEA-SKL-02): the roles catalog references 742 distinct `skills:skill-*` ids; skills published 735. The 7-record gap was admitted through the owner's CR-DEA-SKL-01 pipeline (CSV renamed+extended to bulk-742; manifest sha256/rows/kinds/edges updated; slice registry extended with the roles-taxonomy facets banking/health/public-sector; materialize_skills.py materialized the 7; bespoke index at 742). Evidence per record = the citing roles record (repository-verifiable). Actors and stakeholders carry no direct skill references (roles is the consumer). Interlock: **742/742**.
2. **intangible-resources flips skeleton/0 → populated/740**: SPDX License List + OSI published license registries admitted as candidates (CR-INR-CAT-03/04) and promoted canonical (CR-INR-CAT-05; protection_type=license; ladders completed).
3. **Visibility: six R2 findings RESOLVED** — the owner directed the flip-public for agent-foundry, infrastructure-components, integration-interfaces, ontologies, reference-architecture and solution-hub (2026-11-08 precedent). The two archived repos (permission-probe, taxonomy) reject PATCH while archived (no unarchive REST endpoint) and keep documented red-by-design R2 notes — owner can flip via the UI if desired.
4. **Dual-home finding recorded**: the three IS-semantic-architecture repos (information-system-services, infrastructure-components, integration-interfaces) would duplicate catalogue homes for entities whose canonical `catalog_repo` pointers resolve to api-contracts (dea:IntegrationInterface), application-components (dea:InfrastructureComponent) and platform-services (dea:InformationSystemService) — all three now populated with those entities' records. Owner decision named: archive/redirect or re-allocate; populating them as catalogues would create the dual-home defect class CR-022 exists to prevent. The four no-allocation repos (agent-foundry, ontologies, reference-architecture, solution-hub) likewise need metamodel entity decisions before honest population. NOT enacted here.

## 2. Change

| Row | Change |
|---|---|
| dea-catalog-intangible-resources | skeleton/0 -> populated/740 |
| dea-catalog-skills | notes only: 742 records; interlock 742/742 resolved (CR-DEA-SKL-02) |
| six flipped repos | R2 note: RESOLVED 2026-11-16 (flip-public directed) |
| three IS-semantic-architecture repos | dual-home finding + owner decision named (information-system-services owner foundation CR-IS-CAT-03A stands) |

Register totals: **34 populated / 20 skeleton** of 54. `register_version` stays **12**.

## 3. Verification

1. Register parses; `register_version: 12` unchanged.
2. Reconciler post-merge: R2 findings drop by the six flipped repos (2 archived-repo R2 findings remain documented); no other NEW findings.
3. intangible-resources is R3-visible: registered populated matches observed canonical 740 > 0.

## 4. Acceptance Criteria

1. The rows carry the refreshed values and CR-022F provenance notes.
2. `register_version: 12`, 54 entries, 34 populated / 20 skeleton.
3. Reconciler run post-merge: R2 findings reduce by six; no other NEW findings.

## 5. NOT-List

1. **No canonical admissions in this repo**; no reconciler changes.
2. **No metamodel work**: the dual-home and no-allocation decisions are named, not enacted.
3. **No unarchive of the two archived repos** (API limitation documented); owner UI action if desired.
4. **No register version bump**: snapshot-value amendment only.
