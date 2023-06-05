# This is a sample Python script.

import matplotlib as mpl
import numpy
import numpy as np
import matplotlib.pyplot as plt
import points
import revolutions as rev

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


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
    currently creates and plots a solid of revolution of simple curve around center axis
    -------------------------------------------------------------------------------------
    """

    """
    x,y,z data for all points on in-plane BRDF
    """
    # example data, single curve
    # x = np.arange(-90, 95, 5)
    # y = np.zeros(len(x))
    # z = (np.cos((x/30))+1)/2

    # example data for two sub-curves
    x_1 = np.arange(-90, -10, 5)
    x_2 = np.arange(-10, 95, 5)
    y_1 = np.zeros(len(x_1))
    y_2 = np.zeros(len(x_2))
    z_1 = (-1 * ((x_1+45)**2))
    z_1 = squash(z_1)
    z_2 = (-1 * (x_2**2))
    z_2 = squash(z_2)/2
    x = [*x_1, *x_2]
    y = [*y_1, *y_2]
    z = [*z_1, *z_2]

    # example data for three sub-curves
    # x_1 = np.arange(-90, -30, 5)
    # x_2 = np.arange(-30, 35, 5)
    # x_3 = np.arange(35, 95, 5)
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
    # ps = points.create_points(x, y, z)

    # points for two sub-curves
    ps_1 = points.create_points(x_1, y_1, z_1)
    ps_2 = points.create_points(x_2, y_2, z_2)
    p = ps_1 + ps_2
    p.sort()
    ps = rev.sub_curves_naive(p)

    # points for three sub-curves
    # ps_1 = points.create_points(x_1, y_1, z_1)
    # print(len(x_2), len(y_2), len(z_2))
    # ps_2 = points.create_points(x_2, y_2, z_2)
    # ps_3 = points.create_points(x_3, y_3, z_3)
    # p = ps_1 + ps_2 + ps_3
    # p.sort()
    # ps = rev.sub_curves_naive(p)

    # create solid of revolution for all points around axis
    # px = rev.revolve_all(ps, 100)
    # revolve sub-curves
    # px_1 = rev.revolve_all(ps_1, 1000)
    # px_2 = rev.revolve_all(ps_2, 1000)
    px = rev.revolve_list(ps, 1000)
    points.rasterize(px, 5)

    # turn solid of revolution into plotable data
    px = rev.remove_overlap_simple(px)
    abc = points.convert_points(px)
    a = abc[0]
    b = abc[1]
    c = abc[2]

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlim(-90, 90)
    ax.set_ylim(-90, 90)
    ax.set_zlim(0, 1)
    ax.scatter(x, y, z)

    # noinspection PyRedeclaration
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlim(-90, 90)
    ax.set_ylim(-90, 90)
    ax.set_zlim(0, 1)
    ax.scatter(a, b, c)

    # show all plots
    plt.show()

    """
    templates for creating plots
    """
    # create scatter-plot from data, uses 3 arrays of numbers of equal length
    # transforms an array of arrays into a single array
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # # ax.scatter(xs, ys, zs)
    # ax.scatter(X, Y, Z)

    # create surface plot from data, uses 3 2-dimensional arrays of numbers of equal sizes
    # noinspection PyRedeclaration
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(X, Y, Z, vmin=Z.min() * 2, cmap=mpl.cm.Blues)
