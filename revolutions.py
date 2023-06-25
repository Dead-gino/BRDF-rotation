import numpy as np
import points
from points import Point
import math


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


def revolve_simple(p, center, scale):
    """ creates a circle of points by rotating a given point around a vertical axis that goes through center

    :param p: the original point that is rotated
    :param center: the axis to rotate around
    :param scale: the amount of points created by the rotation
    :return: a list of points created by rotating p around center
    """
    offset = center.x
    base = points.create_point(p.x - offset, p.y, p.z)
    azimuth = base.azimuth
    altitude = base.altitude
    length = base.length
    ps = []
    for i in np.arange(0, 360, 360 / scale):
        round(i)
        new_p = points.from_angles(azimuth + i, altitude, length)
        ps.append(new_p)
    return ps


def revolve_axis(p, axis, offset, scale):
    """ creates a band of points by revolving p around an axis, with the axis offset from going through 0 by the offset

    :param p: the point to revolve
    :param axis: the axis to revolve around
    :param offset: the offset of the axis from 0 along the x-axis
    :param scale: the amount of points on the created band of points
    :return: a list containing all the points on the band
    """
    off_p = points.create_point(p.x, p.y, p.z)
    off_p.shift(-offset, 0, 0)
    ps = []
    cross = axis.cross(off_p)
    dot = axis.dot(off_p)
    for theta in np.arange(0, 360, 360/scale):
        cos = math.cos(math.radians(theta))
        sin = math.sin(math.radians(theta))
        x = (off_p.x * cos) + (cross.x * sin) + (axis.x * (dot * (1 - cos)))
        y = (off_p.y * cos) + (cross.y * sin) + (axis.y * (dot * (1 - cos)))
        z = (off_p.z * cos) + (cross.z * sin) + (axis.z * (dot * (1 - cos)))
        x += offset
        new_p = points.create_point(x, y, z)
        ps.append(new_p)
    return ps


def revolve_all_simple(ps, scale):
    """ creates a solid of revolution from a list of points

    :param ps: the points to turn into a solid of revolution
    :param scale: the amount of points in each band that forms the solid
    :return: a list of Points representing the solid of revolution
    """
    axis = find_axis_vertical(ps)
    px = []
    for p in ps:
        px += revolve_simple(p, axis, scale)
    return px


def revolve_all_axis(ps, axis, offset, scale):
    """ creates a solid of revolution by rotating a list of points around an axis

    :param ps: the list of points to turn into a solid of revolution
    :param axis: a vector describing the direction of the axis of revolution
    :param offset: the x-offset of the axis
    :param scale: the amount of points in each band that forms the solid
    :return: a list of Points representing the solid of revolution
    """
    px = []
    for p in ps:
        px.extend(revolve_axis(p, axis, offset, scale))
    return px


def revolve_list(pss: list, scale):
    """ creates a single solid of revolution from a list of sub-curves, represented by a list of lists of Points

    :param pss: the list of curves to turn into a solid of revolution
    :param scale: the amount of points in each band that from the solid
    :return: a list of Points representing the solid of revolution
    """
    px = []
    for ps in pss:
        p = revolve_all_simple(ps, scale)
        px = px + p
    return px


def remove_overlap_angular(ps: list):
    """ removes overlapping vectors that point in the same direction, leaving the vector with the highest intensity

    :param ps: a list with the points to remove overlapping vectors from
    :return: a new list with the remaining points
    """
    px = []
    for p in ps:
        if len(px) == 0:
            px.append(p)  # if px is empty: add the first point to px
        elif not(px[-1].azimuth == p.azimuth and px[-1].altitude == p.altitude):
            px.append(p)  # if the last point in px is not parallel to p: add p to the end of px
        elif px[-1].azimuth == p.azimuth and px[-1].altitude == p.altitude and px[-1].length < p.length:
            px[-1] = p  # if the last point in px is parallel to p and p is longer: replace the last point in px with p
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


def fill_domain(px: list, scale):
    angs = []
    ps = px.copy()
    for p in px:
        q = (p.azimuth, p.altitude)
        angs.append(q)
    for phi in np.arange(0, 90 + scale, scale):
        for theta in np.arange(-180, 180 + scale, scale):
            p = points.from_angles(theta, phi, 0)
            q = (theta, phi)
            if not(q in angs):
                ps.append(p)
    ps.sort()
    # for p in ps:
    #     print(p)
    return ps
