# Polynomial Model Selection on UK CO₂ Emissions per Capita

This mini-project explores **model selection** using a real global-trend dataset:  
annual **CO₂ emissions per capita** for the **United Kingdom** over the last ~100 years.

We:

- Fit **polynomial models** of orders **1–9** to historical data.
- Hold out the **most recent 10 years** as a “future” test set.
- Compare models using:
  - **χ² per degree of freedom (χ²/DOF)**  
  - **Bayesian Information Criterion (BIC)**
  - **Forecast error (RMSE) on the last 10 years**
- Visualise these metrics as functions of polynomial order.

---

## Dataset

File: `co-emissions-per-capita.csv`

Columns used:

- `Entity` – country name (we use **United Kingdom** only)
- `Code` – country code
- `Year` – calendar year
- `Annual CO₂ emissions (per capita)` – tonnes of CO₂ per person per year

From this file we:

1. Filter `Entity == "United Kingdom"`.
2. Take the **last ~100 years** of data (relative to the latest UK year available).
3. Use the last **10 years** as a test set for forecasting.

---

## Method

All analysis is done in Python using **NumPy**, **Pandas**, and **Matplotlib**.

1. **Load and filter data**
   - Read `co-emissions-per-capita.csv`.
   - Keep only rows for `"United Kingdom"`.
   - Restrict to the most recent 100 years.

2. **Train / test split**
   - Training set: all years up to **(max_year − 10)**.
   - Test set: the **last 10 years** (held out for evaluation).

3. **Time re-centering**
   - For numerical stability, define  
     \[
     t = \text{year} - \bar{t}_{\text{train}}
     \]
   - Polynomials are fitted in `t` rather than the raw year.

4. **Polynomial fitting (orders 1–9)**
   - For each order \( m = 1, 2, \dots, 9 \):
     - Fit a polynomial of degree `m` using `numpy.polyfit`.
     - Compute predictions on the training set, \( \hat{y}_{\text{train}} \).
     - Compute **Residual Sum of Squares (RSS)**:
       \[
       \text{RSS} = \sum (y_{\text{train}} - \hat{y}_{\text{train}})^2
       \]

5. **Metrics**

   For each order \( m \) with \( k = m + 1 \) parameters and \( n \) training points:

   - **χ² per degree of freedom**
     \[
     \chi^2/\text{DOF} = \frac{\text{RSS}}{n - k}
     \]

   - **Bayesian Information Criterion (BIC)**
     \[
     \text{BIC} = n \ln\left(\frac{\text{RSS}}{n}\right) + k \ln(n)
     \]

   - **Forecast RMSE on last 10 years**
     - Predict the test set years using the fitted polynomial.
     - Compute
       \[
       \text{RMSE} = \sqrt{\frac{1}{n_{\text{test}}} \sum (y_{\text{test}} - \hat{y}_{\text{test}})^2}
       \]

6. **Plots produced**

   - **Chi² per DOF vs polynomial order**
   - **BIC vs polynomial order**
   - **Forecast RMSE (last 10 years) vs polynomial order**

---

## How to Run

1. Install dependencies:

   ```bash
   pip install numpy pandas matplotlib