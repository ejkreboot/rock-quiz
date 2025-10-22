#!/usr/bin/env python3
"""
google_image_sampler.py

Search Google Custom Search (Images) for "<query> sample" and download the first
5 valid images, preferring Wikimedia/Wikipedia, .edu, and .gov sources.
Creates an output directory based on the query.

Usage:
  python google_image_sampler.py "Andesite"
  python google_image_sampler.py "Augite" --max 5 --out ./downloads

Requires:
  pip install requests python-dotenv

Env:
  GOOGLE_API_KEY=...
  GOOGLE_CSE_CX=...
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse, unquote

import requests
from dotenv import load_dotenv

API_URL = "https://www.googleapis.com/customsearch/v1"

PREFERRED_DOMAINS = (
    "commons.wikimedia.org",
    "upload.wikimedia.org",
    "wikimedia.org",
    "wikipedia.org",
)

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# ---------- Helpers ----------

def domain_score(url: str, display_link: Optional[str]) -> int:
    """
    Score a result by domain preference.
    Wikimedia/Wikipedia > .edu > .gov > .org (light bump).
    """
    host = (display_link or urlparse(url).netloc or "").lower()

    # Strong preference: Wikimedia/Wikipedia
    if any(h in host for h in PREFERRED_DOMAINS):
        return 100

    # TLD preferences
    if host.endswith(".edu"):
        return 80
    if host.endswith(".gov"):
        return 70

    # Small nudge for .org
    if host.endswith(".org"):
        return 10

    return 0


def size_score(item: dict) -> int:
    """
    Prefer larger images if info available.
    """
    img = item.get("image") or {}
    width = int(img.get("width") or 0)
    height = int(img.get("height") or 0)
    byte_size = int(img.get("byteSize") or 0)
    # weight pixel count more than byte size
    return min(50, (width * height) // (800 * 600)) + min(20, byte_size // (200_000))


def ext_from_content_type(content_type: str) -> str:
    ct = content_type.lower().split(";")[0].strip()
    return {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/bmp": ".bmp",
        "image/tiff": ".tif",
        "image/x-icon": ".ico",
        "image/heic": ".heic",
        "image/heif": ".heif",
        "image/svg+xml": ".svg",
    }.get(ct, "")


def guess_ext_from_url(url: str) -> str:
    path = urlparse(url).path
    base = Path(unquote(path)).name.lower()
    m = re.search(r"\.(jpeg|jpg|png|gif|webp|bmp|tif|tiff|ico|heic|heif|svg)$", base)
    return f".{m.group(1)}" if m else ""


def sanitize_dirname(s: str) -> str:
    s = s.strip().replace(os.sep, "_")
    return re.sub(r"[^a-zA-Z0-9._\- ]+", "_", s)


def filehash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- Google CSE ----------

def cse_search(
    api_key: str,
    cx: str,
    query: str,
    start: int = 1,
    num: int = 10,
    safe: str = "active",
) -> dict:
    resp = requests.get(
        API_URL,
        params={
            "q": query,
            "cx": cx,
            "key": api_key,
            "searchType": "image",
            "num": num,
            "start": start,
            "safe": safe,
        },
        timeout=20,
        headers={"User-Agent": USER_AGENT},
    )
    resp.raise_for_status()
    return resp.json()


def sorted_items(items: List[dict]) -> List[dict]:
    # Sort by (domain preference + size), keeping original order as tiebreaker
    scored = []
    for idx, it in enumerate(items):
        link = it.get("link", "")
        display_link = it.get("displayLink")
        score = domain_score(link, display_link) + size_score(it)
        scored.append((score, idx, it))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [it for _, __, it in scored]


# ---------- Download ----------

def download_image(url: str, out_dir: Path, name_prefix: str, idx: int) -> Optional[Path]:
    headers = {"User-Agent": USER_AGENT, "Accept": "image/*,*/*;q=0.8"}
    try:
        r = requests.get(url, timeout=30, headers=headers, stream=True)
    except Exception as e:
        print(f"  ✗ GET failed: {e} -> {url}")
        return None

    if r.status_code != 200:
        print(f"  ✗ HTTP {r.status_code} -> {url}")
        return None

    ct = r.headers.get("Content-Type", "")
    ext = ext_from_content_type(ct) or guess_ext_from_url(url) or ".jpg"
    fname = f"{name_prefix}_{idx:02d}{ext}"
    fpath = out_dir / fname

    try:
        with fpath.open("wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"  ✗ Write failed: {e} -> {fpath}")
        return None

    # Basic sanity check on bytes
    if fpath.stat().st_size < 1024:  # < 1KB typically junk
        print(f"  ✗ Too small, deleting: {fpath}")
        try:
            fpath.unlink()
        except Exception:
            pass
        return None

    print(f"  ✓ Saved: {fpath}")
    return fpath


# ---------- Main workflow ----------

def run(query_term: str, max_downloads: int, out_root: Path) -> int:
    load_dotenv()  # read .env in CWD

    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_CX")
    if not api_key or not cx:
        print("ERROR: Missing GOOGLE_API_KEY and/or GOOGLE_CSE_CX (check your .env).", file=sys.stderr)
        return 2

    search_query = f"{query_term} sample"
    out_dir = out_root / sanitize_dirname(query_term)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Searching for: {search_query}")
    print(f"Output dir    : {out_dir.resolve()}")

    downloaded = 0
    start = 1  # Google CSE 'start' is 1-based
    seen_links: set[str] = set()

    # Google allows start up to 91 (with num up to 10) → ~100 results
    while downloaded < max_downloads and start <= 91:
        try:
            data = cse_search(api_key, cx, search_query, start=start, num=10, safe="active")
        except requests.HTTPError as e:
            print(f"HTTP error from CSE: {e}", file=sys.stderr)
            break
        except Exception as e:
            print(f"Search error: {e}", file=sys.stderr)
            break

        items = data.get("items") or []
        if not items:
            print("No more results.")
            break

        for item in sorted_items(items):
            if downloaded >= max_downloads:
                break
            url = item.get("link")
            if not url or url in seen_links:
                continue
            seen_links.add(url)

            # Construct a friendly prefix with domain for traceability
            host = (item.get("displayLink") or urlparse(url).netloc or "image").lower()
            host_clean = re.sub(r"[^a-z0-9\-._]", "_", host)
            prefix = f"{host_clean}"

            print(f"→ Trying: {url}")
            saved = download_image(url, out_dir, prefix, downloaded + 1)
            if saved:
                downloaded += 1
            else:
                # keep going—"go deeper if there is a download error"
                pass

            # polite pacing to avoid hammering sources
            time.sleep(0.3)

        # Next page
        start += 10
        # tiny delay to be polite to CSE
        time.sleep(0.4)

    print(f"\nDone. Downloaded {downloaded} image(s).")
    return 0 if downloaded > 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Download first 5 preferred images for '<term> sample' via Google CSE.")
    parser.add_argument("term", help="Rock or mineral name (e.g., 'Andesite')")
    parser.add_argument("--max", type=int, default=5, help="How many images to download (default: 5)")
    parser.add_argument("--out", type=Path, default=Path("./images"), help="Root output directory (default: ./images)")
    args = parser.parse_args()

    sys.exit(run(args.term, args.max, args.out))


if __name__ == "__main__":
    main()
