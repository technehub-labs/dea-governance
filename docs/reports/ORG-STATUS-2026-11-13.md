# TechNeHub Labs — Org-Wide Audit & Metamodel-Conformant Dependency Tree

**Date:** 2026-11-13 · **Scope:** `technehub-labs` (77 repositories, 7 boards) · **Requester:** eaojnr (Discord `#opendea`, thread `1570624014450171977`)

**Method:** every claim below is read from live GitHub state via the API (token `emmanuel-a-otchere`), reconciled against two normative sources — `dea-architecture-framework/model/opendeam-model.yaml` (OpenDEAM v0.9.1) and `dea-governance/registers/catalog-portfolio.yaml` (register v12, 2026-11-12). The register is treated as a *claim to be tested*, not as truth. Where the two disagree, both readings are reported.

---

## 1. Headline

- **77 repositories**: 63 public, 14 private, 5 archived.
- **5,776 promoted canonical records** org-wide; **15,728 entity files** on disk (2.7× — most content is staged, not promoted).
- **16 of 77 repositories have failing CI**; 16 more have never run CI at all.
- **Zero branch protection** on any repository. **Zero CODEOWNERS** on any repository.
- **Zero open PRs org-wide**, yet 75 open issues — work is serialised through a single issue queue, not through review.
- **The dependency graph is cyclic.** 12 catalogs form a single mutually-dependent cluster; a strict topological build order does not exist and cannot be manufactured without changing the metamodel.
- **14 catalogs have no `CATALOG.yaml` index at all** — ~4,400 entity files the org's own tooling cannot enumerate.
- **The federation layer is ungoverned:** the registry's advertised JSON entry point (`lists.technehub.com/data/index.json`) is a **404** that is never built, and **2 of 4** cross-org `wsf:`/`odea:` id references in `dea-metamodel` resolve against **nothing** in WSF's normative vocabulary. No validator reads the mapping; all of it passes green CI. (§11)
- **The org's own reconciler is red on `main`** (`dea-governance` → `reconcile-portfolio`), failing since 2026-11-12 with 11 findings.

---

## 2. Repository census (77)

| Class | Count | Repos |
|---|---|---|
| Catalog (`dea-catalog-*`) | 52 | includes 3 archived |
| Model / governance | 5 | `dea-architecture-framework`, `dea-metamodel`, `dea-metaframework`, `dea-concepts-model`, `dea-governance` |
| Tooling | 5 | `dea-cli`, `dea-web-viewer`, `dea-scripts`, `dea-code-gen`, `aocl` |
| Org infra | 2 | `.github`, `technehub-labs.github.io` |
| Archived / dormant | 5 | `dea-catalog-permission-probe`, `dea-catalog-taxonomy`, `ea-foundation`, `ecosystem-architecture`, `agentic-enterprise-innovation` |
| Other (unclassified) | 8 | `dea-ontology`, `dea-semantic-architecture`, `dea-release-package`, `agentic-enterprise`, `agentic-workflows`, `autonomous-flow`, `autonomous-networks`, `autonomous-operations` |

**Visibility split is a live governance concern.** 14 private repos include 6 catalogs that the metamodel allocates entities to (`dea-catalog-infrastructure-components`, `dea-catalog-integration-interfaces`, `dea-catalog-agent-foundry`, `dea-catalog-solution-hub`, `dea-catalog-reference-architecture`, `dea-catalog-ontologies`). Private repos are invisible to the org's default CI token — which is precisely why `reconcile-portfolio` reports them as *non-existent* rather than *private* (register v12 documents this as red-by-design on the `dea-catalog-agent-foundry` row).

### 2.1 CI health

| State | Repos |
|---|---|
| Green (recent) | 45 |
| **Failing** | **16** |
| Never run | 16 |

Failing repositories, with the failing workflow:

- `.github` — `portfolio-check` (schedule), first/last failing 2026-11-12
- `dea-catalog-business-services` — `catalog-conformance` (pull_request), first/last failing 2026-11-09
- `dea-catalog-financial-resources` — `CI` (push), first/last failing 2026-10-30
- `dea-catalog-information-system-services` — `validate-catalogue` (pull_request), first/last failing 2026-11-11
- `dea-catalog-intangible-resources` — `CI` (push), first/last failing 2026-10-30
- `dea-catalog-metrics` — `validate-metrics` (push), first/last failing 2026-11-09
- `dea-catalog-model-deployments` — `validate-allocation` (pull_request), first/last failing 2026-10-30
- `dea-catalog-organizational-units` — `catalog-conformance` (push), first/last failing 2026-10-16
- `dea-catalog-patterns` — `validate-allocation` (pull_request), first/last failing 2026-10-30
- `dea-catalog-physical-resources` — `CI` (push), first/last failing 2026-10-30
- `dea-catalog-roles` — `validate-entities` (push), first/last failing 2026-11-12
- `dea-cli` — `DEA CLI CI` (push), first/last failing 2026-08-04
- `dea-governance` — `reconcile-portfolio` (push), first/last failing 2026-11-12
- `dea-ontology` — `CI — manifest + structural lint` (push), first/last failing 2026-08-26
- `dea-release-package` — `Federation Audit` (schedule), first/last failing 2026-11-08
- `dea-semantic-architecture` — `CI — manifest + structural lint` (push), first/last failing 2026-08-26

