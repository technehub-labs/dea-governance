# CR-022: Register v12 — Repo Renames, Census Completion, Index-Truth Verdict

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-12
**Admission authority**: yes (register refresh)
**Depends on**: CR-013 (the register and its maintenance rule); CR-MET-022 in dea-metamodel (the catalog_repo repoint that must land first); CR-016 (the undercount-correction precedent for recording observational-truth verdicts); the 2026-11-11/12 org portfolio sweep (observation source)
**Lands after**: CR-MET-022 (dea-metamodel) — merge-ordering constraint, see §2

## 1. Problem Statement

The 2026-11-11/12 exhaustive portfolio sweep (77 repos, full local coverage) confirmed three truths the register v11 does not yet record:

1. **Two register row keys are stale repo names.** GitHub renames are live: `dea-catalog-digital-business-service-factory` → `dea-catalog-business-services` and `dea-catalog-processes` → `dea-catalog-business-processes`. The old names survive only as redirects; v11 keys rows by the old names. CR-013 §4 finding 1 named this drift; CR-MET-014 §6.2 pre-authorized the per-entity-verified repoint (landed as metamodel CR-MET-022). The processes row also still says the canonical-home question "remains a named follow-up" — the rename resolves it: `dea-catalog-business-processes` is the home (3,723-record corpus, v0.5.0 released 2026-11-07, CR-BP-30h).
2. **Ten org catalog-named repositories are unregistered**, contrary to the spirit of the CR-013 §5 maintenance rule ("a new catalog repository MUST be recorded in the same programme that creates it"): `dea-catalog-agent-foundry`, `dea-catalog-ontologies`, `dea-catalog-reference-architecture`, `dea-catalog-references`, `dea-catalog-solution-hub`, `dea-catalog-information-system-services` (no catalog layout yet), `dea-catalog-infrastructure-components`, `dea-catalog-integration-interfaces` (empty repositories on origin), `dea-catalog-taxonomy`, `dea-catalog-permission-probe` (archived; probe empty). v11's declared scope (CR-013 §3) was the repos named by metamodel `catalog_repo` values; none of these ten carries an allocation, which is exactly why they fell through. This CR broadens the scope to **all org catalog-named repositories** and says so.
3. **The processes index-truth question needs a recorded verdict.** The sweep flagged the combination "index `canonical: 3722` + record files `lifecycle_status: candidate`" as a possible inverted CR-SVC-016-family defect. Investigation (CR-022 §4) found **no defect**: in that repo the two fields are independent axes. The verdict must be recorded in the register so future reconcilers and sweeps do not re-flag it (CR-016 precedent).

## 2. Objective

Bump the register to **v12** (`snapshot_date: '2026-11-12'`) with:

1. **Row-key renames (2)**, in place, history preserved in notes:
   - `dea-catalog-digital-business-service-factory` → `dea-catalog-business-services`
   - `dea-catalog-processes` → `dea-catalog-business-processes`
2. **Ten new entries** (state `skeleton`, `canonical_count: 0`, `entities: []`), each with a note recording its sweep-observed condition (no layout / empty repo / archived).
3. **Schema note (informational)**: an optional `archived: true` key on the two archived entries, documented in the file header comment; the reconciler reads only its known keys, so this is inert.
4. **Row order**: the catalogs section is now alphabetical by `repo` (it was de-facto alphabetical; the renames would otherwise leave `business-*` rows parked under "d" and "p").
5. **The index-truth verdict** recorded verbatim in the processes row's notes.

