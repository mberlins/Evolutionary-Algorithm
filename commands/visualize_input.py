import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import vals
from vals import InputFunction
from input import create_function, non_linear_objective, create_3D_figure, create_2D_figure


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

    if not isinstance(args.function_num, int):
        parser.error('Input function number should be an integer.')
    elif args.function_num not in vals.ALLOWED_INPUT_FUNCS_NUMS:
        parser.error(f'Incorrect input function number. Allowed numbers are: {vals.ALLOWED_INPUT_FUNCS_NUMS}.')
    if _args.min >= _args.max:
        parser.error("'max' value must be greater than 'min' value.")

    return _args


if __name__ == '__main__':
    args = parse_args()
    if args.function_num == 1:
        _x, _y, _results = create_function(args.min, args.max, args.step, InputFunction.UnimodalFunction1)
        create_3D_figure(_x, _y, _results, 'Unimodal function 1')
        create_2D_figure(_x, _y, _results, 'Unimodal function 1')
    elif args.function_num == 2:
        _x, _y, _results = create_function(args.min, args.max, args.step, InputFunction.UnimodalFunction2)
        create_3D_figure(_x, _y, _results, 'Unimodal function 2')
        create_2D_figure(_x, _y, _results, 'Unimodal function 2')
