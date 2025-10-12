# world_rule_of_law_map.py
# Recreates a world choropleth for OWID's "Rule of Law Index"
# Save as PNG/SVG and choose any year present in the dataset.

import io
import textwrap
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import requests

warnings.filterwarnings("ignore", category=UserWarning)

# -------------------------
# Config
# -------------------------
YEAR = 2022             # <- change this to your target year
OUTFILE = Path(f"rule_of_law_{YEAR}.png")
TITLE = f"Rule of Law Index — {YEAR}"
SUBTITLE = "Source: World Justice Project via Our World in Data"
CAPTION = "Note: Higher is better. Gray = no data."

# -------------------------
# Load OWID dataset (detect value column automatically)
# -------------------------
OWID_URL = "https://ourworldindata.org/grapher/rule-of-law-index.csv"

r = requests.get(OWID_URL, timeout=60)
r.raise_for_status()
df = pd.read_csv(io.StringIO(r.text))

# Normalize column names and detect indicator column
df = df.rename(columns={"Entity": "entity", "Code": "code", "Year": "year"})
df["year"] = pd.to_numeric(df["year"], errors="coerce")

meta_cols = {"entity", "code", "year"}
value_cols = [c for c in df.columns if c.lower() not in meta_cols]
if not value_cols:
    raise RuntimeError(f"No indicator column found. Columns: {list(df.columns)}")
indicator_col = value_cols[0]

# Keep chosen year and tidy
df_year = (
    df[df["year"] == YEAR][["code", indicator_col]]
    .rename(columns={indicator_col: "value"})
    .copy()
)

# Ensure valid 3-letter codes
df_year = df_year[df_year["code"].astype(str).str.len() == 3].copy()

# -------------------------
# Load world geometries (Natural Earth 1:110m Admin-0 Countries)
# -------------------------
NE_URL = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(NE_URL)

# Pick a reliable ISO3 column present in the file
iso_candidates = ["ISO_A3", "ADM0_A3", "ISO_A3_EH"]
iso_col = next((c for c in iso_candidates if c in world.columns), None)
if iso_col is None:
    raise RuntimeError(f"None of the expected ISO3 columns found: {iso_candidates}")

# Some Natural Earth rows use '-99' for contested areas; drop those for ISO3 join
world = world[world[iso_col].notna() & (world[iso_col] != "-99")].copy()

# -------------------------
# Join on ISO3 codes
# -------------------------
gdf = world.merge(df_year, left_on=iso_col, right_on="code", how="left")

# -------------------------
# Plot
# -------------------------
fig = plt.figure(figsize=(14, 7), dpi=150)
ax = plt.gca()

gdf.plot(
    column="value",
    cmap="viridis",           # perceptual colormap
    linewidth=0.2,
    edgecolor="white",
    legend=True,
    missing_kwds={"color": "#eeeeee", "hatch": "///", "label": "No data"},
    ax=ax
)

# Tidy up frame
ax.set_axis_off()

# Titles
plt.title(TITLE, fontsize=16, weight="bold", loc="left", pad=10)
wrapped = "\n".join(textwrap.wrap(SUBTITLE, width=90))
plt.annotate(
    wrapped,
    xy=(0.005, 0.02),
    xycoords="figure fraction",
    ha="left",
    va="bottom",
    fontsize=9,
    color="#444",
)
plt.annotate(
    CAPTION,
    xy=(0.995, 0.02),
    xycoords="figure fraction",
    ha="right",
    va="bottom",
    fontsize=8,
    color="#666",
)

# Save
fig.savefig(OUTFILE, bbox_inches="tight")
fig.savefig(OUTFILE.with_suffix(".svg"), bbox_inches="tight")
print(f"Saved: {OUTFILE.resolve()}")
print(f"Saved: {OUTFILE.with_suffix('.svg').resolve()}")
