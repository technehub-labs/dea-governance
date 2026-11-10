"""Unit tests for the R6 pin-truth extraction (CR-021).

Offline: pins `_extract_metaframework_pins` against synthetic workflow
texts. The semantics mirror the metaframework's own CST-013 extraction
(step-scoped): a `ref:` counts only under a step that names the
metaframework repository, so the validate-allocation reusable call's
root-model ref is never mistaken for a metaframework pin.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reconcile_portfolio import _extract_metaframework_pins  # noqa: E402


def test_tag_pin_extracted() -> None:
    text = (
        "      - name: Fetch tools\n"
        "        uses: actions/checkout@v4\n"
        "        with:\n"
        "          repository: technehub-labs/dea-metaframework\n"
        "          ref: v2.8.0\n"
        "          path: .metaframework\n"
    )
    pins, floating = _extract_metaframework_pins(text)
    assert pins == ["v2.8.0"], pins
    assert floating is False


def test_root_model_ref_not_mistaken() -> None:
    text = (
        "      - uses: technehub-labs/dea-architecture-framework/"
        ".github/workflows/validate-against-model.yml@v0.2.1\n"
        "      - name: Fetch tools\n"
        "        uses: actions/checkout@v4\n"
        "        with:\n"
        "          repository: technehub-labs/dea-metaframework\n"
        "          ref: v2.7.0\n"
    )
    pins, floating = _extract_metaframework_pins(text)
    assert pins == ["v2.7.0"], pins
    assert floating is False


def test_branch_ref_is_floating_not_tag() -> None:
    text = (
        "        with:\n"
        "          repository: technehub-labs/dea-metaframework\n"
        "          ref: main\n"
    )
    pins, floating = _extract_metaframework_pins(text)
    assert pins == [], pins
    assert floating is True


def test_missing_ref_is_floating() -> None:
    text = (
        "        with:\n"
        "          repository: technehub-labs/dea-metaframework\n"
        "          path: .metaframework\n"
    )
    pins, floating = _extract_metaframework_pins(text)
    assert pins == [], pins
    assert floating is True


def test_no_metaframework_reference_is_clean() -> None:
    text = (
        "      - uses: actions/checkout@v4\n"
        "      - run: python scripts/regenerate_catalog.py --check\n"
    )
    pins, floating = _extract_metaframework_pins(text)
    assert pins == [] and floating is False
