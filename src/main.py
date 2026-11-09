import csv
import folium

# Create map
m = folium.Map(
    location=[64.5, 11],
    zoom_start=5
)

# Read places from CSV
with open("data/places.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        folium.CircleMarker(
            location=[float(row["lat"]), float(row["lon"])],
            radius=8,
            color="blue",
            fill=True,
            fill_color="blue",
            popup=f"""
            <b>{row['name']}</b><br>
            Population: {row['population']}
            Region: {row['region']}
            """
        ).add_to(m)

# Save the map
m.save("maps/map.html")

print("Map saved in maps/map.html")