"""Streamlit web app: explore earthquakes in Chile with filters."""

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

VALPARAISO = (-33.0472, -71.6127)

st.set_page_config(page_title="Earthquakes in Chile", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/earthquakes_chile.csv", parse_dates=["time"])
    df["time"] = df["time"].dt.tz_convert("America/Santiago")
    return df


def depth_color(depth_km: float) -> str:
    if depth_km < 30:
        return "red"
    if depth_km < 70:
        return "orange"
    if depth_km < 150:
        return "gold"
    if depth_km < 300:
        return "green"
    return "blue"


df = load_data()

st.title("Earthquakes in Chile")
st.write(
    "Open USGS data (M4+, last 5 years). The Nazca plate is pushed beneath "
    "South America, which is why Chile has so many earthquakes."
)

with st.expander("What do magnitude and depth mean?"):
    st.markdown(
        """
**Magnitude** measures how much energy an earthquake releases. The scale is
logarithmic: each whole step up is roughly 32 times more energy (and about
10 times larger ground movement on a seismograph). An M6 is therefore far
stronger than an M5, not just a little.

- **M4 to 4.9:** often felt, rarely causes damage
- **M5 to 5.9:** can damage weak buildings
- **M6 to 6.9:** can be destructive near the epicentre
- **M7 and above:** major earthquake

**Depth** is how far below the surface the earthquake starts. For the same
magnitude, shallow earthquakes usually shake the surface harder. In Chile the
depth tells a story: along the coast the Nazca plate meets South America at
shallow depth, and further east the plate has sunk deeper, so the earthquakes
get deeper too.

**Colours on the map:**
🔴 under 30 km &nbsp; 🟠 30 to 70 km &nbsp; 🟡 70 to 150 km &nbsp;
🟢 150 to 300 km &nbsp; 🔵 over 300 km

The size of each circle shows the magnitude.
"""
    )

# Filters in the sidebar
st.sidebar.header("Filters")
mag_max = float(df["mag"].max())
mag_range = st.sidebar.slider(
    "Magnitude", 4.0, mag_max, (4.0, mag_max), 0.1,
    help="How strong the earthquake is. Each whole step is about 32 times more energy.",
)
depth_max = int(df["depth"].max()) + 1
depth_range = st.sidebar.slider(
    "Depth (km)", 0, depth_max, (0, depth_max),
    help="How far below the surface the earthquake starts.",
)

date_min = df["time"].dt.date.min()
date_max = df["time"].dt.date.max()
date_range = st.sidebar.date_input(
    "Date (Chile time)",
    (date_min, date_max),
    min_value=date_min,
    max_value=date_max,
    help="Narrow this to a few days to find a specific earthquake.",
)
if len(date_range) != 2:
    st.info("Pick an end date to apply the date filter.")
    st.stop()
start, end = date_range

filtered = df[
    df["mag"].between(*mag_range)
    & df["depth"].between(*depth_range)
    & (df["time"].dt.date >= start)
    & (df["time"].dt.date <= end)
]

st.metric("Earthquakes shown", f"{len(filtered)} of {len(df)}")

# Map
m = folium.Map(location=[-33.0, -71.0], zoom_start=5, tiles="OpenStreetMap")

for row in filtered.itertuples():
    folium.CircleMarker(
        location=[row.latitude, row.longitude],
        radius=max(row.mag - 2, 1) * 1.5,
        color=depth_color(row.depth),
        weight=1,
        fill=True,
        fill_color=depth_color(row.depth),
        fill_opacity=0.5,
        popup=(
            f"<b>M{row.mag:.1f}</b><br>Depth: {row.depth:.0f} km<br>"
            f"{row.time:%Y-%m-%d %H:%M} Chile time<br>{row.place}"
        ),
    ).add_to(m)

folium.Marker(VALPARAISO, tooltip="Valparaíso", icon=folium.Icon(color="black")).add_to(m)

st_folium(m, height=650, use_container_width=True, returned_objects=[])

st.subheader("Earthquakes in the selected period")
st.caption("Sorted by magnitude. Times are in Chile time.")
table = filtered.sort_values("mag", ascending=False)[
    ["time", "mag", "depth", "place"]
].rename(columns={"time": "Time", "mag": "Magnitude", "depth": "Depth (km)", "place": "Place"})
st.dataframe(table, use_container_width=True, hide_index=True)
