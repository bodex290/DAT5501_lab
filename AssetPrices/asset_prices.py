# asset_prices.py
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Download and clean historical price data for a NASDAQ-listed company."""
    data = yf.download(ticker, period=period)
    return data.dropna()

def calculate_daily_percent_change(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily percentage change."""
    data['Daily % Change'] = data['Close'].pct_change() * 100
    return data

def calculate_std_dev(data: pd.DataFrame) -> float:
    """Return standard deviation of daily percentage changes."""
    return round(data['Daily % Change'].std(), 2)

def plot_prices(data: pd.DataFrame, ticker: str):
    """Plot closing price vs date."""
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
    """Plot daily percentage change vs date."""
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
    ticker = "NVDA"
    df = fetch_data(ticker)
    df = calculate_daily_percent_change(df)
    std_dev = calculate_std_dev(df)
    print(f"Standard deviation of daily % changes for {ticker}: {std_dev}%")
    plot_prices(df, ticker)
    plot_percent_change(df, ticker)