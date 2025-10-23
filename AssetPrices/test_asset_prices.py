# AssetPrices/test_asset_prices.py
import pandas as pd
import pytest
from asset_prices import (
    fetch_data,
    calculate_daily_percent_change,
    calculate_std_dev,
)

@pytest.fixture
def fake_hist_df():
    return pd.DataFrame(
        {
            "Open":      [100.0, 102.0, 101.0, 107.0, 109.0],
            "High":      [103.0, 106.0, 104.0, 109.0, 112.0],
            "Low":       [ 99.0, 101.0, 100.0, 105.0, 108.0],
            "Close":     [100.0, 105.0, 102.0, 108.0, 110.0],
            "Adj Close": [ 99.0, 104.0, 101.0, 107.0, 109.0],
            "Volume":    [ 100,   200,   150,   180,   220],
        },
        index=pd.date_range("2024-01-01", periods=5, freq="D"),
    )

def test_fetch_data_returns_dataframe(fake_hist_df):
    def fake_downloader(ticker, period="1y"):
        return fake_hist_df.copy()

    df = fetch_data("AAPL", period="1mo", downloader=fake_downloader)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Close" in df.columns

def test_calculate_daily_percent_change(fake_hist_df):
    df = calculate_daily_percent_change(fake_hist_df.copy())
    assert "Daily % Change" in df.columns
    assert pd.isna(df['Daily % Change'].iloc[0])
    assert df['Daily % Change'].iloc[1:].apply(lambda x: isinstance(x, float)).all()

def test_calculate_std_dev(fake_hist_df):
    df = calculate_daily_percent_change(fake_hist_df.copy())
    std_dev = calculate_std_dev(df)
    assert isinstance(std_dev, float)
    assert std_dev > 0