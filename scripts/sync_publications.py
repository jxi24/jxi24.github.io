#!/usr/bin/env python3
"""
Sync publications from InspireHEP and ORCID into _bibliography/papers.bib.

Fetches all papers attributed to the configured author on InspireHEP and ORCID,
compares against existing entries (matched by inspirehep_id), and prepends any
missing papers with default al-folio custom fields.

Usage:
    python3 scripts/sync_publications.py [--dry-run]
    python3 scripts/sync_publications.py --bib-file _bibliography/papers.bib
    python3 scripts/sync_publications.py --inspirehep-id 1410753 --orcid 0000-0001-6164-1707
    python3 scripts/sync_publications.py --default-preview arxiv_default.png

After running:
  - Review new entries at the top of papers.bib
  - Add `selected = {true}` to papers you want on the about page
  - Replace `preview = {default.png}` with a real thumbnail in
    assets/img/publication_preview/
  - Add `abbr = {JournalName}` if the journal wasn't auto-detected
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode

# ── Defaults (read from _config.yml at runtime if not overridden) ─────────────
DEFAULT_INSPIREHEP_AUTHOR_ID = "1410753"
DEFAULT_ORCID = "0000-0001-6164-1707"
DEFAULT_BIB_FILE = "_bibliography/papers.bib"
DEFAULT_PREVIEW = "default.png"
API_DELAY = 0.5  # polite pause between requests (seconds)

# ── Journal abbreviation map ──────────────────────────────────────────────────
# Maps the journal string that InspireHEP puts in BibTeX to the abbr badge
# shown on the publications page.  Extend as needed.
JOURNAL_ABBR: dict[str, str] = {
    "Phys. Rev. D": "Phys.Rev.D",
    "Phys.Rev.D": "Phys.Rev.D",
    "Phys. Rev. C": "Phys.Rev.C",
    "Phys.Rev.C": "Phys.Rev.C",
    "Phys. Rev. Lett.": "PRL",
    "Phys.Rev.Lett.": "PRL",
    "JHEP": "JHEP",
    "J. High Energy Phys.": "JHEP",
    "SciPost Phys.": "SciPost Phys.",
    "SciPost Phys": "SciPost Phys.",
    "Eur. Phys. J. C": "Eur.Phys.J.C",
    "Eur.Phys.J.C": "Eur.Phys.J.C",
    "PoS": "PoS",
    "J. Phys. G": "J.Phys.G",
    "J.Phys.G": "J.Phys.G",
    "J. Phys. Conf. Ser.": "J.Phys.Conf.Ser.",
    "Phys. Lett. B": "Phys.Lett.B",
    "Phys.Lett.B": "Phys.Lett.B",
    "Nucl. Phys. B": "Nucl.Phys.B",
    "Nucl.Phys.B": "Nucl.Phys.B",
    "Comput. Phys. Commun.": "Comput.Phys.Commun.",
    "Comput.Phys.Commun.": "Comput.Phys.Commun.",
    "Ann. Rev. Nucl. Part. Sci.": "Ann.Rev.Nucl.Part.Sci.",
}


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _fetch(url: str, accept: str = "application/json", retries: int = 3) -> bytes:
    req = Request(url)
    req.add_header("Accept", accept)
    req.add_header("User-Agent", "sync_publications/1.0 (academic portfolio; python-urllib)")
    for attempt in range(retries):
        try:
            with urlopen(req, timeout=30) as resp:
                return resp.read()
        except (URLError, HTTPError) as exc:
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"    Retry {attempt + 1} after {wait}s ({exc})")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def fetch_json(url: str) -> dict:
    return json.loads(_fetch(url, accept="application/json"))


def fetch_bibtex(inspire_id: int) -> str:
    url = f"https://inspirehep.net/api/literature/{inspire_id}?format=bibtex"
    return _fetch(url, accept="application/x-bibtex").decode()


# ── BibTeX parsing helpers ────────────────────────────────────────────────────

def existing_inspirehep_ids(bib_text: str) -> set[int]:
    """Return the set of inspirehep_ids already present in the bib file."""
    return {int(m.group(1)) for m in re.finditer(r'inspirehep_id\s*=\s*\{(\d+)\}', bib_text)}


def journal_abbr_from_bibtex(bib_entry: str) -> str | None:
    """Extract journal name from a BibTeX entry and look up its abbreviation."""
    m = re.search(r'journal\s*=\s*["{]([^"}]+)["}]', bib_entry)
    if not m:
        return None
    return JOURNAL_ABBR.get(m.group(1).strip())


def normalize_fields(bib_entry: str) -> str:
    """Rename InspireHEP's standard field names to al-folio conventions."""
    # InspireHEP exports `eprint = {2502.08727}` but al-folio uses `arxiv`
    bib_entry = re.sub(r'\beprint\b', 'arxiv', bib_entry)
    return bib_entry


