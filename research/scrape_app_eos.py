#!/usr/bin/env python3
"""
APP Executive Order Scraper
Church Bells / The Statecraft Blueprint
EO Structural Weight Score project

Downloads executive order text from The American Presidency Project
(presidency.ucsb.edu) and saves to structured JSON + CSV index.

Usage:
    # Install dependencies first:
    pip install requests beautifulsoup4 lxml

    # Full corpus (all EOs, newest first — takes ~3 hours):
    python scrape_app_eos.py

    # Mayer validation period only (1949–1999):
    python scrape_app_eos.py --start 1949-01-01 --end 1999-12-31

    # Modern period only (2000–present):
    python scrape_app_eos.py --start 2000-01-01

    # Test run — first 5 EOs only:
    python scrape_app_eos.py --test

    # Resume interrupted run (skips already-downloaded files):
    python scrape_app_eos.py   # just re-run; resume is automatic

Output:
    eo_corpus/
        eo_index.csv          master index (eo_number, title, date, president, url)
        texts/
            EO-10030.json     one file per EO (metadata + full text)
            EO-10031.json
            ...
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://www.presidency.ucsb.edu"
CATEGORY_URL = (
    BASE_URL
    + "/documents/app-categories/written-presidential-orders"
    + "/presidential/executive-orders"
)

OUTPUT_DIR = Path("eo_corpus")
TEXTS_DIR = OUTPUT_DIR / "texts"
INDEX_FILE = OUTPUT_DIR / "eo_index.csv"
ERROR_LOG = OUTPUT_DIR / "errors.log"

ITEMS_PER_PAGE = 60
RATE_LIMIT_SECONDS = 1.5  # polite delay between requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; TSB-EO-Scraper/1.0; "
        "Church Bells Governance Research; "
        "+https://ringthebells.org)"
    )
}

INDEX_FIELDS = ["eo_number", "title", "date", "president", "url", "status"]


# ---------------------------------------------------------------------------
# Helper: date parsing
# ---------------------------------------------------------------------------

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

def parse_app_date(raw: str) -> date | None:
    """Parse dates like 'December 22, 2023' or 'January 5, 1949'."""
    raw = raw.strip()
    # Match: Month Day, Year
    m = re.match(
        r"(\w+)\s+(\d{1,2}),\s+(\d{4})", raw, re.IGNORECASE
    )
    if m:
        month_name, day, year = m.groups()
        month = MONTH_MAP.get(month_name.lower())
        if month:
            try:
                return date(int(year), month, int(day))
            except ValueError:
                pass
    return None


def date_in_range(
    d: date | None,
    start: date | None,
    end: date | None,
) -> bool:
    if d is None:
        return True  # include if we can't parse — filter later
    if start and d < start:
        return False
    if end and d > end:
        return False
    return True


# ---------------------------------------------------------------------------
# Helper: EO number extraction
# ---------------------------------------------------------------------------

def extract_eo_number(title: str, url: str) -> str:
    """Extract EO number from title string like 'Executive Order 14114—...'"""
    # Try title first — number immediately after "Executive Order"
    m = re.search(r"Executive Order\s+([\d]+)", title, re.IGNORECASE)
    if m:
        return m.group(1)
    # Fall back to URL slug
    m = re.search(r"executive-order-([\d]+)", url)
    if m:
        return m.group(1)
    return "UNKNOWN"


def clean_president(raw: str) -> str:
    """
    Strip junk concatenated after the president name.

    The APP selector sometimes grabs:
      "Donald J. Trump (2nd Term)47th President of the United States: 2025—present
       Executive Order 14412—..."

    We want only: "Donald J. Trump (2nd Term)"
    """
    if not raw:
        return raw
    # Truncate at the ordinal number before "President of the United States"
    cleaned = re.split(r"\d+(?:st|nd|rd|th)\s+President", raw)[0]
    # Truncate at any concatenated EO title
    cleaned = re.split(r"Executive Order", cleaned)[0]
    return cleaned.strip()


def pending_eo_id(date_iso: str, url: str) -> str:
    """
    Generate a stable placeholder ID for EOs the APP hasn't numbered yet.
    Format: PENDING-YYYY-MM-DD-slug (first 30 chars of slug)
    """
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    slug = re.sub(r"[^\w-]", "", slug)[:30]
    return f"PENDING-{date_iso}-{slug}" if date_iso else f"PENDING-{slug}"


# ---------------------------------------------------------------------------
# Phase 1: collect EO URLs from category browse pages
# ---------------------------------------------------------------------------

def fetch_category_page(page_num: int) -> list[dict]:
    """
    Fetch one browse page and return list of dicts:
    {title, url, raw_date, president_hint}
    """
    url = f"{CATEGORY_URL}?items_per_page={ITEMS_PER_PAGE}&page={page_num}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    current_date_str = ""

    # The page uses h4 date headers followed by document entries.
    # Iterate through the main content area.
    content = soup.find("div", {"id": "content"}) or soup.find("main") or soup

    for tag in content.find_all(["h4", "h3", "div", "span"], recursive=True):
        # Date headers appear as h4 tags with date text
        if tag.name == "h4":
            text = tag.get_text(strip=True)
            if re.match(r"\w+ \d+, \d{4}", text):
                current_date_str = text
                continue

        # EO links — look for anchor tags whose text starts with "Executive Order"
        if tag.name in ("div", "span"):
            for a in tag.find_all("a", href=True):
                href = a["href"]
                text = a.get_text(strip=True)
                if (
                    "executive-order" in href
                    and text.lower().startswith("executive order")
                ):
                    full_url = href if href.startswith("http") else BASE_URL + href
                    # Try to find associated president link near this tag
                    president = ""
                    parent = a.find_parent()
                    if parent:
                        for pa in parent.find_all("a", href=True):
                            if "/people/president/" in pa["href"]:
                                president = pa.get_text(strip=True)
                                break

                    results.append(
                        {
                            "title": text,
                            "url": full_url,
                            "raw_date": current_date_str,
                            "president": president,
                        }
                    )

    # Deduplicate by URL (same EO may appear multiple times in DOM)
    seen = set()
    deduped = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            deduped.append(r)

    return deduped


def get_total_pages(soup: BeautifulSoup | None = None) -> int:
    """Infer total page count from the site (10,856 EOs / 60 per page)."""
    # Fetch page 0 to read the count dynamically
    url = f"{CATEGORY_URL}?items_per_page={ITEMS_PER_PAGE}&page=0"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Look for "Displaying X - Y of Z" text
    m = re.search(r"of\s+([\d,]+)", soup.get_text())
    if m:
        total = int(m.group(1).replace(",", ""))
        return (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    return 182  # safe fallback based on 10,856 / 60


# ---------------------------------------------------------------------------
# Phase 2: fetch individual EO pages
# ---------------------------------------------------------------------------

def fetch_eo_page(url: str) -> dict:
    """
    Fetch a single EO page and return:
    {url, eo_number, title, date_str, date_iso, president, text}
    """
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # --- Title ---
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""

    # --- Date ---
    # The APP renders the date in a span or div near the top of the document.
    # It follows the h1 and president block.
    date_str = ""
    # Try common Drupal field patterns first
    for sel in [
        ".field-docs-start-date-time",
        ".date-display-single",
        ".field--name-field-docs-start-date",
        ".views-field-field-docs-start-date-time",
    ]:
        el = soup.select_one(sel)
        if el:
            date_str = el.get_text(strip=True)
            break

    # Fallback: scan paragraph/span text near the h1 for a date pattern
    if not date_str:
        for tag in soup.find_all(["p", "span", "div"])[:30]:
            text = tag.get_text(strip=True)
            if re.match(r"\w+ \d{1,2}, \d{4}$", text):
                date_str = text
                break

    parsed_date = parse_app_date(date_str)
    date_iso = parsed_date.isoformat() if parsed_date else ""

    # --- President ---
    president = ""
    # Prefer the anchor tag directly (shortest clean text)
    pres_anchor = soup.select_one("a[href*='/people/president/']")
    if pres_anchor:
        president = clean_president(pres_anchor.get_text(strip=True))
    else:
        for sel in [".field-docs-person", "h3 a[href*='/people/president/']"]:
            el = soup.select_one(sel)
            if el:
                president = clean_president(el.get_text(strip=True))
                break

    # --- Body text ---
    # The document text is in a specific content div
    text = ""
    for sel in [
        ".field-docs-content",
        ".field--name-field-docs-content",
        ".field-body",
        "article .field",
        "#content .field",
    ]:
        el = soup.select_one(sel)
        if el:
            text = el.get_text(separator="\n", strip=True)
            break

    # Last resort: grab everything after the h1 inside main content
    if not text and h1:
        content_area = h1.find_parent("article") or h1.find_parent("main")
        if content_area:
            # Remove nav/sidebar elements
            for unwanted in content_area.find_all(["nav", "aside", "footer"]):
                unwanted.decompose()
            # Text after the h1
            started = False
            chunks = []
            for tag in content_area.descendants:
                if tag == h1:
                    started = True
                    continue
                if started and isinstance(tag, str) and tag.strip():
                    chunks.append(tag.strip())
            text = "\n".join(chunks)

    eo_number = extract_eo_number(title, url)
    if eo_number == "UNKNOWN":
        # EO not yet numbered in Federal Register — use stable date+slug placeholder
        eo_number = pending_eo_id(date_iso, url)

    return {
        "url": url,
        "eo_number": eo_number,
        "title": title,
        "date_str": date_str,
        "date_iso": date_iso,
        "president": president,
        "text": text,
    }


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def eo_filename(eo_number: str) -> str:
    safe = re.sub(r"[^\w-]", "_", eo_number)
    return f"EO-{safe}.json"


def load_existing_index() -> set[str]:
    """Return set of URLs already in the index (successfully downloaded)."""
    if not INDEX_FILE.exists():
        return set()
    done = set()
    with open(INDEX_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status") == "ok":
                done.add(row["url"])
    return done


def append_to_index(row: dict) -> None:
    write_header = not INDEX_FILE.exists()
    with open(INDEX_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INDEX_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def log_error(url: str, error: str) -> None:
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {url} | {error}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Scrape executive orders from The American Presidency Project."
    )
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Start date filter YYYY-MM-DD (inclusive). Default: no filter.",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="End date filter YYYY-MM-DD (inclusive). Default: no filter.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode: download first 5 EOs only.",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=RATE_LIMIT_SECONDS,
        help=f"Seconds between requests (default: {RATE_LIMIT_SECONDS}).",
    )
    args = parser.parse_args()

    start_date = date.fromisoformat(args.start) if args.start else None
    end_date = date.fromisoformat(args.end) if args.end else None

    # Setup output directories
    OUTPUT_DIR.mkdir(exist_ok=True)
    TEXTS_DIR.mkdir(exist_ok=True)

    # Load existing progress
    done_urls = load_existing_index()
    print(f"Resume: {len(done_urls)} EOs already downloaded.")

    # --- Phase 1: collect URLs ---
    print("\nPhase 1: collecting EO URLs from category browse pages...")
    print("(Getting total page count...)")

    try:
        total_pages = get_total_pages()
    except Exception as e:
        print(f"Warning: could not determine total pages ({e}). Using 182.")
        total_pages = 182

    print(f"Total pages to scan: {total_pages}")

    all_entries = []
    for page_num in range(total_pages):
        try:
            entries = fetch_category_page(page_num)
            # Filter by date range
            filtered = []
            for e in entries:
                d = parse_app_date(e["raw_date"])
                if date_in_range(d, start_date, end_date):
                    filtered.append(e)
                elif end_date and d and d < end_date:
                    # EOs are newest-first; once we're past the end date
                    # and now before start_date, we can stop
                    pass

            all_entries.extend(filtered)

            pct = (page_num + 1) / total_pages * 100
            print(
                f"  Page {page_num + 1}/{total_pages} ({pct:.0f}%) — "
                f"{len(filtered)} entries (total collected: {len(all_entries)})",
                end="\r",
            )
            time.sleep(args.rate)

        except KeyboardInterrupt:
            print("\nInterrupted during URL collection. Proceeding with collected URLs.")
            break
        except Exception as e:
            print(f"\nError on page {page_num}: {e}")
            log_error(f"PAGE-{page_num}", str(e))
            time.sleep(args.rate * 2)

    print(f"\nPhase 1 complete. {len(all_entries)} EO URLs collected.")

    if args.test:
        all_entries = all_entries[:5]
        print(f"Test mode: limiting to {len(all_entries)} EOs.")

    # --- Phase 2: download EO texts ---
    print(f"\nPhase 2: downloading EO texts...")

    new_count = 0
    skip_count = 0
    error_count = 0

    for i, entry in enumerate(all_entries):
        url = entry["url"]

        if url in done_urls:
            skip_count += 1
            continue

        try:
            eo_data = fetch_eo_page(url)

            # Save JSON text file
            fname = eo_filename(eo_data["eo_number"])
            json_path = TEXTS_DIR / fname
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(eo_data, f, indent=2, ensure_ascii=False)

            # Append to index
            append_to_index(
                {
                    "eo_number": eo_data["eo_number"],
                    "title": eo_data["title"],
                    "date": eo_data["date_iso"],
                    "president": eo_data["president"],
                    "url": url,
                    "status": "ok",
                }
            )

            new_count += 1
            print(
                f"  [{i+1}/{len(all_entries)}] OK: {eo_data['eo_number']} "
                f"({eo_data['date_iso']}) {eo_data['title'][:60]}",
                end="\r",
            )

        except KeyboardInterrupt:
            print("\nInterrupted. Progress saved. Re-run to resume.")
            sys.exit(0)
        except Exception as e:
            error_count += 1
            print(f"\n  [{i+1}/{len(all_entries)}] ERROR: {url} — {e}")
            log_error(url, str(e))
            append_to_index(
                {
                    "eo_number": entry.get("title", "")[:20],
                    "title": entry.get("title", ""),
                    "date": "",
                    "president": entry.get("president", ""),
                    "url": url,
                    "status": f"error: {e}",
                }
            )

        time.sleep(args.rate)

    print(f"\n\nDone.")
    print(f"  New downloads:  {new_count}")
    print(f"  Skipped (done): {skip_count}")
    print(f"  Errors:         {error_count}")
    print(f"\nOutput: {OUTPUT_DIR.resolve()}")
    print(f"Index:  {INDEX_FILE.resolve()}")
    if error_count:
        print(f"Errors logged to: {ERROR_LOG.resolve()}")
        print("Re-run to retry failed URLs (they'll be skipped for 'ok' ones).")


if __name__ == "__main__":
    main()
