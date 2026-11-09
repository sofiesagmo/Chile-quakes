"""Henter jordskjelv i Chile fra USGS og lagrer dem til data/earthquakes_chile.csv."""

from datetime import date
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Grov bounding box rundt Chile
MIN_LAT, MAX_LAT = -56, -17
MIN_LON, MAX_LON = -76, -66

MIN_MAGNITUDE = 4.0
YEARS_BACK = 5

OUT_FILE = Path("data/earthquakes_chile.csv")


def fetch_year(start: str, end: str) -> pd.DataFrame:
    """Henter ett tidsvindu. USGS tillater maks 20 000 hendelser per kall,
    så vi henter ett år av gangen."""
    params = {
        "format": "csv",
        "starttime": start,
        "endtime": end,
        "minmagnitude": MIN_MAGNITUDE,
        "minlatitude": MIN_LAT,
        "maxlatitude": MAX_LAT,
        "minlongitude": MIN_LON,
        "maxlongitude": MAX_LON,
        "orderby": "time",
    }
    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text))


def main() -> None:
    today = date.today()
    frames = []

    for i in range(YEARS_BACK):
        year_start = date(today.year - YEARS_BACK + i, today.month, today.day)
        year_end = date(today.year - YEARS_BACK + i + 1, today.month, today.day)
        print(f"Henter {year_start} til {year_end} ...")
        frames.append(fetch_year(year_start.isoformat(), year_end.isoformat()))

    df = pd.concat(frames, ignore_index=True).drop_duplicates(subset="id")
    df = df[["time", "latitude", "longitude", "depth", "mag", "place", "id"]]

    OUT_FILE.parent.mkdir(exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"Lagret {len(df)} skjelv i {OUT_FILE}")


if __name__ == "__main__":
    main()
