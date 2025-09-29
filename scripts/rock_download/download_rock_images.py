#!/usr/bin/env python3
"""
Download the first N Google Custom Search JSON (Images) results for each rock type,
convert them to PNG, save as <rocktype>_NNN.png, and record credits (URL -> filename).

This version adds:
- GLOBAL RATE LIMITING for API calls and image downloads.
- RETRY with exponential backoff + jitter and support for `Retry-After`.
- `--debug` flag with verbose per-attempt logging so long waits don't look like hangs.
- Tuple timeouts (connect/read) to avoid long stalls.
- Polished prints that flush immediately.

Optional query helpers:
- `--rights` to pass Google CSE usage-rights filters (e.g., cc_publicdomain, cc_attribute).
- `--public_domain` shortcut for `--rights cc_publicdomain`.
- `--domains` to bias search to certain TLDs (e.g., ".edu,.gov").
- `--sites` to bias/limit search to specific hosts (e.g., "usgs.gov,si.edu").
- `--public_sites` to RESTRICT searches to a curated set of public/educational sources
  (currently .edu, .gov, and {usgs.gov, si.edu, naturalhistory.si.edu, nasa.gov, noaa.gov, nps.gov, blm.gov}).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import random
import re
import time
from pathlib import Path
from typing import Dict, List, Optional

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

# --- Throttling / backoff configuration ---
API_MIN_INTERVAL = 0.75   # seconds between CSE API calls
DL_MIN_INTERVAL  = 0.30   # seconds between image downloads
MAX_RETRIES      = 3      # per-request attempts
BASE_BACKOFF     = 0.8    # seconds (exponential base)
JITTER_RANGE     = (0.05, 0.25)

# Per-request timeout (connect, read) so connect stalls don't hang too long
CSE_TIMEOUT      = (6, 15)
DOWNLOAD_TIMEOUT = (8, 30)

SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")

RIGHTS_CHOICES = {
    "cc_publicdomain",
    "cc_attribute",
    "cc_sharealike",
    "cc_noncommercial",
    "cc_nonderived",
}

# Curated public/educational sources for --public_sites
PUBLIC_TLDS  = [".edu", ".gov"]
PUBLIC_SITES = [
    "usgs.gov",
    "si.edu",
    "naturalhistory.si.edu",
    "nasa.gov",
    "noaa.gov",
    "nps.gov",
    "blm.gov",
    "wikipedia.org",
    "wikimedia.org"
]

# ---------- HTTP helpers (session, limiter, retry) ----------

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (compatible; rock-scraper/1.4)"})

class RateLimiter:
    def __init__(self, min_interval: float):
        self.min_interval = float(min_interval)
        self._next = 0.0

    def wait(self):
        now = time.monotonic()
        if now < self._next:
            time.sleep(self._next - now)
        self._next = time.monotonic() + self.min_interval

API_LIMITER = RateLimiter(API_MIN_INTERVAL)
DL_LIMITER  = RateLimiter(DL_MIN_INTERVAL)

TRANSIENT_STATUSES = {429, 500, 502, 503, 504}
DEBUG = False  # set from --debug


def _parse_retry_after(resp: requests.Response) -> Optional[float]:
    ra = resp.headers.get("Retry-After")
    if not ra:
        return None
    try:
        return float(ra)  # seconds form
    except ValueError:
        return 2.0


def get_with_retries(
    url: str,
    *,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    timeout = (8, 20),
    limiter: Optional[RateLimiter] = None,
    label: str = ""
) -> Optional[requests.Response]:
    """Rate-limited GET with retry/backoff. Returns Response or None after retries."""
    for attempt in range(MAX_RETRIES):
        if limiter:
            limiter.wait()

        try:
            if DEBUG:
                print(f"  -> GET {label or url} (attempt {attempt+1}/{MAX_RETRIES})", flush=True)
            resp = SESSION.get(url, params=params, headers=headers, timeout=timeout, stream=False)
        except requests.RequestException as e:
            delay = BASE_BACKOFF * (2 ** attempt) + random.uniform(*JITTER_RANGE)
            if DEBUG:
                print(f"     ! network error {e.__class__.__name__}: {e}; retrying in {delay:.2f}s", flush=True)
            time.sleep(delay)
            continue

        if resp.status_code in TRANSIENT_STATUSES:
            ra = _parse_retry_after(resp)
            delay = (ra if ra is not None else BASE_BACKOFF * (2 ** attempt)) + random.uniform(*JITTER_RANGE)
            if DEBUG:
                why = f"{resp.status_code} (Retry-After {ra}s)" if ra is not None else f"{resp.status_code}"
                print(f"     ! transient {why}; backing off {delay:.2f}s", flush=True)
            time.sleep(delay)
            continue

        try:
            resp.raise_for_status()
            return resp
        except requests.HTTPError as e:
            if DEBUG:
                print(f"     ! HTTP {resp.status_code} non-retryable: {e}", flush=True)
            return None

    if DEBUG:
        print("     ! exhausted retries", flush=True)
    return None

# ---------- Helpers ----------

def safe_name(s: str) -> str:
    s = s.strip().replace(" ", "_")
    return SAFE_NAME_RE.sub("", s)


def fetch_json(url: str, params: Dict[str, str]) -> Dict:
    resp = get_with_retries(url, params=params, timeout=CSE_TIMEOUT, limiter=API_LIMITER, label="CSE JSON")
    if resp is None:
        raise requests.HTTPError("Failed to fetch JSON after retries")
    return resp.json()


def build_filename(rock: str, index: int) -> str:
    return f"{safe_name(rock)}_{index:03d}.png"


def download_bytes(url: str) -> Optional[bytes]:
    resp = get_with_retries(
        url,
        timeout=DOWNLOAD_TIMEOUT,
        headers={"User-Agent": "Mozilla/5.0 (compatible; rock-scraper/1.4)"},
        limiter=DL_LIMITER,
        label="image",
    )
    if resp is None:
        print(f"  ! Failed to fetch {url} after retries", flush=True)
        return None
    return resp.content


def image_bytes_to_png(image_bytes: bytes) -> Optional[bytes]:
    try:
        with Image.open(io.BytesIO(image_bytes)) as im:
            if getattr(im, "is_animated", False):
                im.seek(0)
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
    """Build a query clause like: (site:.edu OR site:.gov). Accepts '.edu', 'edu', or full hosts."""
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
            cleaned.append(f"site:{d}")
    if not cleaned:
        return ""
    return "(" + " OR ".join(cleaned) + ")"


def build_site_clause(sites: List[str]) -> str:
    """Build a query clause like: (site:usgs.gov OR site:si.edu)"""
    cleaned = []
    for s in sites:
        s = s.strip()
        if not s:
            continue
        cleaned.append(f"site:{s}" if not s.startswith("site:") else s)
    if not cleaned:
        return ""
    return "(" + " OR ".join(cleaned) + ")"

# ---------- Core ----------

def search_images(api_key: str, cx: str, query: str, limit: int, rights: Optional[str]) -> List[Dict]:
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
            print(f"  ! API error at start={start}: {e}", flush=True)
            break
        except Exception as e:
            print(f"  ! Network error at start={start}: {e}", flush=True)
            break

        items = data.get("items", []) or []
        if not items:
            break

        results.extend(items)
        got = len(items)
        remaining -= got
        start += got

    return results[:limit]

# ---------- CLI entry ----------

def main():
    global DEBUG
    load_dotenv()

    parser = argparse.ArgumentParser(description="Download first N Google CSE image results per rock type, convert to PNG, and record credits.")
    parser.add_argument("--limit", "-n", type=int, default=DEFAULT_LIMIT, help="Images per rock type (default: 10)")
    parser.add_argument("--out", "-o", type=str, default="rock_images", help="Output root directory")
    parser.add_argument("--types", "-t", type=str, nargs="*", default=ROCK_TYPES, help="Subset of rock types to fetch")
    parser.add_argument("--query_suffix", type=str, default="rock sample", help='Suffix appended to each rock, e.g. `rock sample`')

    # Licensing / filters
    parser.add_argument("--rights", type=str, default=None, help="Comma-separated usage rights for Google CSE (e.g., 'cc_publicdomain,cc_attribute').")
    parser.add_argument("--public_domain", action="store_true", help="Shortcut for --rights cc_publicdomain")

    # Site scoping
    parser.add_argument("--domains", type=str, default=None, help="Comma-separated list like '.edu,.gov' to add a site: TLD clause to the query.")
    parser.add_argument("--sites", type=str, default=None, help="Comma-separated host list like 'usgs.gov,si.edu' to add site:host clauses to the query.")
    parser.add_argument("--public_sites", action="store_true",
                        help="Restrict to curated public/educational domains (.edu,.gov) and sites (usgs.gov, si.edu, naturalhistory.si.edu, nasa.gov, noaa.gov, nps.gov, blm.gov).")

    parser.add_argument("--debug", action="store_true", help="Verbose HTTP/retry logging")
    args = parser.parse_args()

    DEBUG = args.debug

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
        tokens = [t.strip() for t in args.rights.split(",") if t.strip()]
        invalid = [t for t in tokens if t not in RIGHTS_CHOICES]
        if invalid:
            print(f"! Warning: unknown rights tokens: {', '.join(invalid)} (continuing anyway)")
        if tokens:
            rights = "|".join(tokens)

    # Determine domain/site constraints
    if args.public_sites:
        if args.domains:
            print("! --public_sites overrides --domains", flush=True)
        if args.sites:
            print("! --public_sites overrides --sites", flush=True)
        domains_list = list(PUBLIC_TLDS)
        sites_list   = list(PUBLIC_SITES)
    else:
        domains_list = [d for d in (args.domains.split(",") if args.domains else [])]
        sites_list   = [s for s in (args.sites.split(",") if args.sites else [])]

    domain_clause = build_domain_clause(domains_list)
    site_clause   = build_site_clause(sites_list)

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    credits_csv_path = out_root / "credits.csv"
    credits_json_path = out_root / "credits.json"

    credits_rows: List[Dict[str, str]] = []
    credits_json: List[Dict[str, str]] = []

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

            print(f"  - Fetching: {link}")
            data = download_bytes(link)
            if not data:
                continue

            png_bytes = image_bytes_to_png(data)
            if not png_bytes:
                continue

            saved += 1
            filename = f"{safe_name(rock)}_{saved:03d}.png"
            dest = rock_dir / filename
            try:
                with open(dest, "wb") as f:
                    f.write(png_bytes)
                print(f"    -> Saved {dest.relative_to(out_root)}")

                row = {"rock": rock, "file": str(dest.relative_to(out_root)), "url": link}
                credits_rows.append(row)
                credits_json.append(row)

            except Exception as e:
                print(f"    ! Write failed {dest}: {e}")
                saved -= 1  # keep numbering contiguous if write fails

    # Write credits
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
