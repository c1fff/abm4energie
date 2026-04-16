import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from .repository import data as survey_data



def normalize_value(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned == "" or cleaned == "." or cleaned.lower() == "null":
            return None
        return cleaned
    return str(value)


def fill_defaults(record: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {}
    for key, value in record.items():
        normalized = normalize_value(value)
        if normalized is None:
            if key == "GROUP_BEH":
                cleaned[key] = "6"
            else:
                cleaned[key] = ""
        else:
            cleaned[key] = normalized
    return cleaned


def clean_survey_data(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned_records: List[Dict[str, Any]] = []
    for record in records:
        if "GROUP_BEH" not in record:
            continue
        group = normalize_value(record.get("GROUP_BEH"))
        if group is None:
            group = "6"
        record["GROUP_BEH"] = group
        cleaned_records.append(fill_defaults(record))
    return cleaned_records


def load_survey_data() -> List[Dict[str, Any]]:
    if not isinstance(survey_data, list):
        raise ValueError("survey.json must contain a list of records")
    return clean_survey_data(survey_data)

