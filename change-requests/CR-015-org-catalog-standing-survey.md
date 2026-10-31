# CR-015: Org-Wide Catalog Standing Survey

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (org-wide governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-31
**Admission authority**: yes (register refresh + standing report)
**Depends on**: CR-013 (the register), CR-014 (the reconciler), CR-CATALOG-STRUCT-10 (the kit whose footprint the survey measures), CR-DEA-BC-68 (the candidate-register closure the survey confirms)
**Companion**: metamodel CR-MET-014/015/016/017 (the lifecycle truths the survey verifies)

## 1. Problem Statement

The register's last full observation dates to the 2026-10-30 audit and its v2–v5 patches. Since then the advancement programme landed 21 kits, 3 creations, 4 population tranches, and the identifier/CR-discipline remediations. The portfolio needs a fresh, mechanically verified standing picture, and the capabilities candidate question needed closure before "coverage" could be reported honestly.

## 2. The survey

`docs/reports/CATALOG-STANDING-2026-10-31.md`: all 43 registered repositories observed (GitHub contents + CATALOG.yaml counts, retries; two API flakes corrected by direct verification and noted). Headline: **13 populated catalogs carrying 4,019 canonical records; 25 skeletons (18 with the advancement-programme kit); 5 bespoke/pre-index layouts; 0 missing repos; 0 open candidate investigations.** Lifecycle truth verified: every metamodel lifecycle value agrees with observation except the long-named CR-MET-014 §6 stale-`existing` trio (owner decision, still standing).

## 3. Register v6

- `dea-catalog-business-capabilities` canonical_count 29 → 40 (the admission programme), with the candidate-state subtrees annotated as closed investigations (CR-DEA-BC-68).
- `index: bespoke` flags extended to skills, blueprints, application-components, system-functions (concepts already flagged) — the reconciler's R3 exempts them until they adopt the index discipline.
- Snapshot date 2026-10-31; register_version 6.

## 4. Reconciler verification

R1–R4 run against the refreshed register: **Findings: 0** (online, token-authenticated).

## 5. NOT-list

1. No metamodel changes (the stale-`existing` trio remains an owner decision).
2. No catalog content changes.
3. No new governance rules (the survey reports; the reconciler enforces).

## 6. Definition of Done

1. Standing report + register v6 landed; register parses; reconciler Findings: 0.
2. Register row and CHANGELOG entry in this PR.
