# Institutionalising a General Entity System for OpenDEA

> **Foundation paper (DEA-ID-000). Advisory.** The architectural philosophy for the OpenDEA General Entity System. The normative standard is CR-012. Pilot implementation: CR-BP-121 in `dea-catalog-processes`.

The objective should be to establish a catalog-wide entity governance system, and then repeat the exercise for each subsequent version.

The distinction is architectural. A versioned catalog describes a particular release of catalog content. An entity system establishes the rules under which all catalog entities are defined, identified, related, validated, evolved, and governed over time.

I recommend treating this as a foundational change to `technehub-labs/dea-catalog-business-processes`, with the same principles reusable across other OpenDEA catalogs.

The governing principle is:

> Entity identity and governance are foundational; catalog versions are managed projections of that foundation.

This means the new system must apply to existing entities, newly admitted entities, future catalog versions, and eventually cross-catalog references. It should not depend on any particular directory such as `entities/v1-alpha`, nor assume that every entity is a business process.

## 1. Establish the entity system as a first-class architectural concern

The general system should define five related but distinct concerns.

### 1.1 Entity identity

What is this entity, and how is it identified persistently?

Canonical identifier, namespace, identity stability, aliases, succession, and retirement.

### 1.2 Entity semantics

What kind of thing is it, and what does it mean?

Canonical type, definition, semantic constraints, specialisation, and authoritative metamodel references.

### 1.3 Entity relationships

How does it relate to other entities?

Composition, specialisation, realisation, dependency, association, and typed reference integrity.

### 1.4 Entity lifecycle

How does it evolve without losing its identity or history?

Admission, modification, reclassification, supersession, deprecation, retirement, and provenance.

### 1.5 Entity conformance

How is compliance enforced consistently?

Schemas, semantic validation, naming rules, reference checks, change control, and continuous integration.

These concerns constitute a reusable system. Process-specific constraints then become a specialised application of that system rather than a separate identity and governance mechanism.

## 2. Establish the authority boundaries

Institutionalisation will fail if the catalog repository becomes the place where every entity rule is independently defined.

The existing OpenDEAM architecture already provides the necessary separation of responsibilities: the metamodel defines canonical entity concepts, the ontology and semantic architecture establish grounding, and catalogs instantiate those definitions.

I would formalise the following authority model.

```
OpenDEAM Architecture Framework   (dea-architecture-framework)
  └─ Architectural authority and allocation

Enterprise Concept Framework      (dea-metaframework; ECF)
Canonical Metamodel               (dea-metamodel)
  └─ Conceptual grounding, entity types, properties, relationships

General Entity System             (dea-governance; THIS PAPER'S SUBJECT)
  └─ Shared identity, lifecycle, schemas, references, governance,
     conformance

Business Process Catalog          (dea-catalog-processes)
Other DEA Catalogs                (dea-catalog-*)
  └─ Catalog-specific profiles and instances
```

The general entity system should be implemented in the business-process repository initially if that is the agreed delivery vehicle, but its normative rules must be reusable and governed at the correct architectural level.

In particular:

- The business-process catalog may define a business-process profile, but must not redefine the canonical `BusinessProcess` concept.
- A catalog may choose its storage format and local file organisation within approved constraints, but must not create its own competing identity semantics.
- Shared identity, lifecycle, and validation rules should be centrally specified, with implementations reusable by other catalogs.
- Cross-catalog references must resolve to authoritative entities, rather than silently creating local duplicates.

## 3. Create a general entity CR programme

Rather than framing the work as CRs for `v1-alpha`, establish a dedicated programme of changes for Entity System Institutionalisation.

The CRs below are proposed titles and sequencing. They should be assigned numbers only after checking the repository's actual CR registry and the scope of existing approved CRs.

| Proposed workstream          | Responsibility                                                                      | Principal outcome                |
| ---------------------------- | ----------------------------------------------------------------------------------- | -------------------------------- |
| Entity System Charter        | Establish scope, principles, authority, and applicability                           | Approved normative foundation    |
| Entity Identity Standard     | Define identity, namespace, aliases, and continuity                                 | Stable entity identification     |
| Entity Contract Standard     | Define common envelope and type-specific profiles                                   | Consistent, typed entity records |
| Entity Relationship Standard | Define typed references, composition, and integrity rules                           | Reliable entity graph            |
| Entity Lifecycle Standard    | Govern admission, change, supersession, and retirement                              | Controlled evolution             |
| Entity Conformance Standard  | Define automated validation and release gates                                       | Enforceable compliance           |
| Entity System Adoption       | Apply the approved standard to the business-process catalog and subsequent catalogs | Operational institutionalisation |

These workstreams can be separate CRs or grouped into a smaller number of CRs according to the existing repository's governance practice. The important point is to distinguish normative decisions from implementation changes.

I recommend four implementation phases.

