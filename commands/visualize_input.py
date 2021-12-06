import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import vals
from input import create_function, create_3D_figure, create_2D_figure


def parse_args():
    parser = argparse.ArgumentParser(description='Creating files with input functions')
    parser.add_argument('function_num', type=int, help=f'A required positional integer - input function number '
                                                       f'(allowed are: {vals.ALLOWED_INPUT_FUNCS_NUMS})')
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

    return _args


if __name__ == '__main__':
    args = parse_args()
    x, y, results = create_function(args.min, args.max, args.step, vals.INPUT_FUNCTIONS[args.function_num].formula)
    create_3D_figure(x, y, results, vals.INPUT_FUNCTIONS[args.function_num].name)
    create_2D_figure(x, y, results, vals.INPUT_FUNCTIONS[args.function_num].name)