Ordering constraint: **this CR lands after metamodel CR-MET-022**. Reconciler R1 requires every metamodel `catalog_repo` value to be a registered repo name; until CR-MET-022 merges, the metamodel still points at the old names, which v12 no longer registers. Landing metamodel-first keeps R1 green in every window (CR-017 window precedent; this PR's push to `main` triggers the weekly reconciler immediately via the `registers/**` path filter).

## 3. Register Changes

| Row | Change | Note content |
|---|---|---|
| `dea-catalog-business-services` (renamed from `…-digital-business-service-factory`) | key rename; state/count unchanged (populated/535) | rename + CR-SVC-016 index-truth history (carried from v11 CR-020 note) |
| `dea-catalog-business-processes` (renamed from `dea-catalog-processes`) | key rename; state/count unchanged (populated/3722) | rename + canonical-home resolution + §4 index-truth verdict |
| `dea-catalog-agent-foundry` | new | no catalog layout yet ("Agent Foundry — catalogue of autonomous agent patterns"); no allocation |
| `dea-catalog-ontologies` | new | no catalog layout yet (domain OWL/RDF ontologies); no allocation |
| `dea-catalog-reference-architecture` | new | no catalog layout yet (reference model); no allocation |
| `dea-catalog-references` | new | no catalog layout yet (IANA reference registry); no allocation |
| `dea-catalog-solution-hub` | new | no catalog layout yet (solution archetypes); no allocation |
| `dea-catalog-information-system-services` | new | no catalog layout yet (owner CR-IS-CAT-03A foundation; ISS catalogue); no allocation |
| `dea-catalog-infrastructure-components` | new | empty repository on origin (created 2026-10-19, never initialized); no allocation |
| `dea-catalog-integration-interfaces` | new | empty repository on origin (created 2026-10-19, never initialized); no allocation |
| `dea-catalog-taxonomy` | new, `archived: true` | archived (ADR-0004 D2: Taxonomy Node merged into Concept); completeness only |
| `dea-catalog-permission-probe` | new, `archived: true` | archived + empty (transient Path Y probe); completeness only |

Register totals: 44 → **54 entries**. Registered-but-skeleton rises 26 → 36; populated stays 18.

## 4. Verification (including the index-truth investigation)

The processes verdict recorded in the renamed row's notes, with mechanical evidence gathered 2026-11-12 against the local sync of `dea-catalog-business-processes` @ origin `main`:

1. **Index/files agreement**: `python3 scripts/regenerate_catalog.py --catalog-root . --check` → `OK: …/CATALOG.yaml is current`, exit 0. The index is byte-identical to the regenerator's output (and CI enforces this continuously via the same check, exit 3 on drift — ci.yml lines 96–98). The index cannot disagree with the files.
2. **State semantics**: `infer_state()` (vendored `scripts/regenerate_catalog.py` lines ~257–261) maps any parseable record under the entities tree to `state: canonical` unless its top-level `lifecycle_status` is `deprecated`/`retired` — a containment-slot axis. `lifecycle_status` is copied verbatim from the record (line ~387); the record-level vocabulary is CR-BP-34c LCM-001 `{draft, proposed, validated, published, deprecated, retired}` ∪ legacy `candidate` — **`active` is not in this repo's record vocabulary**, so "canonical ⇒ active" (other catalogs' convention) does not apply here. 3,714 `candidate` + 8 template-older PC records (index `unknown`) + 1 `deprecated` = 3,723 = index `entities` = 3,722 canonical + 1 retired. Exact agreement.
3. **Release truth**: `git cat-file -p v0.5.0` → tag object → commit `3fdddb8c151fa0b1c1d15d08fd06b5c9359e71c0`, the CR-BP-30h carrier; annotated tag, 2026-11-06/07. The v0.5.0 cut already executed; CR-BP-30h's in-file `Proposed` status is backfill debt, not an unexecuted release.
4. **Vendored-regenerator divergence is by design**: `cmp scripts/regenerate_catalog.py` against metaframework `v2.7.0` `tools/regenerate_catalog.py` differs (391 diff lines) — the vendored copy is authoritative per CST-013/CST-014; no action.

**Verdict**: the sweep's "index-truth tension" flag was a false positive caused by reading this repo with another catalog's vocabulary. `canonical: 3722` + `lifecycle_status: candidate` is the truthful reading.

## 5. Acceptance Criteria

1. `registers/catalog-portfolio.yaml` parses (CI parse job green) and carries `register_version: 12`, `snapshot_date: '2026-11-12'`.
2. Post-merge reconciler run reports **no R1 finding** (every metamodel `catalog_repo` value registered — requires CR-MET-022 merged first), **no R2 finding** (all ten new names exist on origin — verified in the sweep), and **no R3 state-truth finding on any changed row** (renamed populated rows read canonical 535 / 3722 from their indexes; new skeleton rows read ABSENT → skeleton, matching).
3. `register_version: 12`; the ten new entries and two renames present exactly once each; the two archived rows carry `archived: true`.

## 6. NOT-List

1. **No GitHub-side renames**: the renames already happened upstream; this CR only records them.
2. **No metamodel edits**: the catalog_repo repoint is CR-MET-022's change, landing before this CR.
3. **No record/index changes in any catalog repo**: this CR writes only the register.
4. **No schema-semantics change**: `archived` is an inert informational key documented in the header comment; the reconciler is not modified.
5. **No reconciliation-rule changes**: R1–R6 are untouched; their greenness after this CR is an acceptance criterion, not a change.
6. **No population work**: the ten skeleton entries record observed initial state; population remains with the repos' own owner series.
7. **No stale-name aliases retained**: v12 registers the real names only; the old names resolve via GitHub redirects for any consumer still reading v11.
