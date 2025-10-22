#!/usr/bin/env python3
import os, io, re, time, json, math, pathlib, mimetypes, shutil
from typing import List, Optional
import requests
from PIL import Image
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

# ----------------------------
# CONFIG
# ----------------------------
OUT_DIR = "geo151_images"  # images saved here
PER_NAME = 3               # target successful downloads per rock/mineral
MAX_SEARCH_RESULTS = 10    # try up to this many search results
QUERY_SUFFIX = "hand sample"
TIMEOUT = 20
HEADERS = {"User-Agent": "geo151-image-bot/1.0 (+for-educational-use)"}

# Provide these to use Google CSE (recommended for best results)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GOOGLE_CSE_CX  = os.getenv("GOOGLE_CSE_CX", "").strip()

# The list from your review sheet (feel free to trim/edit)
MINERALS = [
 "Amphibolite", "Chalk", "Coquina", "Limonite", "Micrite Limestone", "Oolitic Limestone", "Oolitic Limestone", "Schist", "Sphalerite"
]


CATEGORIES = {
    "minerals": MINERALS,
}

# ----------------------------
# UTILITIES
# ----------------------------
def sanitize(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    return name

def ensure_dir(p: pathlib.Path):
    p.mkdir(parents=True, exist_ok=True)

def to_jpeg_bytes(content: bytes) -> bytes:
    with Image.open(io.BytesIO(content)) as im:
        # Convert to RGB for JPEG compatibility
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGB")
        elif im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        out = io.BytesIO()
        im.save(out, format="JPEG", quality=90, optimize=True)
        return out.getvalue()

def fetch_binary(url: str) -> Optional[bytes]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print(f"  ! Download failed: {url} ({e})")
        return None

# ----------------------------
# SEARCH PROVIDERS
# ----------------------------
def google_cse_image_search(query: str, n: int) -> List[str]:
    """Use Google Programmable Search Engine for images."""
    if not (GOOGLE_API_KEY and GOOGLE_CSE_CX):
        return []
    print(f"  (Google) {query}")
    urls = []
    start = 1
    while len(urls) < n and start < 100:
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_CX,
            "searchType": "image",
            "q": query,
            "num": min(10, n - len(urls)),
            "start": start
        }
        try:
            r = requests.get("https://www.googleapis.com/customsearch/v1",
                             params=params, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            for item in data.get("items", []):
                link = item.get("link")
                if link:
                    urls.append(link)
            if "items" not in data or not data["items"]:
                break
            start += len(data["items"])
        except Exception as e:
            print(f"  ! Google CSE error: {e}")
            break
        time.sleep(0.7)  # polite pacing
    return urls[:n]

def wikimedia_image_search(query: str, n: int) -> List[str]:
    """
    Wikimedia Commons search with file URL expansion.
    We search for images matching the query and take original URLs.
    """
    print(f"  (Wikimedia) {query}")
    urls = []
    try:
        s = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={
                "action": "query",
                "generator": "search",
                "gsrsearch": query,
                "gsrnamespace": "6",  # File:
                "gsrlimit": "10",
                "prop": "imageinfo",
                "iiprop": "url|mime",
                "format": "json",
            },
            headers=HEADERS,
            timeout=TIMEOUT
        )
        s.raise_for_status()
        data = s.json()
        pages = list(data.get("query", {}).get("pages", {}).values())
        # Sort by index to respect search order
        pages.sort(key=lambda p: p.get("index", 9999))
        for p in pages:
            ii = p.get("imageinfo", [])
            if not ii:
                continue
            url = ii[0].get("url")
            mime = ii[0].get("mime", "")
            # Filter to common photo types
            if url and ("image/" in mime or url.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"))):
                urls.append(url)
            if len(urls) >= n:
                break
    except Exception as e:
        print(f"  ! Wikimedia error: {e}")
    return urls[:n]

def search_images(query: str, n: int) -> List[str]:
    print(f"    Searching for: {query}")
    urls = []
    # Prefer Google if available, else Wikimedia
    if GOOGLE_API_KEY and GOOGLE_CSE_CX:
        print("    Using Google CSE...")
        urls = google_cse_image_search(query, n)
    else:
        print("    Google CSE not available, using Wikimedia...")
    
    if len(urls) < n:
        print(f"    Got {len(urls)} from Google, trying Wikimedia for more...")
        wikimedia_urls = wikimedia_image_search(query, n*2)
        new_urls = [u for u in wikimedia_urls if u not in urls]
        urls += new_urls
        print(f"    Added {len(new_urls)} from Wikimedia")
    
    print(f"    Total URLs found: {len(urls)}")
    return urls[:n]

# ----------------------------
# MAIN WORKFLOW
# ----------------------------
def save_images_for_name(name: str, out_dir: pathlib.Path):
    base = sanitize(name)
    query = f"{base} {QUERY_SUFFIX}"
    
    # Search for more results than we need in case some downloads fail
    urls = search_images(query, MAX_SEARCH_RESULTS)
    if not urls:
        print(f"  ! No results for: {base}")
        return

    ensure_dir(out_dir)
    successful_downloads = 0
    
    for i, url in enumerate(urls, start=1):
        if successful_downloads >= PER_NAME:
            print(f"    ✓ Target of {PER_NAME} successful downloads reached!")
            break
            
        print(f"    -> Trying {i}/{len(urls)}: {url}")
        content = fetch_binary(url)
        if not content:
            print(f"      ! Download failed, continuing...")
            continue

        # Convert to JPEG regardless of source format
        try:
            jpeg_bytes = to_jpeg_bytes(content)
        except Exception as e:
            print(f"      ! Could not convert to JPEG ({e}); skipping.")
            continue

        # Use successful download counter for filename
        fname = f"{base.replace('/', '-')}-{successful_downloads + 1}.jpg"
        fpath = out_dir / fname
        with open(fpath, "wb") as f:
            f.write(jpeg_bytes)
        
        successful_downloads += 1
        print(f"      ✓ saved {fpath} ({successful_downloads}/{PER_NAME})")
    
    if successful_downloads < PER_NAME:
        print(f"  ! Only got {successful_downloads}/{PER_NAME} successful downloads for: {base}")

def main():
    print(f"Starting image search with output directory: {OUT_DIR}")
    print(f"Google API Key available: {'Yes' if GOOGLE_API_KEY else 'No'}")
    print(f"Google CSE CX available: {'Yes' if GOOGLE_CSE_CX else 'No'}")
    
    root = pathlib.Path(OUT_DIR)
    ensure_dir(root)
    print(f"Created output directory: {root.absolute()}")

    for cat, names in CATEGORIES.items():
        print(f"\n=== {cat.upper()} ===")
        cat_dir = root / cat
        ensure_dir(cat_dir)
        print(f"Processing {len(names)} items in category: {cat}")
        for nm in names:
            print(f"\n  {nm}")
            save_images_for_name(nm, cat_dir)

if __name__ == "__main__":
    main()
