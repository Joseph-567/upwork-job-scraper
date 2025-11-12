import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pipeline.normalizer import normalize_record  # noqa
from pipeline.exporters import export_json, export_csv, export_excel, export_xml  # noqa

def test_normalize_record_fields(tmp_path):
    raw = {
        "_position": 2,
        "id": "9876543210987654321",
        "ciphertext": "~09876543210987654321",
        "title": "Backend Engineer",
        "description": "Maintain services",
        "url": "https://www.upwork.com/freelance-jobs/apply/~09876543210987654321/",
        "skills": ["Python", "Django"],
        "jobType": "HOURLY",
        "hourlyBudgetMin": "40.0",
        "hourlyBudgetMax": "80.0",
        "duration": "1 to 3 months",
        "relevancePosition": 2,
    }
    inputs = {"query": "backend engineer", "timezone": "UTC"}
    out = normalize_record(raw, inputs_summary=inputs, discovered_at=datetime.utcnow().isoformat())
    assert out["id"] == "9876543210987654321"
    assert out["durationWeeks"] in (8, 18, 4)

def test_exporters_roundtrip(tmp_path):
    records = [
        {
            "_input": "default",
            "_position": 1,
            "id": "1",
            "ciphertext": "~01",
            "title": "Example",
            "description": "Desc",
            "url": "https://example.com",
            "skills": [],
            "jobType": "HOURLY",
            "hourlyBudgetMin": "10.0",
            "hourlyBudgetMax": "20.0",
            "fixedPriceAmount": None,
            "duration": None,
            "durationWeeks": None,
            "durationDays": None,
            "contractorTier": None,
            "hourlyEngagementType": None,
            "createTime": None,
            "publishTime": None,
            "sourcingTimestamp": None,
            "weeklyRetainerBudget": None,
            "relevancePosition": 1,
            "client": None,
            "similarJobs": None,
        }
    ]
    j = tmp_path / "out.json"
    c = tmp_path / "out.csv"
    x = tmp_path / "out.xlsx"
    xm = tmp_path / "out.xml"

    export_json(records, j)
    export_csv(records, c)
    export_excel(records, x)
    export_xml(records, xm)

    assert j.exists() and json.loads(j.read_text(encoding="utf-8"))[0]["id"] == "1"
    assert c.exists()
    assert x.exists()
    assert xm.exists()