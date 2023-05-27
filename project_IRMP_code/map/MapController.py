import logging

from db.DataBaseHelper import DataBaseHelper
from map.MapHelper import MapHelper
from map.models.MapObject import MapObject
from map.models.MapPoint import MapPoint
from sqlalchemy.orm import Session


class MapController:
    __db_session__: Session = None
    __map_objects__ = dict()
    __IRMP_map_object__: MapObject = None
    _logger_ = logging.getLogger()

    """
        При инициализации карты ей передаётся начальные координаты робота (gps_location)
    """

    def __init__(self, gps_location):
        self._logger_.info("Старт инициализации контроллера карты")
        self.__db_session__ = DataBaseHelper.create_data_base_connection()
        self.load_base_position(gps_location)
        self.load_nearby_map_objects()
        # TODO дальше загрузка маршрутов

        self._logger_.info("Инициализации контроллера карты завершена")

    """ Обновляем позицию робота на карте """

    def load_base_position(self, gps_location):
        self.__IRMP_map_object__ = self.__db_session__.query(MapObject).filter(MapObject.name == "ИРМП").first()
        if self.__IRMP_map_object__:
            self.__IRMP_map_object__.map_points = [MapPoint(gps_location)]  # TODO нужно пересчитывать центральную точку
        else:
            self.__IRMP_map_object__ = MapObject(
                name="ИРМП",
                description="Интеллектуальная роботизированная модульная платформа",
                map_points=[MapPoint(gps_location)])
        self.__db_session__.commit()
        self.__map_objects__[self.__IRMP_map_object__.name] = self.__IRMP_map_object__

    """Получаем все объекты в квадрате размером 100 на 100 метров """

    def load_nearby_map_objects(self):
        self._logger_.info("Загрузка близлежащих объектов...")
        self.__map_objects__.update(MapHelper.get_all_objects_in_square(self.__IRMP_map_object__.central_point, 100))
        self._logger_.info("Загрузка близлежащих объектов завершена")