Two of these are *governance* failures rather than content failures:

- **`dea-governance` → `reconcile-portfolio`** — the org's own portfolio reconciler fails on `main` (2026-11-12). Its 11 findings are reproduced in §5. This is the control that is supposed to detect drift, and it is itself red.
- **`.github` → `portfolio-check`** — the org-profile registry drift check has been failing on every scheduled run since 2026-09-10. Issue `.github#9` is still open and still lists 13 missing repos and 7 visibility drifts.

---

## 3. Catalog maturity — the decisive distinction

The register's `canonical_count` and a repo's on-disk file count measure **different things**. `state: canonical` in a CATALOG.yaml index marks a *promoted* record; a file under `entities/` may be `candidate`, `proposed`, `research` or `retired`. Reading only the file count overstates maturity by ~2.7×.

| Band | Count | Meaning |
|---|---|---|
| **A — Promoted** | 16 | `state: canonical` > 0 |
| **B — Staged** | 9 | files exist, 0 promoted — content written, admission not completed |
| **C — Empty** | 29 | no entities, no index — scaffold only |

**Band A (16) — genuinely populated:**

`api-contracts` (627) · `business-processes` (3,722) · `business-services` (535) · `platform-services` (500) · `business-capabilities` (40) · `value-streams` (111) · `business-objects` (74) · `information-models` (74) · `information-assets` (25) · `controls` (20) · `stakeholders` (12) · `information-classes` (8) · `knowledge-assets` (8) · `regulations` (8) · `actors` (3)

**Band B (9) — staged, work-in-progress, register under-reports these:**

| Repo | Files | Promoted | Register says | Truth |
|---|---|---|---|---|
| `metrics` | 4433 | 0 | populated / 5 | ok |
| `roles` | 1252 | 0 | populated / 1 | ok |
| `skills` | 735 | 0 | skeleton / 0 | understated |
| `guardrails` | 600 | 0 | skeleton / 0 | understated |
| `application-components` | 747 | 0 | skeleton / 0 | understated |
| `integration-interfaces` | 664 | 0 | skeleton / 0 | understated |
| `information-system-services` | 658 | 0 | skeleton / 0 | understated |
| `system-functions` | 660 | 0 | skeleton / 0 | understated |
| `concepts` | 29 | 0 | populated / 29 | ok |

> **`dea-catalog-metrics` is the sharpest case:** 4,433 entity files and a 4,433-entry index on disk, but the register records `populated` with `canonical_count: 5` and the index carries **zero** `state: canonical` records. The standing report (2026-10-31) flagged this as "owner-active index refresh"; it has not moved in 13 days, and the repo's `validate-metrics` CI is failing.
>
> **`dea-catalog-roles`:** 1,252 entity files, 10 `lifecycle_status: active`, **1** `state: canonical`. The register's `canonical_count: 1` is literally true and materially misleading — and `validate-entities` CI is failing on 7 unresolved `skills:` cross-references.
>
> **`dea-catalog-skills`:** 735 entity files, 0 promoted, and `dea-catalog-roles` references them for 9,550 pending edges. The declared edge `SKL --required by--> ROL` is therefore **live-broken**, not merely unresolved — it is exactly the 7 CI failures.

### 3.1 The index schema has diverged into four incompatible shapes

This is the mechanism behind most of the register's under-reporting, and it is not recorded anywhere in the CR series.

| Index shape | Repos | Meaning |
|---|---|---|
| `state:` per entity | 17 | current schema — `state: canonical` marks a promoted record |
| `lifecycle_status:` only | 3 | `dea-catalog-metrics`, `dea-catalog-roles`, `dea-catalog-skills` — **no `state:` field at all** |
| `entities: []` (no per-entity fields) | 20 | scaffold indexes; content absent |
| **No `CATALOG.yaml` at all** | **14** | bespoke layout — **invisible to every index-based tool** |

