# interactive_rule_of_law_map.py
# Fully interactive OWID-style choropleth with year slider

import io
import requests
import pandas as pd
import plotly.express as px

OWID_URL = "https://ourworldindata.org/grapher/rule-of-law-index.csv"
HTML_OUT = "rule_of_law_interactive.html"

# --- Load OWID grapher CSV ---
r = requests.get(OWID_URL, timeout=60)
r.raise_for_status()
df = pd.read_csv(io.StringIO(r.text))

# Normalize columns
df = df.rename(columns={"Entity": "entity", "Code": "code", "Year": "year"})
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# Detect the indicator column (OWID uses the slug as the column name)
meta = {"entity", "code", "year"}
value_cols = [c for c in df.columns if c.lower() not in meta]
if not value_cols:
    raise RuntimeError(f"No indicator column found. Columns: {list(df.columns)}")
indicator = value_cols[0]

# Tidy for plotting
df_long = df[["entity", "code", "year", indicator]].rename(columns={indicator: "value"})
df_long = df_long[df_long["code"].astype(str).str.len() == 3].copy()

# Set color axis range for consistency across years (index is 0..1)
color_range = [0, 1]

# A sharp, OWID-like blue scale (high contrast). Feel free to swap for "Viridis".
owid_blue_scale = [
    [0.00, "#eff3ff"],
    [0.20, "#c6dbef"],
    [0.40, "#9ecae1"],
    [0.60, "#6baed6"],
    [0.80, "#3182bd"],
    [1.00, "#08519c"],
]

fig = px.choropleth(
    df_long,
    locations="code",
    color="value",
    hover_name="entity",
    animation_frame="year",
    color_continuous_scale=owid_blue_scale,  # or "Viridis"
    range_color=color_range,
    projection="natural earth",
    title="Rule of Law Index — World Justice Project (via Our World in Data)",
)

# Layout polish (tight margins, readable colorbar)
fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=0),
    coloraxis_colorbar=dict(
        title="Index",
        ticks="outside",
        tickformat=".2f",
    ),
    geo=dict(
        showcountries=True,
        showcoastlines=False,
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    ),
)

# Better hover (clean & consistent)
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>Code: %{location}<br>Value: %{z:.3f}<extra></extra>"
)

# Ensure slider starts on the max available year
if len(fig.frames) > 0:
    latest_year = int(df_long["year"].max())
    # Find the frame index for latest_year
    frame_labels = [int(fr.name) for fr in fig.frames]
    if latest_year in frame_labels:
        start_idx = frame_labels.index(latest_year)
        fig.layout.sliders[0].active = start_idx

# Save and show
fig.write_html(HTML_OUT, include_plotlyjs="cdn", full_html=True)
print(f"Saved interactive map to: {HTML_OUT}")
fig.show()
