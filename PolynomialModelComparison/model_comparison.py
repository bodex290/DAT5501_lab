import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Load data and select UK
# -----------------------------
df = pd.read_csv("co-emissions-per-capita.csv")

uk = df[df["Entity"] == "United Kingdom"].copy()

# Last 100 years relative to the latest UK year in the file
max_year = uk["Year"].max()
uk_100 = uk[uk["Year"] >= max_year - 100]

years = uk_100["Year"].values
vals = uk_100["Annual CO₂ emissions (per capita)"].values

# -----------------------------
# 2. Train / test split
#    Train: all but last 10 years
#    Test: last 10 years (for forecast evaluation)
# -----------------------------
train_mask = years <= max_year - 10
test_mask = years > max_year - 10

x_train, y_train = years[train_mask], vals[train_mask]
x_test, y_test = years[test_mask], vals[test_mask]

# Centre years for numerical stability
t0 = x_train.mean()
t_train = x_train - t0
t_test = x_test - t0

# -----------------------------
# 3. Fit polynomials of order 1–9
#    and compute chi2/DOF, BIC, and forecast RMSE
# -----------------------------
orders = range(1, 10)
chi2_dof = []
bics = []
test_rmse = []

n = len(t_train)

for m in orders:
    k = m + 1  # number of parameters

    # Fit polynomial of degree m
    coeffs = np.polyfit(t_train, y_train, deg=m)

    # Predictions on training set
    yhat_train = np.polyval(coeffs, t_train)
    rss = np.sum((y_train - yhat_train) ** 2)  # residual sum of squares

    # Chi-squared per degree of freedom
    chi2_dof.append(rss / (n - k))

    # Bayesian Information Criterion (BIC)
    bics.append(n * np.log(rss / n) + k * np.log(n))

    # Predictions on test set (last 10 years)
    yhat_test = np.polyval(coeffs, t_test)
    test_rmse.append(np.sqrt(np.mean((y_test - yhat_test) ** 2)))

# -----------------------------
# 4. Plots
# -----------------------------

# (a) Chi²/DOF and BIC vs polynomial order
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].plot(orders, chi2_dof, marker="o")
ax[0].set_title("Chi² per DOF vs Polynomial Order")
ax[0].set_xlabel("Polynomial order")
ax[0].set_ylabel("Chi²/DOF")

ax[1].plot(orders, bics, marker="o")
ax[1].set_title("BIC vs Polynomial Order")
ax[1].set_xlabel("Polynomial order")
ax[1].set_ylabel("BIC")

plt.tight_layout()
plt.show()

# (b) Forecast RMSE vs polynomial order
plt.figure(figsize=(6, 4))
plt.plot(orders, test_rmse, marker="o")
plt.title("Forecast RMSE (Last 10 Years) vs Polynomial Order")
plt.xlabel("Polynomial order")
plt.ylabel("RMSE")
plt.tight_layout()
plt.show()




# ==========================================================
# NEW: Polynomial fits comparison plot (like the example)
# ==========================================================

# We already have:
#   years  -> all years in the last ~100 years
#   vals   -> CO2 per capita values
#   max_year -> latest year in the dataset

# 1. Define fit limit and training subset (same as before)
fit_limit_year = max_year - 10
train_mask = years <= fit_limit_year

x_train = years[train_mask]
y_train = vals[train_mask]

# 2. Centre years for numerical stability
t0 = x_train.mean()
t_train = x_train - t0

# 3. Define a smooth year grid for plotting curves
years_plot = np.linspace(years.min(), years.max(), 500)
t_plot = years_plot - t0

# 4. Choose which polynomial orders to show
orders_to_plot = [2, 3, 9]   # change to [6, 11, 20] etc if you want

styles = {
    2: ("Polynomial order 2", "tab:green", "dashed"),
    3: ("Polynomial order 3", "tab:orange", "solid"),
    9: ("Polynomial order 9", "tab:red", "dotted"),
}

# 5. Fit each polynomial and evaluate over full range
fits = {}
for m in orders_to_plot:
    coeffs = np.polyfit(t_train, y_train, deg=m)
    y_plot = np.polyval(coeffs, t_plot)
    fits[m] = y_plot

# 6. Make the figure
plt.figure(figsize=(10, 6))

# Observed data (points)
plt.scatter(years, vals, s=15, color="tab:blue",
            label="Observed data")

# Polynomial curves
for m in orders_to_plot:
    label, color, ls = styles[m]
    y_plot = fits[m]
    plt.plot(years_plot, y_plot, linestyle=ls, color=color, linewidth=2,
             label=label)

# Vertical dashed line at fit limit
plt.axvline(fit_limit_year, color="k", linestyle="--", linewidth=1.5,
            label=f"Fit limit ({fit_limit_year})")

# Labels, title, legend
plt.xlabel("Year")
plt.ylabel("CO₂ emissions per capita (tonnes/person)")
plt.title("UK CO₂ Emissions per Capita\nPolynomial Fit Comparison")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()