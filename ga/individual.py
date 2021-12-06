import sys


class Individual:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fitness = sys.maxsize
        self.normalized_fitness = sys.maxsize
        self.cumulative_sum = sys.maxsize

    def __str__(self):
        return f'Individual on '.ljust(17) + \
               f'({self.x} {self.y}): '.ljust(50) + \
               f'fitness = '.ljust(12) + \
               f'{self.fitness}'.ljust(30) + \
               f'norm. fitness = '.ljust(18) + \
               f'{self.normalized_fitness}'.ljust(30) + \
               f'cum. sum = '.ljust(13) + \
               f'{self.cumulative_sum}'
