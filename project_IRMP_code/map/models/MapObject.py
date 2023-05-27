from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from db.DataBaseObject import DataBaseObject
from map.models.AbstractMapObject import AbstractMapObject
from map.models.MapPoint import MapPoint


class MapObject(AbstractMapObject):
    # __tablename__ = "map_objects"
    # """Имя объекта на карте"""
    # name = Column(String)
    # """Описание объекта на карте"""
    # description = Column(String)

    # map_points = relationship("MapPoint",
    #                           back_populates="map_object")  # TODO если массив изменяется, то нужно ли пеесчитывать центральную точку?

    """Центральная точка объекта"""

    # TODO возможно, временное решение
    @hybrid_property
    def central_point(self) -> MapPoint:
        sr_latitude = 0
        sr_longitude = 0
        len_map_points = self.map_points.__len__()
        for map_point in self.map_points:
            sr_latitude += map_point.latitude
            sr_longitude += map_point.longitude
        return MapPoint(latitude=sr_latitude / len_map_points,
                        longitude=sr_longitude / len_map_points)  # TODO наверное, можно соптимизировать

    # TODO Дальше нужно добавить список всех точек объекта, чтобы можно было строить маршруты и более точное отображение объекта на карте
