# interactive_rule_of_law_map.py
import io
import requests
import pandas as pd
import plotly.express as px

YEAR = 2022
OWID_URL = "https://ourworldindata.org/grapher/rule-of-law-index.csv"

r = requests.get(OWID_URL, timeout=60)
r.raise_for_status()
df = pd.read_csv(io.StringIO(r.text))

df_year = df[df["Year"] == YEAR].copy()

fig = px.choropleth(
    df_year,
    locations="Code",            # ISO-3 country codes
    hover_name="Entity",
    color_continuous_scale="Viridis",
    projection="natural earth",
    title=f"Rule of Law Index — {YEAR}",
)
fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=0),
    coloraxis_colorbar=dict(title="Index"),
)
fig.show()
