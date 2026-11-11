"""Time series: number of earthquakes per month, with the largest events marked."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = Path("data/earthquakes_chile.csv")
OUT_FILE = Path("docs/time_series.png")
BIG_MAGNITUDE = 6.5

df = pd.read_csv(DATA_FILE, parse_dates=["time"])
df["time"] = df["time"].dt.tz_localize(None)

# Earthquakes per month
monthly = df.groupby(df["time"].dt.to_period("M")).size()
monthly.index = monthly.index.to_timestamp()

# The largest earthquakes
big = df[df["mag"] >= BIG_MAGNITUDE].sort_values("mag", ascending=False)
print(f"Earthquakes per month: mean {monthly.mean():.0f}, max {monthly.max()} ({monthly.idxmax():%Y-%m})")
print(f"\nLargest earthquakes (M{BIG_MAGNITUDE}+):")
for row in big.itertuples():
    print(f"  M{row.mag:.1f}  {row.time:%Y-%m-%d}  {row.place}")

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(monthly.index, monthly.values, width=25, color="steelblue")

for row in big.itertuples():
    ax.axvline(row.time, color="red", linestyle="--", alpha=0.6)
    ax.text(row.time, ax.get_ylim()[1] * 0.95, f"M{row.mag:.1f}",
            color="red", rotation=90, ha="right", va="top")

ax.set_xlabel("Month")
ax.set_ylabel("Earthquakes (M4+)")
ax.set_title("Earthquakes in Chile per month")

OUT_FILE.parent.mkdir(exist_ok=True)
fig.savefig(OUT_FILE, dpi=150, bbox_inches="tight")
print(f"\nSaved {OUT_FILE}")
