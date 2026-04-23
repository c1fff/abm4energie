from pathlib import Path
import json
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"

JSON_PATH = DATA_DIR / "survey1.json" # survey1 not survey


def load_survey_json(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected survey.json to contain a list of records.")

    df = pd.DataFrame(data)

    # Replace the survey's missing marker with proper NaN
    df = df.replace(".", pd.NA)

    return df


def main() -> None:
    df = load_survey_json(JSON_PATH)

    print("Loaded DataFrame")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print()

    print("First 5 rows:")
    print(df.head())
    print()

    print("Column names:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()