def inject_custom_fields(bib_entry: str, inspire_id: int, default_preview: str) -> str:
    """
    Append al-folio custom fields to a BibTeX entry (before the closing brace).
    Field order matches the convention used throughout papers.bib.
    """
    bib_entry = bib_entry.rstrip()
    if bib_entry.endswith("}"):
        body = bib_entry[:-1].rstrip().rstrip(",")
    else:
        body = bib_entry.rstrip(",")

    fields: list[str] = []
    abbr = journal_abbr_from_bibtex(bib_entry)
    if abbr:
        fields.append(f"    abbr = {{{abbr}}}")
    fields.append("    bibtex_show = {true}")
    fields.append(f"    inspirehep_id = {{{inspire_id}}}")
    fields.append(f"    preview = {{{default_preview}}}")

    return body + ",\n" + ",\n".join(fields) + "\n}"


# ── InspireHEP fetching ───────────────────────────────────────────────────────

def fetch_inspirehep_ids(author_id: str) -> set[int]:
    """
    Return InspireHEP literature record IDs for the given author control number.

    Searches for 'Isaacson, Joshua' then filters to records where at least one
    author has the matching InspireHEP author record link.
    """
    author_ref_suffix = f"/api/authors/{author_id}"
    found: set[int] = set()
    page, page_size = 1, 100

    while True:
        params = urlencode({
            "q": "a Isaacson, Joshua",
            "sort": "mostrecent",
            "size": page_size,
            "page": page,
            "fields": "authors",
        })
        data = fetch_json(f"https://inspirehep.net/api/literature?{params}")
        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break

        for hit in hits:
            authors = hit.get("metadata", {}).get("authors", [])
            if any(a.get("record", {}).get("$ref", "").endswith(author_ref_suffix)
                   for a in authors):
                found.add(int(hit["id"]))

        total = data["hits"].get("total", 0)
        if page * page_size >= total:
            break
        page += 1
        time.sleep(API_DELAY)

    return found


# ── ORCID fetching ────────────────────────────────────────────────────────────

