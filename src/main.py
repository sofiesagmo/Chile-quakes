import folium

#Map
m = folium.Map(
    location=[64.5, 11],
    zoom_start=5
)

#Trondheim
folium.Marker(
    location=[63.4305, 10.3951],
    popup="Trondheim"
).add_to(m)

m.save("maps/map.html")

print("Kart lagret i maps/map.html")