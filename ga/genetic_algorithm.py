import numpy as np
from numpy.random import randint
from random import random
from random import gauss, randrange
import numpy.random as npr
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

    def calculate_fitness(self, population):
        for individual in population.individuals:
            individual.fitness = self.fitness_func(individual.x, individual.y)

    # @staticmethod
    # def roulette_choice(population, odds):
    #     pop_copy = [ind.cumulative_sum for ind in population.individuals]
    #     pop_copy.append(odds)
    #     pop_copy.sort()
    #     return pop_copy.index(odds)

    @staticmethod
    def selection(population):
        population.individuals.sort(key=lambda ind: ind.fitness)
        fitness_sum = sum([ind.fitness for ind in population.individuals])
        selection_probs = [ind.fitness / fitness_sum for ind in population.individuals]
        selected = list(npr.choice(population.individuals, size=len(population.individuals)//2, p=selection_probs))
        return selected

        # another solution

        # fitness_sum = sum([ind.fitness for ind in population.individuals])
        # for ind in population.individuals:
        #     ind.normalized_fitness = ind.fitness / fitness_sum
        # population.individuals.sort(key=lambda ind: ind.normalized_fitness)
        # population.individuals[0].cumulative_sum = population.individuals[0].normalized_fitness
        # for i in range(1, len(population.individuals)):
        #     population.individuals[i].cumulative_sum = population.individuals[i-1].cumulative_sum + \
        #                                                population.individuals[i].normalized_fitness
        #
        # selected_idxs = []
        # for x in range(len(population.individuals) // 2):
        #     selected_idxs.append(GeneticAlgorithm.roulette_choice(population, random()))
        # selected = [population.individuals[selected_idx] for selected_idx in selected_idxs]
        # return selected




