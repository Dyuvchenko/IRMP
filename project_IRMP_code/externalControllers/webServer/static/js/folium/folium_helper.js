class FoliumHelper {

    static numberPoint = 1;

    static newRoute() {
        numberPoint = 1;
    }

    static addMarker(latitude, longitude) {
        L.circleMarker(
            [latitude,longitude], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map_name}});
    }

    static addBaseMarker(latitude, longitude) {
        L.marker([latitude, longitude])
            .addTo({{map_name}});
    }

    static addMarkerRoute(latitude, longitude) {
        FoliumHelper.addBaseMarker(latitude, longitude);
        let textMarker = L.marker([latitude, longitude]);
        let divIcon = L.divIcon();
        divIcon.options.className = '';
        divIcon.options.html = '<div style="font-size: 20pt">№' + FoliumHelper.numberPoint + '</div>';
        textMarker.setIcon(divIcon)
        textMarker.addTo({{map_name}});

        FoliumHelper.numberPoint += 1;
    }


}