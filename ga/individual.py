import sys


class Individual:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fitness = sys.maxsize

    def __str__(self):
        return f'Individual on '.ljust(17) + \
               f'({self.x} {self.y}): '.ljust(50) + \
               f'fitness = '.ljust(12) + \
               f'{self.fitness}'
