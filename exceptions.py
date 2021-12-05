import vals


class InputFunctionNumberError(Exception):
    def __init__(self, function_num):
        if not isinstance(function_num, int):
            self.message = 'Input function number should be an integer.'
        elif function_num not in vals.ALLOWED_INPUT_FUNCS_NUMS:
            self.message = f'Incorrect input function number. Allowed numbers are: {vals.ALLOWED_INPUT_FUNCS_NUMS}.'

    def __str__(self):
        return self.message


class InvalidRangeError(Exception):
    def __init__(self):
        self.message = 'Maximal range value must be greater than minimal range value.'

    def __str__(self):
        return self.message
