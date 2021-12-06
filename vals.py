from enum import Enum

GAUSSIAN_VALUES_FILEPATH = 'data/results.txt'
ALLOWED_INPUT_FUNCS_NUMS = (1, 2)
DEFAULT_RANGE_MIN = -5
DEFAULT_RANGE_MAX = 5
DEFAULT_STEP = 0.01


class InputFunction(Enum):
    UnimodalFunction1 = lambda x, y: x ** 2 + y ** 2
    UnimodalFunction2 = lambda x, y: 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y
