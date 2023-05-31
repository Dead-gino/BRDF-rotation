import numpy as np
import points
from points import Point
import math
from math import pi


def find_axis(ps):
    # get single highest or a pair of highest points
    max_x_1 = -1
    max_z_1 = -1
    max_x_2 = -1
    max_z_2 = -1
    if isinstance(ps, list):
        for p in ps:
            if isinstance(p, Point):
                if p.z >= max_z_1:
                    max_z_2 = max_z_1
                    max_x_2 = max_x_1
                    max_z_1 = p.z
                    max_x_1 = p.x
                elif p.z >= max_z_2:
                    max_z_2 = p.z
                    max_x_2 = p.x
            else:
                raise TypeError
    else:
        raise TypeError

    if max_z_1 == max_z_2:
        x = (max_x_1 + max_x_2) / 2
    else:
        x = max_x_1

    return Point(x, 0, 0)


def revolve(p, center, scale):
    r = p.dist2D(center)
    ps = [p]
    for i in np.arange(0, 2*pi, (2*pi)/scale):
        x = center.x
        y = center.y
        theta = i
        a = x + (math.cos(theta) * r)
        b = y + (math.sin(theta) * r)
        new_p = Point(a, b, p.z)
        ps.append(new_p)
    return ps


def revolve_all(ps, scale):
    axis = find_axis(ps)
    px = []
    for p in ps:
        px += revolve(p, axis, scale)
    return px
