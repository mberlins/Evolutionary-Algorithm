import argparse

import vals
from ga.genetic_algorithm import GeneticAlgorithm
from ga.space import Space


def parse_args():
    parser = argparse.ArgumentParser(description='Running genetic algorithm')
    parser.add_argument('function_num', type=int, help=f'A required positional integer - input function number '
                                                       f'(allowed are: {vals.ALLOWED_INPUT_FUNCS_NUMS})')
    parser.add_argument('pop_size', type=int, nargs='?', default=vals.DEFAULT_POP_SIZE, help='A required positional '
                                                                                             'positive integer - '
                                                                                             'population size')
    parser.add_argument('min', type=int, nargs='?', default=vals.DEFAULT_RANGE_MIN, help='A required positional integer'
                                                                                         ' - minimal value of axes '
                                                                                         'range')
    parser.add_argument('max', type=int, nargs='?', default=vals.DEFAULT_RANGE_MAX, help='An optional positional '
                                                                                         'integer - maximal value of '
                                                                                         'axes range')
    parser.add_argument('step', type=float, nargs='?', default=vals.DEFAULT_STEP, help='An optional positional float - '
                                                                                       'step of axes')
    _args = parser.parse_args()

    if not isinstance(_args.function_num, int):
        parser.error('Input function number should be an integer.')
    elif _args.function_num not in vals.ALLOWED_INPUT_FUNCS_NUMS:
        parser.error(f'Incorrect input function number. Allowed numbers are: {vals.ALLOWED_INPUT_FUNCS_NUMS}.')
    if _args.min >= _args.max:
        parser.error("'max' value must be greater than 'min' value.")
    if _args.pop_size <= 0 or not isinstance(_args.pop_size, int):
        parser.error("Population size value must be a positive integer value")

    return _args


if __name__ == '__main__':
    args = parse_args()
    space = Space(args.min, args.max, args.step)
    ga = GeneticAlgorithm(space=space,
                          fitness_func=vals.INPUT_FUNCTIONS[args.function_num].formula,
                          pop_size=args.pop_size)
    population = ga.init_population()
    ga.calculate_fitness(population)
    ga.selection(population)


