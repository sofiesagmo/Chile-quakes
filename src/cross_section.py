"""Cross-section of the subduction zone: depth vs longitude around Valparaiso."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = Path("data/earthquakes_chile.csv")
OUT_FILE = Path("docs/cross_section.png")

# Narrow latitude strip around Valparaiso (about 33 degrees south)
MIN_LAT, MAX_LAT = -34.0, -32.0

df = pd.read_csv(DATA_FILE)
strip = df[(df["latitude"] >= MIN_LAT) & (df["latitude"] <= MAX_LAT)]
print(f"{len(strip)} earthquakes in the strip")

fig, ax = plt.subplots(figsize=(10, 6))
points = ax.scatter(
    strip["longitude"],
    strip["depth"],
    c=strip["mag"],
    s=(strip["mag"] - 3) ** 2 * 6,
    cmap="viridis",
    alpha=0.6,
)
ax.invert_yaxis()  # depth increases downwards
ax.set_xlabel("Longitude")
ax.set_ylabel("Depth (km)")
ax.set_title("Nazca plate beneath Chile (latitude 32-34 S)")
fig.colorbar(points, label="Magnitude")

OUT_FILE.parent.mkdir(exist_ok=True)
fig.savefig(OUT_FILE, dpi=150, bbox_inches="tight")
print(f"Saved {OUT_FILE}")
