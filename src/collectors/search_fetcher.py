import json
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Union

try:
    import requests  # noqa
except Exception:
    requests = None  # Offline or minimal env

UserPayload = Union[str, List[Dict[str, Any]], Dict[str, Any]]

def _rand_id() -> str:
    # 19-digit like examples in README
    return "".join(random.choices(string.digits, k=19))

def _cipher_from_id(s: str) -> str:
    return "~0" + s

def _mock_listings(query: str, max_items: int, tz: str) -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    base_title = (query or "Software Engineer").title()
    out = []
    for i in range(max_items):
        job_id = _rand_id()
        publish = now - timedelta(minutes=i * 3)
        item = {
            "_position": i + 1,
            "id": job_id,
            "ciphertext": _cipher_from_id(job_id),
            "title": f"{base_title} #{i+1}",
            "description": f"{base_title} role focusing on APIs, scraping, and data pipelines.",
            "url": f"https://www.upwork.com/freelance-jobs/apply/{_cipher_from_id(job_id)}/",
            "skills": ["Python", "Web Scraping", "Data Pipelines"],
            "jobType": "HOURLY" if i % 2 == 0 else "FIXED",
            "hourlyBudgetMin": "30.0" if i % 2 == 0 else None,
            "hourlyBudgetMax": "60.0" if i % 2 == 0 else None,
            "fixedPriceAmount": None if i % 2 == 0 else 500 + i * 25,
            "duration": "3 to 6 months",
            "durationWeeks": 18,
            "durationDays": None,
            "hourlyEngagementType": "PART_TIME" if i % 3 == 0 else "FULL_TIME",
            "contractorTier": "ExpertLevel" if i % 2 == 0 else "Intermediate",
            "createTime": publish.isoformat(),
            "publishTime": publish.isoformat(),
            "relevancePosition": i + 1,
        }
        out.append(item)
    return out

def fetch_search(search_url: str, query: str, max_items: int, settings: Dict[str, Any]) -> UserPayload:
    """
    Returns data for parsing listings.
    - Offline: a list[dict] mock payload.
    - Online: HTML string (best-effort) or a minimal JSON if API.
    """
    offline = bool(settings.get("offline"))
    if offline or requests is None:
        return _mock_listings(query=query, max_items=max_items, tz=settings.get("timezone", "UTC"))

    # Best-effort online fetch (simple HTML get); this may require cookies in real life.
    # We keep it minimal and robust.
    try:
        timeout = int(settings.get("timeout", 20))
        proxies = None
        proxy_cfg = settings.get("proxy")
        if proxy_cfg and isinstance(proxy_cfg, dict) and proxy_cfg.get("http"):
            proxies = {"http": proxy_cfg["http"], "https": proxy_cfg.get("https", proxy_cfg["http"])}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) UpworkJobScraper/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        url = search_url or "https://www.upwork.com/nx/jobs/search/?sort=recency"
        resp = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
        resp.raise_for_status()
        # Return HTML text for parser
        return resp.text
    except Exception as e:
        # Fallback to mock on any network issue
        return _mock_listings(query=query or "Engineer", max_items=max_items, tz=settings.get("timezone", "UTC"))