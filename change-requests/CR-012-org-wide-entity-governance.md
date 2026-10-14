# CR-012: Org-Wide General Entity Governance Standard

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Admission authority**: yes
**Depends on**: DEA-ID-000 (foundation paper, `docs/design/entity-system-foundation.md`)
**Companion**: CR-BP-121 in `dea-catalog-business-processes` (the pilot implementation)

## 1. Problem Statement

OpenDEAM maintains a portfolio of interoperable models and catalogs representing enterprise architecture concepts, including business capabilities, processes, information, technology, and related architectural concerns.

These assets require a consistent and enforceable means of establishing entity identity, defining canonical entity types, maintaining references between entities, governing lifecycle transitions, and preserving identity across revisions and catalog evolution.

Without a portfolio-wide governance standard, individual repositories may introduce incompatible identification conventions, duplicate entities, ambiguous references, incompatible lifecycle practices, or repository-specific assumptions about entity identity. Such divergence weakens cross-catalog interoperability, model integrity, traceability, and automated conformance.

This change establishes a normative General Entity Governance Standard applicable across OpenDEAM. It defines mandatory governance requirements and assigns conformance responsibilities to the metamodel, applicable catalog repositories, and supporting tooling.

## 2. Objective

Establish one authoritative, implementation-independent governance standard for identifying, defining, referencing, evolving, and validating entities throughout the OpenDEAM portfolio.

The standard SHALL ensure that:

1. Each governed entity has a stable and unambiguous identity.
2. Entity identity is independent of mutable names, descriptions, classifications, hierarchy positions, and catalog release versions.
3. Canonical entity types and their structural contracts are governed by the metamodel.
4. Relationships and references between entities are explicit, valid, and traceable.
5. Entity lifecycle and identity continuity are governed consistently.
6. Catalogs conform to the common governance requirements while retaining their domain-specific semantics.
7. Conformance is machine-verifiable wherever the requirement can be expressed as a deterministic rule.
8. New and modified assets cannot silently bypass applicable governance requirements.

## 3. Normative Requirements

### EGV-001: Canonical Governance Authority

The OpenDEAM metamodel SHALL be the canonical authority for common entity governance contracts, shared identity rules, applicable structural constraints, and cross-catalog conformance requirements.

Catalog repositories MAY define domain-specific entity types and constraints only within the boundaries established by the canonical metamodel and applicable architectural decisions.

### EGV-002: Stable Entity Identity

Every governed entity SHALL possess a persistent identifier that distinguishes it from other entities within its declared identity scope.

An entity identifier SHALL NOT derive its continued validity from a mutable entity name, description, hierarchy position, classification, intent, or framework coordinate.

The identifier allocation policy SHALL explicitly define uniqueness scope, collision prevention, and canonical reference construction.

### EGV-003: Identifier and Namespace Governance

The standard SHALL define how identifiers are allocated, represented, validated, and referenced across repositories.

It SHALL determine whether portfolio-wide uniqueness is achieved through globally unique identifiers, namespace-scoped identifiers combined with canonical URIs, or another explicitly justified policy.

Catalog-specific prefixes or identifier formats SHALL NOT be treated as approved merely because a repository already uses them.

### EGV-004: Identity Continuity

Changes to an entity's mutable attributes SHALL NOT, by themselves, create a new entity identity.

Entity renaming, reclassification, relocation, restructuring, and other revisions SHALL preserve identity where the underlying entity remains the same.

Where an entity is split, merged, superseded, replaced, or determined to be semantically distinct, the applicable transition SHALL be explicitly recorded with appropriate provenance and relationship semantics.

Identifiers SHALL NOT be silently reassigned to different entities.

### EGV-005: Canonical Entity Contract

Each governed entity type SHALL have an explicit contract appropriate to its role in the metamodel or a conformant catalog.

The contract SHALL specify applicable identity requirements, required attributes, structural constraints, relationship constraints, lifecycle rules, and validation requirements.

The standard SHALL distinguish universal entity requirements from requirements that apply only to particular entity types.

### EGV-006: Relationship and Reference Integrity

Relationships between governed entities SHALL conform to canonical relationship definitions and applicable domain constraints.

References SHALL resolve to valid entities within the declared identity scope. Relationship endpoints, direction, cardinality, and other constraints SHALL be validated wherever specified by the metamodel.

A repository SHALL NOT introduce a competing definition of a canonical relationship without an approved normative change.

### EGV-007: Version and Lifecycle Separation

