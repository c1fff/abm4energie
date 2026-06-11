import json
import pandas as pd
from pathlib import Path

try:
    NB_DIR = Path(__file__).resolve().parent  # type: ignore[name-defined]
except NameError:
    NB_DIR = Path.cwd()

BASE = NB_DIR.parent
CLEANED_JSON = BASE / "data" / "processed" / "survey_v1.1.json"
OUT_CSV = BASE / "data" / "processed" / "trig.csv"

# Read cleaned JSON
with open(CLEANED_JSON) as f:
    records = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(records)

# Select id and TRIG columns
trig_cols = [col for col in df.columns if col.startswith('TRIG_')]
selected_cols = ['id'] + sorted(trig_cols)

# Keep only available columns
selected_cols = [col for col in selected_cols if col in df.columns]

df_filtered = df[selected_cols]

# Create output directory if it doesn't exist
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

# Save to CSV
df_filtered.to_csv(OUT_CSV, index=False)

print(f"✓ Created {OUT_CSV}")
print(f"  Rows: {len(df_filtered)}")
print(f"  Columns: {', '.join(selected_cols)}")