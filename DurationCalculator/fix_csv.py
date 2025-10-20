# fix_csv.py
from pathlib import Path
import pandas as pd

in_path = Path("random_dates.csv")
out_path = Path("random_dates_fixed.csv")

# Read file ignoring malformed lines
dates = []
with open(in_path, "r") as f:
    for line in f:
        line = line.strip()
        if line and len(line) == 10 and line.count("-") == 2:
            dates.append(line)

# Save clean version with header
pd.DataFrame({"date": dates}).to_csv(out_path, index=False)
print(f"✅ Cleaned CSV saved as: {out_path}")