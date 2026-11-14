# CR-023: Assessment-Model Federation Reconciliation (New Register, R7/R8/R9)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-14
**Admission authority**: yes (new register + reconciler rules)
**Depends on**: CR-013 (the catalog-portfolio register); CR-014 (the reconciler and its CI); CR-021 (R6, the most recent reconciler rule)
**Companion**: the federation's canonical reference root — `technehub-labs/dea-metamodel` → `assessment-models/catalog/reference-catalog.yaml` and `assessment-models/catalog/model-relations.yaml`; the parallel publication of `technehub-labs/maturity-model-ea-capability`

## 1. Problem Statement

The federation's assessment-model population is reconciled against its canonical reference root by nobody. Two artefacts carry the truth and they are held in different organizations:

- the **reference catalogue** (`dea-metamodel` → `assessment-models/catalog/reference-catalog.yaml`) is the authority for **what** exists: the canonical id and the version under that id for every maturity model;
- the **registry** (`Assessment-Models/assessment-registry` → `registry/maturity-models/*.yaml`) is the authority for **where** it resolves: the repository pointer.

`dea-governance` holds neither. It holds the catalog-portfolio register (CR-013) and the reconciler that keeps it honest (CR-014), and nothing that binds the assessment-model population to the reference root. Three consequences follow.

1. **A register row can drift from the catalogue silently.** Nothing compares a declared canonical version with the catalogue's version for the same canonical id, so a model published at 1.0.0 upstream and recorded as 1.0.1 here is invisible until a consumer notices.
2. **A published model can be dropped from the federation.** The catalogue publishes a maturity model that no register row claims; nothing notices that the federation has lost track of it.
3. **A relation-graph endpoint can dangle.** The upstream relation graph (`model-relations.yaml`) declares edges between canonical maturity-model ids; if an endpoint names an id the catalogue does not publish, the graph carries a reference that resolves to nothing.

Two further defects make the reconciler unable to see any of this even if it tried.

4. **The org is hard-coded.** `registers/reconcile_portfolio.py` carries `ORG = "technehub-labs"` at module level and uses it in **every** API and `raw.githubusercontent` URL. A register row cannot name a repository in another organization — and the assessment-model population is spread across two (`Assessment-Models` for the seven published models, `technehub-labs` for the EA-capability model the org itself owns). The constant is an assumption, not a default.

5. **The register itself does not exist.** There is no `registers/assessment-model-portfolio.yaml`: no row declares a repository, its owning organization, its canonical id, its canonical version, its release, or its ratification date.

## 2. Change

### 2.1 New register: `registers/assessment-model-portfolio.yaml`

A second register, alongside the catalog-portfolio register, seeded with the federation's current maturity-model population (8 rows). Top level: `register_version` (int), `snapshot_date` (date), `ratified_by` (string), `models` (list). Every model row carries:

| Field | Meaning |
|---|---|
| `repo` | repository name (no organization prefix) |
| `organization` | **the GitHub organization that OWNS the repository** — the value every URL for that row is built from |
| `canonical_id` | the federation-wide canonical reference id published by the upstream catalogue (e.g. `dea:maturity-technology`) |
| `canonical_version` | the version published under that canonical id |
| `state` | `published` (the repository and its release resolve) or `pending` (declared, pointer in flight) |
| `release` | the immutable release reference (git tag `vX.Y.Z`) |
| `ratified` | the date this register first recorded the model |

Seed population:

| repo | organization | canonical_id | version | release | state |
|---|---|---|---|---|---|
| maturity-model-technology | Assessment-Models | dea:maturity-technology | 1.0.0 | v1.0.0 | published |
| maturity-model-modernization | Assessment-Models | dea:maturity-modernization | 1.0.0 | v1.0.0 | published |
| maturity-model-operations | Assessment-Models | dea:maturity-operations | 1.0.0 | v1.0.0 | published |
| maturity-model-services-delivery | Assessment-Models | dea:maturity-services-delivery | 1.0.0 | v1.0.0 | published |
| maturity-model-autonomous-operations | Assessment-Models | dea:maturity-autonomous-operations | 1.0.1 | v1.0.1 | published |
| maturity-model-digital-transformation-operationalized | Assessment-Models | dea:maturity-digital-transformation-operationalized | 1.0.1 | v1.0.1 | published |
| maturity-model-digital-transformation | Assessment-Models | dea:maturity-digital-transformation | 1.0.0 | v1.0.0 | published |
| maturity-model-ea-capability | technehub-labs | dea:maturity-ea-capability | 1.0.0 | v1.0.0 | pending |

