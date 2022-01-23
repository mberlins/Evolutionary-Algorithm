import argparse

import vals
from ga.space import Space
from ga.genetic_algorithm import GeneticAlgorithm


def parse_args():
    parser = argparse.ArgumentParser(description='Running genetic algorithm')
    parser.add_argument('function_num', type=int, help=f'A required positional integer - input function number '
                                                       f'(allowed are: {vals.ALLOWED_INPUT_FUNCS_NUMS})')
    parser.add_argument('--pop_size', type=int, default=vals.DEFAULT_POP_SIZE,
                        help='An optional positional positive integer - population size')
    parser.add_argument('--generations_num', type=int, default=vals.DEF_GENERATIONS_NUM,
                        help='An optional positional positive integer - number of generations')
    parser.add_argument('--crossover_prob', type=float, default=vals.DEF_CROSSOVER_PROB,
                        help='An optional positional float in range [0; 1] - crossover probability')
    parser.add_argument('--mutation_prob', type=float, default=vals.DEF_MUTATION_PROB,
                        help='An optional positional float in range [0; 1] - mutation probability')
    parser.add_argument('--exp_val', type=float, default=vals.DEF_EXP_VAL,
                        help='An optional positional float in range [0; 1] - expected value of normal distribution for '
                             'mutation')
    parser.add_argument('--stand_dev', type=float, default=vals.DEF_STAND_DEV,
                        help='An optional positional float - standard deviation of normal distribution for mutation')
    parser.add_argument('--space_min', type=int, default=vals.DEFAULT_SPACE_RANGE_MIN,
                        help='An optional positional integer - minimal value of axes range')
    parser.add_argument('--space_max', type=int, default=vals.DEFAULT_SPACE_RANGE_MAX,
                        help='An optional positional integer - maximal value of axes range')
    parser.add_argument('--space_step', type=float, default=vals.DEFAULT_SPACE_STEP,
                        help='An optional positional float - step of axes')
    parser.add_argument('--init_pop_lower_lim', type=float, default=vals.DEF_INIT_POP_LOWER_LIM,
                        help='An optional positional float - lower limit of initial population coordinates')
    parser.add_argument('--init_pop_upper_lim', type=float, default=vals.DEF_INIT_POP_UPPER_LIM,
                        help='An optional positional float - upper limit of initial population coordinates')
    parser.add_argument('--printing_period', type=int, default=vals.DEF_PRINTING_PERIOD,
                        help='An optional positional integer - number of iterations separating two input visualizations')
    parser.add_argument('--trimmed_mean_coeff', type=float, default=vals.DEF_TRIMMED_MEAN_COEFF,
                        help='An optional positional float - trimmed mean coefficient')
    parser.add_argument('--hubers_metric_coeff', type=float, default=vals.DEF_HUBERS_METRIC_COEFF,
                        help='An optional positional float - hubers metric coefficient')
    parser.add_argument('--mean_worst_part_share', type=float, default=vals.DEF_MEAN_WORST_PART_SHARE,
                        help='An optional positional float - share of individuals rejected in each iteration')
    parser.add_argument('--median_worst_part_share', type=float, default=vals.DEF_MEDIAN_WORST_PART_SHARE,
                        help='An optional positional float - share of individuals rejected in each iteration')

    _args = parser.parse_args()

    if _args.function_num not in vals.ALLOWED_INPUT_FUNCS_NUMS:
        parser.error(f'Incorrect input function number. Allowed numbers are: {vals.ALLOWED_INPUT_FUNCS_NUMS}.')
    if _args.pop_size <= 0:
        parser.error("Population size value must be a positive integer value.")
    if _args.generations_num <= 0:
        parser.error("Number of generations value must be a positive integer value.")
    if _args.mutation_prob < 0 or _args.mutation_prob > 1:
        parser.error("Mutation probability must be a number in range [0; 1].")
    if _args.stand_dev < 0:
        parser.error("Standard deviation of normal distribution must be non-negative.")
    if _args.space_min >= _args.space_max:
        parser.error("'space_max' value must be greater than 'space_min' value.")
    if _args.init_pop_lower_lim < _args.space_min or _args.init_pop_lower_lim >= _args.space_max:
        parser.error("Lower limit of initial population coordinates must be in range ['space_min'; 'space_max').")
    if _args.init_pop_upper_lim > _args.space_max or _args.init_pop_upper_lim <= _args.space_min:
        parser.error("Upper limit of initial population coordinates must be in range ('space_min'; 'space_max'].")
    if _args.printing_period <= 0:
        parser.error("Printing period value must be a positive integer value.")
    if _args.trimmed_mean_coeff <= 0:
        parser.error("Trimmed mean coefficient value must be a positive float value.")
    if _args.hubers_metric_coeff <= 0:
        parser.error("Huber's metric coefficient value must be a positive float value.")
    if _args.mean_worst_part_share <= 0 or _args.mean_worst_part_share > 0.5:
        parser.error("Mean's worst part share must must be within the range of (0, 0.5]")
    if _args.median_worst_part_share <= 0 or _args.median_worst_part_share > 0.5:
        parser.error("Median's worst part share must must be within the range of (0, 0.5]")

    return _args


if __name__ == '__main__':
    args = parse_args()
    # space = Space(args.space_min, args.space_max, args.space_step)
    ga = GeneticAlgorithm(pop_size=args.pop_size,
                          generations_num=args.generations_num,
                          init_pop_lower_lim=args.init_pop_lower_lim,
                          init_pop_upper_lim=args.init_pop_upper_lim,
                          crossover_prob=args.crossover_prob,
                          mutation_prob=args.mutation_prob,
                          expected_val=args.exp_val,
                          stand_dev=args.stand_dev,
                          fitness_func=vals.INPUT_FUNCTIONS[args.function_num].formula)
    ga.run()


