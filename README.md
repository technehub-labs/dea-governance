# OpenDEA Governance

This repository is the org-wide governance home for OpenDEA. It holds the canonical entity-system, identity, lifecycle, and conformance standards that apply across the `technehub-labs/*` portfolio.

The repository is the home of:

- **DEA-ID-000** - Foundation paper: "Institutionalising a General Entity System for OpenDEA". The architectural philosophy, the 5-concern taxonomy (identity / semantics / relationships / lifecycle / conformance), the authority model, the 7-workstream taxonomy, the 4-phase adoption programme.
- **CR-012** - Org-wide General Entity Governance Standard. The 12 EGV-001..012 normative requirements + 8 deliverables + 6 implementation stages.

`dea-metamodel` is the cross-reference for entity-type definitions; the OpenDEAM Architecture Framework (`dea-architecture-framework`) is the architectural authority. This repository is the governance layer between metamodel and catalogs.

## Authority model

```
OpenDEAM Architecture Framework   (dea-architecture-framework)
  └─ Architectural authority and allocation

Enterprise Concept Framework      (dea-metaframework; ECF)
Canonical Metamodel               (dea-metamodel)
  └─ Conceptual grounding, entity types, properties, relationships

General Entity System             (dea-governance; THIS REPO)
  └─ Shared identity, lifecycle, schemas, references, governance,
     conformance

Business Process Catalog          (dea-catalog-processes)
Other DEA Catalogs                (dea-catalog-*)
  └─ Catalog-specific profiles and instances
```

The general entity system governs identity and conformance across all catalogs; the metamodel governs the conceptual entities; the architecture framework governs the architectural decisions. Catalogs instantiate the metamodel through profiles that conform to the entity system.

## Repository structure

The `registers/` directory holds two registers, each reconciled by `registers/reconcile_portfolio.py` (CR-014, extended by CR-023) against observed reality and against the federation's canonical reference root:

- **`registers/catalog-portfolio.yaml`** — the catalog-portfolio register (CR-013, v12: 54 entries): the org's catalog repositories and the metamodel entity allocations they own.
- **`registers/assessment-model-portfolio.yaml`** — the assessment-model register (CR-023, v1: 8 entries): the federation's maturity-model population, each row binding a canonical id published by the upstream reference catalogue to the repository and immutable release that publish it.

```
dea-governance/
├── README.md                                 # this file
├── CHANGELOG.md                              # release notes
├── CONTRIBUTING.md                           # contribution flow
├── LICENSE                                   # MIT
├── docs/
│   └── design/
│       ├── entity-system-foundation.md       # DEA-ID-000
│       └── entity-system-public-surface.md   # Registry of public surfaces (e.g. lists.technehub.com)
├── registers/
│   ├── catalog-portfolio.yaml                # CR-013: the catalog-portfolio register (R1-R6 population)
│   ├── assessment-model-portfolio.yaml       # CR-023: the assessment-model register (R7-R9 population)
│   └── reconcile_portfolio.py                # CR-014 + CR-023: the reconciler (R1-R9)
├── change-requests/
│   ├── README.md
│   ├── CR-012-org-wide-entity-governance.md  # CR-012 (renumbered from CR-DEA-ID-001)
│   └── ...                                   # future org-wide CRs
├── reconciliation/
│   └── ...                                   # governance cross-references
└── schemas/
    └── ...                                   # common entity envelope schema (CR-012)
```

## Reconciliation rules

`registers/reconcile_portfolio.py` enforces nine rules. Any finding fails the run (exit 1).

| Rule | Check | Population |
|---|---|---|
| R1 completeness | every metamodel `catalog_repo` value appears in the register (the CR-013 maintenance rule) | catalog portfolio |
| R2 existence | registered repos exist; `missing`-registered repos are actually absent | catalog portfolio |
| R3 state truth | registered state matches the observed `CATALOG.yaml` counts | catalog portfolio |
| R4 ownership | every metamodel entity allocated to a registered repo appears in that repo's register entry | catalog portfolio |
| R5 directory-size | no tracked directory holds 800+ entries (the entity-storage-layout §4 shard trigger); 500+ prints a watch | catalog portfolio |
| R6 pin-truth | every metaframework release tag a repo's CI pins actually exists | catalog portfolio |
| R7 canonical binding | **bidirectional**: every register row binds a canonical id the upstream reference catalogue publishes, as a maturity-model reference, at the catalogue's own version; **and** every maturity-model reference the catalogue publishes is claimed by exactly one row (none claims it → unclaimed canonical model; several → ambiguous binding) | assessment models |
| R8 dangling reference | every canonical id the assessment-model register references, and every `source_id`/`target_id` of the upstream relation graph, resolves to an id the upstream reference catalogue publishes | assessment models |
| R9 repo resolution | every assessment-model row resolves to a repository that exists **in the organization that row declares**, at the **immutable release that row declares** | assessment models |

R7 and R8 read the federation's canonical reference root — `technehub-labs/dea-metamodel` → `assessment-models/catalog/reference-catalog.yaml` and `assessment-models/catalog/model-relations.yaml`. The catalogue is the authority for **what** version exists (canonical identity + version); the Assessment-Models registry is the authority for **where** it resolves (the repository pointer). Neither duplicates the other, and the two are reconciled against each other here.

**Organizations are per row, never global.** Every URL the reconciler builds for a register row is built from that row's `organization` value, so one reconciler spans organizations (`Assessment-Models`, `technehub-labs`) without a hard-coded assumption. Rows that declare no organization (the catalog-portfolio population, which predates per-row ownership) fall back to the federation default organization, and R1–R6 behave exactly as before.

Offline mode (no `GITHUB_TOKEN`/`GH_TOKEN`) still enforces R1/R4 from the vendored inputs and skips the API-gated rules R2/R3/R5/R6/R9 with a printed WARN. It never crashes and never passes silently; the same holds for any rule whose upstream input is unreachable. A finding never fires on a transport flake.

## Related repositories

| Repository | Role |
|---|---|
| `dea-architecture-framework` | Architectural authority (ADRs; OpenDEAM root model) |
| `dea-metaframework` | Enterprise Concept Framework (the 7x7 axiom-derived matrix) |
| `dea-metamodel` | Canonical entity types, properties, relationships |
| `dea-catalog-processes` | Business Process catalog (the pilot for CR-012) |
| `dea-catalog-*` (10 more) | Other DEA catalogs |

## Change control

This repository follows the standard `technehub-labs/*` change-request (CR) governance. CRs land verbatim on acceptance via squash-merge PRs to `main`. Normative changes require a CR with `**Admission authority**: yes` and the standard `**Status**`, `**Layer**`, `**Owner**`, `**Date**` headers.

## Owner

Emmanuel A. Otchere (per CR-118 / EGV-008 cardinal rule on authorship-bearing fields).
