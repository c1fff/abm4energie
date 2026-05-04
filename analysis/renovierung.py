import json
import pandas as pd
from pathlib import Path

try:
    NB_DIR = Path(__file__).resolve().parent  # type: ignore[name-defined]
except NameError:
    NB_DIR = Path.cwd()

BASE = NB_DIR.parent
RAW_JSON = BASE / "data" / "raw" / "survey.json"
OUT_CSV = BASE / "data" / "processed" / "sanierung.csv"

# Read JSON
with open(RAW_JSON) as f:
    records = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(records)

# Get all REN_* columns
ren_cols = [col for col in df.columns if col.startswith('REF_')]
ren_cols_sorted = sorted(ren_cols)  # Ensure consistent order

# Select columns: id first, then all REN_*
selected_cols = ['id'] + ren_cols_sorted

df_filtered = df[selected_cols].copy()

# Add RE*_COUNT: count occurrences of "1" in REN_1 through REN_7
ren_numeric_cols = ['REF_1', 'REF_2', 'REF_3', 'REF_4', 'REF_5', 'REF_6', 'REF_7', 'REF_8', 'REF_9', 'REF_10', 'REF_11']
df_filtered['REF_COUNT'] = df_filtered[ren_numeric_cols].apply(
    lambda row: sum(1 for val in row if val == "1" or val == 1),
    axis=1
)

# Replace "." with pd.NA
df_filtered = df_filtered.replace({".": pd.NA, "": pd.NA})

# Create output directory if it doesn't exist
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

# Save to CSV
df_filtered.to_csv(OUT_CSV, index=False)

print(f"✓ Created {OUT_CSV}")
print(f"  Rows: {len(df_filtered)}")
print(f"  Columns: {len(df_filtered.columns)}")
print(f"\n  Columns included: id, {', '.join(ren_cols_sorted)}, REF_COUNT")