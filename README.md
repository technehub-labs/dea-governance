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

```
dea-governance/
├── README.md                                 # this file
├── CHANGELOG.md                              # release notes
├── CONTRIBUTING.md                           # contribution flow
├── LICENSE                                   # MIT
├── docs/
│   └── design/
│       └── entity-system-foundation.md       # DEA-ID-000
├── change-requests/
│   ├── README.md
│   ├── CR-012-org-wide-entity-governance.md  # CR-012 (renumbered from CR-DEA-ID-001)
│   └── ...                                   # future org-wide CRs
├── reconciliation/
│   └── ...                                   # governance cross-references
└── schemas/
    └── ...                                   # common entity envelope schema (CR-012)
```

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
