"""Lager et Folium-kart over jordskjelv i Chile med Valparaíso markert."""

from pathlib import Path

import folium
import numpy as np
import pandas as pd

DATA_FILE = Path("data/earthquakes_chile.csv")
OUT_FILE = Path("maps/map.html")

VALPARAISO = (-33.0472, -71.6127)
RADIUS_KM = 100


def haversine_km(lat1, lon1, lat2, lon2):
    """Avstand i km mellom punkter på jorda (fungerer på NumPy-arrays)."""
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = (
        np.sin((lat2 - lat1) / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * r * np.arcsin(np.sqrt(a))


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


def main() -> None:
    df = pd.read_csv(DATA_FILE, parse_dates=["time"])

    # Skjelv nær Valparaíso siste år
    df["dist_valpo_km"] = haversine_km(
        VALPARAISO[0], VALPARAISO[1], df["latitude"], df["longitude"]
    )
    one_year_ago = pd.Timestamp.now(tz="UTC") - pd.DateOffset(years=1)
    nearby = df[(df["dist_valpo_km"] <= RADIUS_KM) & (df["time"] >= one_year_ago)]
    print(f"{len(nearby)} skjelv (M4+) innenfor {RADIUS_KM} km fra Valparaíso siste år")

    # Kart
    m = folium.Map(location=[-33.0, -71.0], zoom_start=5, tiles="OpenStreetMap")

    for row in df.itertuples():
        folium.CircleMarker(
            location=[row.latitude, row.longitude],
            radius=max(row.mag - 2, 1) * 1.5,
            color=depth_color(row.depth),
            weight=1,
            fill=True,
            fill_color=depth_color(row.depth),
            fill_opacity=0.5,
            popup=(
                f"<b>M{row.mag:.1f}</b><br>"
                f"Dybde: {row.depth:.0f} km<br>"
                f"{row.time:%Y-%m-%d %H:%M} UTC<br>"
                f"{row.place}"
            ),
        ).add_to(m)

    # Valparaíso
    folium.Marker(
        location=VALPARAISO,
        tooltip="Valparaíso",
        popup=(
            "<b>Valparaíso</b><br>"
            f"{len(nearby)} skjelv (M4+) innenfor {RADIUS_KM} km siste år"
        ),
        icon=folium.Icon(color="black", icon="home"),
    ).add_to(m)
    folium.Circle(
        location=VALPARAISO,
        radius=RADIUS_KM * 1000,
        color="black",
        weight=1,
        fill=False,
        dash_array="5",
    ).add_to(m)

    OUT_FILE.parent.mkdir(exist_ok=True)
    m.save(OUT_FILE)
    print(f"Kart lagret i {OUT_FILE}")


if __name__ == "__main__":
    main()