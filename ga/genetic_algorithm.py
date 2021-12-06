import numpy as np
from numpy.random import randint
from random import random
from random import gauss, randrange
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import vals
from ga.individual import Individual
from ga.population import Population


class GeneticAlgorithm:
    def __init__(self, space, fitness_func, pop_size):
        self.space = space
        self.pop_size = pop_size
        self.fitness_func = fitness_func

    def __str__(self):
        return f'space: {self.space}\n' \
               f'population_size: {self.pop_size}\n' \
               f'fitness function: {self.fitness_func}'

    @staticmethod
    def create_individual(lower_limit=vals.DEF_INIT_POP_LOWER_LIM, upper_limit=vals.DEF_INIT_POP_UPPER_LIM):
        ind_coords = [random()*(upper_limit - lower_limit) + lower_limit for _ in range(2)]
        return Individual(ind_coords[0], ind_coords[1])

    @staticmethod
    def init_population(pop_size=vals.DEFAULT_POP_SIZE, lower_limit=vals.DEF_INIT_POP_LOWER_LIM,
                        upper_limit=vals.DEF_INIT_POP_UPPER_LIM):
        individuals = [GeneticAlgorithm.create_individual(lower_limit, upper_limit) for _ in range(pop_size)]
        return Population(individuals)


