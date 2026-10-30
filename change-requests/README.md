# Change Requests: OpenDEA Governance

This index tracks every change request that lands on the `dea-governance` repository. The repo is the org-wide governance home; CRs here are normative standards that apply across the `technehub-labs/*` portfolio.

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-012](CR-012-org-wide-entity-governance.md) | Org-Wide General Entity Governance Standard | **Proposed (this PR)** | The 12 EGV-001..012 normative requirements + 8 deliverables + 6 implementation stages. Establishes identity, contract, relationships, lifecycle, and conformance requirements for the OpenDEA portfolio. Renumbered from CR-DEA-ID-001. Foundation paper: [DEA-ID-000](../docs/design/entity-system-foundation.md). Pilot implementation: CR-BP-121 in dea-catalog-processes. |
| [DEA-ID-000](../docs/design/entity-system-foundation.md) | General Entity System Foundation Paper | **Advisory** (this PR) | The architectural philosophy, 5-concern taxonomy, authority model, 7-workstream taxonomy, 4-phase adoption programme. Not normative; the foundation for CR-012. |
| [CR-014](CR-014-org-portfolio-reconciliation-ci.md) | Org-Level Portfolio Reconciliation CI | **Proposed (this PR)** | `registers/reconcile_portfolio.py` (R1 completeness, R2 existence, R3 state truth, R4 ownership) + weekly `reconcile-portfolio.yml` + basic repo CI (parse + authorship, the governance repo's first CI). First run detected and refreshed real drift: dea-catalog-processes observed populated (3,722 canonical) vs the 2026-10-30 skeleton snapshot; register_version 2. Process note: landed by direct push (operator error; correction recorded in the follow-up PR). |
