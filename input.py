from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import numpy as np
from numpy import e
import random

import exceptions as exc
from vals import InputFunction
import vals


def create_function(_min, _max, step, objective):
    x_axis = np.arange(_min, _max, step)
    y_axis = np.arange(_min, _max, step)
    x, y = np.meshgrid(x_axis, y_axis)
    results = objective(x, y)
    return x, y, results


def save_data_to_file(results):
    file = open(vals.GAUSSIAN_VALUES_FILEPATH, 'w')
    file.write(str(results.shape[0]) + '\n')
    file.write(str(results.shape[1]) + '\n')
    for row in results:
        np.savetxt(file, row)
    file.close()


gaussian = lambda _x, _y, x0, y0, x_alpha, y_alpha, A: A * np.exp(-((_x - x0) / x_alpha) ** 2 -
                                                                  ((_y - y0) / y_alpha) ** 2)


def _gaussian(M, *args):
    x, y = M
    arr = np.zeros(x.shape)
    for i in range(len(args) // 5):
        arr += gaussian(x, y, *args[i * 5:i * 5 + 5])
    return arr


def non_linear_objective(x, y):
    try:
        file = open(vals.GAUSSIAN_VALUES_FILEPATH, 'r')
    except OSError:
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
        results *= -1
        results += 5.8

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

        save_data_to_file(fit)

        return fit

    with file:
        x_dim = int(file.readline())
        y_dim = int(file.readline())

    fit = np.loadtxt(vals.GAUSSIAN_VALUES_FILEPATH, skiprows=2).reshape(x_dim, y_dim)

    return fit


# def unimodal_function1(x, y):
#     result = []
#     for x_el in x:
#         for y_el in y:


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


def create_input(function_num, _min=vals.DEFAULT_RANGE_MIN, _max=vals.DEFAULT_RANGE_MAX, step=vals.DEFAULT_STEP):
    if _min >= _max:
        raise exc.InvalidRangeError
    if function_num == 1:
        _x, _y, _results = create_function(_min, _max, step, InputFunction.UnimodalFunction1)
        create_3D_figure(_x, _y, _results, 'Unimodal function 1')
        create_2D_figure(_x, _y, _results, 'Unimodal function 1')
    elif function_num == 2:
        _x, _y, _results = create_function(_min, _max, step, InputFunction.UnimodalFunction2)
        create_3D_figure(_x, _y, _results, 'Unimodal function 2')
        create_2D_figure(_x, _y, _results, 'Unimodal function 2')
    else:
        raise exc.InputFunctionNumberError(function_num)
