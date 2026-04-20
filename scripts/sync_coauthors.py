#!/usr/bin/env python3
"""
Populate _data/coauthors.yml from InspireHEP paper author lists.

Reads inspirehep_id values from papers.bib, fetches each paper's author list,
resolves each co-author's profile URL, and writes coauthors.yml in the format
expected by _layouts/bib.liquid:

    "lastname":
      - firstname: ["Full Name", "F.", "F. M."]
        url: https://...

Name key normalisation matches the Liquid filter chain used in bib.liquid:
    downcase | remove_accents
which is: NFD decompose → strip combining chars → lowercase.

URL priority per co-author:
  1. InspireHEP profile URL marked as "homepage" (PERSONAL_WEBSITE / BLOG)
  2. First URL listed on the InspireHEP author profile
  3. ORCID public profile (https://orcid.org/{orcid})
  4. InspireHEP literature search fallback

Usage:
    python3 scripts/sync_coauthors.py
    python3 scripts/sync_coauthors.py --dry-run
    python3 scripts/sync_coauthors.py --max-authors 15 --self-id 1410753
    python3 scripts/sync_coauthors.py --bib-file _bibliography/papers.bib \\
                                      --output _data/coauthors.yml
"""

import argparse
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    import json
except ImportError:
    import simplejson as json  # type: ignore

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_BIB_FILE = "_bibliography/papers.bib"
DEFAULT_OUTPUT = "_data/coauthors.yml"
DEFAULT_MAX_AUTHORS = 20
DEFAULT_SELF_ID = "1410753"
API_DELAY = 0.4  # seconds between requests


# ── HTTP helper ───────────────────────────────────────────────────────────────

def _fetch_json(url: str, retries: int = 3) -> dict:
    req = Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "sync_coauthors/1.0 (academic portfolio; python-urllib)")
    for attempt in range(retries):
        try:
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except (URLError, HTTPError) as exc:
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"    Retry {attempt + 1} after {wait}s ({exc})")
            time.sleep(wait)
    raise RuntimeError("unreachable")


# ── Name normalisation (matches bib.liquid's downcase | remove_accents) ───────

def _normalise_key(name: str) -> str:
    """NFD-decompose, strip combining chars, lowercase — mirrors Liquid filter."""
    nfd = unicodedata.normalize("NFD", name)
    stripped = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return stripped.lower()


def _first_name_variants(full_first: str) -> list[str]:
    """
    Return all first-name forms that bib.liquid might match against.

    bib.liquid checks:  coauthor.firstname contains author.first
    where author.first is the whitespace-separated first token of the BibTeX
    first name (which InspireHEP formats as "First M." or "First").

    We therefore generate:
      - the full given name as returned by InspireHEP  ("Helena")
      - first word only                                 ("Helena")
      - all initials compressed                         ("H.")
      - first initial only                              ("H.")  [deduped]
    """
    parts = full_first.split()
    variants: list[str] = []
    # Full given name
    variants.append(full_first)
    # First word
    if parts:
        variants.append(parts[0])
    # All initials: "H. M."
    initials = " ".join(p[0] + "." for p in parts if p)
    variants.append(initials)
    # First initial only: "H."
    if parts:
        variants.append(parts[0][0] + ".")
    # Deduplicate while preserving order
    seen: set[str] = set()
    result: list[str] = []
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            result.append(v)
    return result


# ── BibTeX helpers ────────────────────────────────────────────────────────────

def _parse_inspirehep_ids(bib_text: str) -> list[int]:
    """Return all inspirehep_id values found in the bib file, in order."""
    return [int(m.group(1)) for m in re.finditer(r'inspirehep_id\s*=\s*\{(\d+)\}', bib_text)]


# ── InspireHEP API helpers ────────────────────────────────────────────────────

def _author_record_id(ref_url: str) -> str | None:
    """Extract the numeric author record ID from a $ref URL."""
    m = re.search(r'/api/authors/(\d+)$', ref_url)
    return m.group(1) if m else None


def _fetch_paper_authors(lit_id: int) -> list[dict]:
    """Return the authors list for an InspireHEP literature record."""
    params = urlencode({"fields": "authors"})
    data = _fetch_json(f"https://inspirehep.net/api/literature/{lit_id}?{params}")
    return data.get("metadata", {}).get("authors", [])


def _fetch_author_profile(author_id: str) -> dict:
    """Return full author profile metadata from InspireHEP."""
    data = _fetch_json(f"https://inspirehep.net/api/authors/{author_id}")
    return data.get("metadata", {})


def _resolve_url(profile: dict, author_id: str) -> str:
    """
    Choose the best URL for a co-author profile, in priority order:
      1. URL tagged as a personal homepage / blog on InspireHEP
      2. First URL listed on the profile
      3. ORCID public profile
      4. InspireHEP author page as fallback
    """
    urls: list[dict] = profile.get("urls", [])
    # Priority 1: labelled homepage
    homepage_labels = {"PERSONAL_WEBSITE", "BLOG", "TWITTER", "LINKEDIN"}
    for entry in urls:
        desc = entry.get("description", "").upper()
        if any(label in desc for label in ("PERSONAL", "HOMEPAGE", "BLOG")):
            return entry["value"]
    # Priority 2: first URL
    if urls:
        return urls[0]["value"]
    # Priority 3: ORCID
    ids = profile.get("ids", [])
    for id_entry in ids:
        if id_entry.get("schema") == "ORCID":
            return f"https://orcid.org/{id_entry['value']}"
    # Priority 4: InspireHEP fallback
    return f"https://inspirehep.net/authors/{author_id}"


