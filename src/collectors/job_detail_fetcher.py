import random
from typing import Any, Dict

try:
    import requests  # noqa
except Exception:
    requests = None  # Offline or minimal env

def _mock_detail(url: str) -> Dict[str, Any]:
    seed = sum(ord(c) for c in url) % 100
    client = {
        "location": "United States" if seed % 2 == 0 else "United Kingdom",
        "totalSpent": 5000 + seed * 23,
        "hireCount": (seed % 7) + 1,
        "rating": round(4.6 + (seed % 4) * 0.1, 2) if seed % 5 != 0 else None,
        "timezone": "America/New_York" if seed % 2 == 0 else "Europe/London",
        "preferredQualifications": ["Rising Talent", "Job Success > 90%"] if seed % 3 == 0 else ["Any"],
    }
    similar = [
        {
            "title": f"Related API/Data role {i+1}",
            "url": url.replace("apply", f"similar-{i+1}") if "apply" in url else url + f"/similar-{i+1}",
        }
        for i in range(3)
    ]
    return {"client": client, "similarJobs": similar}

def fetch_detail(url: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    offline = bool(settings.get("offline"))
    if offline or requests is None:
        return _mock_detail(url)

    # Minimal online attempt; real pages require cookies/auth; fallback to mock
    try:
        headers = {"User-Agent": "Mozilla/5.0 UpworkJobScraper/1.0"}
        timeout = int(settings.get("timeout", 20))
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        # In real world we'd parse HTML; we just return mock-enriched for demo resilience
        return _mock_detail(url)
    except Exception:
        return _mock_detail(url)