The 14 without an index are exactly the Band-B repos that hold real content: `application-components` (747 entities), `integration-interfaces` (664), `system-functions` (660), `information-system-services` (658), `concepts` (29), plus 9 empty scaffolds. Each carries `metamodel-pointer.yaml`, `schemas/`, `scripts/`, `change-requests/` — a working catalog — but **no index**.

**Consequence:** the reconciler's R3 *state truth* check cannot evaluate these 14 repos at all (it reads `CATALOG.yaml`); the register's `canonical_count` for them is `0` by default rather than by observation; and no tool can enumerate them. **~4,400 entity files sit in repos that the org's own tooling cannot see.** The standing report acknowledged this as "bespoke-index adoption — concepts, skills, blueprints, application-components, system-functions", but the scope is larger: 14 repos, not 5.

**Band C (29) — scaffold only.** These carry the metamodel's *structure* (pointer, schema, gates, CI) but no content. Note that 20 of them pin a metamodel and root-model version they have not yet produced content against — the pins are premature, not wrong.

---

## 4. The dependency tree

### 4.1 How it was derived

The metamodel's `relationships:` block holds **118 typed, directed relationships** across 81 entities. Projecting each relationship onto the entity→repository allocation in `allocation.entities` yields a **repository-level graph of 45 nodes and 75 edges**. Five model names are drifted from their real repos and were resolved:

| Model `catalog_repo` | Actual repository |
|---|---|
| `dea-catalog-processes` | `dea-catalog-business-processes` |
| `dea-catalog-digital-business-service-factory` | `dea-catalog-business-services` |
| `dea-catalog-information-system-components` | `dea-catalog-application-components` |
| `dea-catalog-information-system-functions` | `dea-catalog-system-functions` |
| `dea-catalog-information-system-integration-interfaces` | `dea-catalog-integration-interfaces` |

### 4.2 The graph is cyclic — and that is a finding, not a defect

A naive topological sort fails: 29 of 45 nodes sit in cycles. Tarjan's strongly-connected-components decomposition (verified: 0 internal strong-connectivity violations) resolves this into **34 components** whose condensation is provably acyclic.

**One component is a single mutually-dependent cluster of 12 catalogs:**

> `dea-catalog-api-contracts` · `dea-catalog-application-components` · `dea-catalog-business-capabilities` · `dea-catalog-business-objects` · `dea-catalog-business-processes` · `dea-catalog-data-entities` · `dea-catalog-data-products` · `dea-catalog-event-streams` · `dea-catalog-investment-initiatives` · `dea-catalog-metrics` · `dea-catalog-strategic-objectives` · `dea-catalog-system-functions`

The cycle is structural: capability *is implemented by* process, process *is automated by* system function, system function *is exposed via* API contract, API contract *serves* data entity, data entity *is curated into* data product, data product *is exposed via* API contract. Each edge is legitimate EA semantics. **The metamodel therefore cannot be built one repo at a time in this cluster** — the 12 catalogs must be *admitted together*, or the relationship graph must be relaxed.

**This is the single most important architectural finding in the audit.**

**Scope note — this cycle does *not* explain the `roles → skills` breakage.** `skills` and `roles` sit *outside* the cluster (`skills → roles → actors` is a simple chain, W31 → W29). The 7 failing `roles` CI runs are caused by `skills` having **never published** — 735 files, 0 promoted — not by the cycle. The two are separate problems with separate fixes; the cycle is the architectural one, the skills publication is the immediate one.

### 4.3 Build order (34 waves, dependencies first)

Derived by topological sort of the condensation DAG. Verified: **0 prerequisite-order violations** across all 75 edges.

