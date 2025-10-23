# 📈 Asset Prices Analysis

This activity analyses one year of historical stock prices for a company listed on the **NASDAQ**.  
It demonstrates key data analysis techniques including data retrieval, cleaning, visualisation, and calculation of volatility metrics.

---

## 🧠 Overview

The project downloads one year of daily price data for a chosen company (e.g. **NVIDIA – NVDA**) using the Yahoo Finance API via the `yfinance` library.  
The data is then cleaned and visualised to show:

- **Closing Price vs. Date**
- **Daily Percentage Change vs. Date**

Finally, the **standard deviation of daily percentage changes** is calculated to measure the stock’s volatility.

---

## ⚙️ Features

- Download and clean historical NASDAQ price data  
- Plot **Closing Price** over time  
- Calculate and visualise **Daily % Change**  
- Compute the **Standard Deviation** of daily returns  
- Includes **automated unit tests** for reliability

---

## 🧩 File Structure

```text
AssetPrices/
│
├── asset_prices.py           # Main analysis script
├── test_asset_prices.py      # Unit tests (pytest)
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview

## 🧩 How This Activity Demonstrates the KSBs

### 🧠 Knowledge

- **K54 – Analyse and interpret complex information from diverse datasets**  
  This activity required importing and processing a real-world financial dataset from the Yahoo Finance API.  
  Cleaning, structuring, and analysing time-series data helped demonstrate the ability to **critically evaluate** complex external data sources and extract meaningful insights about market behaviour.

- **K59 – Apply data analytics to improve organisational processes and outputs**  
  By calculating and interpreting daily percentage changes and volatility (standard deviation), the analysis highlights how **data-driven insights** can inform business decisions such as risk assessment, investment strategy, and performance monitoring — directly linking analytics to organisational outcomes.

---

### 🧰 Skills

- **S49 – Apply data analysis to drive improvements for business problems**  
  The project replicates a common financial analysis scenario — understanding stock performance through descriptive analytics.  
  The workflow of downloading, cleaning, analysing, and visualising the data shows a full analytical process that could support better business or investment decisions.

- **S50 – Communicate and visualise data effectively**  
  Using `matplotlib`, the project produces clear, informative charts (Closing Price vs. Date, and Daily % Change vs. Date).  
  These visualisations allow non-technical stakeholders to quickly grasp performance trends, demonstrating **data storytelling** and presentation skills.

- **S55 – Analyse large datasets using standard tools and methods**  
  The project uses **industry-standard Python libraries** (`pandas`, `matplotlib`, `yfinance`) for data wrangling, transformation, and analysis.  
  This reflects practical competence in the use of modern analytical tools to process and interpret large, structured datasets.

---

### 💡 Summary

Overall, this activity integrates **technical competence**, **analytical reasoning**, and **clear communication**, addressing all required KSBs from the **DAT5501: Analysis, Software and Career Practice** module through an authentic, data-driven workflow.