`organization` is the org that owns the repo, not the org that curates it. The seven Assessment-Models models are owned by `Assessment-Models`; the EA-capability model — the DEA-owned model that anchors the federation's dotted line — is owned by `technehub-labs`.

The `state: pending` row is the EA-capability model, whose repository is published in parallel by the owning workstream. **`pending` is not an exemption.** A row whose repository does not resolve is still reported as a finding (R9); `pending` records a known, in-flight pointer, it never silences the finding. On the day this CR is proposed the repository does not yet exist on `technehub-labs`, so **R9 reports one expected finding** — the reconciler reports it rather than crashing, and the finding clears by itself the moment the parallel publication lands.

### 2.2 Per-row organizations (the org stops being a global assumption)

`ORG` is retired as an assumption and becomes `DEFAULT_ORG` — a **fallback used only for register rows that declare no `organization` of their own**. Every URL the reconciler builds for a row is built from that row's `organization`: `api.github.com/repos/{org}/{repo}`, `raw.githubusercontent.com/{org}/{repo}/...`, and the git-trees / git-refs routes.

The catalog-portfolio population predates per-row ownership and carries no `organization` field, so it falls back to `DEFAULT_ORG` and **R1–R6 behave exactly as before** — no rule was rewritten, no register row was touched (`registers/catalog-portfolio.yaml` is unchanged). The assessment-model population declares its owning organization per row, which is what lets one reconciler span `Assessment-Models` and `technehub-labs` without a hard-coded assumption.

### 2.3 R7 — canonical binding agreement (bidirectional)

The register and the upstream catalogue must agree on canonical identity, in **both** directions:

- **row → catalogue**: every register row binds a canonical id the catalogue publishes, as a `kind: maturity-model` reference, at the catalogue's own version. A row naming an unpublished id, binding a non-maturity-model kind, or disagreeing on the version is a finding.
- **catalogue → row**: every `kind: maturity-model` reference the catalogue publishes is claimed by **exactly one** register row. Zero claims → *unclaimed canonical model*. Two or more claims → *ambiguous binding*.

Both directions are needed. One direction alone catches half the drift class: forward-only misses a catalogue model the register dropped; backward-only misses a row that binds the wrong version.

### 2.4 R8 — no dangling catalogue reference

Every canonical id the assessment-model register references, and every `source_id`/`target_id` of the upstream relation graph's edges, must resolve to an id the upstream reference catalogue publishes. A dangling id is a finding.

### 2.5 R9 — repo resolution

Every assessment-model row resolves to a repository that **exists in the organization that row declares**, at the **immutable release that row declares**. Both halves are checked against the row's own organization and release, never against a global assumption.

### 2.6 Offline behaviour, and the flake rule

- Offline mode (no `GITHUB_TOKEN`/`GH_TOKEN`) still enforces R1/R4 from the vendored inputs and **skips the API-gated rules R2/R3/R5/R6/R9 with a printed WARN** — it never crashes and never passes silently.
- R7/R8 read the **public** upstream reference root over `raw.githubusercontent`, so they run whenever that root is reachable, with or without a credential. When it is not reachable, the affected rule is **skipped with a printed WARN** — a rule that cannot read its inputs never passes silently.
- The existing retry-on-transport-flake behaviour is kept: a finding never fires on a transport flake. R9 distinguishes a **definitive** HTTP 404 (the thing is absent → finding) from a transport failure (unreadable → WARN and skip) and from a 403 (exists but invisible to this credential → WARN and skip, the CR-022A private-repo class).

### 2.7 Tests

