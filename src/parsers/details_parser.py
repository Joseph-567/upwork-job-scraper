from typing import Any, Dict

def parse_details(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Currently the detail fetcher already returns a structured dict.
    This function exists to validate and future-proof transformations.
    """
    client = payload.get("client") or {}
    similar = payload.get("similarJobs") or []
    # Minimal normalization
    if client and isinstance(client.get("totalSpent"), (int, float)) and client["totalSpent"] < 0:
        client["totalSpent"] = 0
    return {"client": client, "similarJobs": similar}