| Wave | Catalog | Layer | Promoted | Files | CI | Note |
|---|---|---|---|---|---|---|
| W1 | `information-classes` | L4 | 8 | 8 | ok |  |
| W2 | `integration-interfaces` | L5 | 0 | 664 | ok |  |
| W3 | `platform-services` | L5 | 500 | 500 | ok |  |
| W4 | `information-system-services` | L5 | 0 | 658 | FAIL |  |
| W5 | `api-contracts` | L5 | 627 | 627 | ok | **mutual-cycle cluster** |
| W5 | `application-components` | L5 | 0 | 747 | ok | **mutual-cycle cluster** |
| W5 | `business-capabilities` | L3 | 40 | 43 | ok | **mutual-cycle cluster** |
| W5 | `business-objects` | L3 | 74 | 74 | ok | **mutual-cycle cluster** |
| W5 | `business-processes` | L3 | 3722 | 3882 | ok | **mutual-cycle cluster** |
| W5 | `data-entities` | L4 | 9 | 9 | ok | **mutual-cycle cluster** |
| W5 | `data-products` | L4 | 0 | 0 | ok | **mutual-cycle cluster** |
| W5 | `event-streams` | L4 | 0 | 0 | ok | **mutual-cycle cluster** |
| W5 | `investment-initiatives` | L2 | 0 | 0 | ok | **mutual-cycle cluster** |
| W5 | `metrics` | orthogonal | 0 | 4433 | FAIL | **mutual-cycle cluster** |
| W5 | `strategic-objectives` | L2 | 0 | 0 | ok | **mutual-cycle cluster** |
| W5 | `system-functions` | L5 | 0 | 660 | ok | **mutual-cycle cluster** |
| W6 | `actors` | L3 | 3 | 3 | ok |  |
| W7 | `risk-register` | L2 | 0 | 0 | ok |  |
| W8 | `ai-ml-models` | L4 | 0 | 0 | ok |  |
| W9 | `patterns` | L2/L5 | 0 | 0 | FAIL |  |
| W10 | `blueprints` | L2 | 0 | 0 | ok |  |
| W11 | `business-services` | L3 | 535 | 535 | FAIL |  |
| W12 | `organizational-units` | L3 | 0 | 0 | FAIL |  |
| W13 | `change-initiatives` | L3 | 0 | 0 | ok |  |
| W14 | `concepts` | orthogonal | 0 | 29 | ok |  |
| W15 | `controls` | L2 | 20 | 20 | ok |  |
| W16 | `digital-identities` | L4 | 0 | 0 | ok |  |
| W17 | `ecosystem-platforms` | L1 | 0 | 0 | ok |  |
| W18 | `experiments` | L2 | 0 | 0 | ok |  |
| W19 | `financial-resources` | L3 | 0 | 0 | FAIL |  |
| W20 | `guardrails` | L2 | 0 | 600 | ok |  |
| W21 | `information-assets` | L4 | 25 | 25 | ok |  |
| W22 | `intangible-resources` | L3 | 0 | 0 | FAIL |  |
| W23 | `journey-touchpoints` | L1 | 0 | 0 | ok |  |
| W24 | `tenets` | L2 | 0 | 0 | ok |  |
| W25 | `knowledge-assets` | L4 | 8 | 8 | ok |  |
| W26 | `model-deployments` | L4 | 0 | 0 | FAIL |  |
| W27 | `physical-resources` | L3 | 0 | 0 | FAIL |  |
| W28 | `regulations` | L2 | 8 | 8 | ok |  |
| W29 | `roles` | L3 | 0 | 1252 | FAIL |  |
| W30 | `signals` | L2 | 0 | 0 | ok |  |
| W31 | `skills` | L3 | 0 | 735 | ok |  |
| W32 | `stakeholders` | L1 | 12 | 23 | ok |  |
| W33 | `technology-radar` | L2 | 0 | 0 | ok |  |
| W34 | `value-streams` | L3 | 111 | 111 | ok |  |

### 4.4 Reading the order

- **W1–W4** are true foundations: `information-classes` (classification of data by sensitivity) → `integration-interfaces` → `platform-services` → `information-system-services`. Three of the four are Band B or C — content does not yet exist where the graph says it must.
- **W5** is the 12-catalog cycle. It is the bulk of the org's content (4,522 promoted records, ~78% of all canonical records) and it cannot be decomposed further. **Wave 5 is the critical path for the entire programme.**
- **W6–W9** (`actors`, `risk-register`, `ai-ml-models`, `patterns`) depend only on the cluster and are individually unblocked.
- **W10–W34** fan out from the cluster along governance, measurement and capability edges. `concepts` (W14) and `controls` (W15) are the most load-bearing downstream items — 5 of the 12 cluster members depend on `metrics` (application-components, business-capabilities, data-entities, strategic-objectives, system-functions), and `metrics` sits inside the cycle — 12 catalogs org-wide depend on it.

### 4.5 What the order implies

1. **Admission must be cluster-aware.** The org's current per-catalog admission process (one catalog per CR series) cannot close a 12-node cycle. A *cluster admission* CR is needed, or the cycle must be broken by relaxing one edge (the most defensible candidate: `data-product --exposed via--> API contract`, which is a realisation edge the graph does not need to be mutual).
2. **`metrics` is the chokepoint.** 5 of the 12 cluster members declare `measured by -> metrics` (application-components, business-capabilities, data-entities, strategic-objectives, system-functions); 12 catalogs org-wide depend on it. `metrics` has 4,433 files and **0 promoted records** — so every one of those 12 is blocked on a catalog that has never promoted a record.
3. **The `roles → skills` edge is the canary.** 9,550 pending batch edges, 2,473 resolvable now, 7 CI failures. Publishing `skills` as canonical converts 9,550 pending edges into resolvable ones in one step — the highest-leverage single action in the org.