The governance model SHALL distinguish:

- **Entity identity:** the persistent identity of the entity.
- **Entity revision:** a particular state or revision of that entity.
- **Schema version:** the version of the structural contract used to represent or validate it.
- **Catalog release:** the published state of the catalog containing the entity.

These concepts SHALL NOT be conflated in identifier allocation or reference resolution.

Lifecycle states, permitted transitions, retirement, supersession, and historical traceability SHALL be explicitly governed.

### EGV-008: Provenance and Traceability

Governed entities and identity-affecting transitions SHALL retain sufficient provenance to support traceability, audit, and controlled evolution.

Where applicable, provenance SHALL identify the originating or governing repository, change authority, relevant change request, and supersession or migration history.

The authorship cardinal rule (per CR-118) applies: every authorship-bearing field in any governed artifact SHALL carry `Emmanuel A. Otchere` (or `TechNeHub Labs` for org-level CITATION.cff). The authoring-tool denylist applies to all governed artifacts.

### EGV-009: Catalog Conformance

Each applicable catalog repository SHALL adopt the General Entity Governance Standard through a scoped adoption change.

Catalog-specific contracts MAY extend common requirements but SHALL NOT weaken mandatory requirements or redefine canonical identity semantics.

Adoption SHALL include an assessment of existing assets, identified gaps, migration implications, and a conformance plan.

### EGV-010: Machine-Verifiable Conformance

The OpenDEAM tooling and validation architecture SHALL provide reusable conformance checks for the requirements that can be evaluated deterministically.

Checks SHALL cover, as applicable:

- Identifier presence, format, scope, and uniqueness.
- Required entity-contract fields and schema validity.
- Referential integrity and relationship constraints.
- Invalid or conflicting lifecycle states.
- Duplicate identities and prohibited identifier reuse.
- Catalog-specific violations of common governance rules.

Validation results SHALL be suitable for automated integration into repository CI.

### EGV-011: Change Enforcement

Changes to governed assets SHALL be subject to the applicable conformance checks.

New or modified entities and relationships that violate mandatory requirements SHALL NOT be accepted as conformant.

Any exception mechanism, if required, SHALL be explicitly governed, bounded in scope, documented, and auditable. Exceptions SHALL NOT silently alter the normative standard.

### EGV-012: Legacy Reconciliation

Existing catalog content SHALL be assessed against the approved standard.

Legacy entities SHALL NOT be bulk-renumbered, deleted, or semantically redefined solely to satisfy a proposed identifier convention.

Reconciliation SHALL preserve identity and references wherever the underlying entity remains the same. Any required mapping, migration, alias, deprecation, or replacement SHALL be governed by an approved implementation change.

## 4. Required Deliverables

Approval of this CR SHALL establish the requirement to produce and maintain:

1. A canonical General Entity Governance Standard (this document).
2. An approved identifier and namespace policy (per the Entity Identity Standard workstream in DEA-ID-000 §3).
3. A common entity contract and applicable relationship-integrity rules (per the Entity Contract Standard workstream).
4. Explicit lifecycle, revision, and identity-continuity rules (per the Entity Lifecycle Standard workstream).
5. Reusable machine-readable conformance constraints and validation procedures (per the Entity Conformance Standard workstream).
6. Catalog adoption requirements and a portfolio conformance register.
7. A controlled legacy-reconciliation and migration approach (per EGV-012).
8. Repository-level enforcement and implementation changes linked to this CR (the pilot: CR-BP-121 in `dea-catalog-business-processes`; the cascade: T7 of the umbrella programme).

The normative specification and implementation artifacts SHALL be version-controlled. The approved specification SHALL be the authoritative interpretation of the requirements established by this change.

## 5. Implementation Strategy

Implementation SHALL proceed through controlled stages:

