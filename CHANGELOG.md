# Changelog

All notable changes to this repository are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### CR-014: Org-Level Portfolio Reconciliation CI

`registers/reconcile_portfolio.py` + weekly workflow: the CR-013 register is reconciled against the metamodel allocations and GitHub reality (R1-R4), failing on drift. Basic repository CI (parse + authorship) added - the governance repo's first. First reconciler run detected real drift within 48 hours of the manual snapshot: dea-catalog-processes is populated (3,722 canonical), not skeleton; register refreshed to v2 (2026-11-02).

### CR-013: Catalog Portfolio and Ownership Register

Establishes `registers/catalog-portfolio.yaml` covering all 43 catalog repositories named by metamodel `catalog_repo` values (entity allocations, observed state at the 2026-10-30 audit, ratification dates). Ratifies `dea-catalog-information-assets` at creation; names the naming-drift (processes, services) and stale-existing (BusinessService, SolutionComponent, PerformanceMetric) follow-ups; adds the register maintenance rule for future catalog creations. Companion to metamodel CR-MET-014.

### DEA-ID-000: General Entity System Foundation Paper

Landing of the OpenDEA entity-system foundation paper in `docs/design/entity-system-foundation.md`. The architectural philosophy, 5-concern taxonomy (identity / semantics / relationships / lifecycle / conformance), authority model (Architecture Framework → ECF/Metamodel → General Entity System → Catalogs), 7-workstream taxonomy, 4-phase adoption programme. The paper is the philosophical foundation for the entity-system programme; CR-012 is the normative CR that operationalises it. No entity, schema, or id changes; the foundation paper is advisory.

### CR-012: Org-Wide General Entity Governance Standard (renumbered from CR-DEA-ID-001)

The org-wide normative CR establishing the 12 EGV-001..012 requirements for entity governance across the `technehub-labs/*` portfolio. 8 deliverables + 6 implementation stages. The standard applies to all OpenDEA foundation models, reference catalogs, schemas, specifications, tooling, validation pipelines, and derived architectural assets. Adoption by individual catalog repos happens through scoped adoption CRs (the `CR-BP-121` series in dea-catalog-processes is the pilot; T7 in the umbrella programme is the cross-repo cascade). No entity, schema, or id changes; the standard is the normative foundation.