---

## 5. Reconciler findings (reproduced from the org's own CI log)

`dea-governance` → `reconcile-portfolio` (run 43230817650, 2026-11-12, main): **Findings: 11**

**R2 — registered repo does not exist (8)**
`dea-catalog-agent-foundry` · `dea-catalog-infrastructure-components` · `dea-catalog-integration-interfaces` · `dea-catalog-ontologies` · `dea-catalog-permission-probe` · `dea-catalog-reference-architecture` · `dea-catalog-solution-hub` · `dea-catalog-taxonomy`

> **Correction:** all eight **do** exist. Six are private (invisible to the default workflow token) and two are archived (`permission-probe`, `taxonomy`). The reconciler's own header documents the 404-vs-no-access ambiguity, and the register's `dea-catalog-agent-foundry` row carries a red-by-design note saying exactly this. **These 8 findings are false positives — but they have been failing CI for 13 days, which means the reconciler's token needs org-read scope, or the private repos need to be public.** A red control that cries wolf is worse than no control.

**R5 — directory-size shard trigger exceeded (3)**

| Directory | Entries | Trigger |
|---|---|---|
| `dea-catalog-references/dea/application` | 1,812 | 800 |
| `dea-catalog-references/media-types/application` | 1,812 | 800 |
| `dea-catalog-roles/entities/v1-alpha` | 1,252 | 800 |

These are **genuine** and consequential: GitHub truncates directory listings at 1,000 entries, so a consumer listing `dea-catalog-roles/entities/v1-alpha` sees only the first ~1,000 of 1,252 records. This is a correctness risk, not a style point.

**R5 watch (not failing) (2):** `dea-catalog-api-contracts/entities/v1-alpha` (628) · `dea-catalog-metrics/entities/v1-alpha/c` (604)

**R6 floating pin (1, not failing):** `dea-catalog-organizational-units/.github/workflows/catalog-conformance.yml` names `dea-metaframework` without a release-tag ref.

---

## 6. Governance hygiene (77 repos)

| Control | Present | Coverage |
|---|---|---|
| LICENSE | 69 | 90% |
| NOTICE | 63 | 82% |
| CHANGELOG | 50 | 65% |
| CONTRIBUTING | 49 | 64% |
| CI workflows | 55 | 71% |
| PR template | 5 | **6%** |
| CODEOWNERS | **0** | **0%** |
| Branch protection | **0** | **0%** |
| VERSION file | 2 | 3% |

**Branch protection and CODEOWNERS are at zero across all 77 repositories.** Board card `GOV-C-003` (CODEOWNERS per layer) and `GOV-C-004` (branch protection) are both `Todo`/`Critical` and have been since the board was created. Every one of the 5 board cards in project 7 and all 7 in project 3 are `Todo` — **the board does not reflect the org's actual state, because the work is happening in repos and the board is not being updated.**

### 6.1 Pin currency

| Pin | In use | Newest available | Gap |
|---|---|---|---|
| `root_model_pin` (architecture-framework) | 27 × `v0.8.0`, 1 × `v0.9.0` | `v0.9.0` | 27 catalogs one release behind |
| `metaframework_pin` | 27 × `v2.6.0`, 1 × `v2.8.0` | `v2.8.0` | 27 catalogs two releases behind |
| `metamodel_pin` | 30 × `1.0.0` | `v1.0.0` | current |

