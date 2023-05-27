from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.DataBaseObject import DataBaseObject
from map.models.AbstractMapObject import AbstractMapObject


class MapRoute(AbstractMapObject):
    current_point = None
    next_point = None
    # __tablename__ = "map_route"
    # """Имя объекта на карте"""
    # name = Column(String)
    #
    # map_points = relationship("MapPoint",
    #                           back_populates="map_object")
