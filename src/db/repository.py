import json
from pathlib import Path

SURVEY_FILE = Path(__file__).resolve().parents[2] / "survey.json"

with open(SURVEY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)