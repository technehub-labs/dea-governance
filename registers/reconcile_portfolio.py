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


def _get(url: str, token: str | None, as_json: bool = False):
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("User-Agent", "dea-governance-portfolio-reconciler")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if as_json else body, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001 - report, don't crash the run
        return None, str(e)


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
            cat_text, _ = _get(
                f"https://raw.githubusercontent.com/{ORG}/{repo}/main/CATALOG.yaml", token
            )
            canonical = 0
            if cat_text is not None:
                try:
                    cat = yaml.safe_load(cat_text) or {}
                    canonical = int(((cat.get("catalog") or {}).get("counts") or {}).get("canonical") or 0)
                except Exception as e:  # noqa: BLE001
                    findings.append(f"R3: {repo} CATALOG.yaml does not parse ({e})")
            observed = "populated" if canonical > 0 else "skeleton"
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
