import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from dicttoxml import dicttoxml

def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def export_json(records: List[Dict[str, Any]], path: Path) -> None:
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def export_csv(records: List[Dict[str, Any]], path: Path) -> None:
    _ensure_parent(path)
    df = pd.json_normalize(records)
    df.to_csv(path, index=False)

def export_excel(records: List[Dict[str, Any]], path: Path) -> None:
    _ensure_parent(path)
    df = pd.json_normalize(records)
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, index=False, sheet_name="jobs")

def export_xml(records: List[Dict[str, Any]], path: Path) -> None:
    _ensure_parent(path)
    xml_bytes = dicttoxml(records, custom_root="jobs", attr_type=False)
    with open(path, "wb") as f:
        f.write(xml_bytes)