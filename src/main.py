import folium

# Map centered over Norway
m = folium.Map(
    location=[64.5, 11],
    zoom_start=5
)

# Lagre kartet
m.save("maps/map.html")

print("Kart lagret i maps/map.html")