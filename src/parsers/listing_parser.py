from typing import Any, Dict, List, Union
from bs4 import BeautifulSoup

Payload = Union[str, List[Dict[str, Any]], Dict[str, Any]]

def _from_html(html: str) -> List[Dict[str, Any]]:
    """
    Very forgiving HTML parser. It looks for data-job-id attributes and common
    classes, but gracefully returns empty if not found.
    """
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for idx, card in enumerate(soup.select("[data-job-id]")):
        job_id = card.get("data-job-id")
        title_el = card.select_one(".job-tile-title,.title")
        desc_el = card.select_one(".job-description,.description")
        url_el = card.select_one("a[href]")
        skills = [s.get_text(strip=True) for s in card.select(".skill,.skills .skill")]
        items.append(
            {
                "_position": idx + 1,
                "id": job_id,
                "ciphertext": f"~0{job_id}",
                "title": title_el.get_text(strip=True) if title_el else "Untitled",
                "description": desc_el.get_text(strip=True) if desc_el else "",
                "url": url_el["href"] if url_el else "",
                "skills": skills,
                "jobType": "HOURLY",
                "hourlyBudgetMin": None,
                "hourlyBudgetMax": None,
                "fixedPriceAmount": None,
                "duration": None,
                "durationWeeks": None,
                "durationDays": None,
                "hourlyEngagementType": None,
                "contractorTier": None,
                "createTime": None,
                "publishTime": None,
                "relevancePosition": idx + 1,
            }
        )
    return items

def parse_listings(payload: Payload) -> List[Dict[str, Any]]:
    """
    Accepts:
      - HTML string (from online fetch)
      - list[dict] (from offline generator or API-like response)
    Returns a normalized list of listing dicts (without client details).
    """
    if isinstance(payload, list):
        # Assume already structured
        return payload
    if isinstance(payload, dict):
        # Some APIs return {"results":[...]}
        if "results" in payload and isinstance(payload["results"], list):
            return payload["results"]
        # Unknown dict shape -> wrap
        return [payload]
    if isinstance(payload, str):
        return _from_html(payload)
    # Fallback empty
    return []