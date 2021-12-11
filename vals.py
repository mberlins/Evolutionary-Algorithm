class InputFunction:
    class UnimodalFunction1:
        formula = lambda x, y: x ** 2 + y ** 2
        name = 'Unimodal function 1'

    class UnimodalFunction2:
        formula = lambda x, y: 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y
        name = 'Unimodal function 2'


GAUSSIAN_VALUES_FILEPATH = 'data/results.txt'
DEFAULT_SPACE_RANGE_MIN = -5
DEFAULT_SPACE_RANGE_MAX = 5
DEFAULT_SPACE_STEP = 0.01
DEFAULT_POP_SIZE = 100
DEF_SELECTION_PROB = 0.8
DEF_MUTATION_PROB = 0.01
DEF_EXP_VAL = 0
DEF_STAND_DEV = 1
DEF_INIT_POP_LOWER_LIM = -4
DEF_INIT_POP_UPPER_LIM = -3
DEF_FITNESS_FUNC_NUM = 1
INPUT_FUNCTIONS = {
    1: InputFunction.UnimodalFunction1,
    2: InputFunction.UnimodalFunction2,
}
ALLOWED_INPUT_FUNCS_NUMS = INPUT_FUNCTIONS.keys()

