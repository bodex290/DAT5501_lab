# ============================================
#  US Primary Election Vote Analysis (2016)
#  - Exposes helpers for unit tests
#  - Runs analysis only when executed as a script
# ============================================

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Helpers (imported by tests)
# -----------------------------

def load_election_csv(path: str | Path) -> pd.DataFrame:
    """Load the CSV, handling semicolon-separated data."""
    return pd.read_csv(path, sep=';')

def top_two_candidates(df: pd.DataFrame) -> tuple[str, str]:
    """Return names of top-2 candidates by total votes (descending)."""
    totals = df.groupby("candidate", as_index=False)["votes"].sum()
    if len(totals) < 2:
        raise ValueError("Need at least two candidates")
    winners = totals.sort_values("votes", ascending=False)["candidate"].tolist()
    return winners[0], winners[1]

def compute_state_fraction(df: pd.DataFrame, candidate_name: str) -> pd.Series:
    """
    Weighted state-level vote fraction for a candidate:
      sum(candidate_votes) / sum(total_votes_in_row),
    where total_votes_in_row = votes / fraction_votes.
    """
    work = df.copy()
    work["votes"] = pd.to_numeric(work["votes"], errors="coerce")
    work["fraction_votes"] = pd.to_numeric(work["fraction_votes"], errors="coerce")
    work = work.dropna(subset=["votes", "fraction_votes"])

    work["total_votes_in_row"] = work["votes"] / work["fraction_votes"]
    cdf = work[work["candidate"] == candidate_name]
    agg = cdf.groupby("state").agg(
        candidate_votes=("votes", "sum"),
        total_votes=("total_votes_in_row", "sum"),
    )
    agg["state_fraction"] = agg["candidate_votes"] / agg["total_votes"]
    return agg["state_fraction"]

def compare_two_candidates(df: pd.DataFrame, cand1: str, cand2: str) -> pd.DataFrame:
    """Return a state-indexed DataFrame with columns [cand1, cand2] of state fractions."""
    f1 = compute_state_fraction(df, cand1)
    f2 = compute_state_fraction(df, cand2)
    return pd.DataFrame({cand1: f1, cand2: f2}).dropna()

# -----------------------------
# Script-only plotting workflow
# -----------------------------

def main() -> None:
    # Resolve CSV path near this script or CWD
    csv_name = "US-2016-primary (1).csv"
    script_dir = Path(__file__).resolve().parent
    candidates_paths = [
        Path.cwd() / csv_name,
        script_dir / csv_name,
    ]
    csv_path = next((p for p in candidates_paths if p.exists()), None)
    if csv_path is None:
        raise FileNotFoundError(
            f"Couldn't find {csv_name}. Tried:\n - {candidates_paths[0]}\n - {candidates_paths[1]}"
        )

    # Load data
    df = load_election_csv(csv_path)

    # Quick sanity check for expected columns
    required_cols = {"state", "party", "candidate", "votes", "fraction_votes"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {missing}. Found: {list(df.columns)}")

    # Pick top two candidates
    top1, top2 = top_two_candidates(df)

    # Compute state-level fractions
    state_frac_top1 = compute_state_fraction(df, top1)
    state_frac_top2 = compute_state_fraction(df, top2)

    # Plot histogram for top candidate
    plt.figure(figsize=(9,6))
    plt.hist(state_frac_top1.dropna(), bins=20, edgecolor="black")
    plt.title(f"State-level Vote Fraction Distribution: {top1}")
    plt.xlabel("Vote fraction (0–1)")
    plt.ylabel("Number of states")
    plt.grid(axis="y", alpha=0.6)
    plt.tight_layout()
    plt.show()

    # Scatter comparison
    comparison = compare_two_candidates(df, top1, top2)
    plt.figure(figsize=(9,7))
    plt.scatter(comparison[top1], comparison[top2], alpha=0.7)
    plt.title(f"State-level Vote Fractions: {top1} vs {top2}")
    plt.xlabel(f"{top1} fraction")
    plt.ylabel(f"{top2} fraction")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()