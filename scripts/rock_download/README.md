# Rock Image Downloader (Google CSE JSON API)

This script uses the Google Custom Search JSON API to fetch image results for each rock type
with the query `"<rock type> rock sample"` and downloads the first *N* images into per‑rock folders.

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

### Options

- `--limit / -n`   Images per rock type (default 10)
- `--out / -o`     Output root directory (default `rock_images`)
- `--types / -t`   Subset of rock types (defaults to all 22)
- `--query_suffix` Suffix appended after each rock type (default `rock sample`)
- `--overwrite`    Overwrite files if the same name already exists

### Notes

- The script attempts to determine a reasonable file extension from `Content-Type` or the URL.
- Be mindful of API **quotas** and **rate limits**. You can increase the pauses in the script if needed.
- **Licensing:** Downloaded images are often copyrighted—verify licenses before reuse.
