from numpy import arange
from numpy import meshgrid
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Creating files with input functions')
    parser.add_argument('min', type=int, nargs='?', default=-50, help='A required integer positional minimal value of '
                                                                      'axes range')
    parser.add_argument('max', type=int, nargs='?', default=50, help='An optional integer positional maximal value of '
                                                                     'axes range')
    args = parser.parse_args()
    if args.min >= args.max:
        parser.error("'max' value must be greater than 'min' value.")
    return args


def create_unim_func1(_min, _max):
    x_axis = arange(_min, _max + 1, 1)
    y_axis = arange(_min, _max + 1, 1)
    objective = lambda a, b: a ** 2 + b ** 2
    x, y = meshgrid(x_axis, y_axis)
    results = objective(x, y)
    return x, y, results


def create_3D_figure(x, y, results, title):
    figure = plt.figure(num=f'{title} - 3D')
    axis = figure.gca(projection='3d')
    axis.plot_surface(x, y, results, cmap='jet')
    plt.show()


def create_2D_figure(x, y, results, title):
    figure = plt.figure(num=f'{title} - 2D')
    axis = figure.add_subplot()
    axis.imshow(results, origin='lower', cmap='jet', extent=(x.min(), x.max(), y.min(), y.max()))
    axis.contour(x, y, results, colors='w')
    plt.show()


if __name__ == "__main__":
    args = parse_args()

    _x, _y, _results = create_unim_func1(args.min, args.max)
    create_3D_figure(_x, _y, _results, 'Unimodal function 1')
    create_2D_figure(_x, _y, _results, 'Unimodal function 1')
