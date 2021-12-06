class GeneticAlgorithm:
    def __init__(self, space, fitness_func, pop_size):
        self.space = space
        self.pop_size = pop_size
        self.fitness_func = fitness_func

    def __str__(self):
        return f'space: {self.space}\n' \
               f'population_size: {self.pop_size}\n' \
               f'fitness function: {self.fitness_func}'
