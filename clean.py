import json
import pandas as pd
from pathlib import Path

try:
    NB_DIR = Path(__file__).resolve().parent  # type: ignore[name-defined]
except NameError:
    NB_DIR = Path.cwd()

BASE = NB_DIR.parent
RAW_JSON = BASE / "data" / "raw" / "survey.json"
OUT_CSV = BASE / "data" / "processed" / "renovierung.csv"


# ── Pipeline ────────────────────────────────────────────────────────────────

class Pipeline:
    """
    Load a JSON file, run a sequence of transformation steps, save to CSV.

    Each step is a function with the signature:
        step(df: pd.DataFrame) -> pd.DataFrame

    Usage:
        pipeline = Pipeline(RAW_JSON, OUT_CSV)
        pipeline.add_step(my_step)
        pipeline.run()
    """

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self._steps: list = []

    def add_step(self, fn):
        """Register a transformation step. Steps run in the order they are added."""
        self._steps.append(fn)
        return self  # allows chaining: pipeline.add_step(a).add_step(b)

    def run(self):
        """Entry point: load → transform → save."""
        df = self._load()
        df = self._apply_steps(df)
        self._save(df)

    # ── private ─────────────────────────────────────────────────────────────

    def _load(self) -> pd.DataFrame:
        with open(self.input_path) as f:
            records = json.load(f)
        return pd.DataFrame(records)

    def _apply_steps(self, df: pd.DataFrame) -> pd.DataFrame:
        for step in self._steps:
            df = step(df)
        return df

    def _save(self, df: pd.DataFrame):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, index=False)
        print(f"✓ Created {self.output_path}")
        print(f"  Rows:    {len(df)}")
        print(f"  Columns: {len(df.columns)}")


# ── Built-in steps ───────────────────────────────────────────────────────────
# Each function takes a DataFrame and returns a (modified) DataFrame.

def select_ren_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only 'id' and all REN_* columns (sorted)."""
    ren_cols = sorted(col for col in df.columns if col.startswith("REN_"))
    return df[["id"] + ren_cols].copy()


def add_ren_count(df: pd.DataFrame) -> pd.DataFrame:
    """Add REN_COUNT: number of REN_1–REN_7 cells equal to 1."""
    ren_numeric_cols = ["REN_1", "REN_2", "REN_3", "REN_4", "REN_5", "REN_6", "REN_7"]
    df["REN_COUNT"] = df[ren_numeric_cols].apply(
        lambda row: sum(1 for val in row if val == "1" or val == 1),
        axis=1,
    )
    return df


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace '.' and empty strings with pd.NA."""
    return df.replace({"." : pd.NA, "": pd.NA})


# ── Wiring ───────────────────────────────────────────────────────────────────
# Add or remove steps here. Another agent only needs to define a step function
# and register it with pipeline.add_step().

pipeline = Pipeline(RAW_JSON, OUT_CSV)
pipeline.add_step(select_ren_columns)
pipeline.add_step(add_ren_count)
pipeline.add_step(clean_missing_values)
# pipeline.add_step(your_custom_step)   ← agent adds their step here

pipeline.run()
