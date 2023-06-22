import jinja2
from branca.element import MacroElement
from jinja2 import Template

import ProjectConsts

"""
Добавляет точки маршрута на карту и создаёт маршрут
"""


class RoutePointOnMap(MacroElement):
    """
    When one clicks on a Map that contains a LatLngPopup,
    a popup is shown that displays the latitude and longitude of the pointer.
    """

    @staticmethod
    def get_template():
        templateLoader = jinja2.FileSystemLoader(
            searchpath=ProjectConsts.RootDerictory + "externalControllers/webServer/static/js/folium/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "add_road_marker.js"
        template = templateEnv.get_template(TEMPLATE_FILE)
        # outputText = template.render()  # this is where to put args to the template renderer
        return template

    _template = None

    def __init__(self):
        self._template = RoutePointOnMap.get_template()
        super(RoutePointOnMap, self).__init__()
        self._name = 'LatLngPopup'
