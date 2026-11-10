# Changelog

All notable changes to this repository are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### CR-021: Org-Wide Pin-Truth Audit (Reconciler R6)

The reconciler gains R6: every registered repo's CI workflows are scanned (same tree fetch as R5; file bodies off the raw route) and every `technehub-labs/dea-metaframework` checkout ref is verified against the real tag set; a release-tag pin that does not exist is a FAIL finding (the 404 class: 2026-11-11 a consumer pinned v2.8.0 before the release was cut and 404'd org-visibly until the tag landed), a checkout naming the upstream without a release-tag ref prints a floating-pin watch. Extraction is step-scoped (CST-013 semantics; root-model allocation pins never mistaken) in a pure 5-test function (registers/test_reconcile_pins.py). First live run: 0 R6 findings (all pins resolve, including stakeholders' v2.8.0 post-release-cut), 1 floating-pin watch (dea-catalog-organizational-units); R1..R5 unchanged (roles finding, metrics watch, R3 green on register v11). PR-time counterpart: metaframework CR-CATALOG-STRUCT-13 `pins-resolve` job. Tag list fetched once per run; transport failures warn-and-skip.

### CR-020: Business Services Populated (Register v11)

The DBSF register row reconciles to the observed truth: dea-catalog-digital-business-service-factory -> state populated, canonical_count 535; register_version 10 -> 11. The skeleton reading was green only against a lying index: the services repo's vendored regenerator probed the colon-form entity yaml name while every record file is hyphen-form, so all 535 CR-SVC-004-admitted canonical records classified candidate. dea-catalog-business-services CR-SVC-016 re-vendors the v2.7.0 regenerator (hyphen-form infer_state repair, the stakeholders CR-CATALOG-STRUCT-12 defect family), the index now reads canonical 535 / candidates 0, and the same CR's shard move cleared the repo's two R5 watch findings (entities 536 -> 25 entries, queue 518 -> 24). Lands after CR-SVC-016; naming-drift reconciliation remains the CR-013 section 6 follow-up. Reconciler: 0 findings for this repo's rows.

### CR-019: Org-Wide Directory-Size Audit (Reconciler R5)

The reconciler gains R5: every registered repo's recursive git tree is censused per directory (files + subdirectories, exactly what a GitHub listing shows) and any directory at or over 800 entries (the entity-storage-layout §4 shard trigger; GitHub truncates listings at 1,000) is a FAIL finding; 500+ entries print a non-failing watch line. Register-driven scope (bespoke-index repos audited too), tracked content only, truncated-tree payloads warn-and-skip rather than fire. Counting lives in a pure function with the reconciler's first unit tests (registers/test_reconcile_directory_counts.py, new reconciler-units CI job); the pre-merge regression the tests pin: counting the trees API's explicit `tree` objects double-counts every directory (536 reported as 1,071). First live run (2026-11-10): 1 finding (dea-catalog-roles entities/v1-alpha at 1,252, over the cap), 3 watch (business-services entities 536 / queue 518, metrics c/ 604); R1..R4 clean. Weekly counterpart to the metaframework's CST-017 (CR-CATALOG-STRUCT-11). Register v10: metrics entry's stale "root-position records" clause repaired (CR-MET-024 named follow-up); no observational field changed.

### CR-018: Stakeholders Populated (Register v9)

The Stakeholders catalog advanced to an active, enriched state under the owner's 2026-11-08 directive: first canonical tranche of 11 records — 3 organisation/governance/community capacities (GitHub Inc. as platform supplier, the OSS community, the owner's governing-board capacity) + 8 regulators one-to-one with the regulations catalog's eight active records (7 `enforces` + PCI SSC's `publishes`) — behind a population contract (`docs/FOUNDATIONS.md`, `docs/RECORD-STANDARD.md`, candidate register with honest zeros) and a foundation modernization (OpenDEAM v0.9.0 pin, metamodel v1.0.0 schema projection, regenerator re-vendored with the hyphen-form infer_state fix — resolving the steward_note's exposure; its "records present" clause recorded as inaccurate). Register row `dea-catalog-stakeholders` -> `state: populated`, `canonical_count: 11`; `register_version` 8 -> 9; snapshot 2026-11-08. Lifecycle mirrors promoted root-model CR-AR-FMWK-16 (v0.9.1) + metamodel CR-MET-021. Reconciler Findings: 0.

### Understanding OpenDEA: A Plain-Language Guide

New `docs/understanding-opendea.md`: a non-technical guide to the entity system. Explains the information family (Business Object -> Information Model -> Data Entity -> Information Asset, with Information Class as the overlay), the commercial decomposition chain (Agreement -> Offering -> Product -> Service -> Resource -> Entity), the other entity families, the evidence ladder, and the key org-wide numbers. Written for both technical and non-technical audiences.


### CR-017: Information Model Catalog Registration (Register v8)

Registers dea-catalog-information-models (44th entry; entities [dea:InformationModel]; state skeleton) - the conceptual/logical-blueprint entity of the information family, directed by the owner and allocated in the root model (CR-AR-FMWK-15, v0.9.0). Lands in the window before metamodel CR-MET-019 so reconciler R1 never sees an unregistered catalog_repo. Reconciler verified Findings: 0.

### CR-016: Metrics Undercount Correction and Reconciler v2

The owner challenged CR-015's 4,019 org total and was right: the metrics index is 4 MB and the contents API returns no body over 1 MB, so every index-based observation read metrics as empty. Corrected: dea-catalog-metrics populated with 4,428 records (bespoke index; owner split 5 admitted / 4,423 candidate), roles confirmed as a 1,252-record corpus under a bespoke schema; org-wide record census 9,699 under org-standard machinery. Reconciler v2: size-safe index reads (raw first, git-blobs fallback), bespoke-schema census cross-check, unreadable-index findings instead of silent zeros. PerformanceMetric lifecycle 'existing' vindicated; the stale-existing family shrinks to dbsf's two entities. Standing-report addendum landed.

### CR-015: Org-Wide Catalog Standing Survey

docs/reports/CATALOG-STANDING-2026-10-31.md: all 43 registered catalogs observed mechanically - 13 populated carrying 4,019 canonical records; 25 skeletons (18 with the advancement-programme kit); 5 bespoke/pre-index layouts; 0 missing; 0 open candidate investigations (capabilities candidate register closed under CR-DEA-BC-68). Register v6: capabilities 29 -> 40 canonical, index: bespoke flags extended to the four remaining pre-index repos, snapshot 2026-10-31. Reconciler R1-R4 verified Findings: 0.

### Register v5: business-capabilities correction + infer_state exposure notes

dea-catalog-business-capabilities corrected to populated (29 canonical / 3 candidates / 0 retired): the 0-canonical count behind registers v1-v4 was an upstream toolchain defect (the catalog's vendored regenerator misclassified all hyphen-named canonical records as candidates since the mv1 id migration; fixed dea-metaframework PR #58, corrected dea-catalog-business-capabilities CR-DEA-BC-61). Five owner-active repos receive steward notes flagging possible exposure to the same misclassification family; their index refreshes remain the owner's call. Verified Findings: 0 online.

### Register refresh v4 (advancement programme closure)

Waves 2-4 recorded: 18 foundation-advanced kits (guardrails, strategic-objectives, risk-register, event-streams, change/investment-initiatives, journey-touchpoints, ecosystem-platforms, platform-services, api-contracts, patterns, technology-radar, ai-ml-models, experiments, model-deployments, signals, digital-identities, data-products + tenets-superseded note), 3 creations (financial/intangible/physical-resources), tenets corrected to populated (owner-side CR-TEN series, index bespoke), six owner-active repos steward-noted. Verified Findings: 0 online.

### Register refresh v3 + reconciler hardening (Wave 1 boundary)

Register: data-entities populated (9), controls populated (20), regulations populated (8), knowledge-assets created + populated (8), concepts corrected to populated (29; bespoke pre-index layout, `index: bespoke` stewarded-state flag), processes refreshed at v2 (3,722). Reconciler: `_get` retries (the GitHub API intermittently fails single-flight reads - a finding must never fire on a transport flake); R3 skips `index: bespoke` entries until they adopt the CATALOG.yaml discipline. Verified Findings: 0 online.

### CR-014: Org-Level Portfolio Reconciliation CI

`registers/reconcile_portfolio.py` + weekly workflow: the CR-013 register is reconciled against the metamodel allocations and GitHub reality (R1-R4), failing on drift. Basic repository CI (parse + authorship) added - the governance repo's first. First reconciler run detected real drift within 48 hours of the manual snapshot: dea-catalog-processes is populated (3,722 canonical), not skeleton; register refreshed to v2 (2026-11-02).

### CR-013: Catalog Portfolio and Ownership Register

Establishes `registers/catalog-portfolio.yaml` covering all 43 catalog repositories named by metamodel `catalog_repo` values (entity allocations, observed state at the 2026-10-30 audit, ratification dates). Ratifies `dea-catalog-information-assets` at creation; names the naming-drift (processes, services) and stale-existing (BusinessService, SolutionComponent, PerformanceMetric) follow-ups; adds the register maintenance rule for future catalog creations. Companion to metamodel CR-MET-014.

### DEA-ID-000: General Entity System Foundation Paper

Landing of the OpenDEA entity-system foundation paper in `docs/design/entity-system-foundation.md`. The architectural philosophy, 5-concern taxonomy (identity / semantics / relationships / lifecycle / conformance), authority model (Architecture Framework → ECF/Metamodel → General Entity System → Catalogs), 7-workstream taxonomy, 4-phase adoption programme. The paper is the philosophical foundation for the entity-system programme; CR-012 is the normative CR that operationalises it. No entity, schema, or id changes; the foundation paper is advisory.

### CR-012: Org-Wide General Entity Governance Standard (renumbered from CR-DEA-ID-001)

The org-wide normative CR establishing the 12 EGV-001..012 requirements for entity governance across the `technehub-labs/*` portfolio. 8 deliverables + 6 implementation stages. The standard applies to all OpenDEA foundation models, reference catalogs, schemas, specifications, tooling, validation pipelines, and derived architectural assets. Adoption by individual catalog repos happens through scoped adoption CRs (the `CR-BP-121` series in dea-catalog-processes is the pilot; T7 in the umbrella programme is the cross-repo cascade). No entity, schema, or id changes; the standard is the normative foundation.
