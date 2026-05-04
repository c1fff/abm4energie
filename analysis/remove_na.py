import json
import pandas as pd
from pathlib import Path

try:
    NB_DIR = Path(__file__).resolve().parent  # type: ignore[name-defined]
except NameError:
    NB_DIR = Path.cwd()

BASE = NB_DIR.parent
RAW_JSON = BASE / "data" / "raw" / "survey.json"
OUT_JSON = BASE / "data" / "processed" / "survey_v1.1.json"

# Read JSON
with open(RAW_JSON) as f:
    records = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(records)

# Replace "." and "" with pd.NA
df = df.replace({".": pd.NA, "": pd.NA})

# Create output directory if it doesn't exist
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

# Save as cleaned JSON
df.to_json(OUT_JSON, orient='records', indent=2)

print(f"✓ Created {OUT_JSON}")
print(f"  Records: {len(df)}")