"""Unit tests for the R5 directory-entry census (CR-019).

These pin the counting semantics against a synthetic recursive git-tree
payload. The regression this guards: the trees API lists subdirectories
as explicit `tree` objects, and counting those objects as entries in
their parent double-counts every directory (the first R5 implementation
reported 1,071 entries for a 536-entry directory). Directories are
derived once from path prefixes; only blobs add parent entries.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reconcile_portfolio import _entry_counts_from_tree_entries  # noqa: E402


def _tree_payload() -> list[dict]:
    """A tiny repo: README.md at root; entities/v1-alpha/ holding two
    record dirs (one with yaml+README, one with yaml only) plus .gitkeep;
    docs/ with one file. Mirrors the org's record-dir shape."""
    return [
        {"path": "CATALOG.yaml", "type": "blob"},
        {"path": "README.md", "type": "blob"},
        {"path": "entities", "type": "tree"},
        {"path": "entities/v1-alpha", "type": "tree"},
        {"path": "entities/v1-alpha/.gitkeep", "type": "blob"},
        {"path": "entities/v1-alpha/alpha", "type": "tree"},
        {"path": "entities/v1-alpha/alpha/record-a.yaml", "type": "blob"},
        {"path": "entities/v1-alpha/alpha/README.md", "type": "blob"},
        {"path": "entities/v1-alpha/beta", "type": "tree"},
        {"path": "entities/v1-alpha/beta/record-b.yaml", "type": "blob"},
        {"path": "docs", "type": "tree"},
        {"path": "docs/notes.md", "type": "blob"},
    ]


def test_counts_match_github_listing_semantics() -> None:
    counts = _entry_counts_from_tree_entries(_tree_payload())
    assert counts["entities/v1-alpha"] == 3, counts  # .gitkeep + alpha/ + beta/
    assert counts["entities/v1-alpha/alpha"] == 2, counts
    assert counts["entities/v1-alpha/beta"] == 1, counts
    assert counts["docs"] == 1, counts
    assert counts[""] == 4, counts  # CATALOG.yaml + README.md + entities/ + docs/
    assert counts.get("entities") == 1, counts  # v1-alpha/


def test_no_double_count_of_tree_objects() -> None:
    """The regression: explicit `tree` objects must not count as entries,
    or a 604-entry shard reports 1,207."""
    payload = [{"path": "shard", "type": "tree"}]
    payload += [{"path": f"shard/record-{i}", "type": "tree"} for i in range(603)]
    payload += [
        {"path": f"shard/record-{i}/record-{i}.yaml", "type": "blob"}
        for i in range(603)
    ]
    payload.append({"path": "shard/README.md", "type": "blob"})
    counts = _entry_counts_from_tree_entries(payload)
    assert counts["shard"] == 604, counts  # 603 dirs + 1 README, counted once each
    assert all(counts[f"shard/record-{i}"] == 1 for i in range(603)), counts
