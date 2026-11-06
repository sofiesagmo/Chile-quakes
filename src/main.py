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
        folium.Marker(
            location=[float(row["lat"]), float(row["lon"])],
            popup=row["name"]
        ).add_to(m)

# Save the map
m.save("maps/map.html")

print("Kart lagret i maps/map.html")