# 📈 AssetPrices

A simple Python project for analysing stock price data using **yfinance**, **pandas**, and **matplotlib**.  
It downloads historical prices, computes daily returns, and generates basic visualisations.

---

## Features

- Downloads **1 year** of daily price data for a chosen ticker
- Cleans the dataset (drops missing values)
- Plots:
  - Closing price over time  
  - Daily percentage change  
- Computes:
  - Daily percentage returns (`Close.pct_change()`)
  - Standard deviation of daily % changes
- Includes a **unit-tested `returns()` helper function**

---

## File Structure
```
AssetPrices/
│── asset_prices.py        # Main script + returns() helper
│── test_asset_prices.py   # Unit tests for returns()
│── README.md              # Project documentation
```

---

## Running Tests

From the repository root:

```bash
pytest AssetPrices -q