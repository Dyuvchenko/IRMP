import folium
import jinja2
from branca.element import Element

import ProjectConsts


class FoliumMapHelper:

    @staticmethod
    def add_current_position(folium_map):
        current_IRMP_position = ProjectConsts.Core.__map_controller__.__IRMP_map_object__.central_point
        folium.Marker(
            location=[current_IRMP_position.latitude, current_IRMP_position.longitude],
            popup=[current_IRMP_position.latitude, current_IRMP_position.longitude],
            icon=folium.Icon(
                color='green',
                icon="glyphicon glyphicon-record"

            ),
            tooltip="IRMP находится здесь"
        ).add_to(folium_map)

    """Удаляет дополнительную информацию, которую вставляет folium"""

    @staticmethod
    def delete_folium_info(folium_map):
        folium_map.get_root().html.add_child(folium.JavascriptLink("static/js/folium/delete_base_folium_info.js"))

    @staticmethod
    def add_folium_helper(folium_map):
        templateLoader = jinja2.FileSystemLoader(
            searchpath=ProjectConsts.RootDerictory + "externalControllers/webServer/static/js/folium/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "folium_helper.js"
        template = templateEnv.get_template(TEMPLATE_FILE)
        folium_map.get_root().script.add_child(Element(template.render(map_name=folium_map.get_name())))

    @staticmethod
    def create_folium_map():
        current_position = ProjectConsts.Core.__map_controller__.__IRMP_map_object__.central_point
        f_map = folium.Map(
            width=800,
            height=600,
            max_zoom=19,
            location=[current_position.latitude, current_position.longitude],
            zoom_start=17
        )
        FoliumMapHelper.add_current_position(f_map)
        FoliumMapHelper.delete_folium_info(f_map)
        FoliumMapHelper.add_folium_helper(f_map)
        return f_map
