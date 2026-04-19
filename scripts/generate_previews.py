#!/usr/bin/env python3
"""
Generate preview thumbnails for papers.bib entries by rendering the top of
each paper's first arXiv PDF page (title + authors + abstract).

Requires:
    pip install pymupdf

Usage:
    # Generate all missing previews
    python3 scripts/generate_previews.py

    # Also update preview= fields in papers.bib to point at generated files
    python3 scripts/generate_previews.py --update-bib

    # Preview what would run, without downloading anything
    python3 scripts/generate_previews.py --dry-run

    # Regenerate a single entry (e.g. after tweaking --crop)
    python3 scripts/generate_previews.py --key Isaacson:2025lyx --force

    # Wider crop to include more of the paper body
    python3 scripts/generate_previews.py --crop 0.65
"""

import argparse
import re
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

BIB_FILE = "_bibliography/papers.bib"
PREVIEW_DIR = "assets/img/publication_preview"
ARXIV_DELAY = 3.0   # arXiv ToS: no more than ~1 req/3s for bulk access
DEFAULT_CROP = 0.55  # top fraction of page 1 (covers title+authors+abstract)
DEFAULT_DPI = 200    # render resolution — 150 is faster, 300 is sharper


# ── BibTeX parsing ────────────────────────────────────────────────────────────

def parse_entries(bib_text: str) -> list[dict]:
    """
    Return one dict per entry with keys: key, arxiv, preview, start, end.
    start/end are character offsets into bib_text for in-place edits.
    """
    entries = []
    for m in re.finditer(r'(@\w+\{(\w+:\w+),(.*?)\n\})', bib_text, re.DOTALL):
        body = m.group(3)
        arxiv_m = re.search(r'\barxiv\s*=\s*["{]([^"}\s]+)["}]', body, re.I)
        preview_m = re.search(r'\bpreview\s*=\s*[\{"]+([^}"\n]+)[\}"]', body)
        entries.append({
            'key':     m.group(2),
            'arxiv':   arxiv_m.group(1).strip() if arxiv_m else None,
            'preview': preview_m.group(1).strip() if preview_m else None,
            'start':   m.start(),
            'end':     m.end(),
        })
    return entries


def canonical_preview(key: str) -> str:
    """The conventional preview filename derived from a BibTeX key."""
    return key.replace(':', '_') + '.png'


# ── Downloading + rendering ───────────────────────────────────────────────────

def download_pdf(arxiv_id: str) -> bytes:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    req = Request(url)
    req.add_header("User-Agent", "generate_previews/1.0 (academic portfolio; python-urllib)")
    with urlopen(req, timeout=60) as resp:
        return resp.read()


def render_top_of_page(pdf_bytes: bytes, output_path: Path,
                        crop: float, dpi: int) -> None:
    """
    Render the top `crop` fraction of the first PDF page and save as PNG.
    Requires PyMuPDF (pip install pymupdf).
    """
    try:
        import fitz
    except ImportError:
        sys.exit("PyMuPDF is not installed.  Run:  pip install pymupdf")

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    r = page.rect
    clip = fitz.Rect(r.x0, r.y0, r.x1, r.y1 * crop)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=clip, colorspace=fitz.csRGB)
    pix.save(str(output_path))
    doc.close()


# ── Bib update ────────────────────────────────────────────────────────────────

def _patch_preview(bib_text: str, key: str, new_name: str) -> str:
    entry_pat = r'(@\w+\{' + re.escape(key) + r',)(.*?)\n\}'
    preview_repl = r'\1{' + new_name + r'}'

    def replacer(m: re.Match) -> str:
        patched_body = re.sub(
            r'(\bpreview\s*=\s*)[\{"][^}"\n]*[\}"]',
            preview_repl,
            m.group(2),
        )
        return m.group(1) + patched_body + '\n}'

    return re.sub(entry_pat, replacer, bib_text, flags=re.DOTALL)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Render arXiv PDF first pages as publication preview images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--bib-file",     default=BIB_FILE)
    ap.add_argument("--preview-dir",  default=PREVIEW_DIR)
    ap.add_argument("--key",          metavar="BIBTEX_KEY",
                    help="Process only this entry")
    ap.add_argument("--force",        action="store_true",
                    help="Overwrite images that already exist")
    ap.add_argument("--dry-run",      action="store_true",
                    help="Show plan without downloading or writing")
    ap.add_argument("--update-bib",   action="store_true",
                    help="Rewrite preview= fields in papers.bib to match generated filenames")
    ap.add_argument("--crop",         type=float, default=DEFAULT_CROP,
                    help=f"Fraction of page height to capture (default: {DEFAULT_CROP})")
    ap.add_argument("--dpi",          type=int,   default=DEFAULT_DPI,
                    help=f"Render resolution in DPI (default: {DEFAULT_DPI})")
    args = ap.parse_args()

    bib_path     = Path(args.bib_file)
    preview_dir  = Path(args.preview_dir)

    if not bib_path.exists():
        sys.exit(f"Error: {bib_path} not found")

    bib_text = bib_path.read_text()
    entries  = parse_entries(bib_text)

    # Filter to entries that have an arXiv ID
    candidates = [e for e in entries if e['arxiv']]
    if args.key:
        candidates = [e for e in candidates if e['key'] == args.key]
        if not candidates:
            sys.exit(f"No entry '{args.key}' found with an arxiv field")

    print(f"{len(candidates)} entries with arXiv IDs in {bib_path}")

    if not args.dry_run:
        preview_dir.mkdir(parents=True, exist_ok=True)

    generated: list[str] = []
    skipped:   list[str] = []
    failed:    list[str] = []
    bib_patches: dict[str, str] = {}   # key → new filename

    for i, entry in enumerate(candidates):
        key      = entry['key']
        arxiv_id = entry['arxiv']
        out_name = canonical_preview(key)
        out_path = preview_dir / out_name

        if out_path.exists() and not args.force:
            skipped.append(key)
            if args.update_bib and entry['preview'] != out_name:
                bib_patches[key] = out_name
            continue

        if args.dry_run:
            status = "exists — would skip" if out_path.exists() else "would generate"
            print(f"  {key:35s}  arxiv:{arxiv_id}  → {out_name}  ({status})")
            generated.append(key)
            continue

        print(f"  [{i + 1}/{len(candidates)}] {key}  arxiv:{arxiv_id}", end="", flush=True)
        try:
            pdf_bytes = download_pdf(arxiv_id)
            render_top_of_page(pdf_bytes, out_path, crop=args.crop, dpi=args.dpi)
            size_kb = out_path.stat().st_size // 1024
            print(f"  →  {out_name} ({size_kb} KB)")
            generated.append(key)
            if args.update_bib:
                bib_patches[key] = out_name
        except (URLError, HTTPError) as exc:
            print(f"  FAILED (download): {exc}")
            failed.append(key)
        except Exception as exc:
            print(f"  FAILED: {exc}")
            failed.append(key)

        if i < len(candidates) - 1:
            time.sleep(ARXIV_DELAY)

    # ── Patch preview= fields in the bib ─────────────────────────────────────
    if bib_patches and not args.dry_run:
        updated = bib_text
        for key, new_name in bib_patches.items():
            updated = _patch_preview(updated, key, new_name)
        bib_path.write_text(updated)
        print(f"\nUpdated {len(bib_patches)} preview= field(s) in {bib_path}")

    print(f"\nGenerated : {len(generated)}")
    print(f"Skipped   : {len(skipped)}  (already exist; --force to regenerate)")
    if failed:
        print(f"Failed    : {len(failed)}  —  {', '.join(failed)}")


if __name__ == "__main__":
    main()
