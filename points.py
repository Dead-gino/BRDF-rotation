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
        # return f"(x: {self.x}, y: {self.y}, z: {self.z}, " \
        #        f"azimuth: {self.azimuth}, altitude: {self.altitude}, intensity: {self.length})"
        return f"(azimuth: {self.azimuth}, altitude: {self.altitude}"

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
        if self.altitude == 90:
            return 0
        x = self.x
        y = self.y
        theta = math.degrees(math.atan2(y, x))
        return theta

    def angle_vertical(self):
        l = self.intensity()
        z = self.z
        phi = math.degrees(math.asin(z/l))
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
        alti = self.altitude
        length = self.length
        y = length * (math.sin(math.radians(azi)) * math.cos(math.radians(alti)))
        x = length * (math.cos(math.radians(azi)) * math.cos(math.radians(alti)))
        z = length * (math.sin(math.radians(alti)))
        self.x = x
        self.y = y
        self.z = z

    def update_angles(self):
        self.azimuth = self.angle_horizontal()
        self.altitude = self.angle_vertical()
        self.length = self.intensity()

    def round_angles(self, scale):
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
        self.x += dx
        self.y += dy
        self.z += dz
        self.update_angles()


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
    return [xs, ys, zs]


def rasterize(ps: list, step: int):
    """ Aligns a list of points to a grid of a given step scale

    :param ps: the list of points to align to grid
    :param step: the step scale of the grid, e.g. sample 5 aligns to a grid with distance 5 between each point
    :return: 
    """
    for p in ps:
        # phi_h = p.phi_h
        # phi_v = p.phi_v
        # new_v = __round_to_scale(phi_v, step)
        # if new_v == 90:
        #     new_h = 0
        # else:
        #     new_h = __round_to_scale(phi_h, step)
        #
        # if new_h == -180:
        #     new_h = 180
        # # print(f"from {p.phi_h} to {new_h}, and from {p.phi_v} to {new_v}")
        # p.phi_h = new_h
        # p.phi_v = new_v
        #
        # if p.azimuth % step != 0:
        #     p.azimuth = __round_to_scale(p.azimuth, step)
        # else:
        #     p.azimuth = round(p.azimuth)
        # if p.altitude % step != 0:
        #     p.altitude = __round_to_scale(p.altitude, step)
        # else:
        #     p.altitude = round(p.altitude)
        #
        # if p.altitude == 90:  # points straight up, so azimuth does not matter; set azimuth to 0 for uniformity
        #     p.azimuth = 0
        #
        # if p.azimuth == -180:  # azimuth -180 is equal to azimuth 180, both are 180 degrees away from azimuth 0
        #     p.azimuth = 180
        #
        # p.update_coordinates()
        p.round_angles(step)
        True


def update_all(ps: list):
    for p in ps:
        p.update_coordinates()
    return ps


def __round_to_scale(num: float, scale: int):
    """Rounds a number to a certain scale. e.g. scale 10 will round each number to the closest multiple of 10

    :param num: the number to round
    :param scale: the scale to round to
    :return: the number rounded to the given scale
    """
    # half = scale/2
    # div = num // scale
    # if num % scale >= half:
    #     return (div + 1) * scale
    # else:
    #     return div*scale
    return scale * round(round(num)/scale)


def test_data():
    x = np.arange(-100,105,5)
    y = np.zeros(len(x))
    z = (((-1 * (x**2))/100)+100)
    p = create_points(x, y, z)
    p.sort()
    return p

