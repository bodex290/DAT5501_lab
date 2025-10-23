# AssetPrices/asset_prices.py
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data(ticker: str, period: str = "1y", downloader=None) -> pd.DataFrame:
    """
    Download and clean historical price data.
    Pass a `downloader` function with signature (ticker, period) -> DataFrame.
    This avoids importing yfinance at import-time (important for Py3.8 CI).
    """
    if downloader is None:
        raise RuntimeError("No downloader provided. Pass a function like yfinance.download")
    data = downloader(ticker, period=period)
    return data.dropna()

def calculate_daily_percent_change(data: pd.DataFrame) -> pd.DataFrame:
    data['Daily % Change'] = data['Close'].pct_change() * 100
    return data

def calculate_std_dev(data: pd.DataFrame) -> float:
    return round(data['Daily % Change'].std(), 2)

def plot_prices(data: pd.DataFrame, ticker: str):
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Close'], label='Closing Price')
    plt.title(f"{ticker} Closing Price (1 Year)")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_percent_change(data: pd.DataFrame, ticker: str):
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Daily % Change'], label='Daily % Change')
    plt.title(f"{ticker} Daily Percentage Change (1 Year)")
    plt.xlabel("Date")
    plt.ylabel("Percentage Change (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Import yfinance only when running locally, not during test import
    import yfinance as yf
    ticker = "NVDA"
    df = fetch_data(ticker, downloader=yf.download)
    df = calculate_daily_percent_change(df)
    std_dev = calculate_std_dev(df)
    print(f"Standard deviation of daily % changes for {ticker}: {std_dev}%")
    plot_prices(df, ticker)
    plot_percent_change(df, ticker)