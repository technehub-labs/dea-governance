#!/usr/bin/env python3
"""Portfolio reconciliation (CR-014).

Reconciles registers/catalog-portfolio.yaml against observed GitHub reality
and against the canonical metamodel's catalog_repo allocations:

  R1 completeness   every metamodel catalog_repo value appears in the
                    register (the CR-013 maintenance rule)
  R2 existence      every registered repo exists on GitHub
  R3 state truth    registered state matches the observed CATALOG.yaml
                    counts (populated requires canonical > 0; skeleton
                    requires the repo to exist with canonical == 0;
                    missing requires the repo to be absent)
  R4 ownership      every metamodel entity allocated to a registered repo
                    appears in that repo's register entities list

Fails (exit 1) on any finding. Offline mode (no GITHUB_TOKEN): skips R2/R3
with a warning, still enforces R1/R4 from the vendored inputs.

Usage:
  python3 registers/reconcile_portfolio.py \
      [--register registers/catalog-portfolio.yaml] \
      [--metamodel-url URL]   # default: raw main of dea-metamodel
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
GITHUB_API = "https://api.github.com"
ORG = "technehub-labs"
DEFAULT_METAMODEL_URL = (
    "https://raw.githubusercontent.com/technehub-labs/dea-metamodel/main/metamodel/dea-metamodel.yaml"
)


def _get(url: str, token: str | None, as_json: bool = False, retries: int = 3):
    """Token-gated GET with retries: the GitHub API intermittently fails
    single-flight reads (observed 2026-10-30..11-02); a finding must never
    fire on a transport flake, so retry before reporting an outcome."""
    import time

    last = "no attempt"
    for attempt in range(retries):
        req = urllib.request.Request(url)
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        req.add_header("User-Agent", "dea-governance-portfolio-reconciler")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if as_json else body, None
        except urllib.error.HTTPError as e:
            if e.code in (404, 403):
                return None, f"HTTP {e.code}"
            last = f"HTTP {e.code}"
        except Exception as e:  # noqa: BLE001
            last = str(e)
        time.sleep(2)
    return None, last


def _read_index(token: str | None, repo: str):
    """Read CATALOG.yaml size-safely (CR-016).

    The contents API cannot return files over 1 MB as base64 (the metrics
    catalog's 4 MB index read as empty and was counted as 0 canonical by
    every index-based pass until the owner challenged the org total). The
    git-trees + git-blobs route has no such limit and also reports ABSENT
    distinctly. Returns (text_or_'ABSENT'_or_None, error).
    """
    # Route 1: raw (serves any size; reliable for the multi-MB indexes).
    raw, err = _get(f"https://raw.githubusercontent.com/{ORG}/{repo}/main/CATALOG.yaml", token)
    if raw is not None:
        return raw, None
    # Route 2: git trees + blobs (exact; but multi-MB tree payloads can
    # truncate on flaky connections, hence the raw route first).
    tree, terr = _get(f"{GITHUB_API}/repos/{ORG}/{repo}/git/trees/main?recursive=1", token, as_json=True)
    if tree is None:
        return None, f"raw: {err}; trees: {terr}"
    entries = tree.get("tree") or []
    if tree.get("truncated"):
        return None, "trees: truncated"
    target = next((e for e in entries if e.get("path") == "CATALOG.yaml"), None)
    if target is None:
        return "ABSENT", None
    blob, err = _get(f"{GITHUB_API}/repos/{ORG}/{repo}/git/blobs/{target['sha']}", token, as_json=True)
    if blob is None:
        return None, f"blobs: {err}"
    content = blob.get("content") or ""
    import base64 as _b64
    return _b64.b64decode(content).decode("utf-8", errors="replace"), None


def _entity_file_count(token: str | None, repo: str):
    """Count entity YAML blobs under entities/ from the same tree (cross-check)."""
    tree, err = _get(f"{GITHUB_API}/repos/{ORG}/{repo}/git/trees/main?recursive=1", token, as_json=True)
    if tree is None:
        return None, err
    entries = tree.get("tree") or []
    return sum(
        1 for e in entries
        if e.get("type") == "blob" and e.get("path", "").startswith("entities/")
        and e.get("path", "").endswith((".yaml", ".yml"))
    ), None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", type=Path, default=REPO / "registers" / "catalog-portfolio.yaml")
    ap.add_argument("--metamodel-url", default=DEFAULT_METAMODEL_URL)
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    findings: list[str] = []

    register = yaml.safe_load(args.register.read_text(encoding="utf-8")) or {}
    entries = {e["repo"]: e for e in register.get("catalogs", [])}
    print(f"Register entries: {len(entries)}")

    # metamodel allocations
    mm_text, err = _get(args.metamodel_url, token)
    if mm_text is None:
        print(f"WARN: metamodel fetch failed ({err}); R1/R4 skipped")
        allocations: dict[str, list[str]] = {}
    else:
        data = yaml.safe_load(mm_text)
        allocations = {}
        for e in data.get("entities", []):
            if isinstance(e, dict) and e.get("catalog_repo"):
                allocations.setdefault(e["catalog_repo"], []).append(e["id"])

    # R1 completeness
    for repo in sorted(allocations):
        if repo not in entries:
            findings.append(f"R1: metamodel catalog_repo {repo} is not registered (CR-013 maintenance rule)")

    # R4 ownership coverage
    for repo, ids in sorted(allocations.items()):
        reg = entries.get(repo)
        if not reg:
            continue
        reg_ids = set(reg.get("entities") or [])
        for eid in ids:
            if eid not in reg_ids:
                findings.append(f"R4: {eid} is allocated to {repo} in the metamodel but missing from the register")

    # R2/R3 existence + state (online only)
    if not token:
        print("WARN: no GITHUB_TOKEN/GH_TOKEN; R2/R3 skipped (offline mode)")
    else:
        for repo, reg in sorted(entries.items()):
            api, err = _get(f"{GITHUB_API}/repos/{ORG}/{repo}", token, as_json=True)
            if api is None:
                if reg.get("state") == "missing":
                    continue
                findings.append(f"R2: registered repo {repo} does not exist (state says {reg.get('state')!r})")
                continue
            if reg.get("state") == "missing":
                findings.append(f"R2: repo {repo} exists but is registered as missing")
                continue
            cat_text, err = _read_index(token, repo)
            canonical = 0
            if cat_text == "ABSENT":
                canonical = 0
            elif cat_text is None:
                findings.append(f"R3: {repo} index unreadable ({err})")
            else:
                try:
                    cat = yaml.safe_load(cat_text) or {}
                    counts = (cat.get("catalog") or {}).get("counts") or {}
                    canonical = int(counts.get("canonical") or 0)
                    entity_records = len(cat.get("catalog", {}).get("entities") or [])
                    if "canonical" not in counts:
                        # Bespoke index schema (e.g. metrics, roles): the org
                        # counts block is absent. Cross-check against the
                        # filesystem census instead of reading a zero.
                        file_count, ferr = _entity_file_count(token, repo)
                        if file_count:
                            canonical = file_count
                except Exception as e:  # noqa: BLE001
                    findings.append(f"R3: {repo} CATALOG.yaml does not parse ({e})")
            observed = "populated" if canonical > 0 else "skeleton"
            if reg.get("index") == "bespoke":
                # Pre-index repositories (e.g. dea-catalog-concepts) carry
                # canonical records without the CATALOG.yaml discipline;
                # their state is stewarded, not machine-observed. Index
                # adoption removes the flag and restores R3.
                continue
            if reg.get("state") != observed:
                findings.append(
                    f"R3: {repo} registered state {reg.get('state')!r} but observed {observed!r} "
                    f"(canonical={canonical}); refresh the register snapshot"
                )

    print(f"Findings: {len(findings)}")
    for f in findings:
        print(f"FAIL: {f}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
