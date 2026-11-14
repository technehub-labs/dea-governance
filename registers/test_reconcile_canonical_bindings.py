"""Unit tests for the R7/R8 canonical-binding checks (CR-023).

These pin the semantics of the reconciler's binding to the federation's
canonical reference root, offline: no network, no token, no live
catalogue. The fixtures are the shapes the upstream artefacts actually
have - the reference catalogue publishes {kind, id, version, domain}
entries under a top-level `catalogue` key, and the relation graph
publishes edges under a top-level `relations` key.

The defects these guard are the ones that would silently break the
federation's identity contract:

  - a register row whose version disagrees with the catalogue's version
    for the same canonical id (the two sides must agree on WHICH
    version exists);
  - a catalogue maturity model no register row claims (the federation
    would lose track of a published model);
  - two register rows claiming one canonical id (the binding would be
    ambiguous);
  - a relation-graph endpoint that resolves to nothing (the federation
    would carry a dangling reference).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reconcile_portfolio import (  # noqa: E402
    _row_org,
    catalogue_reference_index,
    check_canonical_bindings,
    check_register_references,
    check_relation_endpoints,
    relation_edge_list,
)


def _catalogue_doc(*refs: dict) -> dict:
    """A reference-catalogue document with the given reference entries."""
    return {"catalogue": {"id": "dea:catalogue-assessment-references", "references": list(refs)}}


def _ref(cid: str, version: str = "1.0.0", kind: str = "maturity-model", domain: str = "technology") -> dict:
    return {"kind": kind, "id": cid, "version": version, "domain": domain}


def _row(repo: str, cid: str, version: str = "1.0.0", org: str = "Assessment-Models") -> dict:
    return {
        "repo": repo,
        "organization": org,
        "canonical_id": cid,
        "canonical_version": version,
        "state": "published",
        "release": f"v{version}",
        "ratified": "2026-11-14",
    }


def _relations_doc(*edges: dict) -> dict:
    """A relation-graph document with the given edges."""
    return {"relations": {"id": "dea:relations-maturity-models", "edges": list(edges)}}


def _edge(eid: str, source: str, target: str) -> dict:
    return {
        "id": eid,
        "source_id": source,
        "target_id": target,
        "relationship_type": "supports",
    }


# ---------------------------------------------------------------------------
# catalogue / relation parsing
# ---------------------------------------------------------------------------

def test_catalogue_index_reads_the_catalogue_shape() -> None:
    doc = _catalogue_doc(
        _ref("dea:maturity-technology", "1.0.0"),
        _ref("dea:capability-technology-architecture", "1.0.0", kind="capability"),
    )
    index = catalogue_reference_index(doc)
    assert set(index) == {"dea:maturity-technology", "dea:capability-technology-architecture"}
    assert index["dea:maturity-technology"]["kind"] == "maturity-model"
    assert index["dea:maturity-technology"]["version"] == "1.0.0"
    assert index["dea:capability-technology-architecture"]["kind"] == "capability"


def test_catalogue_index_tolerates_an_empty_document() -> None:
    assert catalogue_reference_index({}) == {}
    assert catalogue_reference_index({"catalogue": {}}) == {}


def test_relation_edge_list_reads_the_relations_shape() -> None:
    edges = relation_edge_list(
        _relations_doc(
            _edge("dea:edge-a", "dea:maturity-ea-capability", "dea:maturity-technology"),
            _edge("dea:edge-b", "dea:maturity-technology", "dea:maturity-modernization"),
        )
    )
    assert len(edges) == 2
    assert edges[0]["source_id"] == "dea:maturity-ea-capability"
    assert edges[1]["target_id"] == "dea:maturity-modernization"


def test_relation_edge_list_tolerates_an_empty_document() -> None:
    assert relation_edge_list({}) == []
    assert relation_edge_list({"relations": {}}) == []


# ---------------------------------------------------------------------------
# R7 - canonical binding agreement (bidirectional)
# ---------------------------------------------------------------------------

def test_matching_row_passes() -> None:
    """(a) a row that agrees with the catalogue produces no finding."""
    rows = [_row("maturity-model-technology", "dea:maturity-technology", "1.0.0")]
    refs = catalogue_reference_index(_catalogue_doc(_ref("dea:maturity-technology", "1.0.0")))
    assert check_canonical_bindings(rows, refs) == []


def test_version_mismatch_is_a_finding() -> None:
    """(b) the row's version and the catalogue's version must agree."""
    rows = [_row("maturity-model-technology", "dea:maturity-technology", "1.0.1")]
    refs = catalogue_reference_index(_catalogue_doc(_ref("dea:maturity-technology", "1.0.0")))
    findings = check_canonical_bindings(rows, refs)
    assert len(findings) == 1, findings
    assert findings[0].startswith("R7:"), findings
    assert "dea:maturity-technology" in findings[0]
    assert "1.0.1" in findings[0] and "1.0.0" in findings[0]


def test_unclaimed_catalogue_maturity_model_is_a_finding() -> None:
    """(c) every maturity model the catalogue publishes must be claimed."""
    rows = [_row("maturity-model-technology", "dea:maturity-technology", "1.0.0")]
    refs = catalogue_reference_index(
        _catalogue_doc(
            _ref("dea:maturity-technology", "1.0.0"),
            _ref("dea:maturity-modernization", "1.0.0", domain="modernization"),
        )
    )
    findings = check_canonical_bindings(rows, refs)
    assert len(findings) == 1, findings
    assert findings[0].startswith("R7:"), findings
    assert "dea:maturity-modernization" in findings[0]
    assert "claimed by no" in findings[0]


def test_two_rows_claiming_one_canonical_id_is_a_finding() -> None:
    """(d) a canonical id must be claimed by exactly one row."""
    rows = [
        _row("maturity-model-technology", "dea:maturity-technology", "1.0.0"),
        _row("maturity-model-technology-copy", "dea:maturity-technology", "1.0.0"),
    ]
    refs = catalogue_reference_index(_catalogue_doc(_ref("dea:maturity-technology", "1.0.0")))
    findings = check_canonical_bindings(rows, refs)
    assert len(findings) == 1, findings
    assert findings[0].startswith("R7:"), findings
    assert "dea:maturity-technology" in findings[0]
    assert "ambiguous" in findings[0]


def test_unknown_canonical_id_is_a_finding() -> None:
    """A row binding an id the catalogue does not publish cannot bind."""
    rows = [_row("maturity-model-ghost", "dea:maturity-ghost", "1.0.0")]
    refs = catalogue_reference_index(_catalogue_doc(_ref("dea:maturity-technology", "1.0.0")))
    findings = check_canonical_bindings(rows, refs)
    assert any(f.startswith("R7:") and "dea:maturity-ghost" in f for f in findings), findings
    # ...and the catalogue's own maturity model is now unclaimed.
    assert any("claimed by no" in f for f in findings), findings


def test_non_maturity_model_canonical_id_is_a_finding() -> None:
    """A capability id is not a maturity-model binding."""
    rows = [_row("maturity-model-technology", "dea:capability-technology-architecture", "1.0.0")]
    refs = catalogue_reference_index(
        _catalogue_doc(
            _ref("dea:capability-technology-architecture", "1.0.0", kind="capability"),
            _ref("dea:maturity-technology", "1.0.0"),
        )
    )
    findings = check_canonical_bindings(rows, refs)
    assert any("not maturity-model" in f for f in findings), findings
    assert any("claimed by no" in f for f in findings), findings


def test_bidirectional_agreement_cleans_when_both_sides_match() -> None:
    """The real population shape: two models, two rows, both directions."""
    rows = [
        _row("maturity-model-technology", "dea:maturity-technology", "1.0.0"),
        _row("maturity-model-modernization", "dea:maturity-modernization", "1.0.0"),
    ]
    refs = catalogue_reference_index(
        _catalogue_doc(
            _ref("dea:maturity-technology", "1.0.0"),
            _ref("dea:maturity-modernization", "1.0.0", domain="modernization"),
        )
    )
    assert check_canonical_bindings(rows, refs) == []


# ---------------------------------------------------------------------------
# R8 - no dangling catalogue reference
# ---------------------------------------------------------------------------

def test_relation_edge_pointing_at_an_absent_id_is_a_finding() -> None:
    """(e) an edge endpoint that resolves to nothing dangles."""
    ids = {"dea:maturity-technology", "dea:maturity-ea-capability"}
    edges = relation_edge_list(
        _relations_doc(_edge("dea:edge-x", "dea:maturity-ea-capability", "dea:maturity-ghost"))
    )
    findings = check_relation_endpoints(ids, edges)
    assert len(findings) == 1, findings
    assert findings[0].startswith("R8:"), findings
    assert "dea:maturity-ghost" in findings[0]


def test_relation_edge_pointing_at_a_present_id_is_not_a_finding() -> None:
    """(f) an edge whose endpoints both resolve is clean."""
    ids = {"dea:maturity-technology", "dea:maturity-ea-capability"}
    edges = relation_edge_list(
        _relations_doc(_edge("dea:edge-x", "dea:maturity-ea-capability", "dea:maturity-technology"))
    )
    assert check_relation_endpoints(ids, edges) == []


def test_relation_edge_with_a_dangling_source_is_a_finding() -> None:
    """The source end is checked as strictly as the target end."""
    ids = {"dea:maturity-technology"}
    edges = relation_edge_list(
        _relations_doc(_edge("dea:edge-x", "dea:maturity-ghost", "dea:maturity-technology"))
    )
    findings = check_relation_endpoints(ids, edges)
    assert len(findings) == 1, findings
    assert "source_id" in findings[0]
    assert "dea:maturity-ghost" in findings[0]


def test_register_canonical_id_that_does_not_resolve_is_a_finding() -> None:
    """R8 (register side): the register may not name a dangling id."""
    ids = {"dea:maturity-technology"}
    rows = [
        _row("maturity-model-technology", "dea:maturity-technology", "1.0.0"),
        _row("maturity-model-ghost", "dea:maturity-ghost", "1.0.0"),
    ]
    findings = check_register_references(ids, rows)
    assert len(findings) == 1, findings
    assert findings[0].startswith("R8:"), findings
    assert "dea:maturity-ghost" in findings[0]


def test_register_references_are_clean_when_every_id_resolves() -> None:
    ids = {"dea:maturity-technology", "dea:maturity-modernization"}
    rows = [
        _row("maturity-model-technology", "dea:maturity-technology", "1.0.0"),
        _row("maturity-model-modernization", "dea:maturity-modernization", "1.0.0"),
    ]
    assert check_register_references(ids, rows) == []


# ---------------------------------------------------------------------------
# per-row organization (no global org assumption)
# ---------------------------------------------------------------------------

def test_row_org_comes_from_the_row() -> None:
    assert _row_org({"repo": "x", "organization": "Assessment-Models"}) == "Assessment-Models"
    assert _row_org({"repo": "x", "organization": "technehub-labs"}) == "technehub-labs"


def test_row_org_falls_back_to_the_default_for_rows_without_one() -> None:
    """The catalog-portfolio population predates per-row ownership."""
    from reconcile_portfolio import DEFAULT_ORG

    assert _row_org({"repo": "dea-catalog-actors"}) == DEFAULT_ORG
    assert _row_org({"repo": "x", "organization": ""}) == DEFAULT_ORG
