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

# 1. Choose a company — e.g., Nvidia (NVDA)
def main ():
    ticker = TICKER

    # 2. Download 1 year of daily historical prices
    data = yf.download(ticker, period="1y")

    # 3. Clean dataset (drop missing values)
    data = data.dropna()

    # 4. Plot closing price vs. date
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Close'], label="Closing Price")
    plt.title(f"{ticker} Closing Price (1 Year)")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 5. Extra: Calculate daily percentage change
    data['Daily % Change'] = data['Close'].pct_change() * 100

    # 6. Plot daily percentage change vs. date
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Daily % Change'], label="Daily % Change")
    plt.title(f"{ticker} Daily Percentage Change (1 Year)")
    plt.xlabel("Date")
    plt.ylabel("Percentage Change (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 7. Extra extra: Calculate standard deviation
    std_dev = data['Daily % Change'].std()
    print(f"Standard deviation of daily % changes for {ticker}: {std_dev:.2f}%")

if __name__ == "__main__":
    main()