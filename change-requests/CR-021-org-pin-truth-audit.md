# CR-021: Org-Wide Pin-Truth Audit (Reconciler R6)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-11
**Admission authority**: no register change (rule only)
**Depends on**: CR-014 (the reconciler and its weekly CI), CR-019 (the tree-fetch pattern R6 shares), CR-CATALOG-STRUCT-13 in dea-metaframework (the PR-time counterpart gate, `pins-resolve`)
**Trigger**: 2026-11-11: `dea-catalog-stakeholders`' `catalog-conformance.yml` pinned `ref: v2.8.0` while the metaframework release did not exist; every run 404'd at the checkout org-visibly until the tag was cut (cut 2026-11-11 at the CR-CATALOG-STRUCT-12 merge commit `607eef6`). The same session's repair (stakeholders CR-CATALOG-STRUCT-18) surfaced a second latent defect the 404 had masked: a mangled vendored tool copy. The ordering rule (land the change, cut the release, bump the pins in their own PR) is now enforced at the source by CR-CATALOG-STRUCT-13's `pins-resolve` job; this CR audits the other half: every registered repo's pins, weekly, regardless of that repo's own CI hygiene.

## 1. Objective

Add rule R6 (pin-truth) to the portfolio reconciler: for every registered repo, verify that every metaframework release tag pinned in its CI workflows actually exists on `dea-metaframework`, and surface floating checkouts (naming the upstream without a release-tag ref) as a watch.

## 2. The Rule

| Rule | Check |
|---|---|
| R6 pin-truth | from the same recursive tree the R5 census uses, fetch each `.github/workflows/*.y|yaml` blob (raw route, size-safe) and extract the `technehub-labs/dea-metaframework` checkout refs (step-scoped, CST-013 semantics: a `ref:` counts only under a step naming the upstream, so a root-model allocation pin is never mistaken); a release-tag ref that is absent from the real tag set is a FAIL finding; a metaframework checkout with no release-tag ref (branch pin or none) prints a floating-pin watch without failing |

Design decisions, mirroring the reconciler's conventions:

- **One tree fetch per repo** serves R5 and R6 (the workflows list comes from the same tree; file bodies come off the raw route like `_read_index`).
- **Tag set fetched once per run** (`/repos/.../dea-metaframework/tags`, paginated); a transport failure warns and skips R6 without findings.
- **Extraction is a pure, unit-tested function** (`_extract_metaframework_pins`, 5 tests in `registers/test_reconcile_pins.py`, the reconciler's second test module).
- **Floating pins watch, do not fail**: conformant repos already fail CST-013 at PR time; the watch makes the org-visible drift reportable weekly without punishing repos whose own CI hygiene lags. First live run surfaced exactly one: `dea-catalog-organizational-units` (its `catalog-conformance.yml` checks out the metaframework without a release-tag ref).
- **The FAIL tier is the 404 class**: a pin ahead of its release. Message carries the remedy and the order (cut the release first, then bump the pin).

`.github/workflows/reconcile-portfolio.yml` step name now enumerates R1..R6; schedule unchanged. `ci.yml` gains the R6 unit-test step.

## 3. First-Run Observations (2026-11-11, live)

Verified against the live org before landing: 0 R6 findings (every release-tag pin across the 44 registered repos resolves, including stakeholders' v2.8.0 now that the tag exists); 1 R6 floating-pin watch (`dea-catalog-organizational-units`); R1..R5 output unchanged from the CR-019/CR-020 state (roles R5 finding, metrics `c/` watch, R3 green against register v11). Remediation carriers for the watch: an org-units repo PR pinning its checkout to a release tag.

## 4. Files

- `registers/reconcile_portfolio.py`: R6 constants + regexes, `_fetch_tree()` (extracted from the census), `_directory_entry_counts()` (now pure over a fetched tree), `_extract_metaframework_pins()`, `_fetch_raw_file()`, `_fetch_metaframework_tags()`, the R6 branch in the online loop, docstring rule table.
- `registers/test_reconcile_pins.py`: new; 5 extraction tests.
- `.github/workflows/reconcile-portfolio.yml`: step name enumerates R6.
- `.github/workflows/ci.yml`: R6 unit-test step.

## 5. Acceptance Criteria

1. `registers/test_reconcile_pins.py` passes (5 tests) and CI runs it.
2. A live run censuses all 44 repos: 0 R6 findings; the org-units floating-pin watch prints.
3. Transport failures (tag list, raw file, tree) print WARN and skip R6 for the affected repo without findings.
4. Offline mode unchanged: R1/R4 enforced, R2/R3/R5/R6 skipped with the warning.

## 6. NOT-List

- **No new workflow**: R6 rides the weekly schedule.
- **No floating-pin FAIL in this CR**: the watch tier reports; promotion to FAIL is a later decision once repos have had the CST-013 pin path available (it landed v2.7.0, 2026-11-10).
- **No enforcement of non-metaframework pins** (root-model/`dea-architecture-framework` refs, action SHAs): scoped to the toolchain whose 404 class motivated the rule.
- **No stakeholder notification bot**: the failed/watching scheduled job is the report (CR-014 convention).
