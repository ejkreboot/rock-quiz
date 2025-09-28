#!/usr/bin/env python3
"""
Download the first N Google Custom Search JSON (Images) results for each rock type,
convert them to PNG, save as <rocktype>_NNN.png, and record credits (URL -> filename).

New in this version
-------------------
- `--rights` to pass Google CSE usage-rights filters (e.g., cc_publicdomain, cc_attribute).
- `--public_domain` convenience flag (equivalent to --rights cc_publicdomain).
- `--domains` to bias search to certain TLDs (e.g., ".edu,.gov") using `site:` operators in the query.
- `--sites` to bias/limit search to specific hosts (e.g., "usgs.gov,si.edu").

Notes
-----
- Google CSE supports the `rights` parameter for image usage rights. Accepted tokens include:
  cc_publicdomain, cc_attribute, cc_sharealike, cc_noncommercial, cc_nonderived
  You can combine them by comma (internally joined by `|` for the API).
- Domain/Site filters are appended to the query string using `site:` operators.
  Example: (site:.edu OR site:.gov) or (site:usgs.gov OR site:si.edu)

"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse, unquote

import requests
from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError

# ---------- Configuration ----------

ROCK_TYPES = [
    "Andesite","Basalt","Chert","Coal","Conglomerate","Gabbro","Gneiss","Granite",
    "Hornfels","Limestone","Marble","Migmatite","Mudstone","Phyllite","Quartzite",
    "Rhyolite","Sandstone","Shale","Siltstone","Slate","Travertine","Tuff"
]

GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
DEFAULT_LIMIT = 10
REQUEST_TIMEOUT = 20  # seconds
PAUSE_BETWEEN_API_CALLS = 0.6  # seconds; adjust if you hit rate limits
PAUSE_BETWEEN_DOWNLOADS = 0.2   # seconds

SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")

RIGHTS_CHOICES = {
    "cc_publicdomain",
    "cc_attribute",
    "cc_sharealike",
    "cc_noncommercial",
    "cc_nonderived",
}

# ---------- Helpers ----------

def safe_name(s: str) -> str:
    """Sanitize a piece of a filename/path."""
    s = s.strip().replace(" ", "_")
    return SAFE_NAME_RE.sub("", s)

def fetch_json(url: str, params: Dict[str, str]) -> Dict:
    """GET JSON with basic error handling."""
    r = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()

def build_filename(rock: str, index: int) -> str:
    """Return canonical filename for a rock image (PNG)."""
    return f"{safe_name(rock)}_{index:03d}.png"

def download_bytes(url: str) -> Optional[bytes]:
    try:
        with requests.get(url, timeout=REQUEST_TIMEOUT, stream=True, headers={"User-Agent": "Mozilla/5.0 (compatible; rock-scraper/1.2)"}) as r:
            r.raise_for_status()
            return r.content
    except Exception as e:
        print(f"  ! Failed to fetch {url}: {e}")
        return None

def image_bytes_to_png(image_bytes: bytes) -> Optional[bytes]:
    """Convert arbitrary image bytes to PNG bytes using Pillow. Returns None on failure."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as im:
            # Handle animated formats: take first frame
            if getattr(im, "is_animated", False):
                im.seek(0)
            # Convert mode if needed (keep alpha if present)
            if im.mode in ("RGBA", "LA"):
                converted = im
            elif im.mode == "P":
                converted = im.convert("RGBA")
            else:
                converted = im.convert("RGB")
            out = io.BytesIO()
            converted.save(out, format="PNG", optimize=True)
            return out.getvalue()
    except UnidentifiedImageError:
        print("    ! Not an image Pillow can read.")
        return None
    except Exception as e:
        print(f"    ! Pillow conversion error: {e}")
        return None

def build_domain_clause(domains: List[str]) -> str:
    """
    Build a query clause like: (site:.edu OR site:.gov)
    Accepts items like ".edu", ".gov", "edu" and normalizes to ".tld".
    """
    cleaned = []
    for d in domains:
        d = d.strip()
        if not d:
            continue
        if d.startswith("."):
            cleaned.append(f"site:{d}")
        elif "." not in d:
            cleaned.append(f"site:.{d}")
        else:
            # looks like a host (example.gov) — treat as site filter
            cleaned.append(f"site:{d}")
    if not cleaned:
        return ""
    return "(" + " OR ".join(cleaned) + ")"

def build_site_clause(sites: List[str]) -> str:
    """
    Build a query clause like: (site:usgs.gov OR site:si.edu)
    """
    cleaned = []
    for s in sites:
        s = s.strip()
        if not s:
            continue
        if not s.startswith("site:"):
            cleaned.append(f"site:{s}")
        else:
            cleaned.append(s)
    if not cleaned:
        return ""
    return "(" + " OR ".join(cleaned) + ")"

# ---------- Core ----------

