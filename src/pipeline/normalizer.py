from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass
class NormalizedJob:
    _input: str
    _position: int
    id: str
    ciphertext: str
    title: str
    description: str
    url: str
    skills: List[str]
    jobType: Optional[str]
    hourlyBudgetMin: Optional[str]
    hourlyBudgetMax: Optional[str]
    fixedPriceAmount: Optional[float]
    duration: Optional[str]
    durationWeeks: Optional[int]
    durationDays: Optional[int]
    contractorTier: Optional[str]
    hourlyEngagementType: Optional[str]
    createTime: Optional[str]
    publishTime: Optional[str]
    sourcingTimestamp: Optional[str]
    weeklyRetainerBudget: Optional[float]
    relevancePosition: Optional[int]
    client: Optional[Dict[str, Any]] = None
    similarJobs: Optional[List[Dict[str, Any]]] = None

def _inputs_summary(inputs: Dict[str, Any]) -> str:
    # Create a concise, deterministic summary string from inputs
    parts = []
    if inputs.get("contract_to_hire"):
        parts.append("contract_to_hire=true")
    if inputs.get("hourly_rate"):
        parts.append(f"hourly_rate={inputs['hourly_rate']}")
    if inputs.get("query"):
        parts.append(f"search={inputs['query']}")
    if inputs.get("timezone"):
        parts.append(f"timezone={inputs['timezone']}")
    if inputs.get("t") is not None:
        parts.append(f"t={inputs['t']}")
    return " | ".join(parts) if parts else "default"

def _iso_or_none(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    try:
        # Pass-through if already ISO
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return s
    except Exception:
        return None

def normalize_record(raw: Dict[str, Any], inputs_summary: Dict[str, Any], discovered_at: str) -> Dict[str, Any]:
    """
    Map raw record to the public schema with safe defaults.
    """
    norm = NormalizedJob(
        _input=_inputs_summary(inputs_summary),
        _position=int(raw.get("_position") or raw.get("position") or 0),
        id=str(raw.get("id") or ""),
        ciphertext=str(raw.get("ciphertext") or ""),
        title=str(raw.get("title") or "Untitled"),
        description=str(raw.get("description") or ""),
        url=str(raw.get("url") or ""),
        skills=list(raw.get("skills") or []),
        jobType=raw.get("jobType"),
        hourlyBudgetMin=str(raw.get("hourlyBudgetMin")) if raw.get("hourlyBudgetMin") is not None else None,
        hourlyBudgetMax=str(raw.get("hourlyBudgetMax")) if raw.get("hourlyBudgetMax") is not None else None,
        fixedPriceAmount=float(raw.get("fixedPriceAmount")) if raw.get("fixedPriceAmount") is not None else None,
        duration=raw.get("duration"),
        durationWeeks=int(raw.get("durationWeeks")) if raw.get("durationWeeks") is not None else None,
        durationDays=int(raw.get("durationDays")) if raw.get("durationDays") is not None else None,
        contractorTier=raw.get("contractorTier"),
        hourlyEngagementType=raw.get("hourlyEngagementType"),
        createTime=_iso_or_none(raw.get("createTime")),
        publishTime=_iso_or_none(raw.get("publishTime")),
        sourcingTimestamp=discovered_at,
        weeklyRetainerBudget=float(raw.get("weeklyRetainerBudget")) if raw.get("weeklyRetainerBudget") else None,
        relevancePosition=int(raw.get("relevancePosition")) if raw.get("relevancePosition") is not None else None,
        client=raw.get("client"),
        similarJobs=raw.get("similarJobs"),
    )
    out = asdict(norm)

    # Backfill durationWeeks from "duration" if possible
    if out.get("durationWeeks") is None and isinstance(out.get("duration"), str):
        txt = out["duration"].lower()
        if "3 to 6 months" in txt:
            out["durationWeeks"] = 18
        elif "1 to 3 months" in txt:
            out["durationWeeks"] = 8
        elif "less than a month" in txt:
            out["durationWeeks"] = 4

    # Sanity: ensure essential fields
    if not out["id"]:
        out["id"] = f"gen-{abs(hash(out['title'])) % 10**10}"
        out["ciphertext"] = f"~0{out['id']}"

    return out