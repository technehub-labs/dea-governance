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
  R5 directory-size no tracked directory holds 800+ entries (the §4 shard
                    trigger of entity-storage-layout.md; GitHub truncates
                    directory listings at 1,000); 500+ entries print a
                    watch warning without failing
  R6 pin-truth      every metaframework release tag pinned by a repo's CI
                    workflows exists on dea-metaframework (a pin merged
                    ahead of its release 404s at checkout); a workflow
                    naming the metaframework checkout without a release
                    tag ref prints a floating-pin watch without failing

Fails (exit 1) on any finding. Offline mode (no GITHUB_TOKEN): skips R2/R3/R5/R6
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
import re
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

# entity-storage-layout.md §4 (R5, CR-019): GitHub truncates a directory
# listing at 1,000 entries; the ratified contract shards before any
# directory approaches 800. 500+ prints a watch warning without failing,
# so a fast-growing intake surfaces in the weekly output early. The
# census counts git-tracked entries only (the git tree IS the tracked
# content), so local-only noise such as an untracked .venv never counts.
R5_WATCH_ENTRIES = 500
R5_SHARD_TRIGGER = 800

# R6 pin-truth (CR-021): the metaframework toolchain is tag-pinned across
# the org (CST-013/014); a pin merged ahead of its release 404s at every
# consumer checkout (observed 2026-11-11: a consumer pinned v2.8.0 the
# day the release was not yet cut). R6 verifies each release-tag pin
# against dea-metaframework's real tag set; a checkout naming the
# upstream without a release-tag ref is a floating pin ( CST-013 fails
# it at PR time in conformant repos) and prints a watch here.
META_REPOSITORY = "technehub-labs/dea-metaframework"
_META_STEP_SPLIT_RE = re.compile(r"(?=\n\s*-?\s*uses:)")
_META_REPO_RE = re.compile(rf"repository:\s*{re.escape(META_REPOSITORY)}")
_META_REF_RE = re.compile(r"^\s*ref:\s*[\"']?([^\s\"'#]+)", re.MULTILINE)
_TAG_REF_RE = re.compile(r"^v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


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


def _entry_counts_from_tree_entries(entries: list[dict]) -> dict[str, int]:
    """Immediate-entry count per directory from a recursive git-tree
    payload's `tree` list (pure; unit-tested).

    An entry is what a GitHub directory listing shows: a file or a
    subdirectory directly inside it. Blobs contribute one entry to their
    parent; directories are derived once from the path prefixes of the
    listed paths (the payload's explicit `tree` objects are NOT counted
    again, or every subdirectory would count twice). The repo root is
    keyed as ''. Submodule entries (type commit) are skipped: no catalog
    repo uses them, and a recursive tree lists no blobs beneath one.
    """
    counts: dict[str, int] = {}
    dirs: set[str] = set()
    for entry in entries:
        path = entry.get("path") or ""
        if not path:
            continue
        parts = path.split("/")
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]))
        if entry.get("type") == "blob":
            parent = "/".join(parts[:-1])
            counts[parent] = counts.get(parent, 0) + 1
    for d in dirs:
        parent = d.rsplit("/", 1)[0] if "/" in d else ""
        counts[parent] = counts.get(parent, 0) + 1
    return counts


def _fetch_tree(token: str | None, repo: str):
    """Recursive git tree of `main`; returns (tree_list_or_None, error).

    Shared by the R5 census and the R6 pin scan so one fetch serves both.
    A truncated payload returns an error rather than partial data: a
    finding must never fire on incomplete data.
    """
    tree, err = _get(f"{GITHUB_API}/repos/{ORG}/{repo}/git/trees/main?recursive=1", token, as_json=True)
    if tree is None:
        return None, err
    if tree.get("truncated"):
        return None, "trees: truncated"
    return tree.get("tree") or [], None


def _directory_entry_counts(tree_entries: list[dict]) -> dict[str, int]:
    """Immediate-entry census per directory from a fetched tree (R5)."""
    return _entry_counts_from_tree_entries(tree_entries)