1. **Foundation specification** (CR-BP-121 Stage 1 + 2): resolve identity, namespace, entity contract, relationship, lifecycle, and conformance decisions in the pilot catalog. Produces the 4 Stage-1 doc outputs (Charter, Existing Decisions Register, Normative Design Proposal, Implementation Plan) plus the 5 spec documents.
2. **Reference implementation** (CR-BP-121 Stage 3-4): validate the standard against representative catalog entities and cross-catalog references. Ships the entity-system gate, registry, tests, and CI workflow in `dea-catalog-business-processes`.
3. **Catalog adoption** (CR-BP-121 Stage 5 + 6): introduce scoped adoption changes in `dea-catalog-business-processes`. The pilot institutionalises the standard as the mandatory entity-governance baseline.
4. **Automated enforcement** (T7 of the umbrella programme): cascade to the 11 sibling catalogs using the per-repo gate-copy + registry pattern (mirrors the 118b cascade). Each repo gets its own slice number (BC-04, BO-04, OU-04, MF-010, MM-06, AF-04, ACT-02, BL-02, CON-02, STA-07, TEN-02).
5. **Legacy reconciliation** (T8 of the umbrella programme): address existing nonconformant assets through approved migration changes. EGV-012 governs: no bulk renames; per-record disposition register; reconciliation mappings in `reconciliation/migration-id-map.yaml` per repo.
6. **Portfolio enforcement** (T8+): make conformance a mandatory acceptance criterion for applicable future changes across the OpenDEA portfolio.

The order of stages MAY be adjusted through an approved implementation plan, but implementation SHALL NOT bypass unresolved normative decisions by treating provisional conventions as approved policy.

## 6. Acceptance Criteria

This CR SHALL be considered implemented when:

- The canonical governance specification has been approved and published (this document).
- Identifier and namespace semantics are explicit and testable (per the Entity Identity Standard).
- Entity identity is separated from entity revision, schema version, and catalog release (per EGV-007).
- Canonical entity and relationship contracts are documented and machine-readable where appropriate (per the Entity Contract Standard).
- Reference integrity and identity continuity have executable conformance checks (per the Entity Conformance Standard).
- At least one reference catalog demonstrates successful adoption, including cross-catalog reference validation where applicable (the pilot: `dea-catalog-business-processes` via CR-BP-121).
- Applicable repositories have an adoption or migration disposition (T7 cascade in progress).
- CI enforcement is active for the agreed mandatory conformance rules (per the 118b-style gate + workflow pattern).
- Normative decisions, implementation changes, and exceptions are traceable to their governing records.

Approval of this CR establishes the normative obligation. Completion of all implementation stages may require separately approved, traceable changes.

## 7. Non-Goals

This CR SHALL NOT, by itself:

- Define or invent new business capabilities, processes, or other domain entities.
- Mandate a particular identifier string format before the identifier policy is approved.
- Require indiscriminate renumbering of existing catalogs.
- Replace the architecture framework, metaframework, ontology, or semantic architecture.
- Collapse repository-specific catalog lifecycles into one release lifecycle.
- Prescribe a particular programming language, database, serialization format, or validation tool unless separately approved.
- Authorize unreviewed structural changes merely because they are necessary to implement the standard.

## 8. Governance and Dependencies

This CR SHALL be linked to the relevant Architecture Decision Record or Records establishing the architectural rationale, authority boundaries, and consequences of the General Entity Governance Standard. The OpenDEAM Architecture Framework (`dea-architecture-framework`) owns architectural decisions; the metamodel (`dea-metamodel`) owns entity-type definitions; this repository (`dea-governance`) owns identity, lifecycle, and conformance rules.

Dependent implementation and catalog-adoption changes SHALL reference this CR and any applicable normative specification.

Where an existing approved decision conflicts with this proposal, the conflict SHALL be identified and resolved through the established governance process rather than silently overridden.

## 9. Authority Boundaries

The EGV-001..012 requirements presume the following separation of authority (per DEA-ID-000 §2):

| Authority | Repository | EGV-001..012 alignment |
|---|---|---|
| Architectural authority | `dea-architecture-framework` | ADRs that resolve architecture-level conflicts |
| Entity-type definitions | `dea-metamodel` | EGV-005 (canonical entity contract) source-of-truth |
| Entity-system standard | `dea-governance` (this repo) | EGV-001..012 normative rules |
| Catalog-specific profiles | `dea-catalog-*` (per-repo) | EGV-009 (catalog conformance) + per-repo profile |

The General Entity System governs identity, lifecycle, and conformance across the OpenDEA portfolio. The metamodel governs the conceptual entities (entity types, properties, relationships). The architecture framework governs the architectural decisions (ADRs). Catalogs instantiate the metamodel through profiles that conform to the entity system.

## 10. Expected Outcome

OpenDEAM has a single, enforceable governance foundation for entity identity and integrity across its catalog portfolio. Catalogs remain semantically distinct but interoperable through consistent identity, relationship, lifecycle, and conformance rules.

The principal outcome is institutionalisation: a governed, testable, reusable entity system that can be adopted by any current or future `technehub-labs/*` catalog without independent reinvention of identity, lifecycle, or conformance.
