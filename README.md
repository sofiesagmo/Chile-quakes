# Earthquakes in Chile

A small project combining computer science and geoscience. It uses open USGS data to explore earthquakes in Chile, where the Nazca plate is pushed under South America, and shows them on an interactive map with Valparaíso marked.

## Project history

This project started as "Land-Trend", a plan to measure vegetation change around Trondheim with Sentinel-2 satellite images and Google Earth Engine. While I was working on it during my exchange in Chile, a small earthquake suddenly hit, and it made me want to switch topics. The new topic needs no accounts or large raster files, so I can focus on the analysis.

## What it does

- Fetches earthquakes (M4+, last 5 years) from the USGS API
- Shows them on a Folium map: size by magnitude, color by depth
- Marks Valparaíso and counts earthquakes within 100 km in the last year

## Planned

1. Cross-section of the subduction zone (depth vs longitude)
2. Gutenberg-Richter law and b-value
3. Time series and aftershocks
4. Comparison with Norway

## Structure

    data/   Downloaded data (CSV)
    docs/   Notes and figures
    maps/   Generated maps (HTML)
    src/    Python scripts

## Getting started

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    python src/fetch_earthquakes.py
    python src/main.py

Open maps/map.html in a browser.

## Data

USGS Earthquake Catalog: https://earthquake.usgs.gov/fdsnws/event/1/
