# CR-017: Information Model Catalog Registration (Register v8)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-01
**Admission authority**: yes (register admission)
**Depends on**: CR-013 (the register), CR-AR-FMWK-15 (dea-architecture-framework; the IM allocation, v0.9.0)
**Companion**: dea-metamodel CR-MET-019 (canonical entity, lands in the same window); catalog-side CR-IM-CAT-01/02 (dea-catalog-information-models)

## 1. Problem Statement

The owner directed a new **Information Model** entity — the conceptual/logical-blueprint member of the information family, distinct from InformationClass (the sensitivity/regulatory band) and InformationAsset (the consumable form). The governance chain has started: root-model allocation CR-AR-FMWK-15 landed (v0.9.0, tag cut), the new repository `dea-catalog-information-models` is created and scaffolded. R1 of the portfolio reconciler will flag the metamodel's `catalog_repo: dea-catalog-information-models` the moment CR-MET-019 lands unless the register entry exists first — so this CR lands in the window before it.

## 2. The registration

`registers/catalog-portfolio.yaml` gains the 44th entry: `dea-catalog-information-models` / `entities: [dea:InformationModel]` / `state: skeleton` / `canonical_count: 0` / ratified 2026-11-01 — the repo exists (R2 clean), is kitted (foundation lands as CR-IM-CAT-01), and holds zero records pending evidence (CR-IM-CAT-02 population plan).

## 3. Sequencing note

CR-AR-FMWK-15 (root) → this CR (register; repo exists) → CR-MET-019 (metamodel entity; R1 satisfied on landing) → CR-IM-CAT-01 (kit) → CR-IM-CAT-02 (population plan). The metamodel entity's `lifecycle: planned` corrects to `existing` by a later boundary CR once the catalog carries its foundation gates (CR-MET-016 precedent).

## 4. NOT-list

1. No catalog content changes (the foundation and population are the catalog's own CRs).
2. No metamodel changes in this PR.
3. No claim that InformationModel is populated — it is scaffold-stage by design (evidence-only admission).

## 5. Definition of Done

1. Register v8 parses with 44 entries; reconciler R1–R4 Findings: 0 (verified).
2. Register row and CHANGELOG entry in this PR.
