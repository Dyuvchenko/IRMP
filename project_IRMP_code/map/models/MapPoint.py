import utm
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.DataBaseObject import DataBaseObject

"""Первоначальная идея, что это будет хранить в  себе координаты
т.е. мы будем иметь класс, в котором указны GPS координаты и аналогичные им UTM"""


class MapPoint(DataBaseObject):
    __tablename__ = "map_points"

    """Ссылка на объект карты"""
    map_object_id = Column(Integer, ForeignKey("abstract_map_objects.id"))
    map_object = relationship("AbstractMapObject", back_populates="map_points")

    """--------------------GPS--------------------"""
    """Широта"""
    latitude: float = Column(Float)
    """Долгота"""
    longitude: float = Column(Float)

    """--------------------UTM--------------------"""
    """Ориентация на восток"""
    easting = Column(Float)
    """Ориентация на север"""
    northing = Column(Float)
    """Номер UTM зоны"""
    zone_number = Column(Integer)
    """Номер UTM зоны буквенный"""
    zone_letter = Column(String)

    # y = northing
    # x = easting

    """Получает на вход gps координаты в виде string строки"""
    """Пример: (55.755864, 37.617698) """

    def __init__(self, gps_string=None, latitude=None, longitude=None):
        super().__init__()
        if latitude is not None and longitude is not None:
            self.latitude = latitude
            self.longitude = longitude
        else:  # TODO ну, наверное нужно предусмотреть ситуатцию, что всё "none"
            latitude, longitude = gps_string.replace(",", "").split(" ")
            self.latitude, self.longitude = float(latitude), float(longitude)
        self.easting, self.northing, self.zone_number, self.zone_letter = utm.from_latlon(float(self.latitude),
                                                                                          float(self.longitude))

        self.x = self.northing
        self.y = self.easting