def fetch_orcid_inspire_ids(orcid: str) -> set[int]:
    """
    Collect InspireHEP record IDs for all works listed on an ORCID profile.
    Uses DOI-based cross-referencing via the InspireHEP search API.
    """
    data = fetch_json(f"https://pub.orcid.org/v3.0/{orcid}/works")

    dois: list[str] = []
    for group in data.get("group", []):
        for summary in group.get("work-summary", []):
            for ext in summary.get("external-ids", {}).get("external-id", []):
                if ext.get("external-id-type") == "doi":
                    doi = ext.get("external-id-value", "").strip()
                    if doi:
                        dois.append(doi)
                    break  # one per group is enough

    ids: set[int] = set()
    for doi in dois:
        params = urlencode({"q": f"doi {doi}", "fields": "ids", "size": 1})
        try:
            result = fetch_json(f"https://inspirehep.net/api/literature?{params}")
            hits = result.get("hits", {}).get("hits", [])
            if hits:
                ids.add(int(hits[0]["id"]))
        except Exception as exc:
            print(f"    Could not resolve DOI {doi}: {exc}")
        time.sleep(API_DELAY)

    return ids


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Add missing papers from InspireHEP/ORCID to papers.bib",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be added without modifying the file")
    ap.add_argument("--bib-file", default=DEFAULT_BIB_FILE,
                    help=f"Path to BibTeX file (default: {DEFAULT_BIB_FILE})")
    ap.add_argument("--inspirehep-id", default=DEFAULT_INSPIREHEP_AUTHOR_ID,
                    help=f"InspireHEP author ID (default: {DEFAULT_INSPIREHEP_AUTHOR_ID})")
    ap.add_argument("--orcid", default=DEFAULT_ORCID,
                    help=f"ORCID iD (default: {DEFAULT_ORCID})")
    ap.add_argument("--default-preview", default=DEFAULT_PREVIEW,
                    help=f"Fallback preview image filename (default: {DEFAULT_PREVIEW})")
    args = ap.parse_args()

    bib_path = Path(args.bib_file)
    if not bib_path.exists():
        sys.exit(f"Error: {bib_path} not found")

    bib_text = bib_path.read_text()
    already_have = existing_inspirehep_ids(bib_text)
    print(f"Existing entries: {len(already_have)} InspireHEP IDs in {bib_path}")

    # ── Gather all IDs from both sources ──────────────────────────────────────
    print(f"\nQuerying InspireHEP (author ID {args.inspirehep_id})...")
    try:
        inspire_ids = fetch_inspirehep_ids(args.inspirehep_id)
        print(f"  {len(inspire_ids)} papers found")
    except Exception as exc:
        print(f"  Failed: {exc}")
        inspire_ids = set()

    print(f"Querying ORCID ({args.orcid})...")
    try:
        orcid_ids = fetch_orcid_inspire_ids(args.orcid)
        print(f"  {len(orcid_ids)} InspireHEP records resolved from ORCID")
    except Exception as exc:
        print(f"  Failed: {exc}")
        orcid_ids = set()

    all_ids = inspire_ids | orcid_ids
    missing = sorted(all_ids - already_have, reverse=True)  # newest-first by recid
    print(f"\n{len(missing)} new paper(s) to add")

    if not missing:
        print("Bibliography is up to date.")
        return

    # ── Fetch BibTeX for each missing paper ───────────────────────────────────
    new_entries: list[str] = []
    for rid in missing:
        print(f"  Fetching BibTeX for InspireHEP ID {rid}...")
        try:
            bib = fetch_bibtex(rid)
            bib = normalize_fields(bib)
            bib = inject_custom_fields(bib, rid, args.default_preview)
            new_entries.append(bib)
        except Exception as exc:
            print(f"    Warning: skipped {rid}: {exc}")
        time.sleep(API_DELAY)

    if not new_entries:
        print("No entries could be retrieved.")
        return

    if args.dry_run:
        print("\n─── DRY RUN — would prepend these entries ───\n")
        print("\n\n".join(new_entries))
        return

    # ── Insert after Jekyll front matter ──────────────────────────────────────
    front_matter = re.match(r"(^---\n.*?---\n)", bib_text, re.DOTALL)
    if front_matter:
        cut = front_matter.end()
        new_text = (
            bib_text[:cut]
            + "\n"
            + "\n\n".join(new_entries)
            + "\n\n"
            + bib_text[cut:].lstrip("\n")
        )
    else:
        new_text = "\n\n".join(new_entries) + "\n\n" + bib_text

    bib_path.write_text(new_text)
    print(f"\nDone — added {len(new_entries)} paper(s) to {bib_path}")
    print("\nNext steps:")
    print("  1. Add `selected = {true}` to papers to feature on the about page")
    print(f"  2. Replace `preview = {{{args.default_preview}}}` with a real thumbnail")
    print("     in assets/img/publication_preview/")
    print("  3. Add `abbr = {Journal}` for any entry where it wasn't auto-detected")
    print("  4. Run `bundle exec jekyll serve` to preview")

    preview_dest = bib_path.parent.parent / "assets" / "img" / "publication_preview" / args.default_preview
    if not preview_dest.exists():
        print(f"\n  Note: {preview_dest} does not exist.")
        print("  Create a fallback thumbnail there so new entries render correctly.")


if __name__ == "__main__":
    main()
