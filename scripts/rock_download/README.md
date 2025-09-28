# Rock Image Downloader (Google CSE JSON API)

This script uses the Google Custom Search JSON API to fetch image results for each rock type,
downloads the images, converts them to PNG format, and saves them with standardized filenames
(`<rocktype>_NNN.png`). It also generates credits files in both CSV and JSON formats to track
the source URLs of downloaded images.

## Quick Start

1. **Create a Google CSE** with Image Search enabled; note its `cx`.
2. **Create an API key** for the Custom Search JSON API.
3. Download these files, then:
   ```bash
   cp .env.example .env
   # edit .env to add GOOGLE_API_KEY and GOOGLE_CSE_CX
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python download_rock_images.py --limit 10 --out ./rock_images
   ```

## Options

- `--limit / -n`     Images per rock type (default: 10)
- `--out / -o`       Output root directory (default: `rock_images`)
- `--types / -t`     Subset of rock types (defaults to all 22 types)
- `--query_suffix`   Suffix appended after each rock type (default: `rock sample`)
- `--rights`         Usage rights filter for Google CSE (e.g., `cc_publicdomain,cc_attribute`)
- `--public_domain`  Shortcut for `--rights cc_publicdomain`
- `--domains`        Comma-separated TLDs to bias search (e.g., `.edu,.gov`)
- `--sites`          Comma-separated hostnames to limit search (e.g., `usgs.gov,si.edu`)

## New Features

### Usage Rights Filtering
The script now supports Google CSE usage rights filtering to help find images with appropriate licenses:

```bash
# Public domain only
python download_rock_images.py --public_domain

# Multiple usage rights
python download_rock_images.py --rights cc_publicdomain,cc_attribute

# Available rights: cc_publicdomain, cc_attribute, cc_sharealike, cc_noncommercial, cc_nonderived
```

### Domain and Site Filtering
Bias your search towards educational/government sources or specific sites:

```bash
# Prefer .edu and .gov domains
python download_rock_images.py --domains .edu,.gov

# Search only specific sites
python download_rock_images.py --sites usgs.gov,si.edu

# Combine with rights filtering
python download_rock_images.py --public_domain --domains .edu,.gov
```

## Output

The script creates:
- **Image files:** `<rocktype>_001.png`, `<rocktype>_002.png`, etc. (all converted to PNG)
- **Credits CSV:** `credits.csv` with columns: rock, file, url
- **Credits JSON:** `credits.json` with the same data in JSON format

## Notes

- **File format:** All images are converted to PNG format regardless of source format
- **Animated images:** First frame is extracted from animated formats (GIF, WebP, etc.)
- **Error handling:** Invalid images are skipped, and the script continues processing
- **Rate limiting:** Built-in pauses between API calls and downloads to respect limits
- **Licensing:** Always verify image licenses before reuse, even with usage rights filtering
