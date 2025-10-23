import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # ensure no GUI needed for any plotting code

import pandas as pd
import pytest

# Import the helpers from your module
from us_election import (
    load_election_csv,
    top_two_candidates,
    compute_state_fraction,
    compare_two_candidates,
)

# ---------- Fixtures ----------

@pytest.fixture
def sample_df() -> pd.DataFrame:
    """
    Construct a tiny, consistent dataset with two states and two candidates.
    Fractions are per-row shares: fraction_votes = votes / total_votes_in_row.
    """
    # StateA totals per county: 100 and 40 (so state total = 140)
    #  - Candidate A: 60 (0.6 of 100), 20 (0.5 of 40) -> total A = 80
    #  - Candidate B: 40 (0.4 of 100), 20 (0.5 of 40) -> total B = 60
    #  => state_fraction(A) = 80 / 140 = 4/7 ≈ 0.57142857
    data = [
        # state, state_abbreviation, county, fips, party, candidate, votes, fraction_votes
        ("StateA", "SA", "County1", 1, "PartyX", "Candidate A", 60, 0.60),
        ("StateA", "SA", "County1", 1, "PartyX", "Candidate B", 40, 0.40),
        ("StateA", "SA", "County2", 2, "PartyX", "Candidate A", 20, 0.50),
        ("StateA", "SA", "County2", 2, "PartyX", "Candidate B", 20, 0.50),

        # StateB totals per county: 200 and 100 (state total = 300)
        #  - Candidate A: 120 (0.6 of 200),  40 (0.4 of 100) -> 160
        #  - Candidate B:  80 (0.4 of 200),  60 (0.6 of 100) -> 140
        #  => state_fraction(A) = 160 / 300 = 0.53333333
        ("StateB", "SB", "County3", 3, "PartyX", "Candidate A", 120, 0.60),
        ("StateB", "SB", "County3", 3, "PartyX", "Candidate B",  80, 0.40),
        ("StateB", "SB", "County4", 4, "PartyX", "Candidate A",  40, 0.40),
        ("StateB", "SB", "County4", 4, "PartyX", "Candidate B",  60, 0.60),
    ]
    cols = ["state", "state_abbreviation", "county", "fips", "party",
            "candidate", "votes", "fraction_votes"]
    df = pd.DataFrame(data, columns=cols)
    df["votes"] = pd.to_numeric(df["votes"])
    df["fraction_votes"] = pd.to_numeric(df["fraction_votes"])
    return df


# ---------- Tests ----------

def test_load_election_csv_semicolon(tmp_path: Path):
    """CSV should be parsed with semicolon delimiter into separate columns."""
    csv_text = (
        "state;state_abbreviation;county;fips;party;candidate;votes;fraction_votes\n"
        "Vermont;VT;Sutton;95000197;Republican;John Kasich;123;0.25\n"
        "Vermont;VT;Tunbridge;95000204;Republican;Donald Trump;246;0.50\n"
    )
    p = tmp_path / "sample.csv"
    p.write_text(csv_text, encoding="utf-8")

    df = load_election_csv(p)
    assert list(df.columns) == [
        "state", "state_abbreviation", "county", "fips",
        "party", "candidate", "votes", "fraction_votes"
    ]
    assert len(df) == 2
    assert df.loc[0, "candidate"] == "John Kasich"
    assert pd.api.types.is_numeric_dtype(df["votes"])
    assert pd.api.types.is_numeric_dtype(df["fraction_votes"])


def test_top_two_candidates_order(sample_df: pd.DataFrame):
    """Top-2 candidates should be ordered by total votes descending."""
    # Totals:
    # Candidate A: 60+20+120+40 = 240
    # Candidate B: 40+20+80+60  = 200
    c1, c2 = top_two_candidates(sample_df)
    assert c1 == "Candidate A"
    assert c2 == "Candidate B"


def test_compute_state_fraction_weighted(sample_df: pd.DataFrame):
    """
    Weighted state fraction should match manual calculation:
      StateA: A = 80/140 = 4/7 ≈ 0.57142857
      StateB: A = 160/300 ≈ 0.53333333
    """
    fracA = compute_state_fraction(sample_df, "Candidate A")
    assert pytest.approx(fracA.loc["StateA"], rel=1e-6, abs=1e-9) == 4/7
    assert pytest.approx(fracA.loc["StateB"], rel=1e-6, abs=1e-9) == 160/300


def test_compare_two_candidates_alignment(sample_df: pd.DataFrame):
    """Comparison DataFrame should include both columns and only common states."""
    comp = compare_two_candidates(sample_df, "Candidate A", "Candidate B")
    assert list(comp.columns) == ["Candidate A", "Candidate B"]
    # Both candidates appear in both states -> 2 rows
    assert set(comp.index.tolist()) == {"StateA", "StateB"}
    # Values are within [0,1]
    assert ((comp >= 0) & (comp <= 1)).to_numpy().all()

#empyty line