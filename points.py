import numpy as np



class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __lt__(self, other):
        if self.x == other.x and self.y == other.y:
            return self.z < other.z
        elif self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

    def __gt__(self, other):
        if self.x == other.x and self.y == other.y:
            return self.z > other.z
        elif self.x == other.x:
            return self.y > other.y
        else:
            return self.x > other.x

    def __le__(self, other):
        if self.x == other.x and self.y == other.y:
            return self.z <= other.z
        elif self.x == other.x:
            return self.y <= other.y
        else:
            return self.x <= other.x

    def __ge__(self, other):
        if self.x == other.x and self.y == other.y:
            return self.z >= other.z
        elif self.x == other.x:
            return self.y >= other.y
        else:
            return self.x >= other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

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
        x = p.x
        y = p.y
        new_x = __round_to_scale(x, step)
        new_y = __round_to_scale(y, step)
        p.x = new_x
        p.y = new_y


def __round_to_scale(num: float, scale: int):
    """Rounds a number to a certain scale. e.g. scale 10 will round each number to the closest multiple of 10

    :param num: the number to round
    :param scale: the scale to round to
    :return: the number rounded to the given scale
    """
    half = scale/2
    div = num // scale
    if num % scale >= half:
        return (div + 1) * scale
    else:
        return div*scale




