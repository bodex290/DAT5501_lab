# ============================================
#  US Primary Election Vote Analysis (2016)
#  - Auto-detect top 2 candidates by total votes
#  - Weighted state-level fractions
#  - Histogram + Scatter comparison
# ============================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# 1) Load CSV (semicolon-safe)
# -----------------------------
# Adjust this if your file lives elsewhere
csv_name = "US-2016-primary (1).csv"

# Try local dir first; if not, try script dir
here = Path.cwd()
script_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()

candidates_paths = [
    here / csv_name,
    script_dir / csv_name,
]

csv_path = None
for p in candidates_paths:
    if p.exists():
        csv_path = p
        break

if csv_path is None:
    raise FileNotFoundError(
        f"Couldn't find {csv_name}. Tried:\n - {candidates_paths[0]}\n - {candidates_paths[1]}"
    )

# Read with correct delimiter (dataset uses ';')
df = pd.read_csv(csv_path, sep=';')

# Quick sanity checks
required_cols = {"state", "party", "candidate", "votes", "fraction_votes"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing expected columns: {missing}. Found: {list(df.columns)}")

# Ensure types
df["votes"] = pd.to_numeric(df["votes"], errors="coerce")
df["fraction_votes"] = pd.to_numeric(df["fraction_votes"], errors="coerce")
df = df.dropna(subset=["votes", "fraction_votes"])

# -------------------------------------------------------
# 2) Pick top 2 candidates (by total votes across rows)
# -------------------------------------------------------
totals_by_candidate = df.groupby("candidate", as_index=False)["votes"].sum()
totals_by_candidate = totals_by_candidate.sort_values("votes", ascending=False)
if len(totals_by_candidate) < 2:
    raise ValueError("Dataset does not contain at least two candidates.")

top1, top2 = totals_by_candidate.iloc[0]["candidate"], totals_by_candidate.iloc[1]["candidate"]
print("Top candidates by total votes:")
print(totals_by_candidate.head(10).to_string(index=False))
print(f"\nSelected for plots:\n  1) {top1}\n  2) {top2}\n")

# ------------------------------------------------------------------
# 3) Compute state-level fractions (weighted by total votes in state)
# ------------------------------------------------------------------
# For each row: total_votes_in_race = candidate_votes / fraction_votes
df["total_votes_in_row"] = df["votes"] / df["fraction_votes"]

def state_level_fraction(candidate_name: str) -> pd.Series:
    cdf = df[df["candidate"] == candidate_name].copy()
    # Aggregate by state: sum(candidate_votes) / sum(total_votes_in_row)
    by_state = cdf.groupby("state").agg(
        candidate_votes=("votes", "sum"),
        total_votes=("total_votes_in_row", "sum"),
    )
    by_state["state_fraction"] = by_state["candidate_votes"] / by_state["total_votes"]
    return by_state["state_fraction"]

state_frac_top1 = state_level_fraction(top1)
state_frac_top2 = state_level_fraction(top2)

# -----------------------------------------------
# 4) Plot histogram for the top candidate (per state)
# -----------------------------------------------
plt.figure(figsize=(9,6))
plt.hist(state_frac_top1.dropna(), bins=20, edgecolor="black")
plt.title(f"State-level Vote Fraction Distribution: {top1}")
plt.xlabel("Vote fraction (0–1)")
plt.ylabel("Number of states")
plt.grid(axis="y", alpha=0.6)
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# 5) Extra: Compare top two candidates (state-by-state)
# ---------------------------------------------------
comparison = (
    pd.DataFrame({top1: state_frac_top1, top2: state_frac_top2})
    .dropna()  # only states where both are present
)

plt.figure(figsize=(9,7))
plt.scatter(comparison[top1], comparison[top2], alpha=0.7)
for st, row in comparison.iterrows():
    # Optional: label a few extreme points (comment out if cluttered)
    if (row[top1] > 0.75 or row[top2] > 0.75) or (abs(row[top1]-row[top2]) > 0.5):
        plt.annotate(st, (row[top1], row[top2]), fontsize=8, xytext=(3,3), textcoords="offset points")

plt.title(f"State-level Vote Fractions: {top1} vs {top2}")
plt.xlabel(f"{top1} fraction")
plt.ylabel(f"{top2} fraction")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# 6) (Optional) Save figures
# ---------------------------------------------------
# out_dir = script_dir / "figures"
# out_dir.mkdir(exist_ok=True)
# plt.figure(figsize=(9,6))
# plt.hist(state_frac_top1.dropna(), bins=20, edgecolor="black")
# plt.title(f"State-level Vote Fraction Distribution: {top1}")
# plt.xlabel("Vote fraction (0–1)")
# plt.ylabel("Number of states")
# plt.grid(axis="y", alpha=0.6)
# plt.tight_layout()
# plt.savefig(out_dir / f"hist_{top1.replace(' ','_')}.png", dpi=150)

# plt.figure(figsize=(9,7))
# plt.scatter(comparison[top1], comparison[top2], alpha=0.7)
# plt.title(f"State-level Vote Fractions: {top1} vs {top2}")
# plt.xlabel(f"{top1} fraction")
# plt.ylabel(f"{top2} fraction")
# plt.grid(True, linestyle="--", alpha=0.6)
# plt.tight_layout()
# plt.savefig(out_dir / f"scatter_{top1.replace(' ','_')}_vs_{top2.replace(' ','_')}.png", dpi=150)