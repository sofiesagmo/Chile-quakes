"""Check how stable the b-value is when the completeness magnitude Mc changes."""

from pathlib import Path

import numpy as np
import pandas as pd

DATA_FILE = Path("data/earthquakes_chile.csv")
BIN = 0.1

# Round to one decimal to avoid floating point problems at the cutoffs
mags = np.round(pd.read_csv(DATA_FILE)["mag"].to_numpy(), 1)

print(f"{'Mc':>4} {'N':>6} {'b':>6} {'+/-':>6}")
for mc in np.round(np.arange(4.0, 5.1, 0.1), 1):
    above = mags[mags >= mc - 1e-9]
    if len(above) < 50:
        break
    b = np.log10(np.e) / (above.mean() - (mc - BIN / 2))
    err = b / np.sqrt(len(above))  # Aki (1965) standard error
    print(f"{mc:>4.1f} {len(above):>6} {b:>6.2f} {err:>6.2f}")
