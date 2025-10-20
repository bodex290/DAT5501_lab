# duration_from_csv.py
from pathlib import Path
import sys
import numpy as np
import pandas as pd

def days_from_csv(csv_path: str | Path) -> pd.DataFrame:
    p = Path(csv_path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p}")

    df = pd.read_csv(p)              # expects a header "date"
    # Parse to pandas datetime (ns precision)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="raise")

    # Convert to NumPy daily precision for integer day diffs
    dates_d = df["date"].to_numpy(dtype="datetime64[D]")
    today_d = np.datetime64("today", "D")

    df["days_ago"] = (today_d - dates_d).astype(int)
    return df[["date", "days_ago"]]

if __name__ == "__main__":
    csv_arg = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path("random_dates_fixed.csv")
    out = days_from_csv(csv_arg)
    print(out.to_string(index=False))