1. **Foundation and disposition.** Investigate the canonical metamodel, current CR baseline, existing schemas, identifiers, references, and catalog conventions. Produce the entity-system charter and identify any existing rules that already satisfy the requirements.
2. **Normative specification.** Approve the identity, common entity contract, relationship, lifecycle, and conformance rules before bulk catalog changes.
3. **Reference implementation.** Implement shared schemas, validators, tests, ID resolution, and migration tooling in the designated repository. Demonstrate them against representative entities, including existing records and newly proposed entities.
4. **Mandatory adoption.** Require conformance for new and modified entities, migrate existing records according to approved dispositions, and make the same standard an adoption prerequisite for other catalogs.

The last phase is what turns an architecture decision into an institutional capability.

## 4. Design the standard around a universal entity contract

The central technical deliverable should be a General Entity Contract, with specialised contracts derived from it.

The contract should distinguish three different kinds of versioning, which are often conflated:

| Version dimension     | What it governs                                                      | Example                 |
| --------------------- | -------------------------------------------------------------------- | ----------------------- |
| Entity identity       | Which real or conceptual entity is being represented                 | Persistent entity ID    |
| Entity representation | The structure and rules used to encode the entity                    | Entity schema version   |
| Catalog release       | Which collection of entities and relationships is published together | Catalog release version |

An entity should not acquire a new identity merely because its schema or catalog release changes.

### Proposed common entity envelope

Every governed entity should conform to a common envelope, subject to the canonical metamodel and approved schema design.

```yaml
id: <persistent-entity-identifier>
type: <canonical-entity-type>
name: <preferred-human-readable-name>

definition: <normative-meaning>
description: <optional-explanatory-text>

relationships: []
classifications: []
provenance: {}

lifecycle:
  status: <governed-lifecycle-state>
```

This is a conceptual example, not a final schema. In particular, `type`, `relationships`, `classifications`, and `lifecycle` must be reconciled with existing canonical properties rather than introduced as duplicate representations.

The standard should specify which fields are mandatory, which are optional, which are inherited from the canonical metamodel, and which may be extended by a specialised profile.

## 5. Make identity independent of repository layout

For the institutional system, I would adopt these identity principles.

- **Persistent identity:** An entity receives a stable identifier when it is admitted.
- **Canonical typing:** Its type is declared independently of the identifier.
- **Namespace ownership:** The system defines which authority controls identifier allocation.
- **No positional identity:** IDs do not encode catalog version, hierarchy, intent, ECF domain, or mutable classifications.
- **Explicit continuity:** Renames and reclassifications preserve identity when the underlying entity remains the same.
- **Explicit succession:** Splits, mergers, replacements, and retirements preserve historical traceability.
- **Resolvable references:** References use canonical identifiers, with a defined resolution mechanism.
- **Controlled aliases:** Legacy IDs and alternative names remain discoverable through governed mappings.

The exact identifier format should be a consequence of these rules. It should not be the first decision in the programme.

## 6. Institutionalise the rules through CI and governance

The new system should have a conformance gate that runs on every relevant pull request and release.

```
Entity change proposed
  → Identity and schema validation (uniqueness, required properties, type correctness)
  → Semantic and relationship validation (canonical types, valid references, structural invariants)
  → Governance and compatibility validation (approved CR, lifecycle rules, migration and provenance)
  → Conformant entity change (eligible for merge and catalog release)
```

A practical implementation should provide:

- A shared validation library or equivalent reusable tooling.
- Schema validation and canonical metamodel conformance checks.
- Duplicate-ID and broken-reference detection.
- Lifecycle and succession validation.
- A machine-readable catalog manifest or index.
- Negative tests proving that invalid records are rejected.
- CI enforcement, with no silent bypass of mandatory checks.
- A documented migration and compatibility policy.

Do not make every catalog implement these checks independently. Establish one reusable conformance mechanism, then allow each catalog to supply its own type-specific constraints.

## 7. Define success by adoption, not by migration completion

The programme should be considered successful when:

1. The entity system has an approved normative specification.
2. The identifier and lifecycle policies are implemented and tested.
3. New entities cannot enter the governed catalog without satisfying the standard.
4. Existing entities have been reconciled under the same rules, regardless of their original version.
5. Catalog-specific profiles derive from canonical entity definitions.
6. Cross-catalog references can be resolved and validated.
7. Other catalogs can adopt the system without redesigning identity, lifecycle, and conformance from scratch.
8. Repository maintainers can determine which rules are normative, which are implementation details, and which require a new CR to change.

The ultimate test is whether a future catalog can be established using the entity system without having to invent another ID convention, lifecycle model, or validation framework.

## Recommended next step

Start with a General Entity System Recon and Charter CR in `dea-catalog-business-processes`, governed by the repository's existing CR process. Its purpose should be to establish the normative scope, inspect the current baseline, map existing decisions, identify unresolved design questions, and propose the implementation CR sequence.

Do not begin by renumbering records or introducing a new directory layout.

The first CR should produce four concrete outputs:

- **Entity System Charter:** scope, principles, authority, and applicability across catalog families.
- **Existing Decisions and Gap Register:** what is already established, what can be reused, and what needs a new decision.
- **Normative Design Proposal:** identity, entity contracts, relationships, lifecycle, and conformance.
- **Implementation and Adoption Plan:** ordered CRs, acceptance criteria, migration policy, and CI enforcement.

That approach preserves the repository's governance discipline while moving from a collection of versioned entity records to a governed, reusable entity system.
