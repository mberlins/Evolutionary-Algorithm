import numpy as np
from matplotlib import pyplot as plt
import argparse
import random
from scipy.optimize import curve_fit


def parse_args():
    parser = argparse.ArgumentParser(description='Creating files with input functions')
    parser.add_argument('min', type=int, nargs='?', default=-5, help='A required positional integer - minimal value of'
                                                                     ' axes range')
    parser.add_argument('max', type=int, nargs='?', default=5, help='An optional positional integer - maximal value of'
                                                                    ' axes range')
    parser.add_argument('step', type=float, nargs='?', default=0.01, help='An optional positional float - step of axes')
    _args = parser.parse_args()
    if _args.min >= _args.max:
        parser.error("'max' value must be greater than 'min' value.")
    return _args


def create_function(_min, _max, step, objective):
    x_axis = np.arange(_min, _max, step)
    y_axis = np.arange(_min, _max, step)
    x, y = np.meshgrid(x_axis, y_axis)
    results = objective(x, y)
    return x, y, results


gaussian = lambda _x, _y, x0, y0, x_alpha, y_alpha, A: A * np.exp(-((_x - x0) / x_alpha) ** 2 -
                                                                  ((_y - y0) / y_alpha) ** 2)


def _gaussian(M, *args):
    x, y = M
    arr = np.zeros(x.shape)
    for i in range(len(args) // 5):
        arr += gaussian(x, y, *args[i * 5:i * 5 + 5])
    return arr


def non_linear_objective(x, y):
    gprms = [(0, 2, 2.5, 5.4, 1.5),
             (-1, 4, 6, 2.5, 1.8),
             (-3, -0.5, 1, 2, 4),
             (3, 0.5, 2, 1, 5)
             ]
    noise_sigma = 0.1

    results = np.zeros(x.shape)
    for p in gprms:
        results += gaussian(x, y, *p)
    random.seed(123)
    results += noise_sigma * np.random.randn(*results.shape)
    results *= -6

    guess_prms = [(0, 0, 1, 1, 2),
                  (-1.5, 5, 5, 1, 3),
                  (-4, -1, 1.5, 1.5, 6),
                  (4, 1, 1.5, 1.5, 6.5)
                  ]

    p0 = [p for prms in guess_prms for p in prms]
    xdata = np.vstack((x.ravel(), y.ravel()))
    popt, pcov = curve_fit(_gaussian, xdata, results.ravel(), p0)
    fit = np.zeros(results.shape)
    for i in range(len(popt) // 5):
        fit += gaussian(x, y, *popt[i * 5:i * 5 + 5])
    return fit


def create_3D_figure(x, y, results, title):
    figure = plt.figure(num=f'{title} - 3D')
    axis = figure.add_subplot(projection='3d')
    axis.plot_surface(x, y, results, cmap='jet')
    plt.show()


def create_2D_figure(x, y, results, title):
    figure = plt.figure(num=f'{title} - 2D')
    axis = figure.add_subplot()
    axis.imshow(results, origin='lower', cmap='jet', extent=(x.min(), x.max(), y.min(), y.max()))
    axis.contour(x, y, results, levels=30, linewidths=1, colors='w')
    plt.show()


if __name__ == "__main__":
    args = parse_args()

    # _x, _y, _results = create_function(args.min, args.max, args.step, lambda x, y: x ** 2 + y ** 2)
    # create_3D_figure(_x, _y, _results, 'Unimodal function 1')
    # create_2D_figure(_x, _y, _results, 'Unimodal function 1')
    #
    # _x, _y, _results = create_function(args.min, args.max, args.step, lambda x, y: 0.26 * (x ** 2 + y ** 2) -
    #                                                                                0.48 * x * y)
    # create_3D_figure(_x, _y, _results, 'Unimodal function 2')
    # create_2D_figure(_x, _y, _results, 'Unimodal function 2')

    _x, _y, _results = create_function(args.min, args.max, args.step, non_linear_objective)
    create_3D_figure(_x, _y, _results, 'Multimodal function 1')
    create_2D_figure(_x, _y, _results, 'Multimodal function 1')
