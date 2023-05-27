{% macro script(this, kwargs) %}
    var {{this.get_name()}} = L.popup();
    function latLngPop(e) {
        {{this.get_name()}}
//            .setLatLng(e.latlng)
//            .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
//                        "<br>Longitude: " + e.latlng.lng.toFixed(4))
//            .openOn({{this._parent.get_name()}});

            FoliumHelper.addMarkerRoute(e.latlng.lat.toFixed(6), e.latlng.lng.toFixed(6));
        }
    {{this._parent.get_name()}}.on('click', latLngPop);
{% endmacro %}