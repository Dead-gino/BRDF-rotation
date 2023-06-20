# This is a sample Python script.

import matplotlib as mpl
import numpy
import numpy as np
import matplotlib.pyplot as plt
import points
import revolutions as rev
import math

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def printer(ps: list):
    for p in ps:
        if isinstance(p, list):
            printer(p)
        elif isinstance(p, points.Point):
            print(p)


def cp(ps: list):
    pc = []
    for p in ps:
        pc.append(p)
    return pc


def coun(ps: list):
    x = 0
    prev = None
    for p in ps:
        if prev is None:
            prev = p
            x += 1
        elif prev != p:
            prev = p
            x += 1
    return x


def squash(nums):
    if isinstance(nums, numpy.ndarray):
        min_n = abs(min(nums))
        new_nums = (nums/min_n)+1
        return new_nums
    else:
        raise TypeError


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # make use of interactive, pop-out view for plots
    mpl.use('TkAgg')

    # set the style of the plot
    # find styles in https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
    plt.style.use('dark_background')

    """
    -------------------------------------------------------------------------------------
    main bulk of code
    -------------------------------------------------------------------------------------
    """

    """
    
    all points that represent the in-plane BRDF
    
    """
    # example data, single curve
    # f = np.arange(0, 190, 10)
    # x = []
    # z = []
    # for p in f:
    #     xf = math.cos(math.radians(p)) * 100
    #     zf = math.sin(math.radians(p)) * 100
    #     x.append(xf)
    #     z.append(zf)
    # y = np.zeros(len(x))

    # example data for two sub-curves
    f_1 = np.arange(0, 110, 10)
    f_2 = np.arange(170, 190, 10)
    f = np.concatenate([f_1, f_2])
    x_1 = []
    z_1 = []
    for p in f:
        xf = math.cos(math.radians(p)) * 40
        zf = math.sin(math.radians(p)) * 40
        x_1.append(xf)
        z_1.append(zf)
    y_1 = np.zeros(len(x_1))

    f_3 = np.arange(110, 170, 10)
    x_2 = []
    z_2 = []
    for p in f_3:
        s = 75 - abs(135 - p)
        xf = math.cos(math.radians(p)) * s
        zf = math.sin(math.radians(p)) * s
        x_2.append(xf)
        z_2.append(zf)
    y_2 = np.zeros(len(x_2))

    x = np.concatenate([x_1, x_2])
    y = np.concatenate([y_1, y_2])
    z = np.concatenate([z_1, z_2])

    # example data for three sub-curves
    # x_1 = np.arange(-100, -50, 5) #14
    # x_2 = np.arange(-50, 35, 5) #15
    # x_3 = np.arange(35, 105, 5) #14
    # y_1 = np.zeros(len(x_1))
    # y_2 = np.zeros(len(x_2))
    # y_3 = np.zeros(len(x_3))
    # z_1 = (-1 * ((x_1+60)**2))
    # z_1 = squash(z_1)
    # z_2 = (-1 * (x_2**2))
    # z_2 = squash(z_2)
    # z_3 = (-1 * ((x_3-60)**2))
    # z_3 = squash(z_3)
    # x = [*x_1, *x_2, *x_3]
    # y = [*y_1, *y_2, *y_3]
    # z = [*z_1, *z_2, *z_3]

    """
    
    create points for each point in data
    
    """
    # points for single curve
    # ps = [points.create_points(x, y, z)]

    # points for two sub-curves
    ps_1 = points.create_points(x_1, y_1, z_1)
    ps_2 = points.create_points(x_2, y_2, z_2)
    # ps = numpy.concatenate([ps_1, ps_2])
    # ps.sort()
    # ps = rev.sub_curves_naive(ps)

    # points for three sub-curves
    # ps_1 = points.create_points(x_1, y_1, z_1)
    # ps_2 = points.create_points(x_2, y_2, z_2)
    # ps_3 = points.create_points(x_3, y_3, z_3)
    # p = ps_1 + ps_2 + ps_3
    # p.sort()
    # ps = rev.sub_curves_naive(p)

    """
    
    create solid of revolution for all sub-curves
    
    """
    # px = rev.revolve_all(ps, 100)
    # revolve sub-curves
    # px_1 = rev.revolve_all(ps_1, 1000)
    # px_2 = rev.revolve_all(ps_2, 1000)
    # px = px_1 + px_2
    axis_1 = points.create_point(0, 0, 1)
    axis_2 = points.create_point(-1/np.sqrt(2), 0, 1/np.sqrt(2))
    px_1 = rev.revolve_all_axis(ps_1, axis_1, 0, 72)
    px_2 = rev.revolve_all_axis(ps_2, axis_2, 0, 72)
    px = px_1 + px_2
    px.sort()

    """
    
    remove excess data
    
    the scale used in rasterize should be at least 360 divided by the scale of the revolution
    a smaller scale will lead to gaps in the data
    
    """
    points.rasterize(px, 10)
    px = points.update_all(px)
    px.sort()

    px = rev.remove_overlap_angular(px)
    # px = points.update_all(px)

    """
    
    plot the data
    
    """

    # turn solid of revolution into plotable data
    abc = points.convert_points(px)
    a = abc[0]
    b = abc[1]
    c = abc[2]

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.set_zlim(0, 60)
    ax.scatter(x, y, z, c="red")

    # noinspection PyRedeclaration
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.set_zlim(0, 60)
    ax.scatter(a, b, c, c="red")

    # show all plots
    plt.show()

    """
    templates for creating plots

    create scatter-plot from data, uses 3 arrays of numbers of equal length:
    transforms an array of arrays into a single array
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.scatter(xs, ys, zs)

    create surface plot from data, uses 3 2-dimensional arrays of numbers of equal sizes
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.plot_surface(X, Y, Z, vmin=Z.min() * 2, cmap=mpl.cm.Blues)
    """
