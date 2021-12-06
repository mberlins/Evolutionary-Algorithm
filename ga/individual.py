import sys


class Individual:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fitness = sys.maxsize

    def __str__(self):
        return f'Individual on ({self.x}; {self.y})'