def _extract_metaframework_pins(text: str) -> tuple[list[str], bool]:
    """Metaframework checkout refs in one workflow's text (pure; tested).

    Returns (release_tag_pins, has_metaframework_checkout_without_tag).
    A `ref:` counts only inside a step that names the upstream
    repository, so a root-model allocation pin is never mistaken for a
    metaframework pin. Branch refs and missing refs make the second
    element True (floating-pin watch, CR-021); release-tag refs come
    back in the list.
    """
    tag_pins: list[str] = []
    floating = False
    saw_metaframework = False
    for block in _META_STEP_SPLIT_RE.split(text):
        if not _META_REPO_RE.search(block):
            continue
        saw_metaframework = True
        refs = _META_REF_RE.findall(block)
        if not refs:
            floating = True
        for ref in refs:
            if _TAG_REF_RE.match(ref):
                tag_pins.append(ref)
            else:
                floating = True
    if saw_metaframework and floating:
        return tag_pins, True
    return tag_pins, False


def _fetch_raw_file(token: str | None, repo: str, path: str):
    """One file off `main` via raw.githubusercontent (size-safe route)."""
    raw, err = _get(f"https://raw.githubusercontent.com/{ORG}/{repo}/main/{path}", token)
    return raw, err


def _fetch_metaframework_tags(token: str | None):
    """All release tags on dea-metaframework (paginated), or
    (None, error) on transport failure."""
    tags: set[str] = set()
    for page in (1, 2):
        data, err = _get(
            f"{GITHUB_API}/repos/{ORG}/dea-metaframework/tags?per_page=100&page={page}",
            token, as_json=True,
        )
        if data is None:
            return None, err
        names = [t.get("name") for t in data if isinstance(t, dict) and t.get("name")]
        if not names and page == 1:
            break
        tags.update(n for n in names if _TAG_REF_RE.match(n))
        if len(names) < 100:
            break
    return tags, None


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
        print("WARN: no GITHUB_TOKEN/GH_TOKEN; R2/R3/R5/R6 skipped (offline mode)")
    else:
        meta_tags, merr = _fetch_metaframework_tags(token)
        if meta_tags is None:
            print(f"WARN: R6 skipped (metaframework tag list unavailable: {merr})")
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
            # R5 directory-size audit (CR-019) + R6 pin-truth (CR-021),
            # off one tree fetch. Run before the index read so
            # bespoke-index repos (metrics, roles) are audited too; a
            # truncated tree payload warns and skips rather than fail.
            tree_entries, err = _fetch_tree(token, repo)
            if tree_entries is None:
                print(f"WARN: R5/R6 skipped for {repo} ({err})")
            else:
                counts = _directory_entry_counts(tree_entries)
                for d in sorted(counts, key=lambda x: (-counts[x], x)):
                    n = counts[d]
                    if n >= R5_SHARD_TRIGGER:
                        findings.append(
                            f"R5: {repo}/{d or '<root>'} holds {n} entries "
                            f"(entity-storage-layout §4 shard trigger {R5_SHARD_TRIGGER}; "
                            f"GitHub truncates listings at 1,000); introduce a shard "
                            f"(CR-MET-024 recipe)"
                        )
                    elif n >= R5_WATCH_ENTRIES:
                        print(f"WARN: R5 watch: {repo}/{d or '<root>'} holds {n} entries")
                if meta_tags is not None:
                    wf_paths = sorted(
                        e["path"] for e in tree_entries
                        if e.get("type") == "blob"
                        and e.get("path", "").startswith(".github/workflows/")
                        and e.get("path", "").endswith((".yml", ".yaml"))
                    )
                    for wf_path in wf_paths:
                        text, werr = _fetch_raw_file(token, repo, wf_path)
                        if text is None:
                            print(f"WARN: R6 skipped {repo}/{wf_path} ({werr})")
                            continue
                        tag_pins, floating = _extract_metaframework_pins(text)
                        for pin in tag_pins:
                            if pin not in meta_tags:
                                findings.append(
                                    f"R6: {repo} pins nonexistent metaframework release tag "
                                    f"{pin} in {wf_path} (checkout will 404); cut the release "
                                    f"first, then bump the pin"
                                )
                        if floating:
                            print(
                                f"WARN: R6 floating pin: {repo}/{wf_path} names "
                                f"{META_REPOSITORY} without a release-tag ref"
                            )
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
