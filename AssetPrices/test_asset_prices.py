import pandas as pd
import pytest
import asset_prices

def test_returns_column_exists():
    df = pd.DataFrame({"Close": [100.0, 105.0, 102.0]})
    result = asset_prices.returns(df)
    assert "Returns" in result.columns

def test_returns_length_matches_input():
    df = pd.DataFrame({"Close": [100.0, 105.0, 102.0]})
    result = asset_prices.returns(df)
    assert len(result) == len(df)

def test_returns_values_are_correct():
    df = pd.DataFrame({"Close": [100.0, 105.0, 102.0]})
    result = asset_prices.returns(df)
    # The first return should be NaN, then (105-100)/100=0.05, then (102-105)/105≈-0.028571
    assert pd.isna(result["Returns"].iloc[0])
    assert pytest.approx(result["Returns"].iloc[1], rel=1e-6) == 0.05
    expected_third = -1 / 35  # (102 - 105) / 105
    assert pytest.approx(expected_third, rel=1e-6) == result["Returns"].iloc[2]

def test_returns_with_single_row():
    df = pd.DataFrame({"Close": [100.0]})
    result = asset_prices.returns(df)
    assert "Returns" in result.columns

def test_returns_raises_keyerror_if_close_missing():
    df = pd.DataFrame({"Open": [100.0, 102.0]})
    with pytest.raises(KeyError):
        asset_prices.returns(df)