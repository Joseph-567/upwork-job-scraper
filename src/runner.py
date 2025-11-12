import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Make src importable when running from repo root
CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from collectors.search_fetcher import fetch_search
from collectors.job_detail_fetcher import fetch_detail
from parsers.listing_parser import parse_listings
from parsers.details_parser import parse_details
from pipeline.normalizer import normalize_record
from pipeline.exporters import export_json, export_csv, export_excel, export_xml

def load_inputs(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_out_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Upwork Job Scraper (offline-friendly)")
    parser.add_argument(
        "--inputs",
        type=str,
        default=str(REPO_ROOT / "data" / "inputs.sample.json"),
        help="Path to inputs JSON (defaults to data/inputs.sample.json)",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default=str(REPO_ROOT / "data"),
        help="Output directory for exported files",
    )
    parser.add_argument(
        "--formats",
        type=str,
        default="json,csv,excel,xml",
        help="Comma-separated export formats: json,csv,excel,xml",
    )
    parser.add_argument(
        "--include-details",
        action="store_true",
        help="Enrich results with client details (may be slower online; offline uses mock)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Run without network by generating deterministic mock data",
    )
    args = parser.parse_args()

    inputs_path = Path(args.inputs)
    outdir = Path(args.outdir)
    ensure_out_dir(outdir)

    inputs = load_inputs(inputs_path)
    search_url = inputs.get("search_url", "")
    query = inputs.get("query", "")
    max_items = int(inputs.get("max_items", 25))
    timezone = inputs.get("timezone", "UTC")

    settings = {
        "offline": args.offline or inputs.get("offline", False),
        "proxy": inputs.get("proxy"),  # dict or None
        "timeout": int(inputs.get("timeout", 20)),
        "retries": int(inputs.get("retries", 2)),
        "timezone": timezone,
    }

    # 1) Fetch search results page/content (HTML or JSON-like)
    raw_search_payload = fetch_search(
        search_url=search_url, query=query, max_items=max_items, settings=settings
    )

    # 2) Parse listing summaries
    listings = parse_listings(raw_search_payload)

    # 3) Optionally fetch & parse details for each job
    if args.include_details or inputs.get("include_details"):
        enriched = []
        for li in listings:
            try:
                detail_payload = fetch_detail(li.get("url"), settings=settings)
                details = parse_details(detail_payload)
                li["client"] = details.get("client")
                li["similarJobs"] = details.get("similarJobs", [])
            except Exception as e:
                # Minimal error handling; keep the scraper resilient
                li["client_error"] = str(e)
            enriched.append(li)
        listings = enriched

    # 4) Normalize to final schema
    now_iso = datetime.utcnow().isoformat()
    normalized = [
        normalize_record(li, inputs_summary=inputs, discovered_at=now_iso) for li in listings
    ]

    # 5) Export
    formats = [f.strip().lower() for f in args.formats.split(",") if f.strip()]
    base_name = f"upwork_jobs_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    exported = []

    if "json" in formats:
        p = outdir / f"{base_name}.json"
        export_json(normalized, p)
        exported.append(p.name)
    if "csv" in formats:
        p = outdir / f"{base_name}.csv"
        export_csv(normalized, p)
        exported.append(p.name)
    if "excel" in formats:
        p = outdir / f"{base_name}.xlsx"
        export_excel(normalized, p)
        exported.append(p.name)
    if "xml" in formats:
        p = outdir / f"{base_name}.xml"
        export_xml(normalized, p)
        exported.append(p.name)

    # Print a concise summary to stdout
    print(json.dumps({"count": len(normalized), "exported": exported}, indent=2))

if __name__ == "__main__":
    main()