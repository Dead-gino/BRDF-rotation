import numpy as np
from math import pi
import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def dist2D(self, other):
        dx = np.abs(self.x - other.x)
        dy = np.abs(self.y - other.y)
        return np.sqrt(dx ** 2 + dy ** 2)

    def dist3D(self, other):
        dx = np.abs(self.x - other.x)
        dy = np.abs(self.y - other.y)
        dz = np.abs(self.z - other.z)
        return np.sqrt(dx**2 + dy**2 + dz**2)


def zero(self):
    return Point(0, 0, 0)


def create_point(x, y, z):
    return Point(x, y, z)


def create_points(xs, ys, zs):
    iss = np.arange(0, len(xs), 1)
    ps = []
    for i in iss:
        x = xs[i]
        y = ys[i]
        z = zs[i]
        p = Point(x, y, z)
        ps.append(p)
    return ps


def convert_points(ps):
    xs = []
    ys = []
    zs = []
    if isinstance(ps, list):
        for p in ps:
            xs.append(p.x)
            ys.append(p.y)
            zs.append(p.z)
        return [xs, ys, zs]
    else:
        raise TypeError


def rasterize(ps: list, sample: int):
    for p in ps:
        x = p.x
        y = p.y
        new_x = __int_round(x, sample)
        new_y = __int_round(y, sample)
        p.x = new_x
        p.y = new_y


def __int_round(num: int, scale: int):
    half = scale/2
    div = num // scale
    if num % scale >= half:
        return (div + 1) * scale
    else:
        return div*scale




