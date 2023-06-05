import numpy as np
import points
from points import Point
import math
from math import pi


def find_axis_vertical(ps: list):
    """ Get the axis of rotation for a set of points. Only works for completely vertical axes.

    :param ps: a list containing the points to get the rotation axis for
    :return: a point that represents the axis found
    """
    max_x_1 = -1
    max_z_1 = -1
    max_x_2 = -1
    max_z_2 = -1
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

    # use the two highest points if they have equal z, or use the highest point
    if max_z_1 == max_z_2:
        x = (max_x_1 + max_x_2) / 2
    else:
        x = max_x_1

    return Point(x, 0, 0)


def revolve(p, center, scale):
    """ creates a circle of points by rotating a given point around an axis

    :param p: the original point that is rotated
    :param center: the axis to rotate around
    :param scale: the amount of points created by the rotation
    :return: a list of points created by rotating p around center
    """
    r = p.dist2d(center)
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
    """ creates a solid of revolution from a list of points

    :param ps: the points to turn into a solid of revolution
    :param scale: the amount of points in each band that forms the solid
    :return: a list of Points representing the solid of revolution
    """
    axis = find_axis_vertical(ps)
    px = []
    for p in ps:
        px += revolve(p, axis, scale)
    return px


def revolve_list(pss: list, scale):
    """ creates a single solid of revolution from a list of sub-curves, represented by a list of lists of Points

    :param pss: the list of curves to turn into a solid of revolution
    :param scale: the amount of points in each band that from the solid
    :return: a list of Points representing the solid of revolution
    """
    px = []
    for ps in pss:
        p = revolve_all(ps, scale)
        px = px + p
    return px


def remove_overlap_simple(ps: list):
    """ removes overlapping datapoint that have equal x and y values and leaves only the highest number.
        requires grid-aligned data

    :param ps: the points to remove overlap from, all points aligned to the same grid
    :return: the points left after removal
    """
    # sort all points
    ps.sort()

    x = -1
    y = -1
    prev = None
    new_ps = []
    for p in ps:
        # if at a new point on grid, move tracker and reset z
        if x != p.x:
            x = p.x
            if not(prev is None) and not(prev in new_ps):  # ensure there are no duplicate points
                new_ps.append(prev)
            prev = None
        if y != p.y:
            y = p.y
            if not(prev is None) and not(prev in new_ps):  # no duplicates
                new_ps.append(prev)
            prev = None

        if prev is None:
            prev = p
        elif prev.z < p.z:
            prev = p

    return new_ps


def sub_curves_naive(ps: list):
    """ Finds all sub-curves in a naive way;
        assumes data sorted on ascending x, then ascending z
        cannot properly handle multiple points with the same x coordinate

    :param ps: the points to find the sub-curves from
    :return: a list containing lists of points, each list is one sub-curve
    """
    if len(ps) == 1:
        return [ps]
    elif len(ps) == 2:
        return [ps]
    else:
        prev = ps[0]
        curves = [[prev]]
        asc = True
        ci = 0
        for i in np.arange(1, len(ps)):
            cur = ps[i]
            if prev.z > cur.z and asc:
                asc = False
            elif prev.z < cur.z and not asc:
                asc = True
                ci += 1

            if ci == len(curves):
                curves.append([])
            curves[ci].append(cur)
            prev = cur
        return curves
