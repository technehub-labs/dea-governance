# Changelog

All notable changes to this repository are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
