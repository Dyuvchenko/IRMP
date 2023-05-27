#
# line segment intersection using vectors
# see Computer Graphics by F.S. Hill
#
from numpy import *

from db.DataBaseHelper import DataBaseHelper
from map.models.MapObject import MapObject
from map.models.MapPoint import MapPoint


def perp(a):
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1, a2, b1, b2):
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perp(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    return (num / denom.astype(float)) * db + b1


# def vector_mult(ax, ay, bx, by):  # векторное произведение
#     return ax * by - bx * ay
#
#
# def areCrossing(p1, p2, p3, p4):  # проверка пересечения
#
#     v1 = vector_mult(p4.X - p3.X, p4.Y - p3.Y, p1.X - p3.X, p1.Y - p3.Y)
#
#     v2 = vector_mult(p4.X - p3.X, p4.Y - p3.Y, p2.X - p3.X, p2.Y - p3.Y)
#
#     v3 = vector_mult(p2.X - p1.X, p2.Y - p1.Y, p3.X - p1.X, p3.Y - p1.Y)
#
#     v4 = vector_mult(p2.X - p1.X, p2.Y - p1.Y, p4.X - p1.X, p4.Y - p1.Y)
#     if ((v1 * v2) < 0 & & (v3 * v4) < 0)
#         return true
#     return false

# if __name__ == "__main__":
#         p1 = array([0.0, 0.0])
#
#
# p2 = array([1.0, 0.0])
#
# p3 = array([4.0, -5.0])
# p4 = array([4.0, 2.0])
#
# print
# seg_intersect(p1, p2, p3, p4)
#
# p1 = array([2.0, 2.0])
# p2 = array([4.0, 3.0])
#
# p3 = array([6.0, 0.0])
# p4 = array([6.0, 3.0])
#
# print
# seg_intersect(p1, p2, p3, p4)

class MapHelper:
    """Возвращает словарь с объектами, которые попадают в квадрат размером side_square * side_square """
    """side_square задаётся в метрах"""
    """Центр квадрата - base_point"""

    @staticmethod
    def get_all_objects_in_square(base_point, side_square):
        half_side_square = (0.000009 * side_square) / 2
        max_latitude = base_point.latitude + half_side_square
        min_latitude = base_point.latitude - half_side_square
        max_longitude = base_point.longitude + half_side_square
        min_longitude = base_point.longitude - half_side_square

        map_objects = DataBaseHelper.create_data_base_connection().query(MapObject).join(MapPoint).filter(
            MapPoint.map_object_id == MapObject.id and
            MapPoint.latitude < max_latitude and
            MapPoint.latitude > min_latitude and
            MapPoint.longitude < max_longitude and
            MapPoint.longitude > min_longitude
            # max_latitude > MapObject.central_point.latitude > min_latitude and
            # max_longitude > MapObject.central_point.longitude > min_longitude
        ).all()

        result_dict_objects = dict()
        for mapObject in map_objects:
            result_dict_objects[mapObject.name] = mapObject
        return result_dict_objects