`registers/test_reconcile_canonical_bindings.py` (new, 18 tests) unit-tests the rule semantics offline against fixtures shaped like the real upstream artefacts. The rule bodies are pure functions — `check_canonical_bindings(rows, catalogue_refs)`, `check_relation_endpoints(catalogue_ids, edges)`, `check_register_references(catalogue_ids, rows)` — so the semantics are testable without a network or a token. Covered: a matching row passes; a version mismatch is a finding; an unclaimed catalogue maturity model is a finding; two rows claiming one canonical id is a finding; an unknown canonical id is a finding; a non-maturity-model binding is a finding; a relation edge pointing at an absent id is a finding; a relation edge pointing at a present id is not; the register-side dangling id is a finding; and the per-row organization resolution (a row's org is used; a row without one falls back to the default).

The existing `test_reconcile_directory_counts.py` (R5) and `test_reconcile_pins.py` (R6) are unchanged and still pass.

## 3. What this CR does NOT decide

1. **No capability-level join.** The relation graph's comparability surface is model-score-level only, because no two capability maturity models share a capability id or a measure id (the shared coordinate system is the band anchor `dea:maturity-bands-v2`). R7 and R8 verify that references **resolve**; they assert nothing about a capability-level correlation, and no finding here implies one exists.
2. **No repository-layout requirement on the other organization.** Cross-organization dependencies are contractual. The reconciler READS published artefacts; it does not require `Assessment-Models` to change its repository layout, nor the upstream root to change its catalogue shape.
3. **No duplication of the two authorities.** The catalogue remains the authority for what version exists; the Assessment-Models registry remains the authority for where it resolves. This register records the pointer; it does not redefine a canonical id or a canonical version.
4. **No change to the catalog-portfolio register.** `registers/catalog-portfolio.yaml` and the R1–R6 population are untouched.
5. **No merge.** This PR is opened for review; the parent task merges after review.

## 4. Verification

1. `python3 -m pytest registers/ -q` — all tests pass (25 passed), including the 21 new ones and the pre-existing R5/R6 suites.
2. **R7 fires**: with an intentional version mismatch injected into a **temp copy** of the register (never the committed file), the reconciler reports `FAIL: R7: maturity-model-technology binds canonical id dea:maturity-technology at version 9.9.9 but the upstream catalogue publishes version 1.0.0`.
3. **R8 fires**: with a dangling relation endpoint injected into a **temp copy** of the upstream relation graph, the reconciler reports `FAIL: R8: relation edge dea:edge-ea-capability-supports-technology target_id dea:maturity-does-not-exist does not resolve in the upstream reference catalogue`.
4. Live run against the real upstream catalogue and relation graph: R7 and R8 are clean against the published population (8 rows, 8 catalogue maturity-model references, every relation endpoint resolving); R9 reports the one expected finding for the not-yet-published `technehub-labs/maturity-model-ea-capability`.

## 5. Acceptance Criteria

1. `registers/assessment-model-portfolio.yaml` exists with the schema in §2.1 and the 8-row population in §2.1.
2. No global org assumption remains in the reconciler; every row-scoped URL is built from that row's `organization`.
3. R7 is bidirectional (row→catalogue and catalogue→row) and R8 checks both the register side and the relation-graph side.
4. Offline mode runs R1/R4 and skips the API-gated rules with a printed WARN; it never crashes and never passes silently.
5. A finding never fires on a transport flake.
6. `python3 -m pytest registers/ -q` passes.
7. `README.md` documents R7 and R8 (and the new register); `change-requests/README.md` indexes this CR; `CHANGELOG.md` records the change.

## 6. Named Follow-up

- When the parallel publication of `technehub-labs/maturity-model-ea-capability` lands, the R9 finding for that row clears with no register edit. If the repository lands under a different name or organization, the register row — not the rule — is what must be corrected.
- The `state` vocabulary (`published` / `pending`) is deliberately coarse. If the federation needs a third state (e.g. `retired`, for a model the catalogue still publishes but the org no longer maintains), that is a register-schema CR, not a reconciler change.
