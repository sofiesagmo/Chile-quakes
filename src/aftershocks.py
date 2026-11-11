"""Aftershocks: daily earthquake counts near each large earthquake (M6.5+)."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_FILE = Path("data/earthquakes_chile.csv")
OUT_FILE = Path("docs/aftershocks.png")
BIG_MAGNITUDE = 6.5
RADIUS_KM = 150
DAYS_BEFORE = 10
DAYS_AFTER = 30


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = (
        np.sin((lat2 - lat1) / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * r * np.arcsin(np.sqrt(a))


df = pd.read_csv(DATA_FILE, parse_dates=["time"])
df["time"] = df["time"].dt.tz_localize(None)

big = df[df["mag"] >= BIG_MAGNITUDE].sort_values("time")
fig, axes = plt.subplots(len(big), 1, figsize=(10, 3 * len(big)), squeeze=False)

for ax, main in zip(axes[:, 0], big.itertuples()):
    dist = haversine_km(main.latitude, main.longitude, df["latitude"], df["longitude"])
    near = df[(dist <= RADIUS_KM) & (df["id"] != main.id)].copy()
    near["day"] = (near["time"] - main.time).dt.total_seconds() / 86400
    window = near[(near["day"] >= -DAYS_BEFORE) & (near["day"] < DAYS_AFTER)]

    before = (window["day"] < 0).sum()
    after = (window["day"] >= 0).sum()
    print(
        f"M{main.mag:.1f} {main.time:%Y-%m-%d} (depth {main.depth:.0f} km): "
        f"{before} before, {after} after"
    )

    bins = np.arange(-DAYS_BEFORE, DAYS_AFTER + 1)
    ax.hist(window["day"], bins=bins, color="steelblue")
    ax.axvline(0, color="red", linestyle="--")
    ax.set_title(
        f"M{main.mag:.1f}, {main.time:%Y-%m-%d} (depth {main.depth:.0f} km) - {main.place}",
        fontsize=10,
    )
    ax.set_ylabel("Earthquakes per day")

axes[-1, 0].set_xlabel("Days since the large earthquake")

OUT_FILE.parent.mkdir(exist_ok=True)
fig.tight_layout()
fig.savefig(OUT_FILE, dpi=150, bbox_inches="tight")
print(f"Saved {OUT_FILE}")
