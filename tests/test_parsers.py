import sys
from pathlib import Path

# Add src to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from parsers.listing_parser import parse_listings  # noqa
from parsers.details_parser import parse_details  # noqa

def test_parse_listings_from_mock_payload():
    mock = [
        {
            "_position": 1,
            "id": "1234567890123456789",
            "ciphertext": "~01234567890123456789",
            "title": "Data Engineer #1",
            "description": "Build reliable data pipelines.",
            "url": "https://www.upwork.com/freelance-jobs/apply/~01234567890123456789/",
            "skills": ["Python", "ETL"],
            "jobType": "HOURLY",
            "hourlyBudgetMin": "30.0",
            "hourlyBudgetMax": "60.0",
            "fixedPriceAmount": None,
            "duration": "3 to 6 months",
            "durationWeeks": 18,
            "durationDays": None,
            "hourlyEngagementType": "PART_TIME",
            "contractorTier": "ExpertLevel",
            "createTime": "2025-01-01T00:00:00Z",
            "publishTime": "2025-01-01T00:00:00Z",
            "relevancePosition": 1,
        }
    ]
    out = parse_listings(mock)
    assert isinstance(out, list)
    assert out[0]["id"] == "1234567890123456789"
    assert out[0]["title"].startswith("Data Engineer")

def test_parse_details_structured():
    payload = {
        "client": {
            "location": "United States",
            "totalSpent": 12345,
            "hireCount": 3,
            "rating": 4.9,
            "timezone": "America/New_York",
            "preferredQualifications": ["Rising Talent"],
        },
        "similarJobs": [{"title": "Another role", "url": "https://example.com"}],
    }
    out = parse_details(payload)
    assert "client" in out and "similarJobs" in out
    assert out["client"]["totalSpent"] == 12345