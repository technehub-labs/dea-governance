#!/usr/bin/env python3
"""Portfolio reconciliation (CR-014; extended by CR-023).

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

CR-023 extends the reconciler to the federation's assessment-model
population (registers/assessment-model-portfolio.yaml) and binds it to
the federation's canonical reference root (dea-metamodel):

  R7 canonical binding   (bidirectional, register <-> catalogue)
                    every register row binds a canonical id the upstream
                    reference catalogue publishes, as a maturity-model
                    reference, at the catalogue's own version; and every
                    maturity-model reference the catalogue publishes is
                    claimed by EXACTLY ONE register row (none claims it:
                    unclaimed canonical model; several claim it:
                    ambiguous binding)
  R8 dangling reference every canonical id the assessment-model register
                    references, and every source_id/target_id of the
                    upstream relation graph, resolves to an id the
                    upstream reference catalogue publishes
  R9 repo resolution   every assessment-model row resolves to a
                    repository that exists in the organization THAT ROW
                    declares, at the immutable release THAT ROW declares

The canonical reference root is read from dea-metamodel (raw, ref main):
  assessment-models/catalog/reference-catalog.yaml  (the catalogue)
  assessment-models/catalog/model-relations.yaml    (the relation graph)
Both are public, so these reads need no credential; the upstream catalogue
is the authority for WHAT version exists (canonical identity + version),
while the register is the authority for WHERE that version is published
(the repository pointer + the immutable release). Neither duplicates the
other.

ORGANIZATIONS ARE PER ROW, NEVER GLOBAL. Every URL the reconciler builds
for a register row is built from that row's `organization` value. The
catalog-portfolio population predates per-row ownership and carries no
organization field, so it falls back to the federation default
organization (DEFAULT_ORG) and R1-R6 behave exactly as before. The
assessment-model population declares its owning organization per row,
which is what lets one reconciler span organizations (Assessment-Models,
technehub-labs) without a hard-coded assumption.

Fails (exit 1) on any finding. Offline mode (no GITHUB_TOKEN): skips the
API-gated rules R2/R3/R5/R6/R9 with a warning and still enforces R1/R4
from the vendored inputs. The catalogue-backed rules R7/R8 read the
public upstream root and run whenever that root is reachable; when it is
not, they are skipped with a printed WARN - a rule that cannot read its
inputs never passes silently and never fires a finding on a transport
flake.

Usage:
  python3 registers/reconcile_portfolio.py \
      [--register registers/catalog-portfolio.yaml] \
      [--assessment-register registers/assessment-model-portfolio.yaml] \
      [--metamodel-url URL]   # default: raw main of dea-metamodel
      [--catalogue-url URL]   # default: raw main of dea-metamodel
      [--relations-url URL]   # default: raw main of dea-metamodel
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

# DEFAULT_ORG is a FALLBACK, never an assumption. It is used ONLY for
# register rows that declare no `organization` of their own (the whole
# catalog-portfolio population, which predates per-row ownership). A row
# that declares an organization is resolved against THAT organization,
# and every URL built for it carries that organization.
DEFAULT_ORG = "technehub-labs"

DEFAULT_METAMODEL_URL = (
    "https://raw.githubusercontent.com/technehub-labs/dea-metamodel/main/metamodel/dea-metamodel.yaml"
)
DEFAULT_CATALOGUE_URL = (
    "https://raw.githubusercontent.com/technehub-labs/dea-metamodel/main/"
    "assessment-models/catalog/reference-catalog.yaml"
)
DEFAULT_RELATIONS_URL = (
    "https://raw.githubusercontent.com/technehub-labs/dea-metamodel/main/"
    "assessment-models/catalog/model-relations.yaml"
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


def _is_missing(err: str | None) -> bool:
    """True only for a DEFINITIVE "not there" answer.

    A transport failure (timeout, reset, DNS) is not evidence of absence:
    a finding must never fire on a network flake, so only an HTTP 404
    counts. A 403 means the resource exists but is not visible to this
    credential (CR-022A's private-repo class): that is an access
    problem, not absence, so it warns instead of finding.
    """
    return (err or "").strip() == "HTTP 404"


def _row_org(row: dict) -> str:
    """The GitHub organization that owns a register row's repository.

    Every URL the reconciler builds for a row is built from this value.
    Rows that declare no `organization` (the catalog-portfolio
    population, which predates per-row ownership) fall back to the
    federation default organization, which keeps R1-R6 exactly as they
    were.
    """
    org = str(row.get("organization") or "").strip()
    return org or DEFAULT_ORG


def _read_index(token: str | None, repo: str, org: str):
    """Read CATALOG.yaml size-safely (CR-016).

    The contents API cannot return files over 1 MB as base64 (the metrics
    catalog's 4 MB index read as empty and was counted as 0 canonical by
    every index-based pass until the owner challenged the org total). The
    git-trees + git-blobs route has no such limit and also reports ABSENT
    distinctly. Returns (text_or_'ABSENT'_or_None, error).
    """
    # Route 1: raw (serves any size; reliable for the multi-MB indexes).
    raw, err = _get(f"https://raw.githubusercontent.com/{org}/{repo}/main/CATALOG.yaml", token)
    if raw is not None:
        return raw, None
    # Route 2: git trees + blobs (exact; but multi-MB tree payloads can
    # truncate on flaky connections, hence the raw route first).
    tree, terr = _get(f"{GITHUB_API}/repos/{org}/{repo}/git/trees/main?recursive=1", token, as_json=True)
    if tree is None:
        return None, f"raw: {err}; trees: {terr}"
    entries = tree.get("tree") or []
    if tree.get("truncated"):
        return None, "trees: truncated"
    target = next((e for e in entries if e.get("path") == "CATALOG.yaml"), None)
    if target is None:
        return "ABSENT", None
    blob, err = _get(f"{GITHUB_API}/repos/{org}/{repo}/git/blobs/{target['sha']}", token, as_json=True)
    if blob is None:
        return None, f"blobs: {err}"
    content = blob.get("content") or ""
    import base64 as _b64
    return _b64.b64decode(content).decode("utf-8", errors="replace"), None


def _entity_file_count(token: str | None, repo: str, org: str):
    """Count entity YAML blobs under entities/ from the same tree (cross-check)."""
    tree, err = _get(f"{GITHUB_API}/repos/{org}/{repo}/git/trees/main?recursive=1", token, as_json=True)
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


def _fetch_tree(token: str | None, repo: str, org: str):
    """Recursive git tree of `main`; returns (tree_list_or_None, error).

    Shared by the R5 census and the R6 pin scan so one fetch serves both.
    A truncated payload returns an error rather than partial data: a
    finding must never fire on incomplete data.
    """
    tree, err = _get(f"{GITHUB_API}/repos/{org}/{repo}/git/trees/main?recursive=1", token, as_json=True)
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


def _fetch_raw_file(token: str | None, repo: str, path: str, org: str):
    """One file off `main` via raw.githubusercontent (size-safe route)."""
    raw, err = _get(f"https://raw.githubusercontent.com/{org}/{repo}/main/{path}", token)
    return raw, err


def _fetch_metaframework_tags(token: str | None):
    """All release tags on dea-metaframework (paginated), or
    (None, error) on transport failure."""
    tags: set[str] = set()
    for page in (1, 2):
        data, err = _get(
            f"{GITHUB_API}/repos/{META_REPOSITORY}/tags?per_page=100&page={page}",
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


# ---------------------------------------------------------------------------
# CR-023: the canonical binding against the federation's reference root.
#
# The rule semantics live in PURE functions below, unit-tested offline
# (registers/test_reconcile_canonical_bindings.py). The shell around them
# only fetches inputs and turns findings into output.
# ---------------------------------------------------------------------------

def catalogue_reference_index(catalogue: dict) -> dict[str, dict]:
    """Index the upstream reference catalogue: id -> {kind, version, domain}.

    The catalogue's shape is {catalogue: {..., references: [...]}}; every
    entry in `references` is {kind, id, version, domain}. Pure.
    """
    refs: dict[str, dict] = {}
    doc = catalogue or {}
    body = doc.get("catalogue") or {}
    for ref in body.get("references") or []:
        if not isinstance(ref, dict):
            continue
        rid = ref.get("id")
        if not rid:
            continue
        refs[rid] = {
            "kind": ref.get("kind"),
            "version": str(ref.get("version")),
            "domain": ref.get("domain"),
        }
    return refs


def relation_edge_list(relations: dict) -> list[dict]:
    """The relation graph's edges: {relations: {..., edges: [...]}}.

    Each edge carries id, source_id, target_id and relationship_type;
    `dotted_line` and `trace` are optional. Pure.
    """
    doc = relations or {}
    body = doc.get("relations") or {}
    return [e for e in (body.get("edges") or []) if isinstance(e, dict)]


def _version_str(value) -> str:
    """Normalise a version for comparison.

    YAML reads `1.0.0` as a string but `1.0` as a float; the same
    version must compare equal however it was spelled.
    """
    if value is None:
        return ""
    text = str(value).strip()
    if text.endswith(".0") and text.count(".") == 1:
        text = text[:-2]
    return text


def check_canonical_bindings(rows: list[dict], catalogue_refs: dict[str, dict]) -> list[str]:
    """R7: the register and the catalogue must agree on canonical identity.

    Two directions, both required:

      row -> catalogue   every register row binds a canonical id the
                         catalogue publishes, as a maturity-model
                         reference, at the catalogue's own version
      catalogue -> row   every maturity-model reference the catalogue
                         publishes is claimed by EXACTLY ONE register row
                         (no row claims it: unclaimed canonical model;
                         several rows claim it: ambiguous binding)

    `rows` are assessment-model register rows; `catalogue_refs` is the
    catalogue index (id -> {kind, version, domain}). Returns findings.
    Pure.
    """
    findings: list[str] = []
    claims: dict[str, list[str]] = {}

    for row in rows:
        repo = row.get("repo") or "<unnamed row>"
        cid = row.get("canonical_id")
        if not cid:
            findings.append(f"R7: {repo} carries no canonical_id to bind")
            continue
        claims.setdefault(cid, []).append(repo)
        ref = catalogue_refs.get(cid)
        if ref is None:
            findings.append(
                f"R7: {repo} binds canonical id {cid} which the upstream "
                f"reference catalogue does not publish"
            )
            continue
        if ref.get("kind") != "maturity-model":
            findings.append(
                f"R7: {repo} binds canonical id {cid} which the upstream "
                f"catalogue publishes as kind={ref.get('kind')!r}, not maturity-model"
            )
        row_version = _version_str(row.get("canonical_version"))
        cat_version = _version_str(ref.get("version"))
        if row_version != cat_version:
            findings.append(
                f"R7: {repo} binds canonical id {cid} at version {row_version} "
                f"but the upstream catalogue publishes version {cat_version}"
            )

    for cid, ref in sorted(catalogue_refs.items()):
        if ref.get("kind") != "maturity-model":
            continue
        claimants = claims.get(cid) or []
        if not claimants:
            findings.append(
                f"R7: upstream catalogue maturity model {cid} "
                f"(version {ref.get('version')}) is claimed by no assessment-model "
                f"register row"
            )
        elif len(claimants) > 1:
            findings.append(
                f"R7: canonical id {cid} is claimed by {len(claimants)} "
                f"assessment-model register rows ({', '.join(sorted(claimants))}); "
                f"the binding is ambiguous"
            )
    return findings


def check_relation_endpoints(catalogue_ids: set[str], edges: list[dict]) -> list[str]:
    """R8 (relation graph): every edge endpoint must resolve.

    Each edge's source_id and target_id must be an id the upstream
    reference catalogue publishes. `catalogue_ids` is the set of
    catalogue ids; `edges` is the relation graph's edge list. Returns
    findings. Pure.
    """
    findings: list[str] = []
    for edge in edges:
        eid = edge.get("id") or "<unnamed edge>"
        for field in ("source_id", "target_id"):
            cid = edge.get(field)
            if cid is None:
                continue
            if cid not in catalogue_ids:
                findings.append(
                    f"R8: relation edge {eid} {field} {cid} does not resolve "
                    f"in the upstream reference catalogue"
                )
    return findings


def check_register_references(catalogue_ids: set[str], rows: list[dict]) -> list[str]:
    """R8 (register): every canonical id the register names must resolve.

    `catalogue_ids` is the set of ids the upstream reference catalogue
    publishes; `rows` are assessment-model register rows. Returns
    findings. Pure.
    """
    findings: list[str] = []
    for row in rows:
        cid = row.get("canonical_id")
        repo = row.get("repo") or "<unnamed row>"
        if not cid:
            continue
        if cid not in catalogue_ids:
            findings.append(
                f"R8: assessment-model register row {repo} references canonical id "
                f"{cid} which does not resolve in the upstream reference catalogue"
            )
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", type=Path, default=REPO / "registers" / "catalog-portfolio.yaml")
    ap.add_argument(
        "--assessment-register",
        type=Path,
        default=REPO / "registers" / "assessment-model-portfolio.yaml",
    )
    ap.add_argument("--metamodel-url", default=DEFAULT_METAMODEL_URL)
    ap.add_argument("--catalogue-url", default=DEFAULT_CATALOGUE_URL)
    ap.add_argument("--relations-url", default=DEFAULT_RELATIONS_URL)
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
        print(
            "WARN: no GITHUB_TOKEN/GH_TOKEN; R2/R3/R5/R6/R9 skipped (offline mode); "
            "R7/R8 read the public upstream reference root (no credential required)"
        )
    else:
        meta_tags, merr = _fetch_metaframework_tags(token)
        if meta_tags is None:
            print(f"WARN: R6 skipped (metaframework tag list unavailable: {merr})")
        for repo, reg in sorted(entries.items()):
            org = _row_org(reg)
            api, err = _get(f"{GITHUB_API}/repos/{org}/{repo}", token, as_json=True)
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
            tree_entries, err = _fetch_tree(token, repo, org)
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
                        text, werr = _fetch_raw_file(token, repo, wf_path, org)
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
            cat_text, err = _read_index(token, repo, org)
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
                        file_count, ferr = _entity_file_count(token, repo, org)
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

    # ------------------------------------------------------------------
    # CR-023: the assessment-model population, bound to the federation's
    # canonical reference root.
    # ------------------------------------------------------------------
    models: list[dict] = []
    if args.assessment_register.exists():
        assessment = yaml.safe_load(args.assessment_register.read_text(encoding="utf-8")) or {}
        models = [m for m in (assessment.get("models") or []) if isinstance(m, dict)]
        print(f"Assessment-model entries: {len(models)}")
    else:
        print(f"WARN: assessment-model register not found at {args.assessment_register}; R7/R8/R9 skipped")

    # The canonical reference root: the reference catalogue (the authority
    # for canonical identity and version) and the relation graph. Both are
    # public, so these reads work with or without a credential. When the
    # root is unreachable the affected rules are SKIPPED WITH A WARN:
    # never crash, and never pass silently.
    catalogue_refs: dict[str, dict] = {}
    catalogue_ids: set[str] = set()
    edges: list[dict] = []
    catalogue_text, cerr = _get(args.catalogue_url, token)
    if catalogue_text is None:
        print(f"WARN: upstream reference catalogue unavailable ({cerr}); R7/R8 skipped")
    else:
        try:
            catalogue_refs = catalogue_reference_index(yaml.safe_load(catalogue_text) or {})
            catalogue_ids = set(catalogue_refs)
        except Exception as e:  # noqa: BLE001
            print(f"WARN: upstream reference catalogue does not parse ({e}); R7/R8 skipped")
            catalogue_refs = {}

    relations_text, rerr = _get(args.relations_url, token)
    if relations_text is None:
        print(f"WARN: upstream relation graph unavailable ({rerr}); R8 relation-endpoint check skipped")
    else:
        try:
            edges = relation_edge_list(yaml.safe_load(relations_text) or {})
        except Exception as e:  # noqa: BLE001
            print(f"WARN: upstream relation graph does not parse ({e}); R8 relation-endpoint check skipped")
            edges = []

    if models and catalogue_refs:
        # R7: the register and the catalogue agree on canonical identity,
        # in both directions.
        findings.extend(check_canonical_bindings(models, catalogue_refs))
    if models and catalogue_ids:
        # R8 (register side): every canonical id the register names
        # resolves in the catalogue.
        findings.extend(check_register_references(catalogue_ids, models))
    if catalogue_ids:
        # R8 (relation graph side): every edge endpoint resolves.
        findings.extend(check_relation_endpoints(catalogue_ids, edges))

    # R9: the assessment-model repositories resolve, in the organization
    # EACH ROW declares, at the immutable release EACH ROW declares.
    if models:
        if not token:
            print("WARN: R9 skipped for the assessment-model population (offline mode: no token)")
        else:
            for row in models:
                repo = row.get("repo")
                org = _row_org(row)
                release = row.get("release")
                api, err = _get(f"{GITHUB_API}/repos/{org}/{repo}", token, as_json=True)
                if api is None:
                    if _is_missing(err):
                        findings.append(
                            f"R9: assessment-model repository {org}/{repo} does not exist "
                            f"(the register declares it as the home of {row.get('canonical_id')})"
                        )
                    else:
                        print(f"WARN: R9 skipped {org}/{repo} (repository unreadable: {err})")
                    continue
                if not release:
                    findings.append(
                        f"R9: assessment-model repository {org}/{repo} declares no release reference"
                    )
                    continue
                ref, terr = _get(
                    f"{GITHUB_API}/repos/{org}/{repo}/git/ref/tags/{release}", token, as_json=True
                )
                if ref is None:
                    if _is_missing(terr):
                        findings.append(
                            f"R9: assessment-model repository {org}/{repo} has no release "
                            f"{release} (the immutable reference does not resolve)"
                        )
                    else:
                        print(
                            f"WARN: R9 skipped {org}/{repo} (release {release} unreadable: {terr})"
                        )

    print(f"Findings: {len(findings)}")
    for f in findings:
        print(f"FAIL: {f}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