All pins **resolve** — no dangling refs (CR-021's discipline holds). But `dea-architecture-framework` carries `VERSION: 0.9.1` while its newest tag is `v0.9.0`: the repo has an untagged patch release, so the tag set cannot express what is on `main`.

### 6.2 Board hygiene

**11 duplicate card titles** across boards 3, 6 and 7 — 11 redundant cards, all `Todo`. Each duplicated pair corresponds to a pair of duplicate *issues* in `dea-metamodel` (`#4`–`#10` duplicate `#11`–`#17`; `#21`–`#26` duplicate `#22`–`#27`/`#28`–`#35`). The `dea-metamodel` issue queue is 35 issues of which ~24 are duplicates.

Board field state: **51 distinct card titles across 5 boards**; every board's `Status` field is `Todo` except 5 `Done` cards in project 6. There are **no** `In Progress` and **no** `Blocked` cards anywhere in the org.

---

## 7. Register vs live truth — summary of divergences

| # | Divergence | Evidence |
|---|---|---|
| D1 | 5 metamodel `catalog_repo` names have no register entry | R1 findings; names drifted from real repos |
| D2 | 23 live repos are absent from the register | incl. `dea-governance`, `dea-metamodel`, `dea-cli`, `dea-web-viewer` |
| D3 | Register `canonical_count` understates 9 repos | e.g. `metrics` 5 vs 4,433 files |
| D4 | `metrics` registered `populated` with 0 promoted records | `state:` census = 0 canonical |
| D5 | `platform-services` registered `skeleton` but has 500 promoted records | register v12 stale |
| D6 | `roles`/`skills` registered `populated`/`skeleton` with 1/0 promoted | 1,252 / 735 files |
| D7 | `.github` registry stale since 2026-09-10 | issue #9 open, 13 missing + 7 visibility drifts |
| D8 | `dea-architecture-framework` VERSION 0.9.1 untagged | newest tag `v0.9.0` |
| D9 | Reconciler R2 false-positive on 6 private + 2 archived repos | failing on main 13 days |
| D10 | 12-catalog mutual dependency cycle | SCC decomposition |
| D11 | 11 duplicate cards / ~24 duplicate issues | board + issue enumeration |
| D12 | Zero branch protection, zero CODEOWNERS, 6% PR templates | hygiene sweep |
| D13 | 14 catalogs have no `CATALOG.yaml` index at all | contents-API sweep — ~4,400 entities invisible to index tooling |
| D14 | Index schema diverged into 4 incompatible shapes | 17 `state:` · 3 `lifecycle_status:` only · 20 empty · 14 no index |
| D15 | Registry advertises `data/index.json` that is never built and 404s | `index.html` L8 vs `scripts/build.sh` outputs |
| D16 | 2 of 4 cross-org id refs unresolvable against WSF normative vocabulary | `odea:BusinessCapability`, `odea:BusinessProcess` |

---

## 8. Recommended sequence

**Immediate (unblocks the red control, days not weeks):**

1. Fix `reconcile-portfolio`: give the workflow an org-read token (or make the 6 private catalogs public), and exclude the 2 archived repos from the register. This converts 8 false-positive findings into 0 and restores the drift control the whole governance model depends on.
2. Shard the two over-limit directories (`dea-catalog-references` ×2 at 1,812; `dea-catalog-roles/entities/v1-alpha` at 1,252). This is a correctness fix: consumers currently cannot enumerate the full catalog.
3. Publish `dea-catalog-skills` as canonical (735 files already written). Highest-leverage single action — resolves 9,550 pending edges and clears the 7 failing `roles` CI runs.
4. Give the 14 index-less catalogs a `CATALOG.yaml`, and bring `metrics`/`roles`/`skills` onto the `state:` schema. Until then the register cannot measure a third of the org, and R3 is silently inert for those repos.
5. Promote `dea-catalog-metrics` records to `state: canonical`. 4,433 files are staged and 5 of the 12 cluster catalogs (12 org-wide) wait on this one catalog.

**Structural (this is the metamodel conversation):**

6. Decide the cluster-admission question. Either (a) admit the 12-catalog cycle as one unit under a single CR, or (b) relax one edge to break the cycle. Option (b) is cheaper; the defensible edge is `data-product --exposed via--> API contract`. **This is an architectural decision with an explicit trade-off, not an implementation task.**
7. Reconcile the register with reality — refresh to v13 with observed `state:` counts (not file counts) as `canonical_count`, and resolve the 5 drifted `catalog_repo` names in the metamodel so R1 closes.
8. Deduplicate the boards and the `dea-metamodel` issue queue; move every in-flight repo into its board card as a sub-task. A board that says `Todo` while 16 repos are red is a board that has stopped governing.

**Governance:**

9. Turn on branch protection and CODEOWNERS for the 5 model repos and the 16 Band-A catalogs first (21 repos, not 77 — start where the value is). The `GOV-C-003`/`GOV-C-004` cards exist; they need an owner and a date, not another draft.
10. Retire or archive the 5 dormant repos and the 3 orphaned `dea-catalog-*` scaffolds (`ontologies`, `reference-architecture`, `infrastructure-components`) that have no allocation, no content, and no owner-visible activity.

---

## 9. Method, limits, and what this audit does *not* claim

- **Observed vs workflow-observable.** Private repos are visible to the requester's token but not to the default CI token. The audit separates the two and never reports a 404 as *does not exist*.
- **`state:` vs `lifecycle_status`.** Where a CATALOG.yaml carries both and they disagree (e.g. `business-processes`: `lifecycle_status: candidate`, `state: canonical`), `state:` is treated as authoritative because it is the field the register's `canonical_count` is defined against.
- **Federation scope (§11):** the cross-org check covers the `wsf:`/`odea:` ids declared by `technehub-labs` (4 ids, 2 files) against WSF's normative vocabulary. It does **not** audit WSF's own internal consistency, and it does **not** cover the `wsf-connectors` OpenDEA adapter, which expresses a *second* independent copy of the Capability mapping with no check that the two agree.
- **Not claimed:** that any repo's *content* is correct, that relationship semantics are right, or that a build order should be executed. The dependency tree is derived from the metamodel as written. If the metamodel is wrong, the tree inherits that error — which is why finding D10 is framed as a decision for you, not a defect to be patched.
- **Not claimed:** that the 16 failing CI runs indicate broken content. Four are governance controls (`.github`, `dea-governance`, `dea-release-package`), two are dormant (`dea-cli`, `dea-ontology`), and the rest are content-validation failures on Band-B/C repos.
- **Snapshot:** all state read 2026-11-13. The org pushes most days; re-run the reconciler for a current view.

---

## 11. Federation addendum — the org is not the system

The first pass of this audit scoped itself to `technehub-labs`. That is a scope error: the authoritative artefacts for a federated setup live *outside* the org under review. This addendum closes the gap. Re-verified against live state 2026-11-13.

### 11.1 The canonical catalogue is outside the org — and its entry point is broken

`dea-catalog-references` publishes the OpenDEA Reference Registry to `lists.technehub.com` (GitHub Pages). Its landing page advertises a JSON catalogue via:

```html
<link rel="alternate" type="application/json" href="/data/index.json">
```

**`https://lists.technehub.com/data/index.json` returns HTTP 404.** It is not deployed and is not built: `scripts/build.sh` emits `data/media-types/iana-media-types.json`, `data/uri-schemes/iana-uri-schemes.json`, `data/ecf-coordinates/coordinates.json`, `data/paths.tsv` and `data/SHA256SUMS` — **never `data/index.json`**. The `data/` directory in the source repo contains exactly those five entries and no `index.json`.

Everything else on the site resolves (200):

| Path | Status | Size |
|---|---|---|
| `/data/media-types/iana-media-types.json` | 200 | 1,026,636 b |
| `/data/uri-schemes/iana-uri-schemes.json` | 200 | 163,890 b |
| `/data/ecf-coordinates/coordinates.json` | 200 | 17,392 b |
| `/data/paths.tsv` | 200 | 179,463 b |
| `/data/SHA256SUMS` | 200 | 375 b |
| `/media-types/` · `/uri-schemes/` · `/ecf/` · `/dea/` · `/healthz` | 200 | — |
| **`/data/index.json`** | **404** | **9,379 b (error page)** |

The ECF coordinate file is live and healthy — `snapshot_date: 2026-10-16`, 7 domains × 7 stages, sourced from `dea-metaframework/framework/matrix.md`. So the registry's *content* is sound; the **machine-readable entry point consumers are told to use is a dangling reference**.

### 11.2 Two broken cross-org id references in `dea-metamodel/mappings/wsf/mapping.yaml`

`dea-metamodel` declares a federation mapping to WSF. Two of its rows assert that a WSF-side concept is *already published*. Both assertions are false against WSF's normative vocabulary.

| Mapping row | Claims | Reality |
|---|---|---|
| `dea:BusinessCapability` → `odea:BusinessCapability` | *"the WSF side is already published as a specialization of `wsf:Capability` in `wsf/concepts/capability.md`"* | The string `odea:BusinessCapability` **does** appear in `wsf/concepts/capability.md` — but only inside a prose `### OpenDEA Specialization` YAML block. It is **absent from `wsf-spec/turtle/wsf-vocabulary.ttl`**, WSF's normative vocabulary (504 lines, 39 concept ids, **zero `odea:` namespace**). |
| `dea:BusinessProcess` → `odea:BusinessProcess` | *"the WSF side is a specialization of `wsf:Process` in the same template as `odea:BusinessCapability` ↔ `wsf:Capability`"* | **`odea:BusinessProcess` does not exist anywhere in WSF.** Content scan across `wsf` (57 blobs), `wsf-spec` (7) and `wsf-docs` (9): zero occurrences. `wsf/concepts/process.md` (61 lines) has **no** OpenDEA Specialization block and never mentions `Business`. |

**The root-model mapping rows are sound.** `dea:Capability` ↔ `wsf:Capability` and `dea:Process` ↔ `wsf:Process` both check out: `wsf:Capability` and `wsf:Process` are both declared `a wsf:Concept` in the normative vocabulary, and `wsf/concepts/capability.md` carries `semantic_id: wsf:Capability` with `parent: wsf:Capability` on the OpenDEA specialization. The mapping's own note is accurate there.

**Namespace check.** The full set of `wsf:`/`odea:` ids referenced from `technehub-labs` is **4** — `wsf:Capability`, `wsf:Process`, `odea:BusinessCapability`, `odea:BusinessProcess` — confined to two files (`dea-metamodel/mappings/wsf/mapping.yaml` and `dea-metamodel/metamodel/dea-metamodel.yaml`). No `wsf:` id is used as a *native* identifier anywhere in the org, so there is **no cross-org id collision** — the two `odea:` ids are broken *references*, not collisions. Both `wsf:` ids resolve against WSF's normative vocabulary.

### 11.3 CI blindness: nothing detects any of this

- **No validator reads the WSF mapping.** A content scan of all 23 scripts under `dea-metamodel/scripts/` and `dea-metamodel/tools/` found **zero** references to `mappings` or `wsf`. `mappings/wsf/mapping.yaml` is unvalidated, untested, and ungated.
- **The portfolio reconciler does not cover it.** `dea-governance/registers/reconcile_portfolio.py` has no `mappings`/`wsf`/`federat` reference. Its R1–R6 checks are all intra-org.
- **The Federation Watchdog does not cover it.** `dea-release-package/.github/workflows/watchdog.yml` (CR-DEA-RP-03) monitors *release manifests* — pin coherence, cross-version compatibility, asset drift. It never reads semantic mappings.
- **No link check on the registry site.** `dea-catalog-references`' `scripts/validate-data.py` gate checks JSON shape and the `SHA256SUMS` invariants; it does not verify that the `<link rel="alternate">` target in `index.html` exists. That is why the 404 survives green CI.

So all three findings — the broken registry entry point and the two broken `odea:` references — pass silently through green CI. **CI blindness is the finding.**

### 11.4 The sibling org already has the machinery — extend, don't invent

Per the check for an existing reconciler that already does the job for another org:

- `World-Semantic-Foundation/wsf-governance/ID-RECONCILIATION.md` (2026-09-28, author Emmanuel A. Otchere) is an **established** id-reconciliation authority: a stated resolution rule (*"Canonical references: always use ADR-WSF-NNN … subject-namespace aliases are accepted as input but are resolved to the canonical ID"*), a machine-readable companion `id-aliases.yaml`, and explicit deprecation handling. It covers ADR/CR ids — **not** concept ids, so it does not yet cover `odea:BusinessCapability`.
- `World-Semantic-Foundation/wsf-spec/turtle/wsf-vocabulary.ttl` is the **machine-readable concept-id authority** — the natural substrate for a mapping-conformance check.
- `World-Semantic-Foundation/wsf-connectors/adapters/opendea/` is the existing OpenDEA adapter, already mapping `OpenDEA Capability : wsf:Capability` — a *second*, independent place where the same mapping is expressed, with no check that the two agree.

**Recommendation:** do not build a new cross-org reconciler. Extend the existing `dea-governance/registers/reconcile_portfolio.py` with an **R7 — federation-mapping conformance** check that resolves each `wsf:`/`odea:` target in `dea-metamodel/mappings/wsf/mapping.yaml` against WSF's normative vocabulary, and add a **link check** to `dea-catalog-references`' `validate-data.py` for advertised site paths. Both are extensions of existing gates, not new machinery. The vocabulary fetch is a `curl` against one `raw.githubusercontent.com` URL — cheap, and it fails loudly when the upstream id is absent.

**Cross-org write boundary.** The repair for `odea:BusinessCapability` and `odea:BusinessProcess` is **WSF-side** (publish the concepts in `wsf-spec/turtle/wsf-vocabulary.ttl`, or correct the mapping's claim). That is outside `technehub-labs` write authority and needs a WSF-side change request. The two `technehub-labs`-side fixes — the registry `index.json` and the gate — are in scope here.


---

## 10. Reproduction

```bash
# Inventory
gh api '/orgs/technehub-labs/repos?per_page=100&type=all' --paginate

# The org's own reconciler (11 findings)
gh run view 43230817650 --repo technehub-labs/dea-governance --log-failed

# Pin truth
gh api repos/technehub-labs/dea-metaframework/tags --jq '.[].name'
gh api repos/technehub-labs/dea-architecture-framework/tags --jq '.[].name'

# Federation: the registry entry point (expect 404 — never built)
curl -sSL -o /dev/null -w '%{http_code}\n' https://lists.technehub.com/data/index.json

# Federation: WSF normative vocabulary (the concept-id authority)
gh api repos/World-Semantic-Foundation/wsf-spec/contents/turtle/wsf-vocabulary.ttl --jq .content | base64 -d | grep -c 'a wsf:Concept'

# Branch protection (expect 404 on all 77)
gh api repos/technehub-labs/dea-metamodel/branches/main/protection
```