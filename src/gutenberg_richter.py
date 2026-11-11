"""Gutenberg-Richter law: how many earthquakes of each magnitude, and the b-value."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_FILE = Path("data/earthquakes_chile.csv")
OUT_FILE = Path("docs/gutenberg_richter.png")
BIN = 0.1

df = pd.read_csv(DATA_FILE)
mags = df["mag"].to_numpy()

# Magnitude of completeness (Mc): above this, the catalog is assumed complete.
# Simple "maximum curvature" method: the most common magnitude bin.
bins = np.arange(mags.min(), mags.max() + BIN, BIN)
counts, edges = np.histogram(mags, bins=bins)
mc = 4.7  # chosen from b_value_check.py: b stabilizes from here

# b-value with the Aki-Utsu maximum likelihood estimate
above = mags[mags >= mc]
b = np.log10(np.e) / (above.mean() - (mc - BIN / 2))

print(f"Total earthquakes: {len(mags)}")
print(f"Completeness magnitude Mc: {mc:.1f}")
print(f"Earthquakes at or above Mc: {len(above)}")
print(f"b-value: {b:.2f}")

# Cumulative counts: number of earthquakes with magnitude >= M
m_values = np.arange(mags.min(), mags.max(), BIN)
cumulative = np.array([(mags >= m).sum() for m in m_values])

fig, ax = plt.subplots(figsize=(8, 6))
ax.semilogy(m_values, cumulative, "o", markersize=4, label="Observed")

# Fitted line, anchored at Mc
fit_m = m_values[m_values >= mc]
fit_n = len(above) * 10 ** (-b * (fit_m - mc))
ax.semilogy(fit_m, fit_n, "r-", label=f"Fit (b = {b:.2f})")

ax.axvline(mc, color="gray", linestyle="--", label=f"Mc = {mc:.1f}")
ax.set_xlabel("Magnitude")
ax.set_ylabel("Number of earthquakes with magnitude ≥ M")
ax.set_title("Gutenberg-Richter law for Chile")
ax.legend()

OUT_FILE.parent.mkdir(exist_ok=True)
fig.savefig(OUT_FILE, dpi=150, bbox_inches="tight")
print(f"Saved {OUT_FILE}")
