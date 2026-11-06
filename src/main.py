import folium

m = folium.Map(
    location=[63.43, 10.39],
    zoom_start=5
)

m.save("maps/norway_map.html")

print("Map created!")