def search_images(api_key: str, cx: str, query: str, limit: int, rights: Optional[str]) -> List[Dict]:
    """
    Use Google CSE to fetch up to `limit` image results for `query`.
    Returns a list of items (dicts) from the API (may be fewer than limit).
    """
    results: List[Dict] = []
    start = 1  # Google CSE is 1-indexed; max 10 per page
    remaining = limit

    while remaining > 0 and start <= 91:  # CSE caps start at 91
        page_size = min(10, remaining)
        params = {
            "key": api_key,
            "cx": cx,
            "q": query,
            "searchType": "image",
            "num": page_size,
            "start": start,
        }
        if rights:
            params["rights"] = rights  # pipe-delimited per API

        try:
            data = fetch_json(GOOGLE_SEARCH_URL, params)
        except requests.HTTPError as e:
            print(f"  ! API error at start={start}: {e}")
            break
        except Exception as e:
            print(f"  ! Network error at start={start}: {e}")
            break

        items = data.get("items", []) or []
        if not items:
            break

        results.extend(items)
        got = len(items)
        remaining -= got
        start += got

        time.sleep(PAUSE_BETWEEN_API_CALLS)

    return results[:limit]

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Download first N Google CSE image results per rock type, convert to PNG, and record credits.")
    parser.add_argument("--limit", "-n", type=int, default=DEFAULT_LIMIT, help="Images per rock type (default: 10)")
    parser.add_argument("--out", "-o", type=str, default="rock_images", help="Output root directory")
    parser.add_argument("--types", "-t", type=str, nargs="*", default=ROCK_TYPES, help="Subset of rock types to fetch")
    parser.add_argument("--query_suffix", type=str, default="rock sample", help='Suffix appended to each rock, e.g. `rock sample`')
    parser.add_argument("--rights", type=str, default=None,
                        help="Comma-separated usage rights for Google CSE (e.g., 'cc_publicdomain,cc_attribute').")
    parser.add_argument("--public_domain", action="store_true",
                        help="Shortcut for --rights cc_publicdomain")
    parser.add_argument("--domains", type=str, default=None,
                        help="Comma-separated list like '.edu,.gov' to add a site: TLD clause to the query.")
    parser.add_argument("--sites", type=str, default=None,
                        help="Comma-separated host list like 'usgs.gov,si.edu' to add site:host clauses to the query.")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_CX")

    if not api_key or not cx:
        raise SystemExit("Missing GOOGLE_API_KEY or GOOGLE_CSE_CX. Create a .env file (see .env.example).")

    rights = None
    if args.public_domain and args.rights:
        print("! Both --public_domain and --rights specified; --rights will take precedence.")
    if args.public_domain and not args.rights:
        rights = "cc_publicdomain"
    if args.rights:
        # Validate and join as pipes per API
        tokens = [t.strip() for t in args.rights.split(",") if t.strip()]
        invalid = [t for t in tokens if t not in RIGHTS_CHOICES]
        if invalid:
            print(f"! Warning: unknown rights tokens: {', '.join(invalid)} (continuing anyway)")
        if tokens:
            rights = "|".join(tokens)

    domain_clause = build_domain_clause([d for d in (args.domains.split(",") if args.domains else [])])
    site_clause = build_site_clause([s for s in (args.sites.split(",") if args.sites else [])])

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    credits_csv_path = out_root / "credits.csv"
    credits_json_path = out_root / "credits.json"

    # Prepare credits collectors
    credits_rows = []  # list of dicts for CSV
    credits_json = []  # list of dicts for JSON

    for rock in args.types:
        rock_dir = out_root / safe_name(rock)
        rock_dir.mkdir(parents=True, exist_ok=True)

        q_parts = [rock, args.query_suffix]
        tail_filters = [c for c in (domain_clause, site_clause) if c]
        if tail_filters:
            q_parts.append(" ".join(tail_filters))
        query = " ".join([p for p in q_parts if p]).strip()

        print(f"\n== {rock} ==\nQuery: {query}")
        if rights:
            print(f"Rights: {rights}")
        items = search_images(api_key, cx, query, args.limit, rights)
        if not items:
            print("  (no results)")
            continue

        saved = 0
        for item in items:
            link = item.get("link") or item.get("image", {}).get("thumbnailLink")
            if not link:
                print("  ! No link for a result, skipping.")
                continue

            # Download and convert to PNG
            print(f"  - Fetching: {link}")
            data = download_bytes(link)
            if not data:
                continue

            png_bytes = image_bytes_to_png(data)
            if not png_bytes:
                continue

            saved += 1
            filename = build_filename(rock, saved)
            dest = rock_dir / filename
            try:
                with open(dest, "wb") as f:
                    f.write(png_bytes)
                print(f"    -> Saved {dest.relative_to(out_root)}")

                # Record credits
                row = {"rock": rock, "file": str(dest.relative_to(out_root)), "url": link}
                credits_rows.append(row)
                credits_json.append(row)

            except Exception as e:
                print(f"    ! Write failed {dest}: {e}")
                saved -= 1  # keep numbering contiguous if write fails

            time.sleep(PAUSE_BETWEEN_DOWNLOADS)

    # Write credits files
    try:
        with open(credits_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["rock","file","url"])
            writer.writeheader()
            writer.writerows(credits_rows)
        print(f"\nCredits CSV: {credits_csv_path}")
    except Exception as e:
        print(f"\n! Failed to write credits CSV: {e}")

    try:
        with open(credits_json_path, "w", encoding="utf-8") as f:
            json.dump(credits_json, f, indent=2)
        print(f"Credits JSON: {credits_json_path}")
    except Exception as e:
        print(f"! Failed to write credits JSON: {e}")

    print("\nDone.")

if __name__ == "__main__":
    main()
