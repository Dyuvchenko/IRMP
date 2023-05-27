# First, import the geodesic module from the geopy library
import sys

from geopy.distance import geodesic as GD
import utm
import math

from PIL import Image, ImageDraw
from map.models.MapObject import MapObject

u = utm.from_latlon(12.917091, 77.573586)

if __name__ == "__main__":
    # Then, load the latitude and longitude data for New York & Texas
    x = 58.083433
    y = 38.675178
    T1 = (58.083433, 38.675178)
    T2 = (x + 0.000009, y)
    # T2 = (58.083410, 38.675950)
    # T2 = (58.083305, 38.675641)

    # At last, print the distance between two points calculated in kilo-metre
    print("The distance between New York and Texas is: ", GD(T1, T2).m)

    # z, x = T1[:]
    # print(z,x)
    # return z

    u = utm.from_latlon(T1[0], T1[1])
    u2 = utm.from_latlon(T2[0], T2[1])
    print(u)
    print(u2)
    rast = math.sqrt((T2[0] - T1[0]) ** 2 + (T2[1] - T1[1]) ** 2)
    rast = rast * 100000 / 1.3892443989665486
    print(rast)

    print(u[1]-u2[1])
    # print(u2[0])





