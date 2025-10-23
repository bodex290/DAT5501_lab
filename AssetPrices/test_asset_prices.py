# test_asset_prices.py
import pytest
import pandas as pd
from asset_prices import (
    fetch_data,
    calculate_daily_percent_change,
    calculate_std_dev
)

@pytest.fixture
def mock_data():
    """Mock dataset for testing percentage change and std deviation."""
    return pd.DataFrame({
        "Close": [100, 105, 102, 108, 110]
    })

def test_fetch_data_returns_dataframe():
    """Check that fetch_data returns a pandas DataFrame."""
    df = fetch_data("AAPL", period="1mo")
    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns
    assert not df.empty

def test_calculate_daily_percent_change(mock_data):
    """Ensure percent change column is correctly calculated."""
    df = calculate_daily_percent_change(mock_data.copy())
    assert "Daily % Change" in df.columns
    # First value should be NaN since there's no previous day
    assert pd.isna(df['Daily % Change'].iloc[0])
    # Remaining values should be numeric
    assert df['Daily % Change'].iloc[1:].apply(lambda x: isinstance(x, float)).all()

def test_calculate_std_dev(mock_data):
    """Check that standard deviation returns a float value."""
    df = calculate_daily_percent_change(mock_data.copy())
    std_dev = calculate_std_dev(df)
    assert isinstance(std_dev, float)
    assert std_dev > 0