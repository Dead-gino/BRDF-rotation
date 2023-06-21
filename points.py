import numpy as np
import math


class Point:
    """ a point in 3D space that stores its coordinates, its horizontal and vertical angles and its distance to 0

    :var x: the x coordinate, domain: [0,100]
    :var y: the y coordinate, domain: [0,100]
    :var z: the z coordinate, domain: [0,100]
    :var azimuth: the horizontal angle representing the rotation around the normal, lies across the x-y plane,
                    domain: (-180,180]
                    0 when on the x-axis and x is positive, 180 when on the x-axis and x is negative
                    90 when on the y-axis and y is positive, -90 when on the y-axis and y is negative
                    positive when y is positive, negative when y is negative
    :var altitude: the vertical angle representing the angle to the normal, lies across the x-z plane,
                    domain: [0,90]
                    0 when on the z-axis, 90 when on the x-axis
    :var length: the length of the vector from 0 to self
                    represents the intensity of the light reflected in the direction of the vector in percentages
                    domain: [0,100]
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.length = self.intensity()
        self.altitude = self.angle_vertical()
        self.azimuth = self.angle_horizontal()

    def __str__(self):
        return f"(x: {self.x}, y: {self.y}, z: {self.z}, " \
               f"azimuth: {self.azimuth}, altitude: {self.altitude}, intensity: {self.length})"
        # return f"(azimuth: {self.azimuth}, altitude: {self.altitude}"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        if self.altitude != other.altitude:
            return self.altitude < other.altitude
        elif self.azimuth != other.azimuth:
            return self.azimuth < other.azimuth
        else:
            return self.length < other.length

    def __gt__(self, other):
        if self.altitude != other.altitude:
            return self.altitude > other.altitude
        elif self.azimuth != other.azimuth:
            return self.azimuth > other.azimuth
        else:
            return self.length > other.length

    def __le__(self, other):
        if self.altitude != other.altitude:
            return self.altitude <= other.altitude
        elif self.azimuth != other.azimuth:
            return self.azimuth <= other.azimuth
        else:
            return self.length <= other.length

    def __ge__(self, other):
        if self.altitude != other.altitude:
            return self.altitude >= other.altitude
        elif self.azimuth != other.azimuth:
            return self.azimuth >= other.azimuth
        else:
            return self.length >= other.length

    def __eq__(self, other):
        return self.altitude == other.altitude and self.azimuth == other.azimuth and self.length == other.length

    def dist2d(self, other):
        """ calculates the pythagorean distance between self and another point along the x and y axes

        :param other: the point to measure distance to
        :return: the pythagorean distance to other along the x and y axes
        """
        dx = np.abs(self.x - other.x)
        dy = np.abs(self.y - other.y)
        return np.sqrt(dx ** 2 + dy ** 2)

    def dist3d(self, other):
        """ calculates the pythagorean distance between self and another point along all axes

        :param other: the point to measure distance to
        :return: the pythagorean distance to other along all axes
        """
        dx = np.abs(self.x - other.x)
        dy = np.abs(self.y - other.y)
        dz = np.abs(self.z - other.z)
        return np.sqrt(dx**2 + dy**2 + dz**2)

    def angle_horizontal(self):
        """ calculates the azimuth of a Point

        :return: the azimuth of self
        """
        if self.altitude == 90:
            return 0
        x = self.x
        y = self.y
        theta = math.degrees(math.atan2(y, x))
        return theta

    def angle_vertical(self):
        """ calculates the altitude of a Point

        :return: the altitude of self
        """
        i = self.intensity()
        z = self.z
        phi = math.degrees(math.asin(z/i))
        return phi

    def intensity(self):
        """ calculate the length of the vector between the point and (0,0,0)

        :return: the distance between self and (0,0,0)
        """
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def update_coordinates(self):
        """ updates coordinates based on angles

        :return: nothing, point itself is altered
        """
        azi = self.azimuth
        alt = self.altitude
        length = self.length
        y = length * (math.sin(math.radians(azi)) * math.cos(math.radians(alt)))
        x = length * (math.cos(math.radians(azi)) * math.cos(math.radians(alt)))
        z = length * (math.sin(math.radians(alt)))
        self.x = x
        self.y = y
        self.z = z

    def update_angles(self):
        """ recalculates the angles of a Point

        :return: nothing, updates an existing instance of Point
        """
        self.azimuth = self.angle_horizontal()
        self.altitude = self.angle_vertical()
        self.length = self.intensity()

    def round_angles(self, scale):
        """ rounds all angles to a certain scale

        :param scale: the scale to round the angles to
        :return: nothing, updates an existing instance of Point
        """
        azimuth = self.azimuth
        altitude = self.altitude
        half = scale/2
        d_azimuth = azimuth % scale
        d_altitude = altitude % scale
        self.azimuth -= d_azimuth
        self.altitude -= d_altitude
        if d_azimuth > half:
            self.azimuth += scale
        if d_altitude > half:
            self.altitude += scale

    def shift(self, dx, dy, dz):
        """ shifts a point in a direction

        :param dx: the distance to move along the x-axis
        :param dy: the distance to move along the y-axis
        :param dz: the distance to move along the z-axis
        :return: nothing, this method changes an existing instance of a Point
        """
        self.x += dx
        self.y += dy
        self.z += dz
        self.update_angles()

    def cross(self, other):
        """ the cross product between self and other

        :param other: the second argument of the cross product
        :return: the cross product of self and other
        """
        a_1 = self.x
        a_2 = self.y
        a_3 = self.z
        b_1 = other.x
        b_2 = other.y
        b_3 = other.z
        x = a_2 * b_3 - a_3 * b_2
        y = a_3 * b_1 - a_1 * b_3
        z = a_1 * b_2 - a_2 * b_1
        prod = create_point(x, y, z)
        return prod

    def dot(self, other):
        """ the dot product between self and other

        :param other: the second argument of the cross product
        :return: the dot product of self and other
        """
        a_1 = self.x
        a_2 = self.y
        a_3 = self.z
        b_1 = other.x
        b_2 = other.y
        b_3 = other.z
        dot = (a_1 * b_1) + (a_2 * b_2) + (a_3 * b_3)
        return dot

    def mult(self, magnitude):
        """ multiplies the vector with the magnitude

        :param magnitude: the number to multiply the vector by
        :return: nothing, alters an existing instance of Point
        """
        x = self.x * magnitude
        y = self.y * magnitude
        z = self.z * magnitude
        i = self.length * magnitude
        self.x = x
        self.y = y
        self.z = z
        self.length = i


def zero():
    """ Creates a point with all coordinates set to 0

    :return: Point with 0 for all coordinates
    """
    return Point(0, 0, 0)


def create_point(x, y, z):
    """ Creates a Point with the given coordinates

    :param x: the x coordinate of the point
    :param y: the y coordinate of the point
    :param z: the z coordinate of the point
    :return: A point with corresponding coordinates
    """
    return Point(x, y, z)


def from_angles(azimuth, altitude, length):
    """ constructor for a point using the angles and intensity instead of coordinates

    :param azimuth: the azimuth angle of the vector corresponding to the point
    :param altitude: the altitude angle of the vector corresponding to the point
    :param length: the length of the vector corresponding to the point, i.e. the distance from the point to 0
    :return: a Point with coordinates corresponding to the given angles and intensity
    """
    x = length * (math.cos(math.radians(azimuth)) * math.cos(math.radians(altitude)))
    y = length * (math.sin(math.radians(azimuth)) * math.cos(math.radians(altitude)))
    z = length * (math.sin(math.radians(altitude)))
    return Point(x, y, z)


def create_points(xs, ys, zs):
    """ Create a list of points from three lists of coordinates

    :param xs: the list of x coordinates for all points
    :param ys: the list of y coordinates for all points
    :param zs: the list of z coordinates for all points
    :return: a list of Points corresponding to the coordinates
    """
    iss = np.arange(0, len(xs), 1)
    ps = []
    for i in iss:
        x = xs[i]
        y = ys[i]
        z = zs[i]
        p = Point(x, y, z)
        ps.append(p)
    return ps


def convert_points(ps: list):
    """Converts a list of points to three lists of coordinates.
        Each list corresponds to one coordinate

    :param ps: the list of points to convert to coordinates
    :return: a list that contains three lists, each a list of coordinates corresponding to a single axis
    """
    xs = []
    ys = []
    zs = []
    for p in ps:
        xs.append(p.x)
        ys.append(p.y)
        zs.append(p.z)
    return xs, ys, zs


def rasterize(ps: list, step: int):
    """ Aligns a list of vectors to a grid of angles with a given scale
        i.e. rounds both the azimuth and altitude angles to a certain scale

    :param ps: the list of vectors to align
    :param step: the step scale of the grid, e.g. sample 5 aligns to a grid with distance 5 between each angle
    :return: 
    """
    for p in ps:
        p.round_angles(step)


def update_all(ps: list):
    """ updates the coordinates of a list of points

    :param ps: the points to update
    :return: a list with the updated points, which is the same list as the input
    """
    for p in ps:
        p.update_coordinates()
    return ps


def __round_to_scale(num: float, scale: int):
    """Rounds a number to a certain scale. e.g. scale 10 will round each number to the closest multiple of 10

    :param num: the number to round
    :param scale: the scale to round to
    :return: the number rounded to the given scale
    """
    return scale * round(round(num)/scale)
