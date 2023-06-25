# This is a sample Python script.

import matplotlib as mpl
from mpl_toolkits.axisartist.axislines import AxesZero
from matplotlib import cm
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


def printer(pt: list):
    for t in pt:
        if isinstance(t, list):
            printer(t)
        elif isinstance(t, points.Point):
            print(t)


def cp(pt: list):
    pc = []
    for t in pt:
        pc.append(t)
    return pc


def count(pt: list):
    s = 0
    prev = None
    for t in pt:
        if prev is None:
            prev = t
            s += 1
        elif prev != t:
            prev = t
            s += 1
    return s


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

    cmp = cm.plasma

    """
    -------------------------------------------------------------------------------------
    main bulk of code
    -------------------------------------------------------------------------------------
    """

    """
    
    all points that represent the in-plane BRDF
    
    """
    # example data, diffuse
    # f = np.arange(0, 190, 10)
    # x = []
    # z = []
    # for p in f:
    #     xf = math.cos(math.radians(p)) * 50
    #     zf = math.sin(math.radians(p)) * 50
    #     x.append(xf)
    #     z.append(zf)
    # y = np.zeros(len(x))
    x = np.arange(0, 2 * np.pi, (2* np.pi)/19)

    # example data, diffuse shifted
    # f = np.arange(0, 190, 10)
    # x = []
    # z = []
    # for p in f:
    #     xf = 10 + math.cos(math.radians(p)) * 50
    #     zf = math.sin(math.radians(p)) * 50
    #     x.append(xf)
    #     z.append(zf)
    # y = np.zeros(len(x))

    # example data for two sub-curves, diffuse and specular
    # f_1 = np.arange(0, 110, 10)
    # f_2 = np.arange(170, 190, 10)
    # f = np.concatenate([f_1, f_2])
    # x_1 = []
    # z_1 = []
    # for p in f:
    #     xf = math.cos(math.radians(p)) * 40
    #     zf = math.sin(math.radians(p)) * 40
    #     x_1.append(xf)
    #     z_1.append(zf)
    # y_1 = np.zeros(len(x_1))
    #
    # f_3 = np.arange(110, 170, 10)
    # x_2 = []
    # z_2 = []
    # for p in f_3:
    #     s = 75 - abs(135 - p)
    #     xf = math.cos(math.radians(p)) * s
    #     zf = math.sin(math.radians(p)) * s
    #     x_2.append(xf)
    #     z_2.append(zf)
    # y_2 = np.zeros(len(x_2))
    #
    # x = np.concatenate([x_1, x_2])
    # y = np.concatenate([y_1, y_2])
    # z = np.concatenate([z_1, z_2])

    # example data for one curve, specular
    # x = [1, 4.98, 9.8, 16.9, 23.5, 29.45, 34.8, 40.96, 46.2, 47.0, 38.4, 28.68, 20, 13.74, 8.5, 4.53, 1.7, 0.44, 0]
    # y = np.zeros(len(x))
    # z = [0, 0.44, 1.7, 4.53, 8.5, 13.74, 20, 28.68, 38.4, 47.0, 46.2, 40.96, 34.8, 29.45, 23.5, 16.9, 9.8, 4.98, 1]

    # example data for two specular lobes
    # x_1 = [-1.00, -9.96, -19.70, -28.98, -37.60, -45.30, -45.03, -40.95, -30.64, -21.21, -12.86, -5.74, -0.50]
    # y_1 = np.zeros(len(x_1))
    # z_1 = [0.00, 0.87, 3.48, 7.77, 13.68, 21.15, 26.00, 28.70, 25.72, 21.21, 15.32, 8.19, 0.87]
    #
    # x_2 = [1, 4.98, 9.8, 16.9, 23.5, 29.45, 34.8, 40.96, 46.2, 47.0, 38.4, 28.68, 20, 13.74, 8.5, 4.53, 1.7, 0.44, 0]
    # y_2 = np.zeros(len(x_2))
    # z_2 = [0, 0.44, 1.7, 4.53, 8.5, 13.74, 20, 28.68, 38.4, 47.0, 46.2, 40.96, 34.8, 29.45, 23.5, 16.9, 9.8, 4.98, 1]
    #
    # x = np.concatenate([x_1, x_2])
    # y = np.concatenate([y_1, y_2])
    # z = np.concatenate([z_1, z_2])

    # example data for diffuse with two specular lobes
    # x_1 = [-1.00, -9.96, -19.70, -28.98, -37.60, -45.30, -45.03, -40.95, -30.64, -21.21, -12.86, -5.74, -0.50]
    # y_1 = np.zeros(len(x_1))
    # z_1 = [0.00, 0.87, 3.48, 7.77, 13.68, 21.15, 26.00, 28.70, 25.72, 21.21, 15.32, 8.19, 0.87]
    #
    # x_2 = [1, 4.98, 9.8, 16.9, 23.5, 29.45, 34.8, 40.96, 46.2, 47.0, 38.4, 28.68, 20, 13.74, 8.5, 4.53, 1.7, 0.44, 0]
    # y_2 = np.zeros(len(x_2))
    # z_2 = [0, 0.44, 1.7, 4.53, 8.5, 13.74, 20, 28.68, 38.4, 47.0, 46.2, 40.96, 34.8, 29.45, 23.5, 16.9, 9.8, 4.98, 1]
    #
    # f = np.arange(0, 190, 10)
    # x_3 = []
    # z_3 = []
    # for p in f:
    #     xf = math.cos(math.radians(p)) * 40
    #     zf = math.sin(math.radians(p)) * 40
    #     x_3.append(xf)
    #     z_3.append(zf)
    # y_3 = np.zeros(len(x_3))
    #
    # f_1 = np.concatenate([np.arange(0, 40, 10), np.arange(60, 150, 10), np.arange(160, 190, 10)])
    # fx = []
    # fz = []
    # for p in f_1:
    #     xf = math.cos(math.radians(p)) * 40
    #     zf = math.sin(math.radians(p)) * 40
    #     fx.append(xf)
    #     fz.append(zf)
    #
    # x = np.concatenate([fx, [-45.30, -45.06, -40.95], [40.96, 46.2, 47.0, 38.4, 28.68]])
    # z = np.concatenate([fz, [21.15, 26.00, 28.], [28.68, 38.4, 47.0, 46.2, 40.96]])

    """
    
    create points for each point in data
    
    """
    # points for single curve
    # ps = points.create_points(x, y, z)

    # points for two sub-curves
    ps_1 = points.create_points(x_1, y_1, z_1)
    ps_2 = points.create_points(x_2, y_2, z_2)
    ps_3 = points.create_points(x_3, y_3, z_3)
    ps = numpy.concatenate([ps_1, ps_2, ps_3])

    """
    
    create solid of revolution for all sub-curves
    
    """
    # create solid for one sub-curve
    # axis = points.create_point(0, 0, 1)
    # axis = points.create_point(1/np.sqrt(2), 0, 1/np.sqrt(2))
    # px = rev.revolve_all_axis(ps, axis, 0, 72)

    # create solids for two sub-curves
    # axis_1 = points.create_point(0, 0, 1)
    # axis_2 = points.create_point(1 / np.sqrt(2), 0, 1 / np.sqrt(2))
    # px_1 = rev.revolve_all_axis(ps_1, axis_1, 0, 72)
    # px_2 = rev.revolve_all_axis(ps_2, axis_2, 0, 72)
    # px = px_1 + px_2

    # create solids for three sub-curves
    axis_1 = points.create_point(-0.866, 0, 0.5)
    axis_2 = points.create_point(1/np.sqrt(2), 0, 1/np.sqrt(2))
    axis_3 = points.create_point(0, 0, 1)
    px_1 = rev.revolve_all_axis(ps_1, axis_1, 0, 72)
    px_2 = rev.revolve_all_axis(ps_2, axis_2, 0, 72)
    px_3 = rev.revolve_all_axis(ps_3, axis_3, 0, 72)
    px = px_1 + px_2 + px_3

    """
    
    remove excess data
    
    the scale used in rasterize should be at least 360 divided by the scale of the revolution
    a smaller scale will lead to gaps in the data
    
    """
    points.rasterize(px, 10)
    px = points.update_all(px)
    px.sort()

    px = rev.remove_overlap_angular(px)
    px = points.update_all(px)
    px = rev.fill_domain(px, 10)

    """
    
    plot the data
    
    """

    # turn solid of revolution into plot-able data for simple data
    # abc = points.convert_points(px)
    # a = abc[0]
    # b = abc[1]
    # c = abc[2]

    # turn solid of revolution into plot-able data for complex data
    abc = points.convert_points(px)
    ap = abc[0]
    print(len(ap))
    a = []
    q = 37
    for i in range(0, len(ap), q):
        a.append(ap[i:i + q])
    a = np.array(a)
    bp = abc[1]
    b = []
    for i in range(0, len(ap), q):
        b.append(bp[i:i + q])
    b = np.array(b)
    cp = abc[2]
    c = []
    for i in range(0, len(ap), q):
        c.append(cp[i:i + q])
    c = np.array(c)


    # create a scatter plot of the input data
    fig = plt.figure()
    ax = fig.add_subplot(axes_class=AxesZero)
    for direction in ["xzero", "yzero"]:
        # adds X and Y-axis from the origin
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        # hides borders
        ax.axis[direction].set_visible(False)

    ax.set_xlim(-60, 60)
    # ax.set_ylim(-60, 60)
    ax.set_ylim(-20, 100)
    ax.set_aspect('equal', adjustable='box')
    ax.scatter(x, z, c="red")

    # disable axis numbers
    plt.xticks([])
    plt.yticks([])

    # create a surface plot of the resulting data
    # noinspection PyRedeclaration
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.set_zlim(0, 120)
    ax.set_aspect('equal', adjustable='box')

    ax.plot_surface(a, b, c, cmap=cmp)  # create surface plot for complex data
    # ax.plot_trisurf(a, b, c, cmap=cmp, alpha=1) # create surface plot for simple data
    # ax.scatter(a, b, c, c="red")

    # remove axis numbers
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.axes.zaxis.set_ticklabels([])

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
