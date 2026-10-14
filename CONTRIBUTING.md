# Contributing to OpenDEA Governance

This repository follows the standard `technehub-labs/*` change-request (CR) governance discipline.

## Authorship cardinal rule (per CR-118 / EGV-008)

Every authorship-bearing field in any artifact of this repository must carry `Emmanuel A. Otchere` (or, for org-level CFF authors, `TechNeHub Labs`). The authoring-tool denylist (`Coder`, `Agent`, `Hermes`, `Claude`, `GPT`, `Cline`, `OpenAI`, `MiniMax`, `MiniMax-M3`) is enforced by the cardinal-rule gate. See `change-requests/CR-012-org-wide-entity-governance.md` EGV-008 for the provenance rule.

## CR format

Every change that lands on `main` must have a corresponding CR doc in `change-requests/`. The CR template:

```
# CR-NNN: <Title>

**Status**: Proposed | Accepted | Superseded
**Layer**: Cross-cutting | <layer>
**Owner**: Emmanuel A. Otchere
**Date**: YYYY-MM-DD
**Admission authority**: yes (if this CR is itself an admission tranche)
**Depends on**: CR-NNN (if applicable)

## 1. Problem statement
## 2. Objective
## 3. Scope
## 4. ...
## N. Acceptance criteria
## N+1. Implementation strategy
## N+2. What this CR is NOT
```

## PR mechanics

- One branch per CR: `git checkout -b feature/cr-NNN-short-name`
- Atomic commits; one logical change per commit
- Commit message: `<type>: <imperative description>` (feat / fix / refactor / docs)
- PR title: `CR-NNN: <Title>`
- PR body: Summary + Rule (if normative) + Repository changes table + Test posture + D-004 compliance + What this CR is NOT
- Squash-merge with `--delete-branch` after CI is green
- D-004 (no en/em-dash) compliance is required; the cardinal-rule gate enforces authorship cardinal rules

## Local verification before push

```bash
# D-004 (no en-dash, no em-dash, no triple-semicolon; use ASCII or hyphen-minus)
rg -nP '[\x{2013}\x{2014}\x{2E3B}]' . && echo "D-004 VIOLATIONS" || echo "D-004 clean"

# Authorship cardinal rule (118a gate)
python3 scripts/check_authorship.py --strict

# CR-META (if a CR doc is added/modified)
python3 scripts/check_cr_metadata.py
```

## Related governance

- `dea-architecture-framework` for ADRs and architectural decisions
- `dea-metamodel` for entity-type definitions
- `dea-catalog-processes` for the CR-BP-121 entity-system pilot
