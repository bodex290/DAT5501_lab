import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

TICKER = "NVDA"  # Nvidia Corporation

def returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'Returns' column with simple daily percentage returns
    based on the 'Close' price.

    The first row will be NaN because there is no previous day to compare to.
    """
    if "Close" not in df.columns:
        raise KeyError("DataFrame must contain a 'Close' column")

    result = df.copy()
    result["Returns"] = result["Close"].pct_change()
    return result

def download_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Download historical price data for a given ticker and period.
    """
    data = yf.download(ticker, period=period)
    return data.dropna()

def plot_series(x, y, title, xlabel, ylabel, label):
    """
    Plot a time series.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    ticker = TICKER

    # Download and clean data
    data = download_data(ticker)

    # Plot closing price
    plot_series(
        data.index,
        data["Close"],
        f"{ticker} Closing Price (1 Year)",
        "Date",
        "Price (USD)",
        "Closing Price"
    )

    # Calculate and plot daily percentage change
    data = returns(data)
    data["Daily % Change"] = data["Returns"] * 100

    plot_series(
        data.index,
        data["Daily % Change"],
        f"{ticker} Daily Percentage Change (1 Year)",
        "Date",
        "Percentage Change (%)",
        "Daily % Change"
    )

    # Calculate and print standard deviation
    std_dev = data["Daily % Change"].std()
    print(f"Standard deviation of daily % changes for {ticker}: {std_dev:.2f}%")

if __name__ == "__main__":
    main()