from matplotlib import pyplot as plt
import numpy as np

import exceptions as exc
import vals


def create_function(_min, _max, step, objective):
    x_axis = np.arange(_min, _max, step)
    y_axis = np.arange(_min, _max, step)
    x, y = np.meshgrid(x_axis, y_axis)
    results = objective(x, y)
    return x, y, results


def create_3D_figure(x, y, results, title):
    figure = plt.figure(num=f'{title} - 3D')
    axis = figure.add_subplot(projection='3d')
    axis.plot_surface(x, y, results, cmap='jet')
    plt.show()


def create_2D_figure(x, y, results, title, population, center_point):
    figure = plt.figure(num=f'{title} - 2D')
    axis = figure.add_subplot()
    axis.imshow(results, origin='lower', cmap='jet', extent=(x.min(), x.max(), y.min(), y.max()))
    axis.contour(x, y, results, levels=30, linewidths=1, colors='w')

    individuals_x_coors = []
    individuals_y_coors = []

    for individual in population.individuals:
        individuals_x_coors.append(individual.x)
        individuals_y_coors.append(individual.y)

    plt.scatter(center_point.x, center_point.y, s=24, color='green')
    plt.scatter(individuals_x_coors, individuals_y_coors, s=2, color='red')
    best_individual = population.find_best_individual()
    plt.scatter(best_individual.x, best_individual.y, s=4, color='yellow')
    plt.show()


def create_input(function_num, _min=vals.DEFAULT_SPACE_RANGE_MIN, _max=vals.DEFAULT_SPACE_RANGE_MAX,
                 step=vals.DEFAULT_SPACE_STEP):
    if _min >= _max:
        raise exc.InvalidRangeError
    if function_num in vals.ALLOWED_INPUT_FUNCS_NUMS:
        x, y, results = create_function(_min, _max, step, vals.INPUT_FUNCTIONS[function_num].formula)
        create_3D_figure(x, y, results, vals.INPUT_FUNCTIONS[function_num].name)
        create_2D_figure(x, y, results, vals.INPUT_FUNCTIONS[function_num].name)
    else:
        raise exc.InputFunctionNumberError(function_num)
