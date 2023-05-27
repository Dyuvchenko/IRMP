import folium

if __name__ == "__main__":
    map = folium.Map(location=[58.085767, 38.667091], zoom_start=15, tiles="OpenStreetMap")

    # create a polygon with the coordinates
    folium.Polygon([(58.083721, 38.668689), (58.085608, 38.663035), (58.086199, 38.663368),
                    (58.087364, 38.663443), (58.085432, 38.671887)],
                   weight=2,
                   color="red",
                   fill_color="yellow",
                   fill_opacity=0.3).add_to(map)


    map.add_child(folium.LatLngPopup())
    folium.ClickForLatLng
    map.save("map1.html")


