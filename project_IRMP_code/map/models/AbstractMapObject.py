from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.DataBaseObject import DataBaseObject


class AbstractMapObject(DataBaseObject):
    __tablename__ = "abstract_map_objects"

    """Имя объекта на карте"""
    name = Column(String)

    """Описание объекта на карте"""
    description = Column(String)

    map_points = relationship("MapPoint", back_populates="map_object")
    pass