# ── YAML serialiser (no PyYAML dependency) ────────────────────────────────────

def _yaml_string(s: str) -> str:
    """Quote a string only if it contains YAML-unsafe characters."""
    if any(c in s for c in (':', '#', '[', ']', '{', '}', ',', '&', '*', '?',
                             '|', '-', '<', '>', '=', '!', '%', '@', '`', '"',
                             "'")):
        escaped = s.replace('"', '\\"')
        return f'"{escaped}"'
    return s


def _build_yaml(coauthors: dict[str, list[dict]]) -> str:
    lines: list[str] = [
        "# Co-author URL map — used by _layouts/bib.liquid to make author names clickable.",
        "# Generated by scripts/sync_coauthors.py — edit manually to override.",
        "# Key = last name (NFD-stripped, lowercased). firstname list = forms bib.liquid",
        "# may see as author.first (full given name, first word, initials).",
        "",
    ]
    for key in sorted(coauthors):
        lines.append(f'"{key}":')
        for entry in coauthors[key]:
            firstnames = entry["firstname"]
            url = entry["url"]
            fn_items = ", ".join(f'"{fn}"' for fn in firstnames)
            lines.append(f"  - firstname: [{fn_items}]")
            lines.append(f"    url: {_yaml_string(url)}")
            lines.append("")
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Populate _data/coauthors.yml from InspireHEP paper author lists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--bib-file", default=DEFAULT_BIB_FILE,
                    help=f"BibTeX file to read inspirehep_ids from (default: {DEFAULT_BIB_FILE})")
    ap.add_argument("--output", default=DEFAULT_OUTPUT,
                    help=f"Output YAML file (default: {DEFAULT_OUTPUT})")
    ap.add_argument("--max-authors", type=int, default=DEFAULT_MAX_AUTHORS,
                    help=f"Skip papers with more than N authors (default: {DEFAULT_MAX_AUTHORS})")
    ap.add_argument("--self-id", default=DEFAULT_SELF_ID,
                    help=f"Your InspireHEP author ID to exclude (default: {DEFAULT_SELF_ID})")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the YAML that would be written without modifying any file")
    args = ap.parse_args()

    bib_path = Path(args.bib_file)
    if not bib_path.exists():
        sys.exit(f"Error: {bib_path} not found")

    bib_text = bib_path.read_text()
    lit_ids = _parse_inspirehep_ids(bib_text)
    if not lit_ids:
        sys.exit("No inspirehep_id entries found in the bib file.")
    print(f"Found {len(lit_ids)} literature IDs in {bib_path}")

    # author_id → {last, first_variants, url}
    coauthor_data: dict[str, dict] = {}
    skipped_large = 0

    for lit_id in lit_ids:
        print(f"  Fetching authors for InspireHEP {lit_id}...")
        try:
            authors = _fetch_paper_authors(lit_id)
        except Exception as exc:
            print(f"    Warning: skipped {lit_id}: {exc}")
            time.sleep(API_DELAY)
            continue

        if len(authors) > args.max_authors:
            print(f"    Skipping — {len(authors)} authors > --max-authors {args.max_authors}")
            skipped_large += 1
            time.sleep(API_DELAY)
            continue

        for author in authors:
            ref_url = author.get("record", {}).get("$ref", "")
            aid = _author_record_id(ref_url)
            if not aid or aid == args.self_id:
                continue
            if aid in coauthor_data:
                continue  # already resolved

            last = author.get("last_name", "").strip()
            first = author.get("first_name", "").strip()
            if not last:
                continue

            # Resolve full profile (for URL)
            try:
                profile = _fetch_author_profile(aid)
                url = _resolve_url(profile, aid)
            except Exception as exc:
                print(f"    Warning: could not fetch profile for {first} {last} ({aid}): {exc}")
                url = f"https://inspirehep.net/authors/{aid}"

            coauthor_data[aid] = {
                "last": last,
                "first_variants": _first_name_variants(first),
                "url": url,
            }
            time.sleep(API_DELAY)

        time.sleep(API_DELAY)

    print(f"\nResolved {len(coauthor_data)} co-authors "
          f"({skipped_large} large-collaboration paper(s) skipped)")

    # Build the coauthors dict keyed by normalised last name
    coauthors: dict[str, list[dict]] = {}
    for info in coauthor_data.values():
        key = _normalise_key(info["last"])
        entry = {"firstname": info["first_variants"], "url": info["url"]}
        coauthors.setdefault(key, []).append(entry)

    yaml_text = _build_yaml(coauthors)

    if args.dry_run:
        print("\n─── DRY RUN — would write this to", args.output, "───\n")
        print(yaml_text)
        return

    out_path = Path(args.output)
    out_path.write_text(yaml_text)
    print(f"Wrote {len(coauthors)} last-name entries to {out_path}")
    print("Review the file and commit it when satisfied.")


if __name__ == "__main__